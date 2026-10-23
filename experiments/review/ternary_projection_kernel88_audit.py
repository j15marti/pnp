#!/usr/bin/env python3
"""Finite audit for the exact 2-CNF projection kernel in Ladder 88.

This is an implementation check, not an asymptotic lower bound.
"""

from __future__ import annotations

import itertools
import json
import random
import time


SEED = 20261023


def lit_value(lit: int, assignment: tuple[bool, ...]) -> bool:
    value = assignment[abs(lit) - 1]
    return value if lit > 0 else not value


def formula_value(clauses: list[tuple[int, ...]], assignment: tuple[bool, ...]) -> bool:
    return all(any(lit_value(lit, assignment) for lit in clause) for clause in clauses)


def brute_sat(clauses: list[tuple[int, ...]], nvars: int, assumptions: tuple[int, ...] = ()) -> bool:
    extended = clauses + [(lit,) for lit in assumptions]
    return any(formula_value(extended, bits) for bits in itertools.product((False, True), repeat=nvars))


def all_candidates(s: int) -> list[tuple[int, ...]]:
    literals = [lit for var in range(1, s + 1) for lit in (var, -var)]
    candidates: list[tuple[int, ...]] = [(lit,) for lit in literals]
    for i, left in enumerate(literals):
        for right in literals[i + 1 :]:
            if left != -right:
                candidates.append((left, right))
    assert len(candidates) == 2 * s * s
    return candidates


def exact_projection(clauses: list[tuple[int, ...]], nvars: int, s: int):
    calls = 1
    if not brute_sat(clauses, nvars):
        return False, [], calls
    projected: list[tuple[int, ...]] = []
    for clause in all_candidates(s):
        calls += 1
        assumptions = tuple(-lit for lit in clause)
        if not brute_sat(clauses, nvars, assumptions):
            projected.append(clause)
    return True, projected, calls


def has_extension(clauses: list[tuple[int, ...]], nvars: int, prefix: tuple[bool, ...]) -> bool:
    for suffix in itertools.product((False, True), repeat=nvars - len(prefix)):
        if formula_value(clauses, prefix + suffix):
            return True
    return False


def random_clause(rng: random.Random, nvars: int, width: int) -> tuple[int, ...]:
    variables = rng.sample(range(1, nvars + 1), width)
    return tuple(var if rng.randrange(2) else -var for var in variables)


def main() -> None:
    rng = random.Random(SEED)
    started = time.perf_counter()
    instances = 0
    assignments_checked = 0
    projection_clauses = 0
    oracle_calls = 0
    assertions = 0
    sat_controls = 0
    unsat_controls = 0

    # Fixed controls include SAT, UNSAT, source-sharing, and implication chains.
    controls = [
        (2, 1, [(1, 2)]),
        (2, 1, [(1,), (-1,)]),
        (3, 2, [(-1, 3), (-3, 2)]),
        (4, 2, [(1, 3), (-3, 4), (-4, 2)]),
    ]

    corpus: list[tuple[int, int, list[tuple[int, ...]]]] = list(controls)
    for nvars in range(1, 7):
        for s in range(1, nvars + 1):
            for _ in range(24):
                count = rng.randrange(0, 2 * nvars + 4)
                clauses = [random_clause(rng, nvars, 1 if nvars == 1 else rng.choice((1, 2))) for _ in range(count)]
                corpus.append((nvars, s, clauses))

    for nvars, s, base in corpus:
        base_ok, projected, calls = exact_projection(base, nvars, s)
        oracle_calls += calls
        projection_clauses += len(projected)
        if base_ok:
            sat_controls += 1
        else:
            unsat_controls += 1
        assertions += 1
        assert len(projected) <= 2 * s * s

        # Compare exact existential projection on every retained assignment.
        for prefix in itertools.product((False, True), repeat=s):
            expected = has_extension(base, nvars, prefix)
            observed = base_ok and formula_value(projected, prefix)
            assignments_checked += 1
            assertions += 1
            assert expected == observed

            # Add up to three ternary clauses over retained variables and check
            # preservation of the full mixed formula under the same prefix.
            ternary: list[tuple[int, ...]] = []
            if s >= 3:
                for _ in range(min(3, s)):
                    ternary.append(random_clause(rng, s, 3))
            expected_mixed = expected and formula_value(ternary, prefix)
            observed_mixed = observed and formula_value(ternary, prefix)
            assertions += 1
            assert expected_mixed == observed_mixed

        instances += 1

    result = {
        "artifact": "TERNARY_PROJECTION_KERNEL88",
        "seed": SEED,
        "instances": instances,
        "retained_assignments_checked": assignments_checked,
        "entailed_clause_tests_plus_base_tests": oracle_calls,
        "materialized_projection_clauses": projection_clauses,
        "sat_base_controls": sat_controls,
        "unsat_base_controls": unsat_controls,
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite implementation audit only; proof is symbolic",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
