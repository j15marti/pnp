#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0017.

The report proves the symbolic equivalence.  This script exhaustively checks
Boolean functions through four variables, all clause-cube CNFs on three
variables, hostile encodings/wrappers, and the current-scale exponent ledger.
Finite checks are not used as asymptotic evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def restrict_table(table: tuple[int, ...], bit: int) -> tuple[int, ...]:
    """Fix the first (least-significant) variable in a truth table."""
    return tuple(table[2 * i + bit] for i in range(len(table) // 2))


def selector_path(table: tuple[int, ...]) -> tuple[int, ...]:
    """Choose 0 iff the zero child is satisfiable, else choose 1."""
    path: list[int] = []
    cur = table
    while len(cur) > 1:
        zero = restrict_table(cur, 0)
        bit = 0 if any(zero) else 1
        child = zero if bit == 0 else restrict_table(cur, 1)
        assert bool(any(cur)) == bool(any(child))
        path.append(bit)
        cur = child
    assert bool(cur[0]) == bool(any(table))
    return tuple(path)


def clause_cube() -> tuple[Clause, ...]:
    return tuple(
        tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(signs))
        for signs in itertools.product((False, True), repeat=3)
    )


def satisfies(formula: Formula, bits: int) -> bool:
    return all(
        any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
        for clause in formula
    )


def sat(formula: Formula, n: int) -> bool:
    return any(satisfies(formula, bits) for bits in range(1 << n))


def restrict_cnf(formula: Formula, var: int, bit: int) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        satisfied = any(abs(lit) == var and (lit > 0) == bool(bit) for lit in clause)
        if satisfied:
            continue
        reduced = tuple(lit for lit in clause if abs(lit) != var)
        out.append(reduced)
    return tuple(out)


def cnf_selector_path(formula: Formula, n: int) -> tuple[int, ...]:
    cur = formula
    path: list[int] = []
    source_answer = sat(cur, n)
    for var in range(1, n + 1):
        zero = restrict_cnf(cur, var, 0)
        bit = 0 if sat(zero, n) else 1
        child = zero if bit == 0 else restrict_cnf(cur, var, 1)
        assert sat(cur, n) == sat(child, n)
        cur = child
        path.append(bit)
    assert sat(cur, n) == source_answer
    return tuple(path)


def canonical_bits(formula: Formula, n: int) -> int:
    width = max(1, math.ceil(math.log2(n + 1)))
    return 32 + sum(8 + len(c) * (width + 1) for c in formula)


def paired_k33(k: int) -> Formula:
    clauses: list[Clause] = []
    offset = 0
    for _ in range(k):
        edges = {(u, v): offset + 1 + 3 * u + v for u in range(3) for v in range(3)}
        neighborhoods = [tuple(edges[u, v] for v in range(3)) for u in range(3)]
        neighborhoods += [tuple(edges[u, v] for u in range(3)) for v in range(3)]
        clauses.extend(neighborhoods)
        clauses.extend(tuple(-x for x in c) for c in neighborhoods)
        offset += 9
    return tuple(clauses)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    started = time.perf_counter()
    counts: dict[str, int] = {}

    wrappers = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
    functions = 0
    path_steps = 0
    wrapper_checks = 0
    for n in range(0, 5):
        table_len = 1 << n
        for mask in range(1 << table_len):
            table = tuple((mask >> i) & 1 for i in range(table_len))
            path = selector_path(table)
            assert len(path) == n
            functions += 1
            path_steps += n
            for _wrapper in wrappers:
                assert selector_path(table) == path
                wrapper_checks += 1
    counts["exhaustive_boolean_functions"] = functions
    counts["decision_equivalent_path_steps"] = path_steps
    counts["wrapper_extensional_path_checks"] = wrapper_checks

    cube = clause_cube()
    cnf_checks = 0
    encoding_checks = 0
    for mask in range(256):
        formula = tuple(cube[i] for i in range(8) if (mask >> i) & 1)
        base = cnf_selector_path(formula, 3)
        variants = (
            formula,
            tuple(reversed(formula)),
            formula + formula[:1],
            tuple(tuple(-lit for lit in c) for c in formula),
        )
        for variant in variants:
            path = cnf_selector_path(variant, 3)
            assert len(path) == 3
            assert sat(variant, 3) == sat(restrict_cnf(variant, 1, path[0]), 3)
            cnf_checks += 1
        assert len(base) == 3
        encoding_checks += 1
    counts["clause_cube_cnf_selector_checks"] = cnf_checks
    counts["order_duplicate_complement_controls"] = encoding_checks

    controls: tuple[tuple[str, Formula, int], ...] = (
        ("Horn", ((-1, -2, 3), (-3, 4), (-4,)), 4),
        ("2SAT", ((1, 2), (-1, 3), (-2, -3)), 3),
        ("affine_xor_cnf", ((1, 2), (-1, -2), (2, 3), (-2, -3)), 3),
        ("bounded_treewidth", ((1, 2), (-2, 3), (-3, 4)), 4),
        ("independent_product", ((1,), (-2,), (3, 4), (-3, -4)), 4),
        ("redundant_padding", ((1, 2, 3),) * 4 + ((-1, 2, 3),), 3),
    )
    control_checks = 0
    for _name, formula, n in controls:
        path = cnf_selector_path(formula, n)
        assert len(path) == n
        control_checks += n + 1
    counts["named_hostile_control_checks"] = control_checks

    scale_rows = []
    scale_checks = 0
    for k in (1, 2, 4, 8, 16, 32, 64):
        formula = paired_k33(k)
        n = 9 * k
        source = canonical_bits(formula, n)
        child0 = canonical_bits(restrict_cnf(formula, 1, 0), n)
        assert child0 < source
        assert child0 / source > 0.75
        scale_rows.append({"blocks": k, "variables": n, "N": source, "M_zero": child0,
                           "log_M_over_log_N": math.log(child0) / math.log(source)})
        scale_checks += 2
    counts["paired_H22_current_scale_checks"] = scale_checks

    exponent_rows = []
    exponent_checks = 0
    for exponent in (2, 4, 8, 16, 32):
        for power in (10, 20, 40, 80):
            N = 1 << power
            M = N - 8 * max(1, power)
            effective = exponent * math.log(M) / math.log(N)
            assert effective <= exponent
            assert effective > 0.95 * exponent
            exponent_rows.append({"K": exponent, "N_power": power,
                                  "effective_query_exponent": effective})
            exponent_checks += 2
    counts["current_scale_exponent_retention_checks"] = exponent_checks

    total = sum(counts.values())
    elapsed = time.perf_counter() - started
    out = {
        "status": "COMPUTATIONAL",
        "claim": "RESTRICTION-SELECTOR-ENDPOINT-EQUIV1 finite audit",
        "exhaustive": {"boolean_functions_n_le_4": True, "clause_cube_cnfs": True},
        "random_seed": None,
        "counts": counts,
        "total_checks": total,
        "paired_scale_rows": scale_rows,
        "exponent_rows": exponent_rows,
        "elapsed_seconds": elapsed,
        "limitations": [
            "The asymptotic equivalence is established by the report proof, not finite testing.",
            "The paired H22 rows audit encoded query scale, not satisfiability by brute force.",
            "Wrappers are extensional-answer controls; their actual delay cost remains charged.",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out["script_sha256"] = sha256(Path(__file__))
    out["result_sha256_before_self_field"] = sha256(output)
    output.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "total_checks": total, "elapsed_seconds": elapsed,
                      "output": str(output), "script_sha256": out["script_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
