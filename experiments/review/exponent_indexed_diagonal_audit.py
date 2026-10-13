#!/usr/bin/env python3
"""Finite arithmetic audit for the exponent-indexed conditional composition.

This checks only the rational parameter quantifiers used by DIAGTRANSFER1.
It does not construct proofs and does not implement a decider-to-proof transfer.
"""

from fractions import Fraction
import json
import time


def admissible(k: int, p: Fraction, beta: Fraction) -> bool:
    return p > k and p > 1 and Fraction(1) < beta < Fraction(1) + Fraction(1, p)


def main() -> None:
    started = time.perf_counter()
    checks = 0
    rows = []
    for k in range(1, 65):
        p = Fraction(k + 1)
        beta = Fraction(1) + Fraction(1, 2 * p)
        assert admissible(k, p, beta)
        checks += 4

        # With p-k=1, L^p > R L^k for every integer L>R.
        thresholds = {}
        for ratio in (1, 10, 10**6):
            length = ratio + 1
            assert length**p.numerator > ratio * length**k
            thresholds[str(ratio)] = length
            checks += 1

        # Hostile boundary controls.
        assert not admissible(k, Fraction(k), beta)
        assert not admissible(k, p, Fraction(1))
        assert not admissible(k, p, Fraction(1) + Fraction(1, p))
        if k >= 2:
            assert not admissible(k, Fraction(2), Fraction(5, 4))
            checks += 1
        checks += 3

        rows.append({
            "K": k,
            "p": str(p),
            "beta": str(beta),
            "p_minus_K": str(p - k),
            "dominance_thresholds_for_ratio_C_over_c": thresholds,
        })

    output = {
        "status": "COMPUTATIONAL",
        "scope": "finite exact-rational audit of exponent selection only",
        "does_not_test": "decider-to-sCP/triangle-DAG transfer",
        "K_range": [1, 64],
        "checks": checks,
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
