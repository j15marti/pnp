#!/usr/bin/env python3
"""SLICEPAD1 verifier.

Verifies algebraic padding inequalities and runs deterministic randomized
small-instance sanity checks for sparse and middle-slice 3-CNF padding.

Computational evidence only. Symbolic proofs are in the SLICEPAD1 report.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb
import random

SEED = 20261004
N_MIN = 3
N_MAX = 6
TRIALS_PER_VARIANT_PER_N = 50

Clause = tuple[tuple[int, bool], tuple[int, bool], tuple[int, bool]]


def all_proper_clauses(q: int) -> list[Clause]:
    out: list[Clause] = []
    for vars3 in combinations(range(q), 3):
        for signs in product([False, True], repeat=3):
            out.append(tuple(zip(vars3, signs)))
    return out


def clause_satisfied(clause: Clause, assignment: tuple[bool, ...]) -> bool:
    return any(
        assignment[var] if positive else (not assignment[var])
        for var, positive in clause
    )


def formula_satisfiable(formula: list[Clause], q: int) -> bool:
    for assignment in product([False, True], repeat=q):
        if all(clause_satisfied(clause, assignment) for clause in formula):
            return True
    return False


def random_bounded_formula(n: int, rng: random.Random) -> list[Clause]:
    """Generate a proper 3-CNF with variable occurrence at most four."""
    clauses = all_proper_clauses(n)
    rng.shuffle(clauses)
    occurrence = [0] * n
    target = rng.randint(1, max(1, (4 * n) // 3))
    chosen: list[Clause] = []

    for clause in clauses:
        variables = [var for var, _ in clause]
        if all(occurrence[var] < 4 for var in variables):
            chosen.append(clause)
            for var in variables:
                occurrence[var] += 1
            if len(chosen) == target:
                break

    assert all(x <= 4 for x in occurrence)
    assert len(chosen) <= (4 * n) // 3
    return chosen


def filler_pool(n: int) -> tuple[list[Clause], int]:
    q = 2 * n
    controls = set(range(n, q))
    pool = [
        clause
        for clause in all_proper_clauses(q)
        if any(var in controls and positive for var, positive in clause)
    ]
    return pool, q


def pad_formula(formula: list[Clause], n: int, target: int) -> tuple[list[Clause], int]:
    pool, q = filler_pool(n)
    need = target - len(formula)
    assert need >= 0
    assert need <= len(pool)
    padded = formula + pool[:need]
    assert len(set(padded)) == len(padded)
    return padded, q


def exact_counts(n: int) -> tuple[int, int, int]:
    q = 2 * n
    M = 8 * comb(q, 3)
    R = 9 * comb(n, 3) + 6 * n * comb(n, 2)
    P = M - R
    return M, R, P


def main() -> None:
    rng = random.Random(SEED)

    print("SLICEPAD1 verifier")
    print(f"seed={SEED}")
    print(f"n_range={N_MIN}..{N_MAX}")
    print(f"trials_per_variant_per_n={TRIALS_PER_VARIANT_PER_N}")
    print()

    total = 0
    for n in range(N_MIN, N_MAX + 1):
        q = 2 * n
        M, R, P = exact_counts(n)
        identity_rhs = n * (n - 1) * (5 * n + 2) // 3
        assert M - 2 * R == identity_rhs
        assert identity_rhs > 0
        assert P > M // 2

        t_middle = M // 2
        t_sparse = 6 * q
        assert t_sparse <= P

        print(
            f"n={n} q={q} M={M} R={R} P={P} "
            f"M-2R={M - 2*R} middle={t_middle} sparse={t_sparse}"
        )

        for label, target in (("middle", t_middle), ("sparse", t_sparse)):
            passed = 0
            for _ in range(TRIALS_PER_VARIANT_PER_N):
                source = random_bounded_formula(n, rng)
                padded, padded_q = pad_formula(source, n, target)

                source_sat = formula_satisfiable(source, n)
                padded_sat = formula_satisfiable(padded, padded_q)

                assert len(padded) == target
                assert source_sat == padded_sat
                passed += 1
                total += 1

            print(
                f"  {label}: {passed}/{TRIALS_PER_VARIANT_PER_N} "
                "SAT-equivalence checks passed"
            )

    density_base = 2.0 * (7.0 / 8.0) ** 6
    assert density_base < 1.0
    print()
    print(f"union_bound_base=2*(7/8)^6={density_base:.15f}<1")
    print(f"TOTAL_CHECKS={total}")
    print("STATUS=PASS")


if __name__ == "__main__":
    main()
