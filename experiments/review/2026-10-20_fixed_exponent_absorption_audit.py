#!/usr/bin/env python3
"""Exact-rational audit for the fixed-exponent/vanishing-parameter bridge."""

import json
from fractions import Fraction
from pathlib import Path


TIME_CAP = Fraction(241, 200)
SPACE_CAP = Fraction(1, 2)
BASELINES = {
    "one_full_scan": Fraction(1, 1),
    "arc_fixed_point_time": Fraction(6, 5),
}


def strict_integer_threshold(numerator: int, denominator: int) -> int:
    """Smallest integer k with numerator/k < denominator."""
    return numerator // denominator + 1


def run(max_exponent: int = 128) -> dict:
    cases = 0
    inequalities = 0
    failures = []
    maxima = {}

    for label, q in BASELINES.items():
        margin = TIME_CAP - q
        assert margin > 0
        maximum_k = 0
        for C in range(1, max_exponent + 1):
            for D in range(1, max_exponent + 1):
                k_time = strict_integer_threshold(
                    C * margin.denominator, margin.numerator
                )
                k_space = strict_integer_threshold(
                    D * SPACE_CAP.denominator, SPACE_CAP.numerator
                )
                k = max(k_time, k_space)
                maximum_k = max(maximum_k, k)
                cases += 1

                time_exp = q + Fraction(C, k)
                space_exp = Fraction(D, k)
                inequalities += 2
                if not (time_exp < TIME_CAP and space_exp < SPACE_CAP):
                    failures.append(
                        {
                            "label": label,
                            "C": C,
                            "D": D,
                            "k": k,
                            "time": str(time_exp),
                            "space": str(space_exp),
                        }
                    )

                if k > 1:
                    previous_time = q + Fraction(C, k - 1)
                    previous_space = Fraction(D, k - 1)
                    inequalities += 1
                    if previous_time < TIME_CAP and previous_space < SPACE_CAP:
                        failures.append(
                            {
                                "kind": "nonminimal_threshold",
                                "label": label,
                                "C": C,
                                "D": D,
                                "k": k,
                            }
                        )

        maxima[label] = maximum_k

    return {
        "run": "FIXED_EXPONENT_ABSORPTION2",
        "date_seoul": "2026-10-20 00:48",
        "time_cap": "241/200",
        "space_cap": "1/2",
        "formula": {
            "time": "q + C/k",
            "space": "D/k",
            "strict_k_time": "floor(C/(241/200-q))+1",
            "strict_k_space": "2D+1",
        },
        "tested_C_range": [1, max_exponent],
        "tested_D_range": [1, max_exponent],
        "baselines": {k: str(v) for k, v in BASELINES.items()},
        "cases": cases,
        "exact_inequality_checks": inequalities,
        "maximum_minimal_k": maxima,
        "failed_assertions": len(failures),
        "failure_examples": failures[:10],
        "scope": (
            "leading-exponent arithmetic only; requires one uniform all-k "
            "subroutine, sequential call ledger, and separately proved bridge"
        ),
        "P_vs_NP": "OPEN",
    }


if __name__ == "__main__":
    result = run()
    assert result["failed_assertions"] == 0, result["failure_examples"]
    out = Path(
        "results/raw/synthesis/"
        "2026-10-20_0048_FIXED_EXPONENT_ABSORPTION2.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
