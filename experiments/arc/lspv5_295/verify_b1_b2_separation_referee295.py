#!/usr/bin/env python3
"""Independent checks for REFEREE295 (does not import the generator)."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(message)


def main(path: str) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("calculus") != "source-axiom Resolution plus Weakening; unit inference weights":
        fail("unexpected calculus")
    sentinels = data.get("sat_sentinels", [])
    if len(sentinels) != 16:
        fail("wrong sentinel count")
    for row in sentinels:
        k = row["k"]
        if row != {"k": k, "length": 6 * k + 3, "sat": True, "witness": 1}:
            fail(f"bad sentinel row {row}")
    if not all(data.get("malformed_rejected", {}).values()):
        fail("malformed string accepted")
    if data.get("unsat_f4") != {"proof_cost": 7, "sat": False, "verified": True}:
        fail("bad F4 control")
    for row in data.get("blocking_sweep", []):
        n = row["nvars"]
        if row["source_clauses"] != 2**n:
            fail("bad source count")
        if row["proof_cost"] != 2 ** (n + 1) - 1 or not row["verified"]:
            fail("bad blocking proof count")
    env = data.get("envelope_checks", {})
    if env.get("count") != env.get("N_max") - env.get("N_min") + 1:
        fail("bad envelope count")
    if not env.get("all_dominate"):
        fail("delay did not dominate")
    for edge in (env.get("first", {}), env.get("last", {})):
        N, L = edge["N"], edge["sentinel_length"]
        if not (L <= N and L > N - 6 and edge["delay_log2"] == L * L):
            fail("bad sentinel density arithmetic")
        if edge["delay_log2"] < edge["universal_W_log2_upper"]:
            fail("bad domination arithmetic")
    print(json.dumps({
        "verified": True,
        "independent_checks": 16 + 4 + 1 + len(data["blocking_sweep"]) + 2,
        "envelope_rows_attested_by_generator": env["count"],
        "note": "asymptotic Tseitin lower bound remains literature-sourced, not finite-reproved",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: verify_b1_b2_separation_referee295.py RAW_JSON")
    main(sys.argv[1])
