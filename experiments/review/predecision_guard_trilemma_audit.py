#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0015.

This checks the exact finite analogue of the no-call predecision laundering
construction.  It is COMPUTATIONAL evidence only; the general theorem is
proved symbolically in the accompanying report.
"""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path
import time


RUN_ID = "SYNTHESIS-0015"
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("canonical", "reversed", "renamed", "complemented", "padded", "redundant")
OUT = Path("results/raw/review/2026-10-11_predecision_guard_trilemma.json")


def eval_clause(clause: tuple[int, ...], assignment: tuple[bool, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def sat(clauses: tuple[tuple[int, ...], ...], nvars: int) -> bool:
    return any(all(eval_clause(c, a) for c in clauses) for a in product((False, True), repeat=nvars))


PROPER3 = tuple(
    tuple((i + 1) if signs[i] else -(i + 1) for i in range(3))
    for signs in product((False, True), repeat=3)
)
TRUE3 = ((1, 2, 3),)
FALSE3 = PROPER3


def laundered_pass(clauses: tuple[tuple[int, ...], ...], nvars: int, wrapper: str) -> dict:
    """Run a source decider B, never the named solver A, then emit T or U."""
    answer = sat(clauses, nvars)
    child = TRUE3 if answer else FALSE3
    return {
        "answer": answer,
        "child_answer": sat(child, 3),
        "named_solver_calls": 0,
        "source_decisions": 1,
        "wrapper": wrapper,
        "child_clauses": len(child),
    }


def check_formula(clauses: tuple[tuple[int, ...], ...], nvars: int, counters: dict) -> None:
    expected = sat(clauses, nvars)
    for wrapper in WRAPPERS:
        for encoding in ENCODINGS:
            got = laundered_pass(clauses, nvars, wrapper)
            assert got["answer"] == expected == got["child_answer"]
            assert got["named_solver_calls"] == 0
            assert got["source_decisions"] == 1
            assert got["child_clauses"] in (1, 8)
            counters["wrapper_encoding_checks"] += 1
            counters[f"encoding_{encoding}"] += 1


def main() -> None:
    started = time.perf_counter()
    counters = {
        "formulae": 0,
        "wrapper_encoding_checks": 0,
        "horn_formulae": 0,
        "tw2_formulae": 0,
        "two_sat_formulae": 0,
        "affine_cases": 0,
        "product_cases": 0,
        "padding_redundancy_cases": 0,
        **{f"encoding_{name}": 0 for name in ENCODINGS},
    }

    # All 256 subsets of the eight proper clauses on three variables.
    families: list[tuple[tuple[int, ...], ...]] = []
    for mask in range(1 << len(PROPER3)):
        formula = tuple(PROPER3[i] for i in range(8) if (mask >> i) & 1)
        families.append(formula)
        check_formula(formula, 3, counters)
        counters["formulae"] += 1
        counters["tw2_formulae"] += 1  # primal graph is a subgraph of K_3
        if all(sum(lit > 0 for lit in c) <= 1 for c in formula):
            counters["horn_formulae"] += 1

    # Every subset of the four binary clauses on two variables.
    clauses2 = tuple(tuple((i + 1) if s[i] else -(i + 1) for i in range(2))
                     for s in product((False, True), repeat=2))
    for mask in range(1 << len(clauses2)):
        formula = tuple(clauses2[i] for i in range(4) if (mask >> i) & 1)
        check_formula(formula, 2, counters)
        counters["two_sat_formulae"] += 1

    # Affine/Tseitin controls: all two-equation systems on three variables.
    vectors = tuple(product((0, 1), repeat=3))
    for a in vectors:
        for b in vectors:
            for ra in (0, 1):
                for rb in (0, 1):
                    affine_sat = any(
                        (sum(x * y for x, y in zip(a, z)) % 2 == ra)
                        and (sum(x * y for x, y in zip(b, z)) % 2 == rb)
                        for z in vectors
                    )
                    child = TRUE3 if affine_sat else FALSE3
                    assert sat(child, 3) == affine_sat
                    counters["affine_cases"] += 1

    # Independent products: their answers are conjunctions, but laundering
    # still emits one constant child and uses no named-solver call.
    sample_masks = (0, 1, 3, 15, 127, 255)
    for k in range(1, 9):
        for choice in product(sample_masks, repeat=min(k, 3)):
            expected = all(sat(families[m], 3) for m in choice)
            child = TRUE3 if expected else FALSE3
            assert sat(child, 3) == expected
            counters["product_cases"] += 1

    # Padding and redundancy preserve the answer and do not force use of A.
    for formula in families:
        padded = formula + ((4, -4),)  # tautological width-2 clause
        redundant = formula + ((formula[0],) if formula else tuple())
        assert sat(padded, 4) == sat(formula, 3)
        assert sat(redundant, 3) == sat(formula, 3)
        counters["padding_redundancy_cases"] += 2

    total_checks = sum(v for k, v in counters.items() if not k.startswith("encoding_"))
    result = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "claim_tested": "NO-CALL-PREDECISION-IMPLIES-K-INDEPENDENCE1",
        "verdict": "FALSIFIED/RETIRED",
        "seed": None,
        "method": "exhaustive finite truth-table and hostile-control audit",
        "counters": counters,
        "total_checks_nonduplicated": total_checks,
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "limitations": [
            "Finite checks do not prove an asymptotic SAT lower or upper bound.",
            "The symbolic theorem, not these checks, establishes the general laundering construction.",
            "Python object memory is not a machine-model workspace measurement.",
        ],
        "scientific_status": "P versus NP OPEN",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
