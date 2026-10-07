#!/usr/bin/env python3
"""Exact exponent audit for applying Williams STOC 2024 Theorem 1.1
to polynomial-size SAT inputs.

This script does not test a complexity theorem.  It checks the algebra of the
published fixed-alpha recurrence, the tempting but invalid vanishing-alpha
substitution, the source-size term omitted by that substitution, and a
bounded-degree unique-clause control for variable splitting/deduplication.

Run: python williams_polynomial_bridge.py OUTPUT.json
"""

from __future__ import annotations

import hashlib
import json
import math
import signal
import sys
import time
from pathlib import Path


def williams_step(f: float, alpha: float, beta: float) -> float:
    return beta * f / (f + alpha)


def iterate(alpha: float, beta: float, rounds: int) -> float:
    f = beta
    for _ in range(rounds):
        f = williams_step(f, alpha, beta)
    return f


def polynomial_illegal_step(p: float, K: float) -> float:
    """Formal p-coordinate recurrence after setting beta=K alpha."""
    return K * p / (p + 1.0)


def source_floor_step(p: float, K: float, delta: float, source_floor: float = 1.0) -> float:
    """Outer call exponent when its encoded circuit retains the source.

    The self-encoded circuit has size exponent at least
    max(source_floor, delta*p) relative to the original polynomial input.
    Applying an N^K solver multiplies that exponent by K.
    """
    return K * max(source_floor, delta * p)


def unique_cycle_counts(n: int, assigned: int) -> dict:
    """Unique bounded-degree 3-CNF and a worst-position prefix restriction.

    Clauses are (x_i or x_{i+1} or x_{i+2}) with cyclic indices.  They are all
    unique and every variable has occurrence degree three.  Assigning any x
    variables can touch at most 3x clauses, so at least n-3x clauses remain
    completely untouched.  This counting fact is independent of truth values.
    """
    clauses = n
    duplicates_removed = 0
    touched_upper = min(clauses, 3 * assigned)
    untouched_lower = clauses - touched_upper
    # Count an explicit prefix to check the degree bound and uniqueness.
    formula = {
        tuple(sorted((i + 1, (i + 1) % n + 1, (i + 2) % n + 1)))
        for i in range(n)
    }
    assert len(formula) == n
    touched = sum(any(variable <= assigned for variable in clause) for clause in formula)
    assert touched <= touched_upper
    return {
        "n": n,
        "clauses": clauses,
        "assigned_variables": assigned,
        "polynomial_branches_log2": assigned,
        "duplicates_removed": duplicates_removed,
        "explicit_prefix_touched": touched,
        "degree_bound_touched_upper": touched_upper,
        "untouched_clauses_lower": untouched_lower,
        "residual_size_exponent_lower": (
            math.log(max(1, untouched_lower), n) if n > 1 else 0.0
        ),
    }


def deadline(*_: object) -> None:
    raise TimeoutError("25-second exponent audit limit")


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    tolerance = 1e-10

    fixed_recurrence = []
    recurrence_checks = 0
    for alpha in (0.05, 0.1, 0.25, 0.5, 1.0):
        for ratio in (1.0, 1.5, 2.0, 4.0, 10.0):
            beta = ratio * alpha
            values = [iterate(alpha, beta, rounds) for rounds in (0, 1, 2, 4, 8, 16, 64)]
            assert all(values[index + 1] <= values[index] + tolerance for index in range(len(values) - 1))
            limit = 0.0 if abs(beta - alpha) < tolerance else beta - alpha
            assert abs(values[-1] - limit) < 5e-3 or values[-1] >= limit
            fixed_recurrence.append(
                {"alpha": alpha, "beta": beta, "round_values": values, "limit": limit}
            )
            recurrence_checks += 1

    polynomial_substitution = []
    source_floor_checks = 0
    for K in (1.1, 1.5, 2.0, 3.0, 5.0, 10.0):
        formal = K
        formal_values = [formal]
        for _ in range(32):
            formal = polynomial_illegal_step(formal, K)
            formal_values.append(formal)
        formal_limit = 0.0 if abs(K - 1.0) < tolerance else K - 1.0
        assert formal_values[-1] >= formal_limit - tolerance

        grid = []
        for source_floor in (1.0, 0.75, 0.5, 0.25):
            candidates = [
                source_floor_step(K, K, delta / 100.0, source_floor)
                for delta in range(1, 100)
            ]
            best = min(candidates)
            assert abs(best - K * source_floor) < 1e-9
            grid.append(
                {
                    "source_floor": source_floor,
                    "best_next_exponent": best,
                    "improves_on_K": best < K - tolerance,
                }
            )
            source_floor_checks += 1
        assert not grid[0]["improves_on_K"]
        polynomial_substitution.append(
            {
                "K": K,
                "illegal_floor_free_recurrence": formal_values,
                "illegal_limit": formal_limit,
                "source_floor_grid": grid,
            }
        )

    vanishing_alpha = []
    quantifier_checks = 0
    for degree in (1, 2, 4):
        for exponent in (10, 14, 18, 22):
            n = 1 << exponent
            alpha_n = degree * math.log2(n) / n
            K = 3.0
            beta_n = K * alpha_n
            delta = alpha_n / (beta_n + alpha_n)
            source_size = n**degree
            allowed_hardcoded_size = 2 ** (alpha_n * (1.0 - delta) * n)
            hardcode_overflow = source_size / allowed_hardcoded_size
            assert hardcode_overflow > 1.0
            # Any fixed alpha_0 yields exponential time when measured as a
            # polynomial exponent in N=n^degree.
            alpha_0 = 0.01
            fixed_alpha_polynomial_exponent = (
                (K - 1.0) * alpha_0 * n / (degree * math.log2(n))
            )
            vanishing_alpha.append(
                {
                    "degree": degree,
                    "n": n,
                    "alpha_n": alpha_n,
                    "beta_n": beta_n,
                    "delta_formal": delta,
                    "hardcoded_source_overflow_ratio": hardcode_overflow,
                    "fixed_alpha_0": alpha_0,
                    "runtime_exponent_relative_to_N_at_fixed_alpha": fixed_alpha_polynomial_exponent,
                }
            )
            quantifier_checks += 1

    duplicate_controls = []
    duplicate_checks = 0
    for n in (256, 1024, 4096, 16384, 65536):
        assigned = math.ceil(2 * math.log2(n))
        row = unique_cycle_counts(n, assigned)
        duplicate_controls.append(row)
        assert row["duplicates_removed"] == 0
        duplicate_checks += 1

    result = {
        "status": "COMPUTATIONAL_ALGEBRA_AUDIT",
        "theorem_scope": (
            "Williams STOC 2024 Theorem 1.1 assumes fixed positive constants "
            "alpha<=beta before n tends to infinity."
        ),
        "recurrence_checks": recurrence_checks,
        "source_floor_grid_checks": source_floor_checks,
        "vanishing_alpha_quantifier_checks": quantifier_checks,
        "unique_clause_controls": duplicate_checks,
        "errors": 0,
        "seconds": time.perf_counter() - started,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixed_alpha_recurrence": fixed_recurrence,
        "polynomial_substitution": polynomial_substitution,
        "vanishing_alpha": vanishing_alpha,
        "bounded_degree_duplicate_controls": duplicate_controls,
        "finding": (
            "The formal K-to-(K-1) map appears only after illegally replacing "
            "fixed alpha by alpha(n)=Theta(log n/n) and dropping the hardcoded "
            "source-size term. Restoring that term gives p_next>=K when the "
            "source floor is one. Duplicate elimination has source floor one "
            "on the unique-clause controls."
        ),
        "open_bridge": (
            "A uniform source-preserving representation with exponent b<1, "
            "including construction and access, would change the floor to b; "
            "establishing such a representation on all SAT inputs is precisely "
            "the missing compression theorem."
        ),
    }
    destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    signal.alarm(0)
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key
                not in {
                    "fixed_alpha_recurrence",
                    "polynomial_substitution",
                    "vanishing_alpha",
                    "bounded_degree_duplicate_controls",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
