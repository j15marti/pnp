#!/usr/bin/env python3
"""XOR-FRACTIONAL-DESIGN3-CONTROL.

Hostile control for the SLICE-UNSAT fractional-design program.

At a nondegenerate density for the Gaussian-elimination-easy parity shadow:
1. sample exact-weight proper 3-CNF clause sets;
2. label each by consistency of the induced GF(2) 3-XOR system;
3. compute the exact canonical three-clause orbit vector of every sample;
4. use the empirical XOR-SAT mean vector as the negative target;
5. compute its L_infinity distance to the convex hull of XOR-UNSAT vectors.

One invocation is bounded to N <= 10000 and is intended to remain below
roughly 30 seconds.

Status: COMPUTATIONAL hostile control.
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
import time
import json
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
PERM_CODE = {
    v: [TRANS[(v[p[0]], v[p[1]], v[p[2]])] for p in PERMS]
    for v in TRANS
}


def canonical_triple(cset):
    best = None
    for p in PERMS:
        incidence = {}
        for j, idx in enumerate(p):
            for lit in cset[idx]:
                var = abs(lit)
                sign = 1 if lit > 0 else -1
                incidence.setdefault(var, [0, 0, 0])[j] = sign
        pats = []
        for vec in incidence.values():
            a = tuple(vec)
            b = tuple(-x for x in vec)
            pats.append(a if a < b else b)
        key = tuple(sorted(pats))
        if best is None or key < best:
            best = key
    return best


def gen_clause(q, rng):
    vs = rng.sample(range(1, q + 1), 3)
    return tuple(sorted((v if rng.getrandbits(1) else -v for v in vs), key=abs))


def gen_formula(q, t, rng):
    s = set()
    while len(s) < t:
        s.add(gen_clause(q, rng))
    return tuple(sorted(s))


def xor_unsat(formula, q):
    rows = []
    for clause in formula:
        mask = 0
        rhs = 0
        for lit in clause:
            mask ^= 1 << (abs(lit) - 1)
            rhs ^= 1 if lit < 0 else 0
        rows.append([mask, rhs])

    pivot = 0
    for bit in range(q):
        row = next(
            (j for j in range(pivot, len(rows)) if (rows[j][0] >> bit) & 1),
            None,
        )
        if row is None:
            continue
        rows[pivot], rows[row] = rows[row], rows[pivot]
        pmask, prhs = rows[pivot]
        for j in range(len(rows)):
            if j != pivot and ((rows[j][0] >> bit) & 1):
                rows[j][0] ^= pmask
                rows[j][1] ^= prhs
        pivot += 1

    return any(mask == 0 and rhs for mask, rhs in rows)


def orbit_counts(formula):
    counts = Counter()
    for i, j, k in itertools.combinations(range(len(formula)), 3):
        counts[canonical_triple((formula[i], formula[j], formula[k]))] += 1
    return counts


def minimax_distance(pos, target):
    n, m = pos.shape
    objective = np.r_[np.zeros(n), 1.0]
    A = []
    b = []
    for j in range(m):
        A.append(np.r_[pos[:, j], -1.0])
        b.append(target[j])
        A.append(np.r_[-pos[:, j], -1.0])
        b.append(-target[j])

    result = linprog(
        objective,
        A_ub=np.array(A),
        b_ub=np.array(b),
        A_eq=np.array([np.r_[np.ones(n), 0.0]]),
        b_eq=np.array([1.0]),
        bounds=[(0, None)] * n + [(0, None)],
        method="highs",
    )
    weights = result.x[:-1]
    return float(result.x[-1]), int(np.sum(weights > 1e-9))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--density", type=float, default=0.9)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()

    if args.n > 10000:
        raise SystemExit("runtime guard: split N > 10000 into multiple invocations")

    start = time.time()
    q = args.q
    t = round(args.density * q)
    rng = random.Random(args.seed)

    pos = []
    neg = []
    all_keys = set()

    for _ in range(args.n):
        if time.time() - start > 25:
            raise SystemExit("runtime guard: reduce this chunk")
        formula = gen_formula(q, t, rng)
        counts = orbit_counts(formula)
        all_keys.update(counts)
        row = (counts, math.comb(t, 3))
        if xor_unsat(formula, q):
            pos.append(row)
        else:
            neg.append(row)

    keys = sorted(all_keys)

    def matrix(rows):
        return np.array([
            [counts.get(key, 0) / den for key in keys]
            for counts, den in rows
        ])

    P = matrix(pos)
    Q = matrix(neg)
    target = Q.mean(axis=0)

    residual, support = minimax_distance(P, target)

    print(json.dumps({
        "q": q,
        "t": t,
        "density": args.density,
        "N": args.n,
        "seed": args.seed,
        "xor_unsat": len(pos),
        "xor_sat": len(neg),
        "orbits": len(keys),
        "minimax": residual,
        "support": support,
        "elapsed_seconds": time.time() - start,
        "status": "COMPUTATIONAL_HOSTILE_CONTROL",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
