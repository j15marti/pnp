#!/usr/bin/env python3
"""LSPV-5/417: duplicate JSON-member audit of the recovered /341 checker."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"
OUT = ROOT / "results/raw/review/2026-11-07_1348_LSPV5_DUPLICATE_JSON_MEMBER417.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate member: {key}")
        out[key] = value
    return out


def strict_accepts(raw: str) -> bool:
    try:
        json.loads(raw, object_pairs_hook=strict_pairs)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def replace_once(raw: str, old: str, new: str) -> str:
    if raw.count(old) != 1:
        raise AssertionError(f"target count {raw.count(old)} for {old!r}")
    return raw.replace(old, new, 1)


def duplicate_member(base, fixture_index, path, first, second):
    obj = json.loads(json.dumps(base))
    cur = obj["fixtures"][fixture_index]
    for step in path[:-1]:
        cur = cur[step]
    key = path[-1]
    cur[key] = "__LSPV5_417_SENTINEL__"
    raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    old = json.dumps(key) + ":" + json.dumps("__LSPV5_417_SENTINEL__")
    new = (
        json.dumps(key) + ":" + json.dumps(first, separators=(",", ":"))
        + "," + json.dumps(key) + ":" + json.dumps(second, separators=(",", ":"))
    )
    return replace_once(raw, old, new)


def run_checker(raw: str):
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as fh:
        fh.write(raw)
        name = fh.name
    try:
        cp = subprocess.run(
            ["node", str(CHECKER), name], capture_output=True, text=True, timeout=30
        )
        return {
            "accepted": cp.returncode == 0,
            "returncode": cp.returncode,
            "stdout_sha256": sha256(cp.stdout.encode()),
            "stderr_first_line": cp.stderr.splitlines()[0] if cp.stderr else "",
        }
    finally:
        Path(name).unlink(missing_ok=True)


def main():
    base = json.loads(PACKET.read_text())
    baseline_raw = json.dumps(base, separators=(",", ":"), ensure_ascii=False)
    baseline = run_checker(baseline_raw)
    if not baseline["accepted"]:
        raise AssertionError("baseline rejected")

    f = base["fixtures"][0]
    specs = [
        ("source_id_forged_then_canonical", ["clauses", 0, "id"], "forged-source", f["clauses"][0]["id"], True),
        ("source_id_canonical_then_forged", ["clauses", 0, "id"], f["clauses"][0]["id"], "forged-source", False),
        ("derived_id_forged_then_canonical", ["proof", 0, "id"], "forged-derived", f["proof"][0]["id"], True),
        ("derived_id_canonical_then_forged", ["proof", 0, "id"], f["proof"][0]["id"], "forged-derived", False),
        ("parents_forged_then_canonical", ["proof", 0, "parents"], ["forged-a", "forged-b"], f["proof"][0]["parents"], True),
        ("parents_canonical_then_forged", ["proof", 0, "parents"], f["proof"][0]["parents"], ["forged-a", "forged-b"], False),
        ("source_literals_forged_then_canonical", ["clauses", 0, "literals"], [999], f["clauses"][0]["literals"], True),
        ("source_literals_canonical_then_forged", ["clauses", 0, "literals"], f["clauses"][0]["literals"], [999], False),
        ("kind_forged_then_canonical", ["proof", 0, "kind"], "affine", f["proof"][0]["kind"], True),
        ("kind_canonical_then_forged", ["proof", 0, "kind"], f["proof"][0]["kind"], "affine", False),
    ]
    affine_i = next(i for i, p in enumerate(f["proof"]) if p["kind"] == "affine")
    mask = f["proof"][affine_i]["row"]["mask"]
    specs += [
        ("affine_mask_forged_then_canonical", ["proof", affine_i, "row", "mask"], "not-a-bigint", mask, True),
        ("affine_mask_canonical_then_forged", ["proof", affine_i, "row", "mask"], mask, "not-a-bigint", False),
    ]

    cases = []
    for name, path, first, second, expected in specs:
        raw = duplicate_member(base, 0, path, first, second)
        result = run_checker(raw)
        result.update({
            "name": name,
            "path": path,
            "expected_checker_accept": expected,
            "strict_unique_parser_accept": strict_accepts(raw),
            "raw_sha256": sha256(raw.encode()),
            "raw_bytes": len(raw.encode()),
            "same_stdout_as_baseline": result["stdout_sha256"] == baseline["stdout_sha256"],
        })
        if result["accepted"] != expected:
            raise AssertionError(f"unexpected checker result: {result}")
        if result["strict_unique_parser_accept"]:
            raise AssertionError(f"strict parser accepted duplicate: {name}")
        if expected and not result["same_stdout_as_baseline"]:
            raise AssertionError(f"accepted mutation changed stdout: {name}")
        cases.append(result)

    record = {
        "experiment": "LSPV-5/417 duplicate JSON proof-member audit",
        "timestamp_pst": "2026-11-07 13:48 PST",
        "status": "COMPUTATIONAL/PROVED-RESTRICTED",
        "scope": "recovered SOURCE/AND3/XOR checker only",
        "packet": str(PACKET.relative_to(ROOT)),
        "packet_sha256": sha256(PACKET.read_bytes()),
        "checker": str(CHECKER.relative_to(ROOT)),
        "checker_sha256": sha256(CHECKER.read_bytes()),
        "baseline": baseline,
        "case_count": len(cases),
        "accepted_count": sum(c["accepted"] for c in cases),
        "strict_rejection_count": sum(not c["strict_unique_parser_accept"] for c in cases),
        "cases": cases,
        "limitations": [
            "No satisfiable source or shorter refutation is produced.",
            "RES, LOCAL-CONVERT, DEF facets, branching and full historical grammar remain unauthenticated.",
            "Finite parser behavior is not a proof-size or all-algorithm lower bound.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "cases": len(cases),
        "accepted": record["accepted_count"],
        "strict_rejected": record["strict_rejection_count"],
        "baseline_stdout_sha256": baseline["stdout_sha256"],
        "output": str(OUT.relative_to(ROOT)),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
