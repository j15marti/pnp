#!/usr/bin/env python3
"""Exact accounting audit for the pinning-as-contraction candidate.

The experiment uses rational arithmetic for exponent recurrences and exact
integer arithmetic for the declared indexed CNF encoding.  It validates an
accounting theorem; it is not a SAT lower-bound experiment.
"""

from __future__ import annotations

import argparse
import json
import math
import signal
import time
from fractions import Fraction
from pathlib import Path


class BudgetExceeded(RuntimeError):
    pass


def alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


def gamma_len(x: int) -> int:
    assert x >= 1
    return 2 * (x.bit_length() - 1) + 1


def cnf_bits(nvars: int, widths: list[int]) -> int:
    w = max(1, math.ceil(math.log2(nvars + 1)))
    return (gamma_len(nvars) + gamma_len(len(widths) + 1)
            + sum(gamma_len(k + 1) + k * (1 + w) for k in widths))


def proper_pin_base_bits(n: int) -> int:
    return cnf_bits(3 * n, [3] * (4 * n))


def pinned_bits(n: int, prefix: int, mode: str) -> int:
    if mode == "unit":
        return cnf_bits(3 * n, [3] * (4 * n) + [1] * prefix)
    if mode == "proper3":
        return cnf_bits(3 * n + 2 * prefix,
                        [3] * (4 * n + 4 * prefix))
    raise AssertionError(mode)


def recurrence(k: Fraction, eta: Fraction, lam: Fraction,
               local: Fraction, depth: int) -> list[Fraction]:
    values = [k]
    for _ in range(depth):
        values.append(max(local, eta + lam * values[-1]))
    return values


def frac(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def run(max_power: int, max_depth: int) -> dict[str, object]:
    started = time.monotonic()
    length_checks = recurrence_checks = hostile_checks = 0
    length_rows = []
    for p in range(max_power + 1):
        n = 1 << p
        base = proper_pin_base_bits(n)
        d = 3 * n
        for mode in ("unit", "proper3"):
            lengths = [base] + [pinned_bits(n, j, mode) for j in range(1, d + 1)]
            total = sum(lengths)
            assert all(x >= base for x in lengths)
            assert total >= (d + 1) * base
            # Every query has O(n) clauses and O(n) variables, hence an
            # O(n log n) encoding.  This finite guard checks an explicit
            # constant envelope for the declared encoding.
            assert max(lengths) <= 10 * base
            batch_work = 12 * n + 6 * n  # base literal touches + two nvar outputs
            assert batch_work <= base + 6 * n
            length_checks += len(lengths) + 4
            length_rows.append({
                "n": n, "mode": mode, "base_bits": base,
                "queries": d + 1, "total_materialized_bits": total,
                "max_query_bits": max(lengths), "batch_work_units": batch_work,
                "materialized_to_batch_ratio": total / batch_work,
            })

    examples = []
    for k_int in range(1, 13):
        k = Fraction(k_int)
        for eta in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
            for local in (Fraction(0), Fraction(1), Fraction(3, 2)):
                vals = recurrence(k, eta, Fraction(1), local, max_depth)
                assert all(v >= k for v in vals)
                recurrence_checks += len(vals)

                contracted = recurrence(k, eta, Fraction(1, 2), local, max_depth)
                fixed = max(local, 2 * eta)
                # Lambda<1 removes dependence on K only asymptotically/fixed
                # depth chosen after K; lambda=1 never does.
                assert contracted[-1] <= max(k, fixed + Fraction(1, 2 ** max_depth) * k)
                hostile_checks += 1
                if k_int in (2, 5, 12) and eta in (Fraction(0), Fraction(1, 2)) and local == 1:
                    examples.append({
                        "K": frac(k), "eta": frac(eta), "local": frac(local),
                        "lambda_1": [frac(v) for v in vals],
                        "lambda_half": [frac(v) for v in contracted],
                    })

    return {
        "run_id": "SYNTHESIS-0001",
        "status": "PASS",
        "theorem_checked": "PINNING-NOCONTRACT1",
        "candidate_falsified": "PINNING-CONTRACTION1",
        "exact_statement": (
            "For exponent recurrence C_{t+1}=max(r,eta+lambda*C_t), "
            "explicit source-retaining pinning has lambda=1, hence C_t>=K "
            "for every depth. Query count or transcript volume cannot remove K."
        ),
        "parameters": {"max_power": max_power, "max_depth": max_depth},
        "checks": {
            "encoding_and_volume": length_checks,
            "recurrence_values": recurrence_checks,
            "lambda_half_controls": hostile_checks,
        },
        "largest_encoding_cell": length_rows[-1],
        "selected_recurrence_examples": examples,
        "elapsed_seconds": time.monotonic() - started,
        "limitations": [
            "This is exact accounting for the declared recurrence, not an unrestricted SAT lower bound.",
            "Lambda<1 is necessary for this contraction architecture but does not construct a shrinker.",
            "Batch sharing can lower cost on structured families; no universal hard-core batch lower bound is proved.",
            "CORE-ACQUIRE1, QUERY-NOSHARE1, the nonrelativizing hinge, and P versus NP remain open.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-power", type=int, default=8)
    parser.add_argument("--max-depth", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(25)
    try:
        result = run(args.max_power, args.max_depth)
    finally:
        signal.alarm(0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
