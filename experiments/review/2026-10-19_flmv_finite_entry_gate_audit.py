#!/usr/bin/env python3
"""Exact-arithmetic audit for the conditional ARC/FLMV endpoint gate.

This script checks only exponent arithmetic.  It does not construct a SAT
algorithm or the missing hereditary contraction stage.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


FIXED_T = Fraction(6, 5)
FIXED_S = Fraction(1, 2)
SAFE_T = Fraction(241, 200)


def beta(c: Fraction) -> Fraction:
    """FLMV Corollary-5.8 sufficient space exponent used in the project."""
    return ((c + 2) / (c * c) - c) / 2


def step(t: Fraction, s: Fraction) -> tuple[Fraction, Fraction]:
    return max(Fraction(11, 10), Fraction(3, 5) + t / 2), max(FIXED_S, s / 2)


def ceil_log2_fraction(x: Fraction) -> int:
    if x <= 1:
        return 0
    j = 0
    p = Fraction(1)
    while p < x:
        p *= 2
        j += 1
    return j


def formula_bound(t0: Fraction, s0: Fraction) -> int:
    time_scale = 200 * max(t0 - FIXED_T, Fraction(0))
    space_scale = 2 * max(s0, Fraction(0))
    return max(ceil_log2_fraction(time_scale), ceil_log2_fraction(space_scale))


def first_safe_stage(t0: Fraction, s0: Fraction, cap: int = 256) -> tuple[int, Fraction, Fraction]:
    t, s = t0, s0
    for j in range(cap + 1):
        if t <= SAFE_T and s <= FIXED_S:
            return j, t, s
        t, s = step(t, s)
    raise RuntimeError("stage cap exceeded")


def frac_record(x: Fraction) -> dict[str, object]:
    return {
        "numerator": x.numerator,
        "denominator": x.denominator,
        "decimal": float(x),
    }


def audit() -> dict[str, object]:
    safe_beta = beta(SAFE_T)
    fixed_beta = beta(FIXED_T)
    assert fixed_beta == Fraction(23, 45)
    assert safe_beta == Fraction(11642479, 23232400)
    assert safe_beta > FIXED_S

    samples: list[dict[str, object]] = []
    for t_num in range(6, 126):
        t0 = Fraction(t_num, 5)
        for s_num in range(1, 101):
            s0 = Fraction(s_num, 4)
            j, tj, sj = first_safe_stage(t0, s0)
            bound = formula_bound(t0, s0)
            assert j <= bound
            assert tj <= SAFE_T and sj <= FIXED_S
            assert beta(tj) > FIXED_S
            if (t_num, s_num) in {(6, 2), (10, 4), (25, 20), (85, 56), (125, 100)}:
                samples.append(
                    {
                        "t0": str(t0),
                        "s0": str(s0),
                        "first_safe_stage": j,
                        "formula_bound": bound,
                        "t_at_stage": str(tj),
                        "s_at_stage": str(sj),
                    }
                )

    j, tj, sj = first_safe_stage(Fraction(17), Fraction(14))
    assert j == 12
    assert formula_bound(Fraction(17), Fraction(14)) == 12

    # Bisection is numerical and used only to report the time-slack horizon.
    lo, hi = 1.2, 1.3
    for _ in range(100):
        mid = (lo + hi) / 2
        b = ((mid + 2) / (mid * mid) - mid) / 2
        if b > 0.5:
            lo = mid
        else:
            hi = mid

    return {
        "record": "FLMV_FINITE_ENTRY_GATE1",
        "status": {
            "endpoint_arithmetic": "PROVED",
            "grid_audit": "COMPUTATIONAL",
            "hereditary_contraction_stage": "OPEN",
            "p_vs_np": "OPEN",
        },
        "recurrence": {
            "time": "t_next <= max(11/10, 3/5 + t/2)",
            "space": "s_next <= max(1/2, s/2)",
            "fixed_point": {"t": "6/5", "s": "1/2"},
        },
        "flmv_curve": "beta(c)=((c+2)/c^2-c)/2",
        "safe_point": {
            "c": frac_record(SAFE_T),
            "beta_c": frac_record(safe_beta),
            "space_margin_over_one_half": frac_record(safe_beta - FIXED_S),
        },
        "fixed_point": {
            "beta_6_over_5": frac_record(fixed_beta),
            "space_margin_over_one_half": frac_record(fixed_beta - FIXED_S),
        },
        "finite_entry_bound": (
            "J=max(ceil_log2(200*max(t0-6/5,0)), "
            "ceil_log2(2*max(s0,0)))"
        ),
        "case_17_14": {
            "first_safe_stage": j,
            "formula_bound": formula_bound(Fraction(17), Fraction(14)),
            "t_at_stage": frac_record(tj),
            "s_at_stage": frac_record(sj),
            "beta_t_at_stage": frac_record(beta(tj)),
        },
        "numerical_beta_equals_half_root": lo,
        "safe_time_slack_above_fixed_point": float(SAFE_T - FIXED_T),
        "tested_grid": {
            "t0": "{k/5: 6<=k<=125}",
            "s0": "{k/4: 1<=k<=100}",
            "cases": 12000,
            "assertion": "first safe stage <= formula bound and beta(t_stage)>1/2",
        },
        "sample_cases": samples,
        "scope_warning": (
            "The audit verifies exponent recurrence and FLMV endpoint inequalities only; "
            "it does not supply the solver-dependent, uniform, all-input, hereditary, "
            "fully charged contraction stage."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
