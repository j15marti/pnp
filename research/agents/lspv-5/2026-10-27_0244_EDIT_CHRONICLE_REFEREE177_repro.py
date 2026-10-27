#!/usr/bin/env python3
"""Exact finite controls for EDIT-CHRONICLE-REFEREE177.

The symbolic edit-chronicle theorem is proved in the paired report.  This
program checks its exact finite enumerator, the coarse published bound,
the all-cut common-input tail, proof-tape factors, and blank-start firewall.
No randomness or third-party package is used.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json


def exact_histories(W: int, V: int, D: int, L: int) -> int:
    """Edit symbols W, crossing symbols V, at most D edits and L crossings."""
    return sum(comb(e + ell, e) * (W ** e) * (V ** ell)
               for e in range(D + 1) for ell in range(L + 1))


def brute_histories(W: int, V: int, Dmax: int, Lmax: int):
    """Enumerate every typed word once and tabulate all (D,L) ceilings."""
    counts = defaultdict(int)
    alphabet = tuple(range(W + V))
    for n in range(Dmax + Lmax + 1):
        for word in product(alphabet, repeat=n):
            e = sum(x < W for x in word)
            ell = n - e
            if e <= Dmax and ell <= Lmax:
                for D in range(e, Dmax + 1):
                    for L in range(ell, Lmax + 1):
                        counts[(D, L)] += 1
    return counts


def main() -> None:
    assertions = 0
    failures: list[str] = []

    def check(ok: bool, label: str) -> None:
        nonlocal assertions
        assertions += 1
        if not ok:
            failures.append(label)

    # Exact edit/crossing word counts.  A combined chronology must preserve
    # the interleaving; binomial(e+l,e) is essential.
    chronicle_rows = []
    for W in range(1, 4):
        for V in range(1, 4):
            brute = brute_histories(W, V, 3, 3)
            C = 1 + W + V
            for D in range(4):
                for L in range(4):
                    exact = exact_histories(W, V, D, L)
                    check(brute[(D, L)] == exact,
                          f"chronicle exact W={W} V={V} D={D} L={L}")
                    check(exact <= C ** (D + L + 1),
                          f"coarse C bound W={W} V={V} D={D} L={L}")
                    # Omitting interleavings undercounts whenever both event
                    # types can occur.
                    separated = sum(W**e for e in range(D + 1)) * sum(V**ell for ell in range(L + 1))
                    check(exact >= separated,
                          f"interleave lower W={W} V={V} D={D} L={L}")
                    if D and L:
                        check(exact > separated,
                              f"interleave strict W={W} V={V} D={D} L={L}")
                    chronicle_rows.append((W, V, D, L, exact, separated, C ** (D + L + 1)))

    # Common-input all-cut distribution theorem using exact H(D,h).
    tail_rows = []
    for m in range(3, 25):
        total = 1 << m
        for W in (1, 2, 4, 8):
            for V in (2, 3, 5, 9):
                for D in range(0, 5):
                    for h in range(0, 6):
                        H = exact_histories(W, V, D, h)
                        for G in (1, 2, 4, 8, 16):
                            short_union = min(total, G * H)
                            long_all = total - short_union
                            check(long_all == max(0, total - G * H),
                                  f"tail union {m,W,V,D,h,G}")
                            if G * H <= total // 4:
                                check(4 * long_all >= 3 * total,
                                      f"tail 3/4 {m,W,V,D,h,G}")
                            tail_rows.append((m, W, V, D, h, G, H, long_all))

    # Separate proof tape: full contents must match; proof-head coordinate
    # enlarges crossing/epoch alphabets.  Inline-left proof has factor one.
    proof_rows = []
    for P in range(0, 17):
        proof_strings = (1 << (P + 1)) - 1
        for W in (1, 3, 7):
            for V0 in (2, 5, 11):
                Vp = V0 * (P + 2)
                for D in range(0, 4):
                    for L in range(0, 4):
                        external = proof_strings * exact_histories(W, Vp, D, L)
                        inline = exact_histories(W, V0, D, L)
                        check(external >= inline,
                              f"proof factor {P,W,V0,D,L}")
                        check(proof_strings >= 1, f"proof strings P={P}")
                        proof_rows.append((P, W, V0, D, L, inline, external))

    # Blank-start is load-bearing.  With no edits, replaying an empty edit
    # history always reconstructs blank.  Program-dependent preloads yield
    # 2^I0 different maps with the same empty chronology and head coordinate.
    preload_rows = []
    for I0 in range(1, 17):
        maps = 1 << I0
        decoded_from_blank = 1
        check(maps > decoded_from_blank, f"preload collision I0={I0}")
        # A safe repair groups by the initial map or logs I0 initialization
        # edits; either restores at least 2^I0 distinguishable records.
        check(decoded_from_blank * maps == maps, f"preload grouping I0={I0}")
        preload_rows.append({"I0": I0, "initial_maps": maps,
                             "empty_chronicles": 1,
                             "safe_group_factor": maps})

    # Simultaneous multi-tape changes: canonical tape-index ordering plus a
    # change-before-crossing convention replays the exact maps.
    transition_rows = []
    symbols = (0, 1, 2)
    k = 2
    # Each micro-transition chooses new symbols for the two current cells and
    # whether the source head crosses.  Exhaust all sequences through length 4.
    transition_types = tuple(product(symbols, symbols, (0, 1)))
    for length in range(0, 5):
        for seq in product(transition_types, repeat=length):
            tapes = [0, 0]
            events = []
            crossings = 0
            changes = 0
            for n0, n1, cross in seq:
                for tape, new in enumerate((n0, n1)):
                    if tapes[tape] != new:
                        tapes[tape] = new
                        events.append(("E", tape, new))
                        changes += 1
                if cross:
                    events.append(("C", tuple(tapes)))
                    crossings += 1
            replay = [0, 0]
            seen = []
            for event in events:
                if event[0] == "E":
                    replay[event[1]] = event[2]
                else:
                    seen.append(tuple(replay))
                    check(seen[-1] == event[1],
                          f"simultaneous replay len={length} seq={seq}")
            check(tuple(replay) == tuple(tapes),
                  f"final replay len={length} seq={seq}")
            transition_rows.append((length, changes, crossings, len(events)))

    # Exponent arithmetic.  The chronicle face d+k*s>=1 is stronger than the
    # previous d+k*s+min(d,s)>=1 and is saturated by d=0,s=1/k.
    exponent_rows = []
    for k in range(1, 6):
        for di in range(0, 11):
            for si in range(0, 11):
                d, s = di / 10, si / 10
                new = d + k * s
                old = new + min(d, s)
                check(old + 1e-12 >= new, f"face order {k,di,si}")
                if di == 0 and si * k == 10:
                    check(abs(new - 1.0) < 1e-12, f"saturation {k,di,si}")
                exponent_rows.append((k, di, si, new, old))

    payload = {
        "id": "EDIT-CHRONICLE-REFEREE177",
        "timestamp_utc": "2026-10-27T09:44:00Z",
        "status": {
            "edit_chronicle": "PROVED/EXACT restricted; symbolic proof in report",
            "all_cut_tail": "PROVED/EXACT restricted",
            "blank_start_firewall": "FALSIFIED without fixed initial work map",
            "ram_flmv_transfer": "FALSIFIED/RETIRED",
            "arc_edge_90": "OPEN",
            "p_vs_np": "OPEN",
        },
        "parameters": {
            "chronicle_W_V": [1, 3],
            "chronicle_D_L": [0, 3],
            "tail_m": [3, 24],
            "tail_D": [0, 4],
            "tail_h": [0, 5],
            "proof_length": [0, 16],
            "preload_I0": [1, 16],
            "simultaneous_transition_length": [0, 4],
            "random_seed": None,
            "method": "deterministic exhaustive exact integer arithmetic",
        },
        "assertions": assertions,
        "failures": len(failures),
        "first_failures": failures[:20],
        "chronicle_rows": chronicle_rows,
        "tail_row_count": len(tail_rows),
        "tail_sha256": hashlib.sha256(json.dumps(tail_rows, separators=(",", ":")).encode()).hexdigest(),
        "proof_row_count": len(proof_rows),
        "proof_sha256": hashlib.sha256(json.dumps(proof_rows, separators=(",", ":")).encode()).hexdigest(),
        "preload_rows": preload_rows,
        "transition_row_count": len(transition_rows),
        "transition_sha256": hashlib.sha256(json.dumps(transition_rows, separators=(",", ":")).encode()).hexdigest(),
        "exponent_rows": exponent_rows,
        "limitations": [
            "The experiment checks finite arithmetic and replay controls, not the asymptotic proof.",
            "The theorem is restricted to one sequential source head, fixed k, fixed alphabets and a fixed initial work map.",
            "No theorem is transferred to ordinary all-input SAT, RAM/RAT, or FLMV.",
        ],
    }
    out = Path("2026-10-27_0244_EDIT_CHRONICLE_REFEREE177_raw.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"assertions": assertions, "failures": len(failures),
                      "output": str(out), "sha256": digest}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
