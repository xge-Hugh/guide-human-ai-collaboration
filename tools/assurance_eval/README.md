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
the repository. `openai_compat.py` contains a narrow DeepSeek-style Chat
Completions transport. It does not provide a production renderer or a real-run
CLI, so it cannot make a Stage 2 call accidentally.

Every generator and grader adapter requires a separately supplied renderer ID,
renderer source digest, and renderer function. This keeps the exact message and
role mapping behind the human-review gate. The transport records the configured
model alias, operator-declared snapshot, provider-reported model field, and exact
secret-free model-visible request separately.

The local provider file must remain outside the repository. It needs
`api_style: openai_chat_completions` at connection level and a
`declared_model_snapshot` beside each `model_id`. Endpoint URLs and API keys are
never provider descriptor or artifact fields.
