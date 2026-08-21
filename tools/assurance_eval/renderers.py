"""Reviewed semantic-request to model-request renderers."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Mapping

from .experiment import canonical_json, sha256_bytes


GENERATOR_ID = "phase-b-formal-generator-zh-cn-v1"
GRADER_ID = "phase-b-direct-grader-zh-cn-v1-candidate"
GRADER_SYSTEM_INSTRUCTION = (
    "你是独立评分器。仅依据当前用户消息中的材料评价给定响应。"
    "逐轴判断，并只返回符合所给 JSON Schema 的一个 JSON 对象；"
    "不要输出 Markdown、代码围栏或额外文字。"
)
_USER_TEMPLATE = "【前置上下文】\n<packet.pre_context>\n\n【用户当前消息】\n<packet.user_message>"
_GRADER_FIELDS = (
    "case_specific_normative_context", "hidden_semantic_acceptance_boundary",
    "generator_final_response", "grading_axes", "conditional_rule", "required_output_schema",
)
_GRADER_LABELS = (
    ("case_specific_normative_context", "【案例规范与评分上下文】"),
    ("hidden_semantic_acceptance_boundary", "【隐藏语义验收边界】"),
    ("generator_final_response", "【生成器最终响应】"),
    ("grading_axes", "【评分轴与允许值】"),
    ("conditional_rule", "【条件规则】"),
    ("required_output_schema", "【必需 JSON 输出模式】"),
)
_SPECS = {
    GENERATOR_ID: {
        "renderer_id": GENERATOR_ID,
        "language": "zh-CN",
        "user_template": _USER_TEMPLATE,
        "system_instruction_source": "recipe.instructions.generator_base plus selected variant append",
        "parameters_source": "resolved role assignment",
    },
    GRADER_ID: {
        "renderer_id": GRADER_ID,
        "language": "zh-CN",
        "system_instruction": GRADER_SYSTEM_INSTRUCTION,
        "visible_packet_fields": _GRADER_FIELDS,
        "section_labels": _GRADER_LABELS,
        "parameters_source": "resolved role assignment",
    },
}
_PARAMETER_FIELDS = {
    "temperature", "top_p", "max_tokens", "response_format", "thinking",
    "reasoning_effort", "stream",
}


def validate_parameters(parameters: object, role: str) -> None:
    if not isinstance(parameters, Mapping):
        raise ValueError(f"{role} parameters must be an object")
    unknown = sorted(set(parameters) - _PARAMETER_FIELDS)
    if unknown:
        raise ValueError(f"{role} parameters contain renderer-owned or unsupported fields: {unknown}")


def renderer_identity(renderer_id: str) -> dict[str, str]:
    if renderer_id not in _SPECS:
        raise ValueError(f"unknown renderer {renderer_id!r}")
    content = canonical_json(_SPECS[renderer_id]) + b"\0" + Path(__file__).read_bytes()
    return {"id": renderer_id, "sha256": sha256_bytes(content)}


def render_generator(request: Mapping[str, Any], parameters: Mapping[str, Any]) -> dict[str, Any]:
    validate_parameters(parameters, "generator")
    packet = request.get("packet")
    if request.get("call_kind") != "generator" or not isinstance(packet, Mapping):
        raise ValueError("generator renderer requires a generator packet")
    if set(packet) != {"case_id", "pre_context", "user_message"}:
        raise ValueError("generator packet fields differ from the rubric-free contract")
    system = request.get("system_instruction")
    pre_context = packet.get("pre_context")
    user_message = packet.get("user_message")
    if not all(isinstance(value, str) for value in (system, pre_context, user_message)):
        raise ValueError("generator renderer fields must be strings")
    return {
        **deepcopy(dict(parameters)),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"【前置上下文】\n{pre_context}\n\n【用户当前消息】\n{user_message}"},
        ],
    }


def render_grader(request: Mapping[str, Any], parameters: Mapping[str, Any]) -> dict[str, Any]:
    validate_parameters(parameters, "grader")
    packet = request.get("packet")
    if request.get("call_kind") != "grader" or not isinstance(packet, Mapping):
        raise ValueError("grader renderer requires a standalone grader packet")
    missing = [field for field in _GRADER_FIELDS if field not in packet]
    if missing:
        raise ValueError(f"grader packet is missing required fields: {missing}")
    if not isinstance(packet["generator_final_response"], str):
        raise ValueError("generator_final_response must be a string")
    sections = []
    for field, label in _GRADER_LABELS:
        value = packet[field]
        rendered = value if isinstance(value, str) else canonical_json(value).decode("utf-8")
        sections.append(f"{label}\n{rendered}")
    return {
        **deepcopy(dict(parameters)),
        "messages": [
            {"role": "system", "content": GRADER_SYSTEM_INSTRUCTION},
            {"role": "user", "content": "\n\n".join(sections)},
        ],
    }


def get_renderer(renderer_id: str) -> Callable[[Mapping[str, Any], Mapping[str, Any]], dict[str, Any]]:
    try:
        return {GENERATOR_ID: render_generator, GRADER_ID: render_grader}[renderer_id]
    except KeyError:
        raise ValueError(f"unknown renderer {renderer_id!r}") from None
