#!/usr/bin/env python3
"""Exact finite audit for RP-DENSITY-HITTING-TRADEOFF38.

For a universe of q random tapes and a family of m accepting sets, each of
size at least a, greedy set cover leaves at most m((q-a)/q)^t rows after t
seeds.  The strict integer certificate is m(q-a)^t < q^t.
"""

from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


OUT = Path(__file__).resolve().parents[2] / "results/raw/separation/2026-10-21_1048_RP_DENSITY_HITTING_TRADEOFF38_summary.json"


def certified_length(m: int, q: int, a: int) -> int:
    t = 0
    left, right = m, 1
    while left >= right:
        t += 1
        left *= q - a
        right *= q
    return t


def greedy_cover(rows: list[int], q: int) -> list[int]:
    remaining = rows[:]
    chosen: list[int] = []
    while remaining:
        counts = [sum((row >> seed) & 1 for row in remaining) for seed in range(q)]
        seed = max(range(q), key=lambda x: (counts[x], -x))
        assert counts[seed] > 0
        chosen.append(seed)
        remaining = [row for row in remaining if not ((row >> seed) & 1)]
    return chosen


def audit() -> dict:
    assertions = 0
    exhaustive_families = 0
    sampled_families = 0
    max_slack = 0
    by_density: dict[str, dict[str, int]] = {}

    q = 4
    for a in (1, 2, 3):
        valid = [mask for mask in range(1, 1 << q) if mask.bit_count() >= a]
        local = 0
        for family_mask in range(1, 1 << len(valid)):
            rows = [valid[i] for i in range(len(valid)) if (family_mask >> i) & 1]
            m = len(rows)
            t = certified_length(m, q, a)
            chosen = greedy_cover(rows, q)
            assert len(chosen) <= t
            assertions += 1
            assert m * (q - a) ** t < q**t
            assertions += 1
            if t:
                assert m * (q - a) ** (t - 1) >= q ** (t - 1)
                assertions += 1
            max_slack = max(max_slack, t - len(chosen))
            local += 1
        exhaustive_families += local
        by_density[f"{a}/{q}"] = {"valid_rows": len(valid), "families": local}

    rng = random.Random(202610211048)
    q = 8
    for a in (1, 2, 4, 6, 7):
        valid = [mask for mask in range(1, 1 << q) if mask.bit_count() >= a]
        for _ in range(5000):
            m = rng.randint(1, min(80, len(valid)))
            rows = rng.sample(valid, m)
            t = certified_length(m, q, a)
            chosen = greedy_cover(rows, q)
            assert len(chosen) <= t
            assertions += 1
            assert m * (q - a) ** t < q**t
            assertions += 1
            sampled_families += 1

    rp_half_checks = []
    for n in range(1, 41):
        # m=2^n, alpha=1/2: strict union-bound certificate first holds at n+1.
        t = certified_length(2**n, 2, 1)
        assert t == n + 1
        assertions += 1
        rp_half_checks.append({"n": n, "certified_seeds": t})

    # An exponentially rare accepting tape has an exponential certificate.
    rare_checks = []
    for n in range(2, 11):
        q = 2**n
        t = certified_length(2**n, q, 1)
        assert t >= n * 2 ** (n - 1)
        assertions += 1
        rare_checks.append({"n": n, "alpha": f"1/{q}", "certified_seeds": t})

    return {
        "run_id": "RP-DENSITY-HITTING-TRADEOFF38",
        "timestamp_kst": "2026-10-21 10:48",
        "status": "PROVED_SCOPED_PLUS_COMPUTATIONAL_P_VS_RP_OPEN_P_VS_NP_OPEN",
        "theorem": "For m YES inputs and per-input accepting-tape density at least a/q, a machine-and-length-specific hitting list of t seeds exists whenever m(q-a)^t<q^t.",
        "strict_half_density_corollary": "For at most 2^n YES inputs and density 1/2, n+1 seeds suffice.",
        "inverse_polynomial_corollary": "If alpha(n)>=1/poly(n), the advice list and its bit length are polynomial.",
        "rare_event_firewall": "If alpha=2^-n, this certificate is exponential and does not turn random assignment for unique SAT into RP.",
        "exhaustive_q4_families": exhaustive_families,
        "sampled_q8_families": sampled_families,
        "instrumented_assertions": assertions,
        "failures": 0,
        "max_certificate_minus_greedy_slack": max_slack,
        "by_density": by_density,
        "half_density_checks": rp_half_checks,
        "rare_density_checks": rare_checks,
        "seed": 202610211048,
        "scope_firewall": [
            "The list depends on the verifier and input length.",
            "Existence is nonuniform advice, not a uniform constructor.",
            "The result proves containment in P/poly, not P=RP.",
            "A universal public list can be verifier-diagonalized while the language stays in P.",
        ],
    }


if __name__ == "__main__":
    result = audit()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
