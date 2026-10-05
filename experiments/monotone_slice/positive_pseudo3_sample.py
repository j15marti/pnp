#!/usr/bin/env python3
"""POS-PSEUDO3 sampled local-marginal probe.

One invocation handles one q/seed chunk and is designed for <30 seconds.
It:
1. samples exact-t proper 3-CNF;
2. retains UNSAT formulas;
3. exponentially tilts UNSAT to match the exact uniform-slice pair vector;
4. samples canonical clause triples from each retained formula;
5. emits weighted orbit frequencies.

Run the uniform control in a separate invocation with --uniform so the
combined job is decomposed under the runtime rule.
Status: COMPUTATIONAL.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
import time
import json
from collections import defaultdict

import numpy as np
from scipy.optimize import root

from experiments.monotone_slice.moment_balance3 import (
    gen_formula,
    dpll_sat,
    pair_features,
)
from experiments.monotone_slice.pair_match_order3 import canonical_triple


def uniform_pair_target(q: int, t: int) -> np.ndarray:
    M = 8 * math.comb(q, 3)
    n = np.array([
        12 * math.comb(q - 3, 2),
        12 * math.comb(q - 3, 2),
        6 * (q - 3),
        12 * (q - 3),
        6 * (q - 3),
        3, 3, 1,
    ], dtype=float)
    return n * t * (t - 1) / (2 * (M - 1))


def fit_tilt(X: np.ndarray, target: np.ndarray):
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd
    zt = (target - mu) / sd

    def equations(lam):
        a = Z @ lam
        a -= a.max()
        w = np.exp(a)
        w /= w.sum()
        return (w[:, None] * Z).sum(axis=0) - zt

    sol = root(equations, np.zeros(Z.shape[1]), method="hybr")
    lam = sol.x
    a = Z @ lam
    a -= a.max()
    w = np.exp(a)
    w /= w.sum()
    return w, float(np.max(np.abs(equations(lam)))), float(1 / np.dot(w, w))


def sampled_orbits(formula, nsamp: int, rng: random.Random):
    counts = defaultdict(int)
    n = len(formula)
    for _ in range(nsamp):
        i, j, k = rng.sample(range(n), 3)
        key = canonical_triple((formula[i], formula[j], formula[k]))
        counts[repr(key)] += 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--triple-samples", type=int, default=2000)
    ap.add_argument("--uniform", action="store_true")
    args = ap.parse_args()

    if args.n > 16000:
        raise SystemExit("runtime guard: split N > 16000")
    if args.triple_samples > 2500:
        raise SystemExit("runtime guard: split triple sampling above 2500/formula")

    q = args.q
    t = round(3.5 * q)
    rng = random.Random(args.seed)
    start = time.time()

    if args.uniform:
        agg = defaultdict(float)
        for i in range(args.n):
            if i % 25 == 0 and time.time() - start > 25:
                raise SystemExit("runtime guard: reduce uniform chunk")
            f = gen_formula(q, t, rng)
            c = sampled_orbits(f, args.triple_samples, rng)
            for key, v in c.items():
                agg[key] += v / args.triple_samples / args.n
        out = {
            "mode": "uniform",
            "q": q,
            "t": t,
            "N": args.n,
            "seed": args.seed,
            "triple_samples": args.triple_samples,
            "orbit_frequency": dict(agg),
            "elapsed_seconds": time.time() - start,
            "status": "COMPUTATIONAL",
        }
        print(json.dumps(out, sort_keys=True))
        return

    formulas = []
    feats = []
    for i in range(args.n):
        if i % 100 == 0 and time.time() - start > 25:
            raise SystemExit("runtime guard: reduce positive sampling chunk")
        f = gen_formula(q, t, rng)
        if not dpll_sat(f):
            formulas.append(f)
            feats.append(pair_features(f, q))

    X = np.vstack(feats)
    w, fit_error, ess = fit_tilt(X, uniform_pair_target(q, t))

    agg = defaultdict(float)
    for idx, (weight, f) in enumerate(zip(w, formulas)):
        if idx % 25 == 0 and time.time() - start > 25:
            raise SystemExit("runtime guard: separate sampling and orbit-census stages")
        c = sampled_orbits(f, args.triple_samples, rng)
        for key, v in c.items():
            agg[key] += weight * v / args.triple_samples

    out = {
        "mode": "pair_balanced_unsat",
        "q": q,
        "t": t,
        "N": args.n,
        "seed": args.seed,
        "unsat_count": len(formulas),
        "pair_fit_error": fit_error,
        "ess": ess,
        "triple_samples": args.triple_samples,
        "orbit_frequency": dict(agg),
        "elapsed_seconds": time.time() - start,
        "status": "COMPUTATIONAL",
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
