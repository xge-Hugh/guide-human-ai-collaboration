"""Treatment-semantics compatibility for resume and tranche continuation."""

from __future__ import annotations

import copy
import subprocess
from pathlib import Path
from typing import Any, Mapping

from .experiment import loads_exact


_REPO_ROOT = Path(__file__).resolve().parents[2]
_RUBRIC_FIELDS = (
    "reference_case", "expected_applicability", "adjudication",
    "required_protection", "latest_useful_point",
)


def capture_treatment_content(
    plan: Mapping[str, Any],
    generation: Mapping[str, Mapping[str, Any]],
    variants: Mapping[str, Mapping[str, Any]],
    rubrics: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Capture parsed source fields that can reach the selected model calls."""
    cases = plan["selection"]["cases"]
    variant_ids = plan["selection"]["variants"]
    return {
        "schema_version": 1,
        "generation_packets": {
            case_id: {
                "pre_context": generation[case_id]["pre_context"],
                "user_message": generation[case_id]["user_message"],
            }
            for case_id in cases
        },
        "variant_instruction_appends": {
            variant_id: variants[variant_id]["instruction_append"]
            for variant_id in variant_ids
        },
        "grader_rubrics": {
            case_id: {field: rubrics[case_id][field] for field in _RUBRIC_FIELDS}
            for case_id in cases
        },
    }


def _git_source_document(
    plan: Mapping[str, Any], source_name: str, *, repo_root: Path
) -> Mapping[str, Any]:
    revision = plan.get("provenance", {}).get("git_revision")
    recorded_path = plan.get("sources", {}).get(source_name, {}).get("path")
    if not isinstance(revision, str) or not revision or not isinstance(recorded_path, str):
        raise ValueError("legacy plan lacks recorded Git source provenance")
    path = Path(recorded_path)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(repo_root.resolve())
        except ValueError:
            raise ValueError("legacy semantic source is outside the repository") from None
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("legacy semantic source path is unsafe")
    try:
        raw = subprocess.run(
            ["git", "show", f"{revision}:{path.as_posix()}"],
            cwd=repo_root, check=True, capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        raise ValueError(
            f"cannot reconstruct legacy {source_name} content from recorded Git provenance"
        ) from None
    document = loads_exact(raw, f"{revision}:{path.as_posix()}")
    if not isinstance(document, dict):
        raise ValueError(f"legacy {source_name} source is not a JSON object")
    return document


def _legacy_treatment_content(
    plan: Mapping[str, Any], *, repo_root: Path
) -> dict[str, Any]:
    documents = {
        source_name: _git_source_document(plan, source_name, repo_root=repo_root)
        for source_name in ("generation", "variants", "rubrics")
    }
    generation = {
        item["packet_id"]: item for item in documents["generation"].get("packets", [])
    }
    variants = {
        item["variant_id"]: item for item in documents["variants"].get("variants", [])
    }
    rubrics = {
        item["packet_id"]: item for item in documents["rubrics"].get("rubrics", [])
    }
    try:
        return capture_treatment_content(plan, generation, variants, rubrics)
    except (KeyError, TypeError):
        raise ValueError("legacy semantic sources do not contain the selected treatment fields") from None


def _tranche_assignment(schedule: Mapping[str, Any]) -> dict[str, str | None]:
    tranches = schedule.get("operational_tranches") or {}
    by_repetition = {
        repetition: tranche_id
        for tranche_id, value in tranches.items()
        if tranche_id.startswith("tranche_") and isinstance(value, Mapping)
        for repetition in value.get("repetitions", [])
    }
    return {
        str(repetition): by_repetition.get(repetition)
        for repetition in range(1, schedule["repetitions"] + 1)
    }


def extract_treatment_semantics(
    plan: Mapping[str, Any], *, repo_root: Path = _REPO_ROOT
) -> dict[str, Any]:
    """Return model-visible treatment identity, excluding byte/provenance metadata."""
    content = plan.get("treatment_content_snapshot")
    if content is None:
        content = _legacy_treatment_content(plan, repo_root=repo_root)
    if not isinstance(content, Mapping) or content.get("schema_version") != 1:
        raise ValueError("resolved plan treatment-content snapshot is invalid")
    schedule = plan["schedule"]
    return {
        "selection": copy.deepcopy(plan["selection"]),
        "generation_packets": copy.deepcopy(content["generation_packets"]),
        "variant_instruction_appends": copy.deepcopy(content["variant_instruction_appends"]),
        "grader_rubrics": copy.deepcopy(content["grader_rubrics"]),
        "generator_base_instruction": plan["instructions"]["generator_base"],
        "roles": {
            role: {
                "model": plan["roles"][role]["model"],
                "family": plan["roles"][role]["family"],
                "parameters": copy.deepcopy(plan["roles"][role]["parameters"]),
                "renderer": {"semantic_id": plan["roles"][role]["renderer"]["id"]},
            }
            for role in ("generator", "grader")
        },
        "grading": {
            "axes": copy.deepcopy(plan["grading"]["axes"]),
            "conditional_rule": plan["grading"]["conditional_rule"],
            "output_schema": copy.deepcopy(plan["grading"]["output_schema"]),
        },
        "schedule": {
            "repetitions": schedule["repetitions"],
            "variant_order_by_repetition": copy.deepcopy(
                schedule["variant_order_by_repetition"]
            ),
            "tranche_assignment": _tranche_assignment(schedule),
        },
    }


def compare_treatment_semantics(
    current: Mapping[str, Any], prior: Mapping[str, Any], *, repo_root: Path = _REPO_ROOT
) -> dict[str, Any]:
    """Compare two treatment-semantics projections."""
    current_sem = extract_treatment_semantics(current, repo_root=repo_root)
    prior_sem = extract_treatment_semantics(prior, repo_root=repo_root)
    equivalent = current_sem == prior_sem
    return {
        "treatment_semantics": "equivalent" if equivalent else "incompatible",
        "current": current_sem,
        "prior": prior_sem,
        "differences": _diff_keys(current_sem, prior_sem) if not equivalent else [],
    }


def _diff_keys(left: Any, right: Any, prefix: str = "") -> list[str]:
    differences: list[str] = []
    if isinstance(left, dict) and isinstance(right, dict):
        keys = sorted(set(left) | set(right))
        for key in keys:
            path = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                differences.append(path)
            else:
                differences.extend(_diff_keys(left[key], right[key], path))
        return differences
    if left != right:
        return [prefix or "root"]
    return []


def require_compatible_treatment(
    current_plan: Mapping[str, Any],
    prior_plan: Mapping[str, Any],
    *,
    prior_label: str = "prior episode",
    repo_root: Path = _REPO_ROOT,
) -> dict[str, Any]:
    report = compare_treatment_semantics(current_plan, prior_plan, repo_root=repo_root)
    if report["treatment_semantics"] != "equivalent":
        raise ValueError(
            f"{prior_label} treatment semantics are incompatible: {report['differences']}"
        )
    return report


def execution_policy_report(
    current_plan: Mapping[str, Any], prior_plan: Mapping[str, Any] | None
) -> dict[str, Any]:
    current_policy = dict(current_plan.get("execution_policy") or {})
    if prior_plan is None:
        return {"execution_policy": "initial", "reason": None}
    prior_policy = dict(prior_plan.get("execution_policy") or {})
    if current_policy == prior_policy:
        return {"execution_policy": "unchanged", "reason": None}
    return {
        "execution_policy": "amended",
        "reason": "transient transport resilience and resumability",
        "current": current_policy,
        "prior": prior_policy,
    }


def normalize_output_root(path: str) -> str:
    """Normalize output-root representation for harmless path comparison."""
    return str(Path(path).resolve())
