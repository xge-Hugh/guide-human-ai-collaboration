import json
import tempfile
import unittest
from pathlib import Path

from tools.gamma_eval.__main__ import (
    Runner, load_frozen, selection, PARAMETERS, V2,
)
from tools.assurance_eval.models import ModelAssignment, ResolvedProvider, ProviderCredentials
from tools.assurance_eval.models import ProviderError
from tools.gamma_eval.transport import read_sse


class GammaBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = load_frozen()

    def test_manifest_and_payload_sections(self):
        self.assertEqual(len(self.frozen['checks']), 9)
        self.assertEqual(len(self.frozen['prompts']), 9)
        self.assertEqual(len(self.frozen['payloads']), 18)
        source = self.frozen['contents'][V2 + 'audit-payloads.md']
        for item, payload in self.frozen['payloads'].items():
            self.assertIn(payload, source)
            self.assertTrue(payload.startswith('## ' + item + ' — '))
            self.assertEqual(payload.count('\n## '), 0)
            self.assertNotIn('---', payload)

    def test_selection_is_syntactic_and_fixture_scoped(self):
        allowed = ['C13-R1', 'C13-R2']
        self.assertEqual(selection('C13-R2, C13-R1', allowed), ['C13-R2', 'C13-R1'])
        self.assertEqual(selection('No audit items are needed; zero.', allowed), [])
        for value in ['S01-R1', 'C13-R1 C13-R1', 'C13-R1 C13-R2 C13-R3',
                      'Please inspect the mapping code', 'C13-R99']:
            with self.assertRaises(ValueError):
                selection(value, allowed)

    def test_27_fresh_histories_and_persistence_before_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = Runner(Path(tmp), self.frozen)
            runner.roles = {'generator': ResolvedProvider(
                ModelAssignment('fake', 'fake', 'fake', None, PARAMETERS['generator']),
                ProviderCredentials('openai_chat_completions', '', ''))}
            seen_initial = []

            def fake_call(name, role, messages):
                run_id = name.split('/')[1]
                fixture = run_id.split('-')[0]
                if name.endswith('/initial'):
                    self.assertEqual(len(messages), 1)
                    self.assertNotIn('item IDs from the index', messages[0]['content'])
                    self.assertNotIn('D_now', messages[0]['content'])
                    self.assertNotIn(fixture + '-R', messages[0]['content'])
                    self.assertTrue(all(m['role'] != 'tool' for m in messages))
                    runner.save(name + '.response.json', {'text': 'initial judgment'})
                    seen_initial.append(run_id)
                    return 'initial judgment'
                self.assertTrue((Path(tmp) / f'runs/{run_id}/initial.response.json').exists())
                if '/selection-' in name:
                    self.assertEqual(len(messages), 3)
                    return fixture + '-R2, ' + fixture + '-R1'
                self.assertEqual(len(messages), 5)
                self.assertTrue(messages[-1]['content'].startswith(
                    self.frozen['payloads'][fixture + '-R2'] + '\n' + self.frozen['payloads'][fixture + '-R1']))
                return 'final judgment'

            runner.call = fake_call
            for rep in (1, 2, 3):
                for fixture in ('C13', 'S01', 'SH2'):
                    for condition in 'FTD':
                        runner.recipient(fixture, condition, rep)
            self.assertEqual(len(set(seen_initial)), 27)
            for path in Path(tmp).glob('runs/*/record.json'):
                record = json.loads(path.read_text())
                self.assertEqual(record['exact_payloads_returned'], [
                    self.frozen['payloads'][item] for item in record['selected_item_ids']])

    def test_streaming_keeps_final_text_and_requires_completion(self):
        chunks = [
            {'model': 'test-model', 'choices': [{'index': 0, 'delta': {'reasoning_content': 'private reasoning'}}]},
            {'model': 'test-model', 'choices': [{'index': 0, 'delta': {'content': 'initial '}}]},
            {'model': 'test-model', 'choices': [{'index': 0, 'delta': {'content': 'judgment'}, 'finish_reason': 'stop'}]},
        ]
        lines = [('data: ' + json.dumps(c) + '\n').encode() for c in chunks]
        with self.assertRaises(ProviderError):
            read_sse(lines)
        text, model, metadata = read_sse(lines + [b'data: [DONE]\n'])
        self.assertEqual(text, 'initial judgment')
        self.assertNotIn('private reasoning', text)
        self.assertEqual(model, 'test-model')
        self.assertEqual(metadata['finish_reason'], 'stop')

    def test_streaming_rejects_tool_calls(self):
        chunk = {'model': 'test-model', 'choices': [{'delta': {'tool_calls': [{'name': 'read_file'}]}}]}
        with self.assertRaises(ProviderError):
            read_sse([('data: ' + json.dumps(chunk)).encode(), b'data: [DONE]'])


if __name__ == '__main__':
    unittest.main()
