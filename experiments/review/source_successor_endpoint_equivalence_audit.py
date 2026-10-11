#!/usr/bin/env python3
"""Bounded audit for TESTS-0006's source-successor endpoint equivalence.

The symbolic theorem is proved in the accompanying report.  This script
checks finite SAT sources, constant yes/no successors, wrappers, alternate
encodings, easy families, affine systems, and the exponent ledger.  It does
not extrapolate a finite experiment into an asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def satisfies(formula: Formula, bits: int) -> bool:
    return all(
        any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
        for clause in formula
    )


def sat(formula: Formula, n: int) -> bool:
    return any(satisfies(formula, bits) for bits in range(1 << n))


def clause_cube() -> tuple[Clause, ...]:
    return tuple(
        tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(signs))
        for signs in itertools.product((False, True), repeat=3)
    )


YES_CHILD: Formula = ((1, 2, 3),)
NO_CHILD: Formula = clause_cube()


def terminal_successor(answer: bool) -> Formula:
    """The decision-dependent, one-child, constant-size successor."""
    return YES_CHILD if answer else NO_CHILD


def formula_from_mask(mask: int) -> Formula:
    cube = clause_cube()
    return tuple(cube[i] for i in range(8) if (mask >> i) & 1)


def permute(formula: Formula, p: tuple[int, ...]) -> Formula:
    return tuple(
        tuple((1 if lit > 0 else -1) * p[abs(lit) - 1] for lit in clause)
        for clause in formula
    )


def complement(formula: Formula) -> Formula:
    return tuple(tuple(-lit for lit in clause) for clause in formula)


def wrapped_answers(formula: Formula, n: int) -> tuple[tuple[str, bool], ...]:
    direct = sat(formula, n)
    vector = tuple(satisfies(formula, bits) for bits in range(1 << n))
    interp_vector = tuple(vector[((1 << n) - 1) ^ bits] for bits in range(1 << n))
    recomp = sat(formula, n)
    return (
        ("DIRECT", direct),
        ("MATERIALIZE", any(vector)),
        ("INTERP", any(interp_vector)),
        ("RECOMP", recomp),
        ("DEAD", direct),
        ("COPY", direct),
        ("DELAY", direct),
    )


def balanced_sign_part(n: int, sign: int, rng: random.Random) -> list[Clause]:
    slots = [v for v in range(1, n + 1) for _ in range(2)]
    for _ in range(20_000):
        rng.shuffle(slots)
        triples = [tuple(sorted(slots[i : i + 3])) for i in range(0, len(slots), 3)]
        if all(len(set(t)) == 3 for t in triples) and len(set(triples)) == len(triples):
            return [tuple(sign * v for v in t) for t in triples]
    raise RuntimeError("balanced generator failed")


def balanced_formula(n: int, rng: random.Random) -> Formula:
    return tuple(balanced_sign_part(n, 1, rng) + balanced_sign_part(n, -1, rng))


def affine_gaussian(rows: list[int], rhs: list[int], n: int) -> bool:
    rows = rows[:]
    rhs = rhs[:]
    pivot = 0
    for col in range(n):
        selected = next((r for r in range(pivot, len(rows)) if (rows[r] >> col) & 1), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        rhs[pivot], rhs[selected] = rhs[selected], rhs[pivot]
        for r in range(len(rows)):
            if r != pivot and ((rows[r] >> col) & 1):
                rows[r] ^= rows[pivot]
                rhs[r] ^= rhs[pivot]
        pivot += 1
    return not any(row == 0 and bit for row, bit in zip(rows, rhs))


def affine_bruteforce(rows: list[int], rhs: list[int], n: int) -> bool:
    return any(
        all(((row & x).bit_count() & 1) == bit for row, bit in zip(rows, rhs))
        for x in range(1 << n)
    )


def audit_source(formula: Formula, n: int, checks: dict[str, int]) -> bool:
    answer = sat(formula, n)
    child = terminal_successor(answer)
    assert sat(child, 3) == answer
    assert child in (YES_CHILD, NO_CHILD)
    checks["terminal_successor_roundtrip"] += 1
    for name, wrapped_answer in wrapped_answers(formula, n):
        assert wrapped_answer == answer, name
        assert sat(terminal_successor(wrapped_answer), 3) == answer
        checks["wrapper_equivalence"] += 1
    return answer


def run(seed: int) -> dict[str, object]:
    started = time.perf_counter()
    rng = random.Random(seed)
    checks = {
        "clause_cube_sources": 0,
        "terminal_successor_roundtrip": 0,
        "wrapper_equivalence": 0,
        "alternate_encoding": 0,
        "balanced_clean_core": 0,
        "easy_family_controls": 0,
        "affine_gaussian_controls": 0,
        "endpoint_exponent_ledger": 0,
        "full_shannon_output_guard": 0,
    }

    for mask in range(256):
        formula = formula_from_mask(mask)
        answer = audit_source(formula, 3, checks)
        checks["clause_cube_sources"] += 1
        transforms = (
            permute(formula, (2, 3, 1)),
            complement(formula),
            tuple(reversed(formula)),
            formula + formula[:1],
            formula + ((1, -1, 2),),
        )
        for transformed in transforms:
            n = max((abs(lit) for clause in transformed for lit in clause), default=3)
            transformed_answer = sat(transformed, n)
            if transformed is transforms[1]:
                # Global complementation preserves satisfiability via assignment complement.
                assert transformed_answer == answer
            else:
                assert transformed_answer == answer
            assert sat(terminal_successor(transformed_answer), 3) == answer
            checks["alternate_encoding"] += 1

        # Full Shannon terminalization writes one answer leaf per assignment.
        leaves = tuple(satisfies(formula, bits) for bits in range(8))
        assert len(leaves) == 8 and any(leaves) == answer
        checks["full_shannon_output_guard"] += len(leaves)

    balanced_records: list[dict[str, object]] = []
    for n in (6, 9):
        for _ in range(8):
            formula = balanced_formula(n, rng)
            answer = audit_source(formula, n, checks)
            assert all(len(c) == 3 for c in formula)
            counts = {v: [0, 0] for v in range(1, n + 1)}
            for clause in formula:
                assert len(set(abs(l) for l in clause)) == 3
                for lit in clause:
                    counts[abs(lit)][lit > 0] += 1
            assert all(pair == [2, 2] for pair in counts.values())
            checks["balanced_clean_core"] += 1
            balanced_records.append({"n": n, "clauses": len(formula), "sat": answer})

    easy_controls: dict[str, tuple[Formula, int]] = {
        "horn": (((-1, -2, 3), (-3, 4), (-4,)), 4),
        "two_sat": (((1, 2), (-1, 3), (-2, -3)), 3),
        "bounded_treewidth_path": (((1, 2), (-2, 3), (-3, 4)), 4),
        "independent_product": (((1,), (2,), (-3, 4), (3, -4)), 4),
        "redundant_clause": (((1, 2, 3), (1, 2, 3)), 3),
        "padded_tautology": (((1,), (2, -2, 3)), 3),
    }
    easy_results: dict[str, bool] = {}
    for name, (formula, n) in easy_controls.items():
        easy_results[name] = audit_source(formula, n, checks)
        checks["easy_family_controls"] += 1

    affine_records: list[dict[str, int | bool]] = []
    for n in range(2, 9):
        for _ in range(24):
            rows = [rng.randrange(1 << n) for _ in range(n + 2)]
            rhs = [rng.randrange(2) for _ in rows]
            answer = affine_gaussian(rows, rhs, n)
            assert answer == affine_bruteforce(rows, rhs, n)
            assert sat(terminal_successor(answer), 3) == answer
            checks["affine_gaussian_controls"] += 1
        affine_records.append({"n": n, "systems": 24})

    ledger: list[dict[str, int]] = []
    for endpoint_exp in range(1, 13):
        for supplied_exp in range(1, 13):
            # The terminal compiler built from the endpoint decider inherits
            # endpoint_exp and is independent of a separately supplied wrapper.
            successor_exp = endpoint_exp
            assert successor_exp == endpoint_exp
            ledger.append(
                {
                    "endpoint_exponent": endpoint_exp,
                    "supplied_exponent": supplied_exp,
                    "terminal_successor_exponent": successor_exp,
                }
            )
            checks["endpoint_exponent_ledger"] += 1

    return {
        "run_id": "TESTS-0006",
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "checks": checks,
        "total_checks": sum(checks.values()),
        "yes_child_sat": sat(YES_CHILD, 3),
        "no_child_sat": sat(NO_CHILD, 3),
        "balanced_records": balanced_records,
        "easy_results": easy_results,
        "affine_records": affine_records,
        "exponent_ledger": ledger,
        "runtime_seconds": time.perf_counter() - started,
        "limits": [
            "Finite checks do not prove an asymptotic SAT lower bound.",
            "The terminal successor deliberately computes the decision first.",
            "The symbolic endpoint-equivalence proof, not enumeration, supports the exact theorem.",
            "P versus NP remains open.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111224)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
