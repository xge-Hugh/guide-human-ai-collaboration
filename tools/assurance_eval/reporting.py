"""Offline run reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import tree_sha256
from .experiment import loads_exact
from .planning import load_resolved_plan


def load_report(run_dir: Path) -> dict[str, Any]:
    plan = load_resolved_plan(run_dir / "resolved_plan.json")
    summary_path = run_dir / "summary.json"
    status_path = run_dir / "run_status.json"
    if not status_path.is_file():
        status_path = run_dir / "completed.json"
    summary = loads_exact(summary_path.read_bytes(), summary_path)
    status = loads_exact(status_path.read_bytes(), status_path)
    digest = plan["resolved_plan_sha256"]
    if summary.get("resolved_plan_sha256") != digest or status.get("resolved_plan_sha256") != digest:
        raise ValueError("run artifacts disagree on the resolved-plan hash")
    actual_tree = tree_sha256(run_dir, exclude=(status_path.name,))
    if status.get("artifact_tree_sha256") != actual_tree:
        raise ValueError("run artifact tree differs from the finalization digest")
    if status.get("secret_scan") != "pass":
        raise ValueError("run was not finalized with a passing secret scan")
    operational_status = status.get("operational_status", summary.get("operational_status", "completed"))
    groups = summary.get("groups", [])
    return {
        "run_id": summary["run_id"],
        "mode": summary["mode"],
        "evidence_label": summary["evidence_label"],
        "resolved_plan_sha256": summary["resolved_plan_sha256"],
        "execution_scope": summary["execution_scope"],
        "planned_calls": summary["planned_calls"],
        "actual_calls": summary["actual_calls"],
        "network_calls": status.get("network_calls"),
        "generation": summary["generation"],
        "grading": summary["grading"],
        "operational_status": operational_status,
        "blocked_reason": status.get("blocked_reason", summary.get("blocked_reason")),
        "groups": groups,
        "requires_human_adjudication": any(
            group.get("requires_human_adjudication") is True for group in groups
        ),
        "secret_scan": status["secret_scan"],
        "interpretation": summary["interpretation"],
    }


def inspect_case(run_dir: Path, case_id: str) -> dict[str, Any]:
    report = load_report(run_dir)
    flags = {
        (group["case_id"], group["variant_id"]): group["requires_human_adjudication"]
        for group in report["groups"]
    }
    records: list[dict[str, Any]] = []
    for path in sorted((run_dir / "records").glob(f"{case_id}__*.json")):
        record = loads_exact(path.read_bytes(), path)
        generator = record["generator"]
        grader = record["grader"]
        records.append(
            {
                "case_id": record["case_id"],
                "variant_id": record["variant_id"],
                "repetition": record["repetition"],
                "generator_final_response": generator.get("raw_output"),
                "grader_raw_output": grader.get("raw_output") if grader else None,
                "grader_axis_judgments": grader.get("axis_results") if grader else None,
                "call_status": {
                    "generator": {
                        "invocation": generator["invocation_status"],
                        "error": generator.get("error"),
                    },
                    "grader": {
                        "invocation": grader["invocation_status"],
                        "grade_parse": grader.get("grade_parse_status"),
                        "parse_error": grader.get("parse_error"),
                        "error": grader.get("error"),
                    } if grader else None,
                },
                "model_identities": {
                    "generator": {
                        "configured": generator["provider"]["configured_model"],
                        "provider_reported": generator.get("provider_reported_model"),
                    },
                    "grader": {
                        "configured": grader["provider"]["configured_model"] if grader else None,
                        "provider_reported": grader.get("provider_reported_model") if grader else None,
                    },
                },
                "token_usage": {
                    "generator": generator.get("public_response_metadata", {}).get("usage"),
                    "grader": grader.get("public_response_metadata", {}).get("usage") if grader else None,
                },
                "elapsed_ms": {
                    "generator": generator.get("elapsed_ms"),
                    "grader": grader.get("elapsed_ms") if grader else None,
                },
                "operational_status": record.get("operational_status", "completed"),
                "blocked_reason": record.get("blocked_reason"),
                "requires_human_adjudication": flags.get(
                    (record["case_id"], record["variant_id"]), True
                ),
                "artifact_path": str(path),
                "call_evidence_paths": {
                    "generator": str(run_dir / "call_evidence" / f"{path.stem}__generator.json"),
                    "grader": str(run_dir / "call_evidence" / f"{path.stem}__grader.json") if grader else None,
                },
            }
        )
    if not records:
        raise ValueError(f"case {case_id!r} has no records in this run")
    return {
        "run_id": report["run_id"],
        "operational_status": report["operational_status"],
        "case_id": case_id,
        "records": records,
    }
