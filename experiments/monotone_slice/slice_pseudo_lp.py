#!/usr/bin/env python3
"""Exact local pseudo-independence LP for a uniform Hamming slice.

For D = uniform t-subset of [M], determine the least epsilon such that the
k-coordinate marginal is a convex combination of product distributions with
each coordinate bias in [p(1-epsilon), p(1+epsilon)], p=t/M.

Exchangeability and multi-affinity reduce the exact feasibility question to
a (k+1)-variable LP in normalized factorial moments.

Each invocation is tiny and well below the project-wide ~30 second rule.
"""

from __future__ import annotations

import argparse
import math
import json
import time

import numpy as np
from scipy.optimize import linprog


def target_moment(M: int, t: int, r: int) -> float:
    """Normalized r-way inclusion moment divided by p^r."""
    if r == 0:
        return 1.0
    p = t / M
    out = 1.0
    for i in range(r):
        out *= ((t - i) / (M - i)) / p
    return out


def corner_moment(k: int, j: int, r: int, eps: float) -> float:
    """Symmetrized normalized r-moment for a corner with j high biases."""
    if r == 0:
        return 1.0
    den = math.comb(k, r)
    total = 0.0
    lo = max(0, r - (k - j))
    hi = min(r, j)
    for ell in range(lo, hi + 1):
        prob = math.comb(j, ell) * math.comb(k - j, r - ell) / den
        total += prob * (1 + eps) ** ell * (1 - eps) ** (r - ell)
    return total


def feasible(M: int, t: int, k: int, eps: float):
    A = np.zeros((k + 1, k + 1), dtype=float)
    for r in range(k + 1):
        for j in range(k + 1):
            A[r, j] = corner_moment(k, j, r, eps)
    b = np.array([target_moment(M, t, r) for r in range(k + 1)])
    res = linprog(
        np.zeros(k + 1),
        A_eq=A,
        b_eq=b,
        bounds=[(0, None)] * (k + 1),
        method="highs",
        options={
            "primal_feasibility_tolerance": 1e-9,
            "dual_feasibility_tolerance": 1e-9,
        },
    )
    return bool(res.success)


def min_epsilon(M: int, t: int, k: int) -> float | None:
    lo, hi = 0.0, 0.99
    if not feasible(M, t, k, hi):
        return None
    for _ in range(50):
        mid = (lo + hi) / 2
        if feasible(M, t, k, mid):
            hi = mid
        else:
            lo = mid
    return hi


def lower_bound(M: int, t: int, k: int) -> float:
    d = (M - t) / (t * (M - 1))
    return math.sqrt((k - 1) * d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--k-max", type=int, default=10)
    args = ap.parse_args()

    start = time.time()
    q = args.q
    M = 8 * math.comb(q, 3)
    t = round(3.5 * q)

    rows = []
    for k in range(2, args.k_max + 1):
        eps = min_epsilon(M, t, k)
        lb = lower_bound(M, t, k)
        rows.append({
            "k": k,
            "epsilon_min_lp": eps,
            "epsilon_pair_lower_bound": lb,
            "ratio_to_lower_bound": None if eps is None else eps / lb,
        })

    print(json.dumps({
        "q": q,
        "M": M,
        "t": t,
        "p": t / M,
        "rows": rows,
        "elapsed_seconds": time.time() - start,
        "status": "COMPUTATIONAL",
        "criterion": "exact exchangeable corner-product LP",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
