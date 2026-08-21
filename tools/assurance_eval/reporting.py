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
    completed_path = run_dir / "completed.json"
    summary = loads_exact(summary_path.read_bytes(), summary_path)
    completed = loads_exact(completed_path.read_bytes(), completed_path)
    digest = plan["resolved_plan_sha256"]
    if summary.get("resolved_plan_sha256") != digest or completed.get("resolved_plan_sha256") != digest:
        raise ValueError("run artifacts disagree on the resolved-plan hash")
    actual_tree = tree_sha256(run_dir, exclude=("completed.json",))
    if completed.get("artifact_tree_sha256") != actual_tree:
        raise ValueError("run artifact tree differs from the completion digest")
    if completed.get("secret_scan") != "pass":
        raise ValueError("run did not complete with a passing secret scan")
    return {
        "run_id": summary["run_id"],
        "mode": summary["mode"],
        "evidence_label": summary["evidence_label"],
        "resolved_plan_sha256": summary["resolved_plan_sha256"],
        "execution_scope": summary["execution_scope"],
        "planned_calls": summary["planned_calls"],
        "actual_calls": summary["actual_calls"],
        "generation": summary["generation"],
        "grading": summary["grading"],
        "secret_scan": completed["secret_scan"],
        "interpretation": summary["interpretation"],
    }
