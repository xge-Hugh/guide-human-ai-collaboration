"""Non-experimental streaming diagnostic; never starts recipient runs."""

import argparse
import json
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, build_opener

from tools.assurance_eval.config import load_model_catalog
from tools.assurance_eval.transport import _NoRedirect, chat_completions_url
from .__main__ import ROOT, PARAMETERS, encoded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', type=Path, required=True)
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    catalog = load_model_catalog(args.settings, ROOT)
    role = catalog.resolve('gamma-i-v2', PARAMETERS)['grader']
    request = json.loads(args.request.read_text())
    request['stream'] = True
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'request.json').write_text(encoded(request))
    start = time.monotonic()
    result = {'purpose': 'preflight_transport_diagnostic_only', 'chunks': 0}
    content = []
    call = Request(chat_completions_url(role.credentials.base_url),
                   data=json.dumps(request, ensure_ascii=False).encode(),
                   headers={'Authorization': 'Bearer ' + role.credentials.api_key,
                            'Content-Type': 'application/json'}, method='POST')
    try:
        with build_opener(_NoRedirect).open(call, timeout=180) as response:
            result['http_status'] = response.status
            result['content_type'] = response.headers.get('Content-Type', '')
            for raw in response:
                line = raw.decode('utf-8').strip()
                if not line.startswith('data:'):
                    continue
                data = line[5:].strip()
                if data == '[DONE]':
                    result['done'] = True
                    break
                chunk = json.loads(data)
                result['chunks'] += 1
                if result['chunks'] == 1:
                    result['first_chunk_seconds'] = time.monotonic() - start
                    print('First SSE chunk received', flush=True)
                if chunk.get('model'):
                    result['reported_model'] = chunk['model']
                for choice in chunk.get('choices', []):
                    piece = choice.get('delta', {}).get('content')
                    if isinstance(piece, str):
                        content.append(piece)
                    if choice.get('finish_reason'):
                        result['finish_reason'] = choice['finish_reason']
                # Never retain reasoning, credentials, response IDs, or arbitrary metadata.
                if isinstance(chunk.get('usage'), dict):
                    result['usage'] = {k: v for k, v in chunk['usage'].items()
                                       if k in ('prompt_tokens', 'completion_tokens', 'total_tokens') and isinstance(v, int)}
        result['text'] = ''.join(content)
    except Exception as error:
        result['error_type'] = type(error).__name__
        if isinstance(error, URLError):
            result['reason_type'] = type(error.reason).__name__
        if isinstance(getattr(error, 'code', None), int):
            result['http_error_status'] = error.code
        result['partial_content_characters'] = sum(map(len, content))
    result['elapsed_seconds'] = time.monotonic() - start
    text = encoded(result)
    if any(s in text for s in catalog.private_scan_values):
        raise ValueError('Private configuration in result')
    (args.output / 'response.json').write_text(text)
    print(encoded({k: v for k, v in result.items() if k != 'text'}), flush=True)


if __name__ == '__main__':
    main()
