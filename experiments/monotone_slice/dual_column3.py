#!/usr/bin/env python3
"""DUAL-COLUMN3.

One dual-guided column-generation iteration for the exact order-three
fractional-design experiment.

Inputs:
- exact target file from fractional_design3_exact.py;
- exact census chunk files, each carrying a pool_id;
- pool mappings pool_id=pickle_path;
- optional persistent added-column file.

The script solves the current L1-normalized dual separator, starts from the
known UNSAT formula with smallest signed margin, and performs random exact-
weight clause swaps. SAT-preserving proposals are rejected; every accepted
candidate is exactly re-censused. If a violating UNSAT formula is found it is
appended to the persistent added-column file.

Each invocation has a 25-second runtime guard. Status: COMPUTATIONAL.
"""

from __future__ import annotations

import argparse
import itertools
import json
import pickle
import random
import time
from collections import Counter

import numpy as np
from scipy.optimize import linprog

from experiments.monotone_slice.fractional_design3_exact import (
    canonical_triple,
    clause_universe,
    dpll_sat,
)


def exact_counts(formula):
    counts = Counter()
    for i, j, k in itertools.combinations(range(len(formula)), 3):
        counts[canonical_triple(formula[i], formula[j], formula[k])] += 1
    return counts


def read_base(census_files, pool_map):
    rows = []
    formulas = []
    seen = set()

    pools = {}
    for pool_id, path in pool_map.items():
        with open(path, "rb") as fh:
            pools[pool_id] = pickle.load(fh)

    for fn in census_files:
        with open(fn, "rb") as fh:
            obj = pickle.load(fh)
        pool_id = obj["pool_id"]
        for local_idx, counts in obj["rows"]:
            ident = (pool_id, local_idx)
            if ident in seen:
                continue
            seen.add(ident)
            rows.append(counts)
            formulas.append(pools[pool_id]["unsat"][local_idx])

    return rows, formulas


def dual_separator(X, target):
    n, m = X.shape
    D = target[None, :] - X
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
    return a, float(result.x[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--census", nargs="+", required=True)
    ap.add_argument("--pool", action="append", required=True,
                    help="pool_id=pickle_path; repeat for each base pool")
    ap.add_argument("--added", required=True,
                    help="persistent pickle containing a list of added formulas")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--steps", type=int, default=120)
    args = ap.parse_args()

    start = time.time()

    pool_map = {}
    for item in args.pool:
        pool_id, path = item.split("=", 1)
        pool_map[pool_id] = path

    with open(args.target, "rb") as fh:
        target_obj = pickle.load(fh)

    rows, formulas = read_base(args.census, pool_map)

    try:
        with open(args.added, "rb") as fh:
            added = pickle.load(fh)
    except FileNotFoundError:
        added = []

    for formula in added:
        rows.append(exact_counts(formula))
        formulas.append(formula)

    keys = sorted(
        set(target_obj["target"])
        | {key for counts in rows for key in counts}
    )
    target = np.array([target_obj["target"].get(key, 0.0) for key in keys])
    X = np.array([
        [counts.get(key, 0) / sum(counts.values()) for key in keys]
        for counts in rows
    ])

    a, dual_margin = dual_separator(X, target)
    margins = (target[None, :] - X) @ a
    start_idx = int(np.argmin(margins))
    current = list(formulas[start_idx])
    current_set = set(current)

    def score(formula):
        counts = exact_counts(formula)
        x = np.array([
            counts.get(key, 0) / sum(counts.values())
            for key in keys
        ])
        return float((target - x) @ a)

    current_margin = float(margins[start_idx])
    best_formula = tuple(current)
    best_margin = current_margin
    accepted = 0
    unsat_scored = 0

    q = target_obj["q"]
    universe = clause_universe(q)
    rng = random.Random(args.seed)

    for _ in range(args.steps):
        if time.time() - start > 25:
            break

        remove_idx = rng.randrange(len(current))
        add_clause = universe[rng.randrange(len(universe))]
        if add_clause in current_set:
            continue

        old_clause = current[remove_idx]
        proposal = current.copy()
        proposal[remove_idx] = add_clause
        proposal = sorted(proposal)

        if dpll_sat(tuple(proposal)):
            continue

        unsat_scored += 1
        proposal_margin = score(proposal)

        if proposal_margin < current_margin:
            current_set.remove(old_clause)
            current_set.add(add_clause)
            current = proposal
            current_margin = proposal_margin
            accepted += 1

            if proposal_margin < best_margin:
                best_margin = proposal_margin
                best_formula = tuple(proposal)

            if proposal_margin <= 0:
                break

    violating = best_margin <= 0
    before = len(added)

    if violating:
        added.append(best_formula)
        with open(args.added, "wb") as fh:
            pickle.dump(added, fh)

    print(json.dumps({
        "seed": args.seed,
        "columns_before": len(rows),
        "added_before": before,
        "dual_margin": dual_margin,
        "start_margin": float(margins[start_idx]),
        "best_margin": best_margin,
        "violating": violating,
        "accepted_moves": accepted,
        "unsat_proposals_scored": unsat_scored,
        "added_after": len(added),
        "elapsed_seconds": time.time() - start,
        "status": "COMPUTATIONAL",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
