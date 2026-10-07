#!/usr/bin/env python3
"""Exact small-model audit of a witness-preserving sparsification gate.

For F_m = AND_i (x_i OR y_i), every satisfiable bounded-width CNF G whose
solution set is contained in sol(F_m) must mention at least one variable from
every block.  Hence a width-k G needs at least ceil(m/k) clauses.  The analytic
proof is in the companion report; this program exhausts small CNFs with fewer
clauses and checks seeded controls using exact truth-table bitsets.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import time


SEED = 20261007
BUDGET_SECONDS = 25.0


def clause_universe(variable_count: int, width: int) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for size in range(1, width + 1):
        for variables in itertools.combinations(range(variable_count), size):
            for signs in itertools.product((0, 1), repeat=size):
                clauses.append(tuple((v + 1) if sign else -(v + 1) for v, sign in zip(variables, signs)))
    return clauses


def clause_mask(clause: tuple[int, ...], variable_count: int) -> int:
    mask = 0
    for assignment in range(1 << variable_count):
        satisfied = False
        for literal in clause:
            bit = (assignment >> (abs(literal) - 1)) & 1
            if (literal > 0 and bit) or (literal < 0 and not bit):
                satisfied = True
                break
        if satisfied:
            mask |= 1 << assignment
    return mask


def parent_mask(blocks: int) -> int:
    variable_count = 2 * blocks
    mask = 0
    for assignment in range(1 << variable_count):
        if all(((assignment >> (2 * i)) & 1) or ((assignment >> (2 * i + 1)) & 1) for i in range(blocks)):
            mask |= 1 << assignment
    return mask


def mentioned_blocks(formula: tuple[tuple[int, ...], ...]) -> set[int]:
    return {(abs(lit) - 1) // 2 for clause in formula for lit in clause}


def main() -> None:
    start = time.monotonic()
    rng = random.Random(SEED)
    failures: list[str] = []
    rows: list[dict] = []
    checks = 0

    for width, max_blocks in ((2, 5), (3, 6)):
        for blocks in range(1, max_blocks + 1):
            if time.monotonic() - start > BUDGET_SECONDS:
                raise TimeoutError("cooperative 25-second budget exceeded")
            variable_count = 2 * blocks
            all_assignments = (1 << (1 << variable_count)) - 1
            target = parent_mask(blocks)
            clauses = clause_universe(variable_count, width)
            masks = [clause_mask(clause, variable_count) for clause in clauses]
            lower_bound = math.ceil(blocks / width)
            examined = 0
            counterexamples = 0

            for clause_count in range(lower_bound):
                for indices in itertools.combinations(range(len(clauses)), clause_count):
                    if time.monotonic() - start > BUDGET_SECONDS:
                        raise TimeoutError("cooperative 25-second budget exceeded")
                    solution_mask = all_assignments
                    formula = tuple(clauses[index] for index in indices)
                    for index in indices:
                        solution_mask &= masks[index]
                    examined += 1
                    checks += 3
                    useful_child = solution_mask != 0 and (solution_mask & ~target) == 0
                    if useful_child:
                        counterexamples += 1
                        failures.append(
                            f"width={width}, blocks={blocks}, clauses={clause_count}: "
                            f"useful child below coverage bound {formula}"
                        )
                    if len(mentioned_blocks(formula)) > width * clause_count:
                        failures.append("block-incidence counting invariant failed")

            # Positive control: units x_i imply the parent and mention all blocks.
            positive = tuple((2 * i + 1,) for i in range(blocks))
            positive_mask = all_assignments
            clause_to_mask = dict(zip(clauses, masks))
            for clause in positive:
                positive_mask &= clause_to_mask[clause]
            positive_ok = positive_mask != 0 and (positive_mask & ~target) == 0
            checks += 2
            if not positive_ok or len(mentioned_blocks(positive)) != blocks:
                failures.append(f"positive control failed at width={width}, blocks={blocks}")

            rows.append(
                {
                    "width": width,
                    "blocks": blocks,
                    "proved_clause_floor": lower_bound,
                    "formulas_examined_below_floor": examined,
                    "counterexamples": counterexamples,
                    "unit_positive_control": positive_ok,
                }
            )

    # Seeded direct checks of the analytic missing-block move.  Whenever a
    # satisfiable random child omits a block, flip that block to 00 in one
    # satisfying assignment; the child stays true and leaves sol(F_m).
    seeded_cases = 256
    seeded_escapes = 0
    for _ in range(seeded_cases):
        blocks = rng.randint(2, 8)
        width = rng.choice((2, 3))
        variable_count = 2 * blocks
        clauses = clause_universe(variable_count, width)
        formula = tuple(rng.sample(clauses, rng.randint(0, min(6, len(clauses)))))
        mentioned = mentioned_blocks(formula)
        missing = sorted(set(range(blocks)) - mentioned)
        if not missing:
            continue
        witness = None
        for assignment in range(1 << variable_count):
            if all(any((((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)) for lit in clause) for clause in formula):
                witness = assignment
                break
        if witness is None:
            continue
        block = missing[0]
        changed = witness & ~(1 << (2 * block)) & ~(1 << (2 * block + 1))
        child_stays_true = all(
            any((((changed >> (abs(lit) - 1)) & 1) == (lit > 0)) for lit in clause)
            for clause in formula
        )
        parent_becomes_false = not (
            ((changed >> (2 * block)) & 1) or ((changed >> (2 * block + 1)) & 1)
        )
        checks += 2
        if child_stays_true and parent_becomes_false:
            seeded_escapes += 1
        else:
            failures.append("seeded missing-block escape failed")

    elapsed = time.monotonic() - start
    result = {
        "claim_id": "SPARSIFICATION-SOLUTION-COVER-GATE1",
        "status": "COMPUTATIONAL check of a PROVED/EXACT restricted-model lemma",
        "seed": SEED,
        "cooperative_budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": elapsed,
        "checks": checks,
        "passed": not failures,
        "failures": failures,
        "exhaustive_rows": rows,
        "seeded_cases": seeded_cases,
        "seeded_missing_block_escapes": seeded_escapes,
        "scope": (
            "Children are satisfiable width-k CNFs over the parent variables, and their solution sets "
            "must be subsets of the parent's solution set, as follows from exact solution-set union. "
            "The result does not apply to decision-only OR reductions, auxiliary projections, unbounded "
            "representations, or arbitrary semantic SAT shrinkers."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
