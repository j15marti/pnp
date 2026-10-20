#!/usr/bin/env python3
"""Exact rational audit for VIRTUAL-ORDINARY-INPUT16.

This checks the exponent arithmetic only.  It does not construct the missing
SAT-to-MKTP map or the missing all-input ARC child family.
"""

from fractions import Fraction
import json
from pathlib import Path


TAU = Fraction(241, 200)
A = Fraction(6, 5)
U = Fraction(3, 5)
V = Fraction(1, 2)
BASE_TIME = Fraction(11, 10)
BASE_SPACE = Fraction(1, 2)


def flmv_d(c):
    """Corollary 5.8 (k=2) space exponent at time exponent c."""
    return Fraction(1, 2) * ((c + 2) / (c * c) - c)


def arc_step(t, s, g, e=BASE_TIME, h=BASE_SPACE):
    return max(BASE_TIME, e, U + g + V * t), max(BASE_SPACE, h, V * s)


def first_arc_entry(t0, s0, g, limit=10000):
    t, s = t0, s0
    for j in range(limit + 1):
        if t < TAU and s <= BASE_SPACE:
            return j, t, s
        t, s = arc_step(t, s, g)
    return None


def ceil_fraction(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def first_mmw_k(C, D, gamma):
    """Exact first k entering time<TAU and space<=1/2."""
    delta = TAU - A - gamma
    if delta <= 0:
        return None
    # Strict time inequality: k > A(C+1)/delta.
    time_k = (A * (C + 1) / delta).numerator // (A * (C + 1) / delta).denominator + 1
    # Weak space inequality: k >= 2A max(1,D).
    space_k = ceil_fraction(2 * A * max(1, D))
    k = max(1, time_k, space_k)
    t = A * (1 + Fraction(C + 1, k)) + gamma
    s = A * Fraction(max(1, D), k)
    return k, t, s


def main():
    failures = []
    assertions = 0

    # Exact FLMV margin at the selected rational time point.
    d_tau = flmv_d(TAU)
    assertions += 2
    if not d_tau == Fraction(11642479, 23232400):
        failures.append(["flmv_fraction", str(d_tau)])
    if not d_tau > BASE_SPACE:
        failures.append(["flmv_margin", str(d_tau)])

    # ARC fixed point is 6/5+2g.  Strict entry below 241/200 is
    # equivalent to g<1/400 when the other floors stay below TAU.
    arc_g_star = Fraction(1, 400)
    arc_cases = 0
    arc_samples = []
    below = [Fraction(0), Fraction(1, 1600), Fraction(1, 800), Fraction(3, 1600)]
    at_or_above = [arc_g_star, Fraction(1, 200), Fraction(1, 100)]
    for g in below:
        fixed = (U + g) / (1 - V)
        assertions += 2
        if not fixed < TAU:
            failures.append(["arc_fixed_below", str(g), str(fixed)])
        for t0 in range(1, 65):
            for s0 in range(1, 65):
                got = first_arc_entry(Fraction(t0), Fraction(s0), g)
                arc_cases += 1
                assertions += 1
                if got is None:
                    failures.append(["arc_no_entry", str(g), t0, s0])
                elif len(arc_samples) < 10:
                    j, t, s = got
                    arc_samples.append({"g": str(g), "t0": t0, "s0": s0,
                                        "iterations": j, "t": str(t), "s": str(s)})
    for g in at_or_above:
        fixed = (U + g) / (1 - V)
        assertions += 2
        if not fixed >= TAU:
            failures.append(["arc_fixed_at_or_above", str(g), str(fixed)])
        # Starting above the fixed point can never cross strictly below TAU.
        got = first_arc_entry(Fraction(64), Fraction(64), g, limit=4096)
        arc_cases += 1
        assertions += 1
        if got is not None:
            failures.append(["arc_false_entry", str(g), got[0], str(got[1])])

    # MMW virtual-query generation has limiting time exponent 6/5+gamma.
    # The selected time point therefore permits exactly gamma<1/200.
    mmw_gamma_star = Fraction(1, 200)
    mmw_cases = 0
    mmw_samples = []
    for gamma in [Fraction(0), Fraction(1, 800), Fraction(1, 400), Fraction(1, 250)]:
        assertions += 1
        if not A + gamma < TAU:
            failures.append(["mmw_limit_below", str(gamma)])
        for C in range(1, 65):
            for D in range(1, 65):
                got = first_mmw_k(C, D, gamma)
                mmw_cases += 1
                assertions += 2
                if got is None:
                    failures.append(["mmw_no_k", str(gamma), C, D])
                    continue
                k, t, s = got
                if not (t < TAU and s <= BASE_SPACE):
                    failures.append(["mmw_bad_entry", str(gamma), C, D, k])
                if len(mmw_samples) < 10:
                    mmw_samples.append({"gamma": str(gamma), "C": C, "D": D,
                                        "k": k, "t": str(t), "s": str(s)})
    for gamma in [mmw_gamma_star, Fraction(1, 100)]:
        assertions += 2
        if not A + gamma >= TAU:
            failures.append(["mmw_limit_at_or_above", str(gamma)])
        if first_mmw_k(1, 1, gamma) is not None:
            failures.append(["mmw_false_k", str(gamma)])

    result = {
        "run": "VIRTUAL-ORDINARY-INPUT16",
        "status": "PASS" if not failures else "FAIL",
        "scope": "exact exponent audit for lazy random-access simulation; constructions remain open",
        "flmv_time_point": str(TAU),
        "flmv_space_exponent_at_time_point": str(d_tau),
        "flmv_space_margin_over_one_half": str(d_tau - BASE_SPACE),
        "arc_per_access_threshold_strict": str(arc_g_star),
        "mmw_per_access_threshold_strict": str(mmw_gamma_star),
        "arc_cases": arc_cases,
        "mmw_cases": mmw_cases,
        "assertions": assertions,
        "arc_samples": arc_samples,
        "mmw_samples": mmw_samples,
        "failures": failures,
        "global_status": "P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-20_1348_VIRTUAL_ORDINARY_INPUT16.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
