from __future__ import annotations

import copy
import io
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from tools.assurance_eval.config import load_model_catalog
from tools.assurance_eval.__main__ import main
from tools.assurance_eval.execution import _formal_blocking_reason, _summary, execute_resolved_plan
from tools.assurance_eval.experiment import canonical_json, load_experiment, sha256_bytes
from tools.assurance_eval.grading import build_grader_packet, parse_grade
from tools.assurance_eval.planning import build_resolved_plan, plan_preview, verify_resolved_plan
from tools.assurance_eval.renderers import GENERATOR_ID, GRADER_ID, render_generator, render_grader
from tools.assurance_eval.reporting import inspect_case, load_report


REPO_ROOT = Path(__file__).resolve().parents[1]
RECIPE = REPO_ROOT / "docs" / "experiments" / "assurance-v2-phase-b.recipe.json"


def grade_json() -> str:
    return json.dumps(
        {
            "applicability": "applicable",
            "applicability_basis": "Synthetic transport fixture.",
            "timing": "on_time",
            "satisfaction": "satisfied",
            "human_compensation_needed": "no",
            "over_trigger_cost": "none",
            "notes": "not experimental evidence",
        }
    )


class HarnessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.settings = self.root / "setting.json"
        self.settings.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "connections": {
                        "route": {
                            "provider": "custom",
                            "api_style": "openai_chat_completions",
                            "base_url": "https://private.example.invalid",
                            "api_key": "test-secret-key",
                        }
                    },
                    "models": {
                        "gen": {"connection": "route", "model_id": "generator-test", "family": "FamilyG", "declared_snapshot": None},
                        "judge": {"connection": "route", "model_id": "grader-test", "family": "FamilyR", "declared_snapshot": None},
                    },
                    "profiles": {"test": {"roles": {"generator": "gen", "grader": "judge"}}},
                }
            ),
            encoding="utf-8",
        )
        os.chmod(self.settings, 0o600)
        self.catalog = load_model_catalog(self.settings, REPO_ROOT)

    def small_experiment(
        self, output_root: Path, *, cases: list[str] | None = None,
        formal_execution_enabled: bool = False,
    ):
        recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
        experiment_dir = REPO_ROOT / "docs" / "experiments"
        recipe["sources"] = {
            "generation": str(experiment_dir / "assurance-v2-phase-b-generation.json"),
            "variants": str(experiment_dir / "assurance-v2-phase-b-variants.zh-CN.json"),
            "rubrics": str(experiment_dir / "assurance-v2-phase-b-rubrics.json"),
        }
        recipe["selection"] = {"cases": cases or ["p003"], "variants": ["B0"]}
        recipe["schedule"] = {"repetitions": 1, "variant_order_by_repetition": [["B0"]]}
        recipe["formal_execution_enabled"] = formal_execution_enabled
        recipe["output_root"] = str(output_root)
        path = self.root / "small.recipe.json"
        path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        return load_experiment(REPO_ROOT, path)

    def test_checked_in_recipe_preserves_stage3_semantics(self) -> None:
        experiment = load_experiment(REPO_ROOT, RECIPE)
        recipe = experiment.recipe
        self.assertFalse(recipe["formal_execution_enabled"])
        self.assertEqual(recipe["selection"]["cases"], ["p003", "p004", "p005", "p006", "p007", "p008", "p009", "p011", "p012", "p013"])
        self.assertEqual(recipe["selection"]["variants"], ["B0", "B1", "B2"])
        self.assertEqual(recipe["schedule"]["variant_order_by_repetition"], [["B0", "B1", "B2"], ["B1", "B2", "B0"], ["B2", "B0", "B1"]])
        self.assertEqual(recipe["parameters"]["generator"], {"thinking": {"type": "enabled"}, "max_tokens": 4096, "stream": False})
        self.assertEqual(recipe["parameters"]["grader"], {"thinking": {"type": "disabled"}, "max_tokens": 1024, "stream": False})
        self.assertEqual(recipe["schedule"]["operational_tranches"]["tranche_1"]["repetitions"], [1])
        self.assertEqual(recipe["grading"]["interpretation"], {
            "not_a_total_score": True,
            "unresolved_grades_not_favorable": True,
            "preserve_original_grader_judgments_after_adjudication": True,
            "automatic_variant_winner_or_pass_fail": False,
        })
        self.assertEqual(experiment.variants["B0"]["instruction_append"], "")
        chinese = json.loads((RECIPE.parent / recipe["sources"]["variants"]).read_text(encoding="utf-8"))
        self.assertEqual(experiment.variants["B2"]["instruction_append"], f'{experiment.variants["B1"]["instruction_append"]}\n\n{chinese["b2_semantic_frame_append"]}')

    def test_consumed_compatibility_configs_are_historical_and_disabled(self) -> None:
        for name in (
            "assurance-v2-thinking-compatibility-smoke.json",
            "assurance-v2-direct-grader-compatibility-smoke.json",
        ):
            value = json.loads((RECIPE.parent / name).read_text(encoding="utf-8"))
            self.assertEqual(value["status"], "historical_completed")
            self.assertFalse(value["execution_enabled"])

    def test_plan_is_secret_free_complete_and_zero_network(self) -> None:
        experiment = load_experiment(REPO_ROOT, RECIPE)
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        preview = plan_preview(envelope)
        self.assertEqual(preview["expected_calls"], {"generator": 90, "grader": 90, "maximum_total": 180})
        self.assertEqual(preview["roles"]["generator"]["model"], "generator-test")
        self.assertEqual(preview["roles"]["grader"]["family"], "FamilyR")
        self.assertEqual(preview["roles"]["generator"]["renderer"]["id"], GENERATOR_ID)
        self.assertEqual(preview["roles"]["grader"]["renderer"]["id"], GRADER_ID)
        self.assertRegex(preview["roles"]["generator"]["renderer"]["sha256"], r"^[0-9a-f]{64}$")
        serialized = json.dumps(envelope)
        self.assertNotIn("test-secret-key", serialized)
        self.assertNotIn("private.example.invalid", serialized)
        self.assertEqual(verify_resolved_plan(envelope), envelope)

    def test_validate_and_plan_cli_are_offline_and_human_readable(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["validate", "--settings", str(self.settings), "--profile", "test"]), 0)
            self.assertEqual(main(["plan", "--settings", str(self.settings), "--profile", "test", "--mode", "exploratory"]), 0)
        text = output.getvalue()
        self.assertIn('"network_calls": 0', text)
        self.assertIn('"expected_calls"', text)
        self.assertIn('"resolved_plan_sha256"', text)
        self.assertNotIn("test-secret-key", text)
        self.assertNotIn("private.example.invalid", text)

    def test_plan_hash_detects_any_resolved_plan_mutation(self) -> None:
        experiment = self.small_experiment(self.root / "output")
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        changed = copy.deepcopy(envelope)
        changed["plan"]["roles"]["generator"]["parameters"]["max_tokens"] = 1
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            verify_resolved_plan(changed)

    def test_rehashed_noncanonical_plan_is_rejected_before_calls(self) -> None:
        experiment = self.small_experiment(self.root / "output")
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        changed = copy.deepcopy(envelope)
        changed["plan"]["instructions"]["generator_base"] = "mutated after planning"
        changed["resolved_plan_sha256"] = sha256_bytes(canonical_json(changed["plan"]))
        calls = []
        resolved = self.catalog.resolve("test", experiment.recipe["parameters"])
        with self.assertRaisesRegex(ValueError, "canonical projection"):
            execute_resolved_plan(repo_root=REPO_ROOT, envelope=changed, catalog=self.catalog, experiment=experiment, resolved=resolved, authorize_network=True, transport=lambda *args: calls.append(args))
        self.assertEqual(calls, [])

    def test_formal_plan_requires_clean_provenance_and_distinct_families(self) -> None:
        experiment = self.small_experiment(self.root / "output")
        with patch("tools.assurance_eval.planning.git_provenance", return_value={"available": True, "git_revision": "abc", "clean": False, "status_sha256": "x"}):
            with self.assertRaisesRegex(ValueError, "clean committed"):
                build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="formal")
        clean = {"available": True, "git_revision": "abc", "clean": True, "status_sha256": "x", "harness_source_sha256": "x"}
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean):
            with self.assertRaisesRegex(ValueError, "committed repository files"):
                build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="formal")

    def test_renderers_keep_rubric_out_of_generator_and_grader_standalone(self) -> None:
        experiment = load_experiment(REPO_ROOT, RECIPE)
        generator_request = {
            "call_kind": "generator", "context_id": "generator-context", "variant_id": "B0",
            "system_instruction": "base", "packet": {"case_id": "p003", "pre_context": "before", "user_message": "now"},
        }
        rendered_generator = render_generator(generator_request, {"thinking": {"type": "enabled"}, "stream": False})
        serialized = json.dumps(rendered_generator, ensure_ascii=False)
        for field in ("expected_applicability", "required_protection", "latest_useful_point", "adjudication"):
            self.assertNotIn(field, serialized)
        packet = build_grader_packet(case_id="p003", rubric=experiment.rubrics["p003"], generator_output="raw final", grading=experiment.recipe["grading"])
        rendered_grader = render_grader({"call_kind": "grader", "context_id": "grader-context", "packet": packet}, {"thinking": {"type": "disabled"}, "stream": False})
        self.assertIn("raw final", rendered_grader["messages"][1]["content"])
        self.assertNotIn("generator-context", json.dumps(rendered_grader))

    def test_grading_rejects_duplicate_keys_and_invalid_na(self) -> None:
        grading = load_experiment(REPO_ROOT, RECIPE).recipe["grading"]
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            parse_grade('{"applicability":"applicable","applicability":"uncertain"}', grading)
        invalid = json.loads(grade_json())
        invalid.update({"applicability": "not_applicable", "timing": "on_time", "satisfaction": "not_applicable"})
        with self.assertRaisesRegex(ValueError, "exactly when"):
            parse_grade(json.dumps(invalid), grading)

    def test_uncertain_or_disagreeing_grades_require_human_adjudication(self) -> None:
        experiment = self.small_experiment(self.root / "summary-output")
        envelope, _ = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        first = json.loads(grade_json())
        first["applicability"] = "uncertain"
        second = json.loads(grade_json())
        records = []
        for grade in (first, second):
            records.append({
                "case_id": "p003", "variant_id": "B0",
                "generator": {"invocation_status": "succeeded"},
                "grader": {"invocation_status": "succeeded", "grade_parse_status": "parsed", "axis_results": grade},
            })
        group = _summary("run", envelope, records, {"tranche_id": None, "record_count": 2}, "completed", None)["groups"][0]
        self.assertTrue(group["requires_human_adjudication"])

    def test_recipe_parameters_cannot_override_renderer_messages(self) -> None:
        recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
        recipe["parameters"]["generator"]["messages"] = [{"role": "system", "content": "rubric leak"}]
        path = self.root / "bad-parameters.recipe.json"
        recipe["sources"] = {key: str(RECIPE.parent / value) for key, value in recipe["sources"].items()}
        path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "renderer-owned"):
            load_experiment(REPO_ROOT, path)

    def test_private_catalog_values_cannot_enter_a_resolved_plan(self) -> None:
        recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
        recipe["instructions"]["generator_base"] = "accidentally included test-secret-key"
        recipe["sources"] = {key: str(RECIPE.parent / value) for key, value in recipe["sources"].items()}
        recipe["selection"] = {"cases": ["p003"], "variants": ["B0"]}
        recipe["schedule"] = {"repetitions": 1, "variant_order_by_repetition": [["B0"]]}
        recipe["output_root"] = str(self.root / "private-plan-output")
        path = self.root / "secret-plan.recipe.json"
        path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        experiment = load_experiment(REPO_ROOT, path)
        with self.assertRaisesRegex(ValueError, "private catalog value"):
            build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")

    def test_exploratory_execution_records_evidence_without_secrets_or_reasoning(self) -> None:
        output = self.root / "output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        requests: list[dict[str, object]] = []

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            request = json.loads(body)
            requests.append(request)
            if len(requests) == 1:
                envelope["plan"]["schedule"]["execution_order"].clear()
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({"id": "private-response-id", "model": request["model"] + "-reported", "choices": [{"message": {"content": content, "reasoning_content": "private hidden reasoning"}, "finish_reason": "stop"}], "usage": {"completion_tokens_details": {"reasoning_tokens": 7}}}).encode()

        run_dir = execute_resolved_plan(repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog, experiment=experiment, resolved=resolved, authorize_network=True, transport=transport, new_id=iter(("run", "generator-context", "grader-context")).__next__)
        self.assertEqual(len(requests), 2)
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text(encoding="utf-8"))
        self.assertEqual(record["generator"]["raw_output"], "raw generator response")
        self.assertEqual(record["grader"]["grade_parse_status"], "parsed")
        self.assertNotEqual(record["generator"]["request"]["context_id"], record["grader"]["request"]["context_id"])
        artifact_text = "".join(path.read_text(encoding="utf-8") for path in run_dir.rglob("*.json"))
        for forbidden in ("test-secret-key", "private.example.invalid", "private-response-id", "private hidden reasoning"):
            self.assertNotIn(forbidden, artifact_text)
        def has_reasoning_content_key(value: object) -> bool:
            if isinstance(value, dict):
                return "reasoning_content" in value or any(has_reasoning_content_key(child) for child in value.values())
            if isinstance(value, list):
                return any(has_reasoning_content_key(child) for child in value)
            return False
        for path in run_dir.rglob("*.json"):
            self.assertFalse(has_reasoning_content_key(json.loads(path.read_text(encoding="utf-8"))))
        self.assertEqual(json.loads((run_dir / "run_status.json").read_text())["secret_scan"], "pass")
        report = load_report(run_dir)
        self.assertEqual(report["actual_calls"], {"generator": 1, "grader": 1})
        self.assertEqual(report["network_calls"], 2)
        self.assertEqual(len(report["groups"]), 1)
        detail = inspect_case(run_dir, "p003")["records"][0]
        self.assertEqual(detail["generator_final_response"], "raw generator response")
        self.assertEqual(detail["grader_axis_judgments"]["timing"], "on_time")
        self.assertTrue(detail["artifact_path"].endswith("p003__B0__r001.json"))
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["report", str(run_dir), "--case", "p003"]), 0)
        self.assertIn('"generator_final_response": "raw generator response"', output.getvalue())
        for path in (run_dir, *run_dir.rglob("*")):
            mode = stat.S_IMODE(path.stat().st_mode)
            self.assertFalse(mode & (0o077 if path.is_dir() else 0o177))
        summary_path = run_dir / "summary.json"
        summary = json.loads(summary_path.read_text())
        summary["generation"] = {"succeeded": 999}
        summary_path.write_text(json.dumps(summary), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "artifact tree"):
            load_report(run_dir)

    def test_provider_secret_echo_is_sanitized_before_artifact_write(self) -> None:
        output = self.root / "secret-output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            request = json.loads(body)
            return json.dumps({"model": request["model"], "choices": [{"message": {"content": "provider echoed test-secret-key"}, "finish_reason": "stop"}]}).encode()

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved,
            authorize_network=True, transport=transport,
            new_id=iter(("secret-run", "generator-context")).__next__,
        )
        text = "".join(path.read_text(encoding="utf-8") for path in run_dir.rglob("*.json"))
        self.assertNotIn("test-secret-key", text)
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["error"]["type"], "PrivateValueBlocked")
        self.assertIsNone(record["grader"])

    def test_missing_network_or_disabled_formal_execution_makes_zero_calls(self) -> None:
        output = self.root / "output"
        experiment = self.small_experiment(output)
        calls = []
        envelope, resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        with self.assertRaisesRegex(PermissionError, "network authorization"):
            execute_resolved_plan(repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog, experiment=experiment, resolved=resolved, authorize_network=False, transport=lambda *args: calls.append(args))
        self.assertEqual(calls, [])
        clean = {"available": True, "git_revision": "abc", "clean": True, "status_sha256": sha256_bytes(b""), "harness_source_sha256": "x"}
        checked_in = load_experiment(REPO_ROOT, RECIPE)
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean), patch("tools.assurance_eval.planning.require_committed_paths"):
            formal, formal_resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=checked_in, catalog=self.catalog, profile="test", mode="formal")
        with self.assertRaisesRegex(PermissionError, "formal execution remains disabled"):
            execute_resolved_plan(repo_root=REPO_ROOT, envelope=formal, catalog=self.catalog, experiment=checked_in, resolved=formal_resolved, authorize_network=True, transport=lambda *args: calls.append(args))
        self.assertEqual(calls, [])

    def test_transport_failure_is_recorded_once_without_retry_or_grader(self) -> None:
        output = self.root / "failure-output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        calls = 0

        def failing_transport(*args) -> bytes:
            nonlocal calls
            calls += 1
            from tools.assurance_eval.models import ProviderError
            raise ProviderError("synthetic transport failure")

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved,
            authorize_network=True, transport=failing_transport,
            new_id=iter(("failed-run", "generator-context")).__next__,
        )
        self.assertEqual(calls, 1)
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["attempt_count"], 1)
        self.assertEqual(record["generator"]["retry_count"], 0)
        self.assertIsNone(record["grader"])

    def test_formal_invalid_grader_blocks_run_and_stops_future_calls(self) -> None:
        output = self.root / "formal-output"
        output.mkdir(mode=0o700)
        experiment = self.small_experiment(
            output, cases=["p003", "p004"], formal_execution_enabled=True,
        )
        clean = {
            "available": True, "git_revision": "abc", "clean": True,
            "status_sha256": sha256_bytes(b""), "harness_source_sha256": "harness",
        }
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean), patch(
            "tools.assurance_eval.planning.require_committed_paths"
        ):
            envelope, resolved = build_resolved_plan(
                repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
                profile="test", mode="formal",
            )
        calls = 0

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            nonlocal calls
            calls += 1
            request = json.loads(body)
            content = "raw generator response" if calls == 1 else "not-json"
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            run_dir = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
                experiment=experiment, resolved=resolved, authorize_network=True,
                transport=transport,
                new_id=iter(("formal-blocked", "generator-context", "grader-context")).__next__,
            )
        self.assertEqual(calls, 2)
        self.assertEqual(len(list((run_dir / "records").glob("*.json"))), 1)
        report = load_report(run_dir)
        self.assertEqual(report["operational_status"], "blocked")
        self.assertEqual(report["blocked_reason"]["code"], "invalid_or_unparseable_grader_output")
        self.assertTrue(report["requires_human_adjudication"])
        self.assertEqual(report["planned_calls"], {"generator": 2, "grader": 2, "maximum_total": 4})
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["grader"]["raw_output"], "not-json")
        self.assertEqual(record["grader"]["attempt_count"], 1)
        self.assertEqual(record["grader"]["retry_count"], 0)
        detail = inspect_case(run_dir, "p003")["records"][0]
        self.assertEqual(detail["grader_raw_output"], "not-json")
        self.assertEqual(detail["call_status"]["grader"]["grade_parse"], "invalid")
        self.assertIsNotNone(detail["call_status"]["grader"]["parse_error"])
        self.assertTrue(detail["call_evidence_paths"]["grader"].endswith("__grader.json"))

    def test_formal_blocking_condition_classification_is_centralized(self) -> None:
        failed = {"invocation_status": "failed", "error": {"type": "ProviderError", "message": "transport failed"}}
        self.assertEqual(_formal_blocking_reason("generator", failed)["code"], "generator_transport_or_invocation_failure")
        self.assertEqual(_formal_blocking_reason("grader", failed)["code"], "grader_transport_or_invocation_failure")
        private = {"invocation_status": "failed", "error": {"type": "PrivateValueBlocked", "message": "blocked"}}
        self.assertEqual(_formal_blocking_reason("generator", private)["code"], "secret_or_private_value_blocked")
        provenance = {"invocation_status": "failed", "error": {"type": "ProviderError", "message": "formal provenance changed"}}
        self.assertEqual(_formal_blocking_reason("generator", provenance)["code"], "configuration_or_committed_provenance_mismatch")
        unexpected = {"invocation_status": "failed", "error": {"type": "ProviderError", "message": "provider returned an invalid chat completion"}}
        self.assertEqual(_formal_blocking_reason("grader", unexpected)["code"], "unexpected_provider_response")
        non_stop = {"invocation_status": "succeeded", "public_response_metadata": {"finish_reason": "length"}}
        self.assertEqual(_formal_blocking_reason("generator", non_stop)["code"], "generator_finish_reason_not_stop")
        invalid_grade = {
            "invocation_status": "succeeded", "public_response_metadata": {"finish_reason": "stop"},
            "grade_parse_status": "invalid",
        }
        self.assertEqual(_formal_blocking_reason("grader", invalid_grade)["code"], "invalid_or_unparseable_grader_output")

    def test_formal_unexpected_transport_exception_preserves_sanitized_failed_record(self) -> None:
        output = self.root / "formal-transport-output"
        output.mkdir(mode=0o700)
        experiment = self.small_experiment(output, formal_execution_enabled=True)
        clean = {
            "available": True, "git_revision": "abc", "clean": True,
            "status_sha256": sha256_bytes(b""), "harness_source_sha256": "harness",
        }
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean), patch(
            "tools.assurance_eval.planning.require_committed_paths"
        ):
            envelope, resolved = build_resolved_plan(
                repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
                profile="test", mode="formal",
            )
        calls = 0

        def transport(*args) -> bytes:
            nonlocal calls
            calls += 1
            raise RuntimeError("sensitive adapter details")

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            run_dir = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
                experiment=experiment, resolved=resolved, authorize_network=True,
                transport=transport,
                new_id=iter(("formal-transport-blocked", "generator-context")).__next__,
            )
        self.assertEqual(calls, 1)
        report = load_report(run_dir)
        self.assertEqual(report["operational_status"], "blocked")
        self.assertEqual(report["blocked_reason"]["code"], "generator_transport_or_invocation_failure")
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["error"]["message"], "unexpected provider invocation failure")
        self.assertNotIn("sensitive adapter details", json.dumps(record))
        self.assertEqual(record["generator"]["attempt_count"], 1)
        self.assertEqual(record["generator"]["retry_count"], 0)

    def test_discarded_response_id_does_not_redact_identical_final_response(self) -> None:
        output = self.root / "response-id-collision-output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
            profile="test", mode="exploratory",
        )
        calls = 0

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            nonlocal calls
            calls += 1
            request = json.loads(body)
            content = "same-public-text" if calls == 1 else grade_json()
            response_id = "generator-id" if calls == 1 else "same-public-text"
            return json.dumps({
                "id": response_id,
                "model": request["model"],
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport,
            new_id=iter(("collision-run", "generator-context", "grader-context")).__next__,
        )
        self.assertEqual(calls, 2)
        detail = inspect_case(run_dir, "p003")["records"][0]
        self.assertEqual(detail["generator_final_response"], "same-public-text")
        self.assertEqual(load_report(run_dir)["secret_scan"], "pass")


if __name__ == "__main__":
    unittest.main()
