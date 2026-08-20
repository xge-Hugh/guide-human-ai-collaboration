"""Offline-only preparation gate for one thinking-enabled compatibility call."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import stat
from pathlib import Path
from typing import Any, Mapping

from .formal_replay import COMMON_BASE_INSTRUCTION, USER_TEMPLATE
from .local_config import load_only_local_provider_config_and_scan_values
from .transport_smoke import _clean_git_revision, _validate_output_root


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
    if config.get("execution_enabled") is not False:
        raise ValueError("thinking compatibility execution must remain disabled")
    if config.get("status") != "candidate_for_human_cost_privacy_approval":
        raise ValueError("thinking compatibility approval status differs")
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
    }
    if not confirm_network:
        return 2, {**report, "network_confirmation": "missing; no call made"}
    return 3, {
        **report,
        "network_confirmation": "present",
        "execution": "blocked_pending_human_cost_privacy_approval; no call made",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the one-call thinking compatibility proposal without a model call."
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--confirm-network", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    code, report = preflight_thinking_compatibility(
        repo_root=Path(__file__).resolve().parents[2],
        config_path=args.config,
        output_root=args.output_dir,
        confirm_network=args.confirm_network,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
