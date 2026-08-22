"""Human-facing validate / plan / run / report workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_model_catalog
from .execution import execute_resolved_plan
from .experiment import load_experiment
from .planning import build_resolved_plan, load_resolved_plan, plan_preview
from .reporting import inspect_case, load_report


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
    run = commands.add_parser("run", help="Resolve once and execute with explicit network authorization.")
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--plan", type=Path, help="Exploratory compatibility path for an existing plan.")
    source.add_argument("--recipe", type=Path)
    run.add_argument("--settings", required=True, type=Path)
    run.add_argument("--profile", help="Required with --recipe; resolved plans carry their profile.")
    run.add_argument("--mode", choices=("exploratory", "formal"), default="exploratory")
    run.add_argument("--authorize-network", action="store_true")
    run.add_argument("--tranche", help="Operational tranche ID; required for tranche-controlled formal plans.")
    run.add_argument("--prior-run", type=Path, help="Completed prior-tranche run required for formal continuation.")
    run.add_argument("--resume-from", type=Path, help="Prior episode run directory to continue without mutating it.")
    run.add_argument("--grader-parallelism", type=int, help="Override grader worker count for this run.")
    report = commands.add_parser("report", help="Inspect a completed or blocked run; no network.")
    report.add_argument("run_dir", type=Path)
    report.add_argument("--case", dest="case_id", help="Show record-level evidence for one case ID.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "report":
        value = inspect_case(args.run_dir, args.case_id) if args.case_id else load_report(args.run_dir)
        print(json.dumps(value, ensure_ascii=False, indent=2))
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
        print(json.dumps(plan_preview(envelope), ensure_ascii=False, indent=2))
        return 0
    if args.plan is not None:
        envelope = load_resolved_plan(args.plan)
        if envelope["plan"]["mode"] == "formal":
            raise ValueError("formal runs must resolve --recipe and --profile at run start")
        recipe_path = Path(envelope["plan"]["recipe"]["path"])
        if not recipe_path.is_absolute():
            recipe_path = REPO_ROOT / recipe_path
        experiment = load_experiment(REPO_ROOT, recipe_path)
        resolved = catalog.resolve(
            envelope["plan"]["profile"],
            {role: envelope["plan"]["roles"][role]["parameters"] for role in ("generator", "grader")},
        )
    else:
        if not args.profile:
            raise ValueError("--profile is required with --recipe")
        experiment = load_experiment(REPO_ROOT, args.recipe)
        envelope, resolved = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=catalog,
            profile=args.profile, mode=args.mode,
        )
    run_dir = execute_resolved_plan(
        repo_root=REPO_ROOT, envelope=envelope, catalog=catalog,
        experiment=experiment, resolved=resolved, authorize_network=args.authorize_network,
        tranche_id=args.tranche, prior_run=args.prior_run,
        resume_from=args.resume_from, grader_parallelism=args.grader_parallelism,
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
