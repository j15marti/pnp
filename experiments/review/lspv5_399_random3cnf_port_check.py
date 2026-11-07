#!/usr/bin/env python3
"""Finite controls for REFEREE399 random proper-3-CNF source port.

This is an independent finite checker, not the authoritative R_mix341 checker
and not a proof that any sampled formula is UNSAT or proof-size hard.
"""

from __future__ import annotations

import itertools
import json
import math
import random


def universe(n: int):
    return [
        tuple((v if bit else -v) for v, bit in zip(vs, signs))
        for vs in itertools.combinations(range(1, n + 1), 3)
        for signs in itertools.product((0, 1), repeat=3)
    ]


def clause_sat(clause, assignment):
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def clause_polynomial_value(clause, assignment):
    # p_C=prod(1-x_i) for positive literals and prod(x_i) for negative ones.
    out = 1
    for lit in clause:
        x = int(assignment[abs(lit) - 1])
        out *= (1 - x) if lit > 0 else x
    return out


def with_replacement(n: int, m: int, seed: int):
    rng = random.Random(seed)
    u = universe(n)
    return [rng.choice(u) for _ in range(m)]


def without_replacement(n: int, m: int, seed: int):
    rng = random.Random(seed)
    return rng.sample(universe(n), m)


def collision_union_bound(n: int, m: int):
    M = 8 * math.comb(n, 3)
    return math.comb(m, 2) / M


def exact_collision_probability(n: int, m: int):
    M = 8 * math.comb(n, 3)
    if m > M:
        return 1.0
    log_no = sum(math.log1p(-j / M) for j in range(m))
    return 1.0 - math.exp(log_no)


def main():
    assertions = 0
    encoding_cases = 0
    sample_rows = []

    for n in range(3, 8):
        u = universe(n)
        assert len(u) == 8 * math.comb(n, 3)
        assert len(set(u)) == len(u)
        assertions += 2
        for clause in u:
            assert len({abs(x) for x in clause}) == 3
            for a in itertools.product((False, True), repeat=n):
                assert clause_sat(clause, a) == (clause_polynomial_value(clause, a) == 0)
                assertions += 1
                encoding_cases += 1

    for n in (30, 60, 120, 240, 480, 960):
        m = 6 * n
        ub = collision_union_bound(n, m)
        exact = exact_collision_probability(n, m)
        assert 0 <= exact <= ub
        assertions += 1
        # Materializing all 8*C(n,3) clauses is intentionally confined to the
        # small control n=30; the asymptotic rows use the closed forms only.
        if n == 30:
            assert all(len(set(map(abs, c))) == 3 for c in with_replacement(n, m, n))
            assert len(set(without_replacement(n, m, n))) == m
            assertions += 2
        sample_rows.append({
            "n": n,
            "m": m,
            "universe": 8 * math.comb(n, 3),
            "exact_collision_probability": exact,
            "union_bound": ub,
            "n_times_union_bound": n * ub,
        })

    # Corruption controls: malformed width, repeated variable, bad polynomial orientation.
    corruptions_rejected = 0
    bad = [(1, 2), (1, -1, 2), (1, 2, 3, 4)]
    for clause in bad:
        try:
            assert len(clause) == 3 and len(set(map(abs, clause))) == 3
        except AssertionError:
            corruptions_rejected += 1
    for a in itertools.product((False, True), repeat=3):
        c = (1, 2, 3)
        wrong = math.prod(int(a[abs(l) - 1]) if l > 0 else 1 - int(a[abs(l) - 1]) for l in c)
        if clause_sat(c, a) != (wrong == 0):
            corruptions_rejected += 1
            break
    assert corruptions_rejected == 4
    assertions += 1

    result = {
        "status": "COMPUTATIONAL_FINITE_CONTROLS_PLUS_SYMBOLIC_TV_LEMMA_IN_REPORT",
        "assertions": assertions,
        "encoding_truth_table_cases": encoding_cases,
        "corruptions_rejected": corruptions_rejected,
        "density": 6,
        "sampling": {
            "published_AR03": "ordered iid proper signed 3-clauses, repetitions allowed",
            "cnfgen_24e633b": "uniform without repetition",
            "symbolic_bridge": "condition iid sample on no collision; TV <= C(m,2)/(8*C(n,3)) = O(1/n) for m=6n",
        },
        "rows": sample_rows,
        "limitations": [
            "no sampled formula certified UNSAT",
            "no sampled formula certified proof-size hard",
            "not the authoritative historical R_mix341 checker",
            "finite checks do not prove asymptotics",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
