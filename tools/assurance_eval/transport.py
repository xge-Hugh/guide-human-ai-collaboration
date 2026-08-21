"""Secret-safe, stateless OpenAI-compatible provider transport."""

from __future__ import annotations

import json
import socket
from collections.abc import Mapping
from copy import deepcopy
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .models import ProviderError, ProviderResponse, ResolvedProvider, Transport


Renderer = Callable[[Mapping[str, Any], Mapping[str, Any]], dict[str, Any]]
_MODEL_FIELDS = {
    "messages", "temperature", "top_p", "max_tokens", "response_format", "thinking",
    "reasoning_effort", "stream",
}


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def chat_completions_url(base_url: str) -> str:
    if base_url.endswith("/v1/chat/completions"):
        return base_url
    if base_url.endswith("/v1"):
        return f"{base_url}/chat/completions"
    return f"{base_url}/v1/chat/completions"


def urllib_transport(url: str, headers: Mapping[str, str], body: bytes, timeout: float) -> bytes:
    request = Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with build_opener(_NoRedirect).open(request, timeout=timeout) as response:
            return response.read()
    except HTTPError as error:
        raise ProviderError(f"provider HTTP status {error.code}") from None
    except (URLError, TimeoutError, socket.timeout):
        raise ProviderError("provider transport failure") from None


class OpenAIChatCompletionsProvider:
    """One selected model route; no sessions, retries, tools, or reasoning retention."""

    def __init__(
        self, resolved: ResolvedProvider, renderer: Renderer, *, transport: Transport,
        timeout_seconds: float = 60.0,
    ) -> None:
        if resolved.credentials.api_style != "openai_chat_completions":
            raise ValueError("unsupported provider API style")
        self.assignment = resolved.assignment
        self._credentials = resolved.credentials
        self._renderer = renderer
        self._transport = transport
        self._timeout_seconds = timeout_seconds
        self.private_response_values: tuple[str, ...] = ()
        self.last_model_visible_request: Mapping[str, Any] | None = None

    def invoke_standalone(self, request: Mapping[str, Any]) -> ProviderResponse:
        rendered = self._renderer(deepcopy(dict(request)), self.assignment.parameters)
        unknown = sorted(set(rendered) - _MODEL_FIELDS)
        if unknown or not isinstance(rendered.get("messages"), list) or not rendered["messages"]:
            raise ValueError(f"invalid model-visible request; unsupported fields={unknown}")
        if rendered.get("stream") not in (None, False):
            raise ValueError("streaming cannot preserve the required final-response boundary")
        if rendered.get("thinking") not in ({"type": "enabled"}, {"type": "disabled"}) and rendered.get("reasoning_effort") != "none":
            raise ValueError("parameters must explicitly select an approved thinking mode")
        model_request = {"model": self.assignment.model, **rendered}
        self.last_model_visible_request = deepcopy(model_request)
        body = json.dumps(model_request, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")
        raw = self._transport(
            chat_completions_url(self._credentials.base_url),
            {"Authorization": f"Bearer {self._credentials.api_key}", "Content-Type": "application/json"},
            body,
            self._timeout_seconds,
        )
        try:
            response = json.loads(raw)
            choice = response["choices"][0]
            message = choice["message"]
            content = message["content"]
            reported_model = response["model"]
            if not isinstance(content, str) or not isinstance(reported_model, str):
                raise TypeError
        except (json.JSONDecodeError, KeyError, IndexError, TypeError):
            raise ProviderError("provider returned an invalid chat completion") from None
        private = []
        for value in (response.get("id"), message.get("reasoning_content")):
            if isinstance(value, str) and value:
                private.append(value)
        self.private_response_values = tuple(dict.fromkeys((*self.private_response_values, *private)))
        finish_reason = choice.get("finish_reason")
        metadata: dict[str, Any] = {
            "finish_reason": finish_reason if finish_reason in {"stop", "length", "tool_calls", "content_filter"} else "other"
        }
        usage = response.get("usage")
        if isinstance(usage, dict):
            public_usage = {
                key: usage[key] for key in ("prompt_tokens", "completion_tokens", "total_tokens")
                if isinstance(usage.get(key), int) and not isinstance(usage[key], bool) and usage[key] >= 0
            }
            details = usage.get("completion_tokens_details")
            if isinstance(details, dict) and isinstance(details.get("reasoning_tokens"), int) and not isinstance(details["reasoning_tokens"], bool) and details["reasoning_tokens"] >= 0:
                public_usage["completion_tokens_details"] = {"reasoning_tokens": details["reasoning_tokens"]}
            metadata["usage"] = public_usage
        return ProviderResponse(content, reported_model, model_request, metadata)
