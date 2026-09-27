"""Offline integrity checks over an executed frozen gamma-I replay."""

import argparse
import hashlib
import json
from pathlib import Path

from .__main__ import FINAL, SELECT, encoded, load_frozen


def verify(root):
    frozen = load_frozen()
    records = sorted(root.glob('runs/*/record.json'))
    expected = {f'{f}-{c}-{r}' for f in ('C13', 'S01', 'SH2') for c in 'FTD' for r in (1, 2, 3)}
    assert {p.parent.name for p in records} == expected, 'Incomplete run matrix'
    checks = []
    for path in records:
        d = json.loads(path.read_text())
        run = path.parent
        key = d['fixture'] + '-' + d['condition']
        assert d['initial_prompt'] == frozen['prompts'][key]
        assert d['v2_audit_manifest_hash'] == frozen['manifest_sha256']
        initial = json.loads((run / 'initial.request.json').read_text())
        assert initial['messages'] == [{'role': 'user', 'content': frozen['prompts'][key]}]
        assert 'tools' not in initial and 'functions' not in initial
        selection = json.loads((run / 'selection-0.request.json').read_text())
        assert selection['messages'] == [
            initial['messages'][0], {'role': 'assistant', 'content': d['initial_response']},
            {'role': 'user', 'content': SELECT + '\n\n' + encoded(frozen['index']['fixtures'][d['fixture']])}]
        assert (run / 'initial.response.json').stat().st_mtime_ns <= (run / 'selection-0.request.json').stat().st_mtime_ns
        assert len(d['selected_item_ids']) <= 2
        assert len(set(d['selected_item_ids'])) == len(d['selected_item_ids'])
        assert all(item.startswith(d['fixture'] + '-R') for item in d['selected_item_ids'])
        payloads = [frozen['payloads'][item] for item in d['selected_item_ids']]
        assert d['exact_payloads_returned'] == payloads
        assert d['final_prompt'] == '\n'.join(payloads) + ('\n' if payloads else '') + FINAL
        for request_path in run.glob('*.request.json'):
            request = json.loads(request_path.read_text())
            assert 'tools' not in request and 'functions' not in request
            response_path = request_path.with_name(request_path.name.replace('.request.json', '.response.json'))
            response = json.loads(response_path.read_text())
            assert response['metadata']['finish_reason'] == 'stop'
            assert response['messages_sha256'] == hashlib.sha256(encoded(request['messages']).encode()).hexdigest()
        final = json.loads((run / 'final.response.json').read_text())
        assert final['text'] == d['final_response']
        checks.append({'run_id': d['run_id'], 'verified': True, 'selected_ids': d['selected_item_ids']})
    grades = sorted(root.glob('scores/*/*.parsed.json'))
    return {'frozen_input_integrity': True, 'recipient_records_verified': len(checks),
            'scorer_records_present': len(grades), 'checks': checks,
            'provider_reported_models': sorted({json.loads(p.read_text())['reported_model'] for p in root.glob('runs/*/*.response.json')})}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(encoded(verify(args.directory)))


if __name__ == '__main__':
    main()
