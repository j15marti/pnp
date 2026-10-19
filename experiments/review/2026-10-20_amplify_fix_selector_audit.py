#!/usr/bin/env python3
"""Exact finite audit for AMPLIFY-FIX-SELECTOR4.

Checks the 3x3 per-input/random-seed counterexamples and computes the exact
minimal odd repetition count r with 2^n * Pr[Bin(r,1/3) >= (r+1)/2] < 1.
Only Python integers and fractions are used.
"""

from fractions import Fraction
from itertools import product
from math import comb
import json


def majority_all_rows(matrix, seed_tuple):
    need = len(seed_tuple) // 2 + 1
    return all(sum(matrix[row][z] for z in seed_tuple) >= need
               for row in range(3))


def exact_majority_error(r):
    assert r % 2 == 1
    # A trial is bad with probability 1/3.
    numerator = sum(comb(r, j) * (2 ** (r - j))
                    for j in range((r + 1) // 2, r + 1))
    return Fraction(numerator, 3 ** r)


def main():
    matrices = []
    for bits in product((0, 1), repeat=9):
        a = [bits[3 * i:3 * i + 3] for i in range(3)]
        if all(sum(row) >= 2 for row in a) and not any(
                all(a[i][z] for i in range(3)) for z in range(3)):
            matrices.append(a)

    assert len(matrices) == 6
    min_tuple_lengths = []
    witnesses = []
    for a in matrices:
        found = None
        for r in (1, 3, 5):
            for zs in product(range(3), repeat=r):
                if majority_all_rows(a, zs):
                    found = (r, zs)
                    break
            if found:
                break
        assert found is not None
        min_tuple_lengths.append(found[0])
        witnesses.append(list(found[1]))

    minima = {}
    previous_r = {}
    pending = set(range(1, 65))
    r = 1
    while pending:
        err = exact_majority_error(r)
        for n in sorted(tuple(pending)):
            if (2 ** n) * err < 1:
                minima[str(n)] = r
                previous_r[str(n)] = r - 2 if r > 1 else None
                pending.remove(n)
        r += 2

    for n_text, rmin in minima.items():
        n = int(n_text)
        assert (2 ** n) * exact_majority_error(rmin) < 1
        if rmin > 1:
            assert (2 ** n) * exact_majority_error(rmin - 2) >= 1

    selected_n = [1, 2, 4, 8, 16, 32, 64]
    selected = {
        str(n): {
            "minimal_odd_r": minima[str(n)],
            "union_bound": {
                "numerator": (2 ** n * exact_majority_error(minima[str(n)])).numerator,
                "denominator": (2 ** n * exact_majority_error(minima[str(n)])).denominator,
            },
        }
        for n in selected_n
    }

    result = {
        "artifact": "AMPLIFY-FIX-SELECTOR4",
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "matrix_audit": {
            "matrices_enumerated": 512,
            "counterexamples": len(matrices),
            "minimum_repetition_lengths": min_tuple_lengths,
            "majority_seed_tuple_witnesses": witnesses,
        },
        "amplification_audit": {
            "domain_size": "2^n",
            "base_bad_probability": "1/3",
            "criterion": "2^n * Pr[Bin(r,1/3) >= (r+1)/2] < 1",
            "n_range": [1, 64],
            "selected_exact_minima": selected,
            "largest_minimal_odd_r": minima["64"],
            "checks": 512 + 6 + 64 * 2,
        },
        "interpretation": [
            "constant-error per-input seeds need not contain one globally good seed",
            "independent repetition plus a strict union bound yields a globally good seed tuple nonuniformly",
            "the audit does not supply a uniform selector or remove promise/circularity costs",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
