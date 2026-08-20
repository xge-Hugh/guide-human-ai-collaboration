"""No-network preparation gate and canonical renderer for Stage 3."""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import stat
from pathlib import Path
from typing import Any, Mapping

from .loading import load_phase_b_inputs
from .local_config import load_only_local_provider_config_and_scan_values
from .models import CHINESE_VARIANTS_FILE
from .transport_smoke import _clean_git_revision, _validate_output_root


PROPOSAL_FILE = "assurance-v2-stage3-formal-proposal.json"
RUN_MODE = "formal_replay"
EVIDENCE_USE = "phase_b_controlled_replay_raw_evidence_pending_adjudication"
RENDERER_ID = "phase-b-formal-generator-zh-cn-v1"
COMMON_BASE_INSTRUCTION = (
    "你是当前协作中的 AI 助手。请根据提供的前置上下文，\n"
    "自然回应用户当前消息。"
)
USER_TEMPLATE = "【前置上下文】\n<packet.pre_context>\n\n【用户当前消息】\n<packet.user_message>"
MODEL_SETTINGS = {
    "thinking": {"type": "enabled"},
    "max_tokens": 4096,
    "stream": False,
}
LANGUAGE_METADATA = {
    "generator_base": "zh-CN",
    "case_packet": "zh-CN",
    "variant_condition": "zh-CN",
}
CASE_IDS = ("p003", "p004", "p005", "p006", "p007", "p008", "p009", "p011", "p012", "p013")
VARIANT_ORDERS = (
    ("B0", "B1", "B2"),
    ("B1", "B2", "B0"),
    ("B2", "B0", "B1"),
)
RENDERER_SPEC = {
    "renderer_id": RENDERER_ID,
    "common_base_instruction": COMMON_BASE_INSTRUCTION,
    "user_template": USER_TEMPLATE,
    "model_settings": MODEL_SETTINGS,
    "language_components": LANGUAGE_METADATA,
}


def _variant_appends() -> dict[str, str]:
    path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "experiments"
        / CHINESE_VARIANTS_FILE
    )
    document = json.loads(path.read_bytes())
    return {
        item["variant_id"]: item["instruction_append"]
        for item in document["variants"]
    }


def render_generator_request(request: Mapping[str, Any]) -> dict[str, Any]:
    packet = request.get("packet")
    if request.get("call_kind") != "generator" or not isinstance(packet, Mapping):
        raise ValueError("formal renderer requires a generator packet")
    variant_id = request.get("variant_id")
    appends = _variant_appends()
    if variant_id not in {"B0", "B1", "B2"}:
        raise ValueError("formal renderer requires B0, B1, or B2")
    system_instruction = request.get("system_instruction")
    append = appends[variant_id]
    expected_system = (
        COMMON_BASE_INSTRUCTION
        if not append
        else f"{COMMON_BASE_INSTRUCTION}\n\n{append}"
    )
    if system_instruction != expected_system:
        raise ValueError("formal renderer requires the exact reviewed variant instruction")
    pre_context = packet.get("pre_context")
    user_message = packet.get("user_message")
    if not isinstance(pre_context, str) or not isinstance(user_message, str):
        raise ValueError("formal renderer packet fields must be strings")
    return {
        "messages": [
            {"role": "system", "content": system_instruction},
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
    variants_path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "experiments"
        / CHINESE_VARIANTS_FILE
    )
    content = (
        json.dumps(RENDERER_SPEC, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
        + inspect.getsource(render_generator_request)
    ).encode("utf-8") + b"\n" + variants_path.read_bytes()
    return hashlib.sha256(content).hexdigest()


def _load_proposal(repo_root: Path) -> tuple[dict[str, Any], str]:
    path = repo_root / "docs" / "experiments" / PROPOSAL_FILE
    raw = path.read_bytes()
    proposal = json.loads(raw)
    if not isinstance(proposal, dict) or proposal.get("schema_version") != 1:
        raise ValueError("unsupported Stage 3 proposal")
    return proposal, hashlib.sha256(raw).hexdigest()


def _validate_proposal(repo_root: Path, proposal: Mapping[str, Any]) -> None:
    inputs = load_phase_b_inputs(repo_root, variants_file=CHINESE_VARIANTS_FILE)
    experiment_dir = repo_root / "docs" / "experiments"
    chinese_document = json.loads((experiment_dir / CHINESE_VARIANTS_FILE).read_bytes())
    semantic_source = chinese_document.get("semantic_source", {})
    english_path = experiment_dir / "assurance-v2-phase-b-variants.json"
    english_sha256 = hashlib.sha256(english_path.read_bytes()).hexdigest()
    if semantic_source != {
        "path": "docs/experiments/assurance-v2-phase-b-variants.json",
        "language": "en",
        "sha256": english_sha256,
    }:
        raise ValueError("Chinese variant semantic-source provenance is stale")
    case_ids = proposal.get("case_ids")
    variant_ids = proposal.get("variant_ids")
    orders = proposal.get("variant_order_by_repetition")
    if case_ids != list(CASE_IDS):
        raise ValueError("Stage 3 proposal differs from the reviewed case subset")
    if variant_ids != ["B0", "B1", "B2"]:
        raise ValueError("Stage 3 proposal must compare exactly B0/B1/B2")
    if orders != [list(order) for order in VARIANT_ORDERS]:
        raise ValueError("Stage 3 proposal must use the reviewed counterbalanced order")
    b0 = inputs.variants["B0"]["instruction_append"]
    b1 = inputs.variants["B1"]["instruction_append"]
    b2 = inputs.variants["B2"]["instruction_append"]
    semantic_frame = chinese_document.get("b2_semantic_frame_append")
    if b0 != "" or not b1 or not semantic_frame or b2 != f"{b1}\n\n{semantic_frame}":
        raise ValueError("Chinese B0/B1/B2 composition invariant failed")
    if proposal.get("run_mode") != RUN_MODE or proposal.get("evidence_use") != EVIDENCE_USE:
        raise ValueError("Stage 3 evidence identity differs from the reviewed proposal")
    if proposal.get("status") != "revised_after_cloud_review_pending_human_approvals":
        raise ValueError("Stage 3 proposal review status is unexpected")
    if proposal.get("execution_enabled") is not False:
        raise ValueError("Stage 3 execution must remain disabled during preparation")
    if proposal.get("variants_file") != CHINESE_VARIANTS_FILE or proposal.get("repetitions") != 3:
        raise ValueError("Stage 3 source or repetition count differs from the reviewed proposal")
    renderer = proposal.get("renderer")
    if renderer != {
        "id": RENDERER_ID,
        "sha256": renderer_source_sha256(),
        "base_language": "zh-CN",
        "case_packet_language": "zh-CN",
        "variant_condition_language": "zh-CN",
    }:
        raise ValueError("Stage 3 renderer identity or language metadata differs")
    if proposal.get("generator_model") != {
        "configured_model": "deepseek-v4-flash",
        "declared_snapshot": None,
        "thinking": {"type": "enabled"},
        "reasoning_effort": "not_sent_provider_support_unverified",
        "temperature": "not_sent_effect_under_thinking_unverified",
        "top_p": "not_sent_effect_under_thinking_unverified",
        "max_tokens": 4096,
        "output_budget_status": "provisional_pending_compatibility_smoke_and_human_cost_limit",
        "stream": False,
        "max_retries": 0,
    }:
        raise ValueError("Stage 3 generator settings differ from the reviewed proposal")
    expected_sources: dict[str, dict[str, str]] = {}
    for name, filename in (
        ("generation", "assurance-v2-phase-b-generation.json"),
        ("variants", CHINESE_VARIANTS_FILE),
        ("rubrics", "assurance-v2-phase-b-rubrics.json"),
    ):
        path = experiment_dir / filename
        expected_sources[name] = {
            "path": f"docs/experiments/{filename}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    if proposal.get("source_files") != expected_sources:
        raise ValueError("Stage 3 source-file provenance is stale")
    cloud_review_path = experiment_dir / "assurance-v2-stage3-cloud-review.md"
    if proposal.get("cloud_review") != {
        "reviewed_commit": "76207b58d7f79aee3d73416223657d44a32cd11e",
        "path": "docs/experiments/assurance-v2-stage3-cloud-review.md",
        "sha256": hashlib.sha256(cloud_review_path.read_bytes()).hexdigest(),
    }:
        raise ValueError("Stage 3 cloud-review provenance is stale")
    expected_review_sources: dict[str, dict[str, str]] = {}
    for name, filename in (
        ("grader_capability", "assurance-v2-stage3-grader-capability.md"),
        ("thinking_compatibility_smoke", "assurance-v2-thinking-compatibility-smoke.json"),
    ):
        path = experiment_dir / filename
        expected_review_sources[name] = {
            "path": f"docs/experiments/{filename}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    if proposal.get("review_sources") != expected_review_sources:
        raise ValueError("Stage 3 review-source provenance is stale")
    expected_call_count = len(CASE_IDS) * 3 * 3
    if proposal.get("estimated_calls") != {
        "generator": expected_call_count,
        "grader": expected_call_count,
        "maximum_total_without_retries": expected_call_count * 2,
    }:
        raise ValueError("Stage 3 estimated call count differs from the frozen design")
    if proposal.get("grader") != {
        "renderer_id": "phase-b-formal-grader-zh-cn-v1-candidate",
        "language": "zh-CN",
        "required_context_mode": "standalone",
        "preferred_independence": "Level 2 candidate using a distinct model family",
        "fallback_independence": "Level 1 using the generator model family in an isolated call",
        "capability_statement": "docs/experiments/assurance-v2-stage3-grader-capability.md",
        "visible_reasoning_is_evidence": False,
        "max_tokens": 1024,
        "stream": False,
    }:
        raise ValueError("Stage 3 grader proposal differs from the reviewed candidate")
    interpretation = proposal.get("directional_interpretation")
    if not isinstance(interpretation, dict) or any(
        (
            interpretation.get("not_a_total_score") is not True,
            interpretation.get("not_a_statistical_significance_claim") is not True,
            interpretation.get("case_majority_rule")
            != "at_least_2_of_3_repetitions_same_direction",
            len(interpretation.get("b1_vs_b0_directional_value", [])) != 3,
            len(interpretation.get("b2_vs_b1_incremental_value", [])) != 3,
            len(interpretation.get("stop_rules", [])) != 4,
            len(interpretation.get("mechanical_rules_pending_human_freeze", [])) != 7,
        )
    ):
        raise ValueError("Stage 3 directional interpretation is incomplete")
    if proposal.get("required_call_metadata") != [
        "elapsed_ms_per_attempt",
        "numeric_reasoning_tokens_when_returned",
        "never_reasoning_content",
    ]:
        raise ValueError("Stage 3 required call metadata differs")
    tranches = proposal.get("operational_tranches")
    if not isinstance(tranches, dict) or any(
        (
            tranches.get("performance_driven_redesign_between_tranches_forbidden") is not True,
            len(tranches.get("allowed_pause_reasons", [])) != 6,
        )
    ):
        raise ValueError("Stage 3 operational tranche rules are incomplete")


def preflight_formal_replay(
    *,
    repo_root: Path,
    config_path: Path,
    output_root: Path,
    confirm_formal_run: bool,
) -> tuple[int, dict[str, Any]]:
    config, _ = load_only_local_provider_config_and_scan_values(
        config_path, repository_root=repo_root
    )
    revision = _clean_git_revision(repo_root)
    resolved_output_root = _validate_output_root(output_root, repo_root)
    if not resolved_output_root.is_dir():
        raise ValueError("formal output root must already exist as a private directory")
    if stat.S_IMODE(resolved_output_root.stat().st_mode) & 0o077:
        raise PermissionError("formal output root must not be accessible by group or other users")
    proposal, proposal_sha256 = _load_proposal(repo_root)
    _validate_proposal(repo_root, proposal)
    expected_model = proposal["generator_model"]["configured_model"]
    if config.configured_model != expected_model:
        raise ValueError("local configured model differs from the Stage 3 proposal")
    report = {
        "preflight": "passed",
        "run_mode": RUN_MODE,
        "evidence_use": EVIDENCE_USE,
        "network_call_count": 0,
        "generator_call_count": 0,
        "grader_call_count": 0,
        "configured_model": config.configured_model,
        "declared_model_snapshot_status": (
            "known" if config.declared_model_snapshot is not None else "unknown"
        ),
        "renderer_id": RENDERER_ID,
        "renderer_sha256": renderer_source_sha256(),
        "proposal_sha256": proposal_sha256,
        "output_root": str(resolved_output_root),
        "git_revision": revision,
        "working_tree_clean": True,
    }
    if not confirm_formal_run:
        return 2, {**report, "formal_confirmation": "missing; no call made"}
    if proposal.get("execution_enabled") is not True:
        return 3, {
            **report,
            "formal_confirmation": "present",
            "execution": "blocked_pending_human_cloud_review; no call made",
        }
    raise RuntimeError("real formal provider wiring is intentionally not implemented")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the frozen Stage 3 proposal without model calls."
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--confirm-formal-run", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    code, report = preflight_formal_replay(
        repo_root=Path(__file__).resolve().parents[2],
        config_path=args.config,
        output_root=args.output_dir,
        confirm_formal_run=args.confirm_formal_run,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
