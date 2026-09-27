# γ-I v2 mechanics replay — fresh execution attempt

Status: recipient execution complete with one contaminated audit-selection record;
26 records are usable pending replacement and scoring. See [attempt-status.json](attempt-status.json).

This attempt uses the unchanged PR #41 settlement surfaces and scoring plan at
`591b66db881277fb575821e1d240e5a7274d91c3` and the PR #42 v2 audit layer.
The manifest digest is `8c8fabf27d1cf246f1612dd20c4251ec6d89ceffa1e2138db6a4bb904e4086a3`.

The [previous attempt](../gamma-i-feasibility-v2-run-2026-09-27-03/README.md)
exposed two C13 contexts and is excluded from this run matrix. Its first complete
record received an incorrect invalid-ID response after the recipient repeated two
valid selected IDs in its explanation; its second record was interrupted before
the final response. Neither is scored or pooled. This operational parser bug was
fixed before the first recipient in this fresh attempt. It now counts distinct
literal IDs in first-seen order, with no semantic routing of free text. The exact
saved first selection from the excluded attempt resolves to its two originally
selected IDs. Five boundary tests pass.

The earlier three independent packet reviews and provider checks apply to the
same frozen content, route, and model configuration. Their files and hashes are
linked in [runtime-preflight.json](runtime-preflight.json). The S01 reviewer flag
and pre-exposure adjudication remain visible. The frozen scoring plan forbids a
pure fact-selection reading of any D advantage because D provides additional
consequence linkage and verification guidance. The run is mechanics feasibility;
C13 is reported separately from S01 and SH2.

This attempt is bound to the chosen profile, private provider connection
fingerprint, execution source hash, and exact frozen packet hashes. No credential
or endpoint value is saved in the run artifacts. The user explicitly authorized
external delivery of frozen packets, audit payloads, oracles, and scoring material
for this γ-I run.

## Post-run audit check

All 27 recipient records were saved and the frozen payload/boundary integrity
check passed. One C13 final-state record (`C13-F-3`) had an operational audit
selection error. Its recipient listed `C13-R1` and `C13-R5` under “Select,” then
mentioned three other IDs under “Rationale” as alternatives it would not prioritize.
The parser counted all five literal IDs and incorrectly sent the frozen invalid-ID
response. That record's final judgment is contaminated and it is excluded before
scoring or treatment comparison. The raw record remains intact.

The corrected parser reads exact IDs from the explicit selection block preceding
the rationale. Offline replay of every saved selection shows that it would return
the same IDs for the 26 valid records and the intended `C13-R1`/`C13-R5` for the
excluded one. A test confirms that three IDs actually listed as selected are
still rejected. The treatment packets, oracle, scoring rules, and claim boundaries
remain unchanged. One fresh C13 final-state context is needed to restore the
three-valid-runs-per-cell matrix. Any later combined analysis must disclose its
origin and keep the excluded record out of the scores.
