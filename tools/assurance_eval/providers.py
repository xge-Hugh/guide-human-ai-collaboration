"""Provider boundary and a no-network scripted fake."""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any, Callable, Mapping, Protocol, Sequence

from .models import ProviderDescriptor, ProviderResponse


class Provider(Protocol):
    @property
    def descriptor(self) -> ProviderDescriptor: ...

    def invoke_standalone(self, request: Mapping[str, Any]) -> ProviderResponse:
        """Invoke with no conversation, session, or state retained from another call."""
        ...


class ProviderError(Exception):
    """A sanitized provider failure safe to persist in experiment artifacts."""

    def __init__(self, public_message: str, *, retryable: bool = False) -> None:
        super().__init__(public_message)
        self.public_message = public_message
        self.retryable = retryable


FakeStep = ProviderResponse | Exception | Callable[[Mapping[str, Any]], ProviderResponse]


class ScriptedFakeProvider:
    """Return scripted responses while retaining exactly what the runner sent."""

    def __init__(self, descriptor: ProviderDescriptor, steps: Sequence[FakeStep]) -> None:
        if not steps:
            raise ValueError("fake provider requires at least one scripted step")
        self._descriptor = descriptor
        self._steps = deque(steps)
        self.calls: list[dict[str, Any]] = []

    @property
    def descriptor(self) -> ProviderDescriptor:
        return self._descriptor

    def invoke_standalone(self, request: Mapping[str, Any]) -> ProviderResponse:
        self.calls.append(deepcopy(dict(request)))
        if not self._steps:
            raise RuntimeError("fake provider script exhausted")
        step = self._steps.popleft()
        if isinstance(step, Exception):
            raise step
        if callable(step):
            return step(request)
        return step
