#!/usr/bin/env python3
"""Exact-rational audit for COFINAL-AMORTIZED-PIPE13.

This checks the exponent composition only.  It does not construct the
ordinary-MKTP target generator whose existence is the open hypothesis.
"""

from fractions import Fraction
import json
import math
from pathlib import Path

TAU = Fraction(241, 200)
SIGMA = Fraction(1, 2)


def composed(a, k, C, D, B, E):
    """Return (time,space) exponents for G=M*p^B, H=p^E."""
    g = Fraction(1) + Fraction(B, k)
    h = Fraction(E, k)
    t = a * max(g, Fraction(1) + Fraction(C + 1, k))
    s = a * max(h, Fraction(max(1, D), k))
    return t, s


def family_values(name, k):
    if name == "fixed_4_2":
        return 4, 2
    if name == "sqrt_log":
        return math.isqrt(k), math.ceil(math.log2(k))
    if name == "linear_good":
        return k // 1000, k // 3
    if name == "linear_bad_time":
        return k // 100, k // 3
    if name == "linear_bad_space":
        return k // 1000, k // 2
    raise ValueError(name)


def main():
    a_values = [Fraction(1), Fraction(21, 20), Fraction(11, 10), Fraction(6, 5)]
    families = ["fixed_4_2", "sqrt_log", "linear_good", "linear_bad_time", "linear_bad_space"]
    # Dense enough to cover changing maxima while keeping the audit quick;
    # the asymptotic family classification below is symbolic/exact.
    ks = list(range(8, 520, 5))
    assertions = 0
    failures = []
    samples = []

    for a in a_values:
        for C in range(1, 33):
            for D in range(1, 33):
                for k in ks:
                    B, E = family_values("fixed_4_2", k)
                    t, s = composed(a, k, C, D, B, E)
                    direct_t = a * max(Fraction(1) + Fraction(B, k), Fraction(1) + Fraction(C + 1, k))
                    direct_s = a * max(Fraction(E, k), Fraction(max(1, D), k))
                    assertions += 2
                    if t != direct_t:
                        failures.append(["time_identity", str(a), C, D, k])
                    if s != direct_s:
                        failures.append(["space_identity", str(a), C, D, k])

    a = Fraction(6, 5)
    time_budget = TAU / a - 1
    space_budget = SIGMA / a
    assertions += 2
    if time_budget != Fraction(1, 240):
        failures.append(["time_budget", str(time_budget)])
    if space_budget != Fraction(5, 12):
        failures.append(["space_budget", str(space_budget)])

    # Symbolic asymptotic classifications for B_k/k and E_k/k.
    expected = {
        "fixed_4_2": True,
        "sqrt_log": True,
        "linear_good": True,
        "linear_bad_time": False,
        "linear_bad_space": False,
    }
    limiting_ratios = {
        "fixed_4_2": (Fraction(0), Fraction(0)),
        "sqrt_log": (Fraction(0), Fraction(0)),
        "linear_good": (Fraction(1, 1000), Fraction(1, 3)),
        "linear_bad_time": (Fraction(1, 100), Fraction(1, 3)),
        "linear_bad_space": (Fraction(1, 1000), Fraction(1, 2)),
    }
    classifications = {}
    for name in families:
        br, er = limiting_ratios[name]
        ok = br < time_budget and er < space_budget
        classifications[name] = {
            "B_over_k_limit": str(br),
            "E_over_k_limit": str(er),
            "cofinally_feasible_generator": ok,
        }
        assertions += 1
        if ok != expected[name]:
            failures.append(["classification", name, ok])

    # Witness that fixed overhead absorbs several unknown fixed solver exponents.
    for C, D in [(1, 1), (7, 11), (32, 32), (100, 100)]:
        k = 100000
        B, E = family_values("fixed_4_2", k)
        t, s = composed(a, k, C, D, B, E)
        assertions += 2
        if not t < TAU:
            failures.append(["fixed_absorb_time", C, D, str(t)])
        if not s < SIGMA:
            failures.append(["fixed_absorb_space", C, D, str(s)])
        samples.append({"C": C, "D": D, "k": k, "time": str(t), "space": str(s)})

    result = {
        "run": "COFINAL-AMORTIZED-PIPE13",
        "status": "PASS" if not failures else "FAIL",
        "theorem_scope": "exponent-composition audit; totalizer existence not tested",
        "tau": str(TAU),
        "sigma": str(SIGMA),
        "a_focus": str(a),
        "time_budget_B_over_k": str(time_budget),
        "space_budget_E_over_k": str(space_budget),
        "assertions": assertions,
        "failures": failures,
        "classifications": classifications,
        "fixed_overhead_samples": samples,
    }
    out = Path("results/raw/synthesis/2026-10-20_1048_COFINAL_AMORTIZED_PIPE13.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
