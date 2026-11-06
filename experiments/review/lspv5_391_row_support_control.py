#!/usr/bin/env python3
"""Independent symbolic support control for REFEREE391.

Enumerates every nonempty XOR sum of the four authenticated internal vertex
rows on each bridge side.  These are exactly the side-local equation blocks
classified in REFEREE390.
"""
from __future__ import annotations

import json
import resource
import time


LEFT = (
    (frozenset((1, 3, 4)), 1),
    (frozenset((2, 5, 6)), 0),
    (frozenset((3, 5, 7)), 0),
    (frozenset((4, 6, 7)), 0),
)
RIGHT = (
    (frozenset((8, 10, 11)), 0),
    (frozenset((9, 12, 13)), 0),
    (frozenset((10, 12, 14)), 0),
    (frozenset((11, 13, 14)), 0),
)


def xor_rows(rows, subset):
    support = frozenset()
    rhs = 0
    for i, (row, bit) in enumerate(rows):
        if subset >> i & 1:
            support = support.symmetric_difference(row)
            rhs ^= bit
    return support, rhs


def side_record(rows):
    equations = [xor_rows(rows, subset) for subset in range(1, 16)]
    assert len(set(equations)) == 15
    assert all(support for support, _ in equations)
    return {
        "equations": [
            {"subset": subset, "support": sorted(support), "rhs": rhs}
            for subset, (support, rhs) in zip(range(1, 16), equations)
        ],
        "support_sizes": sorted(len(support) for support, _ in equations),
        "minimum_support": min(len(support) for support, _ in equations),
        "zero_equations": sum(not support and rhs == 0 for support, rhs in equations),
        "false_equations": sum(not support and rhs == 1 for support, rhs in equations),
    }, equations


def main():
    start = time.perf_counter()
    left_record, left = side_record(LEFT)
    right_record, right = side_record(RIGHT)
    cross = [
        {
            "left_support": sorted(ls),
            "right_support": sorted(rs),
            "combined_support": sorted(ls | rs),
            "combined_size": len(ls | rs),
            "rhs": lb ^ rb,
        }
        for ls, lb in left
        for rs, rb in right
    ]
    assert all(ls.isdisjoint(rs) for ls, _ in left for rs, _ in right)
    assert min(item["combined_size"] for item in cross) == 4
    assert all(item["combined_size"] > 3 for item in cross)

    hostile = 0
    hostile += int(min(item["combined_size"] for item in cross) != 3)
    hostile += int(left_record["minimum_support"] != 1)
    hostile += int(right_record["minimum_support"] != 1)
    hostile += int(left_record["zero_equations"] != 1)
    hostile += int(right_record["false_equations"] != 1)
    assert hostile == 5

    result = {
        "run": "LSPV-5/REFEREE391 internal-row XOR support control",
        "scope": "all nonempty subsets of four authenticated internal rows per side",
        "left": left_record,
        "right": right_record,
        "cross_pairs": len(cross),
        "minimum_cross_support": min(item["combined_size"] for item in cross),
        "cross_support_at_most_three": sum(item["combined_size"] <= 3 for item in cross),
        "hostile_mutations_rejected": hostile,
        "wall_seconds": time.perf_counter() - start,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "status": "PROVED_EXACT_FINITE_ENUMERATION",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
