#!/usr/bin/env python3
"""Finite checks for LSPV-5/468 count-once history lower bound.

This is an independent mathematical experiment, not the historical
R_mix341 checker.  It checks the elementary distinguishing argument and
enumerates every quotient partition for up to three paid origins.
"""

from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path


def validate_weights(weights: list[int]) -> None:
    if not weights:
        raise ValueError("at least one origin is required")
    if len(set(range(len(weights)))) != len(weights):
        raise ValueError("duplicate origin identifier")
    if any((not isinstance(w, int)) or w <= 0 for w in weights):
        raise ValueError("every origin weight must be a positive integer")


def delta(state: int, origin: int, weights: list[int]) -> int:
    if origin < 0 or origin >= len(weights):
        raise ValueError("origin out of range")
    return 0 if state & (1 << origin) else weights[origin]


def set_partitions(size: int):
    """Yield all set partitions as restricted-growth block-number tuples."""
    if size <= 0:
        yield ()
        return
    labels = [0] * size

    def visit(pos: int, maximum: int):
        if pos == size:
            yield tuple(labels)
            return
        for label in range(maximum + 2):
            labels[pos] = label
            yield from visit(pos + 1, max(maximum, label))

    yield from visit(1, 0)


def blocks(labels: tuple[int, ...]) -> list[list[int]]:
    result = [[] for _ in range(max(labels) + 1)]
    for state, label in enumerate(labels):
        result[label].append(state)
    return result


def exact_charge_partition(labels: tuple[int, ...], weights: list[int]) -> bool:
    for block in blocks(labels):
        for origin in range(len(weights)):
            charges = {delta(state, origin, weights) for state in block}
            if len(charges) != 1:
                return False
    return True


def exact_markov_partition(labels: tuple[int, ...], weights: list[int]) -> bool:
    if not exact_charge_partition(labels, weights):
        return False
    for block in blocks(labels):
        for origin in range(len(weights)):
            successors = {labels[state | (1 << origin)] for state in block}
            if len(successors) != 1:
                return False
    return True


def may_charge(block: list[int], origin: int, weights: list[int]) -> int:
    """Greatest lower charge safe for every concrete history in block."""
    return min(delta(state, origin, weights) for state in block)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-pair-origins", type=int, default=10)
    parser.add_argument("--max-join-origins", type=int, default=8)
    args = parser.parse_args()
    started = time.perf_counter()

    pair_checks = 0
    for n in range(1, args.max_pair_origins + 1):
        weights = list(range(1, n + 1))
        validate_weights(weights)
        for left in range(1 << n):
            for right in range(left + 1, 1 << n):
                diff = left ^ right
                origin = (diff & -diff).bit_length() - 1
                assert delta(left, origin, weights) != delta(right, origin, weights)
                pair_checks += 1

    partition_stats = []
    total_partitions = 0
    total_exact_charge = 0
    total_exact_markov = 0
    total_safe_may_checks = 0
    for n in range(1, 4):
        weights = list(range(1, n + 1))
        stats = {"origins": n, "partitions": 0, "exact_charge": 0,
                 "exact_markov": 0, "safe_may_checks": 0}
        for labels in set_partitions(1 << n):
            stats["partitions"] += 1
            stats["exact_charge"] += int(exact_charge_partition(labels, weights))
            stats["exact_markov"] += int(exact_markov_partition(labels, weights))
            for block in blocks(labels):
                for origin in range(n):
                    charge = may_charge(block, origin, weights)
                    assert all(charge <= delta(s, origin, weights) for s in block)
                    stats["safe_may_checks"] += len(block)
        assert stats["exact_charge"] == 1
        assert stats["exact_markov"] == 1
        partition_stats.append(stats)
        total_partitions += stats["partitions"]
        total_exact_charge += stats["exact_charge"]
        total_exact_markov += stats["exact_markov"]
        total_safe_may_checks += stats["safe_may_checks"]

    join_checks = 0
    for n in range(1, args.max_join_origins + 1):
        weights = list(range(1, n + 1))
        for left in range(1 << n):
            for right in range(1 << n):
                joined = left | right
                for origin in range(n):
                    expected = 0 if ((left | right) & (1 << origin)) else weights[origin]
                    assert delta(joined, origin, weights) == expected
                    join_checks += 1

    lost_charge_controls = []
    for n in range(1, args.max_pair_origins + 1):
        weights = list(range(1, n + 1))
        all_histories = list(range(1 << n))
        charges = [may_charge(all_histories, i, weights) for i in range(n)]
        assert charges == [0] * n
        lost_charge_controls.append(
            {"origins": n, "one_block_may_charges": charges,
             "concrete_all_origins_cost": sum(weights)}
        )

    malformed_rejections = 0
    for bad in ([], [0], [-1], [1, 0], [1, -2]):
        try:
            validate_weights(bad)
        except ValueError:
            malformed_rejections += 1
        else:
            raise AssertionError(f"malformed weights accepted: {bad}")
    try:
        delta(0, 1, [1])
    except ValueError:
        malformed_rejections += 1
    else:
        raise AssertionError("out-of-range origin accepted")

    elapsed = time.perf_counter() - started
    payload = {
        "node": "P2-L5-468",
        "status": "PASS",
        "scope": "declared count-once history transition system; not R_mix341 checker",
        "theorem": "positive-weight exact deterministic charge abstraction has at least 2^n states",
        "pair_checks": pair_checks,
        "partition_stats": partition_stats,
        "total_partitions": total_partitions,
        "total_exact_charge_partitions": total_exact_charge,
        "total_exact_markov_partitions": total_exact_markov,
        "safe_may_inequality_checks": total_safe_may_checks,
        "join_checks": join_checks,
        "lost_charge_controls": lost_charge_controls,
        "malformed_rejections": malformed_rejections,
        "elapsed_seconds": round(elapsed, 6),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
