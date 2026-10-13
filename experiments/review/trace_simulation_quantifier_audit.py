#!/usr/bin/env python3
"""Finite audit for the quantifiers in a trace-to-Resolution transfer claim.

This script deliberately separates three objects:
  * a one-bit deterministic decision trace;
  * Resolution closure depth on the same tiny CNF;
  * the logical quantifiers in a proposed universal simulation statement.

The bounded data are controls only.  They are not used to extrapolate an
asymptotic lower bound.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import deque


Clause = frozenset[int]
CNF = tuple[Clause, ...]


def variables(cnf: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in cnf for lit in clause}))


def clause_true(clause: Clause, assignment: int, pos: dict[int, int]) -> bool:
    return any(
        ((assignment >> pos[abs(lit)]) & 1) == (1 if lit > 0 else 0)
        for lit in clause
    )


def exhaustive_trace_rows(cnf: CNF) -> tuple[bool, int]:
    """Return decision bit and number of deterministic assignments inspected."""
    vs = variables(cnf)
    pos = {v: i for i, v in enumerate(vs)}
    for assignment in range(1 << len(vs)):
        if all(clause_true(clause, assignment, pos) for clause in cnf):
            return True, assignment + 1
    return False, 1 << len(vs)


def resolution_closure(cnf: CNF) -> tuple[int | None, int]:
    """Compute least Resolution derivation depth of empty clause on tiny CNFs."""
    depth: dict[Clause, int] = {c: 0 for c in cnf}
    queue: deque[Clause] = deque(depth)
    while queue:
        left = queue.popleft()
        snapshot = list(depth)
        for right in snapshot:
            for pivot in tuple(left):
                if -pivot not in right:
                    continue
                resolvent = (left - {pivot}) | (right - {-pivot})
                if any(-lit in resolvent for lit in resolvent):
                    continue
                candidate = max(depth[left], depth[right]) + 1
                if resolvent not in depth or candidate < depth[resolvent]:
                    depth[resolvent] = candidate
                    queue.append(resolvent)
    return depth.get(frozenset()), len(depth)


def cnf(*clauses: tuple[int, ...]) -> CNF:
    return tuple(frozenset(c) for c in clauses)


def rename(formula: CNF, mapping: dict[int, int]) -> CNF:
    return tuple(
        frozenset((1 if lit > 0 else -1) * mapping[abs(lit)] for lit in clause)
        for clause in formula
    )


def xor3(rhs: int) -> CNF:
    clauses: list[Clause] = []
    for assignment in range(8):
        parity = ((assignment >> 0) ^ (assignment >> 1) ^ (assignment >> 2)) & 1
        if parity != rhs:
            clauses.append(
                frozenset(
                    -(i + 1) if ((assignment >> i) & 1) else (i + 1)
                    for i in range(3)
                )
            )
    return tuple(clauses)


def main() -> None:
    base = cnf((1, 2), (-1, 2), (1, -2), (-1, -2))
    cases: dict[str, CNF] = {
        "2sat_unsat": base,
        "horn_unsat": cnf((1,), (-1, 2), (-2,)),
        "affine_tseitin_cnf_unsat": xor3(0) + xor3(1),
        "bounded_treewidth_unsat": cnf((1,), (-1, 2), (-2, 3), (-3,)),
        "independent_product": base + cnf((3, 4), (-3, 4)),
        "redundant_clause_wrapper": base + (base[0],),
        "tautology_wrapper": base + cnf((1, -1)),
        "padding_wrapper": base + cnf((3, -3), (4, -4)),
        "renaming_wrapper": rename(base, {1: 2, 2: 1}),
        "alternate_representation": tuple(reversed(base)),
    }

    records = []
    for name, formula in cases.items():
        t0 = time.perf_counter_ns()
        answer, trace_rows = exhaustive_trace_rows(formula)
        t1 = time.perf_counter_ns()
        resolution_depth, closure_clauses = resolution_closure(formula)
        t2 = time.perf_counter_ns()
        assert answer is False
        assert resolution_depth is not None
        records.append(
            {
                "case": name,
                "variables": len(variables(formula)),
                "clauses": len(formula),
                "decision_bit": answer,
                "trace_rows": trace_rows,
                "resolution_depth": resolution_depth,
                "resolution_closure_clauses": closure_clauses,
                "decision_ns": t1 - t0,
                "resolution_closure_ns": t2 - t1,
            }
        )

    # This table is a propositional audit of the proposed statement
    # U_poly := for every uniform polynomial-time exact SAT decider A,
    #           Resolution polynomially simulates A's accepting trace system
    #           on an explicit Resolution-hard family H.
    # Under the known lower bound on H, a polynomial decider satisfying the
    # consequent cannot exist.  Thus U_poly is true exactly when PolyDec is empty.
    quantifier_worlds = [
        {
            "world": "P_ne_NP",
            "uniform_polynomial_sat_decider_exists": False,
            "U_poly": True,
            "reason": "vacuous universal quantification",
        },
        {
            "world": "P_eq_NP",
            "uniform_polynomial_sat_decider_exists": True,
            "U_poly": False,
            "reason": "polynomial trace plus simulation contradicts the Resolution lower bound",
        },
    ]
    assert all(
        row["U_poly"] == (not row["uniform_polynomial_sat_decider_exists"])
        for row in quantifier_worlds
    )

    semantic = {
        "records_without_timing": [
            {k: v for k, v in row.items() if not k.endswith("_ns")} for row in records
        ],
        "quantifier_worlds": quantifier_worlds,
        "derived_equivalence": "U_poly iff no uniform polynomial-time exact SAT decider exists",
        "unrestricted_total_decider_variant": "false by a recognizable-family front door with exact fallback",
        "scope": "finite type/quantifier audit only; no asymptotic extrapolation",
    }
    semantic_bytes = json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "experiment": "trace_simulation_quantifier_audit",
        "status": "COMPUTATIONAL",
        "records": records,
        "quantifier_worlds": quantifier_worlds,
        "derived_equivalence": semantic["derived_equivalence"],
        "unrestricted_total_decider_variant": semantic["unrestricted_total_decider_variant"],
        "scope": semantic["scope"],
        "semantic_sha256": hashlib.sha256(semantic_bytes).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
