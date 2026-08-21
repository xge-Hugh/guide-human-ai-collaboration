from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.assurance_eval.direct_grader import (
    CONFIGURED_MODEL,
    MODEL_FAMILY,
    MODEL_SETTINGS,
    RENDERER_ID,
    render_grader_packet,
    renderer_content_sha256,
)
from tools.assurance_eval.direct_grader_compatibility import execute, prepare_offline


REPO_ROOT = Path(__file__).resolve().parents[1]


class DirectGraderRendererTest(unittest.TestCase):
    def fixture(self) -> dict[str, object]:
        path = (
            REPO_ROOT
            / "docs"
            / "experiments"
            / "assurance-v2-grader-contract-compatibility-fixture.json"
        )
        return json.loads(path.read_text(encoding="utf-8"))["grader_packet"]

    def test_renders_only_one_packet_without_experiment_order_or_reasoning(self) -> None:
        request = render_grader_packet(self.fixture())

        self.assertEqual(CONFIGURED_MODEL, "qwen3.7-max")
        self.assertEqual(MODEL_FAMILY, "Qwen")
        self.assertEqual(RENDERER_ID, "phase-b-direct-grader-zh-cn-v1-candidate")
        self.assertEqual(request["thinking"], {"type": "disabled"})
        self.assertEqual(request["max_tokens"], 1024)
        self.assertFalse(request["stream"])
        self.assertNotIn("temperature", request)
        self.assertNotIn("top_p", request)
        self.assertNotIn("tools", request)
        self.assertEqual(len(request["messages"]), 2)
        visible = json.dumps(request, ensure_ascii=False)
        for forbidden in (
            "reasoning_content",
            "generator_reasoning",
            "other_variants",
            "other_repetitions",
            "expected_ordering",
            "B0",
            "B1",
            "B2",
        ):
            self.assertNotIn(forbidden, visible)

    def test_renderer_is_deterministic_and_does_not_modify_packet(self) -> None:
        packet = self.fixture()
        before = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        first = render_grader_packet(packet)
        second = render_grader_packet(packet)

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(packet, ensure_ascii=False, sort_keys=True), before)
        self.assertEqual(MODEL_SETTINGS["max_tokens"], 1024)
        self.assertRegex(renderer_content_sha256(), r"^[0-9a-f]{64}$")

    def test_prepares_exact_request_without_calls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = prepare_offline(repo_root=REPO_ROOT, output_dir=root)
            request = json.loads(
                (root / "grader_model_visible_request.json").read_text(encoding="utf-8")
            )

        self.assertEqual(report["status"], "prepared_offline_not_executed")
        self.assertTrue(report["execution_enabled"])
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(report["network_calls"], 0)
        self.assertEqual(request["model"], "qwen3.7-max")
        self.assertEqual(request["thinking"], {"type": "disabled"})
        self.assertNotIn("tools", request)

    def test_executes_one_synthetic_transport_call_and_consumes_approval(self) -> None:
        grade = {
            "applicability": "not_applicable",
            "applicability_basis": "synthetic compatibility response",
            "timing": "not_applicable",
            "satisfaction": "not_applicable",
            "human_compensation_needed": "no",
            "over_trigger_cost": "none",
            "notes": "offline transport fixture",
        }
        calls = {"count": 0}

        def transport(url: str, headers: object, body: bytes, timeout: float) -> bytes:
            calls["count"] += 1
            return json.dumps(
                {
                    "id": "private-response-id",
                    "model": "qwen-provider-reported",
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": json.dumps(grade),
                                "reasoning_content": "private synthetic reasoning",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 100,
                        "completion_tokens": 20,
                        "total_tokens": 120,
                    },
                }
            ).encode("utf-8")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "setting.json"
            config_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "connections": [
                            {
                                "label": "private-candidate",
                                "provider": "custom",
                                "api_style": "openai_chat_completions",
                                "base_url": "https://private.example.invalid",
                                "api_key": "test-secret-key",
                                "models": [
                                    {"model_id": "deepseek-v4-flash"},
                                    {"model_id": "qwen3.7-max"},
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            os.chmod(config_path, 0o600)
            output = root / "output"
            output.mkdir(mode=0o700)
            with patch(
                "tools.assurance_eval.direct_grader_compatibility._clean_git_revision",
                return_value="r" * 40,
            ):
                code, report = execute(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_dir=output,
                    confirm_network=True,
                    transport=transport,
                )
                second_output = root / "second-output"
                second_output.mkdir(mode=0o700)
                with self.assertRaisesRegex(ValueError, "already consumed"):
                    execute(
                        repo_root=REPO_ROOT,
                        config_path=config_path,
                        output_dir=second_output,
                        confirm_network=True,
                        transport=transport,
                    )

            artifact_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in output.iterdir()
                if path.is_file()
            )

        self.assertEqual(code, 0)
        self.assertEqual(report["smoke_status"], "passed")
        self.assertEqual(report["network_call_count"], 1)
        self.assertEqual(calls["count"], 1)
        self.assertTrue(report["strict_import_succeeded"])
        self.assertNotIn("private synthetic reasoning", artifact_text)
        self.assertNotIn("test-secret-key", artifact_text)


if __name__ == "__main__":
    unittest.main()
