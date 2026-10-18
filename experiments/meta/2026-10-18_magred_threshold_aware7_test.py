#!/usr/bin/env python3
"""Exact finite controls for the k-wise source-YES obstruction.

These tests verify finite-field and combinatorial identities only.
They do not establish any unrestricted MCSP time lower bound.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

MODULUS = {3: 0b1011, 4: 0b10011}

def mul(x, y, n):
    poly = MODULUS[n]
    mask = (1 << n) - 1
    out = 0
    for _ in range(n):
        if y & 1:
            out ^= x
        y >>= 1
        x <<= 1
        if x & (1 << n):
            x ^= poly
    return out & mask

def trace(x, n):
    out, y = 0, x
    for _ in range(n):
        out ^= y
        y = mul(y, y, n)
    assert out in (0, 1), (x, n, out)
    return out

def eval_poly(coeffs, x, n):
    y = 0
    for a in reversed(coeffs):
        y = mul(y, x, n) ^ a
    return trace(y, n)

def run(n, k):
    N = 1 << n
    # Cover every polynomial coefficient vector in the family.
    polys = list(product(range(N), repeat=k))
    truth = [tuple(eval_poly(coeffs, x, n) for x in range(N)) for coeffs in polys]
    tests = 0
    pattern_tests = 0
    for q in range(1, k + 1):
        for addresses in combinations(range(N), q):
            counts = Counter(tuple(y[a] for a in addresses) for y in truth)
            expected = N**k // 2**q
            for pattern in product((0, 1), repeat=q):
                assert counts[pattern] == expected, (n, k, q, addresses, pattern, counts[pattern], expected)
                pattern_tests += 1
            tests += 1
    # Adaptive choices: all queried addresses distinct. The transcript bits
    # are uniform as a consequence of k-wise independence.
    assert k >= 3
    def adaptive_transcript(y):
        first = 0
        b0 = y[first]
        second = 1 if b0 == 0 else 2
        b1 = y[second]
        third = 3 + b0 * 2 + b1
        assert len({first, second, third}) == 3
        return (b0, b1, y[third])
    adaptive = Counter(adaptive_transcript(y) for y in truth)
    adaptive_expected = N**k // 8
    for pattern in product((0, 1), repeat=3):
        assert adaptive[pattern] == adaptive_expected
    # 'Constant only' toy target: exactly 2 of the 8 three-bit label
    # patterns extend to a constant function; the other 6 do not.
    const_compatible = sum(1 for y in truth if y[0] == y[1] == y[2])
    assert const_compatible * 4 == len(truth)
    return {
      'field_bits': n, 'N': N, 'k': k, 'polynomial_vectors': len(polys),
      'coordinate_subsets_tested': tests,
      'uniform_label_patterns_checked': pattern_tests,
      'adaptive_transcript_pattern_counts': {''.join(map(str, a)): adaptive[a] for a in sorted(adaptive)},
      'constant_only_three_sample_yes_rate': f'{const_compatible}/{len(truth)}',
      'status': 'pass',
    }

out = {'theorem': 'MAGRED-KWISE-YESBUDGET7', 'method': 'exhaustive finite field polynomial coefficients and distinct-address subsets',
       'results': [run(3, 3), run(4, 3)], 'note': 'Finite controls only. Standard circuit-size upper bound proven separately.'}
path = Path('/mnt/data/magred_threshold_aware7_results.json')
path.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
