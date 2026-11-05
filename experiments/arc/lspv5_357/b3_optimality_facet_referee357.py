#!/usr/bin/env python3
"""REFEREE357 finite controls for B3 proof search and DEF facet slots.

This is a finite exhaustive test, not an asymptotic theorem.  It checks:
  * all 16 ordered binary Boolean gates, including swapped and aliased inputs;
  * exact truth-table facet slots;
  * a two-paid-node selector/aggregate grammar divergence;
  * all 256 CNFs over the 8 non-tautological unit/binary clauses on x,y;
  * resolution proof search and replay for every UNSAT member.
"""

from __future__ import annotations

import json
from collections import deque


def gate(mask: int, a: int, b: int) -> int:
    return (mask >> (2 * a + b)) & 1


def facet(mask: int, a: int, b: int, left: int, right: int, out: int):
    """Return the three signed literals for one ordered false-row clause.

    Variables are positive integers.  A signed literal l is true when its
    variable has Boolean value 1 iff l>0.
    """
    q = gate(mask, a, b)
    return ((left if a == 0 else -left),
            (right if b == 0 else -right),
            (out if q == 1 else -out))


def lit_value(lit: int, values: dict[int, int]) -> bool:
    return bool(values[abs(lit)]) == (lit > 0)


def normalized_clause(lits):
    s = frozenset(lits)
    if any(-l in s for l in s):
        return None  # tautological slot remains addressable, but clause is true
    return s


def test_gate_facets():
    checks = 0
    cases = 0
    modes = ((1, 2, "distinct"), (2, 1, "swapped"), (1, 1, "aliased"))
    for mask in range(16):
        for left, right, _ in modes:
            for x in (0, 1):
                for y in (0, 1):
                    inputs = {1: x, 2: y}
                    expected = gate(mask, inputs[left], inputs[right])
                    for z in (0, 1):
                        values = {1: x, 2: y, 3: z}
                        all_facets = []
                        for a in (0, 1):
                            for b in (0, 1):
                                clause = facet(mask, a, b, left, right, 3)
                                all_facets.append(any(lit_value(l, values) for l in clause))
                                checks += 1
                        assert all(all_facets) == (z == expected)
                        cases += 1
    return {"gate_records": 16 * len(modes), "valuation_cases": cases,
            "facet_evaluations": checks}


def selector_divergence():
    # mask 0b0011 is NOT of the first ordered input for index 2*a+b.
    mask = 0b0011
    row = (1, 1)
    raw = facet(mask, row[0], row[1], 1, 1, 2)
    clause = normalized_clause(raw)
    assert clause == frozenset((-1, -2))
    source = frozenset((1,))
    resolvent = frozenset((l for l in source | clause if abs(l) != 1))
    assert resolvent == frozenset((-2,))
    selector_accepts = True  # premise is explicit typed slot (def-id,1,1)
    aggregate_accepts = False  # DEF record is not itself a clause premise
    return {
        "source": [1],
        "def": {"id": 1, "out": 2, "gate_mask": mask,
                "ordered_inputs": [1, 1]},
        "selected_slot": [1, 1],
        "raw_facet": list(raw),
        "normalized_facet": sorted(clause),
        "resolvent": sorted(resolvent),
        "paid_nodes": 2,
        "selector_completion_accepts": selector_accepts,
        "aggregate_completion_accepts": aggregate_accepts,
    }


BASE = (
    frozenset((1,)), frozenset((-1,)),
    frozenset((2,)), frozenset((-2,)),
    frozenset((1, 2)), frozenset((1, -2)),
    frozenset((-1, 2)), frozenset((-1, -2)),
)


def clause_true(clause, x, y):
    values = {1: x, 2: y}
    return any(lit_value(l, values) for l in clause)


def resolution_search(source):
    known = set(source)
    parent = {}
    agenda = deque(source)
    while agenda:
        a = agenda.popleft()
        snapshot = list(known)
        for b in snapshot:
            for pivot in (1, 2):
                if pivot in a and -pivot in b:
                    r = frozenset((a - {pivot}) | (b - {-pivot}))
                elif -pivot in a and pivot in b:
                    r = frozenset((a - {-pivot}) | (b - {pivot}))
                else:
                    continue
                if any(-l in r for l in r):
                    continue
                if r not in known:
                    known.add(r)
                    parent[r] = (a, b, pivot)
                    agenda.append(r)
    if frozenset() not in known:
        return None, parent
    return frozenset(), parent


def replay_empty(source, parent):
    memo = set(source)
    visiting = set()

    def rec(c):
        if c in memo:
            return
        assert c not in visiting and c in parent
        visiting.add(c)
        a, b, pivot = parent[c]
        rec(a); rec(b)
        candidates = []
        if pivot in a and -pivot in b:
            candidates.append(frozenset((a - {pivot}) | (b - {-pivot})))
        if -pivot in a and pivot in b:
            candidates.append(frozenset((a - {-pivot}) | (b - {pivot})))
        assert c in candidates and not any(-l in c for l in c)
        visiting.remove(c)
        memo.add(c)

    rec(frozenset())
    return len(memo - set(source))


def test_two_variable_universe():
    sat = unsat = proofs = total_nodes = 0
    max_nodes = 0
    for bits in range(256):
        source = tuple(BASE[i] for i in range(8) if (bits >> i) & 1)
        is_sat = any(all(clause_true(c, x, y) for c in source)
                     for x in (0, 1) for y in (0, 1))
        empty, parents = resolution_search(source)
        if is_sat:
            sat += 1
            assert empty is None
        else:
            unsat += 1
            assert empty == frozenset()
            nodes = replay_empty(source, parents)
            proofs += 1
            total_nodes += nodes
            max_nodes = max(max_nodes, nodes)
    assert (sat, unsat) == (95, 161)
    return {"formulae": 256, "sat": sat, "unsat": unsat,
            "resolution_proofs_replayed": proofs,
            "total_derived_nodes_replayed": total_nodes,
            "max_derived_nodes_one_proof": max_nodes}


def malformed_controls():
    rejected = 0
    fixtures = [
        {"mask": 16, "inputs": [1, 1], "out": 2},
        {"mask": 3, "inputs": [1], "out": 2},
        {"mask": 3, "inputs": [1, 1], "out": 1},  # not fresh
        {"mask": 3, "inputs": [1, 1], "out": 2, "slot": [2, 0]},
        {"mask": 3, "inputs": [1, 1], "out": 2, "slot": [1]},
    ]
    for f in fixtures:
        ok = (isinstance(f.get("mask"), int) and 0 <= f["mask"] < 16 and
              len(f.get("inputs", [])) == 2 and
              f.get("out") not in f.get("inputs", []))
        if "slot" in f:
            ok = ok and len(f["slot"]) == 2 and all(v in (0, 1) for v in f["slot"])
        assert not ok
        rejected += 1
    return {"fixtures": len(fixtures), "rejected": rejected}


def main():
    result = {
        "run": "LSPV5_REFEREE357",
        "status": {"finite_tests": "COMPUTATIONAL",
                   "asymptotic_claim": "NONE"},
        "ordered_gate_facets": test_gate_facets(),
        "minimal_selector_divergence": selector_divergence(),
        "two_variable_resolution_search": test_two_variable_universe(),
        "malformed_controls": malformed_controls(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
