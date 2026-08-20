"""Data records shared by the Phase B runner and provider adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .loading import DEFAULT_VARIANTS_FILE


EVIDENCE_LABELS = {
    "fake_pipeline": "not_experimental_evidence",
    "transport_smoke": "transport_validation_only_not_phase_b_effect_evidence",
    "thinking_compatibility_smoke": (
        "thinking_compatibility_only_not_phase_b_effect_evidence"
    ),
}

CHINESE_VARIANTS_FILE = "assurance-v2-phase-b-variants.zh-CN.json"


@dataclass(frozen=True)
class ProviderDescriptor:
    provider: str
    configured_model: str
    context_mode: str
    declared_model_snapshot: str | None = None
    public_parameters: Mapping[str, Any] = field(default_factory=dict)
    uncontrolled_parameters: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProviderResponse:
    raw_output: str
    provider_reported_model: str
    model_visible_request: Mapping[str, Any] | None = None
    public_metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RunConfig:
    output_root: Path
    base_generator_instruction: str
    grader_instruction: str
    grader_normative_context: str
    case_ids: tuple[str, ...]
    variant_ids: tuple[str, ...]
    run_mode: str
    generator_base_language: str
    case_packet_language: str
    variant_condition_language: str
    grader_instruction_language: str
    grader_context_language: str
    repetitions: int = 3
    max_retries: int = 0
    variants_file: str = DEFAULT_VARIANTS_FILE
    variant_order_by_repetition: tuple[tuple[str, ...], ...] | None = None

    def validate(self) -> None:
        if self.run_mode not in EVIDENCE_LABELS:
            raise ValueError(f"unsupported run_mode {self.run_mode!r}")
        language_fields = {
            "generator_base_language": self.generator_base_language,
            "case_packet_language": self.case_packet_language,
            "variant_condition_language": self.variant_condition_language,
            "grader_instruction_language": self.grader_instruction_language,
            "grader_context_language": self.grader_context_language,
        }
        for field_name, value in language_fields.items():
            if not value.strip():
                raise ValueError(f"{field_name} must be explicit and non-empty")
        if self.case_packet_language != "zh-CN":
            raise ValueError("the checked-in Phase B case packets are Chinese")
        if any(variant_id != "B0" for variant_id in self.variant_ids):
            expected_variant_language = {
                DEFAULT_VARIANTS_FILE: "en",
                CHINESE_VARIANTS_FILE: "zh-CN",
            }.get(self.variants_file)
            if expected_variant_language is None:
                raise ValueError("variant source language is not recognized")
            if self.variant_condition_language != expected_variant_language:
                raise ValueError(
                    "variant_condition_language does not match the selected variant source"
                )
        elif self.variant_condition_language != "none":
            raise ValueError("B0-only runs must record variant_condition_language='none'")
        if not self.base_generator_instruction.strip():
            raise ValueError("base_generator_instruction must be explicit and non-empty")
        if not self.grader_instruction.strip():
            raise ValueError("grader_instruction must be explicit and non-empty")
        if not self.grader_normative_context.strip():
            raise ValueError("grader_normative_context must be explicit and non-empty")
        if not self.case_ids:
            raise ValueError("at least one case_id is required")
        if not self.variant_ids:
            raise ValueError("at least one variant_id is required")
        if self.repetitions < 1:
            raise ValueError("repetitions must be at least 1")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if self.variant_order_by_repetition is not None:
            if len(self.variant_order_by_repetition) != self.repetitions:
                raise ValueError("variant order must contain one row per repetition")
            expected = sorted(self.variant_ids)
            if any(sorted(order) != expected for order in self.variant_order_by_repetition):
                raise ValueError("each variant order must be a permutation of variant_ids")
        if self.run_mode == "transport_smoke":
            if self.case_ids != ("p002",) or self.variant_ids != ("B0",):
                raise ValueError("transport_smoke is fixed to p002/B0")
            if self.repetitions != 1 or self.max_retries != 0:
                raise ValueError("transport_smoke requires one repetition and zero retries")
        if self.run_mode == "thinking_compatibility_smoke":
            if self.case_ids != ("p002",) or self.variant_ids != ("B0",):
                raise ValueError("thinking_compatibility_smoke is fixed to p002/B0")
            if self.repetitions != 1 or self.max_retries != 0:
                raise ValueError(
                    "thinking_compatibility_smoke requires one repetition and zero retries"
                )

    @property
    def evidence_label(self) -> str:
        return EVIDENCE_LABELS[self.run_mode]
