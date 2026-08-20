"""Secret-safe OpenAI-compatible Chat Completions transport plumbing."""

from __future__ import annotations

import json
import re
import socket
from collections.abc import Callable, Mapping
from copy import deepcopy
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .local_config import LocalProviderConfig
from .models import ProviderDescriptor, ProviderResponse
from .providers import ProviderError


Transport = Callable[[str, Mapping[str, str], bytes, float], bytes]
RequestRenderer = Callable[[Mapping[str, Any]], Mapping[str, Any]]

_MODEL_REQUEST_FIELDS = {
    "messages",
    "temperature",
    "top_p",
    "max_tokens",
    "response_format",
    "thinking",
    "reasoning_effort",
    "stream",
}


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def _chat_completions_url(base_url: str) -> str:
    if base_url.endswith("/v1/chat/completions"):
        return base_url
    if base_url.endswith("/v1"):
        return f"{base_url}/chat/completions"
    return f"{base_url}/v1/chat/completions"


def urllib_transport(url: str, headers: Mapping[str, str], body: bytes, timeout: float) -> bytes:
    request = Request(url, data=body, headers=dict(headers), method="POST")
    opener = build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as error:
        retryable = error.code == 429 or 500 <= error.code <= 599
        raise ProviderError(f"provider HTTP status {error.code}", retryable=retryable) from None
    except (URLError, TimeoutError, socket.timeout):
        raise ProviderError("provider transport failure", retryable=True) from None


class DeepSeekChatCompletionsProvider:
    """Narrow stateless Chat Completions dialect for a DeepSeek-family model route."""

    def __init__(
        self,
        config: LocalProviderConfig,
        *,
        request_renderer: RequestRenderer,
        renderer_id: str,
        renderer_sha256: str,
        timeout_seconds: float = 30.0,
        transport: Transport = urllib_transport,
        allow_thinking: bool = False,
        provider_boundary: str | None = None,
        model_family: str | None = None,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not renderer_id.strip():
            raise ValueError("renderer_id must be non-empty")
        if not re.fullmatch(r"[0-9a-f]{64}", renderer_sha256):
            raise ValueError("renderer_sha256 must be a lowercase SHA-256 digest")
        for field_name, value in (
            ("provider_boundary", provider_boundary),
            ("model_family", model_family),
        ):
            if value is not None and not value.strip():
                raise ValueError(f"{field_name} must be non-empty when provided")
        self._config = config
        self._timeout_seconds = timeout_seconds
        self._transport = transport
        self._request_renderer = request_renderer
        self._allow_thinking = allow_thinking
        self._private_response_identifiers: tuple[str, ...] = ()
        public_parameters = {
            "api_style": config.api_style,
            "renderer_id": renderer_id,
            "renderer_sha256": renderer_sha256,
            "thinking_enabled_allowed": allow_thinking,
            "reasoning_content_retention": "not_recorded",
        }
        if provider_boundary is not None:
            public_parameters["provider_boundary"] = provider_boundary
        if model_family is not None:
            public_parameters["model_family"] = model_family
        self._descriptor = ProviderDescriptor(
            provider=config.provider,
            configured_model=config.configured_model,
            declared_model_snapshot=config.declared_model_snapshot,
            context_mode="standalone",
            public_parameters=public_parameters,
            uncontrolled_parameters=(
                "backend_identity",
                "backend_seed",
                "custom_provider_routing",
                "server_side_model_alias_resolution",
                "provider_retention",
            ),
        )

    @property
    def descriptor(self) -> ProviderDescriptor:
        return self._descriptor

    def invoke_standalone(self, request: Mapping[str, Any]) -> ProviderResponse:
        model_request = self._request_renderer(deepcopy(dict(request)))
        if not isinstance(model_request, Mapping):
            raise ValueError("request requires a model_visible_request mapping")
        unknown = sorted(set(model_request) - _MODEL_REQUEST_FIELDS)
        if unknown:
            raise ValueError(f"unsupported model request fields: {unknown}")
        messages = model_request.get("messages")
        if not isinstance(messages, list) or not messages:
            raise ValueError("model_visible_request requires a non-empty messages list")
        if model_request.get("stream") not in (None, False):
            raise ValueError("streaming is not supported by the evidence recorder")
        thinking_disabled = model_request.get("thinking") == {"type": "disabled"}
        thinking_enabled = model_request.get("thinking") == {"type": "enabled"}
        reasoning_disabled = model_request.get("reasoning_effort") == "none"
        if thinking_enabled and not self._allow_thinking:
            raise ValueError("thinking is not approved for this provider invocation")
        if not (thinking_disabled or reasoning_disabled or thinking_enabled):
            raise ValueError(
                "renderer must explicitly select an approved thinking mode"
            )

        effective_request = {"model": self._config.configured_model, **dict(model_request)}
        body = json.dumps(
            effective_request, ensure_ascii=False, allow_nan=False, separators=(",", ":")
        ).encode("utf-8")
        response_bytes = self._transport(
            _chat_completions_url(self._config.base_url),
            {
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
            },
            body,
            self._timeout_seconds,
        )
        try:
            response = json.loads(response_bytes)
            response_id = response.get("id")
            if isinstance(response_id, str) and response_id:
                self._private_response_identifiers = tuple(
                    dict.fromkeys((*self._private_response_identifiers, response_id))
                )
            choice = response["choices"][0]
            message = choice["message"]
            content = message["content"]
            reasoning_content = message.get("reasoning_content")
            if isinstance(reasoning_content, str) and reasoning_content:
                self._private_response_identifiers = tuple(
                    dict.fromkeys((*self._private_response_identifiers, reasoning_content))
                )
            reported_model = response["model"]
            if not isinstance(content, str) or not isinstance(reported_model, str):
                raise TypeError
        except (json.JSONDecodeError, KeyError, IndexError, TypeError):
            raise ProviderError("provider returned an invalid chat completion", retryable=False) from None

        usage = response.get("usage")
        finish_reason = choice.get("finish_reason")
        allowed_finish_reasons = {"stop", "length", "tool_calls", "content_filter"}
        public_metadata: dict[str, Any] = {
            "finish_reason": (
                finish_reason if finish_reason in allowed_finish_reasons else "other"
            )
        }
        if isinstance(usage, dict):
            public_metadata["usage"] = {
                key: usage[key]
                for key in ("prompt_tokens", "completion_tokens", "total_tokens")
                if isinstance(usage.get(key), int)
                and not isinstance(usage.get(key), bool)
                and usage[key] >= 0
            }
            completion_details = usage.get("completion_tokens_details")
            if isinstance(completion_details, dict):
                reasoning_tokens = completion_details.get("reasoning_tokens")
                if (
                    isinstance(reasoning_tokens, int)
                    and not isinstance(reasoning_tokens, bool)
                    and reasoning_tokens >= 0
                ):
                    public_metadata["usage"]["completion_tokens_details"] = {
                        "reasoning_tokens": reasoning_tokens
                    }
        return ProviderResponse(
            raw_output=content,
            provider_reported_model=reported_model,
            model_visible_request=effective_request,
            public_metadata=public_metadata,
        )

    def private_artifact_scan_values(self) -> tuple[str, ...]:
        """Return provider correlation IDs for local scan without artifact storage."""
        return self._private_response_identifiers
