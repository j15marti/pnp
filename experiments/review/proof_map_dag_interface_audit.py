#!/usr/bin/env python3
"""Exact finite audit for DAG-acquisition versus one-bit SAT decision.

Builds reduced OBDDs for equality under grouped and interleaved variable
orders.  The grouped representation is exponential although the same
treewidth-one 2-CNF has a linear interleaved OBDD and a constant SAT answer.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path


def _alarm(_signum, _frame):
    raise TimeoutError("25-second cooperative budget exceeded")


def equality_cnf(n: int, duplicate: bool = False) -> list[tuple[int, int]]:
    clauses = []
    for i in range(n):
        x, y = i + 1, n + i + 1
        clauses.extend([(-x, y), (x, -y)])
    return clauses * (2 if duplicate else 1)


def eval_cnf(clauses: list[tuple[int, int]], assignment: int) -> int:
    for clause in clauses:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return 0
    return 1


def robdd_size(n: int, order: list[int], complement_y: bool = False) -> int:
    values = [0] * (2 * n)
    unique: dict[tuple[int, int, int], int] = {}
    next_id = 2  # terminals 0 and 1

    def rec(depth: int) -> int:
        nonlocal next_id
        if depth == len(order):
            target = [1 - b for b in values[n:]] if complement_y else values[n:]
            return int(values[:n] == target)
        var = order[depth]
        values[var] = 0
        low = rec(depth + 1)
        values[var] = 1
        high = rec(depth + 1)
        if low == high:
            return low
        key = (var, low, high)
        if key not in unique:
            unique[key] = next_id
            next_id += 1
        return unique[key]

    rec(0)
    return len(unique)


def run(max_n: int) -> dict:
    start = time.perf_counter()
    rows = []
    semantic_checks = 0
    size_checks = 0
    wrapper_checks = 0
    for n in range(1, max_n + 1):
        grouped = list(range(2 * n))
        interleaved = [v for i in range(n) for v in (i, n + i)]
        grouped_size = robdd_size(n, grouped)
        interleaved_size = robdd_size(n, interleaved)
        affine_grouped = robdd_size(n, grouped, complement_y=True)
        affine_interleaved = robdd_size(n, interleaved, complement_y=True)
        assert grouped_size == 3 * ((1 << n) - 1)
        assert interleaved_size == 3 * n
        assert affine_grouped == grouped_size
        assert affine_interleaved == interleaved_size
        size_checks += 4

        cnf = equality_cnf(n)
        duplicate = equality_cnf(n, duplicate=True)
        for assignment in range(1 << (2 * n)):
            x = assignment & ((1 << n) - 1)
            y = assignment >> n
            expected = int(x == y)
            assert eval_cnf(cnf, assignment) == expected
            assert eval_cnf(duplicate, assignment) == expected
            semantic_checks += 1
            wrapper_checks += 1

        rows.append({
            "n_pairs": n,
            "boolean_variables": 2 * n,
            "cnf_clauses": 2 * n,
            "grouped_order_robdd_nodes": grouped_size,
            "interleaved_order_robdd_nodes": interleaved_size,
            "fixed_instance_decision_dag_nodes_at_most": 1,
            "grouped_formula": "3*(2^n-1)",
            "interleaved_formula": "3*n",
        })

    first_grouped_exceeds_linear = next(
        row["n_pairs"] for row in rows
        if row["grouped_order_robdd_nodes"] > 10 * row["n_pairs"]
    )
    return {
        "status": "PASS",
        "scope": {
            "max_n": max_n,
            "exhaustive": True,
            "function": "equality encoded as treewidth-one 2-CNF",
            "warning": "ROBDD size is representation- and variable-order-specific, not arbitrary SAT runtime.",
        },
        "checks": {
            "semantic_assignments": semantic_checks,
            "duplicate_clause_wrapper_checks": wrapper_checks,
            "exact_size_identity_checks": size_checks,
        },
        "first_n_grouped_nodes_exceed_10n": first_grouped_exceeds_linear,
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - start,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    result = run(args.max_n)
    signal.alarm(0)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["checks"], sort_keys=True))
    print(f"elapsed_seconds={result['elapsed_seconds']:.6f}")


if __name__ == "__main__":
    main()
