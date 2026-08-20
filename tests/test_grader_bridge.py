from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.assurance_eval.grader_bridge import (
    EVIDENCE_USE,
    export_compatibility_fixture,
    import_scorer_output,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_private_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    os.chmod(path, 0o600)


def not_applicable_grade() -> dict[str, str]:
    return {
        "applicability": "not_applicable",
        "applicability_basis": "synthetic bridge result",
        "timing": "not_applicable",
        "satisfaction": "not_applicable",
        "human_compensation_needed": "no",
        "over_trigger_cost": "none",
        "notes": "offline fixture only",
    }


class GraderBridgeTest(unittest.TestCase):
    def test_exports_only_one_self_contained_p004_packet_without_forbidden_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = export_compatibility_fixture(
                repo_root=REPO_ROOT, output_dir=Path(directory)
            )
            files = list(Path(directory).iterdir())
            packet = json.loads(files[0].read_text(encoding="utf-8"))

        self.assertEqual(report["status"], "exported_not_scored")
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "grader_packet.json")
        self.assertEqual(packet["case_id"], "p004")
        self.assertEqual(packet["evidence_use"], EVIDENCE_USE)
        self.assertEqual(
            packet["generator_response_provenance"],
            "fixed_synthetic_fixture_not_generator_evidence",
        )
        serialized = json.dumps(packet, ensure_ascii=False)
        for forbidden in (
            "generator_reasoning",
            "reasoning_content",
            "other_repetitions",
            "other_variants",
            "expected_ordering",
            "experiment_summary",
            "prior_grader_results",
        ):
            self.assertNotIn(forbidden, serialized)
        self.assertIn("required_output_schema", packet)
        for absent_key in ("variant_id", "repetition", "experiment_summary"):
            self.assertNotIn(absent_key, packet)

    def test_imports_exact_json_with_provenance_without_modifying_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exported = export_compatibility_fixture(repo_root=REPO_ROOT, output_dir=root)
            packet_path = Path(exported["packet_path"])
            packet_before = packet_path.read_bytes()
            scorer_output = root / "scorer_output.json"
            write_private_json(scorer_output, not_applicable_grade())
            provenance_path = root / "scorer_provenance.json"
            write_private_json(
                provenance_path,
                {
                    "schema_version": 1,
                    "execution_id": "synthetic-offline-import",
                    "execution_path": "local_codex_cli_candidate",
                    "configured_model": "gpt-5.6-sol",
                    "model_family": "OpenAI GPT-5.6",
                    "model_snapshot": None,
                    "client_name": "codex-cli",
                    "client_version": "synthetic",
                    "fresh_context": True,
                    "ephemeral_session": True,
                    "working_directory_outside_repository": True,
                    "repository_access": "unavailable",
                    "conversation_inheritance": "none",
                    "injected_context": ["Codex base system instructions"],
                    "tool_access": "filesystem_isolated",
                    "network_access": "model_service_only",
                    "packet_sha256": hashlib.sha256(packet_before).hexdigest(),
                    "raw_output_sha256": hashlib.sha256(scorer_output.read_bytes()).hexdigest(),
                },
            )
            imported = import_scorer_output(
                repo_root=REPO_ROOT,
                packet_path=packet_path,
                scorer_output_path=scorer_output,
                scorer_provenance_path=provenance_path,
                output_dir=root,
            )

            self.assertEqual(packet_path.read_bytes(), packet_before)
            self.assertTrue((root / "imported_grade.json").is_file())

        self.assertEqual(imported["axis_results"]["applicability"], "not_applicable")
        self.assertEqual(
            imported["independence_claim"], "pending_execution_environment_verification"
        )
        self.assertEqual(
            imported["provenance_verification"]["execution_environment"],
            "externally_declared_not_bridge_verified",
        )
        self.assertFalse(imported["generator_evidence_modified"])
        self.assertEqual(imported["model_calls"], 0)

    def test_rejects_modified_packet_and_invalid_na_cross_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exported = export_compatibility_fixture(repo_root=REPO_ROOT, output_dir=root)
            packet_path = Path(exported["packet_path"])
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            packet["generator_final_response"] = "modified"
            write_private_json(packet_path, packet)
            output_path = root / "scorer_output.json"
            write_private_json(output_path, not_applicable_grade())
            provenance_path = root / "scorer_provenance.json"
            write_private_json(provenance_path, {})
            with self.assertRaisesRegex(ValueError, "packet was modified"):
                import_scorer_output(
                    repo_root=REPO_ROOT,
                    packet_path=packet_path,
                    scorer_output_path=output_path,
                    scorer_provenance_path=provenance_path,
                    output_dir=root,
                )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exported = export_compatibility_fixture(repo_root=REPO_ROOT, output_dir=root)
            packet_path = Path(exported["packet_path"])
            invalid = not_applicable_grade()
            invalid["timing"] = "on_time"
            output_path = root / "scorer_output.json"
            write_private_json(output_path, invalid)
            provenance_path = root / "scorer_provenance.json"
            write_private_json(provenance_path, {})
            with self.assertRaisesRegex(ValueError, "exactly when applicability"):
                import_scorer_output(
                    repo_root=REPO_ROOT,
                    packet_path=packet_path,
                    scorer_output_path=output_path,
                    scorer_provenance_path=provenance_path,
                    output_dir=root,
                )

    def test_rejects_duplicate_grade_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exported = export_compatibility_fixture(repo_root=REPO_ROOT, output_dir=root)
            packet_path = Path(exported["packet_path"])
            output_path = root / "scorer_output.json"
            output_path.write_text(
                '{"applicability":"not_applicable","applicability":"applicable"}',
                encoding="utf-8",
            )
            os.chmod(output_path, 0o600)
            provenance_path = root / "scorer_provenance.json"
            write_private_json(provenance_path, {})
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                import_scorer_output(
                    repo_root=REPO_ROOT,
                    packet_path=packet_path,
                    scorer_output_path=output_path,
                    scorer_provenance_path=provenance_path,
                    output_dir=root,
                )

if __name__ == "__main__":
    unittest.main()
