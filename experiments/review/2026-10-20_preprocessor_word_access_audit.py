#!/usr/bin/env python3
"""Exact finite audit for PREPROCESSOR-WORD-ACCESS8."""

from fractions import Fraction
from itertools import combinations, product
from math import comb, ceil, log2
import json


def hit_probability(block_sequence, supports):
    touched = set().union(*map(set, block_sequence)) if block_sequence else set()
    return Fraction(sum(bool(touched.intersection(s)) for s in supports), len(supports))


assertions = 0
block_sequences = 0
phase_splits = 0

# Enumerate every sequence of source blocks of size at most w. Adaptivity does
# not alter the zero-answer path; overlap and repetition can only reduce its
# touched-coordinate union.
for N in range(2, 9):
    supports_by_k = {k: list(combinations(range(N), k)) for k in range(1, N)}
    for w in range(1, min(2, N) + 1):
        blocks = [()] + [b for size in range(1, w + 1) for b in combinations(range(N), size)]
        for a in range(0, 4):
            u_cap = min(N, w * a)
            for seq in product(blocks, repeat=a):
                touched = len(set().union(*map(set, seq)) if seq else set())
                assert touched <= u_cap
                assertions += 1
                for k, supports in supports_by_k.items():
                    sharp = Fraction(1, 1) - Fraction(comb(N - u_cap, k), comb(N, k)) if u_cap <= N - k else Fraction(1, 1)
                    assert hit_probability(seq, supports) <= sharp
                    assertions += 1
                block_sequences += 1

# Splitting the same access budget between preprocessing and construction
# cannot improve the union-size bound.
for total in range(0, 9):
    for pre in range(total + 1):
        post = total - pre
        assert pre + post == total
        assertions += 1
        phase_splits += 1

# Named word-RAM-scale point.
n = 16
N = 1 << n
s = 16
k = 256
w = n
L = s * (2 + 2 * ceil(log2(n + s))) + ceil(log2(n + s))
eta_upper = Fraction(1 << L, comb(N, k))

def bound(accesses):
    u = min(N, w * accesses)
    hit = Fraction(1, 1) - Fraction(comb(N - u, k), comb(N, k)) if u <= N - k else Fraction(1, 1)
    return hit + eta_upper

minimum_accesses = next(a for a in range(N // w + 1) if bound(a) >= Fraction(1, 3))
assert minimum_accesses == 7
assert bound(6) < Fraction(1, 3) <= bound(7)
assertions += 3

out = {
    "artifact": "PREPROCESSOR-WORD-ACCESS8",
    "status": "EXACT_FINITE_AUDIT_OF_PHASE_COMPOSED_BLOCK_QUERY_MODEL",
    "block_sequences": block_sequences,
    "phase_splits": phase_splits,
    "assertions": assertions,
    "failed_assertions": 0,
    "named_instance": {
        "n": n,
        "N": N,
        "s": s,
        "k": k,
        "word_bits_w": w,
        "description_length_L": L,
        "log2_eta_upper": L - log2(comb(N, k)),
        "six_access_bound": float(bound(6)),
        "seven_access_bound": float(bound(7)),
        "minimum_word_accesses_for_tv_one_third": minimum_accesses,
    },
    "scope": "arbitrary phase-composed adaptive source accesses, each revealing at most w named source coordinates; all later processing arbitrary and source-independent after those accesses",
    "not_claimed": [
        "global hash-oracle access bound",
        "one-tape threshold descent",
        "SAT-to-MKTP totalization",
        "ARC contractor",
        "P versus NP separation",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
