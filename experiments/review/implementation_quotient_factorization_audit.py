#!/usr/bin/env python3
"""Finite audit for implementation-quotient factorization.

The accompanying report proves the symbolic theorem.  This program checks
small exact SAT sources, implementation wrappers, quotient canonicalization,
and the finite counting identity for implementation-invariant Boolean tables.
It does not infer an asymptotic lower bound.
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


def truth_vector(formula: Formula, n: int) -> tuple[int, ...]:
    return tuple(int(satisfies(formula, bits)) for bits in range(1 << n))


def direct(formula: Formula, n: int) -> dict[str, object]:
    bit = int(any(satisfies(formula, x) for x in range(1 << n)))
    return {"tag": "DIRECT", "sat": bit, "payload": None}


def materialize(formula: Formula, n: int) -> dict[str, object]:
    vector = truth_vector(formula, n)
    return {"tag": "MATERIALIZE", "sat": int(any(vector)), "payload": vector}


def interp(formula: Formula, n: int) -> dict[str, object]:
    vector = truth_vector(formula, n)
    transformed = tuple(vector[((1 << n) - 1) ^ x] for x in range(1 << n))
    return {"tag": "INTERP", "sat": int(any(transformed)), "payload": transformed}


def recomp(formula: Formula, n: int) -> dict[str, object]:
    first = int(any(satisfies(formula, x) for x in range(1 << n)))
    second = int(any(satisfies(formula, x) for x in range(1 << n)))
    assert first == second
    return {"tag": "RECOMP", "sat": second, "payload": None}


IMPLEMENTATIONS = (direct, materialize, interp, recomp)


def quotient(rep: dict[str, object]) -> int:
    return int(rep["sat"])


def wrapped_representatives(rep: dict[str, object]) -> tuple[dict[str, object], ...]:
    return (
        {**rep, "tag": f"DEAD({rep['tag']})", "dead": (0, 1, 1, 0)},
        {**rep, "tag": f"COPY({rep['tag']})", "copy": (rep["sat"], rep["sat"])},
        {**rep, "tag": f"DELAY({rep['tag']})", "delay_ticks": 17},
    )


def affine_sat(rows: list[int], rhs: list[int], n: int) -> bool:
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
    return any(all(((row & x).bit_count() & 1) == bit for row, bit in zip(rows, rhs))
               for x in range(1 << n))


def proper_clause_cube() -> tuple[Clause, ...]:
    return tuple(tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(bits))
                 for bits in itertools.product((False, True), repeat=3))


def formula_from_mask(mask: int) -> Formula:
    cube = proper_clause_cube()
    return tuple(cube[i] for i in range(8) if (mask >> i) & 1)


def permute_formula(formula: Formula, permutation: tuple[int, ...]) -> Formula:
    return tuple(tuple((1 if lit > 0 else -1) * permutation[abs(lit) - 1]
                       for lit in clause) for clause in formula)


def complement_formula(formula: Formula) -> Formula:
    return tuple(tuple(-lit for lit in clause) for clause in formula)


def balanced_sign_part(n: int, sign: int, rng: random.Random) -> list[Clause]:
    slots = [v for v in range(1, n + 1) for _ in range(2)]
    for _ in range(20_000):
        rng.shuffle(slots)
        triples = [tuple(sorted(slots[i:i + 3])) for i in range(0, len(slots), 3)]
        if all(len(set(t)) == 3 for t in triples) and len(set(triples)) == len(triples):
            return [tuple(sign * v for v in t) for t in triples]
    raise RuntimeError("balanced generator failed")


def balanced_formula(n: int, rng: random.Random) -> Formula:
    return tuple(balanced_sign_part(n, 1, rng) + balanced_sign_part(n, -1, rng))


def invariant_table_count(implementations: int, sources: int) -> tuple[int, int]:
    cells = implementations * sources
    total = 1 << cells
    invariant = 0
    for table in range(total):
        good = True
        for source in range(sources):
            expected = (table >> source) & 1
            for impl in range(1, implementations):
                if ((table >> (impl * sources + source)) & 1) != expected:
                    good = False
                    break
            if not good:
                break
        invariant += int(good)
    return total, invariant


def run(seed: int) -> dict[str, object]:
    started = time.perf_counter()
    rng = random.Random(seed)
    checks = {
        "clause_cube_semantics": 0,
        "implementation_quotient": 0,
        "raw_representation_separation": 0,
        "encoding_controls": 0,
        "dead_copy_delay_wrappers": 0,
        "balanced_clean_core": 0,
        "affine_gaussian_controls": 0,
        "easy_family_controls": 0,
        "invariant_table_enumeration": 0,
    }

    raw_differences = 0
    for mask in range(256):
        formula = formula_from_mask(mask)
        source_bit = int(any(truth_vector(formula, 3)))
        reps = [impl(formula, 3) for impl in IMPLEMENTATIONS]
        checks["clause_cube_semantics"] += 1
        for rep in reps:
            assert quotient(rep) == source_bit
            checks["implementation_quotient"] += 1
            for wrapped in wrapped_representatives(rep):
                assert quotient(wrapped) == source_bit
                checks["dead_copy_delay_wrappers"] += 1
        raw_keys = {(rep["tag"], repr(rep["payload"])) for rep in reps}
        assert len(raw_keys) > 1
        raw_differences += 1
        checks["raw_representation_separation"] += 1

        transforms = (
            permute_formula(formula, (2, 3, 1)),
            complement_formula(formula),
            formula + formula[:1],
            formula + ((1, -1, 2),),
        )
        for transformed in transforms:
            n = max((abs(lit) for clause in transformed for lit in clause), default=3)
            assert bool(any(truth_vector(transformed, n))) == bool(source_bit)
            checks["encoding_controls"] += 1

    balanced_records: list[dict[str, object]] = []
    for n in (6, 9):
        for _ in range(8):
            formula = balanced_formula(n, rng)
            expected = quotient(direct(formula, n))
            outputs = [quotient(impl(formula, n)) for impl in IMPLEMENTATIONS]
            assert outputs == [expected] * len(IMPLEMENTATIONS)
            checks["balanced_clean_core"] += len(IMPLEMENTATIONS)
            balanced_records.append({"n": n, "clauses": len(formula), "sat": expected})

    easy_controls: dict[str, tuple[Formula, int]] = {
        "horn": (((-1, -2, 3), (-3, 4), (-4,)), 4),
        "two_sat": (((1, 2), (-1, 3), (-2, -3)), 3),
        "bounded_treewidth_path": (((1, 2), (-2, 3), (-3, 4)), 4),
        "independent_product": (((1,), (2,), (-3, 4), (3, -4)), 4),
    }
    easy_results: dict[str, int] = {}
    for name, (formula, n) in easy_controls.items():
        outputs = [quotient(impl(formula, n)) for impl in IMPLEMENTATIONS]
        assert len(set(outputs)) == 1
        easy_results[name] = outputs[0]
        checks["easy_family_controls"] += len(outputs)

    for n in range(2, 9):
        for _ in range(20):
            rows = [rng.randrange(1 << n) for _ in range(n + 2)]
            rhs = [rng.randrange(2) for _ in rows]
            assert affine_sat(rows, rhs, n) == affine_bruteforce(rows, rhs, n)
            checks["affine_gaussian_controls"] += 1

    table_counts: list[dict[str, int]] = []
    for implementations in range(1, 5):
        for sources in range(1, 5):
            total, invariant = invariant_table_count(implementations, sources)
            assert invariant == (1 << sources)
            table_counts.append({
                "implementations": implementations,
                "sources": sources,
                "all_tables": total,
                "invariant_tables": invariant,
            })
            checks["invariant_table_enumeration"] += total

    return {
        "run_id": "LB-0011",
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "checks": checks,
        "total_checks": sum(checks.values()),
        "raw_differences_on_clause_cube": raw_differences,
        "balanced_records": balanced_records,
        "easy_results": easy_results,
        "invariant_table_counts": table_counts,
        "runtime_seconds": time.perf_counter() - started,
        "limits": [
            "Finite checks do not prove an asymptotic SAT lower bound.",
            "The four implementations are hostile controls, not all possible algorithms.",
            "The symbolic factorization theorem, not enumeration, supports the exact claim.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111112)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["script_sha256"] = source_hash
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
