# Assurance Phase B local runner

This directory contains a minimal experimental runner for the controlled replay
described in `docs/experiments/assurance-v2-phase-b-protocol.md`. It is not a
general eval platform and does not establish that any assurance mechanism is
reliable.

The current command uses fake providers only. It performs no network calls and
produces synthetic pipeline artifacts, not Phase B evidence. The common generator
instruction, grader instruction, and grader normative context are required inputs
because the checked-in Phase B package does not fix their exact content. They must
be reviewed before a real smoke test or formal run.

Run a local pipeline check with explicit, non-secret fixture files:

```bash
python3 -m tools.assurance_eval \
  --output-dir /tmp/assurance-eval-runs \
  --base-instructions-file /tmp/base.txt \
  --grader-instructions-file /tmp/grader.txt \
  --grader-context-file /tmp/context.txt \
  --cases p001,p002 \
  --variants B0,B1,B2 \
  --generator-base-language en \
  --case-packet-language zh-CN \
  --variant-condition-language en \
  --grader-instruction-language en \
  --grader-context-language zh-CN \
  --repetitions 2
```

Each run writes one immutable JSON record per packet, variant, and repetition,
plus immediate per-call checkpoints, a manifest, a mechanical summary, and a
completion marker. Manifests label these runs `fake_pipeline` and
`not_experimental_evidence`. Provider adapters must declare standalone context
isolation and pass only secret-free public request, error, and response metadata
to the runner.

The language of each prompt component is explicit run metadata. The checked-in
B1/B2 fixture is English; the runner rejects labeling or reusing it as the
canonical Chinese formal condition.

## Stage 2 transport scaffolding

`local_config.py` loads a mode-`0600` provider file and rejects any path inside
the repository. `openai_compat.py` contains a narrow, standalone Chat
Completions transport; the compatibility name used by the earlier DeepSeek
smoke remains available.

Every generator and grader adapter requires a separately supplied renderer ID,
renderer source digest, and renderer function. This keeps the exact message and
role mapping behind the human-review gate. The transport records the configured
model alias, operator-declared snapshot, provider-reported model field, and exact
secret-free model-visible request separately.

The local provider file must remain outside the repository. It needs
`api_style: openai_chat_completions` at connection level. A
`declared_model_snapshot` beside `model_id` is optional: when the provider cannot
guarantee a pinned backend, omit it and the artifact records `null` rather than
inventing reproducibility. Endpoint URLs and API keys are never provider
descriptor or artifact fields.

One connection may list multiple approved `models`. When it does, callers must
select an exact `model_id`; the loader never chooses by list order. The Stage 3
candidate keeps `deepseek-v4-flash` for generation and adds `qwen3.7-max` as a
second model on the same private connection for direct grading.

The explicit Stage 2 transport smoke path is fixed to `p002`, `B0`, one
repetition, zero retries, a real generator, and a deterministic fake grader. It
uses the reviewed Chinese two-message renderer, disables thinking and streaming,
and writes only to an output directory outside the repository. The run mode is
`transport_smoke`; every artifact is labeled
`transport_validation_only_not_phase_b_effect_evidence` and must not be counted
as B0 or other Phase B effect evidence.

Omitting `--confirm-network` performs the local preflight and exits without a
network call:

```bash
python3 -m tools.assurance_eval.transport_smoke \
  --config /absolute/outside-repository/setting.json \
  --output-dir /absolute/outside-repository/smoke-runs
```

Only after human approval of the provider/model and single-call budget, add
`--confirm-network`. The smoke path enforces a one-shot transport gate and will
not retry. Raw run artifacts remain local unless a human separately approves
sharing them.

## Stage 3 formal replay preparation

The candidate Stage 3 design is documented in
`docs/experiments/assurance-v2-stage3-review-proposal.md`. Its Chinese-native
B0/B1/B2 source remains separate from the English fixture and carries source
provenance. The formal renderer is `phase-b-formal-generator-zh-cn-v1`; all
variants use the same two-message rendering and fixed settings.

The checked-in proposal has `execution_enabled: false`. This command validates
the external local configuration, clean Git state, reviewed input composition,
renderer digest, and external output location without calling a provider:

```bash
python3 -m tools.assurance_eval.formal_replay \
  --config /absolute/outside-repository/setting.json \
  --output-dir /absolute/outside-repository/formal-runs
```

Without `--confirm-formal-run`, it exits with zero generator and grader calls.
During the review stage, adding the flag still fails closed because real formal
provider/grader wiring is deliberately disabled. Human/cloud approval must
resolve the recorded experiment decisions before that interlock is changed.

The different-family grader candidate has a separate no-network preparation
command. It exports the canonical p004 packet and exact Qwen model-visible
request to an external private directory and makes zero calls:

```bash
python3 -m tools.assurance_eval.direct_grader_compatibility \
  --output-dir /absolute/outside-repository/grader-compatibility
```

The checked-in compatibility configuration authorizes exactly one zero-retry
call. Execution additionally requires the external dual-model config, an empty
private output directory, a separate private writable `--approval-state-dir`, a
clean committed tree, an unconsumed durable marker, and `--confirm-network`.
The separate state directory supports read-only mounted credential files without
copying them. Formal replay remains disabled. The strict packet importer remains
the evidence boundary.
