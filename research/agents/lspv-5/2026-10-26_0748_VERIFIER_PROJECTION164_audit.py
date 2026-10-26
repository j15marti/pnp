#!/usr/bin/env python3
"""Independent audit for LSPV-5 VERIFIER-PROJECTION164.

The script checks, on every subset of the eight proper clauses over three
variables and every assignment, both quantified identities used in the
report.  It also recomputes Role-2's published verifier-gate formula and the
size of the direct witness-enumeration projection.  The latter is an upper
bound construction, never a circuit lower bound.
"""

from __future__ import annotations

import hashlib
import json
import math


def clause_value(signs: tuple[int, int, int], assignment: int) -> bool:
    for i, positive in enumerate(signs):
        bit = (assignment >> i) & 1
        if bit == positive:
            return True
    return False


CLAUSES = tuple(
    tuple((mask >> i) & 1 for i in range(3)) for mask in range(8)
)


def verifier(formula_mask: int, assignment: int) -> bool:
    return all(
        clause_value(CLAUSES[j], assignment)
        for j in range(8)
        if (formula_mask >> j) & 1
    )


def first_conflict(formula_mask: int, assignment: int) -> int:
    """One-based source-clause index, or zero when no clause is false."""
    for j in range(8):
        if (formula_mask >> j) & 1 and not clause_value(CLAUSES[j], assignment):
            return j + 1
    return 0


def valid_conflict(formula_mask: int, assignment: int, index: int) -> bool:
    if index <= 0:
        return False
    j = index - 1
    return bool((formula_mask >> j) & 1) and not clause_value(
        CLAUSES[j], assignment
    )


def role2_gate_count(q: int, m: int) -> tuple[int, int, int, int, int]:
    """Equation (1) from CIRCUIT-OBLIVIOUS-INVERSE-SORT166."""
    w = math.ceil(math.log2(q + 1))
    k = 1 << math.ceil(math.log2(q + 3 * m))
    h = int(math.log2(k))
    c_k = k * h * (h + 1) // 4
    g = (
        c_k * (13 * w + 38)
        + 19 * k
        + (k - 1) * (4 * w - 1)
        + m * (36 * w + 16)
        - 1
    )
    b = m * (1 + 3 * (w + 1))
    return w, k, h, b, g


def main() -> None:
    assertions = 0
    sat_count = 0
    unsat_count = 0
    model_histogram: dict[int, int] = {}

    for formula_mask in range(1 << 8):
        models = [a for a in range(8) if verifier(formula_mask, a)]
        projected_sat = any(verifier(formula_mask, a) for a in range(8))
        universal_conflict = all(
            valid_conflict(
                formula_mask, a, first_conflict(formula_mask, a)
            )
            for a in range(8)
        )
        assert projected_sat == bool(models)
        assertions += 1
        assert universal_conflict == (not bool(models))
        assertions += 1

        for a in range(8):
            j = first_conflict(formula_mask, a)
            local = valid_conflict(formula_mask, a, j)
            assert local == (not verifier(formula_mask, a))
            assertions += 1
            assert (j == 0) == verifier(formula_mask, a)
            assertions += 1

        if models:
            sat_count += 1
        else:
            unsat_count += 1
        model_histogram[len(models)] = model_histogram.get(len(models), 0) + 1

    # All eight sign clauses are UNSAT: each assignment falsifies exactly one.
    full = (1 << 8) - 1
    assert not any(verifier(full, a) for a in range(8))
    assertions += 1
    for a in range(8):
        false_count = sum(
            not clause_value(CLAUSES[j], a) for j in range(8)
        )
        assert false_count == 1
        assertions += 1

    role2_rows = []
    for q, m in [(3, 1), (3, 8), (16, 64), (64, 256), (1024, 1024)]:
        w, k, h, b, g = role2_gate_count(q, m)
        direct_projection_gates = (1 << q) * g + (1 << q) - 1
        assert direct_projection_gates >= g
        assertions += 1
        role2_rows.append(
            {
                "q": q,
                "m": m,
                "w": w,
                "K": k,
                "h": h,
                "B": b,
                "verifier_gates_G": g,
                "direct_projection_log2_gates": math.log2(direct_projection_gates),
                "direct_projection_exact_gates": (
                    direct_projection_gates if q <= 16 else None
                ),
            }
        )

    # Published anchors from Roles 2/4.
    assert role2_gate_count(3, 1)[4] == 1824
    assertions += 1
    assert role2_gate_count(3, 8)[4] == 16888
    assertions += 1

    payload = {
        "run_id": "VERIFIER-PROJECTION164",
        "status": {
            "quantified_relational_identities": "PROVED/EXACT",
            "finite_audit": "COMPUTATIONAL",
            "verifier_to_decision_compression": "OPEN",
            "p_vs_np": "OPEN",
        },
        "scope": {
            "formula_family": "all 256 subsets of the 8 proper signed clauses on variables 1,2,3",
            "assignments_per_formula": 8,
            "randomness": "none",
            "projection_gate_counts_are": "explicit upper bounds, not lower bounds",
        },
        "counts": {
            "formulas": 256,
            "sat_formulas": sat_count,
            "unsat_formulas": unsat_count,
            "assertions": assertions,
            "failures": 0,
            "model_histogram": dict(sorted(model_histogram.items())),
        },
        "role2_gate_rows": role2_rows,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
