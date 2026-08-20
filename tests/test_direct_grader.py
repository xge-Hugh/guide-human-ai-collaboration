from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.assurance_eval.direct_grader import (
    CONFIGURED_MODEL,
    MODEL_FAMILY,
    MODEL_SETTINGS,
    RENDERER_ID,
    render_grader_packet,
    renderer_content_sha256,
)
from tools.assurance_eval.direct_grader_compatibility import prepare_offline


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
        self.assertFalse(report["execution_enabled"])
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(report["network_calls"], 0)
        self.assertEqual(request["model"], "qwen3.7-max")
        self.assertEqual(request["thinking"], {"type": "disabled"})
        self.assertNotIn("tools", request)


if __name__ == "__main__":
    unittest.main()
