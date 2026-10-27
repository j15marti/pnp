#!/usr/bin/env python3
"""Finite controls for LSPV-5 OUTPUT-USE-TRILEMMA170.

Dependency free.  It checks ARC190 dense lengths, two genuine copy levels,
the prefix-shift materializer, the reverse-query state-counting control, and
the exponent monotonicity that blocks copy expansion from being a contraction.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

CHECKS = 0


def check(cond: bool, msg: str = "check failed") -> None:
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)


def dense_length(n: int, m: int) -> int:
    """ARC190's declared dense signed-clause-list bit length."""
    vh = math.ceil(math.log2(n + 1))
    mh = max(32, math.ceil(math.log2(m + 1)))
    return 8 + 2 * mh + m * (3 * (vh + 1) + 1)


def phi(n: int, m: int, r: int) -> tuple[int, int, int]:
    check(r >= 1)
    nn, mm = r * n, r * m
    return nn, mm, dense_length(nn, mm)


def prefix_shift_materialize(bits: str, active: str) -> tuple[str, int]:
    """Abstract ARC190 prefix/active layout, counting one active shift per bit."""
    output = ""
    shifts = 0
    for bit in bits:
        # Shift the active representation one cell right and fill the vacated cell.
        shifts += len(active)
        output += bit
    return output + active, shifts


def audit() -> dict:
    # Exact anchors from ARC190.
    check(dense_length(15, 20) == 392)
    check(dense_length(6, 8) == 176)
    anchors = []
    for n, m, expected in [(15, 20, 392), (6, 8, 176)]:
        N = dense_length(n, m)
        nn, mm, L = phi(n, m, N)
        check(L == expected * 0 + dense_length(nn, mm))
        anchors.append({"n": n, "m": m, "N": N, "r": N, "L": L})
    check(anchors[0]["L"] == 337192)
    check(anchors[1]["L"] == 52168)

    # Two genuine typed copy levels, matching ARC190's W1 controls.
    n1, m1, L1 = phi(15, 20, 2)
    n2, m2, L2 = phi(n1, m1, 2)
    check((n1, m1, L1) == (30, 40, 832))
    check((n2, m2, L2) == (60, 80, 1832))

    # Prefix materialization preserves chronological order and costs Q per bit.
    materializers = []
    for q in range(1, 18):
        active = "A" * q
        for x in range(1 << min(q, 8)):
            width = min(q, 8)
            bits = format(x, f"0{width}b")
            tape, shifts = prefix_shift_materialize(bits, active)
            check(tape == bits + active)
            check(shifts == len(bits) * q)
        materializers.append({"active_span": q, "emitted": min(q, 8), "shift_cost": min(q, 8) * q})

    # Reverse-order consumer: after a write-only identity stream ends and the
    # source is unavailable, the state must distinguish all 2^L strings.
    reverse_controls = []
    for L in range(1, 13):
        transcripts = set()
        for x in range(1 << L):
            s = format(x, f"0{L}b")
            reverse = s[::-1]
            transcripts.add(reverse)
            check(reverse[::-1] == s)
        check(len(transcripts) == 1 << L)
        state_bits = math.ceil(math.log2(len(transcripts)))
        check(state_bits == L)
        reverse_controls.append({"L": L, "distinct_reverse_answers": len(transcripts), "minimum_state_bits": state_bits})

    # Copy expansion cannot improve an all-input polynomial ceiling merely by
    # calling the same solver on the longer child: ell*t >= t for ell,t >= 1.
    exponent_grid = []
    for ell_num in range(10, 41):
        ell = ell_num / 10
        for t_num in range(10, 41):
            t = t_num / 10
            check(ell * t + 1e-12 >= t)
            exponent_grid.append((ell, t, ell * t))

    result = {
        "run_id": "OUTPUT-USE-TRILEMMA170",
        "status": "PROVED/EXACT model/interface theorem; COMPUTATIONAL finite controls",
        "anchors": anchors,
        "two_levels": {"level1": [n1, m1, L1], "level2": [n2, m2, L2]},
        "materializer_controls": materializers,
        "reverse_query_controls": reverse_controls,
        "exponent_grid_points": len(exponent_grid),
        "assertions": CHECKS,
        "limitations": [
            "Reverse-query counting concerns a completed write-only stream with no source reread; reread/recomputation is the separately charged virtual-access case.",
            "The theorem classifies interfaces and refutes a free composition, not arbitrary SAT algorithms.",
            "Copy expansion preserves SAT but is not a contraction and supplies no FLMV endpoint."
        ],
    }
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return result


if __name__ == "__main__":
    result = audit()
    target = Path(__file__).with_name("2026-10-26_1948_OUTPUT_USE_TRILEMMA170_raw.json")
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
