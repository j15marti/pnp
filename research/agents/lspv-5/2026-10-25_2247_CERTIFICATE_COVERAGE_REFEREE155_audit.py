#!/usr/bin/env python3
"""Exact finite audit for CIRCUIT-CERTIFICATE-COVERAGE155.

All checks are deliberately tiny and deterministic.  They validate only the
finite counterexample and rational arithmetic stated in the accompanying
report; they are not asymptotic evidence for P != NP.
"""

from fractions import Fraction
import itertools
import json


def clause_value(clause, assignment):
    return any(assignment[abs(lit)] if lit > 0 else not assignment[abs(lit)]
               for lit in clause)


def cnf_value(cnf, assignment):
    return all(clause_value(clause, assignment) for clause in cnf)


def models(cnf, variables):
    out = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if cnf_value(cnf, a):
            out.append("".join("1" if a[v] else "0" for v in variables))
    return out


def restrict(cnf, variable, value):
    residual = []
    for clause in cnf:
        satisfied = any(abs(lit) == variable and ((lit > 0) == value)
                        for lit in clause)
        if satisfied:
            continue
        reduced = tuple(lit for lit in clause if abs(lit) != variable)
        residual.append(reduced)
    return tuple(residual)


def main():
    # Proper 3-CNF U(x;a,b), exactly equivalent to the unit clause x.
    # Every clause has three distinct variables and all four sign patterns on a,b.
    u = (
        (1, 2, 3),
        (1, 2, -3),
        (1, -2, 3),
        (1, -2, -3),
    )
    parent_models = models(u, (1, 2, 3))
    r0 = restrict(u, 1, False)
    r1 = restrict(u, 1, True)
    r0_models = models(r0, (2, 3))
    r1_models = models(r1, (2, 3))
    assert parent_models == ["100", "101", "110", "111"]
    assert r0_models == []
    assert r1_models == ["00", "01", "10", "11"]

    # Exact van Melkebeek Theorem 1.3 arithmetic at d=901/500.
    d = Fraction(901, 500)
    c_threshold = (2 * d - 1) / (d * (d - 1))
    master_at_diagonal = d * d * (d - 1) - 2 * d + 1
    first_condition_lhs = (d - 1) * d
    assert c_threshold == Fraction(651000, 361301)
    assert master_at_diagonal > 0
    assert first_condition_lhs > 1

    # The weighted leaf-volume inequality, exhaustively checked over a bounded grid.
    checked = 0
    for exponent in range(1, 6):
        for length in range(1, 6):
            for leaves in itertools.product(range(1, 7), repeat=length):
                mmax = max(leaves)
                lhs = sum(m ** exponent for m in leaves)
                rhs = (mmax ** (exponent - 1)) * sum(leaves)
                assert lhs <= rhs
                checked += 1

    # Same-machine transport examples for lambda=1.
    # lazy time exponent = g + lambda*t; eager retains a lambda-size buffer.
    t = Fraction(6, 5)
    s = Fraction(1, 2)
    flmv_t = Fraction(241, 200)
    flmv_s = Fraction(11642479, 23232400)
    transport = {
        "lazy_polylog_accessor": {
            "time": str(t), "space": str(s),
            "strictly_inside": bool(t < flmv_t and s < flmv_s),
        },
        "lazy_linear_accessor": {
            "time": str(1 + t), "space": str(s),
            "strictly_inside": bool(1 + t < flmv_t and s < flmv_s),
        },
        "eager_materialization": {
            "time": str(t), "space": "1",
            "strictly_inside": bool(t < flmv_t and Fraction(1, 1) < flmv_s),
        },
    }
    assert transport["lazy_polylog_accessor"]["strictly_inside"]
    assert not transport["lazy_linear_accessor"]["strictly_inside"]
    assert not transport["eager_materialization"]["strictly_inside"]

    result = {
        "run_id": "CIRCUIT-CERTIFICATE-COVERAGE155",
        "proper_3cnf_counterexample": {
            "clauses": [list(c) for c in u],
            "parent_models": parent_models,
            "branch_x_0_models": r0_models,
            "branch_x_1_models": r1_models,
            "finding": "An UNSAT proof for only branch x=0 does not prove the SAT parent UNSAT.",
        },
        "master_theorem_exact": {
            "d": str(d),
            "strict_c_threshold": str(c_threshold),
            "strict_c_threshold_decimal": float(c_threshold),
            "diagonal_second_expression": str(master_at_diagonal),
            "diagonal_second_expression_decimal": float(master_at_diagonal),
            "diagonal_first_lhs": str(first_condition_lhs),
            "diagonal_first_lhs_decimal": float(first_condition_lhs),
        },
        "weighted_volume_checks": checked,
        "transport": transport,
        "status": "FINITE AUDIT PASSED; asymptotic coverage and bit-local compiler remain OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
