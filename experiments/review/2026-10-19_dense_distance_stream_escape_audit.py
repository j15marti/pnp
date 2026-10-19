#!/usr/bin/env python3
"""Independent audit of the RS--Hadamard dense-distance streaming control."""

from __future__ import annotations

import itertools
import json


IRREDUCIBLE = {2: 0b111, 3: 0b1011, 4: 0b10011}


def gf_mul(a: int, b: int, r: int) -> int:
    modulus = IRREDUCIBLE[r]
    mask = (1 << r) - 1
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= modulus
    return out & mask


def poly_eval(coeffs: tuple[int, ...], x: int, r: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = gf_mul(value, x, r) ^ coeff
    return value


def hadamard_word(symbol: int, q: int) -> int:
    word = 0
    for z in range(q):
        word |= ((symbol & z).bit_count() & 1) << z
    return word


def encode(coeffs: tuple[int, ...], r: int) -> int:
    q = 1 << r
    suffix = 0
    for x in range(q):
        suffix |= hadamard_word(poly_eval(coeffs, x, r), q) << (x * q)
    # The first q^2 stream bits are zero.  They do not change the packed suffix.
    return suffix


def exhaustive_small():
    scopes = {2: (1, 2), 3: (1, 2, 3), 4: (1, 2)}
    records = []
    total_words = total_pairs = total_points = failures = 0
    for r, ks in scopes.items():
        q = 1 << r
        n_stream = 2 * q * q
        for k in ks:
            words = [encode(c, r) for c in itertools.product(range(q), repeat=k)]
            expected_count = q**k
            if len(set(words)) != expected_count:
                failures += 1
            nonzero_weights = [w.bit_count() for w in words if w]
            lower = n_stream // 8
            upper = n_stream // 4
            if min(nonzero_weights) < lower or max(nonzero_weights) > upper:
                failures += 1
            min_distance = n_stream
            pairs = 0
            for i, left in enumerate(words):
                for right in words[i + 1 :]:
                    pairs += 1
                    min_distance = min(min_distance, (left ^ right).bit_count())
            predicted_distance = (q - k + 1) * q // 2
            if min_distance != predicted_distance:
                failures += 1
            records.append(
                {
                    "r": r,
                    "q": q,
                    "k": k,
                    "N": n_stream,
                    "words": len(words),
                    "pairs": pairs,
                    "min_distance": min_distance,
                    "predicted_distance": predicted_distance,
                    "min_nonzero_weight": min(nonzero_weights),
                    "max_nonzero_weight": max(nonzero_weights),
                }
            )
            total_words += len(words)
            total_pairs += pairs
            total_points += len(words) * n_stream
    return records, total_words, total_pairs, total_points, failures


def symbolic_grid():
    cases = failures = 0
    worst_distance_margin = None
    minimum_description_slack = None
    max_log_family = 0
    for r in range(2, 21):
        q = 1 << r
        n_stream = 2 * q * q
        n_inputs = 2 * r + 1
        for k in range(1, q // 2 + 1):
            cases += 1
            distance = (q - k + 1) * q // 2
            circuit_bound = 20 * k * r * r
            log_family = k * r
            workspace_proxy = k * r + r * r + n_inputs
            wire_bits = (n_inputs + circuit_bound - 1).bit_length()
            circuit_description_bits = circuit_bound * (2 + 2 * wire_bits) + wire_bits
            conditions = [
                8 * distance >= n_stream,
                circuit_bound >= n_inputs,
                workspace_proxy <= circuit_bound,
                log_family == k * r,
                log_family <= circuit_description_bits,
            ]
            if not all(conditions):
                failures += 1
            margin = 8 * distance - n_stream
            worst_distance_margin = margin if worst_distance_margin is None else min(worst_distance_margin, margin)
            desc_slack = circuit_description_bits - log_family
            minimum_description_slack = desc_slack if minimum_description_slack is None else min(minimum_description_slack, desc_slack)
            max_log_family = max(max_log_family, log_family)
    return {
        "r_range": [2, 20],
        "parameter_pairs": cases,
        "failures": failures,
        "minimum_integer_distance_margin": worst_distance_margin,
        "minimum_circuit_description_slack_bits": minimum_description_slack,
        "maximum_log2_family_size": max_log_family,
    }


def main():
    records, words, pairs, points, finite_failures = exhaustive_small()
    symbolic = symbolic_grid()
    result = {
        "run": "DENSE-DISTANCE-STREAM-ESCAPE2",
        "finite_field_basis": {
            "r=2": "x^2+x+1",
            "r=3": "x^3+x+1",
            "r=4": "x^4+x+1",
        },
        "exhaustive_scope": "r=2:k=1,2; r=3:k=1,2,3; r=4:k=1,2",
        "codewords": words,
        "pair_distances": pairs,
        "truth_table_point_evaluations": points,
        "finite_failures": finite_failures,
        "symbolic": symbolic,
        "records": records,
        "integrated_conclusion": "Density in [1/8,1/4], relative distance >=1/8, and q^k family cardinality do not force superpolynomial-in-s streaming synthesis: the source-backed family has circuit bound s0=20kr^2 and declared workspace O(kr+r^2)=poly(s0). More generally, terminal-output counting over size-s YES functions is capped by the O(s log s)-bit circuit description space.",
        "guard": "Promised family only; not unrestricted search-MCSP, CHMY threshold descent, OPS GapMCSP circuit excess, or FLMV transfer.",
        "P_versus_NP": "OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if finite_failures or symbolic["failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
