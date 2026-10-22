#!/usr/bin/env python3
"""Finite audit for TWO-LABEL-CERTIFICATE-ENVELOPE76."""

from __future__ import annotations

import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path


SEED = 760023
rng = random.Random(SEED)
checks = 0


def check(value: bool) -> None:
    global checks
    checks += 1
    assert value


def transcript(bits: list[int], queried: list[int]) -> tuple[int, ...]:
    return tuple(bits[i] for i in queried)


def main() -> None:
    exhaustive_masks = 0
    random_schedules = 0
    capacity_cases = 0
    union_bound_cases = 0

    # Exact deterministic validation of AND_L needs every location on 1^L.
    for length in range(1, 17):
        ones = [1] * length
        for mask in range((1 << length) - 1):
            queried = [i for i in range(length) if (mask >> i) & 1]
            skipped = next(i for i in range(length) if not ((mask >> i) & 1))
            bad = ones.copy()
            bad[skipped] = 0
            check(transcript(ones, queried) == transcript(bad, queried))
            check(all(ones) and not all(bad))
            exhaustive_masks += 1

    for _ in range(20_000):
        length = rng.randint(2, 4096)
        query_count = rng.randint(0, length - 1)
        queried = sorted(rng.sample(range(length), query_count))
        queried_set = set(queried)
        skipped = next(i for i in range(length) if i not in queried_set)
        ones = [1] * length
        bad = ones.copy()
        bad[skipped] = 0
        check(transcript(ones, queried) == transcript(bad, queried))
        random_schedules += 1

    # Explicit child capacity: Q=N^alpha children of N^beta bits emit at
    # most N^(alpha+beta) bits, apart from subpolynomial factors.
    points = [(0.6, 0.5), (0.595, 0.505)]
    for alpha, beta in points:
        check(abs(alpha + beta - 1.1) < 1e-12)
        for c_milli in range(1000, 10001):
            c = c_milli / 1000
            fits = c <= alpha + beta + 1e-12
            check(fits == (c <= 1.1 + 1e-12))
            capacity_cases += 1

    # Fixed-size circuit families: if at most M=2^ell acceptance sets each
    # have density >=1/2, h=ell+t random tapes miss some set with union-bound
    # probability at most 2^-t.  This is nonuniform existence, not a uniform
    # construction across unbounded size exponents.
    for ell in range(1, 301):
        for slack in range(1, 21):
            h = ell + slack
            log2_union_bound = ell - h
            check(log2_union_bound == -slack)
            check(2.0**log2_union_bound <= 0.5)
            union_bound_cases += 1

    result = {
        "artifact": "TWO-LABEL-CERTIFICATE-ENVELOPE76",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "checks": checks,
        "failures": 0,
        "exhaustive_proper_query_masks": exhaustive_masks,
        "random_proper_query_schedules": random_schedules,
        "capacity_cases": capacity_cases,
        "nonuniform_union_bound_cases": union_bound_cases,
        "scope": "finite audit of proved accounting/query identities only",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/synthesis/2026-10-23_0048_TWO_LABEL_CERTIFICATE_ENVELOPE76.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
