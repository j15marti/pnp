#!/usr/bin/env python3
"""Bounded hostile-control audit for expanded monomials versus compact computation.

This program does not test PC/PCR lower bounds and does not solve the compiled
graph-colouring family.  It falsifies only a generic representation transfer:
large expanded monomial support does not imply large arithmetic-circuit size.
All exhaustive polynomial expansions are capped at t <= 18.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import defaultdict, deque
from pathlib import Path

START = time.monotonic()
CHECKS = defaultdict(int)


def check(ok: bool, group: str) -> None:
    if time.monotonic() - START > 25:
        raise TimeoutError("cooperative 25-second budget exceeded")
    CHECKS[group] += 1
    if not ok:
        raise AssertionError(f"{group} check {CHECKS[group]} failed")


def expand_product(t: int, prime: int, complemented: set[int] | None = None) -> dict[int, int]:
    """Expand product_i (1+x_i) after x_i -> 1-x_i for complemented i.

    Monomials are squarefree bit masks.  Coefficients are reduced mod prime.
    """
    complemented = complemented or set()
    poly = {0: 1}
    for i in range(t):
        # Ordinary factor 1+x_i; complemented factor 2-x_i.
        constant, linear = ((2 % prime), (-1) % prime) if i in complemented else (1, 1)
        nxt: dict[int, int] = defaultdict(int)
        for mask, coeff in poly.items():
            nxt[mask] = (nxt[mask] + coeff * constant) % prime
            nxt[mask | (1 << i)] = (nxt[mask | (1 << i)] + coeff * linear) % prime
        poly = {m: c for m, c in nxt.items() if c % prime}
    return poly


def eval_expanded(poly: dict[int, int], values: list[int], prime: int) -> int:
    total = 0
    for mask, coeff in poly.items():
        term = coeff
        for i, val in enumerate(values):
            if mask >> i & 1:
                term = term * val % prime
        total = (total + term) % prime
    return total


def eval_compact(values: list[int], prime: int, complemented: set[int] | None = None) -> int:
    complemented = complemented or set()
    product = 1
    for i, val in enumerate(values):
        if i in complemented:
            val = (1 - val) % prime
        product = product * (1 + val) % prime
    return product


def compact_metrics(t: int) -> dict[str, int]:
    return {
        "addition_gates": t,
        "multiplication_gates": max(0, t - 1),
        "total_operation_gates": max(1, 2 * t - 1),
        "balanced_depth_upper_bound": 1 + (t - 1).bit_length(),
    }


def two_sat(n: int, clauses: list[tuple[int, int]]) -> bool:
    graph = [[] for _ in range(2 * n)]

    def node(lit: int) -> int:
        v = abs(lit) - 1
        return 2 * v + (0 if lit > 0 else 1)

    def neg(u: int) -> int:
        return u ^ 1

    for a, b in clauses:
        graph[neg(node(a))].append(node(b))
        graph[neg(node(b))].append(node(a))
    index = 0
    stack: list[int] = []
    onstack = [False] * (2 * n)
    indices = [-1] * (2 * n)
    low = [0] * (2 * n)
    comp = [-1] * (2 * n)

    def visit(v: int) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        onstack[v] = True
        for w in graph[v]:
            if indices[w] < 0:
                visit(w)
                low[v] = min(low[v], low[w])
            elif onstack[w]:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            cid = v
            while True:
                w = stack.pop()
                onstack[w] = False
                comp[w] = cid
                if w == v:
                    break

    for v in range(2 * n):
        if indices[v] < 0:
            visit(v)
    return all(comp[2 * i] != comp[2 * i + 1] for i in range(n))


def horn_forward(n: int, rules: list[tuple[tuple[int, ...], int | None]]) -> bool:
    true = set()
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            if all(x in true for x in body):
                if head is None:
                    return False
                if head not in true:
                    true.add(head)
                    changed = True
    return True


def gaussian_consistent(rows: list[tuple[int, int]], n: int) -> tuple[bool, int]:
    rows = [[mask, rhs] for mask, rhs in rows]
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][0] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][0] >> col & 1:
                rows[r][0] ^= rows[rank][0]
                rows[r][1] ^= rows[rank][1]
        rank += 1
    return not any(mask == 0 and rhs for mask, rhs in rows), rank


def bipartite_matching(n: int, edges: list[tuple[int, int]]) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    match = [-1] * n

    def augment(u: int, seen: set[int]) -> bool:
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            if match[v] < 0 or augment(match[v], seen):
                match[v] = u
                return True
        return False

    return sum(augment(u, set()) for u in range(n))


def path_cnf_dp(n: int, forbidden: set[tuple[int, int]]) -> bool:
    states = {0, 1}
    for _ in range(1, n):
        states = {b for a in states for b in (0, 1) if (a, b) not in forbidden}
        if not states:
            return False
    return bool(states)


def main(out: Path) -> None:
    cases = []
    primes = (2, 3, 5, 7, 11)
    for t in range(1, 19):
        metrics = compact_metrics(t)
        ordinary = expand_product(t, 11)
        check(len(ordinary) == 2**t, "ordinary_support")
        for prime in primes:
            for comp in (set(), set(range(0, t, 2)), set(range(t))):
                poly = expand_product(t, prime, comp)
                vals = [(7 * i + 3) % prime for i in range(t)]
                check(eval_expanded(poly, vals, prime) == eval_compact(vals, prime, comp),
                      "expanded_equals_compact")
        cases.append({
            "t": t,
            "expanded_monomials": 2**t,
            **metrics,
            "support_to_gate_ratio": (2**t) / metrics["total_operation_gates"],
            "all_complemented_support_mod_2": len(expand_product(t, 2, set(range(t)))),
            "alternating_complement_support_mod_3": len(expand_product(t, 3, set(range(0, t, 2)))),
        })

    # Independent products preserve compact composability while supports multiply.
    for a, b in ((3, 4), (6, 7), (9, 9)):
        check(2**a * 2**b == 2 ** (a + b), "independent_product_support")
        check((2 * a - 1) + (2 * b - 1) + 1 == 2 * (a + b) - 1,
              "independent_product_gates")

    # Easy controls: real compact algorithms yielding only a decision bit.
    n = 64
    t0 = time.perf_counter()
    two_sat_yes = two_sat(n, [(i, i + 1) for i in range(1, n)] + [(-i, -(i + 1)) for i in range(1, n)])
    two_sat_no = two_sat(1, [(1, 1), (-1, -1)])
    horn_yes = horn_forward(n, [((i,), i + 1) for i in range(n - 1)])
    horn_no = horn_forward(n, [((), 0)] + [((i,), i + 1) for i in range(n - 1)] + [((n - 1,), None)])
    affine_rows = [((1 << i) | (1 << (i + 1)), i & 1) for i in range(n - 1)]
    affine_yes, affine_rank = gaussian_consistent(affine_rows, n)
    affine_no, _ = gaussian_consistent(affine_rows + [(0, 1)], n)
    matching = bipartite_matching(n, [(i, i) for i in range(n)] + [(i, (i + 1) % n) for i in range(n)])
    path_yes = path_cnf_dp(n, {(1, 1)})
    controls_elapsed = time.perf_counter() - t0
    for value, group in ((two_sat_yes, "2sat_yes"), (not two_sat_no, "2sat_no"),
                         (horn_yes, "horn_yes"), (not horn_no, "horn_no"),
                         (affine_yes, "affine_yes"), (not affine_no, "affine_no"),
                         (matching == n, "matching_flow"), (path_yes, "bounded_treewidth")):
        check(value, group)

    semantic = {
        "parameters": {"max_expanded_t": 18, "primes": list(primes), "easy_control_n": n},
        "representation_family": "P_t=product_i(1+x_i)",
        "compact_gate_formula": "2t-1 arithmetic operation gates",
        "cases": cases,
        "phase_control": {
            "substitution": "x_i -> 1-x_i",
            "mod_2_all_complemented_support": cases[-1]["all_complemented_support_mod_2"],
            "interpretation": "support can collapse under an invertible phase switch even while the substituted circuit stays linear-size",
        },
        "easy_controls": {
            "2sat_yes": two_sat_yes, "2sat_no": two_sat_no,
            "horn_yes": horn_yes, "horn_no": horn_no,
            "affine_yes": affine_yes, "affine_no": affine_no,
            "affine_rank": affine_rank, "perfect_matching_size": matching,
            "bounded_treewidth_path_yes": path_yes,
            "elapsed_seconds": controls_elapsed,
        },
        "checks_by_group": dict(sorted(CHECKS.items())),
        "assertions": sum(CHECKS.values()),
        "status": "COMPUTATIONAL",
        "limitations": [
            "The symbolic family proves only that expanded support does not lower-bound arithmetic-circuit size.",
            "No compact refutation of the PC22 graph-colouring family is constructed.",
            "The easy controls are hostile controls, not algorithms for L22.",
            "Finite expansion stops at t=18 and is not used for asymptotic inference.",
        ],
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        **semantic,
        "semantic_sha256": digest,
        "elapsed_seconds": time.monotonic() - START,
        "all_checks_passed": True,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    main(args.out)
