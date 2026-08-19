from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.assurance_eval.models import RunConfig
from tools.assurance_eval.providers import ProviderError
from tools.assurance_eval.transport_smoke import (
    EVIDENCE_LABEL,
    RENDERER_ID,
    SYSTEM_INSTRUCTION,
    execute_transport_smoke,
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
                        "label": "private-test-connection",
                        "provider": "custom",
                        "api_style": "openai_chat_completions",
                        "base_url": "https://private.example.invalid",
                        "api_key": "synthetic-secret-key",
                        "models": [{"model_id": "moving-alias"}],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    os.chmod(path, 0o600)
    return path


class TransportSmokeTest(unittest.TestCase):
    def test_renderer_is_exact_and_does_not_fabricate_history_turns(self) -> None:
        rendered = render_generator_request(
            {
                "call_kind": "generator",
                "variant_id": "B0",
                "system_instruction": SYSTEM_INSTRUCTION,
                "packet": {
                    "case_id": "p002",
                    "pre_context": "场景摘要",
                    "user_message": "当前问题",
                },
            }
        )
        self.assertEqual(RENDERER_ID, "phase-b-transport-smoke-generator-zh-cn-v1")
        self.assertEqual(len(renderer_source_sha256()), 64)
        self.assertEqual(
            rendered["messages"],
            [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {
                    "role": "user",
                    "content": "【前置上下文】\n场景摘要\n\n【用户当前消息】\n当前问题",
                },
            ],
        )

    def test_transport_mode_is_fixed_to_one_p002_b0_call(self) -> None:
        config = RunConfig(
            output_root=Path("/tmp/unused"),
            base_generator_instruction=SYSTEM_INSTRUCTION,
            grader_instruction="fake",
            grader_normative_context="fake",
            case_ids=("p002",),
            variant_ids=("B0",),
            run_mode="transport_smoke",
            generator_base_language="zh-CN",
            case_packet_language="zh-CN",
            variant_condition_language="none",
            grader_instruction_language="synthetic",
            grader_context_language="synthetic",
            repetitions=1,
            max_retries=0,
        )
        config.validate()
        self.assertEqual(config.evidence_label, EVIDENCE_LABEL)
        with self.assertRaisesRegex(ValueError, "p002/B0"):
            RunConfig(**{**config.__dict__, "case_ids": ("p001",)}).validate()

    def test_missing_confirmation_performs_no_transport(self) -> None:
        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with patch(
                "tools.assurance_eval.transport_smoke._clean_git_revision",
                return_value="test-revision",
            ):
                code, report = execute_transport_smoke(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=False,
                    transport=lambda *_: self.fail("transport must not be called"),
                )
        self.assertEqual(code, 2)
        self.assertEqual(report["network_call_count"], 0)

    def test_one_synthetic_call_produces_verified_non_evidence_artifacts(self) -> None:
        transport_calls = 0

        def transport(_url: str, _headers: object, body: bytes, _timeout: float) -> bytes:
            nonlocal transport_calls
            transport_calls += 1
            sent = json.loads(body)
            return json.dumps(
                {
                    "id": "private-response-id",
                    "model": sent["model"],
                    "choices": [
                        {"message": {"content": "synthetic output"}, "finish_reason": "stop"}
                    ],
                    "usage": {"prompt_tokens": 20, "completion_tokens": 4, "total_tokens": 24},
                }
            ).encode("utf-8")

        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with (
                patch(
                    "tools.assurance_eval.transport_smoke._clean_git_revision",
                    return_value="test-revision",
                ),
                patch(
                    "tools.assurance_eval.runner._git_revision",
                    return_value="test-revision",
                ),
                patch(
                    "tools.assurance_eval.runner._working_tree_status",
                    return_value={
                        "available": True,
                        "dirty": False,
                        "entry_count": 0,
                        "status_sha256": "0" * 64,
                    },
                ),
            ):
                code, report = execute_transport_smoke(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=transport,
                )
            run_dir = Path(report["artifact_path"])
            artifact_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in run_dir.rglob("*.json")
            )

        self.assertEqual(code, 0)
        self.assertEqual(transport_calls, 1)
        self.assertEqual(report["network_call_count"], 1)
        self.assertEqual(report["smoke_status"], "passed")
        self.assertEqual(report["evidence_use"], EVIDENCE_LABEL)
        self.assertEqual(report["declared_model_snapshot_status"], "unknown")
        self.assertFalse(report["secret_scan_found"])
        self.assertNotIn("synthetic-secret-key", artifact_text)
        self.assertNotIn("private.example.invalid", artifact_text)
        self.assertNotIn("private-response-id", artifact_text)

    def test_retryable_failure_is_not_retried_or_graded(self) -> None:
        transport_calls = 0

        def failing_transport(*_args: object) -> bytes:
            nonlocal transport_calls
            transport_calls += 1
            raise ProviderError("synthetic transport failure", retryable=True)

        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with (
                patch(
                    "tools.assurance_eval.transport_smoke._clean_git_revision",
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
            ):
                code, report = execute_transport_smoke(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=failing_transport,
                )
            record = json.loads(
                (Path(report["artifact_path"]) / "records" / "p002__B0__r001.json").read_text()
            )

        self.assertEqual(code, 1)
        self.assertEqual(transport_calls, 1)
        self.assertEqual(report["network_call_count"], 1)
        self.assertIsNone(record["grader"])

    def test_dirty_tree_at_transport_boundary_performs_no_transport(self) -> None:
        with tempfile.TemporaryDirectory() as config_dir, tempfile.TemporaryDirectory() as output:
            config_path = write_config(config_dir)
            with (
                patch(
                    "tools.assurance_eval.transport_smoke._clean_git_revision",
                    side_effect=["test-revision", ValueError("dirty")],
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
            ):
                code, report = execute_transport_smoke(
                    repo_root=REPO_ROOT,
                    config_path=config_path,
                    output_root=Path(output),
                    confirm_network=True,
                    transport=lambda *_: self.fail("transport must not be called"),
                )

        self.assertEqual(code, 1)
        self.assertEqual(report["network_call_count"], 0)


if __name__ == "__main__":
    unittest.main()
