#!/usr/bin/env python3
"""Finite arithmetic checks for the hash-length red-team audit.

This illustrates exact bucket formulas only.  It does not establish an
asymptotic SAT result.
"""
from __future__ import annotations

import json
import math
import random


def pair_count(bucket_sizes):
    return sum(x * (x - 1) // 2 for x in bucket_sizes)


def trial(q: int, bits: int, seed: int):
    rng = random.Random(seed)
    buckets = [0] * (1 << bits)
    for _ in range(q):
        buckets[rng.randrange(1 << bits)] += 1
    return pair_count(buckets), max(buckets), sum(x > 0 for x in buckets)


rows = []
for m in range(3, 11):
    # M=2^(3m), target Q=M^(1/3)=2^m and state replay L=M^(2/3)=2^(2m).
    q = 1 << m
    state_bits = 1 << (2 * m)
    for factor in (0, 1, 2):
        h = factor * m
        B = 1 << h
        expected_pairs = q * (q - 1) / (2 * B)
        simulated = [trial(q, h, 1000 * m + factor * 100 + j)[0] for j in range(8)]
        rows.append(
            {
                "m": m,
                "M_log2": 3 * m,
                "Q": q,
                "state_replay_bits": state_bits,
                "hash_bits": h,
                "bucket_count": B,
                "expected_pair_replays": expected_pairs,
                "mean_simulated_pair_replays": sum(simulated) / len(simulated),
                "adversarial_pair_replays": q * (q - 1) // 2,
                "expected_replay_bit_work": expected_pairs * state_bits,
                "adversarial_replay_bit_work": (q * (q - 1) // 2) * state_bits,
            }
        )

checks = {
    "pair_lower_bound": [],
    "common_signature": [],
}
for q in range(2, 80):
    for B in range(1, 25):
        # Balanced buckets minimize sum choose(m_b,2).
        lo, rem = divmod(q, B)
        sizes = [lo + (i < rem) for i in range(B)]
        exact = pair_count(sizes)
        lower = (q * q / B - q) / 2
        assert exact + 1e-12 >= lower
        checks["pair_lower_bound"].append((q, B, exact, lower))

# If R class representatives are mapped by t h-bit public hashes, one joint
# signature contains at least ceil(R/2^(t h)) representatives.
for R in (64, 1024, 65536):
    for h in (1, 2, 4, 8):
        for t in (1, 2, 3, 4):
            lower = math.ceil(R / (1 << (h * t)))
            checks["common_signature"].append((R, h, t, lower))

out = {
    "status": "COMPUTATIONAL_ARITHMETIC_ONLY",
    "seed_policy": "eight deterministic seeds per row",
    "rows": rows,
    "checks": {k: len(v) for k, v in checks.items()},
    "errors": 0,
}
with open("/tmp/hash_length_audit.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print(json.dumps({k: out[k] for k in ("status", "checks", "errors")}, indent=2))
