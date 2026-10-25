#!/usr/bin/env python3
"""Exact weighted-cover proof audit for uniform-sign r=3 M22 port blocks."""

from fractions import Fraction
from math import comb
import json


def C(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def false_count(a, sign, t, h):
    """Assignments with port weight 1 and aux weight h falsifying a fixed clause.

    t is the number of port variables in the proper monotone triple.
    """
    if sign == "P":
        return C(3 - t, 1) * C(a - (3 - t), h)
    return C(3 - t, 1 - t) * C(a - (3 - t), h - (3 - t))


def audit_case(a, aux_weights):
    # aux_weights maps Hamming weight h to a nonnegative integer assignment weight.
    demand = sum(weight * C(3, 1) * C(a, h)
                 for h, weight in aux_weights.items())
    capacity = {
        sign: [sum(weight * false_count(a, sign, t, h)
                   for h, weight in aux_weights.items())
               for t in range(4)]
        for sign in ("P", "N")
    }

    if a == 3:
        # Dominating coefficient per P clause: 2t; per N clause: 3-t.
        dominate_p = [2*t for t in range(4)]
        dominate_n = [3-t for t in range(4)]
        # Signed incidence totals: P ports=3, N auxiliaries=2a.
        degree_cap = 2*3 + 1*(2*a)
    elif a == 6:
        # Dominating coefficient per P clause: 12t+(3-t)=3+11t;
        # per N clause: 11(3-t).
        dominate_p = [3+11*t for t in range(4)]
        dominate_n = [11*(3-t) for t in range(4)]
        # P port=3, P aux=2a, N aux=2a.
        degree_cap = 12*3 + 1*(2*a) + 11*(2*a)
    else:
        raise ValueError("This exact certificate covers only a=3 or a=6")

    assert all(x <= y for x, y in zip(capacity["P"], dominate_p))
    assert all(x <= y for x, y in zip(capacity["N"], dominate_n))
    assert demand > degree_cap
    return {
        "auxiliaries": a,
        "assignment_weights": {str(h): w for h, w in aux_weights.items()},
        "weighted_assignment_demand": demand,
        "positive_clause_capacity_by_port_count_t0_to_t3": capacity["P"],
        "negative_clause_capacity_by_port_count_t0_to_t3": capacity["N"],
        "dominating_positive_degree_coefficients": dominate_p,
        "dominating_negative_degree_coefficients": dominate_n,
        "degree_equation_capacity_cap": degree_cap,
        "strict_deficit": demand - degree_cap,
        "conclusion": "Some full assignment with nonconstant port word satisfies every selected clause."
    }


def main():
    cases = [
        audit_case(3, {1: 1, 2: 2}),
        audit_case(6, {3: 1, 4: 3}),
    ]
    out = {
        "run": "M22-AUX-WEIGHTED-COVER150",
        "classification": "PROVED/EXACT elementary weighted union-bound certificate",
        "scope": "r=3, one pre-used positive occurrence per port, a in {3,6}; sign complement covers all-negative orientation",
        "uses_clause_uniqueness": False,
        "uses_extension_of_000_or_111": False,
        "cases": cases,
        "open": ["a>=9", "contextual/shared blocks", "LOCAL-COOK-TAGGED-SIGNED22-1", "ARC-EDGE-90", "DIRECT-POST", "P versus NP"]
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
