"""Offline export/import bridge for an externally executed packet-isolated grader."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
from pathlib import Path
from typing import Any, Mapping

from .runner import _write_new_json, parse_grade
from .transport_smoke import _validate_output_root


FIXTURE_FILE = "assurance-v2-grader-contract-compatibility-fixture.json"
PACKET_FILENAME = "grader_packet.json"
IMPORTED_GRADE_FILENAME = "imported_grade.json"
EVIDENCE_USE = "grader_contract_compatibility_fixture_not_phase_b_evidence"

_PROVENANCE_FIELDS = {
    "schema_version",
    "execution_id",
    "execution_path",
    "configured_model",
    "model_family",
    "model_snapshot",
    "client_name",
    "client_version",
    "fresh_context",
    "ephemeral_session",
    "working_directory_outside_repository",
    "repository_access",
    "conversation_inheritance",
    "injected_context",
    "tool_access",
    "network_access",
    "packet_sha256",
    "raw_output_sha256",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _loads_exact(raw: bytes) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r}")
            value[key] = child
        return value

    try:
        return json.loads(raw, object_pairs_hook=reject_duplicates)
    except UnicodeDecodeError:
        raise ValueError("grader bridge JSON must be UTF-8") from None


def _private_external_directory(path: Path, repo_root: Path) -> Path:
    resolved = _validate_output_root(path, repo_root)
    if not resolved.is_dir():
        raise ValueError("grader bridge directory must already exist")
    if stat.S_IMODE(resolved.stat().st_mode) & 0o077:
        raise PermissionError("grader bridge directory must be private")
    return resolved


def _private_input_file(path: Path, directory: Path) -> Path:
    if path.is_symlink():
        raise ValueError("grader bridge inputs must not be symlinks")
    resolved = path.resolve()
    if resolved.parent != directory or not resolved.is_file():
        raise ValueError("grader bridge inputs must be files in the private bridge directory")
    if stat.S_IMODE(resolved.stat().st_mode) & 0o077:
        raise PermissionError("grader bridge input files must be private")
    return resolved


def _load_fixture(repo_root: Path) -> tuple[dict[str, Any], str]:
    path = repo_root / "docs" / "experiments" / FIXTURE_FILE
    raw = path.read_bytes()
    fixture = _loads_exact(raw)
    if not isinstance(fixture, dict) or fixture.get("schema_version") != 1:
        raise ValueError("unsupported grader compatibility fixture")
    if fixture.get("status") != "prepared_not_executed":
        raise ValueError("grader compatibility fixture execution status differs")
    if fixture.get("evidence_use") != EVIDENCE_USE:
        raise ValueError("grader compatibility fixture evidence label differs")
    rubric_path = repo_root / "docs" / "experiments" / "assurance-v2-phase-b-rubrics.json"
    if fixture.get("source_rubric") != {
        "path": "docs/experiments/assurance-v2-phase-b-rubrics.json",
        "sha256": _sha256(rubric_path.read_bytes()),
    }:
        raise ValueError("grader fixture rubric provenance is stale")
    rubrics = _loads_exact(rubric_path.read_bytes())["rubrics"]
    p004 = next(item for item in rubrics if item.get("packet_id") == "p004")
    packet = fixture.get("grader_packet")
    if not isinstance(packet, dict):
        raise ValueError("grader compatibility packet is missing")
    if packet.get("case_id") != "p004" or packet.get("evidence_use") != EVIDENCE_USE:
        raise ValueError("grader compatibility packet identity differs")
    if packet.get("case_specific_normative_context") != {
        "reference_case": p004["reference_case"],
        "expected_applicability": p004["expected_applicability"],
        "adjudication": p004["adjudication"],
    }:
        raise ValueError("grader packet normative context differs from p004")
    if packet.get("hidden_semantic_acceptance_boundary") != {
        "required_protection": p004["required_protection"],
        "latest_useful_point": p004["latest_useful_point"],
    }:
        raise ValueError("grader packet hidden boundary differs from p004")
    if packet.get("generator_response_provenance") != (
        "fixed_synthetic_fixture_not_generator_evidence"
    ):
        raise ValueError("grader fixture generator provenance differs")
    return fixture, _sha256(raw)


def export_compatibility_fixture(*, repo_root: Path, output_dir: Path) -> dict[str, Any]:
    directory = _private_external_directory(output_dir, repo_root)
    fixture, fixture_sha256 = _load_fixture(repo_root)
    packet_path = directory / PACKET_FILENAME
    _write_new_json(packet_path, fixture["grader_packet"])
    packet_sha256 = _sha256(packet_path.read_bytes())
    return {
        "status": "exported_not_scored",
        "evidence_use": EVIDENCE_USE,
        "packet_path": str(packet_path),
        "packet_sha256": packet_sha256,
        "fixture_sha256": fixture_sha256,
        "model_calls": 0,
    }


def _validate_scorer_provenance(
    value: object, *, packet_sha256: str, raw_output_sha256: str
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _PROVENANCE_FIELDS:
        raise ValueError("scorer provenance fields differ from the bridge contract")
    for field in (
        "execution_id",
        "execution_path",
        "configured_model",
        "model_family",
        "client_name",
        "client_version",
    ):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"scorer provenance {field} must be non-empty")
    snapshot = value["model_snapshot"]
    if snapshot is not None and (not isinstance(snapshot, str) or not snapshot.strip()):
        raise ValueError("scorer provenance model_snapshot must be null or non-empty")
    for field in ("fresh_context", "ephemeral_session", "working_directory_outside_repository"):
        if not isinstance(value[field], bool):
            raise ValueError(f"scorer provenance {field} must be boolean")
    if value["conversation_inheritance"] not in {"none", "unknown"}:
        raise ValueError("unsupported conversation inheritance declaration")
    if value["repository_access"] not in {"unavailable", "available_not_used", "unknown"}:
        raise ValueError("unsupported repository access declaration")
    if value["tool_access"] not in {"none", "filesystem_isolated", "available_not_used", "unknown"}:
        raise ValueError("unsupported tool access declaration")
    if value["network_access"] not in {"model_service_only", "broader", "unknown"}:
        raise ValueError("unsupported network access declaration")
    injected = value["injected_context"]
    if not isinstance(injected, list) or not all(isinstance(item, str) for item in injected):
        raise ValueError("scorer provenance injected_context must be a string list")
    if value["packet_sha256"] != packet_sha256:
        raise ValueError("scorer provenance packet digest differs")
    if value["raw_output_sha256"] != raw_output_sha256:
        raise ValueError("scorer provenance output digest differs")
    return dict(value)


def import_scorer_output(
    *,
    repo_root: Path,
    packet_path: Path,
    scorer_output_path: Path,
    scorer_provenance_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    directory = _private_external_directory(output_dir, repo_root)
    packet_path = _private_input_file(packet_path, directory)
    scorer_output_path = _private_input_file(scorer_output_path, directory)
    scorer_provenance_path = _private_input_file(scorer_provenance_path, directory)
    fixture, fixture_sha256 = _load_fixture(repo_root)
    packet_raw = packet_path.read_bytes()
    packet = _loads_exact(packet_raw)
    if packet != fixture["grader_packet"]:
        raise ValueError("exported grader packet was modified or is not canonical")
    output_raw = scorer_output_path.read_bytes()
    raw_output = output_raw.decode("utf-8")
    _loads_exact(output_raw)
    axis_results = parse_grade(raw_output)
    provenance_raw = scorer_provenance_path.read_bytes()
    provenance = _validate_scorer_provenance(
        _loads_exact(provenance_raw),
        packet_sha256=_sha256(packet_raw),
        raw_output_sha256=_sha256(output_raw),
    )
    imported = {
        "schema_version": 1,
        "status": "imported_pending_human_review",
        "evidence_use": EVIDENCE_USE,
        "packet_id": packet["packet_id"],
        "case_id": packet["case_id"],
        "packet_sha256": _sha256(packet_raw),
        "fixture_sha256": fixture_sha256,
        "raw_scorer_output": raw_output,
        "raw_scorer_output_sha256": _sha256(output_raw),
        "axis_results": axis_results,
        "scorer_provenance": provenance,
        "provenance_verification": {
            "packet_digest": "bridge_verified",
            "raw_output_digest": "bridge_verified",
            "execution_environment": "externally_declared_not_bridge_verified",
        },
        "independence_claim": "pending_execution_environment_verification",
        "generator_evidence_modified": False,
    }
    destination = directory / IMPORTED_GRADE_FILENAME
    _write_new_json(destination, imported)
    if _sha256(packet_path.read_bytes()) != imported["packet_sha256"]:
        raise RuntimeError("grader packet changed during import")
    return {**imported, "imported_grade_path": str(destination), "model_calls": 0}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline external-grader packet bridge.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    export = subparsers.add_parser("export-fixture")
    export.add_argument("--output-dir", required=True, type=Path)
    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("--packet", required=True, type=Path)
    import_parser.add_argument("--scorer-output", required=True, type=Path)
    import_parser.add_argument("--scorer-provenance", required=True, type=Path)
    import_parser.add_argument("--output-dir", required=True, type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    if args.command == "export-fixture":
        report = export_compatibility_fixture(repo_root=repo_root, output_dir=args.output_dir)
    else:
        report = import_scorer_output(
            repo_root=repo_root,
            packet_path=args.packet,
            scorer_output_path=args.scorer_output,
            scorer_provenance_path=args.scorer_provenance,
            output_dir=args.output_dir,
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
