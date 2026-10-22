#!/usr/bin/env python3
"""Finite audit for FULL-COVER-CHILD-FIREWALL74.

The proof is elementary; this program checks the set semantics, balanced merge
tree, satisfiable tautology control, and the SOURCE-CHANNEL21 counting bound.
"""

from __future__ import annotations

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path


SEED = 740022
RNG = random.Random(SEED)
checks = 0


def check(condition: bool) -> None:
    global checks
    checks += 1
    assert condition


def allowed(universe: set[int], forbidden: set[int]) -> set[int]:
    return universe - forbidden


def merge_levels(m: int) -> list[list[set[int]]]:
    level = [{a} for a in range(m)]
    levels = [level]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(set().union(*level[i : i + 2]))
        level = nxt
        levels.append(level)
    return levels


def main() -> None:
    exhaustive_subsets = 0
    sampled_subsets = 0
    merge_nodes = 0
    source_bound_checks = 0

    # Exhaust every block subset through k=4.
    for k in range(1, 5):
        m = 1 << k
        u = set(range(m))
        check(not allowed(u, u))
        for mask in range((1 << m) - 1):
            t = {a for a in range(m) if (mask >> a) & 1}
            check(bool(allowed(u, t)))
            check(len(allowed(u, t)) == m - len(t))
            exhaustive_subsets += 1

        # Replace one forbidding block by a tautology: full control is SAT.
        for x in range(m):
            forbidden = u - {x}
            check(allowed(u, forbidden) == {x})

        # Every balanced-tree node except the root is a proper, SAT subset.
        levels = merge_levels(m)
        for level_number, level in enumerate(levels):
            for block_set in level:
                is_root = level_number == len(levels) - 1
                check((not allowed(u, block_set)) == is_root)
                if not is_root:
                    check(len(block_set) < m)
                merge_nodes += 1

    # Sample larger instances and adversarial near-full subsets.
    for k in range(5, 15):
        m = 1 << k
        u = set(range(m))
        for _ in range(250):
            omitted_count = RNG.randint(1, min(m, 64))
            omitted = set(RNG.sample(range(m), omitted_count))
            t = u - omitted
            check(allowed(u, t) == omitted)
            sampled_subsets += 1

        for level_number, level in enumerate(merge_levels(m)):
            for block_set in level:
                is_root = level_number == k
                check((len(allowed(u, block_set)) == 0) == is_root)
                merge_nodes += 1

    # SOURCE-CHANNEL21 arithmetic: success <= min(1,h*2^(q+bt-n)).
    # Verify the derived necessary inequality whenever the target is >= 1/2.
    for n in range(4, 65):
        for _ in range(300):
            q = RNG.randint(0, n + 8)
            b = RNG.randint(1, 8)
            t = RNG.randint(0, n + 2)
            h = RNG.randint(1, 1 << min(n, 12))
            log_numerator = q + b * t + (h.bit_length() - 1)
            upper = min(1.0, h * (2.0 ** min(0, q + b * t - n)))
            check(0.0 < upper <= 1.0)
            if h * (2 ** (q + b * t)) < (1 << (n - 1)):
                check(upper < 0.5)
            source_bound_checks += 1

    result = {
        "artifact": "FULL-COVER-CHILD-FIREWALL74",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "checks": checks,
        "failures": 0,
        "exhaustive_proper_subsets": exhaustive_subsets,
        "sampled_proper_subsets": sampled_subsets,
        "balanced_merge_nodes": merge_nodes,
        "source_channel_arithmetic_cases": source_bound_checks,
        "scope": "finite audit only; proofs are in the synthesis report",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/synthesis/2026-10-22_2248_FULL_COVER_CHILD_FIREWALL74.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
