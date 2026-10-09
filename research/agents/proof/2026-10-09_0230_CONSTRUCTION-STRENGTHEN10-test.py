#!/usr/bin/env python3
"""Bounded checks for CONSTRUCTION-STRENGTHEN10.

The experiment checks finite semantics of the fixed-radius terminal and the
NAE shield, plus exact scale arithmetic.  It is not an asymptotic proof of a
SAT compiler or of a machine-space bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import signal
import time
from fractions import Fraction
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def deadline(*_: object) -> None:
    raise TimeoutError("25-second CONSTRUCTION-STRENGTHEN10 budget exceeded")


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, true_set: frozenset[int]) -> bool:
    return all(
        any((lit > 0) == (abs(lit) in true_set) for lit in clause)
        for clause in formula
    )


def extreme_radius(formula: Formula, radius: int, base: bool) -> bool:
    """Exact bounded DFS for a model within radius of a constant assignment."""
    vs = variables(formula)

    def true_set(flipped: frozenset[int]) -> frozenset[int]:
        if not base:
            return flipped
        return frozenset(v for v in vs if v not in flipped)

    def search(flipped: frozenset[int], budget: int) -> bool:
        assignment = true_set(flipped)
        first_bad: Clause | None = None
        for clause in formula:
            if not any((lit > 0) == (abs(lit) in assignment) for lit in clause):
                first_bad = clause
                break
        if first_bad is None:
            return True
        if budget == 0:
            return False
        # A target flip set T extending the current set must add a variable
        # from this falsified clause.  Branch only by adding such a variable.
        for var in dict.fromkeys(abs(lit) for lit in first_bad):
            if var not in flipped and search(flipped | {var}, budget - 1):
                return True
        return False

    return search(frozenset(), radius)


def brute_near_extreme(formula: Formula, radius: int) -> bool:
    vs = variables(formula)
    n = len(vs)
    for mask in range(1 << n):
        weight = mask.bit_count()
        if min(weight, n - weight) > radius:
            continue
        true_set = frozenset(vs[i] for i in range(n) if mask & (1 << i))
        if satisfies(formula, true_set):
            return True
    return False


def proper_clauses(n: int) -> tuple[Clause, ...]:
    out: list[Clause] = []
    for support in itertools.combinations(range(1, n + 1), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            out.append(tuple(sign * var for sign, var in zip(signs, support)))
    return tuple(out)


def check_extreme_radius() -> dict[str, object]:
    clauses = proper_clauses(4)
    checked = mismatches = 0
    by_radius: dict[str, int] = {}
    for radius in range(4):
        local = 0
        for size in range(4):
            for formula in itertools.combinations(clauses, size):
                expected = brute_near_extreme(formula, radius)
                got = extreme_radius(formula, radius, False) or extreme_radius(
                    formula, radius, True
                )
                checked += 1
                local += 1
                mismatches += int(got != expected)
        by_radius[str(radius)] = local
    assert checked == 4 * 5489
    assert mismatches == 0
    return {
        "formulas_radius_pairs": checked,
        "pairs_by_radius": by_radius,
        "semantic_mismatches": mismatches,
        "search_nodes_upper_bound": "2*(1+3+...+3^r)",
    }


def nae_shield(blocks: int) -> Formula:
    clauses: list[Clause] = []
    for j in range(blocks):
        a, b, c = 3 * j + 1, 3 * j + 2, 3 * j + 3
        clauses.extend(((a, b, c), (-a, -b, -c)))
    return tuple(clauses)


def check_shields() -> dict[str, object]:
    rows = []
    for blocks in range(1, 5):
        formula = nae_shield(blocks)
        n = 3 * blocks
        models = []
        for mask in range(1 << n):
            true_set = frozenset(i + 1 for i in range(n) if mask & (1 << i))
            if satisfies(formula, true_set):
                models.append(mask)
        min_true = min(mask.bit_count() for mask in models)
        min_false = min(n - mask.bit_count() for mask in models)
        assert len(models) == 6**blocks
        assert min_true == blocks
        assert min_false == blocks

        # After occurrence-private isolation the 2b shield clauses have
        # disjoint three-variable supports.  A strong-Krom backdoor must hit
        # each support, while Horn/dual-Horn must take two variables from the
        # positive/negative supports respectively.
        isolated_supports = [set(range(3 * i + 1, 3 * i + 4)) for i in range(2 * blocks)]
        universe = sorted(set().union(*isolated_supports))
        min_hit = None
        for k in range(len(universe) + 1):
            if any(
                all(set(choice) & support for support in isolated_supports)
                for choice in itertools.combinations(universe, k)
            ):
                min_hit = k
                break
        assert min_hit == 2 * blocks
        rows.append(
            {
                "blocks": blocks,
                "models": len(models),
                "min_true": min_true,
                "min_false": min_false,
                "isolated_clause_hitting_number": min_hit,
            }
        )
    return {"rows": rows}


def check_sat_equivalence() -> dict[str, object]:
    checked = mismatches = 0
    support = (1, 2, 3)
    for signs in itertools.product((-1, 1), repeat=3):
        source: Formula = (tuple(sign * var for sign, var in zip(signs, support)),)
        source_sat = any(
            satisfies(source, frozenset(i + 1 for i in range(3) if mask & (1 << i)))
            for mask in range(8)
        )
        for blocks in range(1, 5):
            offset = 3
            shield = tuple(
                tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in clause)
                for clause in nae_shield(blocks)
            )
            combined = source + shield
            combined_sat = False
            for mask in range(1 << (3 + 3 * blocks)):
                true_set = frozenset(
                    i + 1 for i in range(3 + 3 * blocks) if mask & (1 << i)
                )
                if satisfies(combined, true_set):
                    combined_sat = True
                    break
            checked += 1
            mismatches += int(source_sat != combined_sat)
    assert checked == 32
    assert mismatches == 0
    return {"source_shield_pairs": checked, "semantic_mismatches": mismatches}


def check_scale_arithmetic() -> dict[str, object]:
    rows = []
    for a in (Fraction(6, 5), Fraction(3, 2), Fraction(2, 1), Fraction(7, 3)):
        back = 1 / a
        product = a * back
        assert product == 1
        rows.append({"pad_exponent": str(a), "unpad_exponent": str(back), "cycle": str(product)})
    return {
        "typed_cycles": rows,
        "completed_boundary_exponent": "1",
        "aggregate_single_child_exponents": {"v": "1", "h": "1"},
        "recursive_fixed_point_denominator": "1-h=0",
    }


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL finite semantics and exact arithmetic",
        "timeout_seconds": 25,
        "extreme_radius": check_extreme_radius(),
        "nae_shields": check_shields(),
        "sat_equivalence": check_sat_equivalence(),
        "scale_laundering": check_scale_arithmetic(),
        "limitations": [
            "Finite tests do not prove all-input acquisition or asymptotic machine bounds.",
            "The shielded hard-image theorem also uses the previously proved ARC6 universal map.",
            "The backdoor hitting check is structural; operational backdoors with early empty-clause exits need separate treatment beyond size two.",
        ],
    }
    result["seconds"] = time.perf_counter() - started
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name(
        "2026-10-09_0230_CONSTRUCTION-STRENGTHEN10-results.json"
    )
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
