"""Explicit one-call thinking-enabled compatibility smoke path."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import stat
from pathlib import Path
from typing import Any, Mapping

from .formal_replay import COMMON_BASE_INSTRUCTION, USER_TEMPLATE
from .loading import load_phase_b_inputs
from .local_config import load_only_local_provider_config_and_scan_values
from .models import ProviderDescriptor, ProviderResponse, RunConfig
from .openai_compat import (
    DeepSeekChatCompletionsProvider,
    Transport,
    _chat_completions_url,
    urllib_transport,
)
from .providers import ProviderError, ScriptedFakeProvider
from .runner import AssuranceEvalRunner, _runner_source_digest
from .transport_smoke import (
    _clean_git_revision,
    _scan_artifacts,
    _tree_sha256,
    _validate_output_root,
)


CONFIG_FILE = "assurance-v2-thinking-compatibility-smoke.json"
RUN_MODE = "thinking_compatibility_smoke"
EVIDENCE_USE = "thinking_compatibility_only_not_phase_b_effect_evidence"
RENDERER_ID = "phase-b-thinking-compat-smoke-generator-zh-cn-v1"
MODEL_SETTINGS = {
    "thinking": {"type": "enabled"},
    "max_tokens": 4096,
    "stream": False,
}
RENDERER_SPEC = {
    "renderer_id": RENDERER_ID,
    "system_instruction": COMMON_BASE_INSTRUCTION,
    "user_template": USER_TEMPLATE,
    "case_id": "p002",
    "variant_id": "B0",
    "model_settings": MODEL_SETTINGS,
}


def render_generator_request(request: Mapping[str, Any]) -> dict[str, Any]:
    packet = request.get("packet")
    if request.get("call_kind") != "generator" or not isinstance(packet, Mapping):
        raise ValueError("thinking compatibility renderer requires a generator packet")
    if request.get("variant_id") != "B0" or packet.get("case_id") != "p002":
        raise ValueError("thinking compatibility renderer is fixed to p002/B0")
    if request.get("system_instruction") != COMMON_BASE_INSTRUCTION:
        raise ValueError("thinking compatibility renderer requires the formal base instruction")
    pre_context = packet.get("pre_context")
    user_message = packet.get("user_message")
    if not isinstance(pre_context, str) or not isinstance(user_message, str):
        raise ValueError("thinking compatibility packet fields must be strings")
    return {
        "messages": [
            {"role": "system", "content": COMMON_BASE_INSTRUCTION},
            {
                "role": "user",
                "content": (
                    f"【前置上下文】\n{pre_context}\n\n"
                    f"【用户当前消息】\n{user_message}"
                ),
            },
        ],
        **MODEL_SETTINGS,
    }


def renderer_source_sha256() -> str:
    content = (
        json.dumps(RENDERER_SPEC, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        + inspect.getsource(render_generator_request)
    ).encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def _load_and_validate(repo_root: Path) -> tuple[dict[str, Any], str]:
    path = repo_root / "docs" / "experiments" / CONFIG_FILE
    raw = path.read_bytes()
    config = json.loads(raw)
    if config.get("schema_version") != 1:
        raise ValueError("unsupported thinking compatibility config")
    expected_renderer = {
        "id": RENDERER_ID,
        "sha256": renderer_source_sha256(),
        "language": "zh-CN",
    }
    if config.get("renderer") != expected_renderer:
        raise ValueError("thinking compatibility renderer identity differs")
    if config.get("execution_enabled") is not True:
        raise ValueError("thinking compatibility execution is not approved")
    if config.get("status") != "human_approved_for_exactly_one_compatibility_call":
        raise ValueError("thinking compatibility approval status differs")
    if config.get("approval_scope") != (
        "one_generator_call_only_no_formal_replay_or_real_grader"
    ):
        raise ValueError("thinking compatibility approval scope differs")
    if any(
        (
            config.get("run_mode") != RUN_MODE,
            config.get("evidence_use") != EVIDENCE_USE,
            config.get("case_id") != "p002",
            config.get("variant_id") != "B0",
            config.get("repetitions") != 1,
            config.get("maximum_generator_network_calls") != 1,
            config.get("grader") != "deterministic_fake_no_network",
        )
    ):
        raise ValueError("thinking compatibility call scope differs")
    if config.get("provider_provenance") != {
        "transport_provider": "custom_isolated_provider",
        "model_family": "DeepSeek",
        "configured_model": "deepseek-v4-flash",
        "declared_snapshot": None,
        "official_deepseek_api_claimed": False,
        "uncontrolled_factors": [
            "custom_provider_routing",
            "backend_identity",
            "backend_seed",
            "server_side_model_alias_resolution",
            "provider_retention",
        ],
    }:
        raise ValueError("thinking compatibility provider provenance differs")
    if config.get("generator_model") != {
        "configured_model": "deepseek-v4-flash",
        "declared_snapshot": None,
        "thinking": {"type": "enabled"},
        "reasoning_effort": "not_sent_provider_support_unverified",
        "temperature": "not_sent_effect_under_thinking_unverified",
        "top_p": "not_sent_effect_under_thinking_unverified",
        "max_tokens": 4096,
        "output_budget_status": "provisional_pending_smoke_and_human_cost_limit",
        "stream": False,
        "max_retries": 0,
    }:
        raise ValueError("thinking compatibility model settings differ")
    if config.get("required_artifacts") != [
        "exact_secret_free_model_visible_request",
        "final_content_without_reasoning_content",
        "finish_reason",
        "numeric_usage_including_reasoning_tokens_when_returned",
        "elapsed_ms",
        "configured_declared_and_provider_reported_model_identity",
    ]:
        raise ValueError("thinking compatibility artifact requirements differ")
    if config.get("blocking_outcomes") != [
        "thinking_parameter_rejected",
        "finish_reason_length",
        "reasoning_content_retained",
        "secret_scan_match",
        "unexpected_provider_response",
    ]:
        raise ValueError("thinking compatibility blocking outcomes differ")
    return config, hashlib.sha256(raw).hexdigest()


def preflight_thinking_compatibility(
    *,
    repo_root: Path,
    config_path: Path,
    output_root: Path,
    confirm_network: bool,
) -> tuple[int, dict[str, Any]]:
    provider_config, _ = load_only_local_provider_config_and_scan_values(
        config_path, repository_root=repo_root
    )
    if _consumption_marker(config_path).exists():
        raise ValueError("thinking compatibility one-call approval was already consumed")
    revision = _clean_git_revision(repo_root)
    resolved_output_root = _validate_output_root(output_root, repo_root)
    if not resolved_output_root.is_dir():
        raise ValueError("compatibility output root must already exist as a private directory")
    if stat.S_IMODE(resolved_output_root.stat().st_mode) & 0o077:
        raise PermissionError(
            "compatibility output root must not be accessible by group or other users"
        )
    smoke_config, config_sha256 = _load_and_validate(repo_root)
    expected_model = smoke_config["generator_model"]["configured_model"]
    if provider_config.configured_model != expected_model:
        raise ValueError("local configured model differs from compatibility proposal")
    if provider_config.provider != "custom":
        raise ValueError("compatibility smoke requires the approved custom provider boundary")
    if provider_config.declared_model_snapshot is not None:
        raise ValueError("compatibility smoke approval requires the snapshot to remain unknown")
    report = {
        "preflight": "passed",
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "network_call_count": 0,
        "generator_call_count": 0,
        "grader_call_count": 0,
        "configured_model": provider_config.configured_model,
        "declared_model_snapshot_status": (
            "known" if provider_config.declared_model_snapshot is not None else "unknown"
        ),
        "renderer_id": RENDERER_ID,
        "renderer_sha256": renderer_source_sha256(),
        "configuration_sha256": config_sha256,
        "git_revision": revision,
        "working_tree_clean": True,
        "transport_provider": "custom_isolated_provider",
        "model_family": "DeepSeek",
    }
    if not confirm_network:
        return 2, {**report, "network_confirmation": "missing; no call made"}
    return 0, {**report, "network_confirmation": "present; approved for one call"}


def _fake_grader() -> ScriptedFakeProvider:
    raw_grade = json.dumps(
        {
            "applicability": "uncertain",
            "applicability_basis": "Deterministic compatibility fixture; not a behavior judgment.",
            "timing": "too_late",
            "satisfaction": "unsatisfied",
            "human_compensation_needed": "unclear",
            "over_trigger_cost": "none",
            "notes": "Fake grader used only to validate non-effect artifact plumbing.",
        }
    )
    return ScriptedFakeProvider(
        ProviderDescriptor(
            provider="fake",
            configured_model="deterministic-thinking-compatibility-fixture",
            context_mode="standalone",
            public_parameters={"network": False, "evidence_role": "compatibility_only"},
        ),
        [ProviderResponse(raw_grade, "deterministic-thinking-compatibility-fixture")],
    )


def _contains_reasoning_content_key(value: object) -> bool:
    if isinstance(value, dict):
        return "reasoning_content" in value or any(
            _contains_reasoning_content_key(child) for child in value.values()
        )
    if isinstance(value, list):
        return any(_contains_reasoning_content_key(child) for child in value)
    return False


def _artifacts_are_private(run_dir: Path) -> bool:
    for path in (run_dir, *run_dir.rglob("*")):
        mode = stat.S_IMODE(path.stat().st_mode)
        if path.is_dir() and mode & 0o077:
            return False
        if path.is_file() and mode & 0o177:
            return False
    return True


def _consumption_marker(config_path: Path) -> Path:
    return config_path.resolve().with_name(
        ".assurance-thinking-compatibility-smoke-v1-consumed"
    )


def _consume_one_call_approval(config_path: Path, revision: str, config_sha256: str) -> None:
    marker = _consumption_marker(config_path)
    payload = json.dumps(
        {
            "approval": "thinking_compatibility_smoke_one_call_consumed",
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


def execute_thinking_compatibility(
    *,
    repo_root: Path,
    config_path: Path,
    output_root: Path,
    confirm_network: bool,
    transport: Transport | None = None,
) -> tuple[int, dict[str, Any]]:
    preflight_code, preflight = preflight_thinking_compatibility(
        repo_root=repo_root,
        config_path=config_path,
        output_root=output_root,
        confirm_network=confirm_network,
    )
    if preflight_code != 0:
        return preflight_code, preflight

    provider_config, private_config_values = load_only_local_provider_config_and_scan_values(
        config_path, repository_root=repo_root
    )
    private_config_sha256 = hashlib.sha256(config_path.resolve().read_bytes()).digest()
    revision = preflight["git_revision"]
    resolved_output_root = _validate_output_root(output_root, repo_root)
    smoke_config, config_sha256 = _load_and_validate(repo_root)
    if (
        provider_config.provider != "custom"
        or provider_config.configured_model
        != smoke_config["generator_model"]["configured_model"]
        or provider_config.declared_model_snapshot is not None
    ):
        raise ValueError("local provider identity differs from the approved smoke")
    source_packet = load_phase_b_inputs(repo_root).generation["p002"]
    semantic_request = {
        "call_kind": "generator",
        "variant_id": "B0",
        "system_instruction": COMMON_BASE_INSTRUCTION,
        "packet": {
            "case_id": "p002",
            "pre_context": source_packet["pre_context"],
            "user_message": source_packet["user_message"],
        },
    }
    expected_request = {
        "model": provider_config.configured_model,
        **render_generator_request(semantic_request),
    }
    expected_body = json.dumps(
        expected_request, ensure_ascii=False, allow_nan=False, separators=(",", ":")
    ).encode("utf-8")
    private_needles = tuple(value.encode("utf-8") for value in private_config_values if value)
    if any(needle in expected_body for needle in private_needles):
        raise ValueError("secret value appears in the canonical model-visible request")

    network_counter = {"count": 0}
    response_observation: dict[str, Any] = {
        "reasoning_tokens_supplied": False,
        "reasoning_tokens_numeric": True,
        "reasoning_tokens": None,
    }
    base_transport = urllib_transport if transport is None else transport

    def one_shot_clean_transport(
        url: str, headers: Mapping[str, str], body: bytes, timeout: float
    ) -> bytes:
        if network_counter["count"] >= smoke_config["maximum_generator_network_calls"]:
            raise ProviderError("one-call network limit already consumed", retryable=False)
        if _clean_git_revision(repo_root) != revision:
            raise ProviderError("working tree changed before network call", retryable=False)
        current_config, current_sha256 = _load_and_validate(repo_root)
        if current_sha256 != config_sha256 or current_config != smoke_config:
            raise ProviderError("compatibility configuration changed before call", retryable=False)
        if hashlib.sha256(config_path.resolve().read_bytes()).digest() != private_config_sha256:
            raise ProviderError("local provider configuration changed before call", retryable=False)
        current_output = _validate_output_root(resolved_output_root, repo_root)
        if stat.S_IMODE(current_output.stat().st_mode) & 0o077:
            raise ProviderError("output directory permissions changed before call", retryable=False)
        if body != expected_body:
            raise ProviderError("model-visible request differs from approved bytes", retryable=False)
        if any(needle in body for needle in private_needles):
            raise ProviderError("secret value appears in model-visible request", retryable=False)
        if url != _chat_completions_url(provider_config.base_url) or dict(headers) != {
            "Authorization": f"Bearer {provider_config.api_key}",
            "Content-Type": "application/json",
        }:
            raise ProviderError("provider transport envelope differs", retryable=False)
        network_counter["count"] += 1
        response_bytes = base_transport(url, headers, body, timeout)
        try:
            response_document = json.loads(response_bytes)
            details = response_document.get("usage", {}).get("completion_tokens_details", {})
            if isinstance(details, dict) and "reasoning_tokens" in details:
                response_observation["reasoning_tokens_supplied"] = True
                value = details["reasoning_tokens"]
                valid = (
                    isinstance(value, int)
                    and not isinstance(value, bool)
                    and value >= 0
                )
                response_observation["reasoning_tokens_numeric"] = valid
                if valid:
                    response_observation["reasoning_tokens"] = value
        except (json.JSONDecodeError, AttributeError):
            pass
        return response_bytes

    generator = DeepSeekChatCompletionsProvider(
        provider_config,
        request_renderer=render_generator_request,
        renderer_id=RENDERER_ID,
        renderer_sha256=renderer_source_sha256(),
        transport=one_shot_clean_transport,
        allow_thinking=True,
        provider_boundary="custom_isolated_provider",
        model_family="DeepSeek",
    )
    runner_config = RunConfig(
        output_root=resolved_output_root,
        base_generator_instruction=COMMON_BASE_INSTRUCTION,
        grader_instruction="Deterministic fake grader for compatibility validation only.",
        grader_normative_context="Compatibility fixture; no Phase B conclusion may be drawn.",
        case_ids=("p002",),
        variant_ids=("B0",),
        run_mode=RUN_MODE,
        generator_base_language="zh-CN",
        case_packet_language="zh-CN",
        variant_condition_language="none",
        grader_instruction_language="synthetic",
        grader_context_language="synthetic",
        repetitions=1,
        max_retries=0,
    )
    _consume_one_call_approval(config_path, revision, config_sha256)
    run_dir = AssuranceEvalRunner(repo_root, generator, _fake_grader()).run(runner_config)
    record = json.loads(
        (run_dir / "records" / "p002__B0__r001.json").read_text(encoding="utf-8")
    )
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    completed = json.loads((run_dir / "completed.json").read_text(encoding="utf-8"))
    generator_record = record["generator"]
    grader_record = record.get("grader")
    metadata = generator_record.get("public_response_metadata", {})
    usage = metadata.get("usage") if isinstance(metadata, dict) else None
    ordinary_usage_recorded = isinstance(usage, dict) and all(
        isinstance(usage.get(key), int)
        and not isinstance(usage.get(key), bool)
        and usage[key] >= 0
        for key in ("prompt_tokens", "completion_tokens", "total_tokens")
    )
    final_content = generator_record.get("raw_output")
    finish_reason = metadata.get("finish_reason") if isinstance(metadata, dict) else None
    provider_reported_model = generator_record.get("provider_reported_model")
    request_preserved = generator_record.get("model_visible_request") == expected_request
    identity_preserved = generator_record.get("model_identity") == {
        "configured_model": provider_config.configured_model,
        "declared_model_snapshot": provider_config.declared_model_snapshot,
        "provider_reported_model": provider_reported_model,
    }
    elapsed_ms = generator_record.get("elapsed_ms")
    elapsed_recorded = (
        isinstance(elapsed_ms, (int, float))
        and not isinstance(elapsed_ms, bool)
        and elapsed_ms >= 0
    )
    attempts = generator_record.get("attempts")
    single_attempt_recorded = (
        isinstance(attempts, list)
        and len(attempts) == 1
        and generator_record.get("retry_count") == 0
        and isinstance(attempts[0].get("elapsed_ms"), (int, float))
        and not isinstance(attempts[0].get("elapsed_ms"), bool)
        and attempts[0]["elapsed_ms"] >= 0
    )
    provider_descriptor = manifest.get("generator_provider", {})
    provider_parameters = provider_descriptor.get("public_parameters", {})
    provider_boundary_valid = (
        provider_descriptor.get("provider") == "custom"
        and provider_parameters.get("provider_boundary") == "custom_isolated_provider"
        and provider_parameters.get("model_family") == "DeepSeek"
        and set(provider_descriptor.get("uncontrolled_parameters", []))
        == {
            "backend_identity",
            "backend_seed",
            "custom_provider_routing",
            "server_side_model_alias_resolution",
            "provider_retention",
        }
    )
    evidence_label_valid = all(
        value == EVIDENCE_USE
        for value in (
            manifest.get("evidence_use"),
            record.get("evidence_use"),
            generator_record.get("evidence_use"),
            (grader_record or {}).get("evidence_use"),
            summary.get("evidence_use"),
            completed.get("evidence_use"),
        )
    )
    grader_is_fake = (
        isinstance(grader_record, dict)
        and grader_record.get("provider", {}).get("provider") == "fake"
        and grader_record.get("invocation_status") == "succeeded"
    )
    provenance_valid = (
        manifest.get("runner_provenance", {}).get("git_revision") == revision
        and manifest.get("runner_provenance", {}).get("working_tree", {}).get("dirty") is False
        and manifest.get("runner_provenance", {}).get("runner_source_sha256")
        == _runner_source_digest(repo_root)
    )
    try:
        post_call_tree_clean = _clean_git_revision(repo_root) == revision
    except ValueError:
        post_call_tree_clean = False
    artifact_documents = [
        json.loads(path.read_text(encoding="utf-8")) for path in run_dir.rglob("*.json")
    ]
    reasoning_content_retained = any(
        _contains_reasoning_content_key(document) for document in artifact_documents
    )
    private_values = (*private_config_values, *generator.private_artifact_scan_values())
    secret_found = _scan_artifacts(run_dir, private_values)
    permissions_private = _artifacts_are_private(run_dir)
    reasoning_tokens = None
    if isinstance(usage, dict):
        details = usage.get("completion_tokens_details")
        if isinstance(details, dict):
            reasoning_tokens = details.get("reasoning_tokens")
    reasoning_usage_preserved = (
        not response_observation["reasoning_tokens_supplied"]
        or (
            response_observation["reasoning_tokens_numeric"]
            and reasoning_tokens == response_observation["reasoning_tokens"]
        )
    )
    blocking_outcomes: list[str] = []
    checks = {
        "generator_invocation_succeeded": generator_record.get("invocation_status") == "succeeded",
        "exactly_one_network_call": network_counter["count"] == 1,
        "valid_final_content": isinstance(final_content, str) and bool(final_content.strip()),
        "finish_reason_stop": finish_reason == "stop",
        "request_preserved": request_preserved,
        "model_identity_preserved": identity_preserved,
        "elapsed_recorded": elapsed_recorded,
        "single_attempt_zero_retries": single_attempt_recorded,
        "ordinary_usage_recorded": ordinary_usage_recorded,
        "numeric_reasoning_tokens_preserved_when_supplied": reasoning_usage_preserved,
        "reasoning_content_not_retained": not reasoning_content_retained,
        "secret_scan_passed": not secret_found,
        "private_artifact_permissions": permissions_private,
        "fake_grader_non_effect_label": grader_is_fake and evidence_label_valid,
        "committed_provenance_valid": provenance_valid,
        "post_call_tree_clean": post_call_tree_clean,
        "provider_boundary_valid": provider_boundary_valid,
    }
    for name, passed in checks.items():
        if not passed:
            blocking_outcomes.append(name)
    verification_passed = not blocking_outcomes
    report = {
        "smoke_status": "passed" if verification_passed else "failed",
        "network_call_count": network_counter["count"],
        "generator_call_count": network_counter["count"],
        "grader_call_count": 0,
        "fake_grader_invocation_count": 1 if grader_is_fake else 0,
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "transport_provider": "custom_isolated_provider",
        "model_family": "DeepSeek",
        "official_deepseek_api_claimed": False,
        "configured_model": provider_config.configured_model,
        "provider_reported_model": provider_reported_model,
        "declared_model_snapshot_status": (
            "known" if provider_config.declared_model_snapshot is not None else "unknown"
        ),
        "finish_reason": finish_reason,
        "usage": usage,
        "reasoning_tokens": reasoning_tokens,
        "elapsed_ms": elapsed_ms,
        "reasoning_content_retained": reasoning_content_retained,
        "request_preserved": request_preserved,
        "secret_scan": "fail" if secret_found else "pass",
        "artifact_permissions": "private" if permissions_private else "failed",
        "artifact_path": str(run_dir),
        "artifact_tree_sha256": _tree_sha256(run_dir),
        "blocking_outcomes": blocking_outcomes,
        "one_call_approval_consumed": _consumption_marker(config_path).exists(),
    }
    return (0 if verification_passed else 1), report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the one approved thinking-enabled compatibility generator call."
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--confirm-network", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    code, report = execute_thinking_compatibility(
        repo_root=Path(__file__).resolve().parents[2],
        config_path=args.config,
        output_root=args.output_dir,
        confirm_network=args.confirm_network,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
