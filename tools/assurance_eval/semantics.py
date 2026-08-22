"""Treatment-semantics compatibility for resume and tranche continuation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def extract_treatment_semantics(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Return experimentally relevant resolved fields; exclude harness provenance."""
    schedule = plan["schedule"]
    return {
        "experiment_id": plan["experiment_id"],
        "selection": plan["selection"],
        "schedule": {
            "repetitions": schedule["repetitions"],
            "variant_order_by_repetition": schedule["variant_order_by_repetition"],
            "operational_tranches": schedule.get("operational_tranches"),
            "execution_order": schedule["execution_order"],
        },
        "roles": plan["roles"],
        "instructions": plan["instructions"],
        "grading": plan["grading"],
        "timeouts_seconds": plan["timeouts_seconds"],
        "formal_execution_enabled": plan["formal_execution_enabled"],
        "sources": plan["sources"],
    }


def compare_treatment_semantics(
    current: Mapping[str, Any], prior: Mapping[str, Any]
) -> dict[str, Any]:
    """Compare two treatment-semantics projections."""
    current_sem = extract_treatment_semantics(current)
    prior_sem = extract_treatment_semantics(prior)
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
) -> dict[str, Any]:
    report = compare_treatment_semantics(current_plan, prior_plan)
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
