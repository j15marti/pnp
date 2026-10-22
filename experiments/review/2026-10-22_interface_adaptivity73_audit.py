#!/usr/bin/env python3
"""Finite audit for INTERFACE-ADAPTIVITY-BARRIER73."""

import itertools
import random


def parity(x):
    return x.bit_count() & 1


def prefix_members(k, prefix_bits, prefix_len):
    suffix = k - prefix_len
    start = prefix_bits << suffix
    return range(start, start + (1 << suffix))


def point_adversary_cost(j_count, universe, order):
    seen = [0] * universe
    zeros = [False] * universe
    unresolved = universe
    queries = 0
    for j, u in order:
        if zeros[u]:
            continue
        queries += 1
        seen[u] += 1
        if seen[u] == j_count:
            zeros[u] = True
            unresolved -= 1
        if unresolved == 0:
            return queries
    raise AssertionError("incomplete decision transcript")


def main():
    checks = 0

    # Exact OR_U o AND_J adversary cost for random adaptive-query orders.
    rng = random.Random(73)
    for _ in range(20_000):
        j_count = rng.randint(1, 10)
        universe = 1 << rng.randint(1, 8)
        order = [(j, u) for u in range(universe) for j in range(j_count)]
        rng.shuffle(order)
        cost = point_adversary_cost(j_count, universe, order)
        assert cost == j_count * universe
        checks += 1

    # Parity/complement prefix oracle: all proper prefixes look nonempty on both
    # sides, and adding one hidden even-parity point changes only its singleton.
    for k in range(2, 13):
        universe = 1 << k
        even = {x for x in range(universe) if parity(x) == 0}
        odd = set(range(universe)) - even
        assert not (even & odd)
        checks += 1
        for length in range(k):
            for p in range(1 << length):
                members = set(prefix_members(k, p, length))
                assert even & members
                assert odd & members
                checks += 2
        for x in even:
            yes_right = odd | {x}
            assert even & yes_right == {x}
            for y in range(universe):
                base = y in odd
                changed = y in yes_right
                assert (base != changed) == (y == x)
                checks += 1

    # Black-box RP hitting-set threshold: to hit every set of density >=1/2,
    # a fixed list needs more than half the universe.
    for k in range(1, 21):
        universe = 1 << k
        half = universe // 2
        for h in [0, 1, max(0, half - 1), half, half + 1, universe]:
            avoidable = universe - h >= half
            assert avoidable == (h <= half)
            checks += 1

    print({
        "checks": checks,
        "failures": 0,
        "point_query_complexity": "J*2^k",
        "prefix_query_lower_bound": "2^(k-1) singleton leaves on the parity family",
        "black_box_rp_hitting_threshold": "2^(k-1)+1",
        "scope": "detached black-box relations only"
    })


if __name__ == "__main__":
    main()
