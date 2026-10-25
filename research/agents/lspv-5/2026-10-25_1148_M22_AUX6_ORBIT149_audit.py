#!/usr/bin/env python3
"""Exact 0/1 MILP search for the r=3,a=6 uniform-sign M22 port gadget.

The selected positive/negative clauses are proper, unique, monotone triples.
Ports 0,1,2 have gadget degrees (1 positive, 2 negative), corresponding to
one already-used positive source occurrence.  Auxiliaries 3..8 have gadget
degrees (2,2).  Existential projection onto the ports is constrained to be
exactly {000,111}.
"""

from itertools import combinations, product
import json
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


NAMES = 9
PORTS = (0, 1, 2)
AUX = tuple(range(3, 9))
EDGES = tuple(combinations(range(NAMES), 3))
M = len(EDGES)


def build_model(enforce_nonconstant=True, require_zero=True, require_one=True):
    # xP[0:M], xN[M:2M], y0[2M:2M+6], y1[...]
    nv = 2 * M + 12
    rows = []
    lows = []
    highs = []

    def add(coeffs, lo=-np.inf, hi=np.inf):
        rows.append(coeffs)
        lows.append(lo)
        highs.append(hi)

    # Exact signed degrees.
    for v in range(NAMES):
        target_p = 1 if v in PORTS else 2
        target_n = 2
        add({i: 1 for i, e in enumerate(EDGES) if v in e}, target_p, target_p)
        add({M + i: 1 for i, e in enumerate(EDGES) if v in e}, target_n, target_n)

    # Every complete assignment extending a nonconstant port word must
    # falsify at least one selected clause.
    if enforce_nonconstant:
        for z in product((0, 1), repeat=3):
            if z in ((0, 0, 0), (1, 1, 1)):
                continue
            for y in product((0, 1), repeat=6):
                val = z + y
                coeffs = {}
                for i, e in enumerate(EDGES):
                    if all(val[v] == 0 for v in e):
                        coeffs[i] = 1
                    if all(val[v] == 1 for v in e):
                        coeffs[M + i] = 1
                add(coeffs, 1, np.inf)

    y0off = 2 * M
    y1off = y0off + 6

    # A selected positive clause must be satisfied by the chosen 000 witness.
    if require_zero:
        for i, e in enumerate(EDGES):
            coeffs = {i: 1}
            for v in e:
                if v in AUX:
                    coeffs[y0off + (v - 3)] = -1
            add(coeffs, -np.inf, 0)

    # For the 000 witness, negative clauses containing a port are automatic;
    # selected all-aux negative triples must contain a zero.
    if require_zero:
        for i, e in enumerate(EDGES):
            if all(v in AUX for v in e):
                coeffs = {M + i: 1}
                for v in e:
                    coeffs[y0off + (v - 3)] = 1
                add(coeffs, -np.inf, 3)

    # For the 111 witness, positive clauses containing a port are automatic;
    # selected all-aux positive triples must contain a one.
    if require_one:
        for i, e in enumerate(EDGES):
            if all(v in AUX for v in e):
                coeffs = {i: 1}
                for v in e:
                    coeffs[y1off + (v - 3)] = -1
                add(coeffs, -np.inf, 0)

    # Every selected negative clause must be satisfied by the 111 witness.
    if require_one:
        for i, e in enumerate(EDGES):
            aux_in_e = [v for v in e if v in AUX]
            coeffs = {M + i: 1}
            for v in aux_in_e:
                coeffs[y1off + (v - 3)] = 1
            add(coeffs, -np.inf, len(aux_in_e))

    A = lil_matrix((len(rows), nv), dtype=float)
    for r, coeffs in enumerate(rows):
        for c, value in coeffs.items():
            A[r, c] = value
    return np.zeros(nv), np.ones(nv, dtype=int), Bounds(0, 1), LinearConstraint(A.tocsr(), lows, highs)


def projection(pos, neg):
    out = []
    witnesses = {}
    for z in product((0, 1), repeat=3):
        ys = []
        for y in product((0, 1), repeat=6):
            val = z + y
            okp = all(any(val[v] for v in e) for e in pos)
            okn = all(any(not val[v] for v in e) for e in neg)
            if okp and okn:
                ys.append(y)
        if ys:
            out.append(z)
            witnesses[str(z)] = ys
    return out, witnesses


def witness_orbits():
    """Canonical (y0,y1) representatives under simultaneous S_6 action."""
    for n00 in range(7):
        for n01 in range(7 - n00):
            for n10 in range(7 - n00 - n01):
                n11 = 6 - n00 - n01 - n10
                pairs = [(0, 0)] * n00 + [(0, 1)] * n01
                pairs += [(1, 0)] * n10 + [(1, 1)] * n11
                yield (n00, n01, n10, n11), tuple(a for a, _ in pairs), tuple(b for _, b in pairs)


def fixed_witness_model(y0, y1):
    """Independent formulation with both constant witnesses fixed."""
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
        for y in product((0, 1), repeat=6):
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

    A = lil_matrix((len(rows), nv), dtype=float)
    for r, coeffs in enumerate(rows):
        for c, value in coeffs.items(): A[r, c] = value
    return np.zeros(nv), np.ones(nv, dtype=int), Bounds(0, 1), LinearConstraint(A.tocsr(), lows, highs)


def audit_fixed_witness_orbits():
    started = time.time()
    counts = {"optimal": 0, "infeasible": 0, "other": 0}
    feasible = []
    representatives = 0
    for signature, y0, y1 in witness_orbits():
        representatives += 1
        c, integ, bounds, constraint = fixed_witness_model(y0, y1)
        res = milp(c, integrality=integ, bounds=bounds, constraints=constraint,
                   options={"time_limit": 60, "presolve": True})
        if res.status == 0:
            counts["optimal"] += 1
            feasible.append(signature)
        elif res.status == 2:
            counts["infeasible"] += 1
        else:
            counts["other"] += 1
    return {
        "method": "84 simultaneous-S6 witness-pair orbit representatives",
        "representatives": representatives,
        "statuses": counts,
        "feasible_signatures": feasible,
        "elapsed_seconds": time.time() - started,
        "all_orbits_certified_infeasible": counts == {"optimal": 0, "infeasible": 84, "other": 0},
    }


def solve_case(name, **kwargs):
    c, integ, bounds, constraint = build_model(**kwargs)
    start = time.time()
    res = milp(c, integrality=integ, bounds=bounds, constraints=constraint,
               options={"time_limit": 600, "presolve": True})
    elapsed = time.time() - start
    result = {
        "case": name,
        "model": "r=3,a=6, each port has one pre-used positive occurrence",
        "variables": len(c),
        "candidate_supports_per_sign": M,
        "linear_constraints": int(constraint.A.shape[0]),
        "solver_status": int(res.status),
        "solver_message": res.message,
        "elapsed_seconds": elapsed,
        "success": bool(res.success),
    }
    if res.x is not None:
        pos = [EDGES[i] for i in range(M) if res.x[i] > 0.5]
        neg = [EDGES[i] for i in range(M) if res.x[M + i] > 0.5]
        proj, witnesses = projection(pos, neg)
        result.update({
            "positive_clauses": pos,
            "negative_clauses": neg,
            "positive_count": len(pos),
            "negative_count": len(neg),
            "projection": proj,
            "witness_counts": {k: len(v) for k, v in witnesses.items()},
            "first_witnesses": {k: v[0] for k, v in witnesses.items()},
            "degree_positive": [sum(v in e for e in pos) for v in range(NAMES)],
            "degree_negative": [sum(v in e for e in neg) for v in range(NAMES)],
            "verified_exact_equality": proj == [(0, 0, 0), (1, 1, 1)],
        })
    return result


def main():
    results = [
        solve_case("degree quotas only", enforce_nonconstant=False,
                   require_zero=False, require_one=False),
        solve_case("both constant port words extend", enforce_nonconstant=False,
                   require_zero=True, require_one=True),
        solve_case("exact equality projection", enforce_nonconstant=True,
                   require_zero=True, require_one=True),
    ]
    output = {
        "aggregate_models": results,
        "independent_fixed_witness_orbit_audit": audit_fixed_witness_orbits(),
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
