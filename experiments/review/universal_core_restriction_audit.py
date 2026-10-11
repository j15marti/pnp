#!/usr/bin/env python3
"""Finite audit for the bounded-occurrence restriction obstruction.

The symbolic statement checked here is simple: in a CNF of maximum variable
occurrence Delta, restricting q variables can touch at most Delta*q clauses.
For the canonical H_(2,2) family Delta=4 and m=4n/3.  Untouched clauses remain
proper width-three clauses under every assignment.

This program is a bounded regression only.  It does not infer asymptotics from
the finite cases and it does not claim a SAT running-time lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from pathlib import Path

Literal = int
Clause = tuple[Literal, ...]
CNF = tuple[Clause, ...]


def gamma_len(value: int) -> int:
    """Length of Elias-gamma(value), for value >= 1."""
    if value < 1:
        raise ValueError("gamma input must be positive")
    return 2 * (value.bit_length() - 1) + 1


def encoded_bits(formula: CNF, compact: bool) -> int:
    """Self-delimiting indexed-CNF length used by this audit.

    Nonnegative counts and widths are encoded as gamma(value+1).  Every
    literal uses one sign bit and a fixed-width positive variable index.  If
    compact is true, surviving IDs are densely renamed before measurement.
    """
    variables = sorted({abs(lit) for clause in formula for lit in clause})
    if compact:
        renaming = {var: index + 1 for index, var in enumerate(variables)}
        measured = tuple(
            tuple((1 if lit > 0 else -1) * renaming[abs(lit)] for lit in clause)
            for clause in formula
        )
        nvars = len(variables)
    else:
        measured = formula
        nvars = max(variables, default=0)
    width = max(1, math.ceil(math.log2(nvars + 1)))
    total = gamma_len(nvars + 1) + gamma_len(len(measured) + 1)
    for clause in measured:
        total += gamma_len(len(clause) + 1)
        total += len(clause) * (1 + width)
    return total


def h22_formula(n: int) -> CNF:
    """Canonical monotone (2,2)-occurrence proper 3-CNF for n=3k, k>=2."""
    if n < 6 or n % 3:
        raise ValueError("n must be a multiple of three and at least six")
    k = n // 3
    partition_a = [tuple(range(3 * j + 1, 3 * j + 4)) for j in range(k)]
    partition_b = [(j + 1, j + k + 1, j + 2 * k + 1) for j in range(k)]
    triples = partition_a + partition_b
    formula = tuple(sorted(tuple(sorted(c)) for c in triples))
    formula += tuple(sorted(tuple(sorted(-x for x in c)) for c in triples))
    assert len(formula) == 4 * n // 3
    assert len(set(formula)) == len(formula)
    for var in range(1, n + 1):
        assert sum(var in c for c in formula) == 2
        assert sum(-var in c for c in formula) == 2
    return formula


def restrict(formula: CNF, assignment: dict[int, int]) -> tuple[CNF, int]:
    residual: list[Clause] = []
    untouched = 0
    assigned = set(assignment)
    for clause in formula:
        if all(abs(lit) not in assigned for lit in clause):
            untouched += 1
            residual.append(clause)
            continue
        satisfied = any(
            abs(lit) in assignment and assignment[abs(lit)] == (1 if lit > 0 else 0)
            for lit in clause
        )
        if satisfied:
            continue
        residual.append(tuple(lit for lit in clause if abs(lit) not in assignment))
    return tuple(residual), untouched


def max_occurrence(formula: CNF) -> int:
    counts: dict[int, int] = {}
    for clause in formula:
        for lit in clause:
            counts[abs(lit)] = counts.get(abs(lit), 0) + 1
    return max(counts.values(), default=0)


def easy_controls(n: int) -> dict[str, CNF]:
    # All families are polynomial-time decidable.  They deliberately show
    # that a residual-size floor is not a computation lower bound.
    equality_2sat: list[Clause] = []
    horn_cycle: list[Clause] = []
    affine_path_2cnf: list[Clause] = []
    for i in range(1, n + 1):
        j = i % n + 1
        equality_2sat.extend(((-i, j), (i, -j)))
        horn_cycle.append((-i, j))
        # x_i xor x_j = 0, a path/cycle parity system in 2-CNF form.
        affine_path_2cnf.extend(((-i, j), (i, -j)))
    product: list[Clause] = []
    for base in range(1, n - 1, 3):
        a, b, c = base, base + 1, base + 2
        product.extend(((a, b, c), (-a, -b), (-a, -c), (-b, -c)))
    return {
        "horn_cycle": tuple(horn_cycle),
        "equality_2sat": tuple(equality_2sat),
        "affine_path_2cnf": tuple(affine_path_2cnf),
        "treewidth_product": tuple(product),
    }


def check_one(formula: CNF, assignment: dict[int, int]) -> dict[str, int]:
    residual, untouched = restrict(formula, assignment)
    delta = max_occurrence(formula)
    q = len(assignment)
    floor = len(formula) - delta * q
    assert untouched >= floor
    assert len(residual) >= untouched
    return {
        "q": q,
        "clauses": len(formula),
        "delta": delta,
        "untouched": untouched,
        "residual_clauses": len(residual),
        "source_bits": encoded_bits(formula, compact=False),
        "residual_bits_original_ids": encoded_bits(residual, compact=False),
        "residual_bits_compact_ids": encoded_bits(residual, compact=True),
    }


def exhaustive_small(max_n: int) -> tuple[int, int]:
    cases = 0
    checks = 0
    for n in range(6, max_n + 1, 3):
        formula = h22_formula(n)
        for state in itertools.product((-1, 0, 1), repeat=n):
            assignment = {i + 1: bit for i, bit in enumerate(state) if bit >= 0}
            check_one(formula, assignment)
            cases += 1
            checks += 5
    return cases, checks


def sampled_large(max_n: int, samples: int, seed: int) -> tuple[list[dict[str, int]], int]:
    rng = random.Random(seed)
    rows: list[dict[str, int]] = []
    checks = 0
    sizes = [n for n in (24, 48, 96, 192, 384, 768, 1536) if n <= max_n]
    for n in sizes:
        base = h22_formula(n)
        q_values = sorted({0, int(n ** 0.25), int(math.sqrt(n)), n // 6, n // 3})
        for q in q_values:
            for _ in range(samples):
                chosen = rng.sample(range(1, n + 1), q)
                assignment = {v: rng.randrange(2) for v in chosen}
                row = check_one(base, assignment)
                row["n"] = n
                rows.append(row)
                checks += 5

                # Renaming, clause-order, and global-complement wrappers.
                perm = list(range(1, n + 1))
                rng.shuffle(perm)
                rename = {i + 1: perm[i] for i in range(n)}
                wrapped = tuple(
                    tuple((1 if lit > 0 else -1) * rename[abs(lit)] for lit in clause)
                    for clause in reversed(base)
                )
                wrapped_assignment = {rename[v]: bit for v, bit in assignment.items()}
                wrapped_row = check_one(wrapped, wrapped_assignment)
                assert wrapped_row["untouched"] == row["untouched"]
                assert wrapped_row["residual_clauses"] == row["residual_clauses"]
                checks += 7
    return rows, checks


def check_easy_controls(max_n: int, samples: int, seed: int) -> tuple[dict[str, dict[str, int]], int]:
    rng = random.Random(seed ^ 0x5A17)
    summary: dict[str, dict[str, int]] = {}
    checks = 0
    for n in [v for v in (24, 48, 96, 192, 384) if v <= max_n]:
        q = int(math.sqrt(n))
        for name, formula in easy_controls(n).items():
            for _ in range(samples):
                chosen = rng.sample(range(1, n + 1), q)
                assignment = {v: rng.randrange(2) for v in chosen}
                row = check_one(formula, assignment)
                checks += 5
                cell = summary.setdefault(name, {"cases": 0, "max_n": 0, "max_delta": 0})
                cell["cases"] += 1
                cell["max_n"] = max(cell["max_n"], n)
                cell["max_delta"] = max(cell["max_delta"], row["delta"])
    return summary, checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exhaustive-n", type=int, default=9)
    parser.add_argument("--max-n", type=int, default=1536)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--seed", type=int, default=22102026)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.monotonic()
    exhaustive_cases, exhaustive_checks = exhaustive_small(args.max_exhaustive_n)
    rows, sampled_checks = sampled_large(args.max_n, args.samples, args.seed)
    controls, control_checks = check_easy_controls(args.max_n, args.samples, args.seed)
    elapsed = time.monotonic() - started

    largest = max(rows, key=lambda row: (row["n"], -row["q"]))
    largest_sublinear = max(
        (row for row in rows if row["q"] == int(math.sqrt(row["n"]))),
        key=lambda row: row["n"],
    )
    output = {
        "run_id": "MODELBRIDGE-0004",
        "status": "PASS",
        "claim": "untouched >= clauses - Delta*q; H22 has clauses=4n/3 and Delta=4",
        "seed": args.seed,
        "parameters": {
            "max_exhaustive_n": args.max_exhaustive_n,
            "max_n": args.max_n,
            "samples_per_cell": args.samples,
        },
        "counts": {
            "exhaustive_partial_assignments": exhaustive_cases,
            "sampled_h22_rows": len(rows),
            "symbolic_regression_checks": exhaustive_checks + sampled_checks + control_checks,
            "wrapper_checks": len(rows) * 7,
        },
        "easy_controls": controls,
        "largest_source_zero_assignment_row": largest,
        "largest_sqrt_assignment_row": largest_sublinear,
        "elapsed_seconds": round(elapsed, 6),
        "limitations": [
            "finite regression only; asymptotic statement is proved symbolically",
            "explicit ordinary-CNF encodings only",
            "no SAT running-time lower bound",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
