#!/usr/bin/env python3
"""Finite controls for RP-HITTING-QUANTIFIER-FIREWALL36.

This checks finite acceptance matrices only.  The asymptotic theorem is proved
separately by averaging/greedy halving.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
from pathlib import Path


OUT = Path("results/raw/separation/2026-10-21_0848_RP_HITTING_QUANTIFIER_FIREWALL36_summary.json")
checks = 0


def require(condition: bool) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError("finite RP hitting-set audit failed")


def greedy_hitting(rows: tuple[int, ...], q: int) -> tuple[int, ...]:
    remaining = set(rows)
    chosen: list[int] = []
    while remaining:
        column = max(range(q), key=lambda j: sum((row >> j) & 1 for row in remaining))
        chosen.append(column)
        remaining = {row for row in remaining if not ((row >> column) & 1)}
    return tuple(chosen)


def hits(rows: tuple[int, ...], chosen: tuple[int, ...]) -> bool:
    mask = sum(1 << j for j in chosen)
    return all(row & mask for row in rows)


def minimum_hitting_size(rows: tuple[int, ...], q: int) -> int:
    for size in range(q + 1):
        for chosen in itertools.combinations(range(q), size):
            if hits(rows, chosen):
                return size
    raise AssertionError("unreachable")


def main() -> None:
    exhaustive_families = 0
    random_families = 0
    exact_minima = 0
    public_list_diagonals = 0

    # Exhaust every nonempty family of dense rows for q <= 4.
    for q in (2, 4):
        dense = tuple(mask for mask in range(1 << q) if mask.bit_count() * 2 >= q)
        for family_mask in range(1, 1 << len(dense)):
            rows = tuple(dense[i] for i in range(len(dense)) if (family_mask >> i) & 1)
            chosen = greedy_hitting(rows, q)
            require(hits(rows, chosen))
            # Greedy halving gives floor(log2 m)+1, hence <= ceil(log2 m)+1.
            require(len(chosen) <= (len(rows).bit_length()))
            optimum = minimum_hitting_size(rows, q)
            exact_minima += 1
            require(optimum <= len(chosen))
            exhaustive_families += 1

    # Deterministic hostile sampling for q=8, including repeated and complementary rows.
    rng = random.Random(202610210848)
    dense8 = tuple(mask for mask in range(256) if mask.bit_count() >= 4)
    for m in range(1, 65):
        for _ in range(512):
            rows = tuple(rng.choice(dense8) for _ in range(m))
            chosen = greedy_hitting(rows, 8)
            require(hits(rows, chosen))
            require(len(chosen) <= m.bit_length())
            random_families += 1

    # A uniformly generated public list H of at most half the seeds is defeated by
    # the RP verifier accepting exactly the complement.  The underlying language is
    # Sigma*, so this is a simulator barrier, not a language lower bound.
    for q in (2, 4, 8, 16):
        universe = set(range(q))
        for size in range(q // 2 + 1):
            for H in itertools.combinations(range(q), size):
                accepting = universe.difference(H)
                require(len(accepting) * 2 >= q)
                require(all(seed not in accepting for seed in H))
                public_list_diagonals += 1

    # Exact enumeration: OR over all 2^r branches agrees with existential acceptance.
    enumeration_tables = 0
    for r in range(0, 5):
        q = 1 << r
        for accepting_mask in range(1 << q):
            enumerated = any((accepting_mask >> seed) & 1 for seed in range(q))
            require(enumerated == (accepting_mask != 0))
            enumeration_tables += 1

    payload = {
        "artifact": "RP-HITTING-QUANTIFIER-FIREWALL36",
        "timestamp_asia_seoul": "2026-10-21 08:48",
        "status_p_vs_rp": "OPEN",
        "status_p_vs_np": "OPEN",
        "scope": "finite acceptance-matrix controls; not a complexity-class separation",
        "exhaustive_families": exhaustive_families,
        "random_families": random_families,
        "exact_minima": exact_minima,
        "public_list_diagonals": public_list_diagonals,
        "enumeration_tables": enumeration_tables,
        "assertions": checks,
        "failures": 0,
        "seed": 202610210848,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
