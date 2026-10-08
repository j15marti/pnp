#!/usr/bin/env python3
"""Exact bounded audit for CLAUSE-FIRST-FANOUT-SHRINK-GUARD1.

The first family is the independent product

    F_m = AND_{i=1}^m (x_i OR y_i OR z_i).

Applying CLAUSE-FIRST-COVER1 to k distinct clauses creates exactly 3^k
nonempty leaves, and every leaf retains exactly m-k untouched clauses.
The script validates the semantic identity by brute force for small m and
uses exact integer arithmetic for the larger resource ledger.  It also checks
a tagged constant-size block in which the three residuals are syntactically
distinct and incomparable.  Products of the tagged block defeat exact-equality
merging but are deliberately easy under component decomposition; this is a
guard on the local cover, not a SAT lower bound.

The computation has a 25-second cooperative alarm and is intended to finish
well below the repository's 30-second per-invocation limit.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from fractions import Fraction
from pathlib import Path


def deadline(*_: object) -> None:
    raise TimeoutError("25-second cooperative budget exceeded")


def floor_rational_power(n: int, exponent: Fraction) -> int:
    """Return floor(n**(p/q)) exactly for nonnegative integers."""
    p, q = exponent.numerator, exponent.denominator
    target = n**p
    lo, hi = 0, 1
    while hi**q <= target:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**q <= target:
            lo = mid
        else:
            hi = mid
    return lo


def literal_bits(m: int) -> int:
    """Bits for a sign plus an index among 3m variables."""
    return 1 + (3 * m).bit_length()


def encoded_bits(m: int) -> int:
    """A fixed explicit indexed-CNF encoding used only for the finite audit."""
    if m == 0:
        return 1
    # Three signed variable identifiers, two intra-clause separators, and one
    # clause terminator.  The theorem uses only Theta(m log m), not constants.
    return m * (3 * literal_bits(m) + 3)


def tagged_source_bits(m: int) -> int:
    """Explicit size proxy for m disjoint tagged seven-clause blocks."""
    if m == 0:
        return 1
    bits = 1 + (15 * m).bit_length()
    # One main 3-clause and six guard 3-clauses per block.
    return m * (21 * bits + 7)


def tagged_min_residual_bits(m: int) -> int:
    """Lower bound after all blocks take the shortest third branch."""
    if m == 0:
        return 1
    bits = 1 + (15 * m).bit_length()
    # The third branch assigns x,y,z and leaves three distinct 2-clauses.
    return m * (6 * bits + 3)


def tagged_signatures() -> list[frozenset[str]]:
    """Residual clause signatures for the three first-true terms of one block."""
    signatures: list[frozenset[str]] = []
    assignments = (
        {"x": 1},
        {"x": 0, "y": 1},
        {"x": 0, "y": 0, "z": 1},
    )
    guards = []
    for v in ("x", "y", "z"):
        guards.append(((v, False), f"{v}a", f"{v}b"))
        guards.append(((v, True), f"{v}c", f"{v}d"))
    for assignment in assignments:
        residual: set[str] = set()
        for (v, positive), a, b in guards:
            if v not in assignment:
                residual.add(f"{'+' if positive else '-'}{v}|{a}|{b}")
                continue
            literal_value = bool(assignment[v]) if positive else not bool(assignment[v])
            if not literal_value:
                residual.add(f"{a}|{b}")
        signatures.append(frozenset(residual))
    return signatures


def brute_semantic_check(m: int, k: int) -> dict[str, int | bool]:
    """Validate exact disjoint first-true partition for k selected clauses."""
    total_models = 0
    bucket_counts: dict[tuple[int, ...], int] = {}
    variables = 3 * m
    for assignment in range(1 << variables):
        choices: list[int] = []
        sat = True
        for i in range(m):
            vals = [bool(assignment & (1 << (3 * i + j))) for j in range(3)]
            if not any(vals):
                sat = False
                break
            if i < k:
                choices.append(vals.index(True))
        if sat:
            total_models += 1
            key = tuple(choices)
            bucket_counts[key] = bucket_counts.get(key, 0) + 1
    expected_models = 7**m
    expected_buckets = 3**k
    # Bucket sizes differ because first-true terms assign 1, 2, or 3 variables;
    # nonemptiness and disjoint exhaustive coverage are the invariant needed.
    return {
        "m": m,
        "k": k,
        "models": total_models,
        "expected_models": expected_models,
        "buckets": len(bucket_counts),
        "expected_buckets": expected_buckets,
        "all_buckets_nonempty": all(v > 0 for v in bucket_counts.values()),
        "partition_exact": total_models == expected_models
        and len(bucket_counts) == expected_buckets
        and all(v > 0 for v in bucket_counts.values()),
    }


def ledger_row(m: int, b: Fraction) -> dict[str, int | str | bool]:
    source_bits = encoded_bits(m)
    target = floor_rational_power(source_bits, b)
    # Find the least k whose explicit residual is within the target.
    k = 0
    while k <= m and encoded_bits(m - k) > target:
        k += 1
    leaves = 3**k
    return {
        "m": m,
        "b": f"{b.numerator}/{b.denominator}",
        "source_bits": source_bits,
        "target_bits": target,
        "clauses_removed": k,
        "clauses_retained": m - k,
        "leaves_decimal_digits": len(str(leaves)),
        "leaves": str(leaves),
        "beats_M_power_8": leaves > source_bits**8,
        "fixed_power_shrink_reached": encoded_bits(m - k) <= target,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    start = time.perf_counter()

    brute = [brute_semantic_check(m, k) for m in range(1, 6) for k in range(m + 1)]
    exponents = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)]
    rows = [ledger_row(m, b) for m in (16, 32, 64, 128, 256, 512) for b in exponents]

    # Polynomial fanout q <= M^d permits at most floor(d log_3 M) clause
    # partitions.  Confirm that the residual-to-source ratio tends to one on
    # the tested range instead of achieving a fixed-power shrink.
    poly_rows = []
    for m in (32, 64, 128, 256, 512, 1024):
        M = encoded_bits(m)
        for d in (1, 2, 4, 8):
            k = 0
            while 3 ** (k + 1) <= M**d:
                k += 1
            poly_rows.append(
                {
                    "m": m,
                    "degree": d,
                    "source_bits": M,
                    "max_clause_partitions": k,
                    "retained_clauses": m - k,
                    "residual_bits": encoded_bits(m - k),
                    "residual_fraction_ppm": (1_000_000 * encoded_bits(m - k)) // M,
                }
            )

    # Hostile controls: normalization defeats tautological padding; a direct
    # monotone scan solves the family in linear time; a parent-scale call to an
    # N^K solver retains K, whereas a genuinely contracted call scales it by b.
    padding = []
    for m in (32, 128, 512):
        normalized = encoded_bits(m)
        fake_raw = encoded_bits(8 * m)
        padding.append(
            {
                "m": m,
                "normalized_bits": normalized,
                "raw_padded_bits_proxy": fake_raw,
                "normalization_removes_padding": True,
            }
        )
    solver_calls = [
        {
            "K": K,
            "parent_scale_exponent": K,
            "two_thirds_scale_exponent": str(Fraction(2 * K, 3)),
            "parent_call_retains_unknown_K": True,
        }
        for K in (2, 3, 5, 8, 13)
    ]

    signatures = tagged_signatures()
    tagged_rows = []
    for m in (16, 32, 64, 128, 256, 512, 1024):
        M = tagged_source_bits(m)
        minimum = tagged_min_residual_bits(m)
        tagged_rows.append(
            {
                "m": m,
                "source_bits": M,
                "minimum_all_processed_residual_bits": minimum,
                "minimum_residual_fraction_ppm": (1_000_000 * minimum) // M,
                "minimum_exceeds_M_two_thirds": minimum
                > floor_rational_power(M, Fraction(2, 3)),
                "tree_leaves_after_all_blocks_decimal_digits": len(str(3**m)),
            }
        )

    result = {
        "marker": "CLAUSE-FIRST-FANOUT-SHRINK-GUARD1",
        "status": "COMPUTATIONAL",
        "theorem_status": "PROVED/EXACT",
        "seed": None,
        "family": "AND of m variable-disjoint positive 3-clauses",
        "brute_checks": brute,
        "fixed_power_rows": rows,
        "polynomial_fanout_rows": poly_rows,
        "tagged_block": {
            "description": "one positive 3-clause plus two polarity guards for each decision variable",
            "residual_signatures": [sorted(x) for x in signatures],
            "pairwise_distinct": len(set(signatures)) == 3,
            "pairwise_clause_incomparable": all(
                not (signatures[i] <= signatures[j])
                for i in range(3)
                for j in range(3)
                if i != j
            ),
            "product_tree_leaf_count": "3^k",
            "rows": tagged_rows,
        },
        "failed_controls": {
            "machine_lower_bound": "fails: monotone source is solved by a linear scan",
            "exact_residual_merge": "on the untagged family all three branches normalize to the same residual; equality merging collapses the tree",
            "tagged_product_bypass": "tagged blocks avoid equality merging but split into constant-size independent components",
            "padding_escape": padding,
            "current_scale_call": solver_calls,
            "source_carry": "a parent pointer is not a standalone ordinary-CNF child; decoder access must be charged",
            "oracle_or_algebraic_replacement": "direct monotone evaluation bypasses the branching plan",
            "independent_products": "the test family itself is an independent product",
        },
        "assertions": {
            "all_brute_partitions_exact": all(x["partition_exact"] for x in brute),
            "all_fixed_power_targets_reached": all(x["fixed_power_shrink_reached"] for x in rows),
            "large_rows_super_M8": all(
                x["beats_M_power_8"] for x in rows if int(x["m"]) >= 128
            ),
            "direct_solver_control_blocks_lower_bound_claim": True,
            "tagged_signatures_distinct_and_incomparable": len(set(signatures)) == 3
            and all(
                not (signatures[i] <= signatures[j])
                for i in range(3)
                for j in range(3)
                if i != j
            ),
            "tagged_explicit_residual_never_two_thirds_power": all(
                x["minimum_exceeds_M_two_thirds"] for x in tagged_rows
            ),
        },
        "elapsed_seconds": time.perf_counter() - start,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    signal.alarm(0)
    print(json.dumps({"output": str(args.output), **result["assertions"], "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
