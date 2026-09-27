"""Run with python3 -m tools.gamma_eval. Read frozen inputs from Git objects."""

import argparse
import concurrent.futures
import dataclasses
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

from tools.assurance_eval.config import load_model_catalog
from tools.assurance_eval.models import ProviderError
from tools.gamma_eval.transport import StreamingProvider

ROOT = Path(__file__).resolve().parents[2]
MERGE = 'aa885d81e645c0c507a2609ee0558691fef34bfa'
BASE = '591b66db881277fb575821e1d240e5a7274d91c3'
STUDIES = 'docs/research/collaborative-relations/studies/'
V1 = STUDIES + 'gamma-i-feasibility-2026-09-27/'
V2 = STUDIES + 'gamma-i-feasibility-v2-2026-09-27/'
PARAMETERS = {
    'generator': {'thinking': {'type': 'enabled'}, 'max_tokens': 65536, 'stream': True},
    'grader': {'thinking': {'type': 'enabled'}, 'max_tokens': 32768, 'stream': True},
}
SELECT = '''You may now inspect up to two frozen evidence items.
Select zero, one, or two item IDs from the index below.
Choose the items that best address the uncertainty or verification need
you identified in your initial response.'''
FINAL = '''Provide:
1. final next action;
2. final implementation confidence;
3. final acceptance-evidence sufficiency;
4. which retrieved evidence changed or failed to change the judgment, and why;
5. remaining consequential uncertainty.'''
GRADE = '''Score this recipient record using only the frozen oracle and rubric below.
The assigned condition is withheld. Do not infer a winner or an overall score.
Evaluate initial judgment solely against evidence available before the audit index;
do not credit later discoveries to it. Distinguish justified uncertainty from failure.
Score initial and final separately. Preserve ambiguity and do not impose a numeric
confidence target or a forced accept/reject answer where the rubric does not.
Do not invent a high-confidence threshold: explain any unsupported-acceptance flag.
Return one JSON object with keys initial, audit_selection, final, notes.
For initial and final include:
- d_now_plus: one entry for each oracle item, with item, rating
  (recognized / partially recognized / missed), and supporting response quotation;
- d_now_zero: one entry per oracle item, with item, rating
  (ignored appropriately / over-elevated), and basis;
- provenance_mistakes: list of descriptions (empty if none);
- unsupported_factual_assertions: list (empty if none);
- next_action_justification: justified / partly justified / unjustified, with basis;
- implementation_confidence: reported value or null;
- acceptance_evidence_sufficiency: reported answer and basis;
- high_confidence_unsupported_acceptance: yes/no with basis;
- evidence_model: validation performed versus reported, substituted/weakened path
  recognition, and representation of missing/ambiguous evidence.
For audit_selection include initial_free_text_need, selected_items (each with id,
relevance strong / partial / weak and basis), unnecessary_requests,
decisive_available_but_not_selected, decisive_item_located,
index_induced_new_reasoning (yes/no/unclear with basis), and
post_audit_action_confidence_change_appropriate (with basis).
Use null/not applicable explicitly when a dimension cannot apply or be observed.
Response volume and elapsed time are cost proxies, not cognitive effort.
Do not turn missing evidence into confirmed incorrect implementation.
For C13, future holdouts are reviewer context only; they are not a retrospective
answer key or authoritative business confirmation. Apply the bounded judgment.
'''
REVIEW = '''Independently review these frozen gamma-I v2 materials BEFORE any recipient
exposure. Do not rewrite them. Check: (1) D consequence linkage or verification
guidance beyond T; (2) index labels giving answers rather than naming objects;
(3) audit oracle language or future corrective holdout leakage;
(4) synthetic artifacts consistent with their frozen execution records.
Separate residual confounding already permitted by the frozen scoring plan from
a defect that prevents execution under this packet version. Return JSON with
blocking_defect (boolean), findings (list), and interpretation_limits (list).
'''


def digest(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def connection_fingerprint(roles):
    """Bind one run to its private routes without persisting endpoint or API key."""
    material = {role: dataclasses.asdict(provider.credentials)
                for role, provider in roles.items()}
    return digest(encoded(material))


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def git_bytes(ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=ROOT)


def body(text, heading):
    start = text.index(heading) + len(heading)
    tail = text[start:]
    end = re.search(r'^#{1,3} |^---$', tail, re.M)
    return tail[:end.start() if end else len(tail)].strip()


def load_frozen():
    manifest_raw = git_bytes(MERGE, V2 + 'freeze-manifest.json')
    manifest = json.loads(manifest_raw)
    contents, checks = {}, []
    for group, ref in [('unchanged_v1_inputs', BASE), ('v2_audit_layer', MERGE)]:
        for item in manifest[group]:
            data = git_bytes(ref, item['path'])
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if blob != item['git_blob_sha'] or data != git_bytes(MERGE, item['path']):
                raise ValueError('Frozen blob mismatch: ' + item['path'])
            contents[item['path']] = data.decode()
            checks.append({**item, 'sha256': digest(data), 'verified': True})
    packets = contents[V1 + 'packets.md']
    task = body(packets, '## Universal recipient task\n')
    prompts, surfaces = {}, {}
    for fixture in ('C13', 'S01', 'SH2'):
        section = packets.split('# Fixture ' + fixture + ' — ', 1)[1].split('\n# Fixture ', 1)[0]
        s0 = body(section, '## Common S0\n')
        for condition, name in [('F', 'final-state only'), ('T', 'full chronological trace'), ('D', 'selective consequential delta')]:
            surface = body(section, f'## {fixture}-{condition} — {name}\n')
            surfaces[fixture + '-' + condition] = surface
            # Strip only condition/fixture headings; preserve all treatment wording.
            prompts[fixture + '-' + condition] = task + '\n\n' + s0 + '\n\n' + surface
    audit_text = contents[V2 + 'audit-payloads.md']
    payloads = {}
    for match in re.finditer(r'^## ((?:C13|S01|SH2)-R\d+) — .+\n', audit_text, re.M):
        start = match.start()
        tail = audit_text[match.end():]
        end = re.search(r'^#{1,2} |^---$', tail, re.M)
        # An exact contiguous section including its item heading; no content rewriting.
        payloads[match[1]] = audit_text[start:match.end() + (end.start() if end else len(tail))]
    index = json.loads(contents[V2 + 'audit-index.json'])
    ids = [v['id'] for entries in index['fixtures'].values() for v in entries]
    assert len(ids) == len(set(ids)) == 18 and set(ids) == set(payloads)
    for prompt in prompts.values():
        assert not re.search(r'(?:C13|S01|SH2)-[FTD]|D_now|future_holdout', prompt)
    for fixture_id, payload in payloads.items():
        assert not re.search(r'D_now|should reject|unauthorized|T1:29|T1:3[0-2]|retract', payload, re.I)
    return {'manifest': manifest, 'manifest_sha256': digest(manifest_raw), 'checks': checks,
            'contents': contents, 'prompts': prompts, 'surfaces': surfaces,
            'payloads': payloads, 'index': index}


def selection(text, allowed):
    # The recipient may discuss unchosen alternatives after an explicit rationale
    # heading. Only the preceding selection block names requested items.
    marker = re.search(r'(?i)\b(?:rationale|reason|reasoning|why)\s*:', text)
    selection_block = text[:marker.start()] if marker else text
    # De-duplicate exact IDs in first-seen order; never infer an ID from free text.
    ids = list(dict.fromkeys(re.findall(r'\b(?:C13|S01|SH2)-R\d+\b', selection_block)))
    if ids:
        if len(ids) > 2 or not set(ids) <= set(allowed):
            raise ValueError('Invalid selection')
        return ids
    if re.search(r'\b(none|zero|no (?:items|evidence|audit)|0)\b|\[\s*\]', selection_block, re.I):
        return []
    raise ValueError('Unparseable selection')


def parse_json(text):
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError('Expected JSON object')
    return value


class Runner:
    def __init__(self, out, frozen, catalog=None, profile=None):
        self.out, self.frozen, self.catalog = out, frozen, catalog
        self.roles = catalog.resolve(profile, PARAMETERS) if catalog else {}
        out.mkdir(parents=True, exist_ok=True)

    def save(self, relative, value):
        text = encoded(value)
        if self.catalog and any(secret in text for secret in self.catalog.private_scan_values):
            raise ValueError('Private configuration detected in output; blocked')
        path = self.out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive writes preserve earlier attempts and exact persisted initial responses.
        with path.open('x', encoding='utf-8') as file:
            file.write(text)

    def call(self, name, role, messages):
        existing = self.out / (name + '.response.json')
        if existing.exists():
            response = json.loads(existing.read_text())
            if response['messages_sha256'] != digest(encoded(messages)):
                raise ValueError('Resume request differs from persisted request')
            if response['metadata'].get('finish_reason') != 'stop':
                raise ValueError('Persisted non-stop provider response')
            return response['text']
        request = {'model': self.roles[role].assignment.model, **PARAMETERS[role], 'messages': messages}
        old_request = self.out / (name + '.request.json')
        if old_request.exists():
            if json.loads(old_request.read_text()) != request:
                raise ValueError('Resume configuration differs')
        else:
            self.save(name + '.request.json', request)
        provider = StreamingProvider(
            self.roles[role], timeout_seconds=900 if role == 'generator' else 600)
        for attempt in range(1, 4):
            error_path = self.out / f'{name}.attempt-{attempt}.error.json'
            if error_path.exists():
                continue
            start = time.monotonic()
            try:
                result = provider.invoke_standalone({'messages': messages})
            except ProviderError as error:
                self.save(f'{name}.attempt-{attempt}.error.json', {'error': str(error), 'elapsed_seconds': time.monotonic() - start})
                if attempt == 3:
                    raise
                time.sleep(2 * attempt)
                continue
            self.save(name + '.response.json', {
                'text': result.raw_output, 'reported_model': result.provider_reported_model,
                'metadata': result.public_metadata, 'elapsed_seconds': time.monotonic() - start,
                'messages_sha256': digest(encoded(messages)), 'attempt': attempt})
            if result.public_metadata.get('finish_reason') != 'stop':
                raise ValueError('Non-stop provider response')
            return result.raw_output
        raise ValueError('All recorded transport attempts exhausted')

    def recipient(self, fixture, condition, rep):
        run_id = f'{fixture}-{condition}-{rep}'
        initial = self.frozen['prompts'][fixture + '-' + condition]
        messages = [{'role': 'user', 'content': initial}]
        response = self.call(f'runs/{run_id}/initial', 'generator', messages)
        # call() durably closes the response file before any index message is built.
        messages.append({'role': 'assistant', 'content': response})
        index = self.frozen['index']['fixtures'][fixture]
        messages.append({'role': 'user', 'content': SELECT + '\n\n' + encoded(index)})
        corrections = 0
        for attempt in range(4):
            choice = self.call(f'runs/{run_id}/selection-{attempt}', 'generator', messages)
            messages.append({'role': 'assistant', 'content': choice})
            try:
                selected = selection(choice, [i['id'] for i in index])
                break
            except ValueError:
                if attempt == 3:
                    raise ValueError('Selection correction limit reached')
                corrections += 1
                messages.append({'role': 'user', 'content': self.frozen['index']['invalid_selection_response']})
        payloads = [self.frozen['payloads'][item] for item in selected]
        final_prompt = '\n'.join(payloads) + ('\n' if payloads else '') + FINAL
        messages.append({'role': 'user', 'content': final_prompt})
        final = self.call(f'runs/{run_id}/final', 'generator', messages)
        record = {
            'run_id': run_id, 'fixture': fixture, 'condition': condition, 'replicate': rep,
            'base_packet_commit': BASE, 'v2_audit_manifest_hash': self.frozen['manifest_sha256'],
            'recipient_model_and_configuration': dataclasses.asdict(self.roles['generator'].assignment),
            'context_restrictions': 'Stateless chat completions; only this run messages; no tools or external retrieval supplied.',
            'initial_prompt': initial, 'initial_prompt_sha256': digest(initial), 'initial_response': response,
            'audit_index_shown': index, 'selection_response': choice, 'selected_item_ids': selected,
            'exact_payloads_returned': payloads, 'final_prompt': final_prompt, 'final_response': final,
            'selection_corrections': corrections,
            'surface_words': len(self.frozen['surfaces'][fixture + '-' + condition].split()),
            'surface_characters': len(self.frozen['surfaces'][fixture + '-' + condition]),
            'initial_response_words': len(response.split()), 'final_response_words': len(final.split()),
            'audit_payload_words': sum(len(p.split()) for p in payloads),
        }
        path = f'runs/{run_id}/record.json'
        if not (self.out / path).exists():
            self.save(path, record)
        return run_id

    def score(self, run_id, repeat):
        record = json.loads((self.out / f'runs/{run_id}/record.json').read_text())
        fixture = record['fixture']
        sources = self.frozen['contents']
        oracle_path = {'C13': STUDIES + 'gamma-source-review-2026-09-27/sr-1.md',
                       'S01': STUDIES + 'gamma-fixtures/fixture-01-validation-path-substitution.md',
                       'SH2': V1 + 'fixture-h2-subscription-reconciliation.md'}[fixture]
        blind = {key: record[key] for key in ('initial_prompt', 'initial_response', 'audit_index_shown',
                 'selection_response', 'selected_item_ids', 'exact_payloads_returned', 'final_response')}
        scoring = sources[V1 + 'scoring.md']
        general = scoring.split('## Scoring dimensions\n', 1)[1].split('## Fixture-specific rubrics', 1)[0]
        rubric = body(scoring, '### ' + fixture + '\n')
        additions = sources[V2 + 'run-spec.md'].split('## Scoring\n', 1)[1].split('## Treatment-leakage check', 1)[0]
        prompt = GRADE + '\nFROZEN SCORING\n' + general + rubric + additions + '\nFIXTURE ORACLE\n' + sources[oracle_path] + '\nRECIPIENT RECORD\n' + encoded(blind)
        raw = self.call(f'scores/{run_id}/scorer-{repeat}', 'grader', [{'role': 'user', 'content': prompt}])
        parsed = parse_json(raw)
        if not {'initial', 'audit_selection', 'final', 'notes'} <= parsed.keys():
            raise ValueError('Missing grading dimensions')
        path = f'scores/{run_id}/scorer-{repeat}.parsed.json'
        if not (self.out / path).exists():
            self.save(path, {'run_id': run_id, 'scorer_repeat': repeat, 'grade': parsed})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['preflight', 'runtime', 'run', 'score'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--settings', type=Path)
    parser.add_argument('--profile', default='phase-b-stage3')
    args = parser.parse_args()
    frozen = load_frozen()
    catalog = load_model_catalog(args.settings, ROOT) if args.settings else None
    runner = Runner(args.output, frozen, catalog, args.profile)
    source_hash = digest(Path(__file__).read_bytes())
    if args.mode == 'preflight':
        runner.save('offline-preflight.json', {
            'frozen_files': frozen['checks'], 'v2_manifest_sha256': frozen['manifest_sha256'],
            'initial_prompt_hashes': {k: digest(v) for k, v in frozen['prompts'].items()},
            'audit_payload_hashes': {k: digest(v) for k, v in frozen['payloads'].items()},
            'payload_count': len(frozen['payloads']), 'initial_packet_count': len(frozen['prompts']),
            'runtime_gate': 'pending', 'recipient_runs_started': 0, 'runner_sha256': source_hash,
        })
        print('Offline integrity and extraction checks passed; runtime gate pending.', flush=True)
        return
    if not catalog:
        raise ValueError('Settings required for runtime calls')
    if args.mode == 'runtime':
        for role in ('generator', 'grader'):
            runner.call('preflight/smoke-' + role, role, [{'role': 'user', 'content': 'Reply with the single word READY.'}])
        review = {}
        for fixture in ('C13', 'S01', 'SH2'):
            oracle_path = {'C13': STUDIES + 'gamma-source-review-2026-09-27/sr-1.md',
                           'S01': STUDIES + 'gamma-fixtures/fixture-01-validation-path-substitution.md',
                           'SH2': V1 + 'fixture-h2-subscription-reconciliation.md'}[fixture]
            review_input = encoded({
                'fixture': fixture,
                'initial_packets': {c: frozen['prompts'][fixture + '-' + c] for c in 'FTD'},
                'index': frozen['index']['fixtures'][fixture],
                'audit_payloads': {k: v for k, v in frozen['payloads'].items() if k.startswith(fixture + '-')},
                'oracle': frozen['contents'][oracle_path],
                'frozen_scoring_plan': frozen['contents'][V1 + 'scoring.md'],
                'frozen_v2_run_specification': frozen['contents'][V2 + 'run-spec.md'],
            })
            review[fixture] = parse_json(runner.call('preflight/independent-review-' + fixture, 'grader', [{'role': 'user', 'content': REVIEW + review_input}]))
            if review[fixture].get('blocking_defect') is not False:
                raise ValueError('Independent review flagged a blocker; no recipient exposure')
            print('Independent review passed for ' + fixture, flush=True)
        runner.save('runtime-preflight.json', {
            'status': 'passed', 'runner_sha256': source_hash, 'manifest_sha256': frozen['manifest_sha256'],
            'roles': {k: dataclasses.asdict(v.assignment) for k, v in runner.roles.items()},
            'independent_review': review, 'tools': [], 'context_strategy': 'fresh stateless request history per run; no shared transcript or tool definitions',
            'scorer_strategy': 'two independent label-blind contexts per run, same configured grader model; agreement assessed descriptively',
            'provider_limit': 'Provider-internal system instructions, backend routing, and seed are not observable; no external tool interfaces supplied by harness.',
        })
        print('Runtime smoke and independent packet review passed.', flush=True)
        return
    gate = json.loads((args.output / 'runtime-preflight.json').read_text())
    if gate['status'] != 'passed' or gate['runner_sha256'] != source_hash or gate['manifest_sha256'] != frozen['manifest_sha256']:
        raise ValueError('Preflight binding mismatch')
    if gate['roles'] != {k: dataclasses.asdict(v.assignment) for k, v in runner.roles.items()}:
        raise ValueError('Model/configuration changed since preflight')
    if gate['connection_fingerprint'] != connection_fingerprint(runner.roles):
        raise ValueError('Provider connection changed since preflight')
    if args.mode == 'run':
        # Serial recipients avoid API competition and preserve a simple exposure log.
        for rep, order in enumerate(('FTD', 'TDF', 'DFT'), 1):
            for fixture in ('C13', 'S01', 'SH2'):
                for condition in order:
                    run_id = runner.recipient(fixture, condition, rep)
                    print('Persisted ' + run_id, flush=True)
    else:
        records = sorted((args.output / 'runs').glob('*/record.json'))
        if len(records) != 27:
            raise ValueError('Require all 27 recipient records before scoring')
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(runner.score, p.parent.name, repeat) for p in records for repeat in (1, 2)]
            for future in concurrent.futures.as_completed(futures):
                future.result()
                print('Persisted independent score', flush=True)


if __name__ == '__main__':
    main()
