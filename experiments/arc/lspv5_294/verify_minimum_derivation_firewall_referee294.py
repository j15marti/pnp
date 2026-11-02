#!/usr/bin/env python3
"""Independent, no-producer-import verifier for REFEREE294."""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-02_1148_LSPV5_MIN_DERIVATION_FIREWALL_REFEREE294_raw.json"


def truth_count(clauses, n):
    return sum(
        all(any(((m >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in clauses)
        for m in range(1 << n)
    )


def all_resolvents(a, b):
    ans = set()
    for l in a:
        if -l in b:
            r = (a - {l}) | (b - {-l})
            if not any(-x in r for x in r):
                ans.add(frozenset(r))
    return ans


def exact_min(clauses):
    start = frozenset(map(frozenset, clauses))
    frontier = {start}
    seen = {start}
    for cost in range(0, 16):
        if any(frozenset() in s for s in frontier):
            return cost
        nxt = set()
        for state in frontier:
            for a, b in combinations(state, 2):
                for r in all_resolvents(a, b):
                    if r not in state:
                        t = frozenset(set(state) | {r})
                        if t not in seen:
                            seen.add(t)
                            nxt.add(t)
        frontier = nxt
        seen |= nxt
        if not frontier:
            return None
    raise AssertionError("tiny control unexpectedly exceeded verifier bound")


def main():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    u1 = [{1}, {-1}]
    f4 = [{-1, 2}, {1, -2}, {1, 2}, {-1, -2}]
    sat1 = [{1, 2}]
    checks = {
        "raw_status": raw["status"] == "PASS",
        "u1_unsat": truth_count(u1, 1) == 0,
        "u1_min_1": exact_min(u1) == 1,
        "f4_unsat": truth_count(f4, 2) == 0,
        "f4_min_3": exact_min(f4) == 3,
        "sat1_three_models": truth_count(sat1, 2) == 3,
        "sat1_no_resolution_refutation": exact_min(sat1) is None,
        "trace_rule_accepts_sat_control": raw["controls"]["sat1"]["trace_only_rule_accepts"] is True,
        "guard_rejects_sat_control": raw["controls"]["sat1"]["guarded_resolution_accepts"] is False,
        "malformed_rejected": raw["controls"]["malformed_literal_zero_rejected"] is True,
        "p_vs_np_open": raw["p_vs_np"] == "OPEN",
    }
    assert all(checks.values()), checks
    print(json.dumps({"status": "PASS", "checks": checks, "assertion_groups": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
