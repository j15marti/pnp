#!/usr/bin/env python3
"""Finite controls for the Rankbridge private-witness quantifier firewall.

The mathematical lower bound is counting, not empirical: one fixed shared
seed is compatible with all 2^q forced private projections b, so advice that
selects every projection must have at least q bits.  This script checks the
3-CNF forcing gadget, small global instances, the counting inequality, and
the k=241 threshold comparison used in the accompanying synthesis.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def lit_value(lit: int, assignment: int) -> bool:
    var = abs(lit) - 1
    value = bool((assignment >> var) & 1)
    return value if lit > 0 else not value


def clause_value(clause: tuple[int, int, int], assignment: int) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


def force_bit_gadget(y: int, u: int, v: int, bit: int) -> list[tuple[int, int, int]]:
    """Four proper 3-clauses force y=bit; u,v remain auxiliary."""
    ylit = y if bit else -y
    return [
        (ylit, u, v),
        (ylit, u, -v),
        (ylit, -u, v),
        (ylit, -u, -v),
    ]


def formula_for_vector(bits: tuple[int, ...]) -> list[tuple[int, int, int]]:
    clauses: list[tuple[int, int, int]] = []
    for j, bit in enumerate(bits):
        y, u, v = 3 * j + 1, 3 * j + 2, 3 * j + 3
        clauses.extend(force_bit_gadget(y, u, v, bit))
    return clauses


def projected_y(assignment: int, q: int) -> tuple[int, ...]:
    return tuple((assignment >> (3 * j)) & 1 for j in range(q))


def serialized_source_bits(q: int) -> int:
    """Conservative canonical literal serialization length for 4q clauses."""
    label_bits = max(1, math.ceil(math.log2(3 * q + 1)))
    return 4 * q * 3 * (label_bits + 1) + 2 * label_bits + 16


def target_threshold(q: int, k: int = 241) -> tuple[int, int, float]:
    nbits = serialized_source_bits(q)
    # M=N^(6/5) at exponent level, so log2 M=(6/5)log2 N.
    log2_m = 1.2 * math.log2(nbits)
    index_floor = math.ceil(log2_m)
    power_term = math.ceil(2 ** (log2_m / k))
    return nbits, max(index_floor, power_term), log2_m


def main() -> None:
    assertions = 0
    failures: list[str] = []

    # Local gadget truth table: satisfiable iff the designated y has the
    # forced value, independently of auxiliary u,v.
    for bit in (0, 1):
        clauses = force_bit_gadget(1, 2, 3, bit)
        for assignment in range(8):
            got = all(clause_value(c, assignment) for c in clauses)
            expected = ((assignment & 1) == bit)
            assertions += 1
            if got != expected:
                failures.append(f"gadget bit={bit} assignment={assignment}")

    # Exhaustive global controls through q=4.
    global_instances = 0
    assignments_checked = 0
    for q in range(1, 5):
        for code in range(1 << q):
            bits = tuple((code >> j) & 1 for j in range(q))
            clauses = formula_for_vector(bits)
            projections = set()
            for assignment in range(1 << (3 * q)):
                assignments_checked += 1
                if all(clause_value(c, assignment) for c in clauses):
                    projections.add(projected_y(assignment, q))
            assertions += 1
            global_instances += 1
            if projections != {bits}:
                failures.append(f"projection q={q} code={code}: {projections}")

    # The same seed admits all 2^q vectors; fewer than q advice bits cannot
    # name them all.  These checks instantiate the exact counting inequality.
    counting_cases = 0
    for q in range(1, 25):
        distinct_vectors = 1 << q
        assertions += 1
        counting_cases += 1
        if distinct_vectors != len({code for code in range(1 << q)}):
            failures.append(f"distinct-vector count q={q}")
        for advice_bits in range(q):
            assertions += 1
            counting_cases += 1
            if not ((1 << advice_bits) < distinct_vectors):
                failures.append(f"capacity q={q} a={advice_bits}")

    # Threshold comparison for representative cofinal sizes.  This does not
    # prove a KT lower bound; it verifies that the q-bit selection burden is
    # far above the intended k=241 budget for this serialization.
    threshold_rows = []
    for exponent in range(4, 25):
        q = 1 << exponent
        nbits, p241, log2_m = target_threshold(q)
        assertions += 1
        if not q > p241:
            failures.append(f"threshold q={q} N={nbits} p={p241}")
        threshold_rows.append(
            {
                "q": q,
                "source_bits_N": nbits,
                "log2_target_M": log2_m,
                "p_241": p241,
                "q_over_p": q / p241,
            }
        )

    result = {
        "run": "RANKBRIDGE-PRIVATE-WITNESS44",
        "status": "PASS" if not failures else "FAIL",
        "theorem_checked": (
            "one common seed with 2^q forced private projections requires "
            "at least q bits of selecting advice"
        ),
        "gadget_rows": 16,
        "global_instances": global_instances,
        "assignments_checked": assignments_checked,
        "counting_cases": counting_cases,
        "threshold_rows": threshold_rows,
        "assertions": assertions,
        "failures": failures,
        "scope_warning": (
            "finite controls plus exact counting identity; not a KT lower "
            "bound, language separation, or unrestricted ARC obstruction"
        ),
        "global_status": "P versus NP OPEN; P versus RP OPEN",
    }
    Path("RANKBRIDGE_PRIVATE_WITNESS44_raw.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
