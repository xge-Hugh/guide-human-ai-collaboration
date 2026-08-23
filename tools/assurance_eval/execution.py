"""Execute an immutable resolved plan and preserve mechanical evidence."""

from __future__ import annotations

import json
import os
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from .artifacts import contains_private_value, scan_private_values, tree_sha256, write_new_json
from .config import ModelCatalog
from .experiment import Experiment, loads_exact
from .grading import build_grader_packet, parse_grade
from .models import ProviderError, ResolvedProvider, Transport
from .planning import public_roles, verify_resolved_plan
from .policy import NetworkGate, git_provenance, validate_private_output
from .renderers import get_renderer
from .retry import DEFAULT_BACKOFF_SECONDS, DEFAULT_MAX_ATTEMPTS, classify_retryability, invoke_logical_call
from .semantics import (
    capture_treatment_content, execution_policy_report, require_compatible_treatment,
)
from .transport import OpenAIChatCompletionsProvider, urllib_transport


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _provider_identity(provider: OpenAIChatCompletionsProvider) -> dict[str, Any]:
    assignment = provider.assignment
    return {
        "provider": assignment.provider,
        "configured_model": assignment.model,
        "model_family": assignment.family,
        "declared_model_snapshot": assignment.declared_snapshot,
        "parameters": dict(assignment.parameters),
        "context_mode": "standalone",
    }


def _record_stem(scheduled: Mapping[str, Any]) -> str:
    return f"{scheduled['case_id']}__{scheduled['variant_id']}__r{scheduled['repetition']:03d}"


def _execution_policy(plan: Mapping[str, Any]) -> dict[str, Any]:
    policy = dict(plan.get("execution_policy") or {})
    if policy.get("automatic_retries", 0) == 0:
        return {
            "max_attempts": 1,
            "backoff_seconds": (),
            "grader_parallelism": 1,
            "decoupled_stages": False,
        }
    return {
        "max_attempts": int(policy.get("max_attempts_per_logical_call", DEFAULT_MAX_ATTEMPTS)),
        "backoff_seconds": tuple(policy.get("retry_backoff_seconds", DEFAULT_BACKOFF_SECONDS)),
        "grader_parallelism": int(policy.get("grader_parallelism", 1)),
        "decoupled_stages": bool(policy.get("decoupled_stages", True)),
    }


def _verify_captured_binding(
    *, repo_root: Path, envelope: Mapping[str, Any], experiment: Experiment,
    resolved: Mapping[str, ResolvedProvider],
) -> None:
    plan = envelope["plan"]
    if experiment.recipe_sha256 != plan["recipe"]["sha256"] or experiment.sources != plan["sources"]:
        raise ValueError("captured experiment differs from the resolved plan")
    expected_content = capture_treatment_content(
        plan, experiment.generation, experiment.variants, experiment.rubrics
    )
    if plan.get("treatment_content_snapshot") not in (None, expected_content):
        raise ValueError("captured treatment content differs from the resolved plan")
    if public_roles(resolved, envelope) != plan["roles"]:
        raise ValueError("captured model assignments differ from the resolved plan")
    recipe = experiment.recipe
    expected_order: list[dict[str, Any]] = []
    tranches = recipe["schedule"].get("operational_tranches") or {}
    tranche_by_repetition = {
        repetition: tranche_id
        for tranche_id, value in tranches.items()
        if tranche_id.startswith("tranche_") and isinstance(value, Mapping)
        for repetition in value.get("repetitions", [])
    }
    for repetition, order in enumerate(recipe["schedule"]["variant_order_by_repetition"], start=1):
        for case_id in recipe["selection"]["cases"]:
            for position, variant_id in enumerate(order, start=1):
                expected_order.append({
                    "execution_index": len(expected_order) + 1,
                    "repetition": repetition,
                    "case_id": case_id,
                    "variant_id": variant_id,
                    "variant_position": position,
                    "tranche_id": tranche_by_repetition.get(repetition),
                })
    if (
        plan["formal_execution_enabled"] != recipe["formal_execution_enabled"]
        or plan["selection"] != recipe["selection"]
        or plan["instructions"] != recipe["instructions"]
        or plan["timeouts_seconds"] != recipe["timeouts_seconds"]
        or plan["grading"] != recipe["grading"]
        or any(
            plan["roles"][role]["parameters"] != recipe["parameters"][role]
            or plan["roles"][role]["renderer"]["id"] != recipe["renderers"][role]
            for role in ("generator", "grader")
        )
        or plan["schedule"]["repetitions"] != recipe["schedule"]["repetitions"]
        or plan["schedule"]["variant_order_by_repetition"] != recipe["schedule"]["variant_order_by_repetition"]
        or plan["schedule"]["operational_tranches"] != recipe["schedule"].get("operational_tranches")
        or plan["schedule"]["execution_order"] != expected_order
    ):
        raise ValueError("resolved plan is not the canonical projection of the captured experiment")
    if plan["mode"] == "formal":
        current = git_provenance(repo_root)
        frozen = plan["provenance"]
        if (
            not current["available"] or not current["clean"]
            or current["git_revision"] != frozen["git_revision"]
            or current["harness_source_sha256"] != frozen["harness_source_sha256"]
        ):
            raise ValueError("formal execution requires the resolved clean committed provenance")


def _load_prior_episode_state(prior_run: Path) -> dict[str, Any]:
    from .reporting import load_report

    prior_report = load_report(prior_run)
    prior_plan = verify_resolved_plan(
        loads_exact((prior_run / "resolved_plan.json").read_bytes(), prior_run / "resolved_plan.json")
    )
    manifest = loads_exact((prior_run / "manifest.json").read_bytes(), prior_run / "manifest.json")
    records: dict[str, dict[str, Any]] = {}
    records_dir = prior_run / "records"
    if records_dir.is_dir():
        for path in sorted(records_dir.glob("*.json")):
            record = loads_exact(path.read_bytes(), path)
            records[path.stem] = record
    return {
        "run_dir": prior_run,
        "run_id": prior_report["run_id"],
        "report": prior_report,
        "plan": prior_plan["plan"],
        "manifest": manifest,
        "records": records,
    }


def _logical_call_complete(role: str, call: Mapping[str, Any] | None) -> bool:
    if call is None:
        return False
    if call.get("imported_from_episode"):
        return call.get("invocation_status") == "succeeded"
    if call.get("invocation_status") != "succeeded":
        return False
    if role == "grader":
        return call.get("grade_parse_status") == "parsed"
    return True


def _import_logical_call(
    prior_run: Path, stem: str, role: str, prior_record: Mapping[str, Any]
) -> dict[str, Any]:
    call = dict(prior_record[role])
    evidence_path = prior_run / "call_evidence" / f"{stem}__{role}.json"
    call["imported_from_episode"] = {
        "run_id": prior_record["run_id"],
        "call_evidence_path": str(evidence_path),
    }
    return call


def _summary(
    run_id: str, envelope: Mapping[str, Any], records: list[dict[str, Any]],
    execution_scope: Mapping[str, Any], operational_status: str,
    blocked_reason: Mapping[str, Any] | None,
    network_accounting: Mapping[str, Any] | None = None,
    execution_episodes: list[dict[str, Any]] | None = None,
    retry_summary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    generation = Counter()
    grading = Counter()
    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for record in records:
        generation["succeeded" if record["generator"]["invocation_status"] == "succeeded" else "failed"] += 1
        grader = record["grader"]
        if grader is None:
            grading["not_run"] += 1
        elif grader["invocation_status"] != "succeeded":
            grading["call_failed"] += 1
        elif grader.get("grade_parse_status") == "parsed":
            grading["succeeded"] += 1
        else:
            grading["invalid_output"] += 1
        key = (record["case_id"], record["variant_id"])
        group = groups.setdefault(key, {"case_id": key[0], "variant_id": key[1], "grades": [], "requires_human_adjudication": False})
        if record.get("operational_status") in {"blocked", "blocked_integrity", "paused_retryable"}:
            group["requires_human_adjudication"] = True
        if grader is not None and grader.get("grade_parse_status") == "parsed":
            group["grades"].append(grader["axis_results"])
            if any(value in {"uncertain", "unclear"} for value in grader["axis_results"].values()):
                group["requires_human_adjudication"] = True
        else:
            group["requires_human_adjudication"] = True
    for group in groups.values():
        for axis in ("applicability", "timing", "satisfaction", "human_compensation_needed", "over_trigger_cost"):
            if len({grade[axis] for grade in group["grades"]}) > 1:
                group["requires_human_adjudication"] = True
    plan = envelope["plan"]
    completed_observations = sum(
        1 for record in records
        if _logical_call_complete("generator", record.get("generator"))
        and _logical_call_complete("grader", record.get("grader"))
    )
    unfinished = len(records) - completed_observations
    paused_retryable = sum(1 for record in records if record.get("operational_status") == "paused_retryable")
    return {
        "schema_version": 2,
        "run_id": run_id,
        "resolved_plan_sha256": envelope["resolved_plan_sha256"],
        "mode": plan["mode"],
        "evidence_label": plan["evidence_label"],
        "execution_scope": dict(execution_scope),
        "operational_status": operational_status,
        "blocked_reason": dict(blocked_reason) if blocked_reason is not None else None,
        "execution_episodes": list(execution_episodes or []),
        "completed_observations": completed_observations,
        "unfinished_observations": unfinished,
        "paused_retryable_observations": paused_retryable,
        "planned_calls": {
            "generator": execution_scope["record_count"], "grader": execution_scope["record_count"],
            "maximum_total": execution_scope["record_count"] * 2,
        },
        "actual_calls": {
            "generator": sum(generation.values()),
            "grader": sum(grading[key] for key in ("succeeded", "call_failed", "invalid_output")),
        },
        "network_accounting": dict(network_accounting or {}),
        "retry_summary": dict(retry_summary or {}),
        "generation": dict(generation),
        "grading": dict(grading),
        "groups": list(groups.values()),
        "interpretation": (
            "Axis judgments remain separate; ambiguous, failed, or uncertain grades are not "
            "counted favorably, and original grader judgments remain preserved for human adjudication."
        ),
    }


def _formal_blocking_reason(role: str, call: Mapping[str, Any]) -> dict[str, str] | None:
    if call.get("final_status") == "failed_retryable":
        return None
    if call["invocation_status"] != "succeeded":
        error = call.get("error") or {}
        message = error.get("message", "")
        if error.get("type") == "PrivateValueBlocked" or "private value" in message:
            code = "secret_or_private_value_blocked"
        elif "provenance" in message or "configuration" in message:
            code = "configuration_or_committed_provenance_mismatch"
        elif "invalid chat completion" in message:
            code = "unexpected_provider_response"
        else:
            code = f"{role}_transport_or_invocation_failure"
        return {"code": code, "role": role}
    finish_reason = call.get("public_response_metadata", {}).get("finish_reason")
    if finish_reason != "stop":
        return {"code": f"{role}_finish_reason_not_stop", "role": role, "finish_reason": str(finish_reason)}
    if role == "grader" and call.get("grade_parse_status") != "parsed":
        return {"code": "invalid_or_unparseable_grader_output", "role": role}
    return None


def _record_operational_status(
    generator_call: Mapping[str, Any], grader_call: Mapping[str, Any] | None, *, mode: str
) -> tuple[str, dict[str, str] | None]:
    if mode != "formal":
        return "completed", None
    generator_block = _formal_blocking_reason("generator", generator_call)
    if generator_block is not None:
        return "blocked_integrity", generator_block
    if generator_call.get("final_status") == "failed_retryable":
        return "paused_retryable", {"code": "generator_transport_retries_exhausted", "role": "generator"}
    if grader_call is None:
        if generator_call["invocation_status"] == "succeeded":
            return "paused_retryable", {"code": "grader_not_started", "role": "grader"}
        return "blocked_integrity", {"code": "generator_transport_or_invocation_failure", "role": "generator"}
    grader_block = _formal_blocking_reason("grader", grader_call)
    if grader_block is not None:
        return "blocked_integrity", grader_block
    if grader_call.get("final_status") == "failed_retryable":
        return "paused_retryable", {"code": "grader_transport_retries_exhausted", "role": "grader"}
    return "completed", None


def _overall_operational_status(record_statuses: list[str]) -> str:
    if any(status == "blocked_integrity" for status in record_statuses):
        return "blocked_integrity"
    if any(status == "paused_retryable" for status in record_statuses):
        return "paused_retryable"
    if record_statuses and all(status == "completed" for status in record_statuses):
        return "completed"
    return "paused_retryable"


def execute_resolved_plan(
    *, repo_root: Path, envelope: Mapping[str, Any], catalog: ModelCatalog,
    experiment: Experiment, resolved: Mapping[str, ResolvedProvider],
    authorize_network: bool,
    tranche_id: str | None = None, prior_run: Path | None = None,
    resume_from: Path | None = None,
    grader_parallelism: int | None = None,
    transport: Transport = urllib_transport, now: Callable[[], str] = _utc_now,
    new_id: Callable[[], str] = lambda: uuid.uuid4().hex,
    sleep: Callable[[float], None] | None = None,
) -> Path:
    envelope = verify_resolved_plan(envelope)
    plan = envelope["plan"]
    digest = envelope["resolved_plan_sha256"]
    policy = _execution_policy(plan)
    if grader_parallelism is not None:
        policy = {**policy, "grader_parallelism": max(1, grader_parallelism)}
    if sleep is None:
        import time
        sleep = time.sleep
    if not authorize_network:
        raise PermissionError("explicit network authorization is required; no calls made")
    if plan["mode"] == "formal" and plan.get("formal_execution_enabled") is not True:
        raise PermissionError("formal execution remains disabled in the committed experiment recipe; no calls made")
    _verify_captured_binding(
        repo_root=repo_root, envelope=envelope, experiment=experiment, resolved=resolved,
    )
    tranches = plan["schedule"].get("operational_tranches") or {}
    tranche_ids = [key for key in tranches if key.startswith("tranche_")]
    prior_evidence: dict[str, Any] | None = None
    prior_episode: dict[str, Any] | None = None
    if tranche_id is not None and tranche_id not in tranche_ids:
        raise ValueError(f"unknown operational tranche {tranche_id!r}")
    if plan["mode"] == "formal" and tranche_ids and tranche_id is None:
        raise ValueError("formal execution requires one explicit operational tranche")
    if plan["mode"] == "formal" and tranche_id in tranche_ids[1:]:
        expected_prior = tranche_ids[tranche_ids.index(tranche_id) - 1]
        if prior_run is None:
            raise PermissionError(f"{tranche_id} requires completed {expected_prior} evidence")
        from .reporting import load_report

        prior_report = load_report(prior_run)
        prior_plan = verify_resolved_plan(
            loads_exact((prior_run / "resolved_plan.json").read_bytes(), prior_run / "resolved_plan.json")
        )
        require_compatible_treatment(
            plan, prior_plan["plan"], prior_label=f"{expected_prior} prior run",
            repo_root=repo_root,
        )
        if (
            prior_report["execution_scope"].get("tranche_id") != expected_prior
            or prior_report["operational_status"] != "completed"
        ):
            raise ValueError("prior tranche evidence does not bind to the required plan and tranche")
        prior_evidence = {
            "run_id": prior_report["run_id"],
            "resolved_plan_sha256": prior_report["resolved_plan_sha256"],
            "tranche_id": expected_prior,
            "treatment_semantics": "equivalent",
        }
    if resume_from is not None:
        prior_episode = _load_prior_episode_state(resume_from)
        compatibility = require_compatible_treatment(
            plan, prior_episode["plan"], prior_label="resume episode", repo_root=repo_root
        )
        if tranche_id is not None and prior_episode["report"]["execution_scope"].get("tranche_id") != tranche_id:
            raise ValueError("resume episode tranche does not match the requested tranche")
    selected_order = [
        row for row in plan["schedule"]["execution_order"]
        if tranche_id is None or row.get("tranche_id") == tranche_id
    ]
    execution_scope = {"tranche_id": tranche_id, "record_count": len(selected_order)}
    output_root = validate_private_output(Path(plan["output_root"]), repo_root, must_exist=plan["mode"] == "formal")
    output_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(output_root, 0o700)
    run_id = new_id()
    run_dir = output_root / run_id
    run_dir.mkdir(mode=0o700, exist_ok=False)
    frozen_revision = plan["provenance"].get("git_revision")

    def before_call() -> None:
        if plan["mode"] == "formal":
            current = git_provenance(repo_root)
            if not current["clean"] or current["git_revision"] != frozen_revision:
                raise ProviderError("formal provenance changed before a network call")

    remaining_logical = 0
    for scheduled in selected_order:
        stem = _record_stem(scheduled)
        prior_record = prior_episode["records"].get(stem) if prior_episode else None
        generator_done = prior_record and _logical_call_complete("generator", prior_record.get("generator"))
        grader_done = prior_record and _logical_call_complete("grader", prior_record.get("grader"))
        if not generator_done:
            remaining_logical += 1
        if not grader_done:
            remaining_logical += 1

    gate = NetworkGate(
        transport, authorize_network, remaining_logical * policy["max_attempts"],
        before_call, catalog.private_scan_values,
        planned_logical_calls=remaining_logical,
    )
    def provider_for(role: str) -> OpenAIChatCompletionsProvider:
        return OpenAIChatCompletionsProvider(
            resolved[role], get_renderer(plan["roles"][role]["renderer"]["id"]),
            transport=gate, timeout_seconds=plan["timeouts_seconds"][role],
        )

    def private_values() -> tuple[str, ...]:
        return catalog.private_scan_values

    def persist(relative_path: str, value: Any) -> None:
        if contains_private_value(value, private_values()):
            raise RuntimeError("private value blocked before artifact persistence")
        write_new_json(run_dir / relative_path, value)

    def sanitize_call(call: dict[str, Any]) -> dict[str, Any]:
        preserved = {
            key: call[key]
            for key in ("attempt_number", "retryability", "axis_results", "grade_parse_status", "parse_error")
            if key in call
        }
        if not contains_private_value(call, private_values()):
            return call
        return {
            **preserved,
            "invocation_status": "failed",
            "requested_at": call.get("requested_at"),
            "elapsed_ms": call.get("elapsed_ms"),
            "successful_attempt_elapsed_ms": call.get("successful_attempt_elapsed_ms"),
            "request": None,
            "model_visible_request": None,
            "provider": call["provider"],
            "provider_reported_model": None,
            "raw_output": None,
            "attempt_count": call.get("attempt_count", 1),
            "retry_count": call.get("retry_count", 0),
            "final_status": "failed_integrity",
            "successful_attempt": None,
            "attempt_evidence_paths": call.get("attempt_evidence_paths", []),
            "error": {
                "type": "PrivateValueBlocked",
                "message": "provider request or response contained a private value and was not persisted",
            },
        }

    def persist_logical_call(stem: str, role: str, logical_call: dict[str, Any], attempts: list[dict[str, Any]]) -> dict[str, Any]:
        attempt_paths: list[str] = []
        sanitized_attempts = [sanitize_call(dict(attempt)) for attempt in attempts]
        for attempt in sanitized_attempts:
            attempt_number = attempt["attempt_number"]
            relative = f"call_evidence/{stem}__{role}__attempt_{attempt_number:03d}.json"
            attempt_payload = {**attempt, "resolved_plan_sha256": digest, "role": role, "logical_stem": stem}
            persist(relative, attempt_payload)
            attempt_paths.append(relative)
        logical_call = sanitize_call(logical_call)
        logical_call.update({
            "resolved_plan_sha256": digest,
            "role": role,
            "attempt_evidence_paths": attempt_paths,
        })
        persist(f"call_evidence/{stem}__{role}.json", logical_call)
        gate.mark_logical_call_completed()
        return logical_call

    def retry_counts(role: str, attempts: list[dict[str, Any]]) -> Counter[str]:
        return Counter(
            f"{role}:{attempt.get('error', {}).get('type', 'unknown')}"
            for attempt in attempts[:-1]
            if attempt.get("retryability") == "retryable"
            and attempt["invocation_status"] == "failed"
        )

    execution_episodes: list[dict[str, Any]] = []
    if prior_evidence is not None:
        execution_episodes.append({
            "episode": len(execution_episodes) + 1,
            "run_id": prior_evidence["run_id"],
            "role": "prior_tranche",
            "path": None,
        })
    if prior_episode is not None:
        execution_episodes.append({
            "episode": len(execution_episodes) + 1,
            "run_id": prior_episode["run_id"],
            "role": "resumed_prefix",
            "path": str(prior_episode["run_dir"]),
            "operational_status": prior_episode["report"]["operational_status"],
        })
    execution_episodes.append({
        "episode": len(execution_episodes) + 1,
        "run_id": run_id,
        "role": "current",
        "path": str(run_dir),
    })
    compatibility_report = (
        require_compatible_treatment(
            plan, prior_episode["plan"], prior_label="resume episode", repo_root=repo_root
        )
        if prior_episode is not None else None
    )
    policy_report = execution_policy_report(plan, prior_episode["plan"] if prior_episode else None)
    persist("resolved_plan.json", envelope)
    persist(
        "manifest.json",
        {
            "schema_version": 2,
            "run_id": run_id,
            "started_at": now(),
            "resolved_plan_sha256": digest,
            "mode": plan["mode"],
            "evidence_label": plan["evidence_label"],
            "runner_provenance": git_provenance(repo_root),
            "roles": plan["roles"],
            "sources": plan["sources"],
            "execution_scope": execution_scope,
            "prior_tranche_evidence": prior_evidence,
            "execution_episodes": execution_episodes,
            "resume_from": (
                {
                    "run_id": prior_episode["run_id"],
                    "path": str(prior_episode["run_dir"]),
                    "treatment_semantics": compatibility_report["treatment_semantics"] if compatibility_report else None,
                    "execution_policy": policy_report,
                }
                if prior_episode is not None else None
            ),
        },
    )

    generator_by_stem: dict[str, dict[str, Any]] = {}
    generator_context_by_stem: dict[str, str] = {}
    retry_counter: Counter[str] = Counter()
    generation_integrity_blocked = False

    for scheduled in selected_order:
        if generation_integrity_blocked:
            break
        stem = _record_stem(scheduled)
        prior_record = prior_episode["records"].get(stem) if prior_episode else None
        if prior_record and _logical_call_complete("generator", prior_record.get("generator")):
            generator_by_stem[stem] = _import_logical_call(
                prior_episode["run_dir"], stem, "generator", prior_record
            )
            generator_context_by_stem[stem] = prior_record["context_id"]
            continue
        case_id = scheduled["case_id"]
        variant_id = scheduled["variant_id"]
        packet = experiment.generation[case_id]
        append = experiment.variants[variant_id]["instruction_append"]
        base = plan["instructions"]["generator_base"]
        context_id = new_id()
        generator_request = {
            "call_kind": "generator", "context_id": context_id, "variant_id": variant_id,
            "system_instruction": base if not append else f"{base}\n\n{append}",
            "packet": {"case_id": case_id, "pre_context": packet["pre_context"], "user_message": packet["user_message"]},
        }
        logical_call, attempts = invoke_logical_call(
            provider_for("generator"), generator_request, now=now,
            max_attempts=policy["max_attempts"],
            backoff_seconds=policy["backoff_seconds"],
            sleep=sleep,
        )
        retry_counter.update(retry_counts("generator", attempts))
        generator_call = persist_logical_call(stem, "generator", logical_call, attempts)
        generator_by_stem[stem] = generator_call
        generator_context_by_stem[stem] = context_id
        if plan["mode"] == "formal":
            block = _formal_blocking_reason("generator", generator_call)
            if block is not None:
                generation_integrity_blocked = True

    grading_jobs: list[tuple[dict[str, Any], str, dict[str, Any], str | None]] = []
    for scheduled in selected_order:
        stem = _record_stem(scheduled)
        generator_call = generator_by_stem.get(stem)
        if generator_call is None or generator_call["invocation_status"] != "succeeded":
            continue
        prior_record = prior_episode["records"].get(stem) if prior_episode else None
        if prior_record and _logical_call_complete("grader", prior_record.get("grader")):
            continue
        grading_jobs.append((scheduled, stem, generator_call, prior_record["context_id"] if prior_record else None))

    grader_results: dict[str, dict[str, Any]] = {}
    imported_graders: dict[str, dict[str, Any]] = {}
    for scheduled in selected_order:
        stem = _record_stem(scheduled)
        prior_record = prior_episode["records"].get(stem) if prior_episode else None
        if prior_record and _logical_call_complete("grader", prior_record.get("grader")):
            imported_graders[stem] = _import_logical_call(
                prior_episode["run_dir"], stem, "grader", prior_record
            )

    def grade_one(
        job: tuple[dict[str, Any], str, dict[str, Any], str | None]
    ) -> tuple[str, dict[str, Any], Counter[str]]:
        scheduled, stem, generator_call, prior_context_id = job
        grader_request = {
            "call_kind": "grader", "context_id": new_id(),
            "packet": build_grader_packet(
                case_id=scheduled["case_id"], rubric=experiment.rubrics[scheduled["case_id"]],
                generator_output=generator_call["raw_output"], grading=plan["grading"],
            ),
        }
        logical_call, attempts = invoke_logical_call(
            provider_for("grader"), grader_request, now=now,
            max_attempts=policy["max_attempts"],
            backoff_seconds=policy["backoff_seconds"],
            sleep=sleep,
        )
        local_retry_counts = retry_counts("grader", attempts)
        if logical_call["invocation_status"] == "succeeded":
            try:
                logical_call["axis_results"] = parse_grade(logical_call["raw_output"], plan["grading"])
                logical_call["grade_parse_status"] = "parsed"
            except (json.JSONDecodeError, ValueError) as error:
                logical_call["grade_parse_status"] = "invalid"
                logical_call["parse_error"] = str(error)
        else:
            logical_call["grade_parse_status"] = "not_available"
        grader_call = persist_logical_call(stem, "grader", logical_call, attempts)
        return stem, grader_call, local_retry_counts

    if grading_jobs:
        workers = policy["grader_parallelism"]
        if workers <= 1:
            for job in grading_jobs:
                stem, grader_call, local_retry_counts = grade_one(job)
                grader_results[stem] = grader_call
                retry_counter.update(local_retry_counts)
        else:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(grade_one, job): job[1] for job in grading_jobs}
                for future in as_completed(futures):
                    stem, grader_call, local_retry_counts = future.result()
                    grader_results[stem] = grader_call
                    retry_counter.update(local_retry_counts)

    records: list[dict[str, Any]] = []
    record_statuses: list[str] = []
    blocked_reason: dict[str, str] | None = None
    for scheduled in selected_order:
        stem = _record_stem(scheduled)
        generator_call = generator_by_stem.get(stem)
        if generator_call is None:
            continue
        grader_call = imported_graders.get(stem) or grader_results.get(stem)
        if generator_call["invocation_status"] == "succeeded" and grader_call is None and stem not in imported_graders:
            grader_call = None
        status, reason = _record_operational_status(generator_call, grader_call, mode=plan["mode"])
        if reason is not None and blocked_reason is None and status == "blocked_integrity":
            blocked_reason = reason
        record = {
            "schema_version": 2,
            "run_id": run_id,
            "resolved_plan_sha256": digest,
            **scheduled,
            "context_id": generator_context_by_stem[stem],
            "rubric_adjudication": experiment.rubrics[scheduled["case_id"]]["adjudication"],
            "mode": plan["mode"],
            "evidence_label": plan["evidence_label"],
            "operational_status": status,
            "blocked_reason": reason,
            "generator": generator_call,
            "grader": grader_call,
        }
        persist(f"records/{stem}.json", record)
        records.append(record)
        record_statuses.append(status)

    operational_status = _overall_operational_status(record_statuses) if records else "completed"
    if operational_status == "paused_retryable" and blocked_reason is None:
        for record in records:
            if record["operational_status"] == "paused_retryable":
                blocked_reason = record["blocked_reason"]
                break
    network_accounting = gate.accounting()
    retry_summary = {
        "by_role_and_error_type": dict(retry_counter),
        "total_retries": sum(retry_counter.values()),
    }
    summary = _summary(
        run_id, envelope, records, execution_scope, operational_status, blocked_reason,
        network_accounting=network_accounting,
        execution_episodes=execution_episodes,
        retry_summary=retry_summary,
    )
    persist("summary.json", summary)
    matches = scan_private_values(run_dir, private_values())
    persist(
        "run_status.json",
        {
            "schema_version": 2,
            "run_id": run_id,
            "finalized_at": now(),
            "resolved_plan_sha256": digest,
            "mode": plan["mode"],
            "evidence_label": plan["evidence_label"],
            "network_calls": gate.calls,
            "network_accounting": network_accounting,
            "retry_summary": retry_summary,
            "execution_scope": execution_scope,
            "execution_episodes": execution_episodes,
            "operational_status": operational_status,
            "blocked_reason": blocked_reason,
            "secret_scan": "pass" if not matches else "fail",
            "secret_match_files": matches,
            "artifact_tree_sha256": tree_sha256(run_dir),
            "resume_from": (
                {
                    "run_id": prior_episode["run_id"],
                    "treatment_semantics": "equivalent",
                    "execution_policy": policy_report,
                }
                if prior_episode is not None else None
            ),
        },
    )
    if matches:
        raise RuntimeError(f"private value found in artifacts: {matches}")
    return run_dir
