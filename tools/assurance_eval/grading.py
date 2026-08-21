"""Standalone grader packet construction and strict Phase B grade validation."""

from __future__ import annotations

import json
from typing import Any, Mapping


AXES = (
    "applicability", "applicability_basis", "timing", "satisfaction",
    "human_compensation_needed", "over_trigger_cost", "notes",
)


def validate_grading_contract(grading: Mapping[str, Any]) -> None:
    axes = grading.get("axes")
    schema = grading.get("output_schema")
    if not isinstance(grading.get("policy_id"), str) or not grading["policy_id"].strip():
        raise ValueError("grading.policy_id must be non-empty")
    if not isinstance(grading.get("conditional_rule"), str) or not grading["conditional_rule"].strip():
        raise ValueError("grading.conditional_rule must be non-empty")
    if not isinstance(axes, dict) or set(axes) != set(AXES):
        raise ValueError("grading axes differ from the Phase B contract")
    if not isinstance(schema, dict) or schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise ValueError("grading output schema must be a closed object")
    if set(schema.get("required", ())) != set(AXES):
        raise ValueError("grading output schema required fields differ")
    properties = schema.get("properties")
    if not isinstance(properties, dict) or set(properties) != set(AXES):
        raise ValueError("grading output schema properties differ")
    for axis in ("applicability", "timing", "satisfaction", "human_compensation_needed", "over_trigger_cost"):
        if not isinstance(axes[axis], list) or properties[axis].get("enum") != axes[axis]:
            raise ValueError(f"grading schema enum differs for {axis}")
    if properties["applicability_basis"] != {"type": "string", "minLength": 1} or properties["notes"] != {"type": "string"}:
        raise ValueError("grading string schema differs")
    expected_conditional = [
        {
            "if": {"properties": {"applicability": {"const": "not_applicable"}}},
            "then": {"properties": {"timing": {"const": "not_applicable"}, "satisfaction": {"const": "not_applicable"}}},
            "else": {"properties": {"timing": {"not": {"const": "not_applicable"}}, "satisfaction": {"not": {"const": "not_applicable"}}}},
        }
    ]
    if schema.get("allOf") != expected_conditional:
        raise ValueError("grading N/A schema differs from the enforced policy")


def build_grader_packet(
    *, case_id: str, rubric: Mapping[str, Any], generator_output: str, grading: Mapping[str, Any]
) -> dict[str, Any]:
    """Build a self-contained packet; no generator context or hidden reasoning is inherited."""
    return {
        "case_specific_normative_context": {
            "reference_case": rubric["reference_case"],
            "expected_applicability": rubric["expected_applicability"],
            "adjudication": rubric["adjudication"],
        },
        "hidden_semantic_acceptance_boundary": {
            "required_protection": rubric["required_protection"],
            "latest_useful_point": rubric["latest_useful_point"],
        },
        "generator_final_response": generator_output,
        "grading_axes": grading["axes"],
        "conditional_rule": grading["conditional_rule"],
        "required_output_schema": grading["output_schema"],
    }


def parse_grade(raw_output: str, grading: Mapping[str, Any]) -> dict[str, str]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r}")
            value[key] = child
        return value

    value = json.loads(raw_output, object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict) or set(value) != set(AXES):
        missing = sorted(set(AXES) - set(value) if isinstance(value, dict) else set(AXES))
        extra = sorted(set(value) - set(AXES)) if isinstance(value, dict) else []
        raise ValueError(f"grader axes differ: missing={missing}, extra={extra}")
    if not all(isinstance(value[axis], str) for axis in AXES):
        raise ValueError("every grader axis must contain a string")
    if not value["applicability_basis"].strip():
        raise ValueError("applicability_basis must be non-empty")
    axes = grading["axes"]
    for axis in ("applicability", "timing", "satisfaction", "human_compensation_needed", "over_trigger_cost"):
        allowed = axes.get(axis)
        if not isinstance(allowed, list) or value[axis] not in allowed:
            raise ValueError(f"invalid {axis}: {value[axis]!r}")
    is_na = value["applicability"] == "not_applicable"
    if (value["timing"] == "not_applicable") != is_na or (value["satisfaction"] == "not_applicable") != is_na:
        raise ValueError("timing and satisfaction must be not_applicable exactly when applicability is not_applicable")
    return {axis: value[axis] for axis in AXES}
