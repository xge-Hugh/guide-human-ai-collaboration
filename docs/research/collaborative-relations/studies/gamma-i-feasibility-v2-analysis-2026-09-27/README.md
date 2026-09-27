# γ-I v2 mechanics-feasibility analysis set

Status: **complete mechanics-feasibility run** — 27 valid recipient records,
54 valid independent scorer judgments, and [results](results.md). The larger
confirmatory γ-I gate is not met under this frozen packet/scorer combination.

The [record provenance](record-provenance.json) maps every analysis run to its
immutable raw source: 26 valid records from the [full attempt](../gamma-i-feasibility-v2-run-2026-09-27-04/README.md)
and one fresh C13 final-state replacement from the [replacement attempt](../gamma-i-feasibility-v2-run-2026-09-27-05/README.md).
The contaminated original C13-F-3 record is preserved in the full attempt and
excluded before scoring or treatment comparison. It received false invalid-ID
feedback because its rationale mentioned unchosen alternatives. The repaired
operational parser leaves all 26 other selections unchanged, as the
[selection-equivalence record](../gamma-i-feasibility-v2-run-2026-09-27-05/selection-equivalence.json)
shows. This is an operational repair; the frozen packet, audit payloads, oracles,
scoring rules, and claim interpretation remain unchanged.

[Recipient integrity](recipient-integrity.json) verifies all 27 initial packets,
stateless request boundaries, audit index timing, at most two selected IDs, exact
frozen payload return, completed final responses, and the reported model. Every
copied file byte-matches its original source. No invalid-ID correction remains
in the analysis set. The frozen manifest is
`8c8fabf27d1cf246f1612dd20c4251ec6d89ceffa1e2138db6a4bb904e4086a3`.

The prior independent packet reviews and S01 pre-exposure adjudication remain
linked through [runtime-preflight.json](runtime-preflight.json). D contains extra
consequence linkage and verification guidance compared with T. Any D advantage
therefore cannot be attributed to fact selection alone. This is an apparatus
feasibility run, with C13 corpus-derived evidence reported separately from S01
and SH2 synthetic evidence. There is no single overall winner score.

The analysis set was scored by separate label-blind Qwen contexts, two valid
independent judgments per recipient record. One complete malformed scorer
response and its independent valid retry are both preserved. Scorer output
remains separate from raw recipient responses, and all model requests and
responses are preserved. The [descriptive summary](descriptive-summary.json)
and [final integrity record](final-integrity.json) support the report.
