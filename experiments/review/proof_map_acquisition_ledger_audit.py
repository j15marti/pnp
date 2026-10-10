#!/usr/bin/env python3
"""Exact finite audit of the CC-0002 acquisition exponent inference."""
from __future__ import annotations

import argparse
import json
import signal
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ns = ap.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(25)

    hostile = []
    positive = []
    for m in range(4, 25, 2):
        n = 1 << m
        w = m // 2
        trials = (1 << (w + 1)) - 1
        claimed_scale = 1 << w
        displayed = trials * (1 + n + w + 1)
        shared = trials * (1 + w + 1)
        assert displayed >= n * claimed_scale
        hostile.append({
            "m": m, "N": n, "w": w,
            "displayed": displayed,
            "displayed_over_N_to_kappa_floor": displayed // claimed_scale,
            "shared_input": shared,
            "shared_over_N_to_kappa_ceiling": (shared + claimed_scale - 1) // claimed_scale,
        })

        q = n
        scale = n * claimed_scale
        displayed_pc = trials * (q + n + w + 1)
        shared_pc = trials * (q + w + 1)
        positive.append({
            "m": m,
            "displayed_over_N_to_1_plus_kappa_ceiling": (displayed_pc + scale - 1) // scale,
            "shared_over_N_to_1_plus_kappa_ceiling": (shared_pc + scale - 1) // scale,
        })

    out = {
        "run_id": "PROOFMAP-0002",
        "status": "PASS",
        "arithmetic": "exact integers",
        "hostile_control": {
            "parameters": "N=2^m, w=(log_2 N)/2, q=1, |p|=0",
            "conclusion": "the displayed CC-0002 product has exponent at least 3/2, not the claimed 1/2",
            "rows": hostile,
        },
        "positive_control": {
            "parameters": "N=2^m, w=(log_2 N)/2, q=N",
            "conclusion": "when q dominates N, both ledgers have exponent 3/2 up to logarithmic factors",
            "rows": positive,
        },
        "repair": (
            "For the displayed per-candidate-copy bound use exponent "
            "kappa+max(v,1) when |p|=O(N).  To recover v+kappa for v<1, "
            "prove a separate shared-read-only-input random-access acquirer "
            "and charge all verifier probes in q."
        ),
        "limitations": [
            "Finite arithmetic witnesses an algebraic mismatch; it is not an all-acquirer lower bound.",
            "The shared-input control is model-dependent and is not promoted here to the COST spine."],
    }
    signal.alarm(0)
    Path(ns.output).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "hostile_rows": len(hostile), "positive_rows": len(positive)}))


if __name__ == "__main__":
    main()
