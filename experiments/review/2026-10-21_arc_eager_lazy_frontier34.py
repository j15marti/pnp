#!/usr/bin/env python3
"""Exact rational audit for ARC-EAGER-LAZY-FRONTIER34.

Compares two simulations of q=N^a children of length L=N^lambda:
eager sequential materialization versus lazy recomputation on every child-bit
probe.  This is an accounting theorem, not an ARC constructor or SAT lower
bound.
"""

from fractions import Fraction
import hashlib
import json


TARGET_T = Fraction(6, 5)
TARGET_S = Fraction(1, 2)


def eager_time(a, lam, t, g, r=Fraction(0)):
    return max(r, a + lam + g, a + lam * t)


def lazy_time(a, lam, t, g, r=Fraction(0)):
    return max(r, a + lam * t + g)


def eager_space(lam, s, eta=Fraction(0), kappa=Fraction(0)):
    return max(lam, lam * s, eta, kappa)


def lazy_space(lam, s, eta=Fraction(0), kappa=Fraction(0)):
    return max(lam * s, eta, kappa)


def fs(x):
    return f"{x.numerator}/{x.denominator}"


def run():
    checks = 0
    rational_cases = 0
    eager_feasible = 0
    lazy_feasible = 0
    dominance_checks = 0
    boundary_checks = 0
    concrete_controls = []

    grid = [Fraction(i, 20) for i in range(0, 25)]
    for a in [x for x in grid if x <= Fraction(3, 5)]:
        for lam in [x for x in grid if Fraction(1, 10) <= x <= Fraction(1, 2)]:
            for g in [x for x in grid if x <= Fraction(2, 5)]:
                et = eager_time(a, lam, TARGET_T, g)
                lt = lazy_time(a, lam, TARGET_T, g)
                es = eager_space(lam, TARGET_S)
                ls = lazy_space(lam, TARGET_S)
                assert et == max(a + lam + g, a + lam * TARGET_T)
                assert lt == a + lam * TARGET_T + g
                assert es == lam
                assert ls == lam * TARGET_S
                checks += 4
                rational_cases += 1
                eager_feasible += int(et <= TARGET_T and es <= TARGET_S)
                lazy_feasible += int(lt <= TARGET_T and ls <= TARGET_S)
                # Eager generation charges each child bit once; lazy access
                # charges the generator for every solver probe.  For t>=1,
                # the access exponent in eager mode never exceeds lazy mode.
                assert a + lam + g <= a + lam * TARGET_T + g
                dominance_checks += 1
                checks += 1

    a = Fraction(3, 5)
    lam = Fraction(1, 2)
    t = Fraction(6, 5)
    # Exact saturated endpoint.
    assert lazy_time(a, lam, t, Fraction(0)) == TARGET_T
    assert lazy_time(a, lam, t, Fraction(1, 20)) == Fraction(5, 4)
    assert eager_time(a, lam, t, Fraction(1, 10)) == TARGET_T
    assert eager_time(a, lam, t, Fraction(3, 20)) == Fraction(5, 4)
    assert eager_space(lam, Fraction(1, 2)) == Fraction(1, 2)
    assert lazy_space(lam, Fraction(1, 2)) == Fraction(1, 4)
    boundary_checks += 6
    checks += 6

    # Direct slack formulas at t*=6/5:
    # lazy g <= 6/5-a-(6/5)lambda;
    # eager g <= 6/5-a-lambda, while solver calls require
    # a+(6/5)lambda <= 6/5.
    for a_num in range(0, 13):
        a = Fraction(a_num, 20)
        for lam_num in range(2, 11):
            lam = Fraction(lam_num, 20)
            lazy_budget = TARGET_T - a - lam * TARGET_T
            eager_budget = TARGET_T - a - lam
            assert eager_budget - lazy_budget == lam * (TARGET_T - 1)
            checks += 1
            boundary_checks += 1

    # Exact integer growth controls at the saturated point and g=1/10.
    # N=2^(10k), q=2^(6k), L=2^(5k), solver probes/child=2^(6k),
    # generator cost=2^k.
    for k in range(1, 21):
        q = 2 ** (6 * k)
        L = 2 ** (5 * k)
        probes = 2 ** (6 * k)
        generator_cost = 2**k
        eager_generation = q * L * generator_cost
        eager_solver = q * probes
        lazy_generation = q * probes * generator_cost
        assert eager_generation == eager_solver
        assert lazy_generation // eager_generation == generator_cost
        concrete_controls.append({
            "k": k,
            "eager_generation": str(eager_generation),
            "eager_solver": str(eager_solver),
            "lazy_generation": str(lazy_generation),
            "lazy_over_eager_generation": generator_cost,
        })
        checks += 2

    result = {
        "name": "ARC-EAGER-LAZY-FRONTIER34",
        "status": "exact accounting frontier; contractor OPEN; P versus NP OPEN",
        "target_time": fs(TARGET_T),
        "target_space": fs(TARGET_S),
        "rational_cases": rational_cases,
        "eager_feasible_cases": eager_feasible,
        "lazy_feasible_cases": lazy_feasible,
        "dominance_checks": dominance_checks,
        "boundary_checks": boundary_checks,
        "concrete_growth_controls": len(concrete_controls),
        "instrumented_assertions": checks,
        "failures": 0,
        "saturated_frontier": {
            "a": "3/5",
            "lambda": "1/2",
            "solver_time_exponent": "6/5",
            "eager_max_access_exponent": "1/10",
            "lazy_max_access_exponent": "0",
            "eager_peak_child_buffer_exponent": "1/2",
            "lazy_solver_space_exponent": "1/4"
        },
        "scope_firewall": [
            "does not construct semantic children",
            "does not prove all-input heredity",
            "does not transfer restricted models",
            "does not prove an unrestricted SAT lower bound"
        ]
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["audit_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
