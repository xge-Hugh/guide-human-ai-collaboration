"""Streaming wire transport; expose only the complete final message to the runner."""

import json
import socket
from http.client import RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

from tools.assurance_eval.models import ProviderError, ProviderResponse
from tools.assurance_eval.transport import _NoRedirect, chat_completions_url


def read_sse(lines):
    parts, model, finish, usage = [], None, None, {}
    done = False
    for raw in lines:
        line = raw.decode('utf-8').strip()
        if not line.startswith('data:'):
            continue
        data = line[5:].strip()
        if data == '[DONE]':
            done = True
            break
        chunk = json.loads(data)
        if 'error' in chunk:
            raise ProviderError('provider returned streaming error')
        if isinstance(chunk.get('model'), str):
            model = chunk['model']
        for choice in chunk.get('choices', []):
            if choice.get('index', 0) != 0:
                raise ProviderError('multiple streaming choices unsupported')
            delta = choice.get('delta', {})
            if delta.get('tool_calls') or delta.get('function_call'):
                raise ProviderError('unexpected tool response')
            value = delta.get('content')
            if isinstance(value, str):
                parts.append(value)
            if choice.get('finish_reason'):
                finish = choice['finish_reason']
        raw_usage = chunk.get('usage')
        if isinstance(raw_usage, dict):
            usage.update({k: v for k, v in raw_usage.items()
                          if k in ('prompt_tokens', 'completion_tokens', 'total_tokens')
                          and isinstance(v, int) and not isinstance(v, bool)})
            details = raw_usage.get('completion_tokens_details', {})
            if isinstance(details, dict) and isinstance(details.get('reasoning_tokens'), int):
                usage['completion_tokens_details'] = {'reasoning_tokens': details['reasoning_tokens']}
    if not done or not model or not finish or not parts:
        raise ProviderError('incomplete streaming response')
    return ''.join(parts), model, {'finish_reason': finish, 'usage': usage, 'stream_done': True}


class StreamingProvider:
    def __init__(self, resolved, timeout_seconds):
        self.resolved = resolved
        self.timeout = timeout_seconds

    def invoke_standalone(self, request):
        resolved = self.resolved
        model_request = {'model': resolved.assignment.model,
                         **resolved.assignment.parameters, 'messages': request['messages']}
        assert model_request.get('stream') is True
        assert 'tools' not in model_request and 'functions' not in model_request
        call = Request(chat_completions_url(resolved.credentials.base_url),
                       data=json.dumps(model_request, ensure_ascii=False, allow_nan=False).encode(),
                       headers={'Authorization': 'Bearer ' + resolved.credentials.api_key,
                                'Content-Type': 'application/json'}, method='POST')
        try:
            with build_opener(_NoRedirect).open(call, timeout=self.timeout) as response:
                text, model, metadata = read_sse(response)
        except HTTPError as error:
            raise ProviderError(f'provider HTTP status {error.code}') from None
        except (URLError, TimeoutError, socket.timeout, RemoteDisconnected,
                ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as error:
            # Class names reveal diagnostics without endpoints or exception text.
            detail = type(error).__name__
            if isinstance(error, URLError):
                detail += '/' + type(error.reason).__name__
            raise ProviderError('provider transport failure: ' + detail) from None
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError):
            raise ProviderError('invalid streaming response') from None
        return ProviderResponse(text, model, model_request, metadata)
