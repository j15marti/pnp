#!/usr/bin/env python3
"""Exact finite audit for CONDITIONED-HARD-SPARSE-QUERY7."""

from fractions import Fraction
from itertools import combinations, product
from math import comb, ceil, log2
import json


def hit_probability(sequence, support_family):
    hits = sum(any(i in support for i in sequence) for support in support_family)
    return Fraction(hits, len(support_family))


assertions = 0
sequence_checks = 0
conditioning_checks = 0

# Every possible zero-answer query path (including repeated queries) is no
# better than q distinct probes against a uniform k-subset.
for N in range(2, 9):
    universe = range(N)
    for k in range(1, N):
        supports = list(combinations(universe, k))
        for q in range(0, min(4, N) + 1):
            sharp = Fraction(1, 1) - Fraction(comb(N - k, q), comb(N, q)) if q <= N - k else Fraction(1, 1)
            canonical = tuple(range(q))
            assert hit_probability(canonical, supports) == sharp
            assertions += 1
            for seq in product(universe, repeat=q):
                assert hit_probability(seq, supports) <= sharp
                assertions += 1
                sequence_checks += 1

# Conditioning away an arbitrary declared easy subfamily costs at most eta.
for N in range(3, 10):
    universe = range(N)
    for k in range(1, N):
        supports = list(combinations(universe, k))
        total = len(supports)
        for q in range(0, min(4, N) + 1):
            sharp = Fraction(1, 1) - Fraction(comb(N - k, q), comb(N, q)) if q <= N - k else Fraction(1, 1)
            query = tuple(range(q))
            for excluded in range(0, min(3, total - 1) + 1):
                hard = supports[excluded:]
                conditioned_hit = hit_probability(query, hard)
                eta = Fraction(excluded, total)
                assert conditioned_hit <= sharp + eta
                assertions += 1
                conditioning_checks += 1

# Reproduce REDTEAM24's named parameter point and exact necessary q.
n = 10
N = 1 << n
s = 4
k = 64
L = s * (2 + 2 * ceil(log2(n + s))) + ceil(log2(n + s))
eta_upper = Fraction(1 << L, comb(N, k))

def tv_bound(q):
    hit = Fraction(1, 1) - Fraction(comb(N - k, q), comb(N, q))
    return hit + eta_upper

necessary_q = next(q for q in range(N - k + 1) if tv_bound(q) >= Fraction(1, 3))
assert necessary_q == 7
assert tv_bound(6) < Fraction(1, 3) <= tv_bound(7)
assertions += 3

out = {
    "artifact": "CONDITIONED-HARD-SPARSE-QUERY7",
    "status": "EXACT_FINITE_AUDIT_OF_RESTRICTED_QUERY_MODEL",
    "sequence_checks": sequence_checks,
    "conditioning_checks": conditioning_checks,
    "assertions": assertions,
    "failed_assertions": 0,
    "named_instance": {
        "n": n,
        "N": N,
        "s": s,
        "k": k,
        "description_length_L": L,
        "log2_eta_upper": log2(float(eta_upper)),
        "q6_bound": float(tv_bound(6)),
        "q7_bound": float(tv_bound(7)),
        "necessary_q_for_tv_one_third": necessary_q,
    },
    "scope": "zero source versus uniform k-sparse sources conditioned to circuit complexity greater than s; arbitrary label-independent randomness and at most q adaptive source-bit probes",
    "not_claimed": [
        "original CHMY generator transport",
        "ordinary SAT-to-MKTP reduction",
        "arbitrary-machine SAT time lower bound",
        "P versus NP separation",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
