# Experiment γ-I feasibility v2 — executable audit repair

- **Date**: 2026-09-27
- **Status**: candidate executable packet; no v2 recipient exposure yet.
- **Predecessor**: `../gamma-i-feasibility-2026-09-27/` (PR #41).
- **Reason for new version**: v1 preflight found that audit artifacts were named but their exact returnable payloads were not frozen. The local agent correctly stopped at 0/27 runs.

## What changes

v2 does **not** change the γ-I settlement treatments. It reuses the exact PR #41 packet commit:

`591b66db881277fb575821e1d240e5a7274d91c3`

v2 adds only the executable audit layer:

- [audit-payloads.md](audit-payloads.md) — exact immutable evidence bodies;
- [audit-index.json](audit-index.json) — fixed post-initial evidence menus;
- [run-spec.md](run-spec.md) — deterministic recipient/audit/runtime procedure.

The recipient, not the orchestrator, maps its verification need to evidence: after the initial answer is persisted, it sees a neutral index and chooses up to two item IDs.

## Provenance

- **C13** audit payloads are controlled recipient-safe renderings of already source-reviewed historical evidence.
- **S01 / SH2** audit payloads are explicitly synthetic v2 artifacts constructed to instantiate their already-frozen synthetic execution records. They are not represented as previously existing logs.

## Scientific boundary

The independent variable remains **settlement form**:

```text
final-state only
vs full chronological trace
vs selective consequential delta
```

Audit access remains common within each fixture/condition and occurs only after the initial response.

Because the post-initial index is itself an information surface, results must distinguish:
1. initial settlement performance;
2. post-index evidence selection;
3. post-payload final judgment.

## Next gate

Do not start the 27 runs until local preflight validates:
- file/hash integrity;
- audit payload/index completeness;
- no C13 future-holdout leakage;
- model/runtime availability;
- fresh context isolation;
- no external tool escape;
- raw run persistence;
- separate scorer capability.

A preflight failure again means **0 experimental exposure should occur**.
