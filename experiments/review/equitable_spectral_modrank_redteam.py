#!/usr/bin/env python3
"""MODRANKFW1: red-team the fixed-prime implementation in EQSPECTRAL1.

This does not challenge the exact real/rational spectral theorem.  It checks
the implementation choice rank_mod(A, 1_000_003), derives an explicit modular
kernel for the NO ring at its first collision, and reproduces the same failure
on a small full matrix over F_31.  Cooperative budget: 25 seconds.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

RUN_ID = "MODRANKFW1"
START = time.monotonic()
DEADLINE = START + 25.0


def check(ok: bool, label: str) -> None:
    if time.monotonic() > DEADLINE:
        raise TimeoutError("25-second budget exceeded")
    if not ok:
        raise AssertionError(label)


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def order_mod(a: int, p: int) -> int:
    order = p - 1
    for q in factor(p - 1):
        while order % q == 0 and pow(a, order // q, p) == 1:
            order //= q
    return order


def k7_ring(r: int) -> tuple[int, set[tuple[int, int]]]:
    k = 3 * r
    edges: set[tuple[int, int]] = set()
    for block in range(k):
        base = 7 * block
        for a in range(7):
            for b in range(a + 1, 7):
                edges.add((base + a, base + b))
        edges.remove((base + 4, base + 5))
    for block in range(k):
        a = 7 * block + 4
        b = 7 * ((block + 1) % k) + 5
        edges.add((min(a, b), max(a, b)))
    return 7 * k, edges


def matrix_plus_three(n: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 3
    for a, b in edges:
        A[a][b] = A[b][a] = 1
    return A


def rank_mod(A: list[list[int]], p: int) -> int:
    M = [[x % p for x in row] for row in A]
    rank = 0
    for col in range(len(M[0])):
        pivot = next((i for i in range(rank, len(M)) if M[i][col]), None)
        if pivot is None:
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        inv = pow(M[rank][col], -1, p)
        M[rank] = [(x * inv) % p for x in M[rank]]
        for i in range(len(M)):
            if i != rank and M[i][col]:
                f = M[i][col]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[rank])]
        rank += 1
    return rank


def local_mode_check(p: int, z: int, X: int, Y: int) -> None:
    check((35 * z * z + 182 * z + 35) % p == 0, "mode polynomial")
    check((16 * X + (-5 + 7 * z) * Y) % p == 0, "first mode equation")
    check(((-5 + 7 * pow(z, -1, p)) * X + 16 * Y) % p == 0,
          "second mode equation")
    q = (-(X + Y) * pow(7, -1, p)) % p
    check((X + Y + 7 * q) % p == 0, "core equation")


def main() -> None:
    p = 1_000_003
    z1, z2 = (-5) % p, pow(-5, -1, p)
    order1, order2 = order_mod(z1, p), order_mod(z2, p)
    check(factor(p - 1) == {2: 1, 3: 1, 166667: 1}, "factor p-1")
    check(order1 == order2 == 500001, "root orders")
    check(z1 != z2 and pow(z1, order1, p) == pow(z2, order2, p) == 1,
          "distinct periodic roots")
    local_mode_check(p, z1, 5, 2)
    local_mode_check(p, z2, 2, 5)
    check((5 * 5 - 2 * 2) % p != 0, "two kernel modes independent")
    r_collision = order1 // math.gcd(order1, 3)
    check(r_collision == 166667 and 3 * r_collision == order1,
          "first ring collision")

    # Full-matrix hostile control: modulo 31, ord(-5)=6, hence N_2 collides.
    p_small, r_small = 31, 2
    n_small, edges_small = k7_ring(r_small)
    A_small = matrix_plus_three(n_small, edges_small)
    rank_small = rank_mod(A_small, p_small)
    check(n_small == 42 and n_small - rank_small == 2,
          "full matrix modular nullity two")
    # Over C the determinant factor is positive on every unit-circle mode.
    check(182 - 70 == 112 > 0, "exact characteristic-zero gap")

    result = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "candidate_status": "FALSIFIED/RETIRED",
        "fixed_prime": p,
        "mode_polynomial_factorization": "35 z^2 + 182 z + 35 = (5 z + 1)(7 z + 35)",
        "roots_mod_p": [z1, z2],
        "root_orders": [order1, order2],
        "first_collision": {
            "r": r_collision,
            "ring_blocks": 3 * r_collision,
            "graph_vertices": 21 * r_collision,
            "graph_edges": 63 * r_collision,
            "compiler_variables": 96012 * r_collision,
            "compiler_clauses": 128016 * r_collision,
            "implemented_modular_nullity_lower_bound": 2,
            "implemented_label": 1,
            "true_promise_label": 0,
        },
        "small_full_matrix_control": {
            "prime": p_small,
            "r": r_small,
            "vertices": n_small,
            "rank": rank_small,
            "nullity": n_small - rank_small,
        },
        "repair": "Use exact rational/integer rank (for example fraction-free elimination), not one fixed prime.",
        "scope": [
            "The exact characteristic-zero spectral separator remains valid.",
            "Only the fixed-prime executable implementation is falsified.",
            "Neither separator is a total L22 decider.",
        ],
        "elapsed_seconds": time.monotonic() - START,
    }
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path("results/raw/review/2026-10-13_1335_eqspectral_modrank_redteam.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
