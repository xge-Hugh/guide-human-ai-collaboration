from __future__ import annotations

import copy
import io
import json
import os
import stat
import sys
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
from tools.assurance_eval.models import ProviderError
from tools.assurance_eval.planning import build_resolved_plan, plan_preview, verify_resolved_plan
from tools.assurance_eval.renderers import GENERATOR_ID, GRADER_ID, render_generator, render_grader
from tools.assurance_eval.reporting import inspect_case, load_report
from tools.assurance_eval.retry import classify_retryability
from tools.assurance_eval.semantics import compare_treatment_semantics, extract_treatment_semantics, require_compatible_treatment


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
        if sys.platform == "win32":
            self._private_path_patch = patch(
                "tools.assurance_eval.config._private_path",
                side_effect=lambda path, repo: path.resolve(),
            )
            self._private_path_patch.start()
            self.addCleanup(self._private_path_patch.stop)
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
        self.assertTrue(recipe["formal_execution_enabled"])
        self.assertEqual(recipe["selection"]["cases"], ["p003", "p004", "p005", "p006", "p007", "p008", "p009", "p011", "p012", "p013"])
        self.assertEqual(recipe["selection"]["variants"], ["B0", "B1", "B2"])
        self.assertEqual(recipe["schedule"]["variant_order_by_repetition"], [["B0", "B1", "B2"], ["B1", "B2", "B0"], ["B2", "B0", "B1"]])
        self.assertEqual(recipe["parameters"]["generator"], {"thinking": {"type": "enabled"}, "max_tokens": 65536, "stream": False})
        self.assertEqual(recipe["parameters"]["grader"], {"thinking": {"type": "enabled"}, "max_tokens": 32768, "stream": False})
        self.assertEqual(recipe["timeouts_seconds"], {"generator": 900, "grader": 600})
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
        self.assertEqual(preview["timeouts_seconds"], {"generator": 900, "grader": 600})
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

        changed = copy.deepcopy(envelope)
        changed["plan"]["timeouts_seconds"]["generator"] = 901
        changed["resolved_plan_sha256"] = sha256_bytes(canonical_json(changed["plan"]))
        with self.assertRaisesRegex(ValueError, "canonical projection"):
            execute_resolved_plan(repo_root=REPO_ROOT, envelope=changed, catalog=self.catalog, experiment=experiment, resolved=resolved, authorize_network=True, transport=lambda *args: calls.append(args))
        self.assertEqual(calls, [])

    def test_recipe_requires_positive_role_timeouts(self) -> None:
        recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
        experiment_dir = RECIPE.parent
        recipe["sources"] = {
            "generation": str(experiment_dir / "assurance-v2-phase-b-generation.json"),
            "variants": str(experiment_dir / "assurance-v2-phase-b-variants.zh-CN.json"),
            "rubrics": str(experiment_dir / "assurance-v2-phase-b-rubrics.json"),
        }
        invalid_values = (
            {"generator": 0, "grader": 600},
            {"generator": True, "grader": 600},
            {"generator": 900},
            {"generator": 900, "grader": 600, "other": 1},
        )
        for index, value in enumerate(invalid_values):
            with self.subTest(value=value):
                recipe["timeouts_seconds"] = value
                path = self.root / f"bad-timeout-{index}.recipe.json"
                path.write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "positive integers"):
                    load_experiment(REPO_ROOT, path)

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
        timeouts: list[float] = []

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            timeouts.append(timeout)
            request = json.loads(body)
            requests.append(request)
            if len(requests) == 1:
                envelope["plan"]["schedule"]["execution_order"].clear()
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({"id": "private-response-id", "model": request["model"] + "-reported", "choices": [{"message": {"content": content, "reasoning_content": "private hidden reasoning"}, "finish_reason": "stop"}], "usage": {"completion_tokens_details": {"reasoning_tokens": 7}}}).encode()

        run_dir = execute_resolved_plan(repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog, experiment=experiment, resolved=resolved, authorize_network=True, transport=transport, new_id=iter(("run", "generator-context", "grader-context")).__next__)
        self.assertEqual(len(requests), 2)
        self.assertEqual(timeouts, [900, 600])
        self.assertTrue(all("timeouts_seconds" not in request for request in requests))
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
        self.assertEqual(report["network_accounting"]["actual_network_attempts"], 2)
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
        disabled = self.small_experiment(self.root / "disabled-formal-output")
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean), patch("tools.assurance_eval.planning.require_committed_paths"):
            formal, formal_resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=disabled, catalog=self.catalog, profile="test", mode="formal")
        with self.assertRaisesRegex(PermissionError, "formal execution remains disabled"):
            execute_resolved_plan(repo_root=REPO_ROOT, envelope=formal, catalog=self.catalog, experiment=disabled, resolved=formal_resolved, authorize_network=True, transport=lambda *args: calls.append(args))
        self.assertEqual(calls, [])

    def test_transport_failure_retries_then_records_all_attempts(self) -> None:
        output = self.root / "failure-output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog, profile="test", mode="exploratory")
        calls = 0

        def failing_transport(*args) -> bytes:
            nonlocal calls
            calls += 1
            raise ProviderError("provider transport failure")

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved,
            authorize_network=True, transport=failing_transport,
            sleep=lambda _seconds: None,
            new_id=iter(("failed-run", "generator-context")).__next__,
        )
        self.assertEqual(calls, 3)
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["attempt_count"], 3)
        self.assertEqual(record["generator"]["retry_count"], 2)
        self.assertEqual(record["generator"]["final_status"], "failed_retryable")
        self.assertEqual(len(record["generator"]["attempt_evidence_paths"]), 3)
        self.assertIsNone(record["grader"])
        self.assertEqual(load_report(run_dir)["network_accounting"]["actual_network_attempts"], 3)

    def test_formal_invalid_grader_blocks_integrity_but_continues_other_records(self) -> None:
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
            content = "raw generator response" if request["model"] == "generator-test" else (
                "not-json" if calls == 3 else grade_json()
            )
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            run_dir = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
                experiment=experiment, resolved=resolved, authorize_network=True,
                transport=transport,
                new_id=iter(("formal-blocked", "g1", "g2", "j1", "j2")).__next__,
            )
        self.assertEqual(calls, 4)
        self.assertEqual(len(list((run_dir / "records").glob("*.json"))), 2)
        report = load_report(run_dir)
        self.assertEqual(report["operational_status"], "blocked_integrity")
        self.assertEqual(report["blocked_reason"]["code"], "invalid_or_unparseable_grader_output")
        self.assertTrue(report["requires_human_adjudication"])
        record = json.loads((run_dir / "records" / "p003__B0__r001.json").read_text())
        self.assertEqual(record["grader"]["raw_output"], "not-json")
        self.assertEqual(record["grader"]["attempt_count"], 1)
        self.assertEqual(record["grader"]["retry_count"], 0)

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
                sleep=lambda _seconds: None,
                new_id=iter(("formal-transport-blocked", "generator-context")).__next__,
            )
        self.assertEqual(calls, 1)
        report = load_report(run_dir)
        self.assertEqual(report["operational_status"], "blocked_integrity")
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

    def test_transient_generator_failure_then_success_on_retry(self) -> None:
        output = self.root / "retry-success-output"
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
            if request["model"] == "generator-test" and calls == 1:
                raise ProviderError("provider transport failure")
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport, sleep=lambda _seconds: None,
            new_id=iter(("retry-success", "generator-context", "grader-context")).__next__,
        )
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["attempt_count"], 2)
        self.assertEqual(record["generator"]["retry_count"], 1)
        self.assertEqual(record["generator"]["successful_attempt"], 2)
        self.assertIsNotNone(record["generator"]["successful_attempt_elapsed_ms"])
        self.assertLess(record["generator"]["successful_attempt_elapsed_ms"], record["generator"]["elapsed_ms"])
        self.assertEqual(len(record["generator"]["attempt_evidence_paths"]), 2)
        self.assertEqual(calls, 3)

    def test_transient_grader_failure_then_success_on_retry(self) -> None:
        output = self.root / "grader-retry-output"
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
            if request["model"] == "grader-test" and calls == 2:
                raise ProviderError("provider HTTP status 503")
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport, sleep=lambda _seconds: None,
            new_id=iter(("grader-retry", "generator-context", "grader-context")).__next__,
        )
        record = json.loads(next((run_dir / "records").glob("*.json")).read_text())
        self.assertEqual(record["grader"]["attempt_count"], 2)
        self.assertEqual(record["grader"]["retry_count"], 1)
        self.assertEqual(record["grader"]["grade_parse_status"], "parsed")

    def test_retry_exhaustion_produces_paused_retryable(self) -> None:
        output = self.root / "paused-output"
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

        def transport(*args) -> bytes:
            raise ProviderError("provider transport failure")

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            run_dir = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
                experiment=experiment, resolved=resolved, authorize_network=True,
                transport=transport, sleep=lambda _seconds: None,
                new_id=iter(("paused-run", "generator-context")).__next__,
            )
        report = load_report(run_dir)
        self.assertEqual(report["operational_status"], "paused_retryable")
        self.assertEqual(report["paused_retryable_observations"], 1)

    def test_no_retry_on_schema_or_integrity_failures(self) -> None:
        self.assertEqual(classify_retryability({"type": "PrivateValueBlocked", "message": "blocked"}), "not_retryable")
        self.assertEqual(classify_retryability({"type": "ProviderError", "message": "provider returned an invalid chat completion"}), "not_retryable")
        self.assertEqual(classify_retryability({"type": "ProviderError", "message": "formal provenance changed"}), "not_retryable")
        self.assertEqual(classify_retryability({"type": "ProviderError", "message": "provider transport failure"}), "retryable")
        self.assertEqual(classify_retryability({"type": "ProviderError", "message": "provider HTTP status 429"}), "retryable")

    def test_resume_reuses_generator_and_retries_only_grader(self) -> None:
        prefix = self.root / "prefix-run"
        prefix.mkdir(mode=0o700)
        experiment = self.small_experiment(prefix, cases=["p003"], formal_execution_enabled=True)
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

        def prefix_transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            nonlocal calls
            calls += 1
            request = json.loads(body)
            if request["model"] == "grader-test":
                raise ProviderError("provider transport failure")
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": "stable generator output"}, "finish_reason": "stop"}],
            }).encode()

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            prefix_run = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
                experiment=experiment, resolved=resolved, authorize_network=True,
                transport=prefix_transport, sleep=lambda _seconds: None,
                new_id=iter(("prefix-run", "generator-context", "grader-context")).__next__,
            )
        self.assertEqual(calls, 4)
        continuation = self.root / "continuation-run"
        continuation.mkdir(mode=0o700)
        experiment2 = self.small_experiment(continuation, cases=["p003"], formal_execution_enabled=True)
        with patch("tools.assurance_eval.planning.git_provenance", return_value=clean), patch(
            "tools.assurance_eval.planning.require_committed_paths"
        ):
            envelope2, resolved2 = build_resolved_plan(
                repo_root=REPO_ROOT, experiment=experiment2, catalog=self.catalog,
                profile="test", mode="formal",
            )
        calls = 0

        def continuation_transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            nonlocal calls
            calls += 1
            request = json.loads(body)
            self.assertEqual(request["model"], "grader-test")
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": grade_json()}, "finish_reason": "stop"}],
            }).encode()

        with patch("tools.assurance_eval.execution.git_provenance", return_value=clean):
            resume_run = execute_resolved_plan(
                repo_root=REPO_ROOT, envelope=envelope2, catalog=self.catalog,
                experiment=experiment2, resolved=resolved2, authorize_network=True,
                transport=continuation_transport, sleep=lambda _seconds: None,
                resume_from=prefix_run,
                new_id=iter(("resume-run", "grader-context")).__next__,
            )
        self.assertEqual(calls, 1)
        record = json.loads(next((resume_run / "records").glob("*.json")).read_text())
        self.assertEqual(record["generator"]["raw_output"], "stable generator output")
        self.assertIn("imported_from_episode", record["generator"])
        self.assertEqual(record["grader"]["grade_parse_status"], "parsed")
        prefix_record_path = next((prefix_run / "records").glob("*.json"))
        self.assertTrue(prefix_record_path.exists())

    def test_resume_rejects_material_semantic_change(self) -> None:
        output = self.root / "semantic-output"
        experiment = self.small_experiment(output)
        envelope, resolved = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
            profile="test", mode="exploratory",
        )

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            request = json.loads(body)
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        prefix_run = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport,
            new_id=iter(("semantic-prefix", "generator-context", "grader-context")).__next__,
        )
        changed = copy.deepcopy(envelope)
        changed["plan"]["instructions"]["generator_base"] = "mutated treatment instruction"
        changed["resolved_plan_sha256"] = sha256_bytes(canonical_json(changed["plan"]))
        changed_experiment = self.small_experiment(self.root / "changed-output")
        changed_experiment.recipe["instructions"]["generator_base"] = "mutated treatment instruction"
        with self.assertRaisesRegex(ValueError, "incompatible"):
            require_compatible_treatment(changed["plan"], envelope["plan"])

    def test_harmless_plan_metadata_diff_allows_semantic_equivalence(self) -> None:
        experiment = self.small_experiment(self.root / "semantic-compare")
        envelope, _ = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
            profile="test", mode="exploratory",
        )
        harmless = copy.deepcopy(envelope["plan"])
        harmless["provenance"] = {
            "available": True, "git_revision": "different", "clean": True,
            "status_sha256": "other", "harness_source_sha256": "other-harness",
        }
        harmless["output_root"] = str(Path(harmless["output_root"]).resolve())
        report = compare_treatment_semantics(envelope["plan"], harmless)
        self.assertEqual(report["treatment_semantics"], "equivalent")
        self.assertNotEqual(envelope["resolved_plan_sha256"], sha256_bytes(canonical_json(harmless)))

    def test_generator_order_remains_serial(self) -> None:
        output = self.root / "serial-output"
        experiment = self.small_experiment(output, cases=["p003", "p004"])
        envelope, resolved = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
            profile="test", mode="exploratory",
        )
        order: list[str] = []

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            request = json.loads(body)
            if request["model"] == "generator-test":
                order.append(request["messages"][1]["content"][:20])
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport,
            new_id=iter(("serial-run", "g1", "j1", "g2", "j2")).__next__,
        )
        self.assertEqual(len(order), 2)
        self.assertNotEqual(order[0], order[1])

    def test_grader_parallelism_isolates_failures(self) -> None:
        output = self.root / "parallel-output"
        experiment = self.small_experiment(output, cases=["p003", "p004"])
        envelope, resolved = build_resolved_plan(
            repo_root=REPO_ROOT, experiment=experiment, catalog=self.catalog,
            profile="test", mode="exploratory",
        )
        calls = 0
        grader_transport_calls = 0

        def transport(url: str, headers, body: bytes, timeout: float) -> bytes:
            nonlocal calls, grader_transport_calls
            calls += 1
            request = json.loads(body)
            if request["model"] == "grader-test":
                grader_transport_calls += 1
                if grader_transport_calls <= 3:
                    raise ProviderError("provider transport failure")
            content = "raw generator response" if request["model"] == "generator-test" else grade_json()
            return json.dumps({
                "model": request["model"] + "-reported",
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            }).encode()

        run_dir = execute_resolved_plan(
            repo_root=REPO_ROOT, envelope=envelope, catalog=self.catalog,
            experiment=experiment, resolved=resolved, authorize_network=True,
            transport=transport, sleep=lambda _seconds: None, grader_parallelism=1,
            new_id=iter(("parallel-run", "g1", "g2", "j1", "j2")).__next__,
        )
        records = {path.stem: json.loads(path.read_text()) for path in (run_dir / "records").glob("*.json")}
        self.assertEqual(records["p003__B0__r001"]["grader"]["final_status"], "failed_retryable")
        self.assertEqual(records["p004__B0__r001"]["grader"]["grade_parse_status"], "parsed")


if __name__ == "__main__":
    unittest.main()
