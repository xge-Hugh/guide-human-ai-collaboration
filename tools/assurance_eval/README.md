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
  --repetitions 2
```

Each run writes one immutable JSON record per packet, variant, and repetition,
plus immediate per-call checkpoints, a manifest, a mechanical summary, and a
completion marker. Manifests label these runs `fake_pipeline` and
`not_experimental_evidence`. Provider adapters must declare standalone context
isolation and pass only secret-free public request, error, and response metadata
to the runner.
