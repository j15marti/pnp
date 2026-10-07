#!/usr/bin/env python3
"""Exact finite checks for PROJECTED-SOLUTION-COVER-GATE1.

The symbolic lemma concerns CNF children G(X,Z) whose satisfying assignments,
after existentially projecting auxiliary variables Z, are contained in the
solution set of F_m = AND_i (x_i OR y_i).  This script exhausts small CNFs and
checks the claimed block-incidence, occurrence, and clause lower bounds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import signal
import time


SEED = 20261007
BUDGET_SECONDS = 25


def clause_masks(variable_count: int, width: int) -> list[tuple[tuple[int, ...], int]]:
    """Return all non-tautological clauses of width at most ``width``."""
    universe = range(1, variable_count + 1)
    result: list[tuple[tuple[int, ...], int]] = []
    assignments = range(1 << variable_count)
    for size in range(1, width + 1):
        for variables in itertools.combinations(universe, size):
            for signs in itertools.product((False, True), repeat=size):
                clause = tuple(v if positive else -v for v, positive in zip(variables, signs))
                mask = 0
                for assignment in assignments:
                    if any(
                        bool((assignment >> (abs(literal) - 1)) & 1) == (literal > 0)
                        for literal in clause
                    ):
                        mask |= 1 << assignment
                result.append((clause, mask))
    return result


def target_masks(m: int, auxiliary_count: int, signs: tuple[tuple[bool, bool], ...] | None = None) -> tuple[int, int]:
    """Return (all assignments, assignments violating the signed product CNF)."""
    if signs is None:
        signs = tuple((True, True) for _ in range(m))
    variable_count = 2 * m + auxiliary_count
    all_mask = (1 << (1 << variable_count)) - 1
    bad_mask = 0
    for assignment in range(1 << variable_count):
        good = True
        for block, (left_positive, right_positive) in enumerate(signs):
            left = bool((assignment >> (2 * block)) & 1) == left_positive
            right = bool((assignment >> (2 * block + 1)) & 1) == right_positive
            if not (left or right):
                good = False
                break
        if not good:
            bad_mask |= 1 << assignment
    return all_mask, bad_mask


def mentioned_blocks(formula: tuple[tuple[int, ...], ...], m: int) -> set[int]:
    return {
        (abs(literal) - 1) // 2
        for clause in formula
        for literal in clause
        if abs(literal) <= 2 * m
    }


def check_case(m: int, width: int, auxiliary_count: int, max_clauses: int) -> dict[str, int]:
    clauses = clause_masks(2 * m + auxiliary_count, width)
    all_mask, bad_mask = target_masks(m, auxiliary_count)
    checked = 0
    contained = 0
    violations = 0
    for count in range(max_clauses + 1):
        for selected in itertools.combinations(clauses, count):
            checked += 1
            sat_mask = all_mask
            for _, clause_mask in selected:
                sat_mask &= clause_mask
            if not sat_mask or sat_mask & bad_mask:
                continue
            contained += 1
            formula = tuple(clause for clause, _ in selected)
            blocks = mentioned_blocks(formula, m)
            occurrences = sum(
                abs(literal) <= 2 * m for clause in formula for literal in clause
            )
            if (
                len(blocks) != m
                or occurrences < m
                or count < math.ceil(m / width)
            ):
                violations += 1
    return {
        "m": m,
        "width": width,
        "auxiliary_variables": auxiliary_count,
        "max_clauses": max_clauses,
        "candidate_clauses": len(clauses),
        "formulas_checked": checked,
        "satisfiable_children_contained_after_projection": contained,
        "violations": violations,
    }


def eval_formula(formula: tuple[tuple[int, ...], ...], assignment: int) -> bool:
    return all(
        any(
            bool((assignment >> (abs(literal) - 1)) & 1) == (literal > 0)
            for literal in clause
        )
        for clause in formula
    )


def contained_after_projection(
    formula: tuple[tuple[int, ...], ...],
    m: int,
    auxiliary_count: int,
    signs: tuple[tuple[bool, bool], ...],
) -> bool:
    _, bad_mask = target_masks(m, auxiliary_count, signs)
    for assignment in range(1 << (2 * m + auxiliary_count)):
        if ((bad_mask >> assignment) & 1) and eval_formula(formula, assignment):
            return False
    return True


def hostile_controls() -> dict[str, int | bool]:
    rng = random.Random(SEED)
    signed_checks = 0
    missing_block_rejections = 0
    auxiliary_rejections = 0
    padding_invariance_checks = 0
    for m in range(2, 7):
        for _ in range(8):
            signs = tuple((bool(rng.getrandbits(1)), bool(rng.getrandbits(1))) for _ in range(m))
            canonical = tuple(
                (
                    (2 * i + 1) if signs[i][0] else -(2 * i + 1),
                    (2 * i + 2) if signs[i][1] else -(2 * i + 2),
                )
                for i in range(m)
            )
            assert contained_after_projection(canonical, m, 0, signs)
            signed_checks += 1

            missing = canonical[:-1]
            if not contained_after_projection(missing, m, 0, signs):
                missing_block_rejections += 1

            z = 2 * m + 1
            auxiliary_child = missing + ((z,),)
            if not contained_after_projection(auxiliary_child, m, 1, signs):
                auxiliary_rejections += 1

            with_unused_padding = canonical
            if contained_after_projection(with_unused_padding, m, 2, signs):
                padding_invariance_checks += 1
    return {
        "signed_renaming_controls": signed_checks,
        "missing_block_rejections": missing_block_rejections,
        "auxiliary_only_padding_rejections": auxiliary_rejections,
        "unused_auxiliary_padding_invariance_checks": padding_invariance_checks,
        "passed": signed_checks == missing_block_rejections == auxiliary_rejections == padding_invariance_checks,
    }


def main() -> None:
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25-second cooperative budget exceeded")))
    signal.alarm(BUDGET_SECONDS)
    started = time.monotonic()
    cases = [
        check_case(m=2, width=2, auxiliary_count=1, max_clauses=2),
        check_case(m=3, width=2, auxiliary_count=1, max_clauses=2),
        check_case(m=3, width=3, auxiliary_count=1, max_clauses=2),
        check_case(m=4, width=2, auxiliary_count=2, max_clauses=2),
    ]
    controls = hostile_controls()
    elapsed = time.monotonic() - started
    signal.alarm(0)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "claim_id": "PROJECTED-SOLUTION-COVER-GATE1",
        "status": "COMPUTATIONAL check of a PROVED/EXACT restricted-model lemma",
        "seed": SEED,
        "cooperative_budget_seconds": float(BUDGET_SECONDS),
        "elapsed_seconds": round(elapsed, 6),
        "exhaustive": True,
        "cases": cases,
        "hostile_controls": controls,
        "total_formulas_checked": sum(case["formulas_checked"] for case in cases),
        "total_contained_children": sum(case["satisfiable_children_contained_after_projection"] for case in cases),
        "total_violations": sum(case["violations"] for case in cases),
        "passed": all(case["violations"] == 0 for case in cases) and bool(controls["passed"]),
        "scope": (
            "Children are satisfiable width-k CNFs over parent variables X and arbitrary tested auxiliary "
            "variables Z. Their existential projections onto X must be contained in the independent-block "
            "2-CNF solution set. This is a finite check only; the symbolic proof supplies the asymptotic result. "
            "Decision-only OR reductions, circuits, unbounded clauses, and compressed non-CNF representations "
            "remain outside scope."
        ),
        "source_sha256": source_hash,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
