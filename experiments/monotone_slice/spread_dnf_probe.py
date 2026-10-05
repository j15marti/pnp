#!/usr/bin/env python3
"""SPREAD-DNF-PROBE.

Builds one exact-pair-balanced empirical UNSAT distribution at density 3.5,
then probes it against one independent random spread monotone DNF and compares
with the uniform exact slice.

One invocation is one q/seed/DNF seed chunk and is designed for <30 seconds.
Status: COMPUTATIONAL.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
import time
import json

import numpy as np
from scipy.optimize import root

from experiments.monotone_slice.moment_balance3 import (
    gen_formula,
    dpll_sat,
    pair_features,
)


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


def fit_pool(q: int, n_total: int, seed: int):
    t = round(3.5 * q)
    rng = random.Random(seed)
    rows = []

    for fidx in range(n_total):
        f = gen_formula(q, t, rng)
        if not dpll_sat(f):
            rows.append((f, pair_features(f, q)))

    X = np.vstack([x for _, x in rows])
    target = uniform_pair_target(q, t)
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

    sol = root(equations, np.zeros(8), method="hybr")
    lam = sol.x
    a = Z @ lam
    a -= a.max()
    w = np.exp(a)
    w /= w.sum()

    return rows, w, float(np.max(np.abs(equations(lam)))), float(1.0 / np.dot(w, w))


def clause_universe(q: int):
    out = []
    for vs in itertools.combinations(range(1, q + 1), 3):
        for bits in range(8):
            out.append(tuple(
                v if ((bits >> j) & 1) else -v
                for j, v in enumerate(vs)
            ))
    return out


def random_terms(M: int, width: int, nterms: int, seed: int):
    rng = random.Random(seed)
    terms = set()
    while len(terms) < nterms:
        terms.add(tuple(sorted(rng.sample(range(M), width))))
    return terms


def accepts(ids, terms, width):
    return any(c in terms for c in itertools.combinations(ids, width))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--width", type=int, choices=[2,3], required=True)
    ap.add_argument("--terms", type=int, required=True)
    ap.add_argument("--dnf-seed", type=int, required=True)
    ap.add_argument("--uniform-samples", type=int, default=1000)
    args = ap.parse_args()

    if args.n > 16000:
        raise SystemExit("runtime guard: split N > 16000")
    if args.width == 3 and args.terms > 300000:
        raise SystemExit("runtime guard: split width-3 probe above 300000 terms")

    start = time.time()
    q = args.q
    t = round(3.5 * q)

    rows, w, fiterr, ess = fit_pool(q, args.n, args.seed)

    universe = clause_universe(q)
    cid = {c: i for i, c in enumerate(universe)}
    terms = random_terms(len(universe), args.width, args.terms, args.dnf_seed)

    pos_ids = [
        tuple(sorted(cid[c] for c in f))
        for f, _ in rows
    ]

    rng = random.Random(args.dnf_seed + 1000003)
    neg_ids = [
        tuple(sorted(cid[c] for c in gen_formula(q, t, rng)))
        for _ in range(args.uniform_samples)
    ]

    pos_accept = np.array([
        accepts(ids, terms, args.width) for ids in pos_ids
    ], dtype=float)
    neg_accept = np.array([
        accepts(ids, terms, args.width) for ids in neg_ids
    ], dtype=float)

    out = {
        "q": q,
        "t": t,
        "N": args.n,
        "seed": args.seed,
        "width": args.width,
        "terms": len(terms),
        "dnf_seed": args.dnf_seed,
        "unsat_count": len(rows),
        "pair_fit_error": fiterr,
        "positive_ess": ess,
        "positive_acceptance": float(np.dot(w, pos_accept)),
        "uniform_slice_acceptance": float(neg_accept.mean()),
        "gap": float(np.dot(w, pos_accept) - neg_accept.mean()),
        "elapsed_seconds": time.time() - start,
        "status": "COMPUTATIONAL",
        "asymptotic_claim": "NONE",
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
