"""Verify the source-review ledger without changing historical sources."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(["git", "-C", repo, *args])


def read_source(source):
    if source["kind"] == "file":
        return Path(source["path"]).read_bytes()
    if source["kind"] == "git_blob":
        spec = source["commit"] + ":" + source["path"]
        assert git(source["repository"], "rev-parse", spec).decode().strip() == source["blob_oid"]
        return git(source["repository"], "show", spec)
    assert source["kind"] == "sqlite_value"
    # URI read-only mode and SELECT-only access; no snapshot of the whole DB.
    con = sqlite3.connect(Path(source["path"]).as_uri() + "?mode=ro", uri=True)
    try:
        row = con.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (source["key"],)).fetchone()
        assert row is not None, source["id"]
        return row[0].encode() if isinstance(row[0], str) else row[0]
    finally:
        con.close()


def normalize(data):
    return data.decode("utf-8-sig").replace("\r\n", "\n").rstrip("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / "sources.json").read_text())
    ledger = json.loads((base / "fact-ledger.json").read_text())
    sources = {s["id"]: s for s in manifest["sources"]}
    assert len(sources) == len(manifest["sources"])
    cases = ledger["decisions"]
    assert len({c["case_id"] for c in cases}) == 3
    for case in cases:
        assert case["decision"] in {"include", "defer", "exclude"}
        assert len(case["gate"]) == 7
        assert set(case["source_snapshot"]) <= sources.keys()
        refs = [r for s in case["S0"] for r in s["evidence_that_shared"]]
        refs += [r for e in case["execution_events"] for r in e["source_addresses"]]
        for ref in refs:
            match = re.fullmatch(r"([A-Z]\d+)(?::(\d+)(?:-(\d+))?)?", ref)
            assert match and match[1] in sources, ref
            if match[2]:
                assert 1 <= int(match[2]) <= int(match[3] or match[2]) <= sources[match[1]]["line_count"], ref
        for event in case["execution_events"]:
            assert event["classification"]["current_decision"] in {"D_now+", "D_now0", "ambiguous"}
            assert event["classification"]["L"] in {"none", "low", "medium", "high", "unknown"}
    gate = ledger["replay_gate"]
    assert gate["included_source_review_cases"] == sum(c["decision"] == "include" for c in cases)
    assert gate["may_run"] is False and gate["frozen_rendered_fixtures"] == 0
    if args.metadata_only:
        print("PASS: ledger structure, references, classifications and replay gate; source bytes NOT checked.")
        return
    data = {}
    for id, source in sources.items():
        data[id] = read_source(source)
        assert digest(data[id]) == source["sha256"], id
    for pair in manifest["normalization_checks"]:
        assert normalize(data[pair["left"]]) == normalize(data[pair["right"]]), pair
    search = manifest["static_search"]
    actual = git(search["repository"], "grep", "-n", "-E", "getCachedBody|HSQ_JOB_APPLICATION", search["commit"][:7], "--", "*.java").decode()
    assert actual == search["result"]
    print(f"PASS: {len(data)} source hashes, blob identities, normalized snapshot matches, historical search and three case ledgers.")


if __name__ == "__main__":
    main()
