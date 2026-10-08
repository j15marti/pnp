#!/usr/bin/env python3
"""Bounded exact test for CLAUSE-DOM-ANTICHAIN1.

The parent CNF is
  AND_i [(x_i OR y_i) AND (NOT x_i OR NOT y_i)].
Restricting every x_i leaves one unit clause on y_i.  The script checks that
the resulting frontier has 2^n distinct, equal-size, pairwise-incomparable
clause sets, and that any two histories can be separated by a common later
restriction.  It is a representation-level countermodel, not a SAT lower
bound: the parent is an easy 2-CNF/XOR instance.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from pathlib import Path


SEED = 20261007


def deadline(_signum: int, _frame: object) -> None:
    raise TimeoutError("25-second cooperative budget exceeded")


def residual(n: int, history: int) -> frozenset[int]:
    """Return unit literals: +j means y_j, -j means not y_j."""
    return frozenset((-(j + 1) if (history >> j) & 1 else (j + 1)) for j in range(n))


def sat_after_unit(res: frozenset[int], var: int, value: bool) -> bool:
    lit = var if value else -var
    return -lit not in res


def run(max_n: int) -> dict:
    rows = []
    exact_pairwise_limit = 10
    for n in range(1, max_n + 1):
        frontier = [residual(n, h) for h in range(1 << n)]
        distinct = len(set(frontier))
        equal_size = all(len(r) == n for r in frontier)

        comparable_pairs = 0
        checked_pairs = 0
        separated_pairs = 0
        if n <= exact_pairwise_limit:
            for a in range(1 << n):
                for b in range(a + 1, 1 << n):
                    ra, rb = frontier[a], frontier[b]
                    checked_pairs += 1
                    if ra <= rb or rb <= ra:
                        comparable_pairs += 1

                    diff = a ^ b
                    j = (diff & -diff).bit_length()  # 1-based y variable
                    satisfy_a = j in ra
                    if sat_after_unit(ra, j, satisfy_a) and not sat_after_unit(rb, j, satisfy_a):
                        separated_pairs += 1
        else:
            # The proof is symbolic for large n; deterministic adjacent and
            # complement controls guard the implementation without quadratic work.
            controls = []
            for a in range(min(1 << n, 4096)):
                controls.append((a, a ^ 1))
                controls.append((a, a ^ ((1 << n) - 1)))
            for a, b in controls:
                ra, rb = frontier[a], frontier[b]
                checked_pairs += 1
                if ra <= rb or rb <= ra:
                    comparable_pairs += 1
                diff = a ^ b
                j = (diff & -diff).bit_length()
                satisfy_a = j in ra
                if sat_after_unit(ra, j, satisfy_a) and not sat_after_unit(rb, j, satisfy_a):
                    separated_pairs += 1

        assert distinct == 1 << n
        assert equal_size
        assert comparable_pairs == 0
        assert separated_pairs == checked_pairs

        literal_occurrences_parent = 4 * n
        literal_occurrences_residual = n
        rows.append(
            {
                "n": n,
                "frontier_size": 1 << n,
                "distinct_residuals": distinct,
                "residual_unit_clauses": n,
                "parent_literal_occurrences": literal_occurrences_parent,
                "residual_literal_occurrences": literal_occurrences_residual,
                "checked_pairs": checked_pairs,
                "comparable_pairs": comparable_pairs,
                "common_continuation_separations": separated_pairs,
            }
        )

    return {
        "claim": "CLAUSE-DOM-ANTICHAIN1",
        "status": "COMPUTATIONAL verification of a PROVED/EXACT finite construction",
        "seed": SEED,
        "max_n": max_n,
        "pairwise_exhaustive_through_n": exact_pairwise_limit,
        "family": "AND_i ((x_i OR y_i) AND (NOT x_i OR NOT y_i))",
        "rows": rows,
        "hostile_controls": {
            "easy_family": "2-CNF and affine XOR; no machine lower bound",
            "source_carry": "parent and history regenerate each residual cheaply",
            "padding": "tautological padding normalizes away; active independent products preserve the antichain",
            "renaming": "literal/variable bijections preserve pairwise incomparability",
            "current_answer_escape": "all residuals are SAT, but every distinct pair is separated by one common y restriction",
            "oracle_algebraic_escape": "2-SAT or Gaussian elimination solves the parent directly",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=14)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 18:
        raise SystemExit("--max-n must be in [1,18] for this bounded run")

    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.monotonic()
    result = run(args.max_n)
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    signal.alarm(0)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
