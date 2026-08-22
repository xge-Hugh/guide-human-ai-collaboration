# Assurance Phase B harness

This is a small, human-operated semantic evaluation harness for the controlled
replay described in `docs/experiments/assurance-v2-phase-b-protocol.md`. It is
not a general eval platform. `validate`, `plan`, and `report` are offline; only
`run --authorize-network` can call a provider.

## Human workflow

Keep `setting.json` outside the repository with mode `0600`. Start from
[`setting.example.json`](setting.example.json), then validate the checked-in
recipe and a named model profile:

```bash
python3 -m tools.assurance_eval validate \
  --settings /absolute/private/setting.json \
  --profile phase-b-stage3
```

Preview an exploratory plan without writing or making network calls:

```bash
python3 -m tools.assurance_eval plan \
  --settings /absolute/private/setting.json \
  --profile phase-b-stage3 \
  --mode exploratory
```

An exploratory run may use modified semantic sources. It resolves the recipe
once at run start, records exact hashes and dirty-tree provenance, and is permanently labeled
`non_formal_exploratory_evidence`:

```bash
python3 -m tools.assurance_eval run \
  --recipe docs/experiments/assurance-v2-phase-b.recipe.json \
  --settings /absolute/private/setting.json \
  --profile phase-b-stage3 \
  --mode exploratory \
  --authorize-network
```

A formal run resolves the recipe and selected profile once at run start. It
captures that secret-free resolved configuration in the run directory and uses
the captured in-memory experiment and model assignments for the entire execution.
There is no frozen-plan file or manual SHA approval step. The output root must
already exist outside the repository with mode `0700`:

```bash
python3 -m tools.assurance_eval run \
  --recipe docs/experiments/assurance-v2-phase-b.recipe.json \
  --settings /absolute/private/setting.json \
  --profile phase-b-stage3 \
  --mode formal \
  --authorize-network \
  --tranche tranche_1
```

The checked-in recipe has `formal_execution_enabled: true`; formal execution
still requires clean committed provenance and explicit network authorization.
No automatic retry occurs. Any operational
failure blocks only that execution, preserves its sanitized call/record evidence,
and stops all further calls; it creates no reusable denial or authorization marker.

Tranche 2 additionally requires the completed private tranche-1 run; the harness
verifies its plan hash, tranche identity, artifact-tree digest, and secret-scan
status before continuation:

```bash
python3 -m tools.assurance_eval run \
  --recipe docs/experiments/assurance-v2-phase-b.recipe.json \
  --settings /absolute/private/setting.json \
  --profile phase-b-stage3 \
  --mode formal \
  --authorize-network \
  --tranche tranche_2 \
  --prior-run /absolute/private/runs/TRANCHE_1_RUN_ID
```

Inspect a completed run offline:

```bash
python3 -m tools.assurance_eval report /absolute/private/runs/RUN_ID

python3 -m tools.assurance_eval report /absolute/private/runs/RUN_ID --case p005
```

## What `plan` shows

The preview includes mode, selected cases and variants, the generator and grader
provider/model/family, parameters, role-specific timeouts, repetitions and counterbalanced order,
planned generator/grader call counts, renderer IDs and hashes, evidence label,
output destination, and the resolved-plan hash. The saved plan also binds source
hashes, grading schema/policy, instructions, exact execution order, provenance,
and the zero-retry/standalone/no-reasoning evidence policy. It never includes an
endpoint, API key, or private connection name.

An abbreviated resolved plan looks like:

```json
{
  "schema_version": 1,
  "resolved_plan_sha256": "<sha256>",
  "plan": {
    "mode": "formal",
    "formal_execution_enabled": true,
    "profile": "phase-b-stage3",
    "selection": {"cases": ["p003", "...", "p013"], "variants": ["B0", "B1", "B2"]},
    "roles": {
      "generator": {"provider": "custom", "model": "deepseek-v4-flash", "family": "DeepSeek", "parameters": {"thinking": {"type": "enabled"}, "max_tokens": 65536, "stream": false}},
      "grader": {"provider": "custom", "model": "qwen3.7-plus", "family": "Qwen", "parameters": {"thinking": {"type": "enabled"}, "max_tokens": 32768, "stream": false}}
    },
    "timeouts_seconds": {"generator": 900, "grader": 600},
    "expected_calls": {"generator": 90, "grader": 90, "maximum_total": 180},
    "evidence_label": "phase_b_controlled_replay_raw_evidence_pending_adjudication"
  }
}
```

## Architecture and migration

| Responsibility | New module | Replaces |
|---|---|---|
| model catalog / profiles | `config.py` | `local_config.py` and per-script model selection |
| recipe / source validation | `experiment.py` | `loading.py` and proposal literal checks |
| immutable schedule and plan hash | `planning.py` | `RunConfig`, formal proposal replay checks, per-script SHA checks |
| request rendering | `renderers.py` | transport, thinking, formal, and direct-grader renderers |
| provider transport | `transport.py` | `openai_compat.py` |
| grader boundary / strict JSON | `grading.py` | runner grading plus grader bridge parsing |
| private append-only evidence | `artifacts.py` | runner writes and per-script scans/tree hashes |
| clean provenance / network gate | `policy.py` | per-script confirmation flags and consumption markers |
| orchestration | `execution.py` | runner and stage-specific execution bodies |
| offline result view | `reporting.py` | stage-specific result reports |
| human CLI | `__main__.py` | separate smoke/formal entry points |

Stage 2 and Stage 3 smoke behavior is now exercised with single-case/single-call
resolved plans and injected no-network transports in the consolidated tests.
There are no special case IDs, model IDs, approval marker files, or alternate
artifact paths in Python.

## Central evidence boundaries

- Generator packets contain only case ID, pre-context, user message, selected
  variant instruction, and common generator instruction. Rubrics are introduced
  only when constructing a fresh standalone grader packet.
- Exact model-visible requests and raw final response text are stored. Provider
  type, configured model, declared family, declared snapshot, and per-call
  provider-reported model remain separate fields. No route identity is invented;
  custom routing, backend identity, alias resolution, and backend seed remain
  uncontrolled where the provider does not expose them.
- Provider response IDs and reasoning text are structurally discarded; only
  numeric reasoning token counts may be retained. Post-run scanning checks
  credentials and private endpoints. Discarded fields are never turned into
  substring deny-lists that could erase identical legitimate final-response text.
- Grade parsing rejects duplicate JSON keys, missing/extra axes, invalid enums,
  empty applicability basis, and violations of the conditional N/A rule.
- Artifacts are new-only, mode `0600` under private mode-`0700` directories,
  outside the repository by default.
- Formal resolution requires a clean committed tree, different declared
  generator/grader families, and explicit network authorization. The automatic
  resolved-plan hash remains provenance metadata; execution uses the once-resolved
  in-memory recipe, sources, and model assignments without reloading them.

The default report includes case/variant groups and adjudication flags. Case
inspection shows final responses, axis judgments, model identities, usage,
timing, status, and artifact paths. The harness does not compute a total score,
automatic B0/B1/B2 winner, or pass/fail conclusion. The old DeepSeek-thinking
and Qwen-grader compatibility configurations are historical, completed, and
non-executable; the unified recipe/harness is the active execution path.
