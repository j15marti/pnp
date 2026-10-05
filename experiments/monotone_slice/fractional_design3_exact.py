#!/usr/bin/env python3
"""FRACTIONAL-DESIGN3-EXACT.

Chunked exact order-three orbit census for exact-layer 3-SAT.

Modes:
  sample         Sample exact-t formulas and retain exact UNSAT instances.
  census         Compute exact canonical 3-clause orbit vectors for a pool slice.
  target         Compute an exact chunk of the uniform-slice order-3 target by
                 fixing one clause and enumerating pairs of remaining clauses.
  combine-target Combine explicit target chunk files.
  lp             Solve the numerical L_infinity distance from the exact target
                 to the convex hull of exact UNSAT orbit vectors.
  dual           Compute an L1-normalized numerical separating polynomial and
                 optionally validate it on fresh exact UNSAT vectors.

Every invocation has an internal runtime guard so larger work is decomposed
rather than given a longer timeout.

Status: COMPUTATIONAL, except the canonical-orbit and fixed-clause target
identities themselves, which are exact combinatorial constructions.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import pickle
import random
import time
from collections import Counter

import numpy as np
from scipy.optimize import linprog

PERMS = list(itertools.permutations(range(3)))

TRANS = {}
for a in (-1, 0, 1):
    for b in (-1, 0, 1):
        for c in (-1, 0, 1):
            if a == b == c == 0:
                continue
            v = (a, b, c)
            nv = tuple(-x for x in v)
            norm = min(v, nv)
            TRANS[v] = (norm[0] + 1) * 9 + (norm[1] + 1) * 3 + (norm[2] + 1)

PERM_CODE = {}
for v in TRANS:
    PERM_CODE[v] = [TRANS[(v[p[0]], v[p[1]], v[p[2]])] for p in PERMS]


def canonical_triple(c1, c2, c3):
    incidence = {}
    for j, clause in enumerate((c1, c2, c3)):
        for lit in clause:
            var = abs(lit)
            sign = 1 if lit > 0 else -1
            arr = incidence.setdefault(var, [0, 0, 0])
            arr[j] = sign

    permuted = [[] for _ in range(6)]
    for arr in incidence.values():
        codes = PERM_CODE[tuple(arr)]
        for i, code in enumerate(codes):
            permuted[i].append(code)
    return min(tuple(sorted(x)) for x in permuted)


def gen_clause(q, rng):
    vs = rng.sample(range(1, q + 1), 3)
    return tuple(sorted((v if rng.getrandbits(1) else -v for v in vs), key=abs))


def gen_formula(q, t, rng):
    clauses = set()
    while len(clauses) < t:
        clauses.add(gen_clause(q, rng))
    return tuple(sorted(clauses))


def simplify(clauses, var, val):
    true_lit = var if val else -var
    false_lit = -true_lit
    out = []
    for clause in clauses:
        if true_lit in clause:
            continue
        if false_lit in clause:
            new_clause = tuple(l for l in clause if l != false_lit)
            if not new_clause:
                return None
            out.append(new_clause)
        else:
            out.append(clause)
    return tuple(out)


def dpll_sat(clauses):
    def rec(cs):
        while True:
            if not cs:
                return True
            unit = None
            for clause in cs:
                if not clause:
                    return False
                if len(clause) == 1:
                    unit = clause[0]
                    break
            if unit is None:
                break
            cs = simplify(cs, abs(unit), unit > 0)
            if cs is None:
                return False

        polarity = {}
        for clause in cs:
            for lit in clause:
                v = abs(lit)
                polarity[v] = polarity.get(v, 0) | (1 if lit > 0 else 2)

        for v, mask in polarity.items():
            if mask in (1, 2):
                reduced = simplify(cs, v, mask == 1)
                return False if reduced is None else rec(reduced)

        clause = min(cs, key=len)
        lit = clause[0]
        v = abs(lit)
        left = simplify(cs, v, lit > 0)
        if left is not None and rec(left):
            return True
        right = simplify(cs, v, lit < 0)
        return right is not None and rec(right)

    return rec(tuple(clauses))


def clause_universe(q):
    out = []
    for vs in itertools.combinations(range(1, q + 1), 3):
        for bits in range(8):
            out.append(tuple(v if ((bits >> j) & 1) else -v for j, v in enumerate(vs)))
    return out


def read_census(files):
    rows = []
    for fn in files:
        with open(fn, "rb") as fh:
            obj = pickle.load(fh)
        pool_id = obj["pool_id"]
        for local_idx, counts in obj["rows"]:
            rows.append((pool_id, local_idx, counts))
    unique = {(pool_id, local_idx): counts for pool_id, local_idx, counts in rows}
    return list(unique.items())


def feature_matrix(rows, target_obj):
    keys = sorted(
        set(target_obj["target"])
        | {key for _, counts in rows for key in counts}
    )
    target = np.array([target_obj["target"].get(key, 0.0) for key in keys])
    X = np.array([
        [counts.get(key, 0) / sum(counts.values()) for key in keys]
        for _, counts in rows
    ])
    return keys, target, X


def minimax_lp(X, target):
    n, m = X.shape
    objective = np.r_[np.zeros(n), 1.0]
    A = []
    b = []
    for j in range(m):
        A.append(np.r_[X[:, j], -1.0])
        b.append(target[j])
        A.append(np.r_[-X[:, j], -1.0])
        b.append(-target[j])
    Aeq = np.array([np.r_[np.ones(n), 0.0]])
    beq = np.array([1.0])
    return linprog(
        objective,
        A_ub=np.array(A),
        b_ub=np.array(b),
        A_eq=Aeq,
        b_eq=beq,
        bounds=[(0, None)] * n + [(0, None)],
        method="highs",
    )


def dual_separator(X, target):
    n, m = X.shape
    D = target[None, :] - X
    # a = u-v, ||a||_1 <= 1; maximize delta.
    objective = np.r_[np.zeros(2 * m), -1.0]
    A = [np.r_[-D[i], D[i], 1.0] for i in range(n)]
    b = [0.0] * n
    A.append(np.r_[np.ones(2 * m), 0.0])
    b.append(1.0)
    result = linprog(
        objective,
        A_ub=np.array(A),
        b_ub=np.array(b),
        bounds=[(0, None)] * (2 * m) + [(None, None)],
        method="highs",
    )
    a = result.x[:m] - result.x[m:2 * m]
    return a, result.x[-1]


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("sample")
    p.add_argument("--q", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("census")
    p.add_argument("--pool", required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("target")
    p.add_argument("--q", type=int, required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("combine-target")
    p.add_argument("--q", type=int, required=True)
    p.add_argument("--parts", nargs="+", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("lp")
    p.add_argument("--census", nargs="+", required=True)
    p.add_argument("--target", required=True)

    p = sub.add_parser("dual")
    p.add_argument("--train-census", nargs="+", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--test-census", nargs="*", default=[])
    p.add_argument("--top", type=int, default=12)

    args = parser.parse_args()
    start_time = time.time()

    if args.mode == "sample":
        q = args.q
        t = round(3.5 * q)
        rng = random.Random(args.seed)
        unsat = []
        for i in range(args.n):
            if i % 100 == 0 and time.time() - start_time > 26:
                raise SystemExit("runtime guard: split sampling into a smaller chunk")
            formula = gen_formula(q, t, rng)
            if not dpll_sat(formula):
                unsat.append(formula)
        pool_id = f"q{q}-seed{args.seed}-N{args.n}"
        with open(args.out, "wb") as fh:
            pickle.dump(
                {"pool_id": pool_id, "q": q, "t": t, "N": args.n,
                 "seed": args.seed, "unsat": unsat},
                fh,
            )
        print(json.dumps({
            "mode": "sample", "pool_id": pool_id, "q": q, "N": args.n,
            "unsat": len(unsat), "seconds": time.time() - start_time,
        }))
        return

    if args.mode == "census":
        with open(args.pool, "rb") as fh:
            obj = pickle.load(fh)
        rows = []
        upper = min(args.end, len(obj["unsat"]))
        for idx in range(args.start, upper):
            formula = obj["unsat"][idx]
            counts = Counter()
            for i, j, k in itertools.combinations(range(len(formula)), 3):
                counts[canonical_triple(formula[i], formula[j], formula[k])] += 1
            rows.append((idx, counts))
            if time.time() - start_time > 26:
                raise SystemExit("runtime guard: split census into a smaller chunk")
        with open(args.out, "wb") as fh:
            pickle.dump(
                {"pool_id": obj["pool_id"], "q": obj["q"], "t": obj["t"],
                 "rows": rows},
                fh,
            )
        print(json.dumps({
            "mode": "census", "pool_id": obj["pool_id"],
            "start": args.start, "end": upper, "done": len(rows),
            "seconds": time.time() - start_time,
        }))
        return

    if args.mode == "target":
        q = args.q
        universe = clause_universe(q)
        fixed_clause = (1, 2, 3)
        fixed_idx = universe.index(fixed_clause)
        others = universe[:fixed_idx] + universe[fixed_idx + 1:]
        counts = Counter()
        pairs = 0
        upper = min(args.end, len(others))
        for a in range(args.start, upper):
            D = others[a]
            for b in range(a + 1, len(others)):
                counts[canonical_triple(fixed_clause, D, others[b])] += 1
                pairs += 1
            if time.time() - start_time > 26:
                raise SystemExit("runtime guard: split target enumeration")
        with open(args.out, "wb") as fh:
            pickle.dump(
                {"q": q, "start": args.start, "end": upper,
                 "pairs": pairs, "counts": counts},
                fh,
            )
        print(json.dumps({
            "mode": "target", "q": q, "start": args.start, "end": upper,
            "pairs": pairs, "orbits": len(counts),
            "seconds": time.time() - start_time,
        }))
        return

    if args.mode == "combine-target":
        counts = Counter()
        pairs = 0
        for fn in args.parts:
            with open(fn, "rb") as fh:
                obj = pickle.load(fh)
            counts.update(obj["counts"])
            pairs += obj["pairs"]
        target = {key: value / pairs for key, value in counts.items()}
        with open(args.out, "wb") as fh:
            pickle.dump(
                {"q": args.q, "pairs": pairs, "counts": counts, "target": target},
                fh,
            )
        print(json.dumps({
            "mode": "combine-target", "parts": len(args.parts),
            "pairs": pairs, "orbits": len(counts),
            "seconds": time.time() - start_time,
        }))
        return

    with open(args.target, "rb") as fh:
        target_obj = pickle.load(fh)

    if args.mode == "lp":
        rows = read_census(args.census)
        keys, target, X = feature_matrix(rows, target_obj)
        result = minimax_lp(X, target)
        weights = result.x[:-1]
        print(json.dumps({
            "mode": "lp", "rows": len(rows), "orbits": len(keys),
            "success": bool(result.success),
            "minimax": float(result.x[-1]),
            "support": int(np.sum(weights > 1e-9)),
            "ess": float(1.0 / np.dot(weights, weights)),
            "seconds": time.time() - start_time,
            "status": "COMPUTATIONAL_NUMERICAL_LP",
        }))
        return

    train_rows = read_census(args.train_census)
    keys, target, X = feature_matrix(train_rows, target_obj)
    a, margin = dual_separator(X, target)
    top_idx = np.argsort(-np.abs(a))[: args.top]
    out = {
        "mode": "dual", "train_rows": len(train_rows),
        "orbits": len(keys), "margin": float(margin),
        "top": [
            {"orbit": repr(keys[j]), "coefficient": float(a[j]),
             "target_frequency": float(target[j])}
            for j in top_idx if abs(a[j]) > 1e-12
        ],
        "seconds": time.time() - start_time,
        "status": "COMPUTATIONAL_NUMERICAL_DUAL",
    }

    if args.test_census:
        test_rows = read_census(args.test_census)
        test_keys, test_target, Y = feature_matrix(test_rows, target_obj)
        if test_keys != keys:
            raise SystemExit("orbit-key mismatch between train and test")
        margins = (test_target[None, :] - Y) @ a
        out.update({
            "test_rows": len(test_rows),
            "test_min_margin": float(margins.min()),
            "test_mean_margin": float(margins.mean()),
            "test_violations": int(np.sum(margins <= 0)),
            "test_violation_fraction": float(np.mean(margins <= 0)),
        })

    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
