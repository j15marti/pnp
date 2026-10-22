#!/usr/bin/env python3
"""Finite arithmetic/quantifier audit for SHRUNK-QUERY-ENVELOPE67."""

from __future__ import annotations

import json
import math


def fixed_point(alpha, beta, gamma):
    assert 0 <= beta < 1
    return max(gamma, alpha / (1 - beta))


def iterate(c, alpha, beta, gamma, rounds):
    values = [c]
    for _ in range(rounds):
        c = max(gamma, alpha + beta * c)
        values.append(c)
    return values


def main():
    checks = 0
    alpha, beta, gamma = 0.6, 0.5, 1.1
    target = fixed_point(alpha, beta, gamma)
    assert abs(target - 1.2) < 1e-12
    checks += 1

    convergence = []
    for c0_tenths in range(13, 1001):
        c0 = c0_tenths / 10
        for eps_exp in range(1, 10):
            eps = 10 ** (-eps_exp)
            k = math.ceil(math.log2(max(1.0, (c0 - target) / eps)))
            values = iterate(c0, alpha, beta, gamma, k)
            assert values[-1] <= target + eps + 1e-12
            assert all(values[i + 1] <= values[i] + 1e-12
                       for i in range(len(values) - 1))
            checks += 2
        convergence.append({
            "c0": c0,
            "rounds_for_eps_1e_6": math.ceil(
                math.log2(max(1.0, (c0 - target) / 1e-6))
            ),
        })

    general_rows = []
    for alpha_i in range(0, 10):
        for beta_i in range(0, 10):
            for gamma_i in range(0, 10):
                a = alpha_i / 10
                b = beta_i / 10
                g = gamma_i / 10
                star = fixed_point(a, b, g)
                vals = iterate(star + 10, a, b, g, 400)
                assert abs(vals[-1] - star) < 1e-8
                assert all(vals[i + 1] <= vals[i] + 1e-12
                           for i in range(len(vals) - 1))
                checks += 2
                general_rows.append({
                    "alpha": a,
                    "beta": b,
                    "gamma": g,
                    "fixed_point": star,
                })

    # Sequential peak-space recurrence: max(delta, beta_s*s).
    delta, beta_s = 0.5, 0.5
    for s0_tenths in range(5, 1001):
        s = s0_tenths / 10
        for _ in range(200):
            s = max(delta, beta_s * s)
        assert abs(s - delta) < 1e-12
        checks += 1

    # Parent-scale beta=1 cannot have alpha+beta*c<c for alpha>=0.
    for alpha_i in range(0, 101):
        a = alpha_i / 100
        for c_tenths in range(1, 1001):
            c = c_tenths / 10
            assert a + c >= c
            checks += 1

    print(json.dumps({
        "status": "arithmetic_and_quantifier_audit_only_no_class_separation",
        "target_parameters": {
            "query_count_exponent_alpha": alpha,
            "child_length_exponent_beta": beta,
            "overhead_exponent_gamma": gamma,
            "time_fixed_point": target,
            "space_fixed_point": delta,
        },
        "checks": checks,
        "failures": 0,
        "tested_starting_time_exponents": len(convergence),
        "tested_general_parameter_triples": len(general_rows),
        "identity": "c_star=max(gamma,alpha/(1-beta))",
        "strict_improvement_condition":
            "gamma<c and alpha<(1-beta)*c",
        "quantifier_note":
            "for each fixed finite c0 and epsilon, a finite external iteration depth exists",
        "excluded_claim":
            "no ARC transformer, FLMV transfer, P-vs-NP result, or P-vs-RP result is proved",
        "convergence": convergence,
        "general_rows": general_rows,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
