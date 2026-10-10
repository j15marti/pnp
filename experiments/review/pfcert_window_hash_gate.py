#!/usr/bin/env python3
"""Exact bounded checks for CC-WINDOW-HASH1.

The experiment validates finite instances of two symbolic lemmas:
(i) the exact number of verifier calls made by exhaustive witness search and
by the bounded-list diagonal enumerator; and
(ii) the fiber criterion for an exact semantic quotient through a finite hash.
It is not evidence for an asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import signal
from pathlib import Path


class BudgetExpired(RuntimeError):
    pass


def _alarm(_signum: int, _frame: object) -> None:
    raise BudgetExpired("25-second cooperative budget expired")


def ceil_log2(value: int) -> int:
    if value <= 1:
        return 0
    return (value - 1).bit_length()


def factor_through(mapping: tuple[int, ...], semantics: tuple[int, ...]) -> bool:
    seen: dict[int, int] = {}
    for key, value in zip(mapping, semantics):
        if key in seen and seen[key] != value:
            return False
        seen[key] = value
    return True


def hash_audit(max_q: int) -> dict[str, object]:
    rows: list[dict[str, int]] = []
    total_maps = 0
    hostile_failures = 0
    collision_cs_checks = 0
    for q in range(1, max_q + 1):
        domain = 1 << q
        for b in range(q):
            codomain = 1 << b
            map_count = codomain ** domain
            min_coll = None
            max_coll = 0
            for mapping in itertools.product(range(codomain), repeat=domain):
                total_maps += 1
                fibers = [0] * codomain
                for value in mapping:
                    fibers[value] += 1
                collision_count = sum(size * size for size in fibers)
                image_size = sum(size > 0 for size in fibers)
                assert image_size * collision_count >= domain * domain
                collision_cs_checks += 1
                min_coll = collision_count if min_coll is None else min(min_coll, collision_count)
                max_coll = max(max_coll, collision_count)

                first: dict[int, int] = {}
                pair = None
                for index, value in enumerate(mapping):
                    if value in first:
                        pair = (first[value], index)
                        break
                    first[value] = index
                assert pair is not None  # b < q, hence pigeonhole collision.
                semantics = [0] * domain
                semantics[pair[1]] = 1
                assert not factor_through(mapping, tuple(semantics))
                hostile_failures += 1

            rows.append(
                {
                    "q": q,
                    "b": b,
                    "domain": domain,
                    "codomain": codomain,
                    "maps": map_count,
                    "min_collision_count": int(min_coll or 0),
                    "max_collision_count": max_coll,
                }
            )
    return {
        "rows": rows,
        "maps_checked": total_maps,
        "hostile_semantics_nonfactorizations": hostile_failures,
        "collision_cauchy_schwarz_checks": collision_cs_checks,
    }


def window_audit() -> dict[str, object]:
    cases = [
        {"name": "fits", "n": 64, "witness_bound": 6, "verify_steps": 1 << 8, "target_steps": 1 << 20},
        {"name": "fails", "n": 64, "witness_bound": 32, "verify_steps": 1 << 8, "target_steps": 1 << 20},
        {"name": "boundary", "n": 32, "witness_bound": 10, "verify_steps": 1 << 7, "target_steps": 1 << 18},
    ]
    for case in cases:
        witness_count = (1 << (case["witness_bound"] + 1)) - 1
        per_candidate = case["verify_steps"] + case["n"] + case["witness_bound"] + 1
        exhaustive_upper = witness_count * per_candidate
        case["witness_strings_leq_bound"] = witness_count
        case["exhaustive_upper_steps"] = exhaustive_upper
        case["fits_target"] = exhaustive_upper <= case["target_steps"]

    list_count_checks = 0
    minimum_missing = None
    diagonal_examples: list[dict[str, int]] = []
    for n in range(2, 13):
        for list_bound in range(1, 1 << (n - 1)):
            k = n - ceil_log2(list_bound) - 1
            if k < 0:
                continue
            programs = (1 << (k + 1)) - 1
            covered_upper = list_bound * programs
            missing_lower = (1 << n) - covered_upper
            assert missing_lower >= 1
            list_count_checks += 1
            minimum_missing = missing_lower if minimum_missing is None else min(minimum_missing, missing_lower)
        if n in (4, 8, 12):
            list_bound = 2
            k = n - 2
            programs = (1 << (k + 1)) - 1
            witness_bound = n // 2
            witnesses = (1 << (witness_bound + 1)) - 1
            verifier_calls = (1 << n) * programs * witnesses
            diagonal_examples.append(
                {
                    "n": n,
                    "list_bound": list_bound,
                    "program_threshold": k,
                    "witness_bound": witness_bound,
                    "verifier_calls": verifier_calls,
                }
            )
    return {
        "acquisition_cases": cases,
        "bounded_list_count_checks": list_count_checks,
        "minimum_missing_lower_bound": minimum_missing,
        "diagonal_examples": diagonal_examples,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q", type=int, default=3)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    result = {
        "run_id": "CC-0002",
        "status": "PASS",
        "arithmetic": "exact integers",
        "randomness": "none; exhaustive",
        "hash_audit": hash_audit(args.max_q),
        "window_audit": window_audit(),
        "limitations": [
            "Finite checks validate the implementation only.",
            "The acquisition bound is for lexicographic exhaustive search, not a lower bound on every acquirer.",
            "The hash test constructs hostile semantics after seeing the hash; it proves no SAT runtime lower bound.",
        ],
    }
    signal.alarm(0)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
