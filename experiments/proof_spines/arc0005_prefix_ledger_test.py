#!/usr/bin/env python3
"""Independent exact checks for WRP-0005.

The test has two purposes.

1. Exhaustively verify the ARC-0005 row-profile orbit formula for all
   clauses over a 3-by-2 signed matrix, without importing the implementation
   under review.
2. Check, with rational exponent arithmetic, how a global prefix using
   time exponent 1 and space exponent 2/3 changes each live endpoint ledger.

Every invocation is guarded by a 25-second alarm and is intended to run under
an external 30-second timeout.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import signal
import time
from fractions import Fraction
from pathlib import Path

START = time.monotonic()
DEADLINE = START + 25.0


class BudgetExceeded(RuntimeError):
    pass


def _alarm(_signum: int, _frame: object) -> None:
    raise BudgetExceeded("25-second alarm")


def tick() -> None:
    if time.monotonic() >= DEADLINE:
        raise BudgetExceeded("25-second cooperative budget")


def profile_signature(row_profiles: tuple[tuple[int, ...], ...]) -> tuple[tuple[tuple[int, ...], int], ...]:
    occupied = sorted(profile for profile in row_profiles if profile)
    return tuple((profile, sum(1 for item in occupied if item == profile))
                 for profile in sorted(set(occupied)))


def orbit_size(signature: tuple[tuple[tuple[int, ...], int], ...], rows: int) -> int:
    occupied = sum(multiplicity for _profile, multiplicity in signature)
    denominator = math.factorial(rows - occupied)
    for _profile, multiplicity in signature:
        denominator *= math.factorial(multiplicity)
    return math.factorial(rows) // denominator


def matrix_clause(row_profiles: tuple[tuple[int, ...], ...], columns: int) -> tuple[int, ...]:
    literals: list[int] = []
    for row, profile in enumerate(row_profiles):
        for column, sign in enumerate(profile):
            if sign:
                variable = row * columns + column + 1
                literals.append(variable if sign > 0 else -variable)
    return tuple(sorted(literals))


def permute_clause(clause: tuple[int, ...], permutation: tuple[int, ...], columns: int) -> tuple[int, ...]:
    image: list[int] = []
    for literal in clause:
        variable = abs(literal) - 1
        row, column = divmod(variable, columns)
        moved = permutation[row] * columns + column + 1
        image.append(moved if literal > 0 else -moved)
    return tuple(sorted(image))


def check_orbits() -> dict[str, int]:
    rows, columns = 3, 2
    row_profile_space = tuple(itertools.product((-1, 0, 1), repeat=columns))
    classes: dict[tuple[tuple[tuple[int, ...], int], ...], set[tuple[int, ...]]] = {}
    orbit_checks = 0
    for row_profiles in itertools.product(row_profile_space, repeat=rows):
        tick()
        signature = profile_signature(row_profiles)
        clause = matrix_clause(row_profiles, columns)
        classes.setdefault(signature, set()).add(clause)
        actual_orbit = {
            permute_clause(clause, permutation, columns)
            for permutation in itertools.permutations(range(rows))
        }
        assert len(actual_orbit) == orbit_size(signature, rows)
        orbit_checks += 1

    incomplete_rejections = 0
    for signature, clauses in classes.items():
        expected = orbit_size(signature, rows)
        assert len(clauses) == expected
        if expected > 1:
            assert len(clauses) - 1 != expected
            incomplete_rejections += 1
    return {
        "rows": rows,
        "columns": columns,
        "clauses_checked": orbit_checks,
        "signature_classes": len(classes),
        "incomplete_orbits_rejected": incomplete_rejections,
    }


def below_phi(value: Fraction) -> bool:
    """Decide value < (1+sqrt(5))/2 using integer arithmetic."""
    shifted = 2 * value - 1
    if shifted < 0:
        return True
    return shifted * shifted < 5


def check_prefix_ledger() -> dict[str, object]:
    prefix_time = Fraction(1, 1)
    prefix_space = Fraction(2, 3)
    grid = tuple(Fraction(n, 12) for n in range(25))
    cells = 0
    product_after_prefix = 0
    small_space_after_prefix = 0
    fortnow_after_prefix = 0
    fortnow_expected = 0
    for fallback_time in grid:
        for fallback_space in grid:
            tick()
            total_time = max(prefix_time, fallback_time)
            total_space = max(prefix_space, fallback_space)
            product = below_phi(total_time + total_space)
            small_space = total_space == 0
            fortnow = total_time <= 1 and total_space < 1
            expected = fallback_time <= 1 and fallback_space < 1
            assert fortnow == expected
            product_after_prefix += int(product)
            small_space_after_prefix += int(small_space)
            fortnow_after_prefix += int(fortnow)
            fortnow_expected += int(expected)
            cells += 1

    assert not below_phi(prefix_time + prefix_space)
    assert product_after_prefix == 0
    assert small_space_after_prefix == 0
    assert fortnow_after_prefix == fortnow_expected
    assert fortnow_after_prefix > 0

    # A fixed finite sequential portfolio takes maxima of exponents after all
    # failed state is discarded; it does not add the exponents.
    member_times = (Fraction(1), Fraction(4, 3), Fraction(5, 4))
    member_spaces = (Fraction(0), Fraction(1, 2), Fraction(2, 3))
    assert max(member_times) == Fraction(4, 3)
    assert max(member_spaces) == Fraction(2, 3)

    return {
        "grid_cells": cells,
        "prefix_time": str(prefix_time),
        "prefix_space": str(prefix_space),
        "prefix_sum": str(prefix_time + prefix_space),
        "five_thirds_below_phi": below_phi(Fraction(5, 3)),
        "product_cells_after_prefix": product_after_prefix,
        "small_space_cells_after_prefix": small_space_after_prefix,
        "fortnow_cells_after_prefix": fortnow_after_prefix,
        "finite_portfolio_time_max": str(max(member_times)),
        "finite_portfolio_space_max": str(max(member_spaces)),
    }


def check_density_gate() -> dict[str, object]:
    """Check the exact inequality behind DENSITY-GATED-PHP-VALUE1.

    For n=ph and e=h*binom(p,2), balance h/2 <= p <= 2h and p>=2 imply
    32 e^2 >= n^3.  This is the squared integer form of
    e >= n^(3/2)/(4*sqrt(2)).
    """
    balanced_cells = 0
    minimum_slack: int | None = None
    boundary_examples: list[dict[str, int]] = []
    for p in range(2, 129):
        for h in range(2, 129):
            tick()
            if h <= 2 * p and p <= 2 * h:
                n = p * h
                edges = h * p * (p - 1) // 2
                slack = 32 * edges * edges - n * n * n
                assert slack >= 0
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                balanced_cells += 1
                if (p, h) in ((2, 2), (24, 24), (25, 24), (49, 48)):
                    boundary_examples.append({"p": p, "h": h, "n": n, "edges": edges, "slack": slack})

    # Removing balance invalidates the 2/3-space inference: p=2, h=128.
    p, h = 2, 128
    n = p * h
    edges = h * p * (p - 1) // 2
    unbalanced_slack = 32 * edges * edges - n * n * n
    assert unbalanced_slack < 0
    return {
        "balanced_cells": balanced_cells,
        "minimum_integer_slack": minimum_slack,
        "selected_examples": boundary_examples,
        "unbalanced_counterexample": {
            "p": p,
            "h": h,
            "n": n,
            "edges": edges,
            "integer_slack": unbalanced_slack,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    status = "PASS"
    error = None
    payload: dict[str, object] = {}
    try:
        payload["orbit_audit"] = check_orbits()
        payload["density_gate_audit"] = check_density_gate()
        payload["prefix_ledger"] = check_prefix_ledger()
    except Exception as exc:  # retained in the raw record
        status = "FAIL"
        error = f"{type(exc).__name__}: {exc}"
    finally:
        signal.alarm(0)

    body = {
        "run_id": "WRP-0005",
        "status": status,
        "elapsed_seconds": time.monotonic() - START,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "results": payload,
        "error": error,
        "limits": [
            "The orbit test is exhaustive only for the declared 3-by-2 matrix model.",
            "The density test checks exact gate arithmetic, not the byte parser or union-find implementation.",
            "The exponent grid checks composition arithmetic, not existence of a general-SAT fallback.",
            "No finite test implies all-CNF coverage or a P versus NP separation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
    print(json.dumps(body, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
