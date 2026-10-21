#!/usr/bin/env python3
"""Finite controls for RP-RELATIVIZATION-BIDIRECTIONAL-BARRIER37.

The program exercises finite clocked query strategies and zero-versus-half
oracle slices.  It does not prove the asymptotic oracle theorem.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


OUT = Path("results/raw/separation/2026-10-21_0948_RP_RELATIVIZATION_BIDIRECTIONAL_BARRIER37_summary.json")
ASSERTIONS = 0


def require(value: bool) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not value:
        raise AssertionError("RP relativization finite control failed")


def run_strategy(n: int, budget: int, salt: int, oracle: set[int]) -> tuple[bool, tuple[int, ...]]:
    size = 1 << n
    used: set[int] = set()
    answers: list[int] = []
    transcript: list[int] = []
    state = (salt * 0x9E3779B1 + n) & 0xFFFFFFFF
    for step in range(budget):
        state = (1664525 * state + 1013904223 + 17 * sum(answers)) & 0xFFFFFFFF
        query = state % size
        while query in used:
            query = (query + 1) % size
        used.add(query)
        transcript.append(query)
        answers.append(int(query in oracle))
    decision = (salt + sum((i + 3) * bit for i, bit in enumerate(answers))) & 1
    return bool(decision), tuple(transcript)


def diagonal_slice(n: int, budget: int, salt: int) -> tuple[set[int], bool, tuple[int, ...]]:
    accept_on_zero, transcript = run_strategy(n, budget, salt, set())
    size = 1 << n
    require(len(transcript) == budget)
    require(len(set(transcript)) == budget)
    require(budget < size // 2)
    if accept_on_zero:
        # NO slice: the deterministic strategy accepts incorrectly.
        oracle: set[int] = set()
        language_bit = False
    else:
        # YES slice: keep the zero-path queries fixed and fill exactly half of
        # the unqueried positions with ones.
        unqueried = [x for x in range(size) if x not in set(transcript)]
        oracle = set(unqueried[: size // 2])
        language_bit = True
    return oracle, language_bit, transcript


def main() -> None:
    stages = 0
    total_queries = 0
    yes_slices = 0
    no_slices = 0
    for n in range(6, 15):
        max_budget = min(4 * n, (1 << (n - 1)) - 1)
        for salt in range(512):
            budget = 1 + ((13 * salt + n) % max_budget)
            oracle, language_bit, zero_path = diagonal_slice(n, budget, salt)
            final_decision, final_path = run_strategy(n, budget, salt, oracle)
            require(final_path == zero_path)
            require(final_decision != language_bit)
            require(len(oracle) in (0, 1 << (n - 1)))
            require(all(query not in oracle for query in zero_path))
            # The RP oracle algorithm makes one uniform query.  Its exact
            # acceptance probability is zero on NO and one half on YES.
            require((len(oracle) == 0) == (not language_bit))
            require((len(oracle) * 2 == (1 << n)) == language_bit)
            if language_bit:
                yes_slices += 1
            else:
                no_slices += 1
            stages += 1
            total_queries += budget

    payload = {
        "artifact": "RP-RELATIVIZATION-BIDIRECTIONAL-BARRIER37",
        "timestamp_asia_seoul": "2026-10-21 09:48",
        "status_p_vs_rp": "OPEN",
        "status_p_vs_np": "OPEN",
        "scope": "finite clocked oracle-strategy controls; not an unrelativized separation",
        "finite_stages": stages,
        "yes_half_density_slices": yes_slices,
        "no_zero_density_slices": no_slices,
        "total_deterministic_queries": total_queries,
        "assertions": ASSERTIONS,
        "failures": 0,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
