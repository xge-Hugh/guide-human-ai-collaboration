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

    def test_both_preflight_gates_make_zero_calls_and_no_artifacts(self) -> None:
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
                blocked_code, blocked = preflight_thinking_compatibility(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                )
            self.assertEqual(list(Path(output).iterdir()), [])

        self.assertEqual(missing_code, 2)
        self.assertEqual(blocked_code, 3)
        for report in (missing, blocked):
            self.assertEqual(report["network_call_count"], 0)
            self.assertEqual(report["generator_call_count"], 0)
            self.assertEqual(report["grader_call_count"], 0)
            self.assertEqual(report["evidence_use"], EVIDENCE_USE)
        self.assertIn("blocked_pending_human_cost_privacy_approval", blocked["execution"])


if __name__ == "__main__":
    unittest.main()
