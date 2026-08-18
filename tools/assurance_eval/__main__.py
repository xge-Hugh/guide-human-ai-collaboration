"""Command-line entry point for a no-network Stage 1 pipeline run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import ProviderDescriptor, ProviderResponse, RunConfig
from .providers import ScriptedFakeProvider
from .runner import AssuranceEvalRunner


def _read_required(path: Path) -> str:
    value = path.read_text(encoding="utf-8")
    if not value.strip():
        raise ValueError(f"{path} is empty")
    return value


def _comma_separated(value: str) -> tuple[str, ...]:
    values = tuple(item.strip() for item in value.split(",") if item.strip())
    if not values:
        raise argparse.ArgumentTypeError("provide at least one comma-separated value")
    return values


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the assurance Phase B pipeline with fake, no-network providers."
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--base-instructions-file", required=True, type=Path)
    parser.add_argument("--grader-instructions-file", required=True, type=Path)
    parser.add_argument("--grader-context-file", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=_comma_separated)
    parser.add_argument("--variants", default=("B0", "B1", "B2"), type=_comma_separated)
    parser.add_argument("--repetitions", default=3, type=int)
    parser.add_argument("--max-retries", default=0, type=int)
    return parser


def main() -> int:
    args = _parser().parse_args()
    call_count = len(args.cases) * len(args.variants) * args.repetitions
    generator_response = ProviderResponse(
        raw_output="FAKE generator output; no model or network was used.",
        actual_model="fake-generator-v1",
    )
    fake_grade = json.dumps(
        {
            "applicability": "uncertain",
            "applicability_basis": "Synthetic Stage 1 result; not experimental evidence.",
            "timing": "too_late",
            "satisfaction": "unsatisfied",
            "human_compensation_needed": "unclear",
            "over_trigger_cost": "none",
            "notes": "Pipeline fixture only.",
        }
    )
    grader_response = ProviderResponse(fake_grade, "fake-grader-v1")
    generator = ScriptedFakeProvider(
        ProviderDescriptor("fake", "fake-generator-v1", "standalone", {"network": False}),
        [generator_response] * call_count,
    )
    grader = ScriptedFakeProvider(
        ProviderDescriptor("fake", "fake-grader-v1", "standalone", {"network": False}),
        [grader_response] * call_count,
    )
    repo_root = Path(__file__).resolve().parents[2]
    config = RunConfig(
        output_root=args.output_dir,
        base_generator_instruction=_read_required(args.base_instructions_file),
        grader_instruction=_read_required(args.grader_instructions_file),
        grader_normative_context=_read_required(args.grader_context_file),
        case_ids=args.cases,
        variant_ids=args.variants,
        run_mode="fake_pipeline",
        repetitions=args.repetitions,
        max_retries=args.max_retries,
    )
    run_dir = AssuranceEvalRunner(repo_root, generator, grader).run(config)
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
