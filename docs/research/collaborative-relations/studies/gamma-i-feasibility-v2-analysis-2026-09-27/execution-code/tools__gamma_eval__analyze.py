"""Descriptive γ-I result view; reads raw judgments without changing them."""

import argparse
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED_PLUS = {
    'C13': ('E2', 'E5'),
    'S01': ('D+1', 'D+2'),
    'SH2': ('H2-D1', 'H2-D2'),
}
VALID_PLUS = {'recognized', 'partially recognized', 'missed'}
VALID_ACTION = {'justified', 'partly justified', 'unjustified'}


def category(value):
    if isinstance(value, dict):
        value = next((value[key] for key in ('rating', 'value', 'status', 'answer', 'assessment', 'judgment')
                      if key in value), None)
    return str(value).strip().lower() if value is not None else None


def action_category(value):
    text = category(value)
    if text is None:
        return None
    for rating in ('partly justified', 'unjustified', 'justified'):
        if re.match(r'^' + re.escape(rating) + r'\b', text):
            return rating
    return text


def unnecessary_count(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, str) and re.match(r'^(?:none|no\b)', value.strip(), re.I):
        return 0
    return None


def sufficiency(value):
    if isinstance(value, dict):
        value = value.get('reported_answer', value.get('answer',
                          value.get('value', value.get('rating'))))
    return category(value)


def code_match(item, code):
    return bool(re.search(r'(?<![A-Za-z0-9])' + re.escape(code) + r'(?![A-Za-z0-9])', str(item)))


def normalize_plus(grade, fixture):
    found, extra, problems = {}, [], []
    values = grade.get('d_now_plus')
    if not isinstance(values, list):
        return found, extra, ['d_now_plus is not a list']
    for value in values:
        if not isinstance(value, dict):
            problems.append('d_now_plus item is not an object')
            continue
        matches = [code for code in REQUIRED_PLUS[fixture] if code_match(value.get('item'), code)]
        if len(matches) != 1:
            extra.append(value)
            continue
        code = matches[0]
        if code in found:
            problems.append('duplicate d_now_plus item ' + code)
            continue
        rating = category(value.get('rating'))
        if rating not in VALID_PLUS:
            problems.append(f'invalid d_now_plus rating for {code}: {rating}')
        found[code] = rating
    for code in REQUIRED_PLUS[fixture]:
        if code not in found:
            problems.append('missing required d_now_plus item ' + code)
    return found, extra, problems


def score_paths(root, run_id):
    directory = root / 'scores' / run_id
    results = []
    for repeat in (1, 2):
        files = [directory / f'scorer-{repeat}.parsed.json']
        files += sorted(directory.glob(f'scorer-{repeat}-retry*.parsed.json'))
        valid = [p for p in files if p.exists()]
        if len(valid) != 1:
            raise ValueError(f'{run_id}: scorer {repeat} has {len(valid)} valid artifacts; expected one')
        results.append(valid[0])
    return results


def read_scores(root):
    records = sorted((root / 'runs').glob('*/record.json'))
    if len(records) != 27:
        raise ValueError('Expected exactly 27 recipient records')
    scores, issues = [], []
    for path in records:
        record = json.loads(path.read_text())
        run_id, fixture = record['run_id'], record['fixture']
        for scorer_no, grade_path in enumerate(score_paths(root, run_id), 1):
            document = json.loads(grade_path.read_text())
            if document['run_id'] != run_id:
                raise ValueError('Score attached to wrong run')
            grade = document['grade']
            normalized = {'run_id': run_id, 'fixture': fixture,
                          'condition': record['condition'], 'replicate': record['replicate'],
                          'scorer': scorer_no, 'artifact': str(grade_path.relative_to(root))}
            for phase in ('initial', 'final'):
                value = grade.get(phase)
                if not isinstance(value, dict):
                    issues.append({'run_id': run_id, 'scorer': scorer_no,
                                   'phase': phase, 'issue': 'missing phase object'})
                    continue
                plus, extra, problems = normalize_plus(value, fixture)
                normalized[phase] = {
                    'd_now_plus': plus,
                    'next_action_justification': action_category(value.get('next_action_justification')),
                    'implementation_confidence': value.get('implementation_confidence'),
                    'acceptance_evidence_sufficiency': sufficiency(value.get('acceptance_evidence_sufficiency')),
                    'high_confidence_unsupported_acceptance': category(value.get('high_confidence_unsupported_acceptance')),
                    'provenance_mistake_count': len(value.get('provenance_mistakes') or []),
                    'unsupported_assertion_count': len(value.get('unsupported_factual_assertions') or []),
                    'd_now_zero': value.get('d_now_zero'),
                    'evidence_model': value.get('evidence_model'),
                }
                if extra:
                    issues.append({'run_id': run_id, 'scorer': scorer_no,
                                   'phase': phase, 'issue': 'extra/nonrequired d_now_plus items',
                                   'items': [v.get('item') for v in extra]})
                for problem in problems:
                    issues.append({'run_id': run_id, 'scorer': scorer_no,
                                   'phase': phase, 'issue': problem})
                action = normalized[phase]['next_action_justification']
                if action not in VALID_ACTION:
                    issues.append({'run_id': run_id, 'scorer': scorer_no,
                                   'phase': phase, 'issue': 'invalid action rating: ' + str(action)})
            normalized['audit_selection'] = grade.get('audit_selection')
            scores.append(normalized)
    return records, scores, issues


def summarize(root):
    records, scores, issues = read_scores(root)
    by_run = defaultdict(list)
    for score in scores:
        by_run[score['run_id']].append(score)
    agreement = {'d_now_plus': defaultdict(lambda: {'same': 0, 'compared': 0}),
                 'action': defaultdict(lambda: {'same': 0, 'compared': 0})}
    disagreements = []
    for run_id, pair in by_run.items():
        if len(pair) != 2:
            raise ValueError('Expected two scorers for ' + run_id)
        a, b = pair
        for phase in ('initial', 'final'):
            for code in REQUIRED_PLUS[a['fixture']]:
                x, y = a[phase]['d_now_plus'].get(code), b[phase]['d_now_plus'].get(code)
                if x in VALID_PLUS and y in VALID_PLUS:
                    agreement['d_now_plus'][phase]['compared'] += 1
                    agreement['d_now_plus'][phase]['same'] += x == y
                    if x != y:
                        disagreements.append({'run_id': run_id, 'phase': phase,
                                              'dimension': code, 'ratings': [x, y]})
            x, y = a[phase]['next_action_justification'], b[phase]['next_action_justification']
            if x in VALID_ACTION and y in VALID_ACTION:
                agreement['action'][phase]['compared'] += 1
                agreement['action'][phase]['same'] += x == y
                if x != y:
                    disagreements.append({'run_id': run_id, 'phase': phase,
                                          'dimension': 'next_action_justification', 'ratings': [x, y]})
    cells = []
    for fixture in ('C13', 'S01', 'SH2'):
        for condition in 'FTD':
            subset = [s for s in scores if s['fixture'] == fixture and s['condition'] == condition]
            recs = [json.loads(p.read_text()) for p in records
                    if p.parent.name in {s['run_id'] for s in subset}]
            row = {'fixture': fixture, 'condition': condition,
                   'recipient_runs': len(recs), 'scorer_judgments': len(subset),
                   'surface_words': recs[0]['surface_words'],
                   'audit_item_count': Counter(len(r['selected_item_ids']) for r in recs),
                   'initial_response_words_mean': statistics.mean(r['initial_response_words'] for r in recs),
                   'final_response_words_mean': statistics.mean(r['final_response_words'] for r in recs),
                   'audit_payload_words_mean': statistics.mean(r['audit_payload_words'] for r in recs),
                   'selected_item_ids': Counter(item for r in recs for item in r['selected_item_ids']),
                   'phases': {}}
            for phase in ('initial', 'final'):
                ratings = {}
                for code in REQUIRED_PLUS[fixture]:
                    ratings[code] = Counter(s[phase]['d_now_plus'].get(code, 'missing') for s in subset)
                confidence = [s[phase]['implementation_confidence'] for s in subset]
                row['phases'][phase] = {
                    'd_now_plus_ratings': ratings,
                    'action_justification': Counter(s[phase]['next_action_justification'] for s in subset),
                    # Scorers preserved heterogeneous recipient scales and formats.
                    # A cross-run arithmetic mean would not be interpretable.
                    'implementation_confidence_reported_values': confidence,
                    'acceptance_evidence_sufficiency': Counter(s[phase]['acceptance_evidence_sufficiency'] for s in subset),
                    'high_confidence_unsupported_acceptance': Counter(s[phase]['high_confidence_unsupported_acceptance'] for s in subset),
                    'provenance_mistake_counts': Counter(s[phase]['provenance_mistake_count'] for s in subset),
                    'unsupported_assertion_counts': Counter(s[phase]['unsupported_assertion_count'] for s in subset),
                    'd_now_zero_over_elevated_count': Counter(sum(
                        category(item.get('rating')) == 'over-elevated'
                        for item in (s[phase]['d_now_zero'] or []) if isinstance(item, dict))
                        for s in subset),
                }
            row['audit_selection'] = {
                'selected_item_relevance': Counter(
                    category(item.get('relevance'))
                    for s in subset for item in (s['audit_selection'] or {}).get('selected_items', [])
                    if isinstance(item, dict)),
                'decisive_item_located': Counter(
                    category((s['audit_selection'] or {}).get('decisive_item_located')) for s in subset),
                'index_induced_new_reasoning': Counter(
                    category((s['audit_selection'] or {}).get('index_induced_new_reasoning')) for s in subset),
                'unnecessary_request_count': Counter(
                    unnecessary_count((s['audit_selection'] or {}).get('unnecessary_requests'))
                    for s in subset),
            }
            cells.append(row)
    return {'study': 'gamma-I-feasibility-v2-2026-09-27',
            'summary_scope': 'Descriptive dimension-wise counts only; no overall winner score, treatment effect estimate, or confidence mean across heterogeneous scales.',
            'recipient_runs': len(records), 'scorer_judgments': len(scores),
            'scorer_quality_issues': issues,
            'scorer_agreement': {axis: dict(value) for axis, value in agreement.items()},
            'scorer_disagreements': disagreements,
            'cells': cells}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    # Some unreported dimensions use null Counter keys; JSON can encode those
    # keys, but sorting mixed null/string keys raises TypeError in Python.
    print(json.dumps(summarize(args.directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
