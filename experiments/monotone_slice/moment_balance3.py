#!/usr/bin/env python3
"""MOMENT-BALANCE3.

One invocation handles exactly one q value and one bounded sample chunk.
Designed for the project-wide ~30 second Python runtime rule.

The experiment:
1. samples exact distinct-clause 3-CNF at density 3.5;
2. solves SAT exactly with DPLL;
3. computes the eight independent signed pair-orbit counts;
4. exponentially tilts the SAT training distribution so its pair-orbit means
   match the UNSAT training means;
5. applies the learned tilt to holdout SAT formulas and compares pair and
   predeclared cubic statistics to held-out UNSAT.

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


def gen_clause(q, rng):
    vs = rng.sample(range(q), 3)
    lits = [(v + 1) if rng.getrandbits(1) else -(v + 1) for v in vs]
    return tuple(sorted(lits, key=abs))


def gen_formula(q, t, rng):
    s = set()
    while len(s) < t:
        s.add(gen_clause(q, rng))
    return tuple(sorted(s))


def simplify(clauses, var, val):
    tl = var if val else -var
    fl = -tl
    out = []
    for c in clauses:
        if tl in c:
            continue
        if fl in c:
            nc = tuple(l for l in c if l != fl)
            if not nc:
                return None
            out.append(nc)
        else:
            out.append(c)
    return tuple(out)


def dpll_sat(clauses):
    def rec(cs):
        while True:
            if not cs:
                return True
            unit = None
            for c in cs:
                if len(c) == 0:
                    return False
                if len(c) == 1:
                    unit = c[0]
                    break
            if unit is None:
                break
            cs = simplify(cs, abs(unit), unit > 0)
            if cs is None:
                return False

        polarity = {}
        for c in cs:
            for l in c:
                v = abs(l)
                polarity[v] = polarity.get(v, 0) | (1 if l > 0 else 2)

        for v, mask in polarity.items():
            if mask in (1, 2):
                rr = simplify(cs, v, mask == 1)
                return False if rr is None else rec(rr)

        c = min(cs, key=len)
        l = c[0]
        v = abs(l)
        a = simplify(cs, v, l > 0)
        if a is not None and rec(a):
            return True
        b = simplify(cs, v, l < 0)
        return b is not None and rec(b)

    return rec(tuple(clauses))


def pair_features(formula, q):
    pos = [0] * q
    neg = [0] * q
    pair_groups = {}
    triple_groups = {}

    for c in formula:
        vs = tuple(abs(l) - 1 for l in c)
        sign = {abs(l) - 1: (1 if l > 0 else -1) for l in c}

        for l in c:
            if l > 0:
                pos[l - 1] += 1
            else:
                neg[-l - 1] += 1

        for a, b in itertools.combinations(vs, 2):
            if a > b:
                a, b = b, a
            pair_groups.setdefault((a, b), []).append((sign[a], sign[b]))

        key = tuple(sorted(vs))
        triple_groups.setdefault(key, []).append(tuple(sign[v] for v in key))

    s3 = [0, 0, 0, 0]
    for arr in triple_groups.values():
        for x, y in itertools.combinations(arr, 2):
            h = sum(a != b for a, b in zip(x, y))
            s3[h] += 1

    raw2 = [0, 0, 0]
    for arr in pair_groups.values():
        for x, y in itertools.combinations(arr, 2):
            h = (x[0] != y[0]) + (x[1] != y[1])
            raw2[h] += 1

    exact2 = raw2[:]
    for h, count in enumerate(s3):
        if count:
            exact2[0] -= count * math.comb(3 - h, 2)
            exact2[1] -= count * h * (3 - h)
            exact2[2] -= count * math.comb(h, 2)

    raw1_same = sum(math.comb(a, 2) + math.comb(b, 2) for a, b in zip(pos, neg))
    raw1_opp = sum(a * b for a, b in zip(pos, neg))

    ex1_same = raw1_same
    ex1_opp = raw1_opp
    for h, count in enumerate(exact2):
        ex1_same -= count * (2 - h)
        ex1_opp -= count * h
    for h, count in enumerate(s3):
        ex1_same -= count * (3 - h)
        ex1_opp -= count * h

    # 00 is determined by total number of clause pairs.
    return np.array([
        ex1_same, ex1_opp,
        exact2[0], exact2[1], exact2[2],
        s3[1], s3[2], s3[3],
    ], dtype=float)


def cubic_features(formula, q):
    pos = [0] * q
    neg = [0] * q
    for c in formula:
        for l in c:
            if l > 0:
                pos[l - 1] += 1
            else:
                neg[-l - 1] += 1

    def c2(x):
        return x * (x - 1) // 2

    def c3(x):
        return x * (x - 1) * (x - 2) // 6

    return np.array([
        sum(c2(a) * b + a * c2(b) for a, b in zip(pos, neg)),
        sum(c3(a) + c3(b) for a, b in zip(pos, neg)),
        sum(c3(a + b) for a, b in zip(pos, neg)),
        sum((a + b) ** 2 for a, b in zip(pos, neg)),
        sum((a * b) ** 2 for a, b in zip(pos, neg)),
    ], dtype=float)


def fit_tilt(rows):
    sat = [r for r in rows if r[0]]
    uns = [r for r in rows if not r[0]]
    xs = np.vstack([r[1] for r in sat])
    xu = np.vstack([r[1] for r in uns])

    mu = xs.mean(axis=0)
    sd = xs.std(axis=0)
    sd[sd == 0] = 1

    zs = (xs - mu) / sd
    zu = (xu - mu) / sd
    target = zu.mean(axis=0)

    def equations(lam):
        a = zs @ lam
        a -= a.max()
        w = np.exp(a)
        w /= w.sum()
        return (w[:, None] * zs).sum(axis=0) - target

    sol = root(equations, np.zeros(zs.shape[1]), method="hybr")
    lam = sol.x
    a = zs @ lam
    a -= a.max()
    w = np.exp(a)
    w /= w.sum()
    ess = 1.0 / np.dot(w, w)

    return {
        "success": bool(sol.success),
        "lambda": lam,
        "mu": mu,
        "sd": sd,
        "target": target,
        "train_uns": len(uns),
        "train_sat": len(sat),
        "train_ess": float(ess),
        "train_pair_max_abs_error": float(np.max(np.abs(equations(lam)))),
    }


def evaluate(rows, fit):
    sat = [r for r in rows if r[0]]
    uns = [r for r in rows if not r[0]]

    xs = np.vstack([r[1] for r in sat])
    xu = np.vstack([r[1] for r in uns])
    zs = (xs - fit["mu"]) / fit["sd"]
    zu = (xu - fit["mu"]) / fit["sd"]

    a = zs @ fit["lambda"]
    a -= a.max()
    w = np.exp(a)
    w /= w.sum()

    pair_diff = (w[:, None] * zs).sum(axis=0) - zu.mean(axis=0)

    cs = np.vstack([r[2] for r in sat])
    cu = np.vstack([r[2] for r in uns])
    cmu = cs.mean(axis=0)
    csd = cs.std(axis=0)
    csd[csd == 0] = 1

    zcs = (cs - cmu) / csd
    zcu = (cu - cmu) / csd
    cubic_diff = (w[:, None] * zcs).sum(axis=0) - zcu.mean(axis=0)

    return {
        "hold_uns": len(uns),
        "hold_sat": len(sat),
        "hold_ess": float(1.0 / np.dot(w, w)),
        "hold_pair_diff_sd": pair_diff.tolist(),
        "hold_pair_max_abs_sd": float(np.max(np.abs(pair_diff))),
        "hold_cubic_diff_sd": cubic_diff.tolist(),
        "hold_cubic_max_abs_sd": float(np.max(np.abs(cubic_diff))),
        "hold_cubic_mean_abs_sd": float(np.mean(np.abs(cubic_diff))),
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
            raise SystemExit("runtime guard: reached 25 seconds; split into a smaller chunk")
        f = gen_formula(q, t, rng)
        sat = dpll_sat(f)
        rows.append((sat, pair_features(f, q), cubic_features(f, q)))

    half = args.n // 2
    fit = fit_tilt(rows[:half])
    out = {
        "q": q,
        "t": t,
        "N": args.n,
        "seed": args.seed,
        "sample_seconds": time.time() - start,
        **{k: v for k, v in fit.items() if k not in ("lambda", "mu", "sd", "target")},
        **evaluate(rows[half:], fit),
        "status": "COMPUTATIONAL",
        "asymptotic_claim": "NONE",
    }
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
