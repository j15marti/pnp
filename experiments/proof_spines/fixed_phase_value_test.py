#!/usr/bin/env python3
"""Bounded audit for FIXED-PHASE-VALUE1.

The partial member checks a fixed list of complete assignments.  It returns
TRUE only after one assignment satisfies every clause; otherwise it returns
FAIL, never FALSE.  The concrete list is [all-true, all-false].  Assignment
bits are regenerated from one phase bit, so construction needs no SAT call
and no explicit assignment table.

The script exhaustively checks every subset of the eight full-width clauses
on three variables, exercises hostile controls, and compares the phase
front-end with the existing FINAL-LINK-HYBRID1 builder on planted controls.
It uses a 25-second cooperative alarm.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools as it
import json
import math
import random
import signal
import sys
import time
from pathlib import Path
from typing import Iterable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import final_link_hybrid_builder as fl


Formula = fl.Formula


def deadline(*_: object) -> None:
    raise TimeoutError("25-second cooperative budget exceeded")


def phase_member(formula: Formula) -> dict[str, object]:
    """Return a sound TRUE plan for all-true/all-false, otherwise FAIL."""
    clause_reads = 0
    literal_reads = 0
    all_true = True
    all_false = True
    for clause in formula:
        clause_reads += 1
        has_positive = False
        has_negative = False
        for literal in clause:
            literal_reads += 1
            has_positive |= literal > 0
            has_negative |= literal < 0
        all_true &= has_positive
        all_false &= has_negative
    if all_true:
        return {
            "status": "SUCCESS",
            "value": True,
            "phase": True,
            "clause_reads": clause_reads,
            "literal_reads": literal_reads,
            "recursive_children": 0,
            "sat_calls": 0,
        }
    if all_false:
        return {
            "status": "SUCCESS",
            "value": True,
            "phase": False,
            "clause_reads": clause_reads,
            "literal_reads": literal_reads,
            "recursive_children": 0,
            "sat_calls": 0,
        }
    return {
        "status": "FAIL",
        "clause_reads": clause_reads,
        "literal_reads": literal_reads,
        "recursive_children": 0,
        "sat_calls": 0,
    }


def phase_assignment(formula: Formula, phase: bool) -> dict[int, bool]:
    return {v: phase for v in fl.variables(formula)}


def brute_sat(formula: Formula) -> bool:
    variables = fl.variables(formula)
    for bits in it.product((False, True), repeat=len(variables)):
        if fl.satisfies(formula, dict(zip(variables, bits))):
            return True
    return False


def independent_positive(blocks: int) -> Formula:
    return fl.canonical((3 * i + 1, 3 * i + 2, 3 * i + 3) for i in range(blocks))


def independent_negative(blocks: int) -> Formula:
    return fl.canonical((-(3 * i + 1), -(3 * i + 2), -(3 * i + 3)) for i in range(blocks))


def signed_rename(formula: Formula, flipped: set[int]) -> Formula:
    return fl.canonical(
        tuple(-lit if abs(lit) in flipped else lit for lit in clause)
        for clause in formula
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="fixed_phase_value_results.json")
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    rng = random.Random(20261007)
    checks = 0

    # Exhaustive semantic audit on all subsets of full-width three-variable
    # clauses.  Success must always carry a real complete satisfying phase.
    signed_clauses = list(it.product(*[(v, -v) for v in range(1, 4)]))
    exhaustive_successes = 0
    exhaustive_fails = 0
    for mask in range(1 << len(signed_clauses)):
        formula = fl.canonical(
            clause for i, clause in enumerate(signed_clauses) if (mask >> i) & 1
        )
        result = phase_member(formula)
        sat = brute_sat(formula)
        checks += 1
        if result["status"] == "SUCCESS":
            exhaustive_successes += 1
            phase = bool(result["phase"])
            assert sat
            assert fl.satisfies(formula, phase_assignment(formula, phase))
            checks += 2
        else:
            exhaustive_fails += 1

    controls: list[dict[str, object]] = []
    control_formulas = [
        ("positive_product_64", independent_positive(64), "SUCCESS"),
        ("negative_product_64", independent_negative(64), "SUCCESS"),
        ("contradictory_units", fl.canonical([(1,), (-1,)]), "FAIL"),
        ("mixed_satisfiable", fl.canonical([(1,), (-2,)]), "FAIL"),
        ("php_5_4", fl.php(5, 4), "FAIL"),
        ("xor_cycle_8", fl.xor_cycle(8, inconsistent=False), "SUCCESS"),
    ]
    for name, formula, expected in control_formulas:
        result = phase_member(formula)
        assert result["status"] == expected, (name, result)
        checks += 1
        if expected == "SUCCESS":
            phase = bool(result["phase"])
            assert fl.satisfies(formula, phase_assignment(formula, phase))
            checks += 1
        controls.append(
            {
                "name": name,
                "input_bits": fl.encoding_bits(formula),
                "clauses": len(formula),
                **result,
            }
        )

    # Padding and signed-renaming controls. Tautologies vanish under the
    # declared normalization. Signed renaming may reduce coverage but may not
    # create a false success.
    positive = independent_positive(10)
    padded = fl.canonical(list(positive) + [(1, -1), (2, -2)])
    assert phase_member(padded)["status"] == "SUCCESS"
    checks += 1
    flipped = set(rng.sample(list(fl.variables(positive)), 11))
    renamed = signed_rename(positive, flipped)
    renamed_result = phase_member(renamed)
    if renamed_result["status"] == "SUCCESS":
        phase = bool(renamed_result["phase"])
        assert fl.satisfies(renamed, phase_assignment(renamed, phase))
    checks += 1

    # The existing planted generators deliberately exclude all-negative
    # clauses, so every such formula is settled by the all-true phase. Compare
    # against the unmodified hybrid to quantify the finite acquisition saved.
    comparisons: list[dict[str, object]] = []
    planted_cases = [
        ("planted3_16", fl.random_3cnf(16, 80, 12016, planted=True)),
        ("planted3_24", fl.random_3cnf(24, 120, 12024, planted=True)),
        ("hub_24", fl.hub_formula(24, 14024)),
    ]
    for name, formula in planted_cases:
        phase = phase_member(formula)
        assert phase["status"] == "SUCCESS" and phase["phase"] is True
        assert fl.satisfies(formula, phase_assignment(formula, True))
        builder = fl.Builder(formula, "short", node_cap=4096)
        root, summary = builder.run()
        assert root is not None and summary["complete"]
        checks += 3
        comparisons.append(
            {
                "name": name,
                "input_bits": fl.encoding_bits(formula),
                "phase_literal_reads": phase["literal_reads"],
                "hybrid_construction_work_proxy": summary["metrics"]["construction_work_proxy"],
                "hybrid_plan_nodes": summary["plan_nodes"],
                "hybrid_peak_logical_workspace_bits": summary["metrics"]["peak_logical_workspace_bits"],
                "hybrid_empirical_work_exponent": summary["empirical_work_exponent"],
                "phase_zero_children": True,
            }
        )

    gamma = 2.0 * math.cos(math.pi / 7.0)
    exponent_cells = []
    for u_num, u_den in ((0, 1), (1, 3), (4, 5), (5, 6)):
        u = u_num / u_den
        c = 1.0 + u
        exponent_cells.append(
            {
                "assignment_count_exponent_u": f"{u_num}/{u_den}",
                "bit_query_exponent_v": "0/1",
                "time_exponent_c": c,
                "below_williams_gamma": c < gamma,
            }
        )
        checks += 1
    assert exponent_cells[0]["below_williams_gamma"]
    assert exponent_cells[1]["below_williams_gamma"]
    assert exponent_cells[2]["below_williams_gamma"]
    assert not exponent_cells[3]["below_williams_gamma"]
    checks += 4

    elapsed = time.perf_counter() - started
    signal.alarm(0)
    here = Path(__file__)
    builder_path = Path("final_link_hybrid_builder.py")
    result = {
        "run_id": "WRP-0004",
        "claim_id": "FIXED-PHASE-VALUE1",
        "status": "COMPUTATIONAL",
        "seed": 20261007,
        "checks": checks,
        "elapsed_seconds": elapsed,
        "internal_budget_seconds": 25,
        "exhaustive": {
            "three_variable_clause_subsets": 256,
            "successes": exhaustive_successes,
            "fails": exhaustive_fails,
        },
        "controls": controls,
        "signed_renaming_status": renamed_result["status"],
        "comparisons": comparisons,
        "exponent_cells": exponent_cells,
        "williams_gamma": gamma,
        "source_sha256": sha256(here),
        "imported_builder_sha256": sha256(builder_path),
        "limitations": [
            "The phase member is partial and never certifies UNSAT on failure.",
            "Finite coverage counts do not imply all-input coverage.",
            "The comparison uses the existing explicit-plan hybrid only as a measured baseline.",
            "The theorem requires charged assignment-bit access; the concrete phases have constant-time bits.",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
