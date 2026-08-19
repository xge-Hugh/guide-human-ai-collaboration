from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.assurance_eval.local_config import (
    LocalProviderConfig,
    load_local_provider_config,
)
from tools.assurance_eval import (
    AssuranceEvalRunner,
    ProviderDescriptor,
    ProviderResponse,
    RunConfig,
    ScriptedFakeProvider,
)
from tools.assurance_eval.openai_compat import DeepSeekChatCompletionsProvider


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDERER_SHA256 = "0" * 64


def model_request_renderer(request: object) -> dict[str, object]:
    request_dict = dict(request)  # type: ignore[arg-type]
    return dict(request_dict["model_visible_request"])


class LocalConfigTest(unittest.TestCase):
    def test_loads_private_config_without_exposing_secrets_in_repr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "setting.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "connections": [
                            {
                                "label": "candidate-1",
                                "provider": "custom",
                                "api_style": "openai_chat_completions",
                                "base_url": "https://private.example.invalid",
                                "api_key": "test-secret-key",
                                "models": [
                                    {
                                        "model_id": "moving-alias",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            os.chmod(path, 0o600)
            config = load_local_provider_config(
                path, connection_label="candidate-1", repository_root=REPO_ROOT
            )

        self.assertEqual(config.configured_model, "moving-alias")
        self.assertIsNone(config.declared_model_snapshot)
        self.assertNotIn("test-secret-key", repr(config))
        self.assertNotIn("private.example.invalid", repr(config))

    def test_rejects_group_readable_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "setting.json"
            path.write_text("{}", encoding="utf-8")
            os.chmod(path, 0o640)
            with self.assertRaises(PermissionError):
                load_local_provider_config(
                    path, connection_label="candidate-1", repository_root=REPO_ROOT
                )

    def test_rejects_config_inside_repository(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT) as directory:
            path = Path(directory) / "setting.json"
            path.write_text("{}", encoding="utf-8")
            os.chmod(path, 0o600)
            with self.assertRaisesRegex(ValueError, "outside the repository"):
                load_local_provider_config(
                    path, connection_label="candidate-1", repository_root=REPO_ROOT
                )


class OpenAICompatProviderTest(unittest.TestCase):
    def config(self) -> LocalProviderConfig:
        return LocalProviderConfig(
            label="candidate-1",
            provider="custom",
            api_style="openai_chat_completions",
            configured_model="moving-alias",
            declared_model_snapshot="fixed-snapshot",
            base_url="https://private.example.invalid",
            api_key="test-secret-key",
        )

    def test_sends_exact_model_request_and_returns_only_public_metadata(self) -> None:
        captured: dict[str, object] = {}

        def transport(url: str, headers: object, body: bytes, timeout: float) -> bytes:
            captured.update(url=url, headers=headers, body=body, timeout=timeout)
            return json.dumps(
                {
                    "id": "private-correlation-id",
                    "model": "reported-alias",
                    "choices": [
                        {
                            "message": {"role": "assistant", "content": "原样输出\n"},
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 12,
                        "completion_tokens": 3,
                        "total_tokens": 15,
                    },
                },
                ensure_ascii=False,
            ).encode("utf-8")

        provider = DeepSeekChatCompletionsProvider(
            self.config(),
            request_renderer=model_request_renderer,
            renderer_id="toy-test-renderer",
            renderer_sha256=RENDERER_SHA256,
            timeout_seconds=7.0,
            transport=transport,
        )
        model_request = {
            "messages": [
                {"role": "system", "content": "共同指令"},
                {"role": "user", "content": "当前消息"},
            ],
            "temperature": 0,
            "max_tokens": 512,
            "thinking": {"type": "disabled"},
            "stream": False,
        }
        response = provider.invoke_standalone(
            {"call_kind": "generator", "model_visible_request": model_request}
        )

        sent = json.loads(captured["body"])
        self.assertEqual(sent, {"model": "moving-alias", **model_request})
        self.assertTrue(str(captured["url"]).endswith("/v1/chat/completions"))
        self.assertEqual(response.raw_output, "原样输出\n")
        self.assertEqual(response.provider_reported_model, "reported-alias")
        self.assertEqual(response.model_visible_request, sent)
        self.assertEqual(
            response.public_metadata,
            {
                "finish_reason": "stop",
                "usage": {"prompt_tokens": 12, "completion_tokens": 3, "total_tokens": 15},
            },
        )
        artifact_text = json.dumps(
            {
                "descriptor": provider.descriptor.__dict__,
                "request": response.model_visible_request,
                "metadata": response.public_metadata,
            },
            default=str,
        )
        self.assertNotIn("test-secret-key", artifact_text)
        self.assertNotIn("private.example.invalid", artifact_text)
        self.assertNotIn("private-correlation-id", artifact_text)

    def test_rejects_enabled_thinking_until_retention_is_decided(self) -> None:
        provider = DeepSeekChatCompletionsProvider(
            self.config(),
            request_renderer=model_request_renderer,
            renderer_id="toy-test-renderer",
            renderer_sha256=RENDERER_SHA256,
            transport=lambda *_: self.fail("transport must not be called"),
        )
        with self.assertRaisesRegex(ValueError, "explicitly disable thinking"):
            provider.invoke_standalone(
                {
                    "model_visible_request": {
                        "messages": [{"role": "user", "content": "test"}],
                        "thinking": {"type": "enabled"},
                    }
                }
            )

    def test_runner_uses_injected_renderer_without_network(self) -> None:
        def semantic_renderer(request: object) -> dict[str, object]:
            value = dict(request)  # type: ignore[arg-type]
            packet = value["packet"]
            return {
                "messages": [
                    {"role": "system", "content": value["system_instruction"]},
                    {
                        "role": "user",
                        "content": (
                            f"TOY CONTEXT: {packet['pre_context']}\n"
                            f"TOY MESSAGE: {packet['user_message']}"
                        ),
                    },
                ],
                "temperature": 0,
                "max_tokens": 64,
                "thinking": {"type": "disabled"},
                "stream": False,
            }

        def transport(_url: str, _headers: object, body: bytes, _timeout: float) -> bytes:
            sent = json.loads(body)
            return json.dumps(
                {
                    "model": sent["model"],
                    "choices": [
                        {"message": {"content": "toy generator"}, "finish_reason": "stop"}
                    ],
                    "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
                }
            ).encode("utf-8")

        generator = DeepSeekChatCompletionsProvider(
            self.config(),
            request_renderer=semantic_renderer,
            renderer_id="toy-runner-generator",
            renderer_sha256=RENDERER_SHA256,
            transport=transport,
        )
        grade = json.dumps(
            {
                "applicability": "uncertain",
                "applicability_basis": "toy integration result",
                "timing": "too_late",
                "satisfaction": "unsatisfied",
                "human_compensation_needed": "unclear",
                "over_trigger_cost": "none",
                "notes": "not evidence",
            }
        )
        grader = ScriptedFakeProvider(
            ProviderDescriptor(
                provider="fake",
                configured_model="fake-grader",
                context_mode="standalone",
            ),
            [ProviderResponse(grade, "fake-grader")],
        )
        with tempfile.TemporaryDirectory() as directory:
            run_dir = AssuranceEvalRunner(REPO_ROOT, generator, grader).run(
                RunConfig(
                    output_root=Path(directory),
                    base_generator_instruction="TOY BASE",
                    grader_instruction="TOY GRADER",
                    grader_normative_context="TOY CONTEXT",
                    case_ids=("p001",),
                    variant_ids=("B0",),
                    run_mode="fake_pipeline",
                    generator_base_language="en",
                    case_packet_language="zh-CN",
                    variant_condition_language="none",
                    grader_instruction_language="en",
                    grader_context_language="en",
                    repetitions=1,
                )
            )
            record = json.loads(next((run_dir / "records").iterdir()).read_text())

        self.assertEqual(record["generator"]["raw_output"], "toy generator")
        self.assertEqual(
            record["generator"]["model_identity"],
            {
                "configured_model": "moving-alias",
                "declared_model_snapshot": "fixed-snapshot",
                "provider_reported_model": "moving-alias",
            },
        )
        self.assertEqual(
            record["generator"]["provider"]["public_parameters"]["renderer_id"],
            "toy-runner-generator",
        )


if __name__ == "__main__":
    unittest.main()
