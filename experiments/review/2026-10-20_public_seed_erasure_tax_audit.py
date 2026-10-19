#!/usr/bin/env python3
"""Exact arithmetic audit for PUBLIC-SEED-ERASURE-TAX5."""

from fractions import Fraction
import json


def product_tv(alpha, repeats):
    return 1 - (1 - alpha) ** repeats


def minimal_repeats(alpha, target=Fraction(1, 3)):
    """Exact binary search for least r >= 1 with product TV >= target."""
    lo, hi = 0, 1
    while product_tv(alpha, hi) < target:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if product_tv(alpha, mid) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def fraction_record(x):
    return {"numerator": x.numerator, "denominator": x.denominator}


def main():
    exact_alphas = [Fraction(1, 16), Fraction(1, 8), Fraction(1, 16),
                    Fraction(3, 16), Fraction(3, 16)]
    port_labels = ["1", "2", "1,2", "1,3", "1,2,3"]
    ports = []
    checks = 0
    for label, alpha in zip(port_labels, exact_alphas):
        r = minimal_repeats(alpha)
        assert product_tv(alpha, r) >= Fraction(1, 3)
        checks += 1
        if r > 1:
            assert product_tv(alpha, r - 1) < Fraction(1, 3)
            checks += 1
        assert product_tv(alpha, r) <= r * alpha
        checks += 1
        ports.append({
            "ports": label,
            "single_copy_tv": fraction_record(alpha),
            "minimal_repeats_for_tv_at_least_one_third": r,
            "tv_at_minimum": fraction_record(product_tv(alpha, r)),
        })

    scaling = []
    for log2_n in range(3, 7):
        n = 1 << log2_n
        for kappa in (1, 2):
            # delta=1/8 and t=(1+kappa)log_2 N give U=1/(8N^kappa).
            upper_alpha = Fraction(1, 8 * (n ** kappa))
            r = minimal_repeats(upper_alpha)
            assert product_tv(upper_alpha, r) >= Fraction(1, 3)
            assert product_tv(upper_alpha, r - 1) < Fraction(1, 3)
            assert r * upper_alpha >= Fraction(1, 3)
            checks += 3
            scaling.append({
                "N": n,
                "kappa": kappa,
                "tv_upper_bound": fraction_record(upper_alpha),
                "necessary_repeats_from_upper_bound": r,
                "r_times_upper_alpha": fraction_record(r * upper_alpha),
            })

    result = {
        "artifact": "PUBLIC-SEED-ERASURE-TAX5",
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "public_seed_port_controls": ports,
        "polynomial_erasure_scaling_controls": scaling,
        "checks": checks,
        "failures": 0,
        "scope": [
            "independent repetitions of one public-seed deterministic map",
            "TV identity is mathematical; finite cases audit arithmetic only",
            "does not analyze the original private-G1 CHMY generator",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
