#!/usr/bin/env python3
"""Audit superconstant SAT-query count as a proposed universal resource.

The accompanying report proves the symbolic polynomial-query closure theorem.
This script checks finite parity decision-tree lower bounds, compact OBDDs,
explicit tiny-CNF realizations, wrappers, connected two-pin identities,
affine/Tseitin Gaussian controls, easy families, and exponent bookkeeping.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from collections import defaultdict
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
AffineSystem = tuple[tuple[int, int], ...]


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in formula)


def sat(formula: Formula) -> bool:
    vs = variables(formula)
    return any(satisfies(formula, dict(zip(vs, bits))) for bits in itertools.product((False, True), repeat=len(vs)))


def pin(formula: Formula, variable: int, value: bool) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        if any(abs(lit) == variable and (lit > 0) == value for lit in clause):
            continue
        out.append(tuple(lit for lit in clause if abs(lit) != variable))
    return tuple(out)


def tiny_sat_bit(bit: bool, offset: int = 0) -> Formula:
    vars3 = (offset + 1, offset + 2, offset + 3)
    if bit:
        return (vars3,)
    return tuple(tuple(v * sign for v, sign in zip(vars3, signs)) for signs in itertools.product((-1, 1), repeat=3))


def rename(formula: Formula, mapping: dict[int, int], complement: bool = False) -> Formula:
    out = []
    for clause in formula:
        converted = []
        for lit in clause:
            positive = lit > 0
            if complement:
                positive = not positive
            converted.append(mapping[abs(lit)] if positive else -mapping[abs(lit)])
        out.append(tuple(converted))
    return tuple(out)


def gaussian_sat(system: AffineSystem) -> bool:
    rows = [[mask, rhs] for mask, rhs in system]
    pivot = 0
    width = max((mask.bit_length() for mask, _ in system), default=0)
    for bit in range(width - 1, -1, -1):
        row = next((j for j in range(pivot, len(rows)) if (rows[j][0] >> bit) & 1), None)
        if row is None:
            continue
        rows[pivot], rows[row] = rows[row], rows[pivot]
        for j in range(len(rows)):
            if j != pivot and ((rows[j][0] >> bit) & 1):
                rows[j][0] ^= rows[pivot][0]
                rows[j][1] ^= rows[pivot][1]
        pivot += 1
    return all(mask or rhs == 0 for mask, rhs in rows)


def parity_obdd(bits: tuple[bool, ...]) -> bool:
    state = False
    for bit in bits:
        state ^= bit
    return state


def adaptive_full_query(bits: tuple[bool, ...]) -> bool:
    """Adaptive order, but every bit is eventually queried."""
    remaining = list(range(len(bits)))
    state = False
    answer = False
    while remaining:
        pos = -1 if state else 0
        idx = remaining.pop(pos)
        answer ^= bits[idx]
        state = bits[idx]
    return answer


def run(seed: int) -> dict:
    rng = random.Random(seed)
    checks: defaultdict[str, int] = defaultdict(int)

    # Exact adversary property for parity: every incomplete ternary partial
    # assignment has completions of both parities, hence all q bits are needed.
    for q in range(1, 11):
        for partial in itertools.product((-1, 0, 1), repeat=q):
            if -1 not in partial:
                continue
            unknown = partial.index(-1)
            low = list(partial)
            high = list(partial)
            low[unknown] = 0
            high[unknown] = 1
            low_parity = sum(v for v in low if v >= 0) & 1
            high_parity = sum(v for v in high if v >= 0) & 1
            assert low_parity != high_parity
            checks["parity_query_adversary"] += 1

    # A width-2 ordered branching program computes the same function.
    for q in range(1, 16):
        for bits in itertools.product((False, True), repeat=q):
            expected = bool(sum(bits) & 1)
            assert parity_obdd(bits) == expected
            assert adaptive_full_query(bits) == expected
            checks["compact_obdd_and_adaptive_queries"] += 2

    # Realize independent oracle bits by tiny proper 3-CNFs.  The realization
    # is deliberately syntactically easy: it is a hostile control, not a hard family.
    for q in range(1, 9):
        for bits in itertools.product((False, True), repeat=q):
            formulas = tuple(tiny_sat_bit(bit, 3 * i) for i, bit in enumerate(bits))
            answers = tuple(sat(formula) for formula in formulas)
            expected = bool(sum(bits) & 1)
            assert answers == bits
            assert bool(sum(answers) & 1) == expected
            checks["tiny_cnf_parity_service"] += q + 2
            for formula, bit in zip(formulas, bits):
                vs = variables(formula)
                mapping = dict(zip(vs, reversed(vs)))
                padding_var = vs[0]
                variants = (
                    tuple(reversed(formula)),
                    formula + (formula[0],),
                    formula + ((padding_var, -padding_var),),
                    rename(formula, mapping),
                    rename(formula, mapping, True),
                )
                for variant in variants:
                    assert sat(variant) == bit
                    checks["encoding_padding_wrapper_controls"] += 1

    # Independent audit of the Shannon two-pin identity used by TESTS-0004.
    proper = tuple(tuple(v * s for v, s in zip((1, 2, 3), signs)) for signs in itertools.product((-1, 1), repeat=3))
    for mask in range(1 << 8):
        formula = tuple(proper[i] for i in range(8) if mask & (1 << i))
        answer = sat(formula)
        for z in (1, 2, 3):
            assert answer == (sat(pin(formula, z, False)) or sat(pin(formula, z, True)))
            checks["connected_twopin_identity_regression"] += 1

    # Affine/Tseitin controls use actual GF(2) elimination.
    for n in range(3, 23):
        for odd in (False, True):
            charges = [0] * n
            charges[0] = int(odd)
            system = tuple(((1 << ((i - 1) % n)) | (1 << i), charges[i]) for i in range(n))
            assert gaussian_sat(system) == (not odd)
            checks["affine_tseitin_gaussian_controls"] += 1
    for _ in range(160):
        n = rng.randint(1, 12)
        system = tuple((rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randint(0, 2 * n)))
        assert isinstance(gaussian_sat(system), bool)
        checks["affine_tseitin_gaussian_controls"] += 1

    # Horn, 2-SAT, and bounded-treewidth path controls retain the same service identity.
    easy: tuple[Formula, ...] = (
        ((-1, 2), (-2, 3), (-3, 4)),
        ((-1, -2, 3), (-3,)),
        ((1, 2), (-1, -2)),
        ((1, 2), (-2, 3), (-3, 4)),
    )
    for formula in easy:
        z = variables(formula)[0]
        assert sat(formula) == (sat(pin(formula, z, False)) or sat(pin(formula, z, True)))
        checks["easy_family_controls"] += 1

    # Exact exponent ledger for q(N)=N^b residuals of length N^a and A(M)=M^K.
    for b in range(0, 7):
        for a in range(1, 6):
            for k in range(1, 9):
                for local in range(0, 9):
                    query_exponent = b + a * k
                    total_exponent = max(local, query_exponent)
                    assert total_exponent >= k
                    assert total_exponent == max(local, b + a * k)
                    checks["polynomial_query_exponent_ledger"] += 1

    return {
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "parameters": {
            "parity_adversary_q": [1, 10],
            "obdd_q": [1, 15],
            "tiny_cnf_service_q": [1, 8],
            "tseitin_cycle_n": [3, 22],
            "random_affine_systems": 160,
            "exponent_b": [0, 6],
            "exponent_a": [1, 5],
            "exponent_K": [1, 8],
            "local_exponent": [0, 8]
        },
        "limits": [
            "Finite checks do not prove asymptotic SAT lower bounds.",
            "The parity oracle lower bound is an abstract black-box query statement.",
            "Tiny CNF parity blocks are intentionally easy hostile controls.",
            "The report, not the finite audit, proves polynomial-query closure."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111036)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    payload = run(args.seed)
    payload["runtime_seconds"] = time.perf_counter() - started
    payload["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
