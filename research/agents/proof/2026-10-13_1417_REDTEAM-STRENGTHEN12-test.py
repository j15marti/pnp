#!/usr/bin/env python3
"""Bounded finite audit of the ROUNDINGSQUEEZE5 lifting repair.

The symbolic proof remains in the companion report.  This program attacks
four finite failure modes: sign monotonicity, no-weakening cube elimination,
the half-rectangle step for nested (triangle) relations, and exact rational
parameter arithmetic.  It is deterministic and self-times against the
automation's 25-second per-invocation budget.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
from fractions import Fraction
from pathlib import Path


def satisfying_count(formula: tuple[tuple[int, ...], ...], n: int) -> int:
    total = 0
    for bits in itertools.product((0, 1), repeat=n):
        if all(any((sgn == 1 and bits[i]) or (sgn == -1 and not bits[i])
                   for i, sgn in enumerate(clause) if sgn)
               for clause in formula):
            total += 1
    return total


def sign_monotonicity() -> dict[str, int]:
    checked = 0
    for n, max_clauses in ((3, 3), (4, 2)):
        clauses = tuple(v for v in itertools.product((-1, 0, 1), repeat=n)
                        if any(v))
        for size in range(max_clauses + 1):
            for formula in itertools.combinations(clauses, size):
                monotone = tuple(tuple(-1 if sgn else 0 for sgn in clause)
                                 for clause in formula)
                assert satisfying_count(monotone, n) >= satisfying_count(formula, n)
                checked += 1
    return {"formulas": checked}


Literal = tuple[int, int]  # (variable, sign); opposite signs resolve.
Clause = frozenset[Literal]


def resolve(a: Clause, b: Clause, pivot: int) -> Clause:
    assert (pivot, 1) in a and (pivot, -1) in b
    return frozenset((a - {(pivot, 1)}) | (b - {(pivot, -1)}))


def eliminate(leaves: dict[tuple[int, ...], Clause], free: tuple[int, ...],
              parent: Clause, prefix: tuple[int, ...] = ()) -> tuple[Clause, int, int]:
    """Return derived clause, added depth, and resolution-line count."""
    level = len(prefix)
    if level == len(free):
        out = leaves[prefix]
        cube = parent | frozenset((v, 1 if bit == 0 else -1)
                                  for v, bit in zip(free, prefix))
        assert out <= cube
        return out, 0, 0
    pivot = free[level]
    left, dl, ll = eliminate(leaves, free, parent, prefix + (0,))
    right, dr, lr = eliminate(leaves, free, parent, prefix + (1,))
    if (pivot, 1) not in left:
        out, extra = left, 0
    elif (pivot, -1) not in right:
        out, extra = right, 0
    else:
        out, extra = resolve(left, right, pivot), 1
    allowed = parent | frozenset((v, 1 if bit == 0 else -1)
                                 for v, bit in zip(free[:level], prefix))
    assert out <= allowed
    return out, max(dl, dr) + extra, ll + lr + extra


def cube_elimination(rng: random.Random) -> dict[str, int]:
    exhaustive = 0
    parent = frozenset({(9, 1)})
    free = (0, 1)
    patterns = tuple(itertools.product((0, 1), repeat=2))
    options: dict[tuple[int, ...], tuple[Clause, ...]] = {}
    for pat in patterns:
        cube = parent | frozenset((v, 1 if bit == 0 else -1)
                                  for v, bit in zip(free, pat))
        items = tuple(cube)
        options[pat] = tuple(frozenset(items[i] for i in range(len(items)) if mask >> i & 1)
                             for mask in range(1 << len(items)))
    for chosen in itertools.product(*(options[p] for p in patterns)):
        out, depth, lines = eliminate(dict(zip(patterns, chosen)), free, parent)
        assert out <= parent and depth <= 2 and lines <= 3 and len(out) <= len(parent)
        exhaustive += 1

    randomized = 0
    free = (0, 1, 2)
    patterns = tuple(itertools.product((0, 1), repeat=3))
    for _ in range(4096):
        leaves = {}
        for pat in patterns:
            cube = list(parent | frozenset((v, 1 if bit == 0 else -1)
                                           for v, bit in zip(free, pat)))
            leaves[pat] = frozenset(x for x in cube if rng.randrange(2))
        out, depth, lines = eliminate(leaves, free, parent)
        assert out <= parent and depth <= 3 and lines <= 7 and len(out) <= len(parent)
        randomized += 1
    return {"exhaustive_leaf_families": exhaustive, "random_leaf_families": randomized}


def nondecreasing_sequences(length: int, maximum: int):
    yield from itertools.combinations_with_replacement(range(maximum + 1), length)


def triangle_half_rectangles() -> dict[str, int]:
    checked = 0
    for rows in range(1, 7):
        for cols in range(1, 7):
            need_r, need_c = (rows + 1) // 2, (cols + 1) // 2
            for thresholds in nondecreasing_sequences(rows, cols):
                pivot = thresholds[rows - need_r]
                if pivot >= need_c:
                    chosen_rows = range(rows - need_r, rows)
                    chosen_cols = range(need_c)
                    assert all(c < thresholds[r] for r in chosen_rows for c in chosen_cols)
                else:
                    chosen_rows = range(need_r)
                    chosen_cols = range(cols - need_c, cols)
                    assert all(c >= thresholds[r] for r in chosen_rows for c in chosen_cols)
                checked += 1
    return {"nested_relations": checked}


def ceiling_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def parameter_recipe() -> dict[str, object]:
    cases = (
        (Fraction(6, 5), Fraction(3, 2)),
        (Fraction(6, 5), Fraction(7, 4)),
        (Fraction(2, 1), Fraction(4, 3)),
        (Fraction(3, 1), Fraction(6, 5)),
        (Fraction(10, 1), Fraction(21, 20)),
    )
    certificates = []
    for p, beta in cases:
        assert p > 1 and 1 < beta < 1 + 1 / p
        rho = ((beta - 1) + 1 / p) / 2
        gap = 1 + rho - beta
        delta = gap / (2 * (1 + rho))
        a = ceiling_fraction(4 * beta / gap)
        h = a * (1 - delta) * (1 + rho) - beta * (a + 1)
        assert 0 < rho < 1 / p and 0 < delta < 1 and h > 0
        k1 = ceiling_fraction(p * (4 * a + 1) / (1 - p * rho)) + 1
        k2 = ceiling_fraction((a * (1 - delta) + beta * (4 * a + 1)) / h) + 1
        k = max(k1, k2)
        c = (rho * k).numerator // (rho * k).denominator
        q = 4 * a + c + 1
        u = a * (k + 4) + k
        z = a * (1 - delta) * (k + c)
        assert k > p * q
        assert z > beta * (u + 1)
        certificates.append({
            "p": str(p), "beta": str(beta), "rho": str(rho),
            "delta": str(delta), "a": a, "k": k, "c": c,
            "k_minus_pq": str(k - p * q),
            "z_minus_beta_u1": str(z - beta * (u + 1)),
        })
    endpoint = Fraction(1, 2) * ((Fraction(6, 5) + 2) / Fraction(6, 5) ** 2
                                - Fraction(6, 5))
    assert endpoint == Fraction(23, 45)
    return {"cases": certificates, "flmv_c_6_5": str(endpoint)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=20261013)
    args = parser.parse_args()
    signal.alarm(24)
    started = time.perf_counter()
    rng = random.Random(args.seed)
    payload = {
        "run_id": "REDTEAM-STRENGTHEN12",
        "seed": args.seed,
        "status": "PASS",
        "sign_monotonicity": sign_monotonicity(),
        "cube_elimination": cube_elimination(rng),
        "triangle_half_rectangles": triangle_half_rectangles(),
        "parameter_recipe": parameter_recipe(),
    }
    semantic = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    payload["runtime_seconds"] = round(time.perf_counter() - started, 6)
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")


if __name__ == "__main__":
    main()
