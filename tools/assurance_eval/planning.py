"""Pure run planning and resolved-plan hash verification."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping

from .config import ModelCatalog
from .artifacts import contains_private_value
from .experiment import Experiment, canonical_json, loads_exact, sha256_bytes
from .models import ResolvedProvider
from .policy import EVIDENCE_LABELS, git_provenance, require_committed_paths, validate_private_output
from .renderers import renderer_identity


def _execution_order(
    case_ids: list[str], orders: list[list[str]], tranches: Mapping[str, Any] | None
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    tranche_by_repetition = {
        repetition: tranche_id
        for tranche_id, value in (tranches or {}).items()
        if tranche_id.startswith("tranche_") and isinstance(value, Mapping)
        for repetition in value.get("repetitions", [])
    }
    for repetition, order in enumerate(orders, start=1):
        for case_id in case_ids:
            for position, variant_id in enumerate(order, start=1):
                rows.append(
                    {
                        "execution_index": len(rows) + 1,
                        "repetition": repetition,
                        "case_id": case_id,
                        "variant_id": variant_id,
                        "variant_position": position,
                        "tranche_id": tranche_by_repetition.get(repetition),
                    }
                )
    return rows


def _public_role(provider: ResolvedProvider, renderer_id: str) -> dict[str, Any]:
    assignment = provider.assignment
    return {
        "provider": assignment.provider,
        "model": assignment.model,
        "family": assignment.family,
        "declared_snapshot": assignment.declared_snapshot,
        "parameters": dict(assignment.parameters),
        "renderer": renderer_identity(renderer_id),
        "context_mode": "standalone",
    }


def build_resolved_plan(
    *, repo_root: Path, experiment: Experiment, catalog: ModelCatalog, profile: str, mode: str
) -> tuple[dict[str, Any], dict[str, ResolvedProvider]]:
    if mode not in {"exploratory", "formal"}:
        raise ValueError("mode must be exploratory or formal")
    recipe = experiment.recipe
    providers = catalog.resolve(profile, recipe["parameters"])
    provenance = git_provenance(repo_root)
    if mode == "formal" and (not provenance["available"] or not provenance["clean"]):
        raise ValueError("formal planning requires clean committed provenance")
    if mode == "formal":
        require_committed_paths(
            repo_root, (experiment.recipe_path, *experiment.source_paths.values())
        )
    if mode == "formal" and providers["generator"].assignment.family == providers["grader"].assignment.family:
        raise ValueError("formal Phase B requires different declared generator and grader families")
    if mode == "formal" and providers["generator"].assignment.model == providers["grader"].assignment.model:
        raise ValueError("formal Phase B requires distinct configured generator and grader models")
    selection = recipe["selection"]
    schedule = recipe["schedule"]
    order = _execution_order(
        selection["cases"], schedule["variant_order_by_repetition"],
        schedule.get("operational_tranches"),
    )
    output_value = Path(recipe["output_root"])
    output_root = output_value if output_value.is_absolute() else experiment.recipe_path.parent / output_value
    output_root = validate_private_output(output_root, repo_root, must_exist=False)
    try:
        recipe_display_path = str(experiment.recipe_path.relative_to(repo_root))
    except ValueError:
        recipe_display_path = str(experiment.recipe_path)
    body: dict[str, Any] = {
        "schema_version": 1,
        "experiment_id": recipe["experiment_id"],
        "profile": profile,
        "mode": mode,
        "formal_execution_enabled": recipe["formal_execution_enabled"],
        "evidence_label": EVIDENCE_LABELS[mode],
        "recipe": {"path": recipe_display_path, "sha256": experiment.recipe_sha256},
        "sources": dict(experiment.sources),
        "selection": {"cases": list(selection["cases"]), "variants": list(selection["variants"])},
        "schedule": {
            "repetitions": schedule["repetitions"],
            "variant_order_by_repetition": schedule["variant_order_by_repetition"],
            "operational_tranches": schedule.get("operational_tranches"),
            "execution_order": order,
        },
        "roles": {
            role: _public_role(providers[role], recipe["renderers"][role])
            for role in ("generator", "grader")
        },
        "instructions": dict(recipe["instructions"]),
        "grading": dict(recipe["grading"]),
        "expected_calls": {
            "generator": len(order),
            "grader": len(order),
            "maximum_total": len(order) * 2,
        },
        "execution_policy": {
            "network_authorization_required": True,
            "automatic_retries": 0,
            "exact_requests_and_raw_final_outputs": True,
            "reasoning_content_retained": False,
            "standalone_grader": True,
        },
        "output_root": str(output_root),
        "provenance": provenance,
    }
    digest = sha256_bytes(canonical_json(body))
    envelope = {"schema_version": 1, "resolved_plan_sha256": digest, "plan": body}
    if contains_private_value(envelope, catalog.private_scan_values):
        raise ValueError("resolved plan contains a private catalog value")
    return envelope, providers


def verify_resolved_plan(envelope: object) -> dict[str, Any]:
    if not isinstance(envelope, dict) or set(envelope) != {"schema_version", "resolved_plan_sha256", "plan"}:
        raise ValueError("resolved plan envelope fields differ")
    if envelope["schema_version"] != 1 or not isinstance(envelope["plan"], dict):
        raise ValueError("unsupported resolved plan schema")
    actual = sha256_bytes(canonical_json(envelope["plan"]))
    if envelope["resolved_plan_sha256"] != actual:
        raise ValueError("resolved plan hash mismatch")
    plan = envelope["plan"]
    if plan.get("mode") not in {"exploratory", "formal"}:
        raise ValueError("resolved plan mode is invalid")
    if plan.get("evidence_label") != EVIDENCE_LABELS[plan["mode"]]:
        raise ValueError("resolved plan evidence label differs from execution policy")
    expected_policy = {
        "network_authorization_required": True,
        "automatic_retries": 0,
        "exact_requests_and_raw_final_outputs": True,
        "reasoning_content_retained": False,
        "standalone_grader": True,
    }
    if plan.get("execution_policy") != expected_policy:
        raise ValueError("resolved plan execution policy differs")
    order = plan.get("schedule", {}).get("execution_order")
    if not isinstance(order, list) or plan.get("expected_calls") != {
        "generator": len(order), "grader": len(order), "maximum_total": len(order) * 2
    }:
        raise ValueError("resolved plan call counts differ from its execution order")
    roles = plan.get("roles")
    if not isinstance(roles, dict) or set(roles) != {"generator", "grader"} or any(
        roles[role].get("context_mode") != "standalone" for role in roles
    ):
        raise ValueError("resolved plan roles must be standalone generator and grader")
    if plan["mode"] == "formal":
        if roles["generator"].get("family") == roles["grader"].get("family"):
            raise ValueError("formal resolved plan requires different declared model families")
        if roles["generator"].get("model") == roles["grader"].get("model"):
            raise ValueError("formal resolved plan requires distinct configured models")
    return copy.deepcopy(envelope)


def load_resolved_plan(path: Path) -> dict[str, Any]:
    return verify_resolved_plan(loads_exact(path.read_bytes(), path))


def public_roles(providers: Mapping[str, ResolvedProvider], plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        role: _public_role(providers[role], plan["plan"]["roles"][role]["renderer"]["id"])
        for role in ("generator", "grader")
    }


def plan_preview(envelope: Mapping[str, Any]) -> dict[str, Any]:
    plan = envelope["plan"]
    return {
        "mode": plan["mode"],
        "formal_execution_enabled": plan["formal_execution_enabled"],
        "cases": plan["selection"]["cases"],
        "variants": plan["selection"]["variants"],
        "roles": plan["roles"],
        "repetitions": plan["schedule"]["repetitions"],
        "variant_order_by_repetition": plan["schedule"]["variant_order_by_repetition"],
        "expected_calls": plan["expected_calls"],
        "evidence_label": plan["evidence_label"],
        "output_root": plan["output_root"],
        "resolved_plan_sha256": envelope["resolved_plan_sha256"],
    }
