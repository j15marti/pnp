#!/usr/bin/env python3
"""Finite controls for CAP-ACCESSOR-LEDGER181.

This checks only arithmetic/accounting identities used in the report.  It is
not a SAT lower-bound experiment and does not measure native TM transitions.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path


def stopped_calls(bits: tuple[int, ...], accept_cut: int, reject_cut: int) -> int:
    """Number of calls made by the fixed-order gap stopping rule."""
    accepts = rejects = 0
    for i, bit in enumerate(bits, 1):
        accepts += bit
        rejects += 1 - bit
        if accepts >= accept_cut or rejects >= reject_cut:
            return i
    return len(bits)


def main() -> None:
    assertions = 0
    failures: list[str] = []
    examples: list[dict[str, int]] = []

    def check(ok: bool, msg: str) -> None:
        nonlocal assertions
        assertions += 1
        if not ok:
            failures.append(msg)

    # Exact black-box seed-gap stopping identity K=R-(B-A)+1.
    stop_cases = 0
    for r in range(1, 13):
        for a in range(r + 1):
            for b in range(a + 1, r + 1):
                bound = r - (b - a) + 1
                observed = 0
                for bits in product((0, 1), repeat=r):
                    calls = stopped_calls(bits, a + 1, r - b + 1)
                    observed = max(observed, calls)
                    check(calls <= bound, f"stop bound r={r} a={a} b={b}")
                check(observed == bound, f"stop tight r={r} a={a} b={b}")
                stop_cases += 1

    # Disjoint cap-accessor ledger: total = cap evaluation + enumeration.
    # Delays model an explicitly supplied accessor implementation.  Equal cap
    # values with different delays demonstrate representation dependence only;
    # they are not an inherent lower bound for the mathematical cap function.
    ledger_cases = 0
    max_ratio = 0.0
    for n in range(2, 65):
        for q in range(0, min(8, n) + 1):
            for r in (1, 2, 3, 5, 8, 13):
                for tau in (1, 2, 7, 31):
                    enum = (1 << q) * r * tau
                    for delay in (0, 1, n, n * n, 1 << min(n, 20)):
                        total = delay + enum
                        check(total >= enum, "omitted accessor cannot exceed total")
                        check(total - enum == delay, "ledger must be disjoint")
                        check(max(delay, enum) <= total <= 2 * max(delay, enum),
                              "sum/max normalization")
                        ratio = total / max(1, enum)
                        max_ratio = max(max_ratio, ratio)
                        ledger_cases += 1
                        if n in (8, 16, 32, 64) and q in (0, 4, 8) and r == 5 and tau == 7 and delay == (1 << min(n, 20)):
                            examples.append({"N": n, "q": q, "delay": delay,
                                             "enumeration": enum, "charged_total": total})

    # Peak space is max, not a sum of histories.  Include cap evaluator state,
    # verifier state, persistent physical dictionary and counters.
    space_cases = 0
    for sq in range(0, 17):
        for s in range(0, 17):
            for q in range(0, 17):
                for address_width in (1, 2, 4, 8, 16):
                    for logr in (0, 1, 3, 7):
                        dictionary = q * (address_width + 1)
                        peak = max(sq, s + dictionary + logr)
                        check(peak >= sq, "peak covers cap evaluator")
                        check(peak >= s + dictionary + logr, "peak covers enumeration")
                        check(peak <= sq + s + dictionary + logr,
                              "peak no larger than phase sum")
                        space_cases += 1

    # Finite-exception uniformity control.  For a fixed delta and fixed N0,
    # the small-input truth table is one finite constant in one program; it is
    # not a changing advice string indexed by the live input length.
    finite_table_cases = 0
    for n0 in range(1, 65):
        table = {n: (n * n + 3 * n + 1) & 1 for n in range(n0)}
        frozen = tuple(sorted(table.items()))
        for live_n in range(0, 128):
            same_program_table = tuple(sorted(table.items()))
            check(same_program_table == frozen, "finite table changed with live N")
            if live_n < n0:
                check(live_n in table, "small input must be table-covered")
            else:
                check(live_n not in table, "large input must use uniform branch")
            finite_table_cases += 1

    # Fixed seed order and early stopping use the actual stopped physical union.
    union_cases = 0
    for r in range(1, 11):
        seeds = tuple(range(r))
        for bits in product((0, 1), repeat=r):
            for a in range(r + 1):
                for b in range(a + 1, r + 1):
                    k = stopped_calls(bits, a + 1, r - b + 1)
                    stopped_union = set(seeds[:k])
                    full_union = set(seeds)
                    check(stopped_union <= full_union, "stopped union subset")
                    check(len(stopped_union) == k, "one unique key per executed seed")
                    union_cases += 1

    payload = {
        "run_id": "CAP-ACCESSOR-LEDGER181",
        "status": "COMPUTATIONAL finite arithmetic controls only",
        "random_seed": None,
        "exhaustive": True,
        "assertions": assertions,
        "failures": failures,
        "stop_cases": stop_cases,
        "ledger_cases": ledger_cases,
        "space_cases": space_cases,
        "finite_table_cases": finite_table_cases,
        "stopped_union_cases": union_cases,
        "max_omitted_accessor_ratio": max_ratio,
        "examples": examples,
        "limitations": [
            "No ordinary SAT instances are solved.",
            "Artificial delays demonstrate charged implementation cost, not an inherent lower bound for a cap function.",
            "Finite controls do not prove asymptotic complexity claims."
        ],
    }
    out = Path(__file__).with_name("2026-10-27_0648_LSPV-5_CAP_ACCESSOR_LEDGER181_raw.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    code_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    raw_sha = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"assertions": assertions, "failures": len(failures),
                      "code_sha256": code_sha, "raw_sha256": raw_sha,
                      "raw_path": str(out)}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
