#!/usr/bin/env python3
"""Exact finite audit for INTERFACE-SIGN-COLLISION165.

The declared residual signature records (i) the multiset of unordered
variable-pair supports and (ii) each variable's positive/negative occurrence
counts.  It deliberately forgets how signs are correlated inside a clause.
"""

from __future__ import annotations

import hashlib
import itertools
import json


Literal = tuple[int, int]  # (zero-based variable, satisfying bit)
Clause = tuple[Literal, Literal]
Formula = tuple[Clause, ...]


def clauses_on(n: int) -> list[Clause]:
    return [
        ((i, si), (j, sj))
        for i, j in itertools.combinations(range(n), 2)
        for si, sj in itertools.product((0, 1), repeat=2)
    ]


def signature(formula: Formula, n: int) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    signed_degrees = tuple(
        sum(1 for clause in formula for var, sign in clause if var == i and sign == b)
        for i in range(n)
        for b in (0, 1)
    )
    pair_supports = tuple(sorted(tuple(sorted(var for var, _ in clause)) for clause in formula))
    return signed_degrees, pair_supports


def models(formula: Formula, n: int) -> list[tuple[int, ...]]:
    return [
        assignment
        for assignment in itertools.product((0, 1), repeat=n)
        if all(any(assignment[var] == sign for var, sign in clause) for clause in formula)
    ]


def lit(var: int, positive: bool) -> Literal:
    return var, int(positive)


# A is UNSAT: its first pair forces not x and its second pair forces x.
A: Formula = (
    (lit(0, False), lit(1, False)),
    (lit(0, False), lit(1, True)),
    (lit(0, True), lit(2, False)),
    (lit(0, True), lit(2, True)),
)

# B is SAT: y = not x and z = not x.
B: Formula = (
    (lit(0, False), lit(1, False)),
    (lit(0, True), lit(1, True)),
    (lit(0, False), lit(2, False)),
    (lit(0, True), lit(2, True)),
)


def parent_models() -> list[tuple[int, int, int, int]]:
    """Models of P=(s or A_i)_i and (not s or B_i)_i.

    Assignment order is (s,x,y,z).  Literals in A/B use x,y,z indices 0..2.
    """
    out: list[tuple[int, int, int, int]] = []
    for s, x, y, z in itertools.product((0, 1), repeat=4):
        xyz = (x, y, z)
        a_ok = all(s == 1 or any(xyz[var] == sign for var, sign in clause) for clause in A)
        b_ok = all(s == 0 or any(xyz[var] == sign for var, sign in clause) for clause in B)
        if a_ok and b_ok:
            out.append((s, x, y, z))
    return out


def main() -> None:
    assertions = 0
    assert signature(A, 3) == signature(B, 3)
    assertions += 1
    assert not models(A, 3)
    assertions += 1
    assert models(B, 3) == [(0, 1, 1), (1, 0, 0)]
    assertions += 1
    assert parent_models() == [(1, 0, 1, 1), (1, 1, 0, 0)]
    assertions += 1

    census: list[dict[str, int]] = []
    first_mixed = None
    for n in (2, 3):
        universe = clauses_on(n)
        for m in range(1, min(4, len(universe)) + 1):
            buckets: dict[object, set[bool]] = {}
            formulas = 0
            for formula in itertools.combinations(universe, m):
                formulas += 1
                sat = bool(models(formula, n))
                assertions += 1
                buckets.setdefault(signature(formula, n), set()).add(sat)
            mixed = sum(1 for labels in buckets.values() if len(labels) == 2)
            if mixed and first_mixed is None:
                first_mixed = (n, m)
            census.append(
                {
                    "variables": n,
                    "clauses": m,
                    "formulas": formulas,
                    "signature_buckets": len(buckets),
                    "mixed_sat_unsat_buckets": mixed,
                }
            )

    assert first_mixed == (3, 4)
    assertions += 1

    # Randomized fingerprints are an escape only with error: one parity bit
    # collides on unequal strings.  This control prevents an exact checker from
    # silently importing bounded-error equality.
    parity_collisions = 0
    for u in itertools.product((0, 1), repeat=4):
        for v in itertools.product((0, 1), repeat=4):
            if u != v and (sum(u) & 1) == (sum(v) & 1):
                parity_collisions += 1
            assertions += 1
    assert parity_collisions == 112
    assertions += 1

    payload = {
        "run_id": "INTERFACE-SIGN-COLLISION165",
        "status": "COMPUTATIONAL finite audit supporting a PROVED/EXACT symbolic counterexample",
        "scope": "sign-blind pair-support plus signed-degree residual interfaces only; not arbitrary SAT",
        "formula_A_models": models(A, 3),
        "formula_B_models": models(B, 3),
        "shared_signature": signature(A, 3),
        "proper_ternary_parent_models_s_x_y_z": parent_models(),
        "first_mixed_bucket_in_exhaustive_n_le_3_m_le_4_census": first_mixed,
        "census": census,
        "four_bit_parity_fingerprint_unequal_collisions": parity_collisions,
        "assertion_groups": assertions,
        "failed": 0,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["normalized_payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
