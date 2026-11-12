#!/usr/bin/env python3
"""Verify the scoped three-anchor obstruction, without a SAT-hardness claim.

The family targets the frozen closure-polynomial representation and the search
for vertex separators of size at most two. It has explicit satisfying witnesses.
"""
from __future__ import annotations

import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from closure_parity import solve_2cnf_affine, solve_horn_affine


def source(m):
    n = 3 * m + 3
    anchors = tuple(range(3 * m + 1, n + 1))
    triples = [tuple(range(3 * j + 1, 3 * j + 4)) for j in range(m)]
    clauses = []
    for triple in triples:
        clauses.extend((-x, -y) for x, y in combinations(triple, 2))
        clauses.extend((-x, z) for x in triple for z in anchors)
    masks = [sum(1 << (x - 1) for x in triple) for triple in triples]
    return n, anchors, triples, clauses, masks


def check_witness(n, clauses, rows, assignment):
    assert 0 <= assignment < 2 ** n
    assert all(any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)
    assert all(sum(((assignment >> j) & 1) * ((mask >> j) & 1)
                   for j in range(n)) % 2 == rhs for mask, rhs in rows)


def graph(n, clauses, rows):
    neighbors = [set() for _ in range(n)]
    scopes = [set(abs(lit) - 1 for lit in clause) for clause in clauses]
    scopes += [{j for j in range(n) if (mask >> j) & 1} for mask, _ in rows]
    for scope in scopes:
        for x, y in combinations(scope, 2):
            neighbors[x].add(y)
            neighbors[y].add(x)
    return neighbors


def components(neighbors, removed):
    remaining = set(range(len(neighbors))) - set(removed)
    parts = []
    while remaining:
        root = min(remaining)
        part = {root}
        queue = [root]
        remaining.remove(root)
        while queue:
            v = queue.pop()
            for u in neighbors[v] & remaining:
                remaining.remove(u)
                part.add(u)
                queue.append(u)
        parts.append(part)
    return parts


def actual_backend_control(m):
    n, anchors, triples, clauses, masks = source(m)
    base_result = solve_2cnf_affine(n, clauses, [])
    assert base_result["status"] == "SAT"
    base = base_result["witness"]
    rows = [(mask, 1 ^ ((mask & base).bit_count() % 2)) for mask in masks]
    explicit = sum(1 << (a - 1) for a in anchors)
    for triple, (_, rhs) in zip(triples, rows):
        if rhs:
            explicit |= 1 << (triple[0] - 1)
    check_witness(n, clauses, rows, explicit)
    result = solve_2cnf_affine(n, clauses, rows)
    assert result["status"] == "SAT", result
    check_witness(n, clauses, rows, result["witness"])
    sizes = result["counters"]["polynomial_stage_sizes"]
    assert sizes == [3 ** j for j in range(m + 1)], (m, sizes)
    assert result["counters"]["parity_factor_sizes"] == [3] * m
    assert result["counters"]["affine_rank"] == m
    assert result["counters"]["candidate_products"] == 3 * (3 ** m - 1) // 2
    adjacency = graph(n, clauses, rows)
    probes = 0
    for size in range(3):
        for removed in combinations(range(n), size):
            assert len(components(adjacency, removed)) == 1, (m, removed)
            probes += 1
    assert len(components(adjacency, [a - 1 for a in anchors])) == m
    cap_control = solve_2cnf_affine(n, clauses, rows, term_cap=2)
    assert cap_control["status"] == "UNRESOLVED"
    return {"triples": m, "variables": n, "clauses": len(clauses),
            "affine_rank": m, "base_assignment": base,
            "right_hand_sides": [b for _, b in rows],
            "explicit_witness": explicit, "stage_sizes": sizes,
            "candidate_products": result["counters"]["candidate_products"],
            "connectivity_probes": probes, "vertex_connectivity": 3,
            "term_cap_2_status": cap_control["status"]}


def every_small_base_control(m):
    n, anchors, triples, clauses, masks = source(m)
    tested = 0
    for choices in product(range(4), repeat=m):
        selectors = sum(1 << (triples[j][c - 1] - 1)
                        for j, c in enumerate(choices) if c)
        anchor_patterns = (7,) if selectors else range(8)
        for ap in anchor_patterns:
            base = selectors | (ap << (3 * m))
            check_witness(n, clauses, [], base)
            translated = [tuple(-lit if (base >> (abs(lit) - 1)) & 1 else lit
                                for lit in clause) for clause in clauses]
            # Opposing every original base parity makes every translated RHS one.
            result = solve_horn_affine(n, translated, [(mask, 1) for mask in masks])
            assert result["status"] == "SAT", result
            assert result["counters"]["polynomial_stage_sizes"] == [3 ** j for j in range(m + 1)]
            tested += 1
    return tested


def main():
    results = [actual_backend_control(m) for m in range(2, 10)]
    bases = {str(m): every_small_base_control(m) for m in (2, 3)}
    report = {"status": "PASS", "scope": "specified separator search and closure representation",
              "engine_sha256": hashlib.sha256((ROOT / "closure_parity.py").read_bytes()).hexdigest(),
              "backend_controls": results, "all_valid_small_bases": bases}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
