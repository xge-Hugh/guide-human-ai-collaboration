"""Offline-only preparation for the direct Qwen grader compatibility check."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import time
from pathlib import Path
from typing import Any, Mapping

from .direct_grader import (
    CONFIGURED_MODEL,
    MODEL_FAMILY,
    MODEL_SETTINGS,
    RENDERER_ID,
    render_grader_packet,
    renderer_content_sha256,
)
from .grader_bridge import export_compatibility_fixture
from .grader_bridge import import_scorer_output
from .local_config import load_only_local_provider_config_and_scan_values
from .openai_compat import (
    OpenAIChatCompletionsProvider,
    Transport,
    _chat_completions_url,
    urllib_transport,
)
from .providers import ProviderError
from .runner import _write_new_json
from .transport_smoke import (
    _clean_git_revision,
    _scan_artifacts,
    _tree_sha256,
    _validate_output_root,
)


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
    if value.get("status") != "human_approved_for_exactly_one_compatibility_call":
        raise ValueError("direct grader compatibility approval status differs")
    if value.get("execution_enabled") is not True:
        raise ValueError("direct grader compatibility execution is not approved")
    if value.get("approval_scope") != (
        "one_qwen_grader_compatibility_call_only_no_formal_replay"
    ):
        raise ValueError("direct grader compatibility approval scope differs")
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


def _consumption_marker(config_path: Path) -> Path:
    return config_path.resolve().with_name(
        ".assurance-direct-qwen-grader-compatibility-v1-consumed"
    )


def _consume_approval(config_path: Path, revision: str, config_sha256: str) -> None:
    marker = _consumption_marker(config_path)
    payload = json.dumps(
        {
            "approval": "direct_qwen_grader_compatibility_one_call_consumed",
            "git_revision": revision,
            "configuration_sha256": config_sha256,
        },
        sort_keys=True,
    ).encode("utf-8")
    try:
        descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise ProviderError("one-call approval was already consumed", retryable=False) from None
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def _write_new_bytes(path: Path, value: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def _artifacts_private(directory: Path) -> bool:
    for path in (directory, *directory.rglob("*")):
        mode = stat.S_IMODE(path.stat().st_mode)
        if path.is_dir() and mode & 0o077:
            return False
        if path.is_file() and mode & 0o177:
            return False
    return True


def preflight(
    *, repo_root: Path, config_path: Path, output_dir: Path, confirm_network: bool
) -> tuple[int, dict[str, Any]]:
    smoke_config, config_sha256 = load_and_validate(repo_root)
    provider_config, _ = load_only_local_provider_config_and_scan_values(
        config_path, repository_root=repo_root, model_id=CONFIGURED_MODEL
    )
    if _consumption_marker(config_path).exists():
        raise ValueError("direct grader compatibility approval was already consumed")
    revision = _clean_git_revision(repo_root)
    directory = _validate_output_root(output_dir, repo_root)
    if not directory.is_dir() or stat.S_IMODE(directory.stat().st_mode) & 0o077:
        raise PermissionError("direct grader compatibility output directory must be private")
    if any(directory.iterdir()):
        raise ValueError("direct grader compatibility output directory must be empty")
    if (
        provider_config.provider != "custom"
        or provider_config.configured_model != CONFIGURED_MODEL
        or provider_config.declared_model_snapshot is not None
    ):
        raise ValueError("local provider identity differs from approved Qwen compatibility")
    report = {
        "preflight": "passed",
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "configured_model": CONFIGURED_MODEL,
        "model_family": MODEL_FAMILY,
        "snapshot_status": "unknown",
        "configuration_sha256": config_sha256,
        "git_revision": revision,
        "network_call_count": 0,
        "formal_replay_authorized": False,
    }
    if not confirm_network:
        return 2, {**report, "network_confirmation": "missing; no call made"}
    return 0, {**report, "network_confirmation": "present; approved for one call"}


def execute(
    *,
    repo_root: Path,
    config_path: Path,
    output_dir: Path,
    confirm_network: bool,
    transport: Transport | None = None,
) -> tuple[int, dict[str, Any]]:
    preflight_code, preflight_report = preflight(
        repo_root=repo_root,
        config_path=config_path,
        output_dir=output_dir,
        confirm_network=confirm_network,
    )
    if preflight_code != 0:
        return preflight_code, preflight_report
    smoke_config, config_sha256 = load_and_validate(repo_root)
    provider_config, private_values = load_only_local_provider_config_and_scan_values(
        config_path, repository_root=repo_root, model_id=CONFIGURED_MODEL
    )
    private_config_sha256 = hashlib.sha256(config_path.resolve().read_bytes()).digest()
    revision = preflight_report["git_revision"]
    directory = _validate_output_root(output_dir, repo_root)
    prepared = prepare_offline(repo_root=repo_root, output_dir=directory)
    packet_path = directory / "grader_packet.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    expected_request = json.loads(
        (directory / REQUEST_FILENAME).read_text(encoding="utf-8")
    )
    semantic_request = {
        "call_kind": "grader",
        "packet_sha256": prepared["packet_sha256"],
    }

    def renderer(request: Mapping[str, Any]) -> Mapping[str, Any]:
        if dict(request) != semantic_request:
            raise ValueError("direct grader semantic request differs")
        return render_grader_packet(packet)

    expected_body = json.dumps(
        expected_request, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")
    needles = tuple(value.encode("utf-8") for value in private_values if value)
    if any(needle in expected_body for needle in needles):
        raise ValueError("secret value appears in direct grader request")
    network_counter = {"count": 0}
    base_transport = urllib_transport if transport is None else transport

    def one_shot_transport(
        url: str, headers: Mapping[str, str], body: bytes, timeout: float
    ) -> bytes:
        if network_counter["count"] >= 1:
            raise ProviderError("one-call network limit already consumed", retryable=False)
        if _clean_git_revision(repo_root) != revision:
            raise ProviderError("working tree changed before network call", retryable=False)
        current_config, current_sha256 = load_and_validate(repo_root)
        if current_config != smoke_config or current_sha256 != config_sha256:
            raise ProviderError("compatibility configuration changed before call", retryable=False)
        if hashlib.sha256(config_path.resolve().read_bytes()).digest() != private_config_sha256:
            raise ProviderError("local provider configuration changed before call", retryable=False)
        if body != expected_body or any(needle in body for needle in needles):
            raise ProviderError("direct grader request differs or contains a secret", retryable=False)
        if url != _chat_completions_url(provider_config.base_url) or dict(headers) != {
            "Authorization": f"Bearer {provider_config.api_key}",
            "Content-Type": "application/json",
        }:
            raise ProviderError("provider transport envelope differs", retryable=False)
        network_counter["count"] += 1
        return base_transport(url, headers, body, timeout)

    provider = OpenAIChatCompletionsProvider(
        provider_config,
        request_renderer=renderer,
        renderer_id=RENDERER_ID,
        renderer_sha256=renderer_content_sha256(),
        transport=one_shot_transport,
        allow_thinking=False,
        provider_boundary="custom_isolated_provider",
        model_family=MODEL_FAMILY,
    )
    _consume_approval(config_path, revision, config_sha256)
    started = time.perf_counter()
    try:
        response = provider.invoke_standalone(semantic_request)
    except (ProviderError, ValueError) as error:
        elapsed_ms = (time.perf_counter() - started) * 1000
        failure = {
            "schema_version": 1,
            "smoke_status": "failed",
            "run_mode": RUN_MODE,
            "evidence_use": EVIDENCE_USE,
            "git_revision": revision,
            "network_call_count": network_counter["count"],
            "configured_model": CONFIGURED_MODEL,
            "snapshot_status": "unknown",
            "elapsed_ms": elapsed_ms,
            "failure_type": type(error).__name__,
            "one_call_approval_consumed": True,
            "formal_replay_executed": False,
        }
        _write_new_json(directory / "transport_failure.json", failure)
        secret_found = _scan_artifacts(directory, private_values)
        return 1, {
            **failure,
            "secret_scan": "fail" if secret_found else "pass",
            "artifact_path": str(directory),
            "artifact_tree_sha256": _tree_sha256(directory),
            "blocking_outcomes": ["provider_invocation_failed_no_retry"],
        }
    elapsed_ms = (time.perf_counter() - started) * 1000
    scorer_output_path = directory / "scorer_output.json"
    raw_output = response.raw_output.encode("utf-8")
    _write_new_bytes(scorer_output_path, raw_output)
    provenance_path = directory / "scorer_provenance.json"
    _write_new_json(
        provenance_path,
        {
            "schema_version": 1,
            "execution_id": f"qwen-compat-{revision[:12]}",
            "execution_path": "direct_custom_provider_chat_completions",
            "configured_model": CONFIGURED_MODEL,
            "model_family": MODEL_FAMILY,
            "model_snapshot": None,
            "client_name": "assurance-eval-openai-compatible-transport",
            "client_version": revision,
            "fresh_context": True,
            "ephemeral_session": True,
            "working_directory_outside_repository": True,
            "repository_access": "unavailable",
            "conversation_inheritance": "none",
            "injected_context": ["canonical system message", "canonical grader packet"],
            "tool_access": "none",
            "network_access": "model_service_only",
            "packet_sha256": prepared["packet_sha256"],
            "raw_output_sha256": _sha256(raw_output),
        },
    )
    import_error: str | None = None
    try:
        imported = import_scorer_output(
            repo_root=repo_root,
            packet_path=packet_path,
            scorer_output_path=scorer_output_path,
            scorer_provenance_path=provenance_path,
            output_dir=directory,
        )
        import_succeeded = True
    except (ValueError, json.JSONDecodeError) as error:
        imported = None
        import_succeeded = False
        import_error = type(error).__name__
    metadata = dict(response.public_metadata)
    finish_reason = metadata.get("finish_reason")
    usage = metadata.get("usage") if isinstance(metadata.get("usage"), dict) else None
    request_preserved = response.model_visible_request == expected_request
    identity_preserved = bool(response.provider_reported_model)
    _write_new_json(
        directory / "transport_evidence.json",
        {
            "schema_version": 1,
            "run_mode": RUN_MODE,
            "evidence_use": EVIDENCE_USE,
            "git_revision": revision,
            "network_call_count": network_counter["count"],
            "configured_model": CONFIGURED_MODEL,
            "declared_model_snapshot": None,
            "provider_reported_model": response.provider_reported_model,
            "model_family": MODEL_FAMILY,
            "model_family_basis": (
                "human_declared_distinct_family_provider_route_not_api_verified"
            ),
            "renderer_id": RENDERER_ID,
            "renderer_sha256": renderer_content_sha256(),
            "request_sha256": prepared["request_sha256"],
            "raw_output_sha256": _sha256(raw_output),
            "finish_reason": finish_reason,
            "usage": usage,
            "elapsed_ms": elapsed_ms,
            "strict_import_succeeded": import_succeeded,
            "strict_import_error_type": import_error,
            "formal_replay_authorized": False,
        },
    )
    secret_found = _scan_artifacts(
        directory, (*private_values, *provider.private_artifact_scan_values())
    )
    try:
        post_call_tree_clean = _clean_git_revision(repo_root) == revision
    except ValueError:
        post_call_tree_clean = False
    checks = {
        "exactly_one_network_call": network_counter["count"] == 1,
        "finish_reason_stop": finish_reason == "stop",
        "nonempty_final_content": bool(response.raw_output.strip()),
        "request_preserved": request_preserved,
        "provider_reported_model_present": identity_preserved,
        "strict_import_succeeded": import_succeeded,
        "secret_scan_passed": not secret_found,
        "artifacts_private": _artifacts_private(directory),
        "post_call_tree_clean": post_call_tree_clean,
    }
    blocking = [name for name, passed in checks.items() if not passed]
    report = {
        "smoke_status": "passed" if not blocking else "failed",
        "network_call_count": network_counter["count"],
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "configured_model": CONFIGURED_MODEL,
        "provider_reported_model": response.provider_reported_model,
        "snapshot_status": "unknown",
        "finish_reason": finish_reason,
        "usage": usage,
        "elapsed_ms": elapsed_ms,
        "request_preserved": request_preserved,
        "reasoning_content_retained": False,
        "secret_scan": "fail" if secret_found else "pass",
        "artifact_path": str(directory),
        "artifact_tree_sha256": _tree_sha256(directory),
        "strict_import_succeeded": import_succeeded,
        "blocking_outcomes": blocking,
        "one_call_approval_consumed": _consumption_marker(config_path).exists(),
        "formal_replay_executed": False,
    }
    return (0 if not blocking else 1), report


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare or run the direct grader compatibility check.")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--confirm-network", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[2]
    if args.config is None:
        report = prepare_offline(repo_root=repo_root, output_dir=args.output_dir)
        code = 0
    else:
        code, report = execute(
            repo_root=repo_root,
            config_path=args.config,
            output_dir=args.output_dir,
            confirm_network=args.confirm_network,
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
