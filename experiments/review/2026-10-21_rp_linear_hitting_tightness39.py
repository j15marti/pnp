#!/usr/bin/env python3
"""Finite audit for RP-LINEAR-HITTING-TIGHTNESS39.

For x,r in F_2^n define the RP verifier

    M(x;r) = 1                         if x = 0,
             <x,r> mod 2               otherwise.

Its language is Sigma*, yet a seed list H hits every input iff span(H)=F_2^n.
The program exhausts every seed subset for n<=4 and samples larger n.
"""

from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


OUT = Path(__file__).resolve().parents[2] / "results/raw/separation/2026-10-21_1148_RP_LINEAR_HITTING_TIGHTNESS39_summary.json"


def parity(x: int) -> int:
    return x.bit_count() & 1


def accepts(x: int, r: int) -> bool:
    return x == 0 or parity(x & r) == 1


def rank_gf2(rows: list[int], n: int) -> int:
    basis = [0] * n
    rank = 0
    for value in rows:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if basis[pivot]:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                rank += 1
                break
    return rank


def hits_all(seeds: list[int], n: int) -> bool:
    return all(any(accepts(x, r) for r in seeds) for x in range(1 << n))


def accepting_count(x: int, n: int) -> int:
    return sum(accepts(x, r) for r in range(1 << n))


def audit() -> dict:
    assertions = 0
    exhaustive_seed_sets = 0
    exhaustive_input_seed_pairs = 0
    sampled_seed_lists = 0
    minima: dict[str, int] = {}

    # Every subset of the entire seed universe is feasible through n=4.
    for n in range(1, 5):
        universe = list(range(1 << n))
        min_hitting = None

        for x in universe:
            count = accepting_count(x, n)
            expected = (1 << n) if x == 0 else (1 << (n - 1))
            assert count == expected
            assertions += 1
            exhaustive_input_seed_pairs += 1 << n

        for family_mask in range(1 << len(universe)):
            seeds = [universe[i] for i in range(len(universe)) if (family_mask >> i) & 1]
            rank = rank_gf2(seeds, n)
            hit = hits_all(seeds, n)
            assert hit == (rank == n)
            assertions += 1
            exhaustive_seed_sets += 1
            if hit:
                min_hitting = len(seeds) if min_hitting is None else min(min_hitting, len(seeds))

        assert min_hitting == n
        assertions += 1
        minima[str(n)] = min_hitting

        standard_basis = [1 << i for i in range(n)]
        assert hits_all(standard_basis, n)
        assert rank_gf2(standard_basis, n) == n
        assertions += 2

    # Larger dimensions: seeded random lists and exact linear-algebra oracle.
    rng = random.Random(202610211148)
    for n in range(5, 13):
        for _ in range(5000):
            length = rng.randint(0, n + 3)
            seeds = [rng.randrange(1 << n) for _ in range(length)]
            rank = rank_gf2(seeds, n)
            hit = hits_all(seeds, n)
            assert hit == (rank == n)
            assertions += 1
            sampled_seed_lists += 1

        standard_basis = [1 << i for i in range(n)]
        assert hits_all(standard_basis, n)
        assert all(not hits_all(standard_basis[:k], n) for k in range(n))
        assertions += 2

    return {
        "run_id": "RP-LINEAR-HITTING-TIGHTNESS39",
        "timestamp_kst": "2026-10-21 11:48",
        "status": "PROVED_SCOPED_PLUS_COMPUTATIONAL_P_VS_RP_OPEN_P_VS_NP_OPEN",
        "language": "Sigma* on n-bit strings",
        "verifier": "M(x;r)=1 for x=0, otherwise inner_product_GF2(x,r)",
        "yes_density": "1 for x=0; exactly 1/2 for every nonzero x",
        "exact_theorem": "A seed list H hits every input iff span_GF2(H)=GF2^n; hence the minimum number of seeds is exactly n.",
        "advice_bits": "n seeds of n bits each, i.e. n^2 bits for this verifier",
        "deterministic_bypass": "The recognized language is Sigma*, so one unconditional accept state decides it.",
        "exhaustive_seed_sets_n_le_4": exhaustive_seed_sets,
        "exhaustive_input_seed_pairs_n_le_4": exhaustive_input_seed_pairs,
        "sampled_seed_lists_n_5_to_12": sampled_seed_lists,
        "instrumented_assertions": assertions,
        "failures": 0,
        "minimum_hitting_sizes_exhaustive": minima,
        "seed": 202610211148,
        "scope_firewall": [
            "This is an exact verifier-specific hitting-set lower bound, not a language lower bound.",
            "The verifier is uniform, uses n random bits and O(n) parity time.",
            "Linear algebra is confined to this affine acceptance family.",
            "No conclusion about P versus RP, P versus NP, ordinary KT, or unrestricted SAT time follows.",
        ],
    }


if __name__ == "__main__":
    result = audit()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
