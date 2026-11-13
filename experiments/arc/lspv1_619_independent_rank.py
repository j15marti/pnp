#!/usr/bin/env python3
"""LSPV-1/619: independent standard-library GF(2) rank/consistency audit.
For the exact bridgeless hexagonal-prism SOURCE fixture accepted by archived /341.
No proof-system lower bound or historical mixed-rule checker is claimed.
Run: python3 experiments/arc/lspv1_619_independent_rank.py
"""
import json

EDGES = [
    (0, 1), (5, 0), (8, 9), (9, 10), (1, 2), (2, 3),
    (3, 4), (4, 5), (6, 7), (7, 8), (0, 6), (10, 11),
    (3, 9), (11, 6), (1, 7), (2, 8), (4, 10), (5, 11)
]
V, E = 12, len(EDGES)
INC = [[i for i, (a, b) in enumerate(EDGES) if v in (a, b)]
       for v in range(V)]
Q = [0] * V
Q[1] = 1
ROWS = [
    sum(1 << e for e in (es[:2] if v in (0, 9) else es))
    for v, es in enumerate(INC)
]

def rank_and_consistency(rows, rhs):
    rows, rhs = rows[:], rhs[:]
    rank = 0
    for e in range(E):
        j = next((i for i in range(rank, len(rows))
                  if rows[i] >> e & 1), None)
        if j is None:
            continue
        rows[j], rows[rank] = rows[rank], rows[j]
        rhs[j], rhs[rank] = rhs[rank], rhs[j]
        for i in range(len(rows)):
            if i != rank and rows[i] >> e & 1:
                rows[i] ^= rows[rank]
                rhs[i] ^= rhs[rank]
        rank += 1
    return rank, not any(mask == 0 and bit for mask, bit in zip(rows, rhs))

def connected(excluded_edge=None, excluded_vertex=None):
    vs = [v for v in range(V) if v != excluded_vertex]
    seen = {vs[0]}
    todo = [vs[0]]
    for a in todo:
        for i, (x, y) in enumerate(EDGES):
            if i == excluded_edge or excluded_vertex in (x, y):
                continue
            b = y if x == a else x if y == a else None
            if b is not None and b not in seen:
                seen.add(b)
                todo.append(b)
    return len(seen) == len(vs)

def main():
    assert all(len(es) == 3 for es in INC)
    assert INC[0] == [0, 1, 10] and INC[9] == [2, 3, 12]
    assert connected()
    assert all(connected(excluded_edge=i) for i in range(E))
    assert all(connected(excluded_vertex=v) for v in range(V))
    base_rank, base_consistent = rank_and_consistency(ROWS, Q)
    assert (base_rank, base_consistent) == (12, True)
    pins = []
    for v, es in enumerate(INC):
        for pattern in range(8):
            bits = [(pattern >> j) & 1 for j in range(3)]
            parity = bits[0] ^ bits[1] ^ (0 if v in (0, 9) else bits[2])
            if parity == Q[v]:
                continue
            rhs = Q[:]
            rhs[v] ^= 1
            rank, consistent = rank_and_consistency(
                ROWS + [1 << e for e in es], rhs + bits
            )
            assert (rank, consistent) == (14, True), (v, pattern, rank, consistent)
            pins.append([v, pattern, rank, 1 << (E - rank)])
    assert len(pins) == 48
    output = {
        "run": "LSPV-1/619 independent GF(2) rank audit",
        "graph": "bridgeless hexagonal prism",
        "V": V, "E": E, "bridgeless": True, "vertex_biconnected": True,
        "source_rank": base_rank, "source_consistent": base_consistent,
        "source_models": 1 << (E - base_rank),
        "source_clauses": len(pins),
        "all_deletion_pin_systems_rank": 14,
        "all_deletion_pin_systems_consistent": True,
        "deletion_models_per_clause": 16,
        "total_deletion_pin_controls": len(pins),
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
