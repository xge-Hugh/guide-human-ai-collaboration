"""Canonical no-network renderer for the different-family direct API grader."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping


RENDERER_ID = "phase-b-direct-grader-zh-cn-v1-candidate"
MODEL_FAMILY = "Qwen"
CONFIGURED_MODEL = "qwen3.7-max"
SYSTEM_INSTRUCTION = (
    "你是独立评分器。仅依据当前用户消息中的材料评价给定响应。"
    "逐轴判断，并只返回符合所给 JSON Schema 的一个 JSON 对象；"
    "不要输出 Markdown、代码围栏或额外文字。"
)
MODEL_SETTINGS = {
    "thinking": {"type": "disabled"},
    "max_tokens": 1024,
    "stream": False,
}
VISIBLE_PACKET_FIELDS = (
    "case_specific_normative_context",
    "hidden_semantic_acceptance_boundary",
    "generator_final_response",
    "grading_axes",
    "conditional_rule",
    "required_output_schema",
)
SECTION_LABELS = (
    ("case_specific_normative_context", "【案例规范与评分上下文】"),
    ("hidden_semantic_acceptance_boundary", "【隐藏语义验收边界】"),
    ("generator_final_response", "【生成器最终响应】"),
    ("grading_axes", "【评分轴与允许值】"),
    ("conditional_rule", "【条件规则】"),
    ("required_output_schema", "【必需 JSON 输出模式】"),
)
RENDERER_SPEC = {
    "renderer_id": RENDERER_ID,
    "language": "zh-CN",
    "system_instruction": SYSTEM_INSTRUCTION,
    "visible_packet_fields": VISIBLE_PACKET_FIELDS,
    "section_labels": SECTION_LABELS,
    "model_settings": MODEL_SETTINGS,
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))


def render_grader_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Render only the reviewed fields of one self-contained grader packet."""
    missing = [field for field in VISIBLE_PACKET_FIELDS if field not in packet]
    if missing:
        raise ValueError(f"grader packet is missing required fields: {missing}")
    response = packet["generator_final_response"]
    if not isinstance(response, str):
        raise ValueError("generator_final_response must be a string")
    sections: list[str] = []
    for field, label in SECTION_LABELS:
        value = packet[field]
        rendered = value if isinstance(value, str) else _canonical_json(value)
        sections.append(f"{label}\n{rendered}")
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": "\n\n".join(sections)},
        ],
        **deepcopy(MODEL_SETTINGS),
    }


def renderer_content_sha256() -> str:
    return hashlib.sha256(_canonical_json(RENDERER_SPEC).encode("utf-8")).hexdigest()
