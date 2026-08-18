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
    public_parameters: Mapping[str, Any] = field(default_factory=dict)
    uncontrolled_parameters: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProviderResponse:
    raw_output: str
    actual_model: str
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
    repetitions: int = 3
    max_retries: int = 0

    def validate(self) -> None:
        if self.run_mode != "fake_pipeline":
            raise ValueError("Stage 1 supports only run_mode='fake_pipeline'")
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
