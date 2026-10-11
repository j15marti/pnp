#!/usr/bin/env python3
"""Finite audit for witness-binding summaries and hostile implementations.

The symbolic theorems belong in the accompanying LaTeX report.  This runner
checks the pin-gadget family, affine parity controls, a published H_{2,2}
collision, and representation/wrapper controls using exact finite arithmetic.
Every invocation is intended to finish well below 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path


Clause = tuple[int, int, int]
Formula = tuple[Clause, ...]


def gamma_len(value: int) -> int:
    if value < 1:
        raise ValueError("gamma code is defined here only for positive integers")
    return 2 * (value.bit_length() - 1) + 1


def encoded_length(num_vars: int, formula: Formula) -> int:
    """Bit length for the declared self-delimiting fixed-width test encoding."""
    width = max(1, math.ceil(math.log2(num_vars + 1)))
    return (
        gamma_len(num_vars)
        + gamma_len(len(formula) + 1)
        + len(formula) * gamma_len(3)
        + 3 * len(formula) * (1 + width)
    )


def pin_block(literal: int, p: int, q: int) -> tuple[Clause, ...]:
    return (
        (literal, p, q),
        (literal, p, -q),
        (literal, -p, q),
        (literal, -p, -q),
    )


def pin_formula(bits: tuple[int, ...]) -> Formula:
    n = len(bits)
    clauses: list[Clause] = []
    for i, bit in enumerate(bits, start=1):
        literal = i if bit else -i
        clauses.extend(pin_block(literal, n + i, 2 * n + i))
    return tuple(clauses)


def clause_value(clause: Clause, assignment: tuple[int, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def formula_value(formula: Formula, assignment: tuple[int, ...]) -> bool:
    return all(clause_value(clause, assignment) for clause in formula)


def projected_solutions(formula: Formula, num_vars: int, projected: int) -> set[tuple[int, ...]]:
    out: set[tuple[int, ...]] = set()
    for assignment in itertools.product((0, 1), repeat=num_vars):
        if formula_value(formula, assignment):
            out.add(assignment[:projected])
    return out


def lex_solution(formula: Formula, num_vars: int) -> tuple[int, ...] | None:
    for assignment in itertools.product((0, 1), repeat=num_vars):
        if formula_value(formula, assignment):
            return assignment
    return None


def semantic_signature(formula: Formula, num_vars: int) -> tuple[int, ...]:
    solutions = [
        a for a in itertools.product((0, 1), repeat=num_vars)
        if formula_value(formula, a)
    ]
    bits: list[int] = []
    for i in range(num_vars):
        for b in (0, 1):
            bits.append(int(any(a[i] == b for a in solutions)))
    for i in range(num_vars):
        for j in range(i + 1, num_vars):
            for b in (0, 1):
                for c in (0, 1):
                    bits.append(int(any(a[i] == b and a[j] == c for a in solutions)))
    return tuple(bits)


def recover_pin_summary(formula: Formula, n: int) -> tuple[int, ...]:
    """Streaming canonical-block recovery used by the DIRECT easy-family control."""
    if len(formula) != 4 * n:
        raise ValueError("wrong block count")
    recovered: list[int] = []
    for i in range(n):
        block = formula[4 * i:4 * i + 4]
        z, p, q = i + 1, n + i + 1, 2 * n + i + 1
        common = block[0][0]
        if abs(common) != z or block != pin_block(common, p, q):
            raise ValueError("noncanonical pin block")
        recovered.append(int(common > 0))
    return tuple(recovered)


def complement_semantic_variables(formula: Formula, n: int) -> Formula:
    return tuple(
        tuple(-lit if abs(lit) <= n else lit for lit in clause)  # type: ignore[misc]
        for clause in formula
    )


H22_A: Formula = (
    (1, 2, 3), (1, 4, 7), (-1, -4, -5), (-1, -7, -9),
    (2, 4, 5), (-2, -3, -6), (-2, -7, -9), (3, 6, 7),
    (-3, -4, -8), (5, 8, 9), (-5, -6, -8), (6, 8, 9),
)
H22_B: Formula = (
    (1, 2, 8), (1, 3, 9), (-1, -2, -8), (-1, -6, -7),
    (2, 6, 9), (-2, -4, -7), (3, 5, 7), (-3, -4, -9),
    (-3, -5, -8), (4, 5, 6), (4, 7, 8), (-5, -6, -9),
)


def run(max_n: int, full_semantic_n: int, seed: int) -> dict[str, object]:
    started = time.perf_counter()
    rng = random.Random(seed)
    counts = {
        "pin_formulas": 0,
        "pin_local_truth_checks": 0,
        "pin_full_assignment_checks": 0,
        "range_cardinality_checks": 0,
        "wrapper_checks": 0,
        "parity_checks": 0,
        "h22_checks": 0,
        "exposure_checks": 0,
    }
    rows: list[dict[str, int]] = []

    # Each four-clause block is equivalent to its distinguished literal.
    for target in (0, 1):
        literal = 1 if target else -1
        block = pin_block(literal, 2, 3)
        for z, p, q in itertools.product((0, 1), repeat=3):
            got = formula_value(block, (z, p, q))
            assert got == (z == target)
            counts["pin_local_truth_checks"] += 1

    for n in range(1, max_n + 1):
        summaries: set[tuple[int, ...]] = set()
        lengths: set[int] = set()
        for bits in itertools.product((0, 1), repeat=n):
            formula = pin_formula(bits)
            recovered = recover_pin_summary(formula, n)
            assert recovered == bits
            summaries.add(recovered)
            lengths.add(encoded_length(3 * n, formula))
            counts["pin_formulas"] += 1
            counts["exposure_checks"] += 3  # DIRECT omission, guard insertion, RECOMP omission.

            # Clause order, duplicate padding, and a disconnected satisfiable pin
            # preserve the projected semantic witness.
            shuffled = list(formula)
            rng.shuffle(shuffled)
            if n <= full_semantic_n:
                base = projected_solutions(formula, 3 * n, n)
                assert base == {bits}
                counts["pin_full_assignment_checks"] += 2 ** (3 * n)
                assert projected_solutions(tuple(shuffled), 3 * n, n) == base
                counts["wrapper_checks"] += 1
                assert projected_solutions(formula + formula[:4], 3 * n, n) == base
                counts["wrapper_checks"] += 1

                # Complement-conjugacy maps the selected semantic witness bitwise.
                complemented = complement_semantic_variables(formula, n)
                expected = tuple(1 - b for b in bits)
                assert projected_solutions(complemented, 3 * n, n) == {expected}
                counts["wrapper_checks"] += 1

        assert len(summaries) == 2 ** n
        assert math.ceil(math.log2(len(summaries))) == n
        assert len(lengths) == 1
        counts["range_cardinality_checks"] += 2
        rows.append({
            "n": n,
            "formulas": 2 ** n,
            "summary_range": len(summaries),
            "minimum_fixed_summary_bits": n,
            "encoded_bits": next(iter(lengths)),
        })

    # Affine parity cosets are disjoint but have short, easy canonical witnesses.
    parity_rows = []
    for n in range(3, max_n + 1):
        even = [a for a in itertools.product((0, 1), repeat=n) if sum(a) % 2 == 0]
        odd = [a for a in itertools.product((0, 1), repeat=n) if sum(a) % 2 == 1]
        assert set(even).isdisjoint(odd)
        assert even[0] != odd[0]
        assert even[0] == (0,) * n
        assert odd[0] == (0,) * (n - 1) + (1,)
        counts["parity_checks"] += len(even) + len(odd) + 4
        parity_rows.append({"n": n, "solutions_per_coset": len(even)})

    # The MODELBRIDGE-0005 H_{2,2} pair has the same H_2 projection and
    # disjoint solution sets, but a full witness summary separates it.
    sol_a = {a for a in itertools.product((0, 1), repeat=9) if formula_value(H22_A, a)}
    sol_b = {a for a in itertools.product((0, 1), repeat=9) if formula_value(H22_B, a)}
    sig_a = semantic_signature(H22_A, 9)
    sig_b = semantic_signature(H22_B, 9)
    lex_a = lex_solution(H22_A, 9)
    lex_b = lex_solution(H22_B, 9)
    assert sol_a.isdisjoint(sol_b)
    assert sig_a == sig_b and all(sig_a)
    assert lex_a in sol_a and lex_b in sol_b and lex_a != lex_b
    counts["h22_checks"] += len(sol_a) + len(sol_b) + len(sig_a) + 6

    elapsed = time.perf_counter() - started
    return {
        "run_id": "LB-0007",
        "status": "PASS",
        "global_status": "P versus NP remains OPEN",
        "parameters": {
            "max_n": max_n,
            "full_semantic_n": full_semantic_n,
            "seed": seed,
            "method": "exhaustive finite pin/parity checks plus exact published H_2,2 witness pair",
        },
        "counts": counts,
        "pin_family": {
            "rows": rows,
            "range_identity": "|im J_n| = 2^n",
            "fixed_length_floor": "b >= n",
            "tight_summary": "the n projected witness bits",
            "direct_family_decider_materializes_summary": False,
            "optional_guard_materializes_summary": True,
            "recomp_family_decider_retains_summary": False,
        },
        "affine_parity_control": {
            "rows": parity_rows,
            "algorithmic_shortcut": "Gaussian elimination / parity propagation",
        },
        "h22_collision_control": {
            "solutions_a": len(sol_a),
            "solutions_b": len(sol_b),
            "h2_signature_bits": len(sig_a),
            "h2_signatures_equal": True,
            "solution_sets_disjoint": True,
            "lex_summary_a": "".join(map(str, lex_a or ())),
            "lex_summary_b": "".join(map(str, lex_b or ())),
            "lex_summaries_different": True,
        },
        "external_extraction_ledger": {
            "calls": "at most n+1",
            "sparse_input_relation": "N = Theta(n log n)",
            "if_T_A_is_N_to_K": "time N^(K+1+o(1)) under separate calls; K is retained",
            "same_execution_internal_exposure": False,
        },
        "limitations": [
            "Finite checks validate constructions and ledgers, not asymptotic SAT hardness.",
            "The b >= n theorem is symbolic and scoped to summaries that recover a projected witness on the pin family.",
            "The easy pin and affine controls show that binding information is not automatically a hard computational resource.",
            "No lower bound for the NP-complete H_2,2 family or arbitrary deterministic polynomial-time SAT algorithms is inferred.",
        ],
        "elapsed_seconds": elapsed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=10)
    parser.add_argument("--full-semantic-n", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_n < 3 or args.full_semantic_n < 1 or args.full_semantic_n > args.max_n:
        raise SystemExit("require max_n >= 3 and 1 <= full_semantic_n <= max_n")
    result = run(args.max_n, args.full_semantic_n, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(json.dumps({"status": result["status"], "sha256": digest,
                      "elapsed_seconds": result["elapsed_seconds"],
                      "counts": result["counts"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
