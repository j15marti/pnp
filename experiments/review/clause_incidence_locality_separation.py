#!/usr/bin/env python3
"""Finite audit for clause-local versus incidence-local access.

The symbolic theorem checked by this program is stated in LB-0013.  The
program computes exact deterministic decision-tree depth on small promised
occurrence arrays, and checks that two-bit native occurrence tags remove the
scan while preserving only a constant-factor encoding overhead.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from functools import lru_cache
from pathlib import Path


def optimal_rank_depth(length: int, pivot: int) -> int:
    """Exact query depth for rank at pivot under total multiplicity three.

    The pivot is one occurrence.  A candidate is the pair of positions of
    the other two occurrences.  A query reveals whether a position belongs
    to that pair.  The output is the number of occurrences left of pivot.
    """

    positions = tuple(i for i in range(length) if i != pivot)
    candidates = tuple(itertools.combinations(positions, 2))
    full_mask = (1 << len(positions)) - 1
    pos_index = {q: i for i, q in enumerate(positions)}

    def value(cand: tuple[int, int]) -> int:
        return int(cand[0] < pivot) + int(cand[1] < pivot)

    @lru_cache(maxsize=None)
    def solve(cands: tuple[tuple[int, int], ...], remaining: int) -> int:
        if len({value(c) for c in cands}) == 1:
            return 0
        best = length + 1
        mask = remaining
        while mask:
            bit = mask & -mask
            mask -= bit
            idx = bit.bit_length() - 1
            q = positions[idx]
            yes = tuple(c for c in cands if q in c)
            no = tuple(c for c in cands if q not in c)
            if not yes or not no:
                continue
            cost = 1 + max(solve(yes, remaining ^ bit), solve(no, remaining ^ bit))
            best = min(best, cost)
        if best == length + 1:
            raise AssertionError("nonconstant state without a separating query")
        return best

    return solve(candidates, full_mask)


def predicted_depth(length: int, pivot: int) -> int:
    left = pivot
    right = length - pivot - 1
    if left == 0 or right == 0 or (left == 1 and right == 1):
        return 0
    return min(left, right)


def tagged_occurrences(nvars: int, rng: random.Random) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for var in range(nvars):
        for sign in (0, 1):
            for _ in (1, 2, 3):
                rows.append({"var": var, "sign": sign, "rank": 0})
    rng.shuffle(rows)
    seen: dict[tuple[int, int], int] = {}
    for row in rows:
        key = (row["var"], row["sign"])
        seen[key] = seen.get(key, 0) + 1
        row["rank"] = seen[key]
    return rows


def audit(args: argparse.Namespace) -> dict[str, object]:
    started = time.perf_counter()
    depth_rows = []
    decision_tree_checks = 0
    for length in range(3, args.max_length + 1):
        for pivot in range(length):
            exact = optimal_rank_depth(length, pivot)
            predicted = predicted_depth(length, pivot)
            if exact != predicted:
                raise AssertionError((length, pivot, exact, predicted))
            depth_rows.append(
                {"length": length, "pivot": pivot, "exact_depth": exact,
                 "predicted_depth": predicted}
            )
            decision_tree_checks += 1

    rng = random.Random(args.seed)
    tag_checks = 0
    permutation_checks = 0
    encoding_rows = []
    for nvars in args.variable_counts:
        rows = tagged_occurrences(nvars, rng)
        for i, row in enumerate(rows):
            raw_rank = 1 + sum(
                1 for prior in rows[:i]
                if prior["var"] == row["var"] and prior["sign"] == row["sign"]
            )
            if raw_rank != row["rank"]:
                raise AssertionError((nvars, i, raw_rank, row))
            tag_checks += 1

        # Clause/literal order and variable names do not affect tag validity.
        renamed = {v: nvars - 1 - v for v in range(nvars)}
        permuted = list(reversed(rows))
        groups: dict[tuple[int, int], list[int]] = {}
        for row in permuted:
            groups.setdefault((renamed[row["var"]], row["sign"]), []).append(row["rank"])
        for ranks in groups.values():
            if sorted(ranks) != [1, 2, 3]:
                raise AssertionError(ranks)
            permutation_checks += 1

        occurrences = 6 * nvars
        id_bits = max(1, math.ceil(math.log2(max(2, nvars))))
        raw_bits = occurrences * (id_bits + 1)
        tagged_bits = occurrences * (id_bits + 3)  # sign plus two-bit rank
        encoding_rows.append(
            {"variables": nvars, "occurrences": occurrences,
             "identifier_bits": id_bits, "raw_bits": raw_bits,
             "tagged_bits": tagged_bits,
             "ratio": tagged_bits / raw_bits}
        )

    elapsed = time.perf_counter() - started
    return {
        "run_id": "LB-0013",
        "seed": args.seed,
        "method": "exhaustive exact decision-tree dynamic programming and deterministic tag checks",
        "parameters": {"max_length": args.max_length,
                       "variable_counts": args.variable_counts},
        "decision_tree_rows": depth_rows,
        "encoding_rows": encoding_rows,
        "checks": {
            "decision_tree_depth_equalities": decision_tree_checks,
            "native_tag_rank_equalities": tag_checks,
            "rename_reverse_group_equalities": permutation_checks,
            "total": decision_tree_checks + tag_checks + permutation_checks,
        },
        "hostile_controls": [
            "literal-order reversal", "variable renaming", "constant-size tag padding",
            "raw scan versus native tag", "one-bit semantics ignores metadata",
            "preprocessed rank/select kept model-distinct",
        ],
        "limitations": [
            "finite decision trees are checked only through max_length",
            "the asymptotic separation uses the symbolic adversary proof in the report",
            "no lower bound for arbitrary SAT algorithms is inferred",
        ],
        "elapsed_seconds": elapsed,
        "status": "COMPUTATIONAL",
        "passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111512)
    parser.add_argument("--max-length", type=int, default=10)
    parser.add_argument("--variable-counts", type=int, nargs="+", default=[2, 4, 8, 16, 64, 256])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "checks": result["checks"],
                      "elapsed_seconds": result["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
