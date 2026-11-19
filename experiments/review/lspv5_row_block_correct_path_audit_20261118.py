#!/usr/bin/env python3
"""Exact finite audit for the LSPV-5 row/block correct-path reproduction.

The experiment checks only finite semantic controls and exact rational exponent
arithmetic.  It is not an asymptotic lower-bound proof and it does not provide a
SAT oracle.  Every exhaustive component is constant-size and finishes quickly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


UNKNOWN = "UNKNOWN"
SAT = "SAT"
UNSAT = "UNSAT"


def q(x: Fraction) -> dict[str, object]:
    return {
        "fraction": f"{x.numerator}/{x.denominator}",
        "decimal": float(x),
    }


def sat_row_verifier(table: tuple[tuple[bool, ...], ...], row: int) -> str:
    """Sound partial SAT verifier: a row is a certificate iff every block is SAT."""
    if 0 <= row < len(table) and all(table[row]):
        return SAT
    return UNKNOWN


def unsat_route_verifier(
    table: tuple[tuple[bool, ...], ...], route: tuple[int, ...]
) -> str:
    """Sound partial UNSAT verifier: each row names an actually refutable block."""
    if len(route) != len(table):
        return UNKNOWN
    width = len(table[0])
    for row, block in enumerate(route):
        if not (0 <= block < width) or table[row][block]:
            return UNKNOWN
    return UNSAT


def exhaustive_boolean_layout(rows: int = 3, blocks: int = 3) -> dict[str, int]:
    patterns = sat_patterns = unsat_patterns = assertions = 0
    route_space = tuple(product(range(blocks), repeat=rows))
    for bits in product((False, True), repeat=rows * blocks):
        table = tuple(
            tuple(bits[r * blocks + b] for b in range(blocks))
            for r in range(rows)
        )
        global_sat = any(all(row) for row in table)
        global_unsat = all(any(not cell for cell in row) for row in table)
        assert global_sat != global_unsat
        assertions += 1
        patterns += 1

        if global_sat:
            sat_patterns += 1
            witness_row = next(r for r, row in enumerate(table) if all(row))
            assert sat_row_verifier(table, witness_row) == SAT
            assertions += 1
        else:
            unsat_patterns += 1
            route = tuple(next(b for b, cell in enumerate(row) if not cell) for row in table)
            assert unsat_route_verifier(table, route) == UNSAT
            assertions += 1

        # Wrong-path soundness: no verifier may certify the opposite global answer.
        for r in range(rows):
            result = sat_row_verifier(table, r)
            assert result in (SAT, UNKNOWN)
            assert result != SAT or global_sat
            assertions += 2
        for route in route_space:
            result = unsat_route_verifier(table, route)
            assert result in (UNSAT, UNKNOWN)
            assert result != UNSAT or global_unsat
            assertions += 2

    return {
        "patterns": patterns,
        "sat_patterns": sat_patterns,
        "unsat_patterns": unsat_patterns,
        "routes_per_pattern": len(route_space),
        "assertions": assertions,
    }


def t5_h9_control() -> dict[str, object]:
    # Four source paths BBB/FBB/FFF/BB represented by their forbidden differences.
    forbidden = ({4}, {3}, {1}, {0, 2})
    coverage = [0, 0, 0, 0]
    assertions = 0
    route = {}
    for a, b in product(range(5), repeat=2):
        d = (b - a) % 5
        bad = [i for i, excluded in enumerate(forbidden) if d in excluded]
        assert len(bad) == 1
        assertions += 1
        coverage[bad[0]] += 1
        route[f"{a},{b}"] = bad[0]
    assert coverage == [5, 5, 5, 10]
    assertions += 1
    assert set().union(*forbidden) == set(range(5))
    assertions += 1
    return {
        "terminal_rows": 25,
        "path_names": ["BBB", "FBB", "FFF", "BB"],
        "forbidden_differences": [sorted(x) for x in forbidden],
        "coverage": coverage,
        "unique_bad_block_route": route,
        "assertions": assertions,
    }


def exponent_audit() -> dict[str, object]:
    row = Fraction(39, 200)       # 0.195
    block_count = Fraction(13, 20)  # 0.65
    child = Fraction(7, 20)       # 0.35
    scan_calls = row + block_count
    local_work = Fraction(239, 200)  # 1.195
    target_time = Fraction(133, 100)
    target_space = Fraction(1, 2)
    time_seed_gate = (target_time - scan_calls) / child
    space_seed_gate = target_space / child
    fixed_time = scan_calls / (1 - child)
    fixed_space = child

    assert time_seed_gate == Fraction(97, 70)
    assert space_seed_gate == Fraction(10, 7)
    assert fixed_time == Fraction(13, 10)

    t = Fraction(100)
    s = Fraction(100)
    iterations = []
    for j in range(1, 9):
        t = max(local_work, scan_calls + child * t)
        s = max(child, child * s)
        iterations.append({"iteration": j, "time": q(t), "space": q(s)})
    assert t < target_time
    assert s == child

    # Ordinary bit-pinning: B*m=n queries; writing an m-sized residual each time.
    witness_queries = block_count + child
    witness_materialization = witness_queries + child
    direct_seed_130 = witness_queries + child * Fraction(13, 10)
    assert witness_queries == 1
    assert witness_materialization == Fraction(27, 20)
    assert direct_seed_130 == Fraction(291, 200)

    return {
        "row_exponent": q(row),
        "block_count_exponent": q(block_count),
        "child_length_exponent": q(child),
        "scan_call_exponent": q(scan_calls),
        "local_validation_exponent": q(local_work),
        "one_step_time_seed_gate_for_1_33": q(time_seed_gate),
        "one_step_space_seed_gate_for_0_5": q(space_seed_gate),
        "hereditary_fixed_time": q(fixed_time),
        "hereditary_fixed_space": q(fixed_space),
        "iterations_from_100": iterations,
        "naive_witness_query_exponent": q(witness_queries),
        "naive_witness_materialization_exponent": q(witness_materialization),
        "naive_witness_time_with_seed_1_30": q(direct_seed_130),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = {
        "status": "PASS",
        "scope": "finite semantic controls and exact rational exponent arithmetic only",
        "boolean_layout": exhaustive_boolean_layout(),
        "t5_h9_control": t5_h9_control(),
        "exponents": exponent_audit(),
    }
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["result_payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
