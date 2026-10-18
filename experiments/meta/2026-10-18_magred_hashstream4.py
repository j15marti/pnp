#!/usr/bin/env python3
"""MAGRED-HASHSTREAM4 deterministic exhaustive finite-rank audit.
Pure Python 3, no dependencies or randomness. All parameters fixed and public.
Checks rank of first/last b powers of alpha for every alpha in GF(2^b),
b=3..8; all 2^b binary prefixes for one full-degree alpha per field.
These are finite checks of the independent symbolic lemma, NOT a P != NP test.
"""
import json
from collections import Counter

POLYS = {
    3: 0b1011,      # x^3+x+1
    4: 0b10011,     # x^4+x+1
    5: 0b100101,    # x^5+x^2+1
    6: 0b1000011,   # x^6+x+1
    7: 0b10000011,  # x^7+x+1
    8: 0x11d,       # x^8+x^4+x^3+x^2+1
}

def gf_mul(a, b, bits, irreducible):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << bits):
            a ^= irreducible
    return out & ((1 << bits) - 1)

def binary_rank(columns, bits):
    pivots = [0] * bits
    rank = 0
    for col in columns:
        v = col
        while v:
            pivot = v.bit_length() - 1
            if pivots[pivot]:
                v ^= pivots[pivot]
            else:
                pivots[pivot] = v
                rank += 1
                break
    return rank

def powers(alpha, N, bits, poly):
    v = 1
    result = []
    for _ in range(N):
        result.append(v)
        v = gf_mul(v, alpha, bits, poly)
    return result

def main():
    results = []
    basis_checks = 0
    dependency_checks = 0
    for bits, poly in POLYS.items():
        N = 4 * bits
        histogram = Counter()
        full_degree = []
        for alpha in range(1 << bits):
            vals = powers(alpha, N, bits, poly)
            first = binary_rank(vals[:bits], bits)
            last = binary_rank(vals[-bits:], bits)
            histogram[first] += 1
            if alpha != 0:
                assert first == last, (bits, alpha, first, last)
            else:
                assert last == 0
            if first == bits:
                assert last == bits
                full_degree.append(alpha)
                basis_checks += 2
                for coord in range(bits):
                    # Last b source positions can change this output coordinate.
                    assert any((v >> coord) & 1 for v in vals[-bits:])
                    dependency_checks += 1
        assert full_degree
        witness_alpha = full_degree[0]
        first_powers = powers(witness_alpha, bits, bits, poly)
        image = set()
        for prefix in range(1 << bits):
            fingerprint = 0
            for i, val in enumerate(first_powers):
                if prefix & (1 << i):
                    fingerprint ^= val
            image.add(fingerprint)
        assert len(image) == (1 << bits)
        results.append({
            "field_bits": bits,
            "source_bits": N,
            "total_seeds": 1 << bits,
            "full_degree_seeds": len(full_degree),
            "first_last_basis_rank": bits,
            "full_rank_prefix_image_size": len(image),
            "example_full_degree_seed": witness_alpha,
            "rank_histogram": {str(k): v for k,v in sorted(histogram.items())},
        })
    print(json.dumps({
        "run": "MAGRED-HASHSTREAM4",
        "date": "2026-10-18",
        "mode": "EXHAUSTIVE_FINITE",
        "random_seed": None,
        "number_of_seed_cases": sum(1 << b for b in POLYS),
        "basis_checks": basis_checks,
        "output_dependency_checks": dependency_checks,
        "results": results,
        "meaning": "Checks small-field linear ranks only, not a general time lower bound.",
    }, indent=2))

if __name__ == "__main__":
    main()
