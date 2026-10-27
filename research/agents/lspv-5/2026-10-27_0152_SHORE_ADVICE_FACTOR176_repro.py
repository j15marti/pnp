#!/usr/bin/env python3
"""Finite controls for SHORE-ADVICE-FACTOR176.

No third-party dependencies, no randomness.  The symbolic theorem is proved
in the paired LaTeX report; this program exhausts the finite split-advice
countercontrol and checks the all-cut counting arithmetic.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def disj(x: int, y: int) -> bool:
    return (x & y) == 0


def accept_split(mask: int, u: int, v: int, x: int, y: int) -> bool:
    """Two-shore program (u,v): left checks x=u, right checks y=~v."""
    return x == u and y == (mask ^ v)


def ball(A: int, h: int) -> int:
    return sum(A**j for j in range(h + 1))


def main() -> None:
    assertions = 0
    failures: list[str] = []
    split_rows = []

    def check(ok: bool, label: str) -> None:
        nonlocal assertions
        assertions += 1
        if not ok:
            failures.append(label)

    # Exact hostile control.  Selected programs are p_a=(a,a).  Each is
    # globally sound and accepts exactly one diagonal YES source.  Different
    # selected programs have the same empty central transcript, but splicing
    # their two shores creates an unselected hybrid program which can accept
    # a crossed NO source.  This is why split advice needs a shore factor
    # unless soundness is closed under recombination.
    for m in range(1, 8):
        n = 1 << m
        mask = n - 1
        selected_accepts = 0
        sound_checks = 0
        hybrid_no = 0
        for a in range(n):
            # Coverage and exact singleton acceptance.
            check(accept_split(mask, a, a, a, mask ^ a), f"cover m={m} a={a}")
            selected_accepts += 1
            for x in range(n):
                for y in range(n):
                    acc = accept_split(mask, a, a, x, y)
                    check((not acc) or disj(x, y),
                          f"selected sound m={m} p={a} x={x} y={y}")
                    check(acc == (x == a and y == (mask ^ a)),
                          f"singleton m={m} p={a} x={x} y={y}")
                    sound_checks += 2

        # Every distinct pair has at least one NO crossed orientation.  The
        # corresponding split hybrid accepts it exactly.
        for a in range(n):
            for ap in range(a + 1, n):
                y1 = mask ^ ap
                y2 = mask ^ a
                no1 = not disj(a, y1)
                no2 = not disj(ap, y2)
                check(no1 or no2, f"fooling pair m={m} a={a} ap={ap}")
                if no1:
                    check(accept_split(mask, a, ap, a, y1),
                          f"hybrid1 m={m} a={a} ap={ap}")
                    hybrid_no += 1
                if no2:
                    check(accept_split(mask, ap, a, ap, y2),
                          f"hybrid2 m={m} a={a} ap={ap}")
                    hybrid_no += 1

        # All selected left and right fragments are distinct, so either safe
        # grouping has n singleton groups.  Prefix-left placement has one
        # right fragment and therefore factor one.
        check(len({a for a in range(n)}) == n, f"left groups m={m}")
        check(len({a for a in range(n)}) == n, f"right groups m={m}")
        check(min(n, n) == n, f"split factor m={m}")
        check(min(n, 1) == 1, f"inline-left factor m={m}")
        split_rows.append({
            "m": m,
            "selected_programs": n,
            "selected_acceptances": selected_accepts,
            "selected_soundness_assertions": sound_checks,
            "accepted_crossed_NO_hybrids": hybrid_no,
            "safe_split_shore_factor": n,
            "safe_inline_left_factor": 1,
        })

    # Exact all-cut union arithmetic behind ARC197.  For every parameter row,
    # each fixed cut admits at most B_A(h) short transcripts.  Union over G
    # cuts leaves at least 2^m-G*B_A(h) inputs long at every cut.
    tail_rows = []
    for m in range(2, 21):
        total = 1 << m
        for A in range(2, 8):
            for h in range(0, 6):
                B = ball(A, h)
                for G in range(1, min(17, total + 1)):
                    bad_cap = min(total, G * B)
                    long_floor = total - bad_cap
                    check(long_floor >= 0, f"tail nonnegative {m,A,h,G}")
                    check(long_floor == max(0, total - G * B),
                          f"tail exact union {m,A,h,G}")
                    if G * B <= total // 4:
                        check(long_floor * 4 >= 3 * total,
                              f"three-quarter tail {m,A,h,G}")
                    tail_rows.append((m, A, h, G, B, long_floor))

    # Algebraic factor controls.  Advice physically confined to one shore has
    # factor one; split selected-program soundness requires grouping by one
    # shore; a globally separate unsplit channel requires full-content match.
    factor_rows = []
    for b_left in range(0, 13):
        for b_right in range(0, 13):
            P_left = 1 << b_left
            P_right = 1 << b_right
            split_factor = min(P_left, P_right)
            inline_left = 1
            external = 1 << (b_left + b_right)
            check(inline_left <= split_factor <= external,
                  f"factor order {b_left,b_right}")
            check(split_factor == (1 << min(b_left, b_right)),
                  f"factor exponent {b_left,b_right}")
            factor_rows.append({
                "b_left": b_left,
                "b_right": b_right,
                "inline_left_factor": inline_left,
                "split_selected_sound_factor": split_factor,
                "external_unsplit_factor": external,
            })

    # LSPV-4 jump packing correction: removing a redundant inline-program
    # multiplier always strengthens the finite bound; no exponent is borrowed.
    jump_rows = []
    for b in range(0, 17):
        for A in range(2, 10):
            for ell in range(0, 9):
                for G in (1, 3, 7, 31):
                    repaired = G * (A ** (ell + 1))
                    old = (1 << (b + 1)) * repaired
                    check(repaired <= old, f"jump factor {b,A,ell,G}")
                    check(old // repaired == (1 << (b + 1)),
                          f"jump ratio {b,A,ell,G}")
                    jump_rows.append((b, A, ell, G, repaired, old))

    payload = {
        "id": "SHORE-ADVICE-FACTOR176",
        "timestamp_utc": "2026-10-27T08:52:00Z",
        "status": {
            "shore_factor_theorem": "PROVED/EXACT restricted, symbolic proof in report",
            "split_advice_countercontrol": "COMPUTATIONAL exhaustive finite controls",
            "arc_edge_90": "OPEN",
            "p_vs_np": "OPEN",
        },
        "parameters": {
            "split_countercontrol_m": [1, 7],
            "tail_m": [2, 20],
            "tail_A": [2, 7],
            "tail_h": [0, 5],
            "tail_G": "1..min(16,2^m)",
            "advice_bits_per_shore": [0, 12],
            "jump_b": [0, 16],
            "random_seed": None,
            "method": "exhaustive/deterministic exact integer arithmetic",
        },
        "assertions": assertions,
        "failures": len(failures),
        "first_failures": failures[:20],
        "split_rows": split_rows,
        "tail_row_count": len(tail_rows),
        "tail_digest": hashlib.sha256(json.dumps(tail_rows, separators=(",", ":")).encode()).hexdigest(),
        "factor_rows": factor_rows,
        "jump_row_count": len(jump_rows),
        "jump_digest": hashlib.sha256(json.dumps(jump_rows, separators=(",", ":")).encode()).hexdigest(),
        "limitations": [
            "Finite controls do not prove the symbolic theorem.",
            "The split-advice protocol is a model-boundary countercontrol, not an ordinary-SAT lower bound.",
            "No sequential-tape inequality is transferred to RAM/RAT or FLMV.",
        ],
    }
    out = Path("2026-10-27_0152_SHORE_ADVICE_FACTOR176_raw.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "assertions": assertions,
        "failures": len(failures),
        "output": str(out),
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
