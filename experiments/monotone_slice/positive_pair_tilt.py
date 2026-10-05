#!/usr/bin/env python3
"""POSITIVE-PAIR-TILT.

One bounded invocation:
1. sample exact-t proper 3-CNF formulas;
2. retain UNSAT formulas;
3. fit the maximum-entropy exponential tilt on the eight nontrivial
   signed pair-orbit counts so the weighted UNSAT sample matches the exact
   uniform-t-slice pair expectations;
4. report feasibility, effective sample size, KL cost, and fit error.

Designed to obey the project-wide ~30 second Python rule.
Status: COMPUTATIONAL.
"""

from __future__ import annotations

import argparse
import math
import random
import time
import json

import numpy as np
from scipy.optimize import root, linprog

from experiments.monotone_slice.moment_balance3 import (
    gen_formula,
    dpll_sat,
    pair_features,
)


def uniform_pair_target(q: int, t: int) -> np.ndarray:
    M = 8 * math.comb(q, 3)
    # pair_features order:
    # (1,0),(1,1),(2,0),(2,1),(2,2),(3,1),(3,2),(3,3)
    n = np.array([
        12 * math.comb(q - 3, 2),
        12 * math.comb(q - 3, 2),
        6 * (q - 3),
        12 * (q - 3),
        6 * (q - 3),
        3,
        3,
        1,
    ], dtype=float)
    return n * t * (t - 1) / (2 * (M - 1))


def fit_maxent(X: np.ndarray, target: np.ndarray):
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd
    ztarget = (target - mu) / sd

    def equations(lam):
        a = Z @ lam
        a -= a.max()
        w = np.exp(a)
        w /= w.sum()
        return (w[:, None] * Z).sum(axis=0) - ztarget

    sol = root(equations, np.zeros(Z.shape[1]), method="hybr")
    lam = sol.x
    a = Z @ lam
    a -= a.max()
    w = np.exp(a)
    w /= w.sum()

    kl = float(np.sum(w * np.log(np.maximum(w * len(w), 1e-300))))
    ess = float(1.0 / np.dot(w, w))

    lp = linprog(
        np.zeros(len(X)),
        A_eq=np.vstack([np.ones(len(X)), X.T]),
        b_eq=np.r_[1.0, target],
        bounds=(0, None),
        method="highs",
    )

    return {
        "success": bool(sol.success),
        "fit_error": float(np.max(np.abs(equations(lam)))),
        "ess": ess,
        "ess_fraction": ess / len(X),
        "kl_to_uniform_unsat_sample": kl,
        "lambda_norm": float(np.linalg.norm(lam)),
        "convex_hull_feasible": bool(lp.success),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()

    if args.n > 16000:
        raise SystemExit("runtime guard: split N > 16000 into multiple invocations")

    q = args.q
    t = round(3.5 * q)
    rng = random.Random(args.seed)

    rows = []
    start = time.time()

    for i in range(args.n):
        if i % 100 == 0 and time.time() - start > 25:
            raise SystemExit("runtime guard: reached 25 seconds; use a smaller chunk")
        f = gen_formula(q, t, rng)
        if not dpll_sat(f):
            rows.append(pair_features(f, q))

    if len(rows) < 20:
        raise SystemExit("too few UNSAT formulas; increase total work using more separate chunks")

    X = np.vstack(rows)
    target = uniform_pair_target(q, t)
    fit = fit_maxent(X, target)

    out = {
        "q": q,
        "t": t,
        "N": args.n,
        "seed": args.seed,
        "unsat_count": len(rows),
        "sampling_seconds": time.time() - start,
        **fit,
        "status": "COMPUTATIONAL",
        "asymptotic_claim": "NONE",
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
