"""Bounded retry classification and logical-call invocation."""

from __future__ import annotations

import time
from typing import Any, Callable, Mapping

from .models import Provider, ProviderError


DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_BACKOFF_SECONDS = (1.0, 2.0)


def classify_retryability(error: Mapping[str, Any] | None) -> str:
    """Return 'retryable' or 'not_retryable' for a sanitized provider error."""
    if error is None:
        return "not_retryable"
    error_type = error.get("type", "")
    message = str(error.get("message", ""))
    if error_type == "PrivateValueBlocked" or "private value" in message:
        return "not_retryable"
    if "provenance" in message or "configuration" in message:
        return "not_retryable"
    if "invalid chat completion" in message or "invalid model-visible" in message:
        return "not_retryable"
    if "network authorization" in message or "budget exhausted" in message:
        return "not_retryable"
    if message == "provider transport failure":
        return "retryable"
    if message.startswith("provider HTTP status "):
        try:
            code = int(message.rsplit(" ", 1)[-1])
        except ValueError:
            return "not_retryable"
        if code == 429 or 500 <= code < 600:
            return "retryable"
        return "not_retryable"
    if error_type in {"ProviderError", "URLError", "TimeoutError", "socket.timeout"}:
        if "transport" in message or "timeout" in message.lower():
            return "retryable"
    return "not_retryable"


def _provider_identity(provider: Provider) -> dict[str, Any]:
    assignment = provider.assignment
    return {
        "provider": assignment.provider,
        "configured_model": assignment.model,
        "model_family": assignment.family,
        "declared_model_snapshot": assignment.declared_snapshot,
        "parameters": dict(assignment.parameters),
        "context_mode": "standalone",
    }


def _single_attempt(
    provider: Provider, request: Mapping[str, Any], *, now: Callable[[], str]
) -> dict[str, Any]:
    requested_at = now()
    started = time.monotonic()
    try:
        response = provider.invoke_standalone(request)
    except Exception as error:
        message = (
            str(error)
            if isinstance(error, (ProviderError, ValueError))
            else "unexpected provider invocation failure"
        )
        return {
            "invocation_status": "failed",
            "requested_at": requested_at,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
            "request": dict(request),
            "model_visible_request": getattr(provider, "last_model_visible_request", None),
            "provider": _provider_identity(provider),
            "provider_reported_model": None,
            "raw_output": None,
            "error": {"type": type(error).__name__, "message": message},
        }
    return {
        "invocation_status": "succeeded",
        "requested_at": requested_at,
        "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
        "request": dict(request),
        "model_visible_request": dict(response.model_visible_request),
        "provider": _provider_identity(provider),
        "provider_reported_model": response.provider_reported_model,
        "model_identity": {
            "configured_model": provider.assignment.model,
            "declared_model_snapshot": provider.assignment.declared_snapshot,
            "provider_reported_model": response.provider_reported_model,
        },
        "raw_output": response.raw_output,
        "public_response_metadata": dict(response.public_metadata),
        "error": None,
    }


def invoke_logical_call(
    provider: Provider,
    request: Mapping[str, Any],
    *,
    now: Callable[[], str],
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Execute one logical model call with bounded retry; return summary and attempts."""
    attempts: list[dict[str, Any]] = []
    logical_started = time.monotonic()
    first_requested_at = now()
    successful_attempt: int | None = None
    successful_attempt_elapsed_ms: float | None = None

    for attempt_number in range(1, max_attempts + 1):
        attempt = _single_attempt(provider, request, now=now)
        attempt["attempt_number"] = attempt_number
        attempt["retryability"] = (
            "not_applicable"
            if attempt["invocation_status"] == "succeeded"
            else classify_retryability(attempt.get("error"))
        )
        attempts.append(attempt)
        if attempt["invocation_status"] == "succeeded":
            successful_attempt = attempt_number
            successful_attempt_elapsed_ms = attempt["elapsed_ms"]
            break
        if attempt["retryability"] != "retryable" or attempt_number >= max_attempts:
            break
        delay = backoff_seconds[min(attempt_number - 1, len(backoff_seconds) - 1)]
        sleep(delay)

    retry_count = len(attempts) - 1
    final_status = "succeeded" if successful_attempt is not None else (
        "failed_retryable" if attempts and attempts[-1]["retryability"] == "retryable" else "failed_integrity"
    )
    final = attempts[-1]
    logical_call: dict[str, Any] = {
        "invocation_status": "succeeded" if successful_attempt is not None else "failed",
        "requested_at": first_requested_at,
        "elapsed_ms": round((time.monotonic() - logical_started) * 1000, 3),
        "successful_attempt_elapsed_ms": successful_attempt_elapsed_ms,
        "request": final["request"],
        "model_visible_request": final.get("model_visible_request"),
        "provider": final["provider"],
        "provider_reported_model": final.get("provider_reported_model"),
        "raw_output": final.get("raw_output"),
        "attempt_count": len(attempts),
        "retry_count": retry_count,
        "final_status": final_status,
        "successful_attempt": successful_attempt,
        "attempt_evidence_paths": [],
        "error": None if successful_attempt is not None else final.get("error"),
    }
    if successful_attempt is not None:
        logical_call["model_identity"] = final.get("model_identity")
        logical_call["public_response_metadata"] = final.get("public_response_metadata")
    return logical_call, attempts
