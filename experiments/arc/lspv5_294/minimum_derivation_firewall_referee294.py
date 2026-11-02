#!/usr/bin/env python3
"""REFEREE294: exact finite audit of minimum derivations and trace soundness.

This is deliberately tiny.  It computes minimum unit-cost resolution-DAG
inference counts by breadth-first search over sets of derived clauses.  Source
clauses are free axioms and each new non-tautological binary resolvent costs 1.
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-02_1148_LSPV5_MIN_DERIVATION_FIREWALL_REFEREE294_raw.json"


def strict_cnf(obj):
    if not isinstance(obj, list) or not obj:
        raise ValueError("CNF must be a nonempty list")
    out = []
    for clause in obj:
        if not isinstance(clause, list) or not clause:
            raise ValueError("clause must be a nonempty list")
        if any(not isinstance(x, int) or isinstance(x, bool) or x == 0 for x in clause):
            raise ValueError("literals must be nonzero integers")
        c = frozenset(clause)
        if any(-x in c for x in c):
            raise ValueError("tautological source clause rejected by this encoding")
        out.append(c)
    return frozenset(out)


def sat_count(cnf):
    n = max(abs(x) for c in cnf for x in c)
    count = 0
    for mask in range(1 << n):
        if all(any(((mask >> (abs(x) - 1)) & 1) == (x > 0) for x in c) for c in cnf):
            count += 1
    return count


def resolvents(a, b):
    out = set()
    for x in a:
        if -x not in b:
            continue
        r = (a - {x}) | (b - {-x})
        if any(-y in r for y in r):
            continue
        out.add(frozenset(r))
    return out


def minimum_resolution_dag_stats(cnf):
    """Return exact minimum and finite BFS-search accounting."""
    start = frozenset(cnf)
    if frozenset() in start:
        return {"cost": 0, "states_popped": 0, "states_seen": 1, "peak_frontier": 1}
    q = deque([(start, 0)])
    seen = {start}
    popped = 0
    peak = 1
    while q:
        state, depth = q.popleft()
        popped += 1
        clauses = tuple(state)
        for i, a in enumerate(clauses):
            for b in clauses[i + 1 :]:
                for r in resolvents(a, b):
                    if r in state:
                        continue
                    if not r:
                        return {"cost": depth + 1, "states_popped": popped,
                                "states_seen": len(seen), "peak_frontier": peak}
                    nxt = frozenset(set(state) | {r})
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, depth + 1))
                        peak = max(peak, len(q))
    return {"cost": None, "states_popped": popped, "states_seen": len(seen),
            "peak_frontier": peak}


def minimum_resolution_dag(cnf):
    return minimum_resolution_dag_stats(cnf)["cost"]


def trace_only_accepts(machine_output):
    """Unsound candidate rule: any well-formed rejecting trace closes a proof."""
    return machine_output == "UNSAT"


def guarded_accepts(cnf):
    """Sound finite control: closure only through the declared resolution rules."""
    return minimum_resolution_dag(cnf) is not None


def main():
    u1 = strict_cnf([[1], [-1]])
    # Equality AND inequality on the same two variables.
    # Equality: (not x or y) & (x or not y)
    # Inequality: (x or y) & (not x or not y)
    f4 = strict_cnf([[-1, 2], [1, -2], [1, 2], [-1, -2]])
    sat1 = strict_cnf([[1, 2]])

    data = {
        "run_id": "LSPV5_MIN_DERIVATION_FIREWALL_REFEREE294",
        "status": "PASS",
        "model": "fixed source-axiom binary Resolution; unit weight per distinct derived clause",
        "free_optimal_sequence": True,
        "controls": {
            "u1": {"sat_count": sat_count(u1), "minimum_resolution_dag": minimum_resolution_dag(u1),
                   "offline_bfs": minimum_resolution_dag_stats(u1)},
            "f4_equality_and_inequality": {
                "sat_count": sat_count(f4),
                "minimum_resolution_dag": minimum_resolution_dag(f4),
                "offline_bfs": minimum_resolution_dag_stats(f4),
                "native_xor_addition_cost": 1,
                "cnf_to_xor_extraction_plus_addition_cost": 3,
            },
            "sat1": {
                "sat_count": sat_count(sat1),
                "minimum_resolution_dag": minimum_resolution_dag(sat1),
                "offline_bfs": minimum_resolution_dag_stats(sat1),
                "reject_all_trace_claims_unsat": True,
                "trace_only_rule_accepts": trace_only_accepts("UNSAT"),
                "guarded_resolution_accepts": guarded_accepts(sat1),
            },
            "malformed_literal_zero_rejected": False,
        },
        "falsifiers": {
            "trace_only_rule": "UNSOUND: accepts a one-step reject-all trace on SAT1",
            "instance_specific_false_axiom": "INVALID MODEL: changes R after seeing the instance",
            "semantic_jump": "UNSOUND unless backed by an independently checkable fixed rule",
            "xor_switch": "VALID ESCAPE: F4 falls from Resolution cost 3 to native-XOR cost 1",
        },
        "claim_scope": "finite exact optima and a soundness counterexample; no asymptotic SAT lower bound",
        "p_vs_np": "OPEN",
    }
    try:
        strict_cnf([[0]])
    except ValueError:
        data["controls"]["malformed_literal_zero_rejected"] = True

    assert data["controls"]["u1"]["sat_count"] == 0
    assert data["controls"]["u1"]["minimum_resolution_dag"] == 1
    assert data["controls"]["f4_equality_and_inequality"]["sat_count"] == 0
    assert data["controls"]["f4_equality_and_inequality"]["minimum_resolution_dag"] == 3
    assert data["controls"]["sat1"]["sat_count"] == 3
    assert data["controls"]["sat1"]["minimum_resolution_dag"] is None
    assert data["controls"]["sat1"]["trace_only_rule_accepts"] is True
    assert data["controls"]["sat1"]["guarded_resolution_accepts"] is False
    assert data["controls"]["malformed_literal_zero_rejected"] is True

    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
