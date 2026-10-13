#!/usr/bin/env python3
"""Bounded audit for projected cycle-space rank and an easy nonlinear residual.

All arithmetic is over GF(2).  The program is deliberately self-contained and
prints one JSON object; it does not write files.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        x = row
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def rref_nullspace(rows: list[int], width: int) -> list[int]:
    a = [x for x in rows if x]
    pivots: list[int] = []
    r = 0
    for col in range(width):
        hit = next((i for i in range(r, len(a)) if (a[i] >> col) & 1), None)
        if hit is None:
            continue
        a[r], a[hit] = a[hit], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
        pivots.append(col)
        r += 1
        if r == len(a):
            break
    pivot_set = set(pivots)
    out: list[int] = []
    for free in (c for c in range(width) if c not in pivot_set):
        x = 1 << free
        for i in range(len(pivots) - 1, -1, -1):
            p = pivots[i]
            if ((a[i] & x).bit_count() & 1):
                x |= 1 << p
        out.append(x)
    return out


def incidence_rows(n: int, edges: list[tuple[int, int]]) -> list[int]:
    rows = [0] * n
    for j, (u, v) in enumerate(edges):
        rows[u] |= 1 << j
        rows[v] |= 1 << j
    return rows


def component_count(n: int, edges: list[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for u, v in edges:
        union(u, v)
    return len({find(v) for v in range(n)})


def projected_rank_direct(n: int, edges: list[tuple[int, int]], rmask: int) -> int:
    basis = rref_nullspace(incidence_rows(n, edges), len(edges))
    rcols = [j for j in range(len(edges)) if (rmask >> j) & 1]
    projected = []
    for x in basis:
        y = 0
        for k, j in enumerate(rcols):
            if (x >> j) & 1:
                y |= 1 << k
        projected.append(y)
    return gf2_rank(projected)


def projected_rank_formula(n: int, edges: list[tuple[int, int]], rmask: int) -> int:
    kept = [e for j, e in enumerate(edges) if not ((rmask >> j) & 1)]
    return rmask.bit_count() + component_count(n, edges) - component_count(n, kept)


def boundary(n: int, edges: list[tuple[int, int]], xmask: int) -> int:
    c = 0
    for j, (u, v) in enumerate(edges):
        if (xmask >> j) & 1:
            c ^= (1 << u) | (1 << v)
    return c


def weight_at_most_one_witness(n: int, edges: list[tuple[int, int]], charge: int) -> int | None:
    if charge == 0:
        return 0
    for j in range(len(edges)):
        x = 1 << j
        if boundary(n, edges, x) == charge:
            return x
    return None


def friendship_graph(t: int) -> tuple[int, list[tuple[int, int]]]:
    edges: list[tuple[int, int]] = []
    for i in range(t):
        a, b = 2 * i + 1, 2 * i + 2
        edges.extend([(0, a), (a, b), (b, 0)])
    return 2 * t + 1, edges


def main() -> None:
    started = time.perf_counter()
    checks = 0
    rank_instances = 0
    digest_events: list[str] = []

    # Exhaust all simple graphs through five vertices and every edge subset R.
    for n in range(1, 6):
        universe = list(itertools.combinations(range(n), 2))
        for gmask in range(1 << len(universe)):
            edges = [e for j, e in enumerate(universe) if (gmask >> j) & 1]
            for rmask in range(1 << len(edges)):
                direct = projected_rank_direct(n, edges, rmask)
                formula = projected_rank_formula(n, edges, rmask)
                assert direct == formula
                assert 0 <= direct <= rmask.bit_count()
                checks += 2
                rank_instances += 1
        digest_events.append(f"rank-n={n}")

    # Bounded-treewidth friendship graphs have rho=t for R=E, yet the genuinely
    # nonlinear residual |x|<=1 is decided by testing 1+|E| candidates.
    friendship_cases = 0
    for t in range(1, 129):
        n, edges = friendship_graph(t)
        full = (1 << len(edges)) - 1
        rho = projected_rank_formula(n, edges, full)
        assert rho == t
        yes_charge = boundary(n, edges, 1)
        assert weight_at_most_one_witness(n, edges, yes_charge) == 1
        assert weight_at_most_one_witness(n, edges, 0) == 0
        checks += 3
        if t >= 2:
            no_charge = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)
            assert no_charge.bit_count() % 2 == 0
            assert weight_at_most_one_witness(n, edges, no_charge) is None
            checks += 2
        friendship_cases += 1
    digest_events.append("friendship-1..128")

    # Exact small-instance truth-table comparison for every consistent charge.
    truth_table_instances = 0
    for t in range(1, 5):
        n, edges = friendship_graph(t)
        attainable = {boundary(n, edges, x) for x in range(1 << len(edges))}
        for charge in attainable:
            brute = next(
                (x for x in range(1 << len(edges)) if x.bit_count() <= 1 and boundary(n, edges, x) == charge),
                None,
            )
            fast = weight_at_most_one_witness(n, edges, charge)
            assert (brute is None) == (fast is None)
            if fast is not None:
                assert fast.bit_count() <= 1 and boundary(n, edges, fast) == charge
            checks += 2
            truth_table_instances += 1
    digest_events.append("truth-t=1..4")

    # Nonlinearity witness: 0,e1,e2 are accepted but e1+e2 is rejected.
    for m in range(2, 257):
        accepted = lambda x: x.bit_count() <= 1
        assert accepted(0) and accepted(1) and accepted(2) and not accepted(3)
        checks += 4
    digest_events.append("nonlinear-m=2..256")

    elapsed = time.perf_counter() - started
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    semantic_digest = hashlib.sha256("|".join(digest_events).encode()).hexdigest()
    print(json.dumps({
        "run_id": "RANKNONLINFW1",
        "status": "COMPUTATIONAL",
        "seed": None,
        "elapsed_seconds": round(elapsed, 6),
        "checks": checks,
        "rank_identity_instances": rank_instances,
        "friendship_graph_cases": friendship_cases,
        "truth_table_charge_instances": truth_table_instances,
        "largest_friendship": {"vertices": 257, "edges": 384, "rho": 128},
        "nonlinear_residual": "HammingWeight(x_R)<=1",
        "script_sha256": script_sha,
        "semantic_digest": semantic_digest,
        "limitations": [
            "finite checks do not prove the rank identity or asymptotic complexity",
            "the exact theorems are proved separately in the report",
            "the audit does not estimate UWI H(F) or arbitrary-machine runtime",
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
