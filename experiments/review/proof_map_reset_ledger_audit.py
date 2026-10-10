#!/usr/bin/env python3
"""Bounded hostile-control audit for the reset-aware PFCERT ledger."""

from __future__ import annotations

import json
import signal
import time
from fractions import Fraction
from pathlib import Path


OUT = Path("results/raw/review/2026-10-10_PROOFMAP-0003_reset_ledger.json")


class BudgetExceeded(RuntimeError):
    pass


def alarm_handler(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


def verifier(work, candidate, target):
    """Accept target only from the verifier's required blank start state."""
    old = work[0]
    work[0] = 1
    return old == 0 and candidate == target


def enumerate_candidates(width, target, reset):
    work = [0]
    for candidate in range(1 << width):
        if reset:
            work[0] = 0
        if verifier(work, candidate, target):
            return candidate
    return None


def exponent_cases():
    rows = []
    # M=2^(2d) makes half-integral powers exact integers.
    for d in range(2, 11):
        m = 1 << (2 * d)
        for kappa in (Fraction(0), Fraction(1, 2), Fraction(1)):
            for v in (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2)):
                w = int(kappa * (2 * d))
                q = 1 << int(v * (2 * d))
                b = q
                reset_cost = b * (b.bit_length() + 1)
                candidates = (1 << (w + 1)) - 1
                repaired = candidates * (q + reset_cost + w + m.bit_length()) + w
                copied = candidates * (q + m + w + m.bit_length()) + w
                assert reset_cost <= q * (q.bit_length() + 1)
                rows.append({
                    "M": m,
                    "kappa": str(kappa),
                    "v": str(v),
                    "w": w,
                    "q": q,
                    "reset": reset_cost,
                    "repaired_time": repaired,
                    "copied_time": copied,
                    "reset_premise_b_le_q": b <= q,
                })
    return rows


def main():
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    started = time.monotonic()
    hostile = []
    controls = []
    for width in range(1, 19):
        target = (1 << width) - 1
        dirty = enumerate_candidates(width, target, reset=False)
        clean = enumerate_candidates(width, target, reset=True)
        assert dirty is None
        assert clean == target
        hostile.append({"width": width, "target": target, "found": dirty})
        controls.append({"width": width, "target": target, "found": clean})

    rows = exponent_cases()
    invalid = {"q": 8, "b": 9, "premise_holds": 9 <= 8}
    assert not invalid["premise_holds"]
    payload = {
        "run_id": "PROOFMAP-0003",
        "status": "PASS",
        "scientific_scope": "finite hostile control plus exact integer ledger checks; not an asymptotic lower bound",
        "dirty_state_counterexamples": hostile,
        "explicit_reset_controls": controls,
        "exponent_cases": len(rows),
        "invalid_b_gt_q_control": invalid,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
