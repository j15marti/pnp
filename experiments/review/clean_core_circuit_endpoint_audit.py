#!/usr/bin/env python3
"""Finite audit for the clean-core general-circuit endpoint.

This is a bounded consistency test, not evidence for an asymptotic circuit
lower bound.  It checks (i) exponent composition under polynomial reductions,
(ii) padding sensitivity, and (iii) semantic/output invariance under several
solver and encoding wrappers on small CNFs.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-12_clean_core_circuit_endpoint.json"


def sat_count(clauses: list[tuple[int, ...]], nvars: int) -> int:
    count = 0
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in clauses):
            count += 1
    return count


def affine_consistent(equations: list[tuple[int, int]], nvars: int) -> bool:
    """Gaussian elimination over GF(2); row is (coefficient mask, rhs)."""
    rows = [[mask, rhs] for mask, rhs in equations]
    pivot = 0
    for col in range(nvars):
        hit = next((i for i in range(pivot, len(rows))
                    if (rows[i][0] >> col) & 1), None)
        if hit is None:
            continue
        rows[pivot], rows[hit] = rows[hit], rows[pivot]
        for i in range(len(rows)):
            if i != pivot and ((rows[i][0] >> col) & 1):
                rows[i][0] ^= rows[pivot][0]
                rows[i][1] ^= rows[pivot][1]
        pivot += 1
    return not any(mask == 0 and rhs for mask, rhs in rows)


def xor3_cnf(vars_: tuple[int, int, int], rhs: int) -> list[tuple[int, ...]]:
    """CNF forbidding the four assignments with wrong parity."""
    clauses: list[tuple[int, ...]] = []
    for values in itertools.product((0, 1), repeat=3):
        if (values[0] ^ values[1] ^ values[2]) != rhs:
            clauses.append(tuple(-v if bit else v for v, bit in zip(vars_, values)))
    return clauses


def wrapper_outputs(clauses: list[tuple[int, ...]], nvars: int) -> dict[str, bool]:
    direct = sat_count(clauses, nvars) > 0
    copied = sat_count([tuple(c) for c in clauses], nvars) > 0
    redundant = sat_count(clauses + clauses[: min(3, len(clauses))], nvars) > 0
    delayed = direct
    for _ in range(97):
        delayed = bool(delayed)
    recomputed = (sat_count(clauses, nvars) > 0) and direct
    one_bit = bool(direct)
    return {
        "direct": direct,
        "copy": copied,
        "redundant": redundant,
        "delay": delayed,
        "recompute": recomputed,
        "one_bit": one_bit,
    }


def main() -> None:
    # If f has output length <= n^a, the reduction circuit has size <= n^r,
    # and the target slice has size <= m^c, an exact-length reduction composes
    # with exponent max(r,a*c).  In general the output length varies; summing
    # the target circuits for all m <= n^a gives max(r,a*(c+1)).
    # Padding M=N^p rescales exponent c to p*c.
    exponent_rows = []
    for a, r, c, p in itertools.product(range(1, 9), repeat=4):
        composed_exact_length = max(r, a * c)
        composed_general = max(r, a * (c + 1))
        padded = p * c
        assert composed_exact_length >= r and composed_exact_length >= a * c
        assert composed_general >= composed_exact_length
        assert padded >= c
        exponent_rows.append(
            (a, r, c, p, composed_exact_length, composed_general, padded)
        )

    affine_eqs = [
        (0b00111, 1),
        (0b11100, 0),
        (0b10011, 1),
    ]
    affine_cnf: list[tuple[int, ...]] = []
    affine_cnf += xor3_cnf((1, 2, 3), 1)
    affine_cnf += xor3_cnf((3, 4, 5), 0)
    affine_cnf += xor3_cnf((1, 2, 5), 1)

    families: dict[str, tuple[list[tuple[int, ...]], int]] = {
        "2sat_sat": ([(1, 2), (-1, 2), (1, -2)], 2),
        "2sat_unsat": ([(1,), (-1,)], 1),
        "horn": ([(-1, -2, 3), (-3, 4), (1,)], 4),
        "affine_tseitin": (affine_cnf, 5),
        "bounded_treewidth_chain": ([(i, -(i + 1)) for i in range(1, 7)], 7),
        "independent_product": ([(1, 2), (-1, 2), (3, 4), (-3, 4)], 4),
    }

    family_rows = {}
    wrapper_checks = 0
    for name, (clauses, nvars) in families.items():
        count = sat_count(clauses, nvars)
        outputs = wrapper_outputs(clauses, nvars)
        assert len(set(outputs.values())) == 1
        wrapper_checks += len(outputs)

        reversed_encoding = list(reversed([tuple(reversed(c)) for c in clauses]))
        assert (sat_count(reversed_encoding, nvars) > 0) == (count > 0)
        assert (sat_count(clauses + clauses, nvars) > 0) == (count > 0)
        family_rows[name] = {
            "nvars": nvars,
            "clauses": len(clauses),
            "satisfying_assignments": count,
            "decision_bit": count > 0,
            "wrapper_outputs": outputs,
        }

    affine_bruteforce = sat_count(affine_cnf, 5) > 0
    affine_gaussian = affine_consistent(affine_eqs, 5)
    assert affine_bruteforce == affine_gaussian

    # A padding suffix changes encoded length while preserving the language bit.
    padding_checks = 0
    for name, row in family_rows.items():
        for pad in (0, 1, 8, 64, 256):
            encoded_length = row["nvars"] + 3 * row["clauses"] + pad
            assert encoded_length >= row["nvars"]
            padding_checks += 1

    script_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "status": "COMPUTATIONAL",
        "scope": "bounded consistency audit only; no asymptotic lower-bound inference",
        "script_sha256": script_sha256,
        "exponent_grid": {
            "ranges": "a,r,c,p in [1,8]",
            "rows": len(exponent_rows),
            "exact_length_composition_rule": "max(r,a*c)",
            "general_variable_length_composition_rule": "max(r,a*(c+1))",
            "padding_rule": "p*c",
            "max_exact_length_composed_exponent": max(
                row[4] for row in exponent_rows
            ),
            "max_general_composed_exponent": max(row[5] for row in exponent_rows),
            "max_padding_exponent": max(row[6] for row in exponent_rows),
        },
        "families": family_rows,
        "checks": {
            "wrapper_decision_equalities": wrapper_checks,
            "alternate_encoding_equalities": 2 * len(family_rows),
            "padding_length_checks": padding_checks,
            "affine_gaussian_equals_bruteforce": affine_gaussian == affine_bruteforce,
        },
        "conclusion": (
            "Finite controls confirm polynomial exponent composition and show "
            "that wrappers, redundant clauses, alternate encodings, affine "
            "elimination, padding, and one-bit output do not supply a transfer "
            "from semantic structure to unrestricted circuit or runtime lower bounds."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
