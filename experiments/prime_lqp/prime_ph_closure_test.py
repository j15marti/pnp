#!/usr/bin/env python3
"""PRIMEPH1: finite alternating-search closure control for prime provenance.

Exhaustively tests a toy relation with the project's current quantifier shape:
    exists sigma forall u exists z forall y R(sigma,u,z,y)

This is a finite control illustrating prefix search. It does NOT assume or test P=NP.
"""

from itertools import product
import json
import math

TARGET = (1, 0, 1, 1, 0)
NONUNIQUE = {
    (0, 0, 0, 1, 1),
    (1, 0, 1, 1, 0),
    (1, 1, 1, 1, 1),
}
PRIMES = (2, 3, 5, 7, 11)


def fz(sigma, u):
    parity = sum(sigma) % 2
    return tuple(u[i] ^ parity for i in range(3))


def r_unique(sigma, u, z, y):
    return sigma == TARGET and z == fz(sigma, u)


def r_multi(sigma, u, z, y):
    return sigma in NONUNIQUE and z == fz(sigma, u)


def good(sigma, relation):
    """forall u exists z forall y R."""
    for u in product((0, 1), repeat=3):
        if not any(
            all(relation(sigma, u, z, y) for y in product((0, 1), repeat=2))
            for z in product((0, 1), repeat=3)
        ):
            return False
    return True


def extension_exists(prefix, relation):
    """exists completion sigma_suffix such that forall u exists z forall y R."""
    return any(
        good(prefix + suffix, relation)
        for suffix in product((0, 1), repeat=5 - len(prefix))
    )


def select_sigma(relation):
    prefix = ()
    queries = []
    while len(prefix) < 5:
        candidate0 = prefix + (0,)
        answer = extension_exists(candidate0, relation)
        queries.append(
            {
                "prefix0": "".join(map(str, candidate0)),
                "extension_exists": answer,
            }
        )
        prefix = candidate0 if answer else prefix + (1,)
    assert good(prefix, relation)
    return prefix, queries


def prime_annotation(sigma):
    return math.prod(p ** (bit + 1) for p, bit in zip(PRIMES, sigma))


def bitstring(bits):
    return "".join(map(str, bits))


def main():
    unique_valid = [
        s for s in product((0, 1), repeat=5) if good(s, r_unique)
    ]
    multi_valid = [
        s for s in product((0, 1), repeat=5) if good(s, r_multi)
    ]

    unique_selected, unique_queries = select_sigma(r_unique)
    multi_selected, multi_queries = select_sigma(r_multi)

    result = {
        "experiment": "PRIMEPH1",
        "alternation_prefix": "exists sigma forall u exists z forall y",
        "sigma_bits": 5,
        "u_bits": 3,
        "z_bits": 3,
        "y_bits": 2,
        "unique_valid_sigmas": [bitstring(s) for s in unique_valid],
        "unique_selected_sigma": bitstring(unique_selected),
        "unique_prefix_queries": unique_queries,
        "unique_prime_annotation": prime_annotation(unique_selected),
        "multi_valid_sigmas": [bitstring(s) for s in multi_valid],
        "multi_selected_sigma": bitstring(multi_selected),
        "multi_selected_is_lexicographically_first": multi_selected == min(NONUNIQUE),
        "multi_prefix_queries": multi_queries,
        "multi_prime_annotation": prime_annotation(multi_selected),
        "conclusion": (
            "Finite exhaustive control confirms bit-by-bit selection from an "
            "alternating extension predicate; it is not evidence that P=NP."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
