"""Small immutable records shared across the assurance harness."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol


@dataclass(frozen=True)
class ModelAssignment:
    provider: str
    model: str
    family: str
    declared_snapshot: str | None
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderCredentials:
    api_style: str
    base_url: str = field(repr=False)
    api_key: str = field(repr=False)


@dataclass(frozen=True)
class ResolvedProvider:
    assignment: ModelAssignment
    credentials: ProviderCredentials = field(repr=False)


@dataclass(frozen=True)
class ProviderResponse:
    raw_output: str
    provider_reported_model: str
    model_visible_request: Mapping[str, Any]
    public_metadata: Mapping[str, Any] = field(default_factory=dict)


class ProviderError(Exception):
    """A sanitized provider failure that is safe to persist."""

    def __init__(self, public_message: str) -> None:
        super().__init__(public_message)
        self.public_message = public_message


class Provider(Protocol):
    assignment: ModelAssignment

    def invoke_standalone(self, request: Mapping[str, Any]) -> ProviderResponse:
        """Invoke exactly one fresh, standalone request."""


Transport = Callable[[str, Mapping[str, str], bytes, float], bytes]
