#!/usr/bin/env python3
"""Independent audit for PORTFOLIO-PRISM-FIREWALL101.

Constructs a connected signed exact-(2,2) proper 3-CNF from a prism graph.
It verifies the Role-1 complementary-pair defect, the Role-2 greedy paired-
support defect, and an explicit linear-time satisfying assignment.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict


SEED = 202610232348


def prism(q: int):
    vertices = [(i, s) for s in range(2) for i in range(q)]
    edges = []
    for s in range(2):
        for i in range(q):
            edges.append(tuple(sorted(((i, s), ((i + 1) % q, s)))))
    for i in range(q):
        edges.append(((i, 0), (i, 1)))
    assert len(set(edges)) == 3 * q
    return vertices, edges


def build(q: int):
    vertices, edges = prism(q)
    x = {e: i + 1 for i, e in enumerate(edges)}
    y0 = len(edges) + 1
    clauses = []

    incident = defaultdict(list)
    for e in edges:
        u, v = e
        incident[u].append(x[e])
        incident[v].append(-x[e])
    for v in vertices:
        clauses.append(tuple(sorted(incident[v], key=abs)))

    for i, e in enumerate(edges):
        yi = y0 + i
        yn = y0 + ((i + 1) % len(edges))
        xe = x[e]
        clauses.append((yi, -yn, xe))
        clauses.append((yi, -yn, -xe))

    assignment = {}
    # Orient each ring cyclically; every vertex receives one ring edge.
    for s in range(2):
        for i in range(q):
            u = (i, s)
            v = ((i + 1) % q, s)
            e = tuple(sorted((u, v)))
            head = v
            lower, _ = e
            assignment[x[e]] = head == lower
    for i in range(q):
        e = ((i, 0), (i, 1))
        assignment[x[e]] = False
    for i in range(len(edges)):
        assignment[y0 + i] = False
    return vertices, edges, clauses, assignment


def sat_clause(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def complementary_pair_defect(clauses):
    used = set()
    pairs = 0
    for i, a in enumerate(clauses):
        if i in used:
            continue
        aset = set(a)
        for j in range(i + 1, len(clauses)):
            if j in used:
                continue
            bset = set(clauses[j])
            common = aset & bset
            if len(common) == 2:
                ra = list(aset - common)
                rb = list(bset - common)
                if len(ra) == len(rb) == 1 and ra[0] == -rb[0]:
                    used.add(i)
                    used.add(j)
                    pairs += 1
                    break
    return len(clauses) - 2 * pairs, pairs


def role2_greedy_defect(clauses):
    pos = defaultdict(list)
    neg = defaultdict(list)
    for idx, clause in enumerate(clauses):
        support = tuple(sorted(abs(x) for x in clause))
        if all(x > 0 for x in clause):
            pos[support].append(idx)
        elif all(x < 0 for x in clause):
            neg[support].append(idx)
    paired = 0
    variable_support_count = Counter()
    for support in sorted(set(pos) & set(neg)):
        for _ in range(min(len(pos[support]), len(neg[support]))):
            if all(variable_support_count[v] <= 1 for v in support):
                paired += 1
                for v in support:
                    variable_support_count[v] += 1
    return len(clauses) - 2 * paired, paired


def check_instance(q: int):
    vertices, edges, clauses, assignment = build(q)
    n = 2 * len(edges)
    assert len(vertices) == 2 * q
    assert len(edges) == 3 * q
    assert len(clauses) == 8 * q
    assert len(set(clauses)) == len(clauses)
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
    counts = Counter(clauses_lit for c in clauses for clauses_lit in c)
    assert all(counts[v] == 2 and counts[-v] == 2 for v in range(1, n + 1))
    assert all(sat_clause(c, assignment) for c in clauses)
    delta, complement_pairs = complementary_pair_defect(clauses)
    t, role2_pairs = role2_greedy_defect(clauses)
    assert complement_pairs == 3 * q
    assert delta == 2 * q
    assert role2_pairs == 0
    assert t == 8 * q
    return {
        "q": q,
        "variables": n,
        "clauses": len(clauses),
        "role1_delta": delta,
        "role1_exponent_floor_5delta_over_8": (5 * delta) // 8,
        "role2_t": t,
        "role2_branch_bound": f"3^{t}",
        "witness_verified": True,
    }


def controls():
    sat = [(1, 2, 3)]
    unsat = [tuple((a if mask & (1 << i) else -a) for i, a in enumerate((1, 2, 3)))
             for mask in range(8)]

    def brute(formula):
        for mask in range(8):
            a = {i + 1: bool(mask & (1 << i)) for i in range(3)}
            if all(sat_clause(c, a) for c in formula):
                return True
        return False

    assert brute(sat)
    assert not brute(unsat)
    return {"sat_control": True, "unsat_control": True}


def main():
    rows = [check_instance(q) for q in range(3, 65)]
    payload = {
        "label": "COMPUTATIONAL",
        "seed": SEED,
        "instances": len(rows),
        "checks": 62 * 11 + 2,
        "failures": 0,
        "controls": controls(),
        "first": rows[0],
        "last": rows[-1],
        "rows": rows,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["sha256_without_sha_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
