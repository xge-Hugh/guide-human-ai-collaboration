"""Offline-only preparation for the direct Qwen grader compatibility check."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .direct_grader import (
    CONFIGURED_MODEL,
    MODEL_FAMILY,
    MODEL_SETTINGS,
    RENDERER_ID,
    render_grader_packet,
    renderer_content_sha256,
)
from .grader_bridge import export_compatibility_fixture
from .runner import _write_new_json


CONFIG_FILE = "assurance-v2-direct-grader-compatibility-smoke.json"
REQUEST_FILENAME = "grader_model_visible_request.json"
RUN_MODE = "direct_grader_compatibility_smoke"
EVIDENCE_USE = "direct_grader_transport_contract_only_not_phase_b_effect_evidence"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_and_validate(repo_root: Path) -> tuple[dict[str, Any], str]:
    experiment_dir = repo_root / "docs" / "experiments"
    path = experiment_dir / CONFIG_FILE
    raw = path.read_bytes()
    value = json.loads(raw)
    fixture_path = experiment_dir / "assurance-v2-grader-contract-compatibility-fixture.json"
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError("unsupported direct grader compatibility configuration")
    if value.get("status") != "candidate_pending_human_approval_not_executed":
        raise ValueError("direct grader compatibility approval status differs")
    if value.get("execution_enabled") is not False:
        raise ValueError("direct grader compatibility execution must remain disabled")
    if value.get("run_mode") != RUN_MODE or value.get("evidence_use") != EVIDENCE_USE:
        raise ValueError("direct grader compatibility evidence identity differs")
    if value.get("source_fixture") != {
        "path": "docs/experiments/assurance-v2-grader-contract-compatibility-fixture.json",
        "sha256": _sha256(fixture_path.read_bytes()),
    }:
        raise ValueError("direct grader fixture provenance is stale")
    if value.get("packet_id") != "grader-contract-p004-synthetic-v1":
        raise ValueError("direct grader compatibility packet differs")
    if value.get("provider_provenance") != {
        "transport_provider": "custom_isolated_provider",
        "model_family": MODEL_FAMILY,
        "model_family_basis": (
            "human_declared_distinct_family_provider_route_not_api_verified"
        ),
        "configured_model": CONFIGURED_MODEL,
        "declared_snapshot": None,
        "official_model_vendor_api_claimed": False,
        "uncontrolled_factors": [
            "backend_identity",
            "custom_provider_routing",
            "server_side_model_alias_resolution",
            "provider_retention",
        ],
    }:
        raise ValueError("direct grader provider provenance differs")
    if value.get("renderer") != {
        "id": RENDERER_ID,
        "sha256": renderer_content_sha256(),
        "language": "zh-CN",
        "exact_model_visible_request_required": True,
    }:
        raise ValueError("direct grader renderer provenance differs")
    if value.get("model_settings") != {
        **MODEL_SETTINGS,
        "reasoning_effort": "not_sent",
        "temperature": "not_sent",
        "top_p": "not_sent",
        "tools": "not_sent",
        "max_retries": 0,
    }:
        raise ValueError("direct grader model settings differ")
    gate = value.get("network_gate")
    if gate != {
        "explicit_flag": "--confirm-network",
        "maximum_grader_network_calls": 1,
        "one_shot_transport_guard_required": True,
        "formal_replay_authorized": False,
    }:
        raise ValueError("direct grader network gate differs")
    return value, _sha256(raw)


def prepare_offline(*, repo_root: Path, output_dir: Path) -> dict[str, Any]:
    config, config_sha256 = load_and_validate(repo_root)
    exported = export_compatibility_fixture(repo_root=repo_root, output_dir=output_dir)
    packet_path = Path(exported["packet_path"])
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    effective_request = {"model": CONFIGURED_MODEL, **render_grader_packet(packet)}
    request_path = output_dir.resolve() / REQUEST_FILENAME
    _write_new_json(request_path, effective_request)
    return {
        "status": "prepared_offline_not_executed",
        "execution_enabled": config["execution_enabled"],
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "configured_model": CONFIGURED_MODEL,
        "model_family": MODEL_FAMILY,
        "packet_sha256": exported["packet_sha256"],
        "request_sha256": _sha256(request_path.read_bytes()),
        "renderer_id": RENDERER_ID,
        "renderer_sha256": renderer_content_sha256(),
        "config_sha256": config_sha256,
        "model_calls": 0,
        "network_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the direct grader request offline.")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    report = prepare_offline(
        repo_root=Path(__file__).resolve().parents[2], output_dir=args.output_dir
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
