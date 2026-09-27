# γ-I v2 replacement context

Status: one fresh C13 final-state replacement is authorized and pending.

The [prior 27-run attempt](../gamma-i-feasibility-v2-run-2026-09-27-04/README.md)
contains 26 valid recipient records and one contaminated `C13-F-3` audit. This
directory collects one independent replacement for that cell, with the same frozen
PR #41 settlement packet and PR #42 v2 audit layer, the same model/profile and
private provider connection, and a corrected operational exact-ID parser.

The parser now reads IDs from the explicit selection block before a `Rationale:`
or `Reason:` section. It does not map free text to evidence. The
[selection-equivalence check](selection-equivalence.json) applies it offline to
all 27 saved first selections from the prior attempt: it leaves all 26 valid
selections unchanged and extracts the two IDs the affected recipient explicitly
selected. Three IDs listed in the selection block still trigger the frozen
invalid-ID response. Five boundary tests pass.

No packet, audit payload, oracle, scoring rule, or claim interpretation changed.
The invalid raw record remains preserved and excluded. The later analysis set
will name the origin of every valid record; it will not silently substitute the
replacement into the earlier attempt.
