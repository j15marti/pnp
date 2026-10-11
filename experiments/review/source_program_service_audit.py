#!/usr/bin/env python3
"""Finite audit for the source-plus-program continuation-service control.

This is a falsification harness, not an asymptotic lower-bound experiment.
For small CNFs it checks that a fixed generic evaluator, given the source
formula and a query assignment, returns exactly the corresponding coordinate
of the materialized restriction-answer service.  It also checks semantic
wrappers and the elementary exponent ledger showing that black-box service
evaluation retains the unknown exponent of the supplied SAT decider.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]


def variables(formula: Formula) -> Tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, assignment: Mapping[int, int]) -> bool:
    return all(any(bool(assignment[abs(lit)]) == (lit > 0) for lit in clause)
               for clause in formula)


def residual_sat(formula: Formula, query: Mapping[int, int]) -> bool:
    """Generic exact evaluator: enumerate only variables not fixed by query."""
    free = tuple(v for v in variables(formula) if v not in query)
    for bits in itertools.product((0, 1), repeat=len(free)):
        assignment = dict(query)
        assignment.update(zip(free, bits))
        if satisfies(formula, assignment):
            return True
    return False


def projected_service(formula: Formula, query_vars: Sequence[int]) -> Dict[Tuple[int, ...], bool]:
    """Independent construction: enumerate full models once and project."""
    all_vars = variables(formula)
    answer = {bits: False for bits in itertools.product((0, 1), repeat=len(query_vars))}
    for full_bits in itertools.product((0, 1), repeat=len(all_vars)):
        assignment = dict(zip(all_vars, full_bits))
        if satisfies(formula, assignment):
            answer[tuple(assignment[v] for v in query_vars)] = True
    return answer


def canonical_bytes(formula: Formula) -> bytes:
    payload = [[int(lit) for lit in clause] for clause in formula]
    return json.dumps(payload, separators=(",", ":"), sort_keys=False).encode("ascii")


def xor_gate(a: int, b: int, c: int) -> Formula:
    # c = a xor b, as four proper three-clauses.
    return ((a, b, -c), (a, -b, c), (-a, b, c), (-a, -b, -c))


def h22_block(offset: int = 0) -> Formula:
    edges = ((1, 2, 3), (3, 4, 5), (5, 6, 1), (2, 4, 6))
    clauses: List[Clause] = []
    for edge in edges:
        pos = tuple(offset + x for x in edge)
        clauses.extend((pos, tuple(-x for x in pos)))
    return tuple(clauses)


def disjoint_h22(blocks: int) -> Formula:
    return tuple(clause for b in range(blocks) for clause in h22_block(6 * b))


@dataclass(frozen=True)
class Case:
    name: str
    formula: Formula
    query_vars: Tuple[int, ...]


def cases() -> Tuple[Case, ...]:
    horn_equality: Formula = tuple(
        clause
        for i in range(1, 8)
        for clause in ((-i, i + 1), (i, -(i + 1)))
    )
    two_sat_path: Formula = tuple(
        clause
        for i in range(1, 8)
        for clause in ((i, i + 1), (-i, i + 1))
    )
    affine: Formula = tuple(
        clause
        for gate in (xor_gate(1, 2, 4), xor_gate(4, 3, 5), xor_gate(5, 6, 7))
        for clause in gate
    ) + ((7, 7, 7),)
    bounded_tw: Formula = tuple(
        clause
        for i in range(1, 8)
        for clause in ((i, -(i + 1)), (-i, i + 1))
    ) + ((1, 1, 1),)
    return (
        Case("horn_equality", horn_equality, (1, 3, 5, 7)),
        Case("two_sat_path", two_sat_path, (1, 3, 5, 7)),
        Case("affine_tseitin", affine, (1, 2, 3, 6)),
        Case("bounded_treewidth_path", bounded_tw, (2, 4, 6, 8)),
        Case("h22_block", disjoint_h22(1), (1, 2, 3, 4, 5)),
        Case("h22_independent_product", disjoint_h22(2), tuple(list(range(1, 6)) + list(range(7, 12)))),
    )


def permute(formula: Formula, permutation: Mapping[int, int]) -> Formula:
    return tuple(tuple((1 if lit > 0 else -1) * permutation[abs(lit)] for lit in clause)
                 for clause in formula)


def complement(formula: Formula, flipped: Iterable[int]) -> Formula:
    flip = set(flipped)
    return tuple(tuple(-lit if abs(lit) in flip else lit for lit in clause)
                 for clause in formula)


def query_bits(query_vars: Sequence[int]) -> Iterable[Tuple[int, ...]]:
    return itertools.product((0, 1), repeat=len(query_vars))


def audit_case(case: Case) -> Dict[str, object]:
    service = projected_service(case.formula, case.query_vars)
    coordinates = 0
    wrapper_checks = 0

    all_vars = variables(case.formula)
    reverse = {v: all_vars[-1 - i] for i, v in enumerate(all_vars)}
    perm_formula = permute(case.formula, reverse)
    perm_qvars = tuple(reverse[v] for v in case.query_vars)
    flip = {v for v in all_vars if v % 2 == 0}
    comp_formula = complement(case.formula, flip)

    copied = case.formula + case.formula
    dead = case.formula + ((all_vars[0], -all_vars[0]),)
    padded_var = max(all_vars) + 1
    padded = case.formula + ((padded_var, -padded_var),)

    for bits in query_bits(case.query_vars):
        query = dict(zip(case.query_vars, bits))
        expected = service[bits]
        assert residual_sat(case.formula, query) == expected
        coordinates += 1

        # COPY, DEAD, padding, DELAY (semantic no-op), and RECOMP.
        for wrapped in (copied, dead, padded, tuple(tuple(c) for c in case.formula), case.formula):
            assert residual_sat(wrapped, query) == expected
            wrapper_checks += 1

        # INTERP: variable renaming and variable complementation.
        perm_query = {reverse[v]: bit for v, bit in query.items()}
        assert residual_sat(perm_formula, perm_query) == expected
        wrapper_checks += 1
        comp_query = {v: (1 - bit if v in flip else bit) for v, bit in query.items()}
        assert residual_sat(comp_formula, comp_query) == expected
        wrapper_checks += 1

    # One-bit endpoint: the empty query is precisely SAT(F).
    assert residual_sat(case.formula, {}) == any(service.values())
    source_bits = 8 * len(canonical_bytes(case.formula))
    return {
        "case": case.name,
        "variables": len(all_vars),
        "clauses": len(case.formula),
        "query_variables": len(case.query_vars),
        "service_coordinates": coordinates,
        "satisfying_coordinates": sum(service.values()),
        "source_representation_bits": source_bits,
        "explicit_vector_bits": 1 << len(case.query_vars),
        "wrapper_checks": wrapper_checks,
        "one_bit_endpoint_checked": True,
    }


def symbolic_h22_rows(max_blocks: int) -> List[Dict[str, object]]:
    rows = []
    for b in range(1, max_blocks + 1):
        # Count a concrete source serialization without materializing its service.
        source_bits = 8 * len(canonical_bytes(disjoint_h22(b)))
        rows.append({
            "blocks": b,
            "source_bits": source_bits,
            "query_bits": 5 * b,
            "explicit_vector_bits": 1 << (5 * b),
            "source_program_payload_bits": source_bits,
            "fixed_evaluator_code_counted_separately": True,
        })
    return rows


def exponent_ledger() -> Dict[str, object]:
    rows = []
    for a in (Fraction(1, 1), Fraction(3, 2), Fraction(2, 1)):
        for construction in (1, 2, 3):
            for k in range(1, 13):
                inherited = max(Fraction(construction, 1), a * k)
                assert inherited >= k
                rows.append({
                    "restriction_length_exponent": str(a),
                    "construction_exponent": construction,
                    "decider_exponent_K": k,
                    "service_exponent": str(inherited),
                    "retains_K": inherited >= k,
                })
    return {"checks": len(rows), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbolic-blocks", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    start = time.perf_counter()
    finite = [audit_case(case) for case in cases()]
    ledger = exponent_ledger()
    elapsed = time.perf_counter() - start
    result = {
        "experiment": "source_program_service_audit",
        "status": "COMPUTATIONAL",
        "seed": args.seed,
        "method": "exhaustive finite truth checks plus exact rational exponent arithmetic",
        "runtime_seconds": elapsed,
        "finite_cases": finite,
        "totals": {
            "service_coordinates": sum(int(row["service_coordinates"]) for row in finite),
            "wrapper_checks": sum(int(row["wrapper_checks"]) for row in finite),
            "one_bit_endpoints": len(finite),
            "exponent_checks": ledger["checks"],
        },
        "symbolic_h22_scaling": symbolic_h22_rows(args.symbolic_blocks),
        "exponent_ledger": ledger,
        "limitations": [
            "Finite formula checks do not establish asymptotic lower bounds.",
            "The generic evaluator is exhaustive; it witnesses description size, not fast evaluation.",
            "Under SAT in P, replacing exhaustive search by the assumed decider gives polynomial evaluation but retains its unknown exponent K.",
            "The concrete JSON byte count is illustrative; the theorem applies to any fixed injective source encoding by storing that encoding verbatim.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["totals"], sort_keys=True))
    print(f"runtime_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
