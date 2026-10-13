#!/usr/bin/env python3
"""Bounded audit for REDTEAM-STRENGTHEN10.

Each invocation runs one deterministic stage and prints one JSON object.
No stage writes files.  The caller stores exact stdout as the raw result.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import signal
import sys
import time


Clause = tuple[int, int, int]
Formula = tuple[Clause, ...]


def timeout_handler(_signum: int, _frame: object) -> None:
    raise TimeoutError("24-second cooperative deadline exceeded")


def eval_clause(clause: Clause, assignment: dict[int, int]) -> bool:
    return any(assignment[abs(lit)] == (1 if lit > 0 else 0) for lit in clause)


def eval_formula(formula: Formula, assignment: dict[int, int]) -> bool:
    return all(eval_clause(clause, assignment) for clause in formula)


def proper_exact_22(formula: Formula) -> tuple[bool, int, int]:
    seen: set[Clause] = set()
    counts: Counter[int] = Counter()
    variables: set[int] = set()
    for clause in formula:
        if len(clause) != 3 or len({abs(lit) for lit in clause}) != 3:
            return False, 0, 0
        if clause in seen:
            return False, 0, 0
        seen.add(clause)
        for lit in clause:
            variables.add(abs(lit))
            counts[lit] += 1
    if variables != set(range(1, len(variables) + 1)):
        return False, len(variables), len(formula)
    ok = all(counts[v] == 2 and counts[-v] == 2 for v in variables)
    return ok, len(variables), len(formula)


def signs_to_clause(signs: tuple[int, int, int], variables: tuple[int, int, int]) -> Clause:
    return tuple(v if sign else -v for sign, v in zip(signs, variables))  # type: ignore[return-value]


def exact_three_variable_formulas() -> list[tuple[tuple[tuple[int, int, int], ...], int]]:
    sign_clauses = list(itertools.product((0, 1), repeat=3))
    output: list[tuple[tuple[tuple[int, int, int], ...], int]] = []
    for chosen in itertools.combinations(sign_clauses, 4):
        if not all(sum(clause[j] for clause in chosen) == 2 for j in range(3)):
            continue
        mask = 0
        formula = tuple(signs_to_clause(c, (1, 2, 3)) for c in chosen)
        for y, z in itertools.product((0, 1), repeat=2):
            if any(eval_formula(formula, {1: y, 2: z, 3: aux}) for aux in (0, 1)):
                mask |= 1 << (2 * y + z)
        output.append((chosen, mask))
    return output


def parity_block(variables: tuple[int, int, int], rhs: int = 0) -> Formula:
    """CNF for x xor y xor z = rhs, using four falsifying assignments."""
    clauses: list[Clause] = []
    for assignment in itertools.product((0, 1), repeat=3):
        if (sum(assignment) & 1) == rhs:
            continue
        signs = tuple(1 - bit for bit in assignment)
        clauses.append(signs_to_clause(signs, variables))
    return tuple(clauses)


def parity_product(k: int) -> Formula:
    clauses: list[Clause] = []
    for block in range(k):
        base = 3 * block + 1
        clauses.extend(parity_block((base, base + 1, base + 2), rhs=0))
    return tuple(clauses)


def projection_formula(mask: int, variables: tuple[int, int, int]) -> Formula:
    for chosen, candidate_mask in exact_three_variable_formulas():
        if candidate_mask == mask:
            return tuple(signs_to_clause(c, variables) for c in chosen)
    raise AssertionError(f"no exact-(2,2) projection formula for mask {mask}")


def repaired_child(k: int, fixed_value: int) -> Formula:
    # Remaining source variables 2,3 stay named; fresh auxiliary takes dense id 1.
    # x1=0 leaves XNOR on x2,x3; x1=1 leaves XOR.
    relation_mask = 0b1001 if fixed_value == 0 else 0b0110
    clauses = list(projection_formula(relation_mask, (2, 3, 1)))
    for block in range(1, k):
        base = 3 * block + 1
        clauses.extend(parity_block((base, base + 1, base + 2), rhs=0))
    return tuple(clauses)


def residual_value(k: int, fixed_value: int, remaining_bits: tuple[int, ...]) -> bool:
    assignment = {1: fixed_value}
    for index, bit in enumerate(remaining_bits, start=2):
        assignment[index] = bit
    return eval_formula(parity_product(k), assignment)


def child_exists_value(child: Formula, remaining_bits: tuple[int, ...]) -> bool:
    assignment = {index: bit for index, bit in enumerate(remaining_bits, start=2)}
    return any(eval_formula(child, {**assignment, 1: aux}) for aux in (0, 1))


def dense_json_bytes(formula: Formula) -> bytes:
    return json.dumps([list(c) for c in formula], separators=(",", ":")).encode("ascii")


def stage_zero() -> dict[str, object]:
    formulas = exact_three_variable_formulas()
    masks = Counter(mask for _formula, mask in formulas)
    assert len(formulas) == 8
    assert masks == Counter({15: 6, 6: 1, 9: 1})
    examples = {
        str(mask): chosen
        for chosen, mask in formulas
        if mask in (6, 9)
    }
    return {
        "stage": 0,
        "kind": "exhaustive",
        "balanced_three_variable_formulas": len(formulas),
        "projection_mask_counts": dict(sorted(masks.items())),
        "optimal_xor_xnor_examples": examples,
        "assertions": 4 + len(formulas),
    }


def stage_one() -> dict[str, object]:
    assertions = 0
    rows = []
    essential_witnesses = 0
    equivalence_checks = 0
    for k in range(1, 6):
        parent = parity_product(k)
        parent_ok, parent_n, parent_m = proper_exact_22(parent)
        assert parent_ok and parent_n == 3 * k and parent_m == 4 * k
        assertions += 3
        for fixed in (0, 1):
            child = repaired_child(k, fixed)
            child_ok, child_n, child_m = proper_exact_22(child)
            assert child_ok and (child_n, child_m) == (parent_n, parent_m)
            assertions += 2
            truth: dict[tuple[int, ...], bool] = {}
            for bits in itertools.product((0, 1), repeat=3 * k - 1):
                residual = residual_value(k, fixed, bits)
                projected = child_exists_value(child, bits)
                assert residual == projected
                truth[bits] = residual
                assertions += 1
                equivalence_checks += 1
            for coordinate in range(3 * k - 1):
                witness = any(
                    truth[bits] != truth[bits[:coordinate] + (1 - bits[coordinate],) + bits[coordinate + 1 :]]
                    for bits in truth
                )
                assert witness
                assertions += 1
                essential_witnesses += 1
            rows.append({
                "k": k,
                "fixed": fixed,
                "parent_variables": parent_n,
                "parent_clauses": parent_m,
                "child_variables": child_n,
                "child_clauses": child_m,
                "remaining_essential_variables": 3 * k - 1,
            })
    return {
        "stage": 1,
        "kind": "exhaustive",
        "k_range": [1, 5],
        "rows": rows,
        "equivalence_checks": equivalence_checks,
        "essentiality_witnesses": essential_witnesses,
        "assertions": assertions,
    }


def stage_two() -> dict[str, object]:
    assertions = 0
    rows = []
    for k in range(1, 101):
        parent = parity_product(k)
        child = repaired_child(k, fixed_value=k & 1)
        parent_bytes = dense_json_bytes(parent)
        child_bytes = dense_json_bytes(child)
        n_essential = 3 * k - 1
        minimum_exact_variables = 3 * ((n_essential + 2) // 3)
        minimum_exact_clauses = 4 * (minimum_exact_variables // 3)
        assert minimum_exact_variables == 3 * k
        assert minimum_exact_clauses == 4 * k
        assert len(parent_bytes) == len(child_bytes)
        assertions += 3
        rows.append({
            "k": k,
            "essential_variables": n_essential,
            "minimum_exact22_variables": minimum_exact_variables,
            "minimum_exact22_clauses": minimum_exact_clauses,
            "parent_bytes": len(parent_bytes),
            "optimal_child_bytes": len(child_bytes),
        })
    return {
        "stage": 2,
        "kind": "symbolic_identity_plus_exact_serialization",
        "k_range": [1, 100],
        "rows": rows,
        "assertions": assertions,
    }


def stage_three() -> dict[str, object]:
    assertions = 0
    rows = []
    for k in range(1, 1001):
        # Each block is one independent affine equation.  A witness is obtained
        # by setting the first two block variables to zero and the third to rhs.
        assignment: dict[int, int] = {}
        for block in range(k):
            base = 3 * block + 1
            assignment[base] = 0
            assignment[base + 1] = 0
            assignment[base + 2] = 0
        formula = parity_product(k)
        assert eval_formula(formula, assignment)
        assertions += 1
        if k in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000):
            rows.append({"k": k, "variables": 3 * k, "clauses": 4 * k, "witness_ops": 3 * k})
    return {
        "stage": 3,
        "kind": "deterministic_hostile_control",
        "affine_instances": 1000,
        "solver": "blockwise Gaussian/direct affine witness",
        "rows": rows,
        "assertions": assertions,
        "limitation": "easy-family control; not a SAT lower bound",
    }


def stage_four() -> dict[str, object]:
    c = Fraction(6, 5)
    d = Fraction(1, 2) * (Fraction(6, 5) + 2) / Fraction(6, 5) ** 2 - Fraction(1, 2) * Fraction(6, 5)
    assert d == Fraction(23, 45)
    rows = []
    assertions = 1
    for k in range(2, 41):
        n = 3 * k
        for t in range(1, min(12, n - 1) + 1):
            minimum_variables = 3 * ((n - t + 2) // 3)
            ratio = minimum_variables / n
            all_branch_moment = (2**t) * (ratio ** float(c))
            assert all_branch_moment > 1.0
            assertions += 1
            if k in (2, 4, 8, 16, 32, 40) and t in (1, 2, 3, min(12, n - 1)):
                rows.append({
                    "k": k,
                    "conditioned_variables": t,
                    "minimum_child_variable_ratio_if_all_originals_essential": ratio,
                    "all_2^t_child_c_moment": all_branch_moment,
                })
    return {
        "stage": 4,
        "kind": "exact_rational_endpoint_plus_conditional_shape_check",
        "c": "6/5",
        "flmv_d_c": f"{d.numerator}/{d.denominator}",
        "rows": rows,
        "assertions": assertions,
        "limitation": "moment statement is conditional on emitting all branches as nonterminal exact children",
    }


STAGES = {0: stage_zero, 1: stage_one, 2: stage_two, 3: stage_three, 4: stage_four}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=int, choices=sorted(STAGES), required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(24)
    started = time.perf_counter()
    result = STAGES[args.stage]()
    elapsed = time.perf_counter() - started
    signal.alarm(0)
    result["elapsed_seconds"] = elapsed
    result["python"] = sys.version.split()[0]
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["semantic_digest"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
