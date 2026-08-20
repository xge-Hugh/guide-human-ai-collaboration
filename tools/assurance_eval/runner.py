"""Controlled replay orchestration and append-only JSON artifacts."""

from __future__ import annotations

import json
import os
import subprocess
import uuid
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from .loading import PhaseBInputs, load_phase_b_inputs
from .models import ProviderDescriptor, ProviderResponse, RunConfig
from .providers import Provider, ProviderError


GRADING_AXES = (
    "applicability",
    "applicability_basis",
    "timing",
    "satisfaction",
    "human_compensation_needed",
    "over_trigger_cost",
    "notes",
)

_ALLOWED_GRADES = {
    "applicability": {"applicable", "not_applicable", "uncertain"},
    "timing": {"on_time", "late_recoverable", "late_contaminated", "too_late"},
    "satisfaction": {"satisfied", "partial", "unsatisfied"},
    "human_compensation_needed": {"yes", "no", "unclear"},
    "over_trigger_cost": {"none", "low", "material"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_revision(repo_root: Path) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _runner_source_digest(repo_root: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    source_root = repo_root / "tools" / "assurance_eval"
    for path in sorted(source_root.glob("*.py")):
        digest.update(str(path.relative_to(repo_root)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _working_tree_status(repo_root: Path) -> dict[str, Any]:
    import hashlib

    try:
        lines = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        return {
            "available": False,
            "dirty": None,
            "entry_count": None,
            "status_sha256": None,
        }
    status_text = "\n".join(lines).encode("utf-8")
    return {
        "available": True,
        "dirty": bool(lines),
        "entry_count": len(lines),
        "status_sha256": hashlib.sha256(status_text).hexdigest(),
    }


def _write_new_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _descriptor_dict(descriptor: ProviderDescriptor) -> dict[str, Any]:
    result = asdict(descriptor)
    result["public_parameters"] = dict(descriptor.public_parameters)
    result["uncontrolled_parameters"] = list(descriptor.uncontrolled_parameters)
    return result


def _parse_grade(raw_output: str) -> dict[str, str]:
    value = json.loads(raw_output)
    if not isinstance(value, dict):
        raise ValueError("grader output must be a JSON object")
    missing = [axis for axis in GRADING_AXES if axis not in value]
    extra = sorted(set(value) - set(GRADING_AXES))
    if missing or extra:
        raise ValueError(f"grader axes differ: missing={missing}, extra={extra}")
    if not all(isinstance(value[axis], str) for axis in GRADING_AXES):
        raise ValueError("every grader axis must contain a string")
    if not value["applicability_basis"].strip():
        raise ValueError("applicability_basis must be non-empty")
    for axis, allowed in _ALLOWED_GRADES.items():
        if value[axis] not in allowed:
            raise ValueError(f"invalid {axis}: {value[axis]!r}")
    return {axis: value[axis] for axis in GRADING_AXES}


class AssuranceEvalRunner:
    def __init__(
        self,
        repo_root: Path,
        generator: Provider,
        grader: Provider,
        *,
        now: Callable[[], str] = _utc_now,
        new_id: Callable[[], str] = lambda: uuid.uuid4().hex,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.generator = generator
        self.grader = grader
        for role, provider in (("generator", generator), ("grader", grader)):
            if provider.descriptor.context_mode != "standalone":
                raise ValueError(f"{role} provider must declare standalone context mode")
        self.now = now
        self.new_id = new_id

    def run(self, config: RunConfig) -> Path:
        config.validate()
        inputs = load_phase_b_inputs(self.repo_root, variants_file=config.variants_file)
        self._validate_selection(config, inputs)

        execution_plan = self._execution_plan(config)

        run_id = self.new_id()
        provenance = {
            "git_revision": _git_revision(self.repo_root),
            "working_tree": _working_tree_status(self.repo_root),
            "runner_source_sha256": _runner_source_digest(self.repo_root),
        }
        run_dir = config.output_root.resolve() / run_id
        run_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
        os.chmod(run_dir, 0o700)
        started_at = self.now()
        manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "started_at": started_at,
            "run_mode": config.run_mode,
            "evidence_use": config.evidence_label,
            "runner_provenance": provenance,
            "source_files": inputs.source_files,
            "config": {
                "base_generator_instruction": config.base_generator_instruction,
                "grader_instruction": config.grader_instruction,
                "grader_normative_context": config.grader_normative_context,
                "case_ids": list(config.case_ids),
                "variant_ids": list(config.variant_ids),
                "variants_file": config.variants_file,
                "run_mode": config.run_mode,
                "language_components": {
                    "generator_base": config.generator_base_language,
                    "case_packet": config.case_packet_language,
                    "variant_condition": config.variant_condition_language,
                    "grader_instruction": config.grader_instruction_language,
                    "grader_context": config.grader_context_language,
                },
                "repetitions": config.repetitions,
                "max_retries": config.max_retries,
                "variant_order_by_repetition": (
                    None
                    if config.variant_order_by_repetition is None
                    else [list(order) for order in config.variant_order_by_repetition]
                ),
                "planned_execution_order": execution_plan,
            },
            "generator_provider": _descriptor_dict(self.generator.descriptor),
            "grader_provider": _descriptor_dict(self.grader.descriptor),
        }
        _write_new_json(run_dir / "manifest.json", manifest)

        records: list[dict[str, Any]] = []
        for planned in execution_plan:
            record = self._run_record(
                run_dir,
                run_id,
                planned["case_id"],
                planned["variant_id"],
                planned["repetition"],
                planned["execution_index"],
                planned["variant_position"],
                config,
                inputs,
            )
            filename = (
                f"{planned['case_id']}__{planned['variant_id']}__"
                f"r{planned['repetition']:03d}.json"
            )
            relative_path = Path("records") / filename
            _write_new_json(run_dir / relative_path, record)
            records.append({"path": str(relative_path), "record": record})

        _write_new_json(
            run_dir / "summary.json",
            self._summarize(run_id, config.run_mode, config.evidence_label, records),
        )
        _write_new_json(
            run_dir / "completed.json",
            {
                "schema_version": 1,
                "run_id": run_id,
                "run_mode": config.run_mode,
                "evidence_use": config.evidence_label,
                "completed_at": self.now(),
            },
        )
        return run_dir

    @staticmethod
    def _execution_plan(config: RunConfig) -> list[dict[str, Any]]:
        plan: list[dict[str, Any]] = []
        if config.variant_order_by_repetition is None:
            selections = (
                (case_id, variant_id, repetition, config.variant_ids.index(variant_id) + 1)
                for case_id in config.case_ids
                for variant_id in config.variant_ids
                for repetition in range(1, config.repetitions + 1)
            )
        else:
            selections = (
                (case_id, variant_id, repetition, position)
                for repetition, order in enumerate(config.variant_order_by_repetition, start=1)
                for case_id in config.case_ids
                for position, variant_id in enumerate(order, start=1)
            )
        for execution_index, (case_id, variant_id, repetition, variant_position) in enumerate(
            selections, start=1
        ):
            plan.append(
                {
                    "execution_index": execution_index,
                    "case_id": case_id,
                    "variant_id": variant_id,
                    "repetition": repetition,
                    "variant_position": variant_position,
                }
            )
        return plan

    @staticmethod
    def _validate_selection(config: RunConfig, inputs: PhaseBInputs) -> None:
        unknown_cases = sorted(set(config.case_ids) - set(inputs.generation))
        unknown_variants = sorted(set(config.variant_ids) - set(inputs.variants))
        if unknown_cases or unknown_variants:
            raise ValueError(
                f"unknown selections: cases={unknown_cases}, variants={unknown_variants}"
            )
        if len(set(config.case_ids)) != len(config.case_ids):
            raise ValueError("case_ids cannot contain duplicates")
        if len(set(config.variant_ids)) != len(config.variant_ids):
            raise ValueError("variant_ids cannot contain duplicates")

    def _run_record(
        self,
        run_dir: Path,
        run_id: str,
        case_id: str,
        variant_id: str,
        repetition: int,
        execution_index: int,
        variant_position: int,
        config: RunConfig,
        inputs: PhaseBInputs,
    ) -> dict[str, Any]:
        packet = inputs.generation[case_id]
        variant = inputs.variants[variant_id]
        context_id = self.new_id()
        appended = variant["instruction_append"]
        system_instruction = config.base_generator_instruction
        if appended:
            system_instruction = f"{system_instruction}\n\n{appended}"
        generator_request = {
            "call_kind": "generator",
            "context_id": context_id,
            "variant_id": variant_id,
            "system_instruction": system_instruction,
            "packet": {
                "case_id": case_id,
                "pre_context": packet["pre_context"],
                "user_message": packet["user_message"],
            },
        }
        generator_call = self._invoke(self.generator, generator_request, config.max_retries)
        generator_call["run_mode"] = config.run_mode
        generator_call["evidence_use"] = config.evidence_label
        record_stem = f"{case_id}__{variant_id}__r{repetition:03d}"
        _write_new_json(
            run_dir / "call_evidence" / f"{record_stem}__generator.json",
            generator_call,
        )
        record: dict[str, Any] = {
            "schema_version": 1,
            "run_id": run_id,
            "case_id": case_id,
            "variant_id": variant_id,
            "repetition": repetition,
            "execution_index": execution_index,
            "variant_position": variant_position,
            "context_id": context_id,
            "rubric_adjudication": inputs.rubrics[case_id]["adjudication"],
            "run_mode": config.run_mode,
            "evidence_use": config.evidence_label,
            "generator": generator_call,
            "grader": None,
        }
        if generator_call["invocation_status"] != "succeeded":
            return record

        grader_packet = {
            "case_id": case_id,
            "normative_context": config.grader_normative_context,
            "reference_semantic_boundary": inputs.rubrics[case_id],
            "raw_generator_output": generator_call["raw_output"],
            "axes": list(GRADING_AXES),
        }
        grader_request = {
            "call_kind": "grader",
            "context_id": self.new_id(),
            "system_instruction": config.grader_instruction,
            "packet": grader_packet,
        }
        grader_call = self._invoke(self.grader, grader_request, config.max_retries)
        grader_call["run_mode"] = config.run_mode
        grader_call["evidence_use"] = config.evidence_label
        if grader_call["invocation_status"] == "succeeded":
            try:
                grader_call["axis_results"] = _parse_grade(grader_call["raw_output"])
                grader_call["grade_parse_status"] = "parsed"
            except (json.JSONDecodeError, ValueError) as error:
                grader_call["grade_parse_status"] = "invalid"
                grader_call["parse_error"] = str(error)
        else:
            grader_call["grade_parse_status"] = "not_available"
        _write_new_json(
            run_dir / "call_evidence" / f"{record_stem}__grader.json",
            grader_call,
        )
        record["grader"] = grader_call
        return record

    def _invoke(
        self, provider: Provider, request: Mapping[str, Any], max_retries: int
    ) -> dict[str, Any]:
        descriptor = _descriptor_dict(provider.descriptor)
        request_snapshot = deepcopy(dict(request))
        attempts: list[dict[str, Any]] = []
        for attempt_number in range(1, max_retries + 2):
            requested_at = self.now()
            try:
                response: ProviderResponse = provider.invoke_standalone(deepcopy(request_snapshot))
            except ProviderError as error:
                attempts.append(
                    {
                        "attempt": attempt_number,
                        "requested_at": requested_at,
                        "error": {
                            "type": type(error).__name__,
                            "message": error.public_message,
                            "retryable": error.retryable,
                        },
                    }
                )
                if not error.retryable:
                    break
                continue
            except Exception as error:
                attempts.append(
                    {
                        "attempt": attempt_number,
                        "requested_at": requested_at,
                        "error": {
                            "type": type(error).__name__,
                            "message": "unclassified provider exception; details omitted",
                            "retryable": False,
                        },
                    }
                )
                break
            attempts.append({"attempt": attempt_number, "requested_at": requested_at, "error": None})
            return {
                "invocation_status": "succeeded",
                "request": request_snapshot,
                "model_visible_request": (
                    request_snapshot
                    if response.model_visible_request is None
                    else dict(response.model_visible_request)
                ),
                "provider": descriptor,
                "provider_reported_model": response.provider_reported_model,
                "model_identity": {
                    "configured_model": descriptor["configured_model"],
                    "declared_model_snapshot": descriptor["declared_model_snapshot"],
                    "provider_reported_model": response.provider_reported_model,
                },
                "attempts": attempts,
                "retry_count": attempt_number - 1,
                "raw_output": response.raw_output,
                "public_response_metadata": dict(response.public_metadata),
            }
        return {
            "invocation_status": "failed",
            "request": request_snapshot,
            "provider": descriptor,
            "provider_reported_model": None,
            "attempts": attempts,
            "retry_count": len(attempts) - 1,
            "raw_output": None,
            "public_response_metadata": {},
        }

    @staticmethod
    def _summarize(
        run_id: str,
        run_mode: str,
        evidence_label: str,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        generation = Counter()
        grading = Counter()
        groups: dict[tuple[str, str], dict[str, Any]] = {}
        references: list[dict[str, Any]] = []
        for item in records:
            record = item["record"]
            generator_succeeded = record["generator"]["invocation_status"] == "succeeded"
            generation["succeeded" if generator_succeeded else "failed"] += 1
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
            group = groups.setdefault(
                key,
                {
                    "case_id": record["case_id"],
                    "variant_id": record["variant_id"],
                    "rubric_adjudication": record["rubric_adjudication"],
                    "requires_human_adjudication": record["rubric_adjudication"] != "clear",
                    "repetitions": [],
                    "axis_counts": {axis: Counter() for axis in _ALLOWED_GRADES},
                },
            )
            repetition_result = {
                "repetition": record["repetition"],
                "execution_index": record["execution_index"],
                "variant_position": record["variant_position"],
                "generator_invocation": record["generator"]["invocation_status"],
                "grader_invocation": None if grader is None else grader["invocation_status"],
                "grade_parse_status": None if grader is None else grader.get("grade_parse_status"),
            }
            group["repetitions"].append(repetition_result)
            if grader is not None and grader.get("grade_parse_status") == "parsed":
                for axis in _ALLOWED_GRADES:
                    group["axis_counts"][axis][grader["axis_results"][axis]] += 1
            references.append(
                {
                    "case_id": record["case_id"],
                    "variant_id": record["variant_id"],
                    "repetition": record["repetition"],
                    "execution_index": record["execution_index"],
                    "variant_position": record["variant_position"],
                    "rubric_adjudication": record["rubric_adjudication"],
                    "record_path": item["path"],
                }
            )
        summarized_groups = []
        for group in groups.values():
            summarized_groups.append(
                {
                    **group,
                    "axis_counts": {
                        axis: dict(counts) for axis, counts in group["axis_counts"].items()
                    },
                }
            )
        return {
            "schema_version": 1,
            "run_id": run_id,
            "run_mode": run_mode,
            "evidence_use": evidence_label,
            "record_count": len(records),
            "generation": dict(generation),
            "grading": dict(grading),
            "groups": summarized_groups,
            "records": references,
            "interpretation": "Mechanical summary only; inspect per-run raw evidence before drawing conclusions.",
        }
