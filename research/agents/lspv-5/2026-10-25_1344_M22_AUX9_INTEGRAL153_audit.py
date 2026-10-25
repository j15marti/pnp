#!/usr/bin/env python3
"""Exact/relaxed feasibility audit for the r=3,a=9 uniform-sign M22 port block.

Ports 0,1,2 have already used one positive source occurrence, hence the
standalone block must give them signed degrees (1,2).  Private auxiliaries
3,...,11 have degrees (2,2).  Every clause is a unique proper pure-sign
ternary clause.  The exact case asks for existential port projection
{000,111}; the controls retain only degrees, or degrees plus witnesses for
the two constant port words.  Each solver call has a 25-second limit.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
import json
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


A = 9
NAMES = A + 3
PORTS = (0, 1, 2)
AUX = tuple(range(3, NAMES))
EDGES = tuple(combinations(range(NAMES), 3))
M = len(EDGES)


def build_model(enforce_nonconstant: bool, require_zero: bool, require_one: bool):
    # xP[0:M], xN[M:2M], y0[2M:2M+A], y1[...]
    nv = 2 * M + 2 * A
    rows: list[dict[int, float]] = []
    lows: list[float] = []
    highs: list[float] = []

    def add(coeffs, lo=-np.inf, hi=np.inf):
        rows.append(coeffs); lows.append(lo); highs.append(hi)

    for v in range(NAMES):
        tp = 1 if v in PORTS else 2
        add({i: 1 for i, e in enumerate(EDGES) if v in e}, tp, tp)
        add({M + i: 1 for i, e in enumerate(EDGES) if v in e}, 2, 2)

    if enforce_nonconstant:
        for z in product((0, 1), repeat=3):
            if z in ((0, 0, 0), (1, 1, 1)):
                continue
            for y in product((0, 1), repeat=A):
                val = z + y
                coeffs: dict[int, float] = {}
                for i, e in enumerate(EDGES):
                    if all(val[v] == 0 for v in e): coeffs[i] = 1
                    if all(val[v] == 1 for v in e): coeffs[M + i] = 1
                add(coeffs, 1, np.inf)

    y0off = 2 * M
    y1off = y0off + A

    if require_zero:
        # Each selected positive clause must contain a 1 in the 000 witness.
        for i, e in enumerate(EDGES):
            coeffs = {i: 1}
            for v in e:
                if v in AUX: coeffs[y0off + v - 3] = -1
            add(coeffs, -np.inf, 0)
        # Only all-aux negative clauses can fail at ports 000.
        for i, e in enumerate(EDGES):
            if all(v in AUX for v in e):
                coeffs = {M + i: 1}
                for v in e: coeffs[y0off + v - 3] = 1
                add(coeffs, -np.inf, 3)

    if require_one:
        # Only all-aux positive clauses can fail at ports 111.
        for i, e in enumerate(EDGES):
            if all(v in AUX for v in e):
                coeffs = {i: 1}
                for v in e: coeffs[y1off + v - 3] = -1
                add(coeffs, -np.inf, 0)
        # Every selected negative clause must contain a 0 in the 111 witness.
        for i, e in enumerate(EDGES):
            av = [v for v in e if v in AUX]
            coeffs = {M + i: 1}
            for v in av: coeffs[y1off + v - 3] = 1
            add(coeffs, -np.inf, len(av))

    mat = lil_matrix((len(rows), nv), dtype=float)
    for r, coeffs in enumerate(rows):
        for c, value in coeffs.items(): mat[r, c] = value
    return np.zeros(nv), Bounds(0, 1), LinearConstraint(mat.tocsr(), lows, highs)


def projection(pos, neg):
    out = []
    witness_counts = {}
    first = {}
    for z in product((0, 1), repeat=3):
        count = 0
        first_y = None
        for y in product((0, 1), repeat=A):
            val = z + y
            okp = all(any(val[v] for v in e) for e in pos)
            okn = all(any(not val[v] for v in e) for e in neg)
            if okp and okn:
                count += 1
                if first_y is None: first_y = y
        if count:
            out.append(z)
            witness_counts["".join(map(str, z))] = count
            first["".join(map(str, z))] = first_y
    return out, witness_counts, first


def witness_orbits():
    """Canonical (y0,y1) pairs under simultaneous permutations of 9 auxiliaries."""
    for n00 in range(A + 1):
        for n01 in range(A + 1 - n00):
            for n10 in range(A + 1 - n00 - n01):
                n11 = A - n00 - n01 - n10
                pairs = [(0, 0)] * n00 + [(0, 1)] * n01
                pairs += [(1, 0)] * n10 + [(1, 1)] * n11
                yield (n00, n01, n10, n11), tuple(x for x, _ in pairs), tuple(y for _, y in pairs)


def fixed_witness_model(y0, y1):
    """Binary clause-selection model with both constant-word witnesses fixed."""
    nv = 2 * M
    rows, lows, highs = [], [], []

    def add(coeffs, lo=-np.inf, hi=np.inf):
        rows.append(coeffs); lows.append(lo); highs.append(hi)

    for v in range(NAMES):
        tp = 1 if v in PORTS else 2
        add({i: 1 for i, e in enumerate(EDGES) if v in e}, tp, tp)
        add({M + i: 1 for i, e in enumerate(EDGES) if v in e}, 2, 2)

    for z in product((0, 1), repeat=3):
        if z in ((0, 0, 0), (1, 1, 1)):
            continue
        for y in product((0, 1), repeat=A):
            val = z + y
            coeffs = {}
            for i, e in enumerate(EDGES):
                if all(val[v] == 0 for v in e): coeffs[i] = 1
                if all(val[v] == 1 for v in e): coeffs[M + i] = 1
            add(coeffs, 1, np.inf)

    val0 = (0, 0, 0) + tuple(y0)
    val1 = (1, 1, 1) + tuple(y1)
    for i, e in enumerate(EDGES):
        if all(val0[v] == 0 for v in e): add({i: 1}, 0, 0)
        if all(val0[v] == 1 for v in e): add({M + i: 1}, 0, 0)
        if all(val1[v] == 0 for v in e): add({i: 1}, 0, 0)
        if all(val1[v] == 1 for v in e): add({M + i: 1}, 0, 0)

    mat = lil_matrix((len(rows), nv), dtype=float)
    for r, coeffs in enumerate(rows):
        for c, value in coeffs.items(): mat[r, c] = value
    return np.zeros(nv), Bounds(0, 1), LinearConstraint(mat.tocsr(), lows, highs)


def solve_orbit_chunk(start: int, end: int, per_orbit_time: float, relaxed: bool):
    orbits = list(witness_orbits())
    selected = orbits[start:end]
    records = []
    counts = {"optimal": 0, "infeasible": 0, "limit": 0, "other": 0}
    began = time.time()
    for idx, (signature, y0, y1) in enumerate(selected, start=start):
        c, bounds, constraint = fixed_witness_model(y0, y1)
        integ = np.zeros(len(c), dtype=int) if relaxed else np.ones(len(c), dtype=int)
        res = milp(c, integrality=integ, bounds=bounds,
                   constraints=constraint,
                   options={"time_limit": per_orbit_time, "presolve": True,
                            "mip_rel_gap": 0.0})
        label = {0: "optimal", 1: "limit", 2: "infeasible"}.get(int(res.status), "other")
        counts[label] += 1
        rec = {"index": idx, "signature": signature, "status": int(res.status),
               "label": label, "message": res.message}
        if res.x is not None:
            rec["max_fractionality"] = float(np.max(np.abs(res.x - np.rint(res.x))))
        if res.x is not None and res.status == 0 and not relaxed:
            pos = [EDGES[i] for i in range(M) if res.x[i] > 0.5]
            neg = [EDGES[i] for i in range(M) if res.x[M + i] > 0.5]
            proj, wc, first = projection(pos, neg)
            rec.update({"positive_clauses": pos, "negative_clauses": neg,
                        "projection": proj, "witness_counts": wc,
                        "first_witnesses": first,
                        "verified_exact_equality": proj == [(0, 0, 0), (1, 1, 1)]})
        records.append(rec)
    return {"model": "fixed-witness simultaneous-S9 orbit audit",
            "relaxed": relaxed,
            "total_orbits": len(orbits), "start": start, "end": end,
            "per_orbit_time_limit": per_orbit_time, "counts": counts,
            "elapsed_seconds": time.time() - began, "records": records}


def solve(case: str, relaxed: bool):
    flags = {
        "degree": (False, False, False),
        "constants": (False, True, True),
        "exact": (True, True, True),
    }[case]
    c, bounds, constraint = build_model(*flags)
    integrality = np.zeros(len(c), dtype=int) if relaxed else np.ones(len(c), dtype=int)
    started = time.time()
    res = milp(c, integrality=integrality, bounds=bounds, constraints=constraint,
               options={"time_limit": 25, "presolve": True, "mip_rel_gap": 0.0})
    result = {
        "case": case,
        "relaxed": relaxed,
        "model": "r=3,a=9; port block degrees (+1,-2), aux (+2,-2)",
        "variables": len(c),
        "candidate_supports_per_sign": M,
        "linear_constraints": int(constraint.A.shape[0]),
        "solver_status": int(res.status),
        "solver_message": res.message,
        "elapsed_seconds": time.time() - started,
        "success": bool(res.success),
    }
    if res.x is not None:
        result["max_fractionality"] = float(np.max(np.abs(res.x - np.rint(res.x))))
        result["objective"] = float(res.fun)
        if not relaxed and res.status == 0:
            pos = [EDGES[i] for i in range(M) if res.x[i] > 0.5]
            neg = [EDGES[i] for i in range(M) if res.x[M + i] > 0.5]
            proj, counts, first = projection(pos, neg)
            result.update({
                "positive_clauses": pos,
                "negative_clauses": neg,
                "projection": proj,
                "witness_counts": counts,
                "first_witnesses": first,
                "degree_positive": [sum(v in e for e in pos) for v in range(NAMES)],
                "degree_negative": [sum(v in e for e in neg) for v in range(NAMES)],
                "verified_exact_equality": proj == [(0, 0, 0), (1, 1, 1)],
            })
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=("degree", "constants", "exact", "orbits"), required=True)
    ap.add_argument("--relaxed", action="store_true")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=10)
    ap.add_argument("--per-orbit-time", type=float, default=2.0)
    args = ap.parse_args()
    if args.case == "orbits":
        result = solve_orbit_chunk(args.start, args.end, args.per_orbit_time, args.relaxed)
    else:
        result = solve(args.case, args.relaxed)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
