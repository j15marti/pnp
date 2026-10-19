#!/usr/bin/env python3
"""Exact audit of the conditional ARC/FLMV overhead-space frontier.

This checks exponent arithmetic only.  It does not construct the missing
all-input, hereditary SAT contraction stage.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


BASE_TIME = Fraction(11, 10)
AFFINE_FIXED_TIME = Fraction(6, 5)
BASE_SPACE = Fraction(1, 2)


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def time_step(t: Fraction, q: Fraction) -> Fraction:
    return max(BASE_TIME, q, Fraction(3, 5) + t / 2)


def space_step(s: Fraction, r: Fraction) -> Fraction:
    return max(BASE_SPACE, r, s / 2)


def endpoint(q: Fraction, r: Fraction) -> tuple[Fraction, Fraction]:
    return max(AFFINE_FIXED_TIME, q), max(BASE_SPACE, r)


def margin(q: Fraction, r: Fraction) -> Fraction:
    c, d = endpoint(q, r)
    return beta(c) - d


def first_forbidden_stage(
    q: Fraction,
    r: Fraction,
    t0: Fraction = Fraction(17),
    s0: Fraction = Fraction(14),
    cap: int = 4096,
) -> int | None:
    t, s = t0, s0
    for j in range(cap + 1):
        # Exact positive-root test for t < phi: t^2 < t+1.
        if t * t < t + 1 and s < beta(t):
            return j
        t, s = time_step(t, q), space_step(s, r)
    return None


def fraction_record(x: Fraction) -> dict[str, object]:
    return {
        "numerator": x.numerator,
        "denominator": x.denominator,
        "decimal": float(x),
    }


def root_beta_half() -> Decimal:
    """Positive root of c^3+c^2-c-2=0 by deterministic bisection."""
    getcontext().prec = 60
    lo, hi = Decimal("1.2"), Decimal("1.21")
    for _ in range(240):
        mid = (lo + hi) / 2
        value = mid**3 + mid**2 - mid - 2
        if value < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def audit() -> dict[str, object]:
    cases = [
        ("baseline", Fraction(11, 10), Fraction(1, 2)),
        ("time_safe_241_over_200", Fraction(241, 200), Fraction(1, 2)),
        ("time_near_safe", Fraction(2411, 2000), Fraction(1, 2)),
        ("time_unsafe_12057_over_10000", Fraction(12057, 10000), Fraction(1, 2)),
        ("time_unsafe_121_over_100", Fraction(121, 100), Fraction(1, 2)),
        ("space_safe_51_over_100", Fraction(6, 5), Fraction(51, 100)),
        ("space_boundary_23_over_45", Fraction(6, 5), Fraction(23, 45)),
        ("space_unsafe_13_over_25", Fraction(6, 5), Fraction(13, 25)),
    ]
    records: list[dict[str, object]] = []
    for name, q, r in cases:
        c, d = endpoint(q, r)
        m = beta(c) - d
        stage = first_forbidden_stage(q, r)
        assert (stage is not None) == (m > 0)
        records.append(
            {
                "name": name,
                "q": str(q),
                "r": str(r),
                "endpoint_time": str(c),
                "endpoint_space": str(d),
                "flmv_margin": fraction_record(m),
                "strictly_inside_sufficient_region": m > 0,
                "first_forbidden_stage_from_17_14": stage,
            }
        )

    # Exhaustive rational grid: exact endpoint classification must agree with
    # eventual entry from (17,14) for every tested point away from equality.
    checked = 0
    boundary = 0
    for q_milli in range(1050, 1301, 5):
        q = Fraction(q_milli, 1000)
        for r_milli in range(450, 651, 5):
            r = Fraction(r_milli, 1000)
            m = margin(q, r)
            stage = first_forbidden_stage(q, r, cap=256)
            if m == 0:
                boundary += 1
                assert stage is None
            else:
                assert (stage is not None) == (m > 0)
            checked += 1

    root = root_beta_half()
    assert Decimal("1.2055") < root < Decimal("1.2057")
    assert margin(Fraction(2411, 2000), Fraction(1, 2)) > 0
    assert margin(Fraction(12057, 10000), Fraction(1, 2)) < 0
    assert margin(Fraction(6, 5), Fraction(23, 45)) == 0

    return {
        "record": "ARC_OVERHEAD_SPACE_PHASE1",
        "status": {
            "phase_frontier_arithmetic": "PROVED/EXACT",
            "grid_audit": "COMPUTATIONAL",
            "hereditary_contraction_stage": "OPEN",
            "p_vs_np": "OPEN",
        },
        "conditional_envelope": {
            "time": "t_next <= max(11/10, q, 3/5+t/2)",
            "space": "s_next <= max(1/2, r, s/2)",
            "endpoint_time": "C=max(6/5,q)",
            "endpoint_space": "R=max(1/2,r)",
        },
        "flmv_sufficient_curve": "beta(c)=((c+2)/c^2-c)/2",
        "strict_entry_condition": "max(1/2,r) < beta(max(6/5,q))",
        "half_space_time_cutoff": {
            "defining_polynomial": "c^3+c^2-c-2=0",
            "root_decimal": str(root),
            "safe_iff": "q < root (when r<=1/2)",
        },
        "low_time_space_cutoff": {
            "condition": "r < 23/45 (when q<=6/5)",
            "margin_at_r_equals_one_half": fraction_record(Fraction(1, 90)),
        },
        "representative_cases": records,
        "grid": {
            "q": "{k/1000: 1050<=k<=1300, k divisible by 5}",
            "r": "{k/1000: 450<=k<=650, k divisible by 5}",
            "pairs_checked": checked,
            "exact_boundary_pairs": boundary,
            "assertion": "positive endpoint margin iff finite FLMV entry from (17,14)",
        },
        "scope_warning": (
            "This is an exact phase diagram for a conditional resource envelope. "
            "It neither constructs the all-input hereditary contraction stage nor "
            "transfers MCSP, proof-system, circuit, or physical lower bounds to SAT."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(audit(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
