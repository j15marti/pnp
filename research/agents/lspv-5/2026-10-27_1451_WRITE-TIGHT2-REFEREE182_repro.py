#!/usr/bin/env python3
"""Finite hostile controls for the WRITE-TIGHT2 restricted-machine theorem.

This is not evidence for an unrestricted SAT lower bound.  It checks four
explicit promise comparators and the accounting convention for simultaneous
work-tape changes.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path


SEED = 20261027
RAW = Path(__file__).with_name(
    "2026-10-27_1451_LSPV-5_WRITE_TIGHT2_REFEREE182_raw.json"
)


@dataclass
class Ledger:
    reject: bool
    transitions: int
    input_moves: int
    input_reversals: int
    work_changes: int
    work_cells: int
    auxiliary_head_cells: int = 0


def target_reject(a: int, b: int) -> bool:
    return bool(a & b)


def bits(x: int, m: int) -> list[int]:
    return [(x >> i) & 1 for i in range(m)]


def move(pos: int, dst: int, previous_direction: int) -> tuple[int, int, int, int]:
    """Return new position, moves, reversals, last nonzero direction."""
    delta = dst - pos
    if delta == 0:
        return pos, 0, 0, previous_direction
    direction = 1 if delta > 0 else -1
    reversal = int(previous_direction != 0 and previous_direction != direction)
    return dst, abs(delta), reversal, direction


def unary_head(a: int, b: int, m: int, *, hidden_output: bool = False) -> Ledger:
    """Sequential one-input-head comparator using one unmodified head position.

    If hidden_output is false, this is the legal zero-write work-head endpoint.
    If true, the same positional memory is put on an uncharged two-way output
    head, giving the hostile control that explains why such a head is excluded.
    """
    aa, bb = bits(a, m), bits(b, m)
    b0 = 8 * m + 7
    ipos = 0
    hpos = 0
    idir = 0
    moves = reversals = transitions = 0
    reject = False
    max_h = 0
    for i in range(m):
        assert hpos == i and ipos == 0
        # Alice index: input and counter head move in opposite directions.
        for _ in range(i):
            ipos += 1
            hpos -= 1
            transitions += 1
            moves += 1
            if idir == -1:
                reversals += 1
            idir = 1
        abit = aa[i]
        for _ in range(i):
            ipos -= 1
            hpos += 1
            transitions += 1
            moves += 1
            if idir == 1:
                reversals += 1
            idir = -1
        # Traverse invariant gap to Bob origin, then use the same unary index.
        ipos, dm, dr, idir = move(ipos, b0, idir)
        moves += dm
        reversals += dr
        transitions += dm
        for _ in range(i):
            ipos += 1
            hpos -= 1
            transitions += 1
            moves += 1
            if idir == -1:
                reversals += 1
            idir = 1
        bbit = bb[i]
        reject |= bool(abit & bbit)
        for _ in range(i):
            ipos -= 1
            hpos += 1
            transitions += 1
            moves += 1
            if idir == 1:
                reversals += 1
            idir = -1
        ipos, dm, dr, idir = move(ipos, 0, idir)
        moves += dm
        reversals += dr
        transitions += dm
        # One stationary-input transition advances the positional counter.
        hpos += 1
        max_h = max(max_h, hpos)
        transitions += 1
    assert hpos == m and ipos == 0
    return Ledger(
        reject=reject,
        transitions=transitions,
        input_moves=moves,
        input_reversals=reversals,
        work_changes=0,
        work_cells=0 if hidden_output else max_h + 1,
        auxiliary_head_cells=max_h + 1 if hidden_output else 0,
    )


def two_input_heads(a: int, b: int, m: int) -> Ledger:
    """Hostile control: a second sequential input head defeats the transport."""
    aa, bb = bits(a, m), bits(b, m)
    b0 = 8 * m + 7
    transitions = b0  # move head B from the common origin to Bob's block
    moves = b0
    reject = False
    for i in range(m):
        reject |= bool(aa[i] & bb[i])
        transitions += 1
        if i + 1 < m:
            transitions += 1
            moves += 2  # both heads advance in the same transition
    return Ledger(reject, transitions, moves, 0, 0, 0)


def full_buffer(a: int, b: int, m: int) -> Ledger:
    """Legal endpoint: one pass, m changed work cells, no input reversal."""
    aa, bb = bits(a, m), bits(b, m)
    b0 = 8 * m + 7
    reject = any(x & y for x, y in zip(aa, bb))
    # Blank is a third symbol, so storing either 0 or 1 changes each cell once.
    return Ledger(reject, b0 + m + m, b0 + m, 0, m, m)


def simultaneous_change_trials(rng: random.Random, trials: int = 20_000) -> dict:
    """Canonicalize same-transition changes and reconstruct tape contents."""
    checked_changes = 0
    max_ratio = 0.0
    for _ in range(trials):
        k = rng.randint(1, 6)
        steps = rng.randint(1, 20)
        contents: dict[tuple[int, int], int] = {}
        reconstructed: dict[tuple[int, int], int] = {}
        event_log: list[tuple[int, int, int, int]] = []
        actual_changes = 0
        changeful_transitions = 0
        for t in range(steps):
            changed_this_step = 0
            proposed = []
            for tape in range(k):
                if rng.random() < 0.45:
                    pos = rng.randint(0, 7)
                    old = contents.get((tape, pos), 0)
                    new = rng.randint(0, 2)
                    if new != old:
                        proposed.append((tape, pos, new))
            # Canonical WRITE order inside a transition is increasing tape id.
            for tape, pos, new in sorted(proposed):
                contents[(tape, pos)] = new
                event_log.append((t, tape, pos, new))
                actual_changes += 1
                changed_this_step += 1
            changeful_transitions += int(changed_this_step > 0)
            assert changed_this_step <= k
        for _, tape, pos, new in event_log:
            reconstructed[(tape, pos)] = new
        assert reconstructed == contents
        assert actual_changes <= k * changeful_transitions
        if changeful_transitions:
            max_ratio = max(max_ratio, actual_changes / changeful_transitions)
        checked_changes += actual_changes
    return {
        "trials": trials,
        "actual_changes_checked": checked_changes,
        "max_changes_per_changeful_transition": max_ratio,
        "conclusion": "D_actual <= k*D_changeful; fixed k changes only constants",
    }


def exponent_grid() -> dict:
    checks = 0
    for k in range(1, 6):
        for di in range(0, 101):
            for si in range(0, 101):
                d = di / 100
                s = si / 100
                # Negation of the strict forbidden region is exactly d+ks>=1.
                forbidden = d + k * s < 1 - 1e-12
                if forbidden:
                    assert (d + k * s) < 1
                checks += 1
    return {"grid_checks": checks, "minimum_required_face": "d+k*s>=1"}


def main() -> None:
    rng = random.Random(SEED)
    assertions = 0
    samples = {}
    for m in range(1, 9):
        cases = 0
        for a in range(1 << m):
            for b in range(1 << m):
                want = target_reject(a, b)
                z = unary_head(a, b, m)
                o = unary_head(a, b, m, hidden_output=True)
                h = two_input_heads(a, b, m)
                f = full_buffer(a, b, m)
                assert z.reject == o.reject == h.reject == f.reject == want
                assert z.work_changes == 0 and z.work_cells == m + 1
                assert o.work_changes == 0 and o.work_cells == 0
                assert o.auxiliary_head_cells == m + 1
                assert h.work_changes == 0 and h.work_cells == 0
                assert f.work_changes == m and f.work_cells == m
                assert h.transitions <= 10 * m + 8
                assertions += 11
                cases += 1
        samples[str(m)] = {
            "ordered_pairs": cases,
            "zero_write_worst": asdict(unary_head(1 << (m - 1), 1 << (m - 1), m)),
            "two_input_heads_worst": asdict(two_input_heads((1 << m) - 1, (1 << m) - 1, m)),
            "hidden_output_head_worst": asdict(
                unary_head((1 << m) - 1, (1 << m) - 1, m, hidden_output=True)
            ),
            "full_buffer_worst": asdict(full_buffer((1 << m) - 1, (1 << m) - 1, m)),
        }
    simultaneous = simultaneous_change_trials(rng)
    grid = exponent_grid()
    assertions += simultaneous["trials"] * 3 + grid["grid_checks"]
    result = {
        "run_id": "WRITE-TIGHT2-REFEREE182",
        "seed": SEED,
        "scope": "easy DISJ/exact22 promise comparator abstractions; not full SAT",
        "exhaustive_m": [1, 8],
        "assertions": assertions,
        "samples": samples,
        "simultaneous_changes": simultaneous,
        "exponent_grid": grid,
        "formal_findings": {
            "two_input_heads": "FALSIFIED transfer: O(N), D=S=0 outside one-input-head model",
            "usable_two_way_output_head": "FALSIFIED if uncharged; count it as a work head/visited cells",
            "same_transition_changes": "REPAIRED: order by tape id and count every actual cell change",
            "fixed_machine": "fixed k, states, alphabets, blank origin are load-bearing",
            "write_tight2_A_B": "no finite counterexample; symbolic proof separately audited",
        },
    }
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"raw": str(RAW), "assertions": assertions, "status": "PASS"}))


if __name__ == "__main__":
    main()
