from __future__ import annotations

import json
import tempfile
import unittest
from itertools import count
from pathlib import Path

from tools.assurance_eval import (
    AssuranceEvalRunner,
    ProviderDescriptor,
    ProviderError,
    ProviderResponse,
    RunConfig,
    ScriptedFakeProvider,
)
from tools.assurance_eval.loading import load_phase_b_inputs
from tools.assurance_eval.runner import _parse_grade


REPO_ROOT = Path(__file__).resolve().parents[1]


def valid_grade(**overrides: str) -> str:
    grade = {
        "applicability": "applicable",
        "applicability_basis": "The response addressed the protected boundary.",
        "timing": "on_time",
        "satisfaction": "satisfied",
        "human_compensation_needed": "no",
        "over_trigger_cost": "none",
        "notes": "fake grade",
    }
    grade.update(overrides)
    return json.dumps(grade, ensure_ascii=False)


class RunnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_root = Path(self.temp_dir.name)
        self.id_counter = count(1)

    def new_id(self) -> str:
        return f"id-{next(self.id_counter):03d}"

    def config(self, **overrides: object) -> RunConfig:
        values = {
            "output_root": self.output_root,
            "base_generator_instruction": "COMMON BASE",
            "grader_instruction": "GRADE EACH AXIS; RETURN JSON",
            "grader_normative_context": "SYNTHETIC NORMATIVE CONTEXT",
            "case_ids": ("p001",),
            "variant_ids": ("B0",),
            "run_mode": "fake_pipeline",
            "generator_base_language": "en",
            "case_packet_language": "zh-CN",
            "variant_condition_language": "none",
            "grader_instruction_language": "en",
            "grader_context_language": "zh-CN",
            "repetitions": 1,
            "max_retries": 0,
        }
        values.update(overrides)
        return RunConfig(**values)  # type: ignore[arg-type]

    @staticmethod
    def descriptor(role: str) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider="fake",
            configured_model=f"fake-{role}",
            context_mode="standalone",
            public_parameters={"temperature": 0.2, "reasoning": "none"},
            uncontrolled_parameters=("backend_seed",),
        )

    def test_loads_checked_in_packets_and_rejects_unknown_selection(self) -> None:
        inputs = load_phase_b_inputs(REPO_ROOT)
        self.assertEqual(set(inputs.generation), set(inputs.rubrics))
        self.assertEqual(set(inputs.variants), {"B0", "B1", "B2"})
        for source in inputs.source_files.values():
            self.assertEqual(len(source["sha256"]), 64)

        generator = ScriptedFakeProvider(
            self.descriptor("generator"), [ProviderResponse("unused", "fake-generator")]
        )
        grader = ScriptedFakeProvider(
            self.descriptor("grader"), [ProviderResponse(valid_grade(), "fake-grader")]
        )
        runner = AssuranceEvalRunner(REPO_ROOT, generator, grader, new_id=self.new_id)
        with self.assertRaisesRegex(ValueError, "unknown selections"):
            runner.run(self.config(case_ids=("missing",)))
        self.assertFalse(any(self.output_root.iterdir()))

    def test_not_applicable_grade_requires_conditional_na_axes(self) -> None:
        parsed = _parse_grade(
            valid_grade(
                applicability="not_applicable",
                timing="not_applicable",
                satisfaction="not_applicable",
                over_trigger_cost="none",
                human_compensation_needed="no",
            )
        )
        self.assertEqual(parsed["applicability"], "not_applicable")
        for invalid in (
            valid_grade(applicability="not_applicable"),
            valid_grade(timing="not_applicable", satisfaction="not_applicable"),
        ):
            with self.assertRaisesRegex(ValueError, "exactly when applicability"):
                _parse_grade(invalid)

    def test_isolates_variants_rubrics_and_repetitions(self) -> None:
        inputs = load_phase_b_inputs(REPO_ROOT)

        def generator_reply(request: object) -> ProviderResponse:
            request_dict = dict(request)  # type: ignore[arg-type]
            return ProviderResponse(
                raw_output=f"  raw::{request_dict['context_id']}::响应\n",
                provider_reported_model="fake-generator-snapshot",
                public_metadata={"finish_reason": "stop"},
            )

        call_count = 6
        generator = ScriptedFakeProvider(
            self.descriptor("generator"), [generator_reply] * call_count
        )
        grader = ScriptedFakeProvider(
            self.descriptor("grader"),
            [ProviderResponse(valid_grade(), "fake-grader-snapshot")] * call_count,
        )
        runner = AssuranceEvalRunner(
            REPO_ROOT,
            generator,
            grader,
            now=lambda: "2026-08-19T00:00:00+00:00",
            new_id=self.new_id,
        )
        run_dir = runner.run(
            self.config(
                variant_ids=("B0", "B1", "B2"),
                variant_condition_language="en",
                repetitions=2,
            )
        )

        self.assertEqual(len(generator.calls), call_count)
        self.assertEqual(len(grader.calls), call_count)
        generator_json = json.dumps(generator.calls, ensure_ascii=False)
        self.assertNotIn("expected_applicability", generator_json)
        self.assertNotIn("required_protection", generator_json)
        self.assertNotIn("latest_useful_point", generator_json)
        self.assertNotIn("reference_case", generator_json)

        contexts = [call["context_id"] for call in generator.calls]
        self.assertEqual(len(contexts), len(set(contexts)))
        for call in generator.calls:
            self.assertEqual(call["call_kind"], "generator")
            self.assertEqual(
                call["packet"],
                {
                    "case_id": "p001",
                    "pre_context": inputs.generation["p001"]["pre_context"],
                    "user_message": inputs.generation["p001"]["user_message"],
                },
            )

        b0_calls = [call for call in generator.calls if call["system_instruction"] == "COMMON BASE"]
        self.assertEqual(len(b0_calls), 2)
        for variant_id in ("B1", "B2"):
            expected = "COMMON BASE\n\n" + inputs.variants[variant_id]["instruction_append"]
            self.assertEqual(
                sum(call["system_instruction"] == expected for call in generator.calls), 2
            )

        for generator_call, grader_call in zip(generator.calls, grader.calls):
            self.assertNotEqual(generator_call["context_id"], grader_call["context_id"])
            self.assertEqual(grader_call["call_kind"], "grader")
            self.assertEqual(
                grader_call["packet"]["reference_semantic_boundary"],
                inputs.rubrics["p001"],
            )
            expected_raw = f"  raw::{generator_call['context_id']}::响应\n"
            self.assertEqual(grader_call["packet"]["raw_generator_output"], expected_raw)

        records = sorted((run_dir / "records").glob("*.json"))
        self.assertEqual(len(records), call_count)
        saved = [json.loads(path.read_text(encoding="utf-8")) for path in records]
        self.assertEqual(
            {record["repetition"] for record in saved if record["variant_id"] == "B0"},
            {1, 2},
        )
        for record in saved:
            self.assertEqual(
                record["generator"]["raw_output"],
                f"  raw::{record['context_id']}::响应\n",
            )
            self.assertIn("axis_results", record["grader"])
            self.assertEqual(
                record["generator"]["model_identity"],
                {
                    "configured_model": "fake-generator",
                    "declared_model_snapshot": None,
                    "provider_reported_model": "fake-generator-snapshot",
                },
            )

        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["record_count"], call_count)
        self.assertEqual(summary["generation"], {"succeeded": call_count})
        self.assertEqual(summary["grading"], {"succeeded": call_count})
        self.assertEqual(len(summary["groups"]), 3)
        self.assertTrue(all(len(group["repetitions"]) == 2 for group in summary["groups"]))
        self.assertEqual(len(summary["records"]), call_count)
        self.assertNotIn("raw_output", json.dumps(summary))
        self.assertTrue(all(path.exists() for path in records))
        self.assertEqual(len(list((run_dir / "call_evidence").glob("*.json"))), call_count * 2)
        self.assertTrue((run_dir / "completed.json").is_file())
        manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["run_mode"], "fake_pipeline")
        self.assertEqual(manifest["evidence_use"], "not_experimental_evidence")
        self.assertEqual(
            manifest["config"]["language_components"],
            {
                "generator_base": "en",
                "case_packet": "zh-CN",
                "variant_condition": "en",
                "grader_instruction": "en",
                "grader_context": "zh-CN",
            },
        )
        self.assertIn("runner_source_sha256", manifest["runner_provenance"])

    def test_records_failures_retries_and_unparsed_grader_output(self) -> None:
        generator = ScriptedFakeProvider(
            self.descriptor("generator"),
            [ProviderError("transient", retryable=True), ProviderResponse("RAW", "actual-generator")],
        )
        grader = ScriptedFakeProvider(
            self.descriptor("grader"), [ProviderResponse("not json", "actual-grader")]
        )
        runner = AssuranceEvalRunner(
            REPO_ROOT, generator, grader, new_id=self.new_id, now=lambda: "timestamp"
        )
        run_dir = runner.run(self.config(max_retries=1))
        record_path = next((run_dir / "records").iterdir())
        record = json.loads(record_path.read_text(encoding="utf-8"))

        self.assertEqual(record["generator"]["invocation_status"], "succeeded")
        self.assertEqual(record["generator"]["retry_count"], 1)
        self.assertEqual(record["generator"]["attempts"][0]["error"]["type"], "ProviderError")
        self.assertEqual(record["generator"]["raw_output"], "RAW")
        self.assertEqual(record["grader"]["invocation_status"], "succeeded")
        self.assertEqual(record["grader"]["grade_parse_status"], "invalid")
        self.assertEqual(record["grader"]["raw_output"], "not json")
        self.assertIn("parse_error", record["grader"])

        summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["generation"], {"succeeded": 1})
        self.assertEqual(summary["grading"], {"invalid_output": 1})

    def test_records_numeric_elapsed_time_for_each_attempt(self) -> None:
        ticks = iter((10.0, 10.125, 20.0, 20.25))
        generator = ScriptedFakeProvider(
            self.descriptor("generator"), [ProviderResponse("RAW", "actual-generator")]
        )
        grader = ScriptedFakeProvider(
            self.descriptor("grader"), [ProviderResponse(valid_grade(), "actual-grader")]
        )
        runner = AssuranceEvalRunner(
            REPO_ROOT,
            generator,
            grader,
            new_id=self.new_id,
            now=lambda: "timestamp",
            monotonic=lambda: next(ticks),
        )
        run_dir = runner.run(self.config())
        record = json.loads(next((run_dir / "records").iterdir()).read_text())

        self.assertEqual(record["generator"]["elapsed_ms"], 125.0)
        self.assertEqual(record["generator"]["attempts"][0]["elapsed_ms"], 125.0)
        self.assertEqual(record["grader"]["elapsed_ms"], 250.0)
        self.assertEqual(record["grader"]["attempts"][0]["elapsed_ms"], 250.0)

    def test_requires_providers_to_declare_standalone_contexts(self) -> None:
        provider = ScriptedFakeProvider(
            ProviderDescriptor("fake", "stateful", "stateful"),
            [ProviderResponse("unused", "shared")],
        )
        grader = ScriptedFakeProvider(
            self.descriptor("grader"), [ProviderResponse(valid_grade(), "grader")]
        )
        with self.assertRaisesRegex(ValueError, "standalone context mode"):
            AssuranceEvalRunner(REPO_ROOT, provider, grader)

    def test_does_not_allow_english_variants_to_be_labeled_chinese(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not match the selected variant source"):
            self.config(
                variant_ids=("B1",), variant_condition_language="zh-CN"
            ).validate()


if __name__ == "__main__":
    unittest.main()
