"""Human-facing validate / plan / run / report workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .artifacts import write_new_json
from .config import load_model_catalog
from .execution import execute_resolved_plan
from .experiment import load_experiment
from .planning import build_resolved_plan, load_resolved_plan, plan_preview
from .policy import validate_private_output
from .reporting import load_report


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RECIPE = REPO_ROOT / "docs" / "experiments" / "assurance-v2-phase-b.recipe.json"


def _common_recipe(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--recipe", type=Path, default=DEFAULT_RECIPE)
    parser.add_argument("--settings", required=True, type=Path)
    parser.add_argument("--profile", required=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Small, human-operated assurance evaluation harness.")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate recipe, sources, catalog, and profile; no network.")
    _common_recipe(validate)
    validate.add_argument("--mode", choices=("exploratory", "formal"), default="exploratory")
    plan = commands.add_parser("plan", help="Resolve and preview an immutable, secret-free plan; no network.")
    _common_recipe(plan)
    plan.add_argument("--mode", choices=("exploratory", "formal"), required=True)
    plan.add_argument("--freeze", type=Path, help="Write the resolved plan to a new private file.")
    run = commands.add_parser("run", help="Execute a resolved plan with explicit network authorization.")
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--plan", type=Path)
    source.add_argument("--recipe", type=Path)
    run.add_argument("--settings", required=True, type=Path)
    run.add_argument("--profile", help="Required with --recipe; frozen plans carry their profile.")
    run.add_argument("--authorize-network", action="store_true")
    run.add_argument("--approve-plan-sha256")
    run.add_argument("--tranche", help="Operational tranche ID; required for tranche-controlled formal plans.")
    run.add_argument("--prior-run", type=Path, help="Completed prior-tranche run required for formal continuation.")
    report = commands.add_parser("report", help="Inspect a completed run; no network.")
    report.add_argument("run_dir", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "report":
        print(json.dumps(load_report(args.run_dir), ensure_ascii=False, indent=2))
        return 0
    catalog = load_model_catalog(args.settings, REPO_ROOT)
    if args.command == "validate":
        experiment = load_experiment(REPO_ROOT, args.recipe)
        build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=catalog,
            profile=args.profile, mode=args.mode,
        )
        print(json.dumps({"status": "valid", "experiment_id": experiment.recipe["experiment_id"], "profile": args.profile, "mode": args.mode, "network_calls": 0}, ensure_ascii=False, indent=2))
        return 0
    if args.command == "plan":
        experiment = load_experiment(REPO_ROOT, args.recipe)
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=catalog, profile=args.profile, mode=args.mode)
        if args.mode == "formal" and args.freeze is None:
            raise ValueError("formal planning requires --freeze")
        if args.freeze is not None:
            parent = validate_private_output(args.freeze.parent, REPO_ROOT, must_exist=True)
            write_new_json(parent / args.freeze.name, envelope)
        print(json.dumps(plan_preview(envelope), ensure_ascii=False, indent=2))
        return 0
    if args.plan is not None:
        envelope = load_resolved_plan(args.plan)
    else:
        if not args.profile:
            raise ValueError("--profile is required with --recipe")
        experiment = load_experiment(REPO_ROOT, args.recipe)
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=catalog, profile=args.profile, mode="exploratory")
    run_dir = execute_resolved_plan(
        repo_root=REPO_ROOT, envelope=envelope, catalog=catalog,
        authorize_network=args.authorize_network, approved_plan_sha256=args.approve_plan_sha256,
        tranche_id=args.tranche, prior_run=args.prior_run,
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
