from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.assurance_eval.formal_replay import (
    COMMON_BASE_INSTRUCTION,
    EVIDENCE_USE,
    RENDERER_ID,
    preflight_formal_replay,
    render_generator_request,
    renderer_source_sha256,
)
from tools.assurance_eval.loading import load_phase_b_inputs
from tools.assurance_eval.models import CHINESE_VARIANTS_FILE, ProviderDescriptor, ProviderResponse, RunConfig
from tools.assurance_eval.providers import ScriptedFakeProvider
from tools.assurance_eval.runner import AssuranceEvalRunner


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_config(directory: str) -> Path:
    path = Path(directory) / "setting.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "connections": [
                    {
                        "label": "synthetic-formal-connection",
                        "provider": "custom",
                        "api_style": "openai_chat_completions",
                        "base_url": "https://private.example.invalid",
                        "api_key": "synthetic-secret-key",
                        "models": [{"model_id": "deepseek-v4-flash"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    os.chmod(path, 0o600)
    return path


def grade_response() -> ProviderResponse:
    return ProviderResponse(
        json.dumps(
            {
                "applicability": "applicable",
                "applicability_basis": "synthetic schedule fixture",
                "timing": "on_time",
                "satisfaction": "satisfied",
                "human_compensation_needed": "no",
                "over_trigger_cost": "none",
                "notes": "not evidence",
            }
        ),
        "fake-grader",
    )


class FormalReplayTest(unittest.TestCase):
    def test_chinese_variants_are_distinct_and_b2_is_exactly_b1_plus_frame(self) -> None:
        english = load_phase_b_inputs(REPO_ROOT)
        chinese = load_phase_b_inputs(REPO_ROOT, variants_file=CHINESE_VARIANTS_FILE)
        chinese_document = json.loads(
            (REPO_ROOT / "docs" / "experiments" / CHINESE_VARIANTS_FILE).read_text()
        )
        self.assertEqual(chinese.variants["B0"]["instruction_append"], "")
        b1 = chinese.variants["B1"]["instruction_append"]
        b2 = chinese.variants["B2"]["instruction_append"]
        self.assertEqual(
            b2, f"{b1}\n\n{chinese_document['b2_semantic_frame_append']}"
        )
        self.assertNotEqual(b1, english.variants["B1"]["instruction_append"])
        self.assertEqual(
            chinese.source_files["variants"]["path"],
            f"docs/experiments/{CHINESE_VARIANTS_FILE}",
        )

    def test_formal_renderer_is_exact_and_shared_by_all_variants(self) -> None:
        variants = load_phase_b_inputs(
            REPO_ROOT, variants_file=CHINESE_VARIANTS_FILE
        ).variants
        for variant_id in ("B0", "B1", "B2"):
            append = variants[variant_id]["instruction_append"]
            system = COMMON_BASE_INSTRUCTION if not append else f"{COMMON_BASE_INSTRUCTION}\n\n{append}"
            rendered = render_generator_request(
                {
                    "call_kind": "generator",
                    "variant_id": variant_id,
                    "system_instruction": system,
                    "packet": {"pre_context": "场景摘要", "user_message": "当前消息"},
                }
            )
            self.assertEqual(
                rendered["messages"],
                [
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": "【前置上下文】\n场景摘要\n\n【用户当前消息】\n当前消息",
                    },
                ],
            )
            self.assertEqual(rendered["thinking"], {"type": "enabled"})
            self.assertEqual(rendered["max_tokens"], 4096)
            self.assertFalse(rendered["stream"])
            self.assertNotIn("temperature", rendered)
            self.assertNotIn("top_p", rendered)
        with self.assertRaisesRegex(ValueError, "exact reviewed variant"):
            render_generator_request(
                {
                    "call_kind": "generator",
                    "variant_id": "B0",
                    "system_instruction": f"{COMMON_BASE_INSTRUCTION}\n\nunexpected",
                    "packet": {"pre_context": "场景摘要", "user_message": "当前消息"},
                }
            )
        self.assertEqual(RENDERER_ID, "phase-b-formal-generator-zh-cn-v1")
        self.assertRegex(renderer_source_sha256(), r"^[0-9a-f]{64}$")

    def test_formal_preflight_never_calls_a_provider(self) -> None:
        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with patch(
                "tools.assurance_eval.formal_replay._clean_git_revision",
                return_value="test-revision",
            ):
                missing_code, missing = preflight_formal_replay(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_formal_run=False,
                )
                blocked_code, blocked = preflight_formal_replay(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_formal_run=True,
                )
        self.assertEqual(missing_code, 2)
        self.assertEqual(blocked_code, 3)
        self.assertEqual(missing["network_call_count"], 0)
        self.assertEqual(blocked["network_call_count"], 0)
        self.assertEqual(blocked["evidence_use"], EVIDENCE_USE)
        self.assertIn("blocked_pending_human_cloud_review", blocked["execution"])

    def test_counterbalanced_schedule_is_recorded_with_clean_contexts(self) -> None:
        call_count = 18
        generator = ScriptedFakeProvider(
            ProviderDescriptor("fake", "fake-generator", "standalone"),
            [ProviderResponse("synthetic", "fake-generator")] * call_count,
        )
        grader = ScriptedFakeProvider(
            ProviderDescriptor("fake", "fake-grader", "standalone"),
            [grade_response()] * call_count,
        )
        with tempfile.TemporaryDirectory() as output:
            config = RunConfig(
                output_root=Path(output),
                base_generator_instruction=COMMON_BASE_INSTRUCTION,
                grader_instruction="synthetic",
                grader_normative_context="synthetic",
                case_ids=("p003", "p004"),
                variant_ids=("B0", "B1", "B2"),
                run_mode="fake_pipeline",
                generator_base_language="zh-CN",
                case_packet_language="zh-CN",
                variant_condition_language="zh-CN",
                grader_instruction_language="synthetic",
                grader_context_language="synthetic",
                repetitions=3,
                variants_file=CHINESE_VARIANTS_FILE,
                variant_order_by_repetition=(
                    ("B0", "B1", "B2"),
                    ("B1", "B2", "B0"),
                    ("B2", "B0", "B1"),
                ),
            )
            run_dir = AssuranceEvalRunner(REPO_ROOT, generator, grader).run(config)
            records = [
                json.loads(path.read_text())
                for path in (run_dir / "records").glob("*.json")
            ]
            manifest = json.loads((run_dir / "manifest.json").read_text())

        by_index = sorted(records, key=lambda record: record["execution_index"])
        expected = [
            (repetition, case_id, variant_id)
            for repetition, order in (
                (1, ("B0", "B1", "B2")),
                (2, ("B1", "B2", "B0")),
                (3, ("B2", "B0", "B1")),
            )
            for case_id in ("p003", "p004")
            for variant_id in order
        ]
        self.assertEqual(
            [
                (record["repetition"], record["case_id"], record["variant_id"])
                for record in by_index
            ],
            expected,
        )
        self.assertEqual([record["variant_position"] for record in by_index], [1, 2, 3] * 6)
        self.assertEqual(
            [
                (call["packet"]["case_id"], call["variant_id"])
                for call in generator.calls
            ],
            [(case_id, variant_id) for _, case_id, variant_id in expected],
        )
        self.assertEqual(len({record["context_id"] for record in records}), call_count)
        self.assertEqual(manifest["config"]["planned_execution_order"], [
            {
                "execution_index": record["execution_index"],
                "case_id": record["case_id"],
                "variant_id": record["variant_id"],
                "repetition": record["repetition"],
                "variant_position": record["variant_position"],
            }
            for record in by_index
        ])

    def test_core_runner_rejects_formal_mode_until_orchestrator_is_approved(self) -> None:
        config = RunConfig(
            output_root=Path("/tmp/unused"),
            base_generator_instruction=COMMON_BASE_INSTRUCTION,
            grader_instruction="pending review",
            grader_normative_context="pending review",
            case_ids=("p003",),
            variant_ids=("B0", "B1", "B2"),
            run_mode="formal_replay",
            generator_base_language="zh-CN",
            case_packet_language="zh-CN",
            variant_condition_language="zh-CN",
            grader_instruction_language="zh-CN",
            grader_context_language="zh-CN",
            variants_file=CHINESE_VARIANTS_FILE,
        )
        with self.assertRaisesRegex(ValueError, "unsupported run_mode"):
            config.validate()


if __name__ == "__main__":
    unittest.main()
