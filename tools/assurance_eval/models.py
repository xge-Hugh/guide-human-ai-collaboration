"""Data records shared by the Phase B runner and provider adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


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

    def validate(self) -> None:
        if self.run_mode != "fake_pipeline":
            raise ValueError("Stage 1 supports only run_mode='fake_pipeline'")
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
            if self.variant_condition_language != "en":
                raise ValueError(
                    "the checked-in B1/B2 rendering is English; a different language "
                    "requires a separately reviewed variant source"
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
