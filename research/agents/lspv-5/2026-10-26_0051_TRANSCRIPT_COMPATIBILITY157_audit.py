#!/usr/bin/env python3
"""Exact finite audit for TRANSCRIPT_COMPATIBILITY157.

Builds the binary simplex/Hadamard evaluation image
    y_v = <v,z> mod 2, for every nonzero v in F_2^r.
Every one- and two-coordinate projection is full, but the global image has
only 2^r=k+1 points rather than 2^k.  Also checks the parity-query control.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def dot2(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b)) & 1


def simplex_image(r: int) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    seeds = list(itertools.product((0, 1), repeat=r))
    forms = [v for v in seeds if any(v)]
    image = [tuple(dot2(v, z) for v in forms) for z in seeds]
    return forms, image


def parity(bits: tuple[int, ...]) -> int:
    return sum(bits) & 1


def main() -> None:
    rows = []
    assertions = 0
    for r in range(2, 9):
        forms, image = simplex_image(r)
        k = len(forms)
        assert k == 2**r - 1
        assertions += 1
        assert len(set(image)) == 2**r
        assertions += 1

        singleton_full = True
        for i in range(k):
            support = {y[i] for y in image}
            singleton_full &= support == {0, 1}
            assertions += 1

        pairwise_full = True
        pair_count_uniform = True
        for i in range(k):
            for j in range(i + 1, k):
                counts = {(a, b): 0 for a in (0, 1) for b in (0, 1)}
                for y in image:
                    counts[(y[i], y[j])] += 1
                pairwise_full &= set(q for q, n in counts.items() if n) == set(counts)
                pair_count_uniform &= set(counts.values()) == {2 ** (r - 2)}
                assertions += 2

        assert singleton_full and pairwise_full and pair_count_uniform
        assertions += 3
        local_log_support_sum = k
        global_log_image = r
        deficit = local_log_support_sum - global_log_image
        assert deficit == k - r
        assertions += 1
        rows.append(
            {
                "r": r,
                "k": k,
                "local_product_support": 2**k,
                "global_image_size": 2**r,
                "global_image_equals_k_plus_one": 2**r == k + 1,
                "compatibility_deficit_bits": deficit,
                "all_singletons_full": singleton_full,
                "all_pairs_full_and_uniform": pairwise_full and pair_count_uniform,
            }
        )

    # Exact sensitivity/query control for parity on p bits.
    parity_rows = []
    for p in range(2, 13):
        inputs = list(itertools.product((0, 1), repeat=p))
        all_sensitive = True
        for x in inputs:
            fx = parity(x)
            for i in range(p):
                y = list(x)
                y[i] ^= 1
                all_sensitive &= parity(tuple(y)) != fx
                assertions += 1
        assert all_sensitive
        parity_rows.append(
            {
                "p": p,
                "inputs": 2**p,
                "sensitivity_each_input": p,
                "final_labels": 2,
                "minimum_exact_initial_bit_probes": p,
            }
        )

    result = {
        "marker": "TRANSCRIPT_COMPATIBILITY157",
        "assertions": assertions,
        "failures": 0,
        "simplex_rows": rows,
        "parity_rows": parity_rows,
        "r3_image": ["".join(map(str, y)) for y in simplex_image(3)[1]],
        "interpretation": (
            "Two final labels do not cap query transcripts: sensitivity can force reads. "
            "Conversely, full singleton and pair projections do not make channels independent: "
            "the simplex image has only k+1 global states although the local product has 2^k."
        ),
    }
    out = Path(__file__).with_name(
        "2026-10-26_0051_TRANSCRIPT_COMPATIBILITY157_results.json"
    )
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
