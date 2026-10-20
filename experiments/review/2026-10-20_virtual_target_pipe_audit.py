#!/usr/bin/env python3
"""Exact exponent audit for VIRTUAL-TARGET-PIPE12.

This checks a conditional composition ledger only.  It does not construct the
online totalizer, prove SAT hardness of MKTP, or certify an FLMV simulation.
"""

from fractions import Fraction as F
import json

TAU = F(241, 200)
HALF = F(1, 2)


def strict_k(a, b, c, e, d):
    """Smallest integer k making both conservative inequalities strict."""
    h = max(b, c + 1)
    j = max(e, d, 1)
    barrier = max(a * h / (TAU - a), 2 * a * j)
    k = barrier.numerator // barrier.denominator + 1
    return k, h, j


checks = 0
max_k = 0
max_case = None
for a in [F(1), F(21, 20), F(11, 10), F(6, 5)]:
    for b in range(1, 17):
        for c in range(1, 17):
            for e in range(1, 17):
                for d in range(1, 17):
                    k, h, j = strict_k(a, b, c, e, d)
                    assert a * (1 + F(h, k)) < TAU
                    assert a * F(j, k) < HALF
                    if k > 1:
                        assert not (
                            a * (1 + F(h, k - 1)) < TAU
                            and a * F(j, k - 1) < HALF
                        )
                    checks += 3
                    if k > max_k:
                        max_k = k
                        max_case = [str(a), b, c, e, d, h, j]

# Representative ledgers, including the near-output-ceiling case a=6/5.
samples = []
for a, b, c, e, d in [
    (F(1), 2, 4, 2, 2),
    (F(21, 20), 3, 7, 4, 5),
    (F(11, 10), 8, 3, 7, 2),
    (F(6, 5), 1, 4, 1, 2),
]:
    k, h, j = strict_k(a, b, c, e, d)
    samples.append(
        {
            "a": str(a),
            "B": b,
            "C": c,
            "E": e,
            "D": d,
            "H": h,
            "J": j,
            "minimal_k": k,
            "time_exponent": str(a * (1 + F(h, k))),
            "space_exponent": str(a * F(j, k)),
        }
    )
    checks += 2

# Falsifiers: explicit full-target retention and k-dependent local exponent.
for a in [F(1), F(21, 20), F(11, 10), F(6, 5)]:
    assert a > HALF  # retaining M bits misses the space cap
    for k in range(1, 257):
        b_k = k
        assert a * (1 + F(b_k, k)) == 2 * a
        assert 2 * a > TAU
        checks += 2

# The output-length floor alone blocks a >= tau.
for a in [TAU, F(5, 4), F(3, 2), F(2)]:
    assert not a < TAU
    checks += 1

result = {
    "run": "VIRTUAL-TARGET-PIPE12",
    "date_kst": "2026-10-20 09:48",
    "status": "PASS_CONDITIONAL_LEDGER_P_VS_NP_OPEN",
    "time_cap": str(TAU),
    "space_cap": str(HALF),
    "parameter_tuples": 4 * 16**4,
    "exact_assertions": checks,
    "maximum_minimal_k": max_k,
    "maximum_case_a_B_C_E_D_H_J": max_case,
    "samples": samples,
    "falsifiers": {
        "M_bit_retention": "space exponent a > 1/2",
        "B_k_equals_k": "time exponent 2a > 241/200",
        "a_at_least_241_over_200": "explicit output floor misses strict cap",
    },
    "open_interface": "construct total deterministic online R_k bit generator with fixed B,E and ordinary MKTP semantics",
}
print(json.dumps(result, indent=2, sort_keys=True))
