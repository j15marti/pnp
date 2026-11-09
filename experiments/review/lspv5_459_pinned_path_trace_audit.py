#!/usr/bin/env python3
"""Independent source/Resolution audit for peer node P2-L3-532."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "experiments/arc/lspv3_532_pinned_ternary_path_linear.cjs"


def edge(k: int, vertex: int):
    if k == 1:
        return [(0, 1), (1, 1), (2, 1)]
    if vertex == 0:
        return [(0, 1), (1, 1), (k + 2, 1)]
    if vertex == k - 1:
        return [(k + 2 + vertex - 1, -1), (k, 1), (k + 1, 1)]
    return [(k + 2 + vertex - 1, -1), (vertex + 1, 1), (k + 2 + vertex, 1)]


def lit(edge_id: int, residue: int) -> int:
    return 3 * edge_id + residue + 1


def expected_source(k: int):
    out = []
    for e in range(2 * k + 1):
        out.append(([lit(e, r) for r in range(3)], "ALO"))
    for v in range(k):
        inc = edge(k, v)
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    vals = (a, b, c)
                    if sum(s * x for (_, s), x in zip(inc, vals)) % 3:
                        out.append(([-lit(e, x) for (e, _), x in zip(inc, vals)], f"wrong{v}"))
    base = 3 * (2 * k + 1)
    for j in range(k + 2):
        a = 1 if j == k + 1 else 0
        p, u, v = lit(j, a), base + 2 * j + 1, base + 2 * j + 2
        out.extend([
            ([p, u, v], "pin"), ([p, u, -v], "pin"),
            ([p, -u, v], "pin"), ([p, -u, -v], "pin"),
        ])
    return out


def canonical(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))


def verify(packet, exact_source=True):
    k = packet["k"]
    source, rules = packet["source"], packet["rules"]
    assert packet["variables"] == 8 * k + 7
    assert len(source) == 24 * k + 9
    assert len(rules) == 9 * k + 3
    clauses, ancestors, depths = {}, {}, {}
    expected = expected_source(k)
    for index, item in enumerate(source, 1):
        assert item["id"] == index
        c = item["c"]
        assert len(c) == 3 and len(set(map(abs, c))) == 3
        assert not any(-x in c for x in c)
        if exact_source:
            assert (c, item["tag"]) == expected[index - 1]
        clauses[index] = canonical(c)
        ancestors[index] = {index}
        depths[index] = 0
    for offset, rule in enumerate(rules, 1):
        rid = len(source) + offset
        assert rule["id"] == rid
        a, b, pivot = rule["a"], rule["b"], rule["p"]
        assert a < rid and b < rid and a in clauses and b in clauses
        A, B = set(clauses[a]), set(clauses[b])
        assert pivot in A and -pivot in B
        result = (A - {pivot}) | (B - {-pivot})
        assert not any(-x in result for x in result)
        assert canonical(rule["c"]) == canonical(result)
        clauses[rid] = canonical(result)
        ancestors[rid] = ancestors[a] | ancestors[b]
        depths[rid] = 1 + max(depths[a], depths[b])
    assert packet["empty"] == rules[-1]["id"]
    assert clauses[packet["empty"]] == ()
    assert len(ancestors[packet["empty"]]) == 7 * k + 6
    assert depths[packet["empty"]] == 4 * k + 1
    return {
        "k": k,
        "variables": packet["variables"],
        "source_clauses": len(source),
        "paid_resolution": len(rules),
        "premise_references": 2 * len(rules),
        "span": depths[packet["empty"]],
        "source_ancestors": len(ancestors[packet["empty"]]),
    }


def run_peer(k: int):
    raw = subprocess.check_output(["node", str(GEN), str(k)], text=True)
    return json.loads(raw)


def expect_reject(packet, mutator):
    broken = copy.deepcopy(packet)
    mutator(broken)
    try:
        verify(broken)
    except (AssertionError, KeyError, IndexError, TypeError):
        return True
    return False


def dpll(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    while True:
        reduced, units = [], []
        for clause in clauses:
            if any(assignment.get(abs(x)) == (x > 0) for x in clause):
                continue
            rest = [x for x in clause if abs(x) not in assignment]
            if not rest:
                return None
            if len(rest) == 1:
                units.append(rest[0])
            reduced.append(rest)
        if not units:
            break
        for u in units:
            var, value = abs(u), u > 0
            if var in assignment and assignment[var] != value:
                return None
            assignment[var] = value
        clauses = reduced
    if not clauses:
        return assignment
    variable = abs(min(clauses, key=len)[0])
    for value in (False, True):
        result = dpll(clauses, {**assignment, variable: value})
        if result is not None:
            return result
    return None


def deletion_witness(packet):
    k = packet["k"]
    # First facet of final boundary pin: ALO + wrong rows precede pin gadgets.
    final_first = (2 * k + 1) + 18 * k + 4 * (k + 1) + 1
    clauses = [s["c"] for s in packet["source"] if s["id"] != final_first]
    # Independent closed-form witness: every edge takes residue 0; every pin
    # auxiliary is false.  With the first final-pin facet removed, all three
    # remaining facets of that gadget are satisfied although its requested
    # residue-1 indicator is false.
    witness = {}
    for e in range(2 * k + 1):
        for residue in range(3):
            witness[lit(e, residue)] = residue == 0
    base = 3 * (2 * k + 1)
    for j in range(k + 2):
        witness[base + 2 * j + 1] = False
        witness[base + 2 * j + 2] = False
    assert all(any(witness[abs(x)] == (x > 0) for x in c) for c in clauses)
    return final_first


def main():
    cases, mutation_checks, deleted = [], 0, []
    for k in (1, 2, 3, 4, 5, 8, 12):
        packet = run_peer(k)
        cases.append(verify(packet))
        deleted.append({"k": k, "deleted_source_id": deletion_witness(packet)})
        mutations = [
            lambda p: p["rules"][0].__setitem__("p", -p["rules"][0]["p"]),
            lambda p: p["rules"][0].__setitem__("a", p["rules"][0]["id"]),
            lambda p: p["rules"][-1].__setitem__("c", [1]),
            lambda p: p["source"][0]["c"].__setitem__(0, -p["source"][0]["c"][0]),
            lambda p: p.__setitem__("empty", p["empty"] - 1),
            lambda p: p["source"][0].__setitem__("id", 2),
        ]
        for mutation in mutations:
            assert expect_reject(packet, mutation)
            mutation_checks += 1
    result = {
        "status": "PASS",
        "peer_blob": "1ffb5122a29a61cf98a1e158162dda055355a560",
        "cases": cases,
        "corruptions_rejected": mutation_checks,
        "deletion_witnesses": deleted,
        "scope": "ordinary Resolution upper bound; not a minimum or mixed-calculus lower bound",
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
