"""Execute an immutable resolved plan and preserve mechanical evidence."""

from __future__ import annotations

import json
import os
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from .artifacts import contains_private_value, scan_private_values, tree_sha256, write_new_json
from .config import ModelCatalog
from .experiment import Experiment
from .grading import build_grader_packet, parse_grade
from .models import Provider, ProviderError, ResolvedProvider, Transport
from .planning import public_roles, verify_resolved_plan
from .policy import NetworkGate, git_provenance, validate_private_output
from .renderers import get_renderer
from .transport import OpenAIChatCompletionsProvider, urllib_transport


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _provider_identity(provider: Provider) -> dict[str, Any]:
    assignment = provider.assignment
    return {
        "provider": assignment.provider,
        "configured_model": assignment.model,
        "model_family": assignment.family,
        "declared_model_snapshot": assignment.declared_snapshot,
        "parameters": dict(assignment.parameters),
        "context_mode": "standalone",
    }


def _invoke(
    provider: OpenAIChatCompletionsProvider, request: Mapping[str, Any], *, now: Callable[[], str]
) -> dict[str, Any]:
    requested_at = now()
    started = time.monotonic()
    try:
        response = provider.invoke_standalone(request)
    except Exception as error:
        message = str(error) if isinstance(error, (ProviderError, ValueError)) else "unexpected provider invocation failure"
        return {
            "invocation_status": "failed",
            "requested_at": requested_at,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
            "request": dict(request),
            "model_visible_request": provider.last_model_visible_request,
            "provider": _provider_identity(provider),
            "provider_reported_model": None,
            "raw_output": None,
            "attempt_count": 1,
            "retry_count": 0,
            "error": {"type": type(error).__name__, "message": message},
        }
    return {
        "invocation_status": "succeeded",
        "requested_at": requested_at,
        "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
        "request": dict(request),
        "model_visible_request": dict(response.model_visible_request),
        "provider": _provider_identity(provider),
        "provider_reported_model": response.provider_reported_model,
        "model_identity": {
            "configured_model": provider.assignment.model,
            "declared_model_snapshot": provider.assignment.declared_snapshot,
            "provider_reported_model": response.provider_reported_model,
        },
        "raw_output": response.raw_output,
        "public_response_metadata": dict(response.public_metadata),
        "attempt_count": 1,
        "retry_count": 0,
        "error": None,
    }


def _verify_captured_binding(
    *, repo_root: Path, envelope: Mapping[str, Any], experiment: Experiment,
    resolved: Mapping[str, ResolvedProvider],
) -> None:
    plan = envelope["plan"]
    if experiment.recipe_sha256 != plan["recipe"]["sha256"] or experiment.sources != plan["sources"]:
        raise ValueError("captured experiment differs from the resolved plan")
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


def _summary(
    run_id: str, envelope: Mapping[str, Any], records: list[dict[str, Any]],
    execution_scope: Mapping[str, Any], operational_status: str,
    blocked_reason: Mapping[str, Any] | None,
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
        elif grader["grade_parse_status"] == "parsed":
            grading["succeeded"] += 1
        else:
            grading["invalid_output"] += 1
        key = (record["case_id"], record["variant_id"])
        group = groups.setdefault(key, {"case_id": key[0], "variant_id": key[1], "grades": [], "requires_human_adjudication": False})
        if record.get("operational_status") == "blocked":
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
    return {
        "schema_version": 1,
        "run_id": run_id,
        "resolved_plan_sha256": envelope["resolved_plan_sha256"],
        "mode": plan["mode"],
        "evidence_label": plan["evidence_label"],
        "execution_scope": dict(execution_scope),
        "operational_status": operational_status,
        "blocked_reason": dict(blocked_reason) if blocked_reason is not None else None,
        "planned_calls": {
            "generator": execution_scope["record_count"], "grader": execution_scope["record_count"],
            "maximum_total": execution_scope["record_count"] * 2,
        },
        "actual_calls": {"generator": sum(generation.values()), "grader": sum(grading[key] for key in ("succeeded", "call_failed", "invalid_output"))},
        "generation": dict(generation),
        "grading": dict(grading),
        "groups": list(groups.values()),
        "interpretation": (
            "Axis judgments remain separate; ambiguous, failed, or uncertain grades are not "
            "counted favorably, and original grader judgments remain preserved for human adjudication."
        ),
    }


def _formal_blocking_reason(role: str, call: Mapping[str, Any]) -> dict[str, str] | None:
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


def execute_resolved_plan(
    *, repo_root: Path, envelope: Mapping[str, Any], catalog: ModelCatalog,
    experiment: Experiment, resolved: Mapping[str, ResolvedProvider],
    authorize_network: bool,
    tranche_id: str | None = None, prior_run: Path | None = None,
    transport: Transport = urllib_transport, now: Callable[[], str] = _utc_now,
    new_id: Callable[[], str] = lambda: uuid.uuid4().hex,
) -> Path:
    envelope = verify_resolved_plan(envelope)
    plan = envelope["plan"]
    digest = envelope["resolved_plan_sha256"]
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
        if (
            prior_report["resolved_plan_sha256"] != digest
            or prior_report["execution_scope"].get("tranche_id") != expected_prior
            or prior_report["operational_status"] != "completed"
        ):
            raise ValueError("prior tranche evidence does not bind to the required plan and tranche")
        prior_evidence = {
            "run_id": prior_report["run_id"],
            "resolved_plan_sha256": digest,
            "tranche_id": expected_prior,
        }
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

    gate = NetworkGate(
        transport, authorize_network, len(selected_order) * 2,
        before_call, catalog.private_scan_values,
    )
    providers = {
        role: OpenAIChatCompletionsProvider(
            resolved[role], get_renderer(plan["roles"][role]["renderer"]["id"]),
            transport=gate, timeout_seconds=plan["timeouts_seconds"][role],
        )
        for role in ("generator", "grader")
    }
    def private_values() -> tuple[str, ...]:
        return catalog.private_scan_values

    def persist(relative_path: str, value: Any) -> None:
        if contains_private_value(value, private_values()):
            raise RuntimeError("private value blocked before artifact persistence")
        write_new_json(run_dir / relative_path, value)

    def sanitize_call(call: dict[str, Any]) -> dict[str, Any]:
        if not contains_private_value(call, private_values()):
            return call
        return {
            "invocation_status": "failed",
            "requested_at": call.get("requested_at"),
            "elapsed_ms": call.get("elapsed_ms"),
            "request": None,
            "model_visible_request": None,
            "provider": call["provider"],
            "provider_reported_model": None,
            "raw_output": None,
            "attempt_count": 1,
            "retry_count": 0,
            "error": {
                "type": "PrivateValueBlocked",
                "message": "provider request or response contained a private value and was not persisted",
            },
        }

    persist("resolved_plan.json", envelope)
    persist(
        "manifest.json",
        {
            "schema_version": 1, "run_id": run_id, "started_at": now(),
            "resolved_plan_sha256": digest, "mode": plan["mode"],
            "evidence_label": plan["evidence_label"], "runner_provenance": git_provenance(repo_root),
            "roles": plan["roles"], "sources": plan["sources"],
            "execution_scope": execution_scope, "prior_tranche_evidence": prior_evidence,
        },
    )
    records: list[dict[str, Any]] = []
    blocked_reason: dict[str, str] | None = None
    for scheduled in selected_order:
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
        generator_call = _invoke(providers["generator"], generator_request, now=now)
        generator_call = sanitize_call(generator_call)
        generator_call.update({"resolved_plan_sha256": digest, "role": "generator"})
        stem = f"{case_id}__{variant_id}__r{scheduled['repetition']:03d}"
        persist(f"call_evidence/{stem}__generator.json", generator_call)
        grader_call: dict[str, Any] | None = None
        generator_block = _formal_blocking_reason("generator", generator_call) if plan["mode"] == "formal" else None
        if generator_call["invocation_status"] == "succeeded" and generator_block is None:
            grader_request = {
                "call_kind": "grader", "context_id": new_id(),
                "packet": build_grader_packet(
                    case_id=case_id, rubric=experiment.rubrics[case_id],
                    generator_output=generator_call["raw_output"], grading=plan["grading"],
                ),
            }
            grader_call = _invoke(providers["grader"], grader_request, now=now)
            grader_call = sanitize_call(grader_call)
            grader_call.update({"resolved_plan_sha256": digest, "role": "grader"})
            if grader_call["invocation_status"] == "succeeded":
                try:
                    grader_call["axis_results"] = parse_grade(grader_call["raw_output"], plan["grading"])
                    grader_call["grade_parse_status"] = "parsed"
                except (json.JSONDecodeError, ValueError) as error:
                    grader_call["grade_parse_status"] = "invalid"
                    grader_call["parse_error"] = str(error)
            else:
                grader_call["grade_parse_status"] = "not_available"
            persist(f"call_evidence/{stem}__grader.json", grader_call)
            if plan["mode"] == "formal":
                blocked_reason = _formal_blocking_reason("grader", grader_call)
        elif generator_block is not None:
            blocked_reason = generator_block
        record = {
            "schema_version": 1, "run_id": run_id, "resolved_plan_sha256": digest,
            **scheduled, "context_id": context_id, "rubric_adjudication": experiment.rubrics[case_id]["adjudication"],
            "mode": plan["mode"], "evidence_label": plan["evidence_label"],
            "operational_status": "blocked" if blocked_reason is not None else "completed",
            "blocked_reason": blocked_reason,
            "generator": generator_call, "grader": grader_call,
        }
        persist(f"records/{stem}.json", record)
        records.append(record)
        if blocked_reason is not None:
            break
    operational_status = "blocked" if blocked_reason is not None else "completed"
    summary = _summary(
        run_id, envelope, records, execution_scope, operational_status, blocked_reason,
    )
    persist("summary.json", summary)
    matches = scan_private_values(run_dir, private_values())
    persist(
        "run_status.json",
        {
            "schema_version": 1, "run_id": run_id, "finalized_at": now(),
            "resolved_plan_sha256": digest, "mode": plan["mode"],
            "evidence_label": plan["evidence_label"], "network_calls": gate.calls,
            "execution_scope": execution_scope,
            "operational_status": operational_status, "blocked_reason": blocked_reason,
            "secret_scan": "pass" if not matches else "fail", "secret_match_files": matches,
            "artifact_tree_sha256": tree_sha256(run_dir),
        },
    )
    if matches:
        raise RuntimeError(f"private value found in artifacts: {matches}")
    return run_dir
