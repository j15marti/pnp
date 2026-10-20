#!/usr/bin/env python3
"""Exact exponent/quantifier audit for SELECTOR-ELIMINATION11."""

from fractions import Fraction
import json

TIME_TARGET = Fraction(241, 200)
SPACE_TARGET = Fraction(1, 2)


def exponents(C, D, k):
    return Fraction(1, 1) + Fraction(C + 1, k), Fraction(max(1, D), k)


def admissible(C, D, k):
    t, s = exponents(C, D, k)
    return t < TIME_TARGET and s < SPACE_TARGET


def admissible_stretch(C, D, k, a):
    t, s = exponents(C, D, k)
    return a * t < TIME_TARGET and a * s < SPACE_TARGET


def threshold(C, D):
    # Strict inequalities: k > 200(C+1)/41 and k > 2 max(1,D).
    a = Fraction(200 * (C + 1), 41)
    b = Fraction(2 * max(1, D), 1)
    q = max(a, b)
    return q.numerator // q.denominator + 1


def next_power_two(n):
    return 1 << (n - 1).bit_length()


def main():
    assertions = 0
    fixed_solver_cases = 0
    hutter_cases = 0
    maxima = {"minimal_k": 0, "power_two_k": 0, "hutter_minimal_k": 0}

    # A fixed solver exponent is absorbable; even the sparse cofinal set {2^r} works.
    for C in range(1, 257):
        for D in range(1, 257):
            k = threshold(C, D)
            assert admissible(C, D, k); assertions += 1
            if k > 1:
                assert not admissible(C, D, k - 1); assertions += 1
            kp = next_power_two(k)
            assert admissible(C, D, kp); assertions += 1
            fixed_solver_cases += 1
            maxima["minimal_k"] = max(maxima["minimal_k"], k)
            maxima["power_two_k"] = max(maxima["power_two_k"], kp)

    # Hutter's published time bound includes time to evaluate the proved bound.
    # Its exponent is H=max(C,E), never smaller than C.
    for C in range(1, 65):
        for E in range(1, 65):
            for D in range(1, 17):
                H = max(C, E)
                k = threshold(H, D)
                assert admissible(H, D, k); assertions += 1
                assert H >= C; assertions += 1
                hutter_cases += 1
                maxima["hutter_minimal_k"] = max(maxima["hutter_minimal_k"], k)

    # If the query solver changes with k and C_k=k^2, increasing k never helps.
    dependent_successes = []
    for k in range(1, 4097):
        Ck = k * k
        if admissible(Ck, 1, k):
            dependent_successes.append(k)
        assert Fraction(1, 1) + Fraction(Ck + 1, k) > TIME_TARGET
        assertions += 1
    assert not dependent_successes; assertions += 1

    # A finite menu of k cannot absorb an arbitrary fixed exponent.
    finite_menu = list(range(1, 101))
    finite_counterexample = {"C": 1000, "D": 1}
    assert not any(admissible(1000, 1, k) for k in finite_menu); assertions += 1

    # Concrete comparison: direct existential solver versus certified universal wrapper.
    concrete = []
    for C, D, E in [(4, 2, 1), (4, 2, 9), (20, 7, 3), (20, 7, 40)]:
        kd = threshold(C, D)
        H = max(C, E)
        kh = threshold(H, D)
        assert kh >= kd; assertions += 1
        concrete.append({"C": C, "D": D, "bound_eval_E": E,
                         "direct_k": kd, "hutter_H": H, "hutter_k": kh})

    stretch_controls = []
    expected = {
        Fraction(1, 1): 25,
        Fraction(21, 20): 34,
        Fraction(11, 10): 53,
        Fraction(6, 5): 1201,
    }
    for a in [Fraction(1, 1), Fraction(21, 20), Fraction(11, 10),
              Fraction(6, 5), Fraction(241, 200), Fraction(5, 4), Fraction(2, 1)]:
        found = next((k for k in range(1, 10000)
                      if admissible_stretch(4, 2, k, a)), None)
        if a in expected:
            assert found == expected[a]; assertions += 1
        else:
            assert found is None; assertions += 1
        stretch_controls.append({"a": f"{a.numerator}/{a.denominator}",
                                 "minimal_k": found})

    result = {
        "run": "SELECTOR_ELIMINATION_QUANTIFIERS11",
        "date_kst": "2026-10-20 09:48",
        "time_target": "241/200",
        "space_target": "1/2",
        "formula": {"time": "1+(C+1)/k", "space": "max(1,D)/k"},
        "length_stretch_formula": {"time": "a(1+(C+1)/k)",
                                   "space": "a max(1,D)/k"},
        "fixed_solver_cases": fixed_solver_cases,
        "hutter_cases": hutter_cases,
        "assertions": assertions,
        "maxima": maxima,
        "cofinal_control": "powers of two always supplied an admissible fixed k",
        "solver_dependent_control": {"C_k": "k^2", "k_tested": 4096,
                                     "admissible_k": dependent_successes},
        "finite_menu_counterexample": {"menu": "1..100", **finite_counterexample,
                                        "admissible": False},
        "concrete": concrete,
        "stretch_controls_C4_D2": stretch_controls,
        "proved_interpretation": "Any one fixed polynomial query solver plus a cofinal fixed-k reduction family suffices existentially; selecting the fastest solver is unnecessary.",
        "open_interface": "No total charged ordinary-MKTP R_k family is constructed.",
        "P_vs_NP": "OPEN"
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
