from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.assurance_eval.formal_replay import COMMON_BASE_INSTRUCTION
from tools.assurance_eval.thinking_compatibility import (
    EVIDENCE_USE,
    RENDERER_ID,
    _consumption_marker,
    execute_thinking_compatibility,
    preflight_thinking_compatibility,
    render_generator_request,
    renderer_source_sha256,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_config(directory: str) -> Path:
    path = Path(directory) / "setting.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "connections": [
                    {
                        "label": "synthetic-thinking-connection",
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


class ThinkingCompatibilityTest(unittest.TestCase):
    def test_renderer_is_exactly_one_thinking_enabled_p002_b0_request(self) -> None:
        rendered = render_generator_request(
            {
                "call_kind": "generator",
                "variant_id": "B0",
                "system_instruction": COMMON_BASE_INSTRUCTION,
                "packet": {
                    "case_id": "p002",
                    "pre_context": "完整低风险问题",
                    "user_message": "当前问题",
                },
            }
        )
        self.assertEqual(RENDERER_ID, "phase-b-thinking-compat-smoke-generator-zh-cn-v1")
        self.assertRegex(renderer_source_sha256(), r"^[0-9a-f]{64}$")
        self.assertEqual(
            rendered["messages"],
            [
                {"role": "system", "content": COMMON_BASE_INSTRUCTION},
                {
                    "role": "user",
                    "content": "【前置上下文】\n完整低风险问题\n\n【用户当前消息】\n当前问题",
                },
            ],
        )
        self.assertEqual(rendered["thinking"], {"type": "enabled"})
        self.assertEqual(rendered["max_tokens"], 4096)
        self.assertFalse(rendered["stream"])
        for absent in ("temperature", "top_p", "reasoning_effort"):
            self.assertNotIn(absent, rendered)

    def test_preflight_requires_confirmation_without_consuming_approval(self) -> None:
        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with patch(
                "tools.assurance_eval.thinking_compatibility._clean_git_revision",
                return_value="test-revision",
            ):
                missing_code, missing = preflight_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=False,
                )
                approved_code, approved = preflight_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                )
            self.assertEqual(list(Path(output).iterdir()), [])
            self.assertFalse(_consumption_marker(config_path).exists())

        self.assertEqual(missing_code, 2)
        self.assertEqual(approved_code, 0)
        for report in (missing, approved):
            self.assertEqual(report["network_call_count"], 0)
            self.assertEqual(report["generator_call_count"], 0)
            self.assertEqual(report["grader_call_count"], 0)
            self.assertEqual(report["evidence_use"], EVIDENCE_USE)
        self.assertIn("approved for one call", approved["network_confirmation"])

    def test_one_synthetic_call_is_verified_and_consumes_approval(self) -> None:
        transport_calls = 0

        def transport(_url: str, _headers: object, body: bytes, _timeout: float) -> bytes:
            nonlocal transport_calls
            transport_calls += 1
            sent = json.loads(body)
            self.assertEqual(sent["thinking"], {"type": "enabled"})
            for absent in ("temperature", "top_p", "reasoning_effort"):
                self.assertNotIn(absent, sent)
            return json.dumps(
                {
                    "id": "private-thinking-response-id",
                    "model": "provider-reported-synthetic-model",
                    "choices": [
                        {
                            "message": {
                                "content": "synthetic final content",
                                "reasoning_content": "private synthetic reasoning",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 30,
                        "completion_tokens": 12,
                        "total_tokens": 42,
                        "completion_tokens_details": {"reasoning_tokens": 7},
                    },
                }
            ).encode("utf-8")

        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with (
                patch(
                    "tools.assurance_eval.thinking_compatibility._clean_git_revision",
                    return_value="test-revision",
                ),
                patch("tools.assurance_eval.runner._git_revision", return_value="test-revision"),
                patch(
                    "tools.assurance_eval.runner._working_tree_status",
                    return_value={
                        "available": True,
                        "dirty": False,
                        "entry_count": 0,
                        "status_sha256": "0" * 64,
                    },
                ),
                patch(
                    "tools.assurance_eval.thinking_compatibility._runner_source_digest",
                    return_value="synthetic-runner-digest",
                ),
                patch(
                    "tools.assurance_eval.runner._runner_source_digest",
                    return_value="synthetic-runner-digest",
                ),
            ):
                code, report = execute_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=transport,
                )
            run_dir = Path(report["artifact_path"])
            artifact_text = "\n".join(
                path.read_text(encoding="utf-8") for path in run_dir.rglob("*.json")
            )
            self.assertTrue(_consumption_marker(config_path).exists())
            with self.assertRaisesRegex(ValueError, "already consumed"):
                execute_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=lambda *_: self.fail("second transport must not be called"),
                )

        self.assertEqual(code, 0)
        self.assertEqual(transport_calls, 1)
        self.assertEqual(report["smoke_status"], "passed")
        self.assertEqual(report["network_call_count"], 1)
        self.assertEqual(report["fake_grader_invocation_count"], 1)
        self.assertEqual(report["provider_reported_model"], "provider-reported-synthetic-model")
        self.assertEqual(report["reasoning_tokens"], 7)
        self.assertFalse(report["reasoning_content_retained"])
        self.assertEqual(report["secret_scan"], "pass")
        self.assertEqual(report["blocking_outcomes"], [])
        self.assertNotIn("private synthetic reasoning", artifact_text)
        self.assertNotIn("private-thinking-response-id", artifact_text)

    def test_length_response_blocks_without_retry(self) -> None:
        transport_calls = 0

        def transport(_url: str, _headers: object, _body: bytes, _timeout: float) -> bytes:
            nonlocal transport_calls
            transport_calls += 1
            return json.dumps(
                {
                    "model": "synthetic-model",
                    "choices": [{"message": {"content": "partial"}, "finish_reason": "length"}],
                    "usage": {"prompt_tokens": 5, "completion_tokens": 4, "total_tokens": 9},
                }
            ).encode("utf-8")

        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with (
                patch(
                    "tools.assurance_eval.thinking_compatibility._clean_git_revision",
                    return_value="test-revision",
                ),
                patch("tools.assurance_eval.runner._git_revision", return_value="test-revision"),
                patch(
                    "tools.assurance_eval.runner._working_tree_status",
                    return_value={"available": True, "dirty": False, "entry_count": 0, "status_sha256": "0" * 64},
                ),
                patch(
                    "tools.assurance_eval.thinking_compatibility._runner_source_digest",
                    return_value="synthetic-runner-digest",
                ),
                patch(
                    "tools.assurance_eval.runner._runner_source_digest",
                    return_value="synthetic-runner-digest",
                ),
            ):
                code, report = execute_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=transport,
                )

        self.assertEqual(code, 1)
        self.assertEqual(transport_calls, 1)
        self.assertIn("finish_reason_stop", report["blocking_outcomes"])


if __name__ == "__main__":
    unittest.main()
