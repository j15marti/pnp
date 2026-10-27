#!/usr/bin/env python3
"""Physical-head controls for the k-dimensional zero-write endpoint.

The simulated machine has one sequential read-only input head and k fixed
blank work tapes.  The host's Python indices are instrumentation only: every
simulated input/work-head move is charged.  No work symbol is ever changed.
"""

from __future__ import annotations

import itertools
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path


SEED = 20261027
RAW = Path(__file__).with_name(
    "2026-10-27_1550_LSPV-5_KDIM_ZEROWRITE_SATURATION183_raw.json"
)


@dataclass
class Ledger:
    reject: bool
    transitions: int
    input_moves: int
    reversals: int
    crossings: int
    work_cells: int
    work_changes: int
    max_work_positions: list[int]


def bits_little(x: int, m: int) -> list[int]:
    return [(x >> i) & 1 for i in range(m)]


def encode_tensor(bit_values: list[int], k: int, B: int) -> str:
    """Fixed-k hierarchical encoding with one delimiter per outer level."""
    it = iter("1" if b else "0" for b in bit_values)

    def rec(level: int) -> str:
        if level == k - 1:
            return "".join(next(it) for _ in range(B))
        sep = chr(ord("a") + level)
        return sep.join(rec(level + 1) for _ in range(B))

    out = rec(0)
    try:
        next(it)
        raise AssertionError("unused tensor bit")
    except StopIteration:
        return out


class PhysicalMachine:
    def __init__(self, tape: str, k: int, a_start: int, b_start: int, cut: int):
        self.tape = tape
        self.k = k
        self.a_start = a_start
        self.b_start = b_start
        self.cut = cut
        self.ipos = a_start
        self.heads = [0] * k
        self.max_heads = [0] * k
        self.transitions = 0
        self.input_moves = 0
        self.reversals = 0
        self.last_dir = 0
        self.crossings = 0
        self.cross_history: list[tuple] = []

    def step(
        self,
        input_delta: int = 0,
        work_index: int | None = None,
        work_delta: int = 0,
        state: str = "SCAN",
        cache: int | None = None,
    ) -> None:
        assert input_delta in (-1, 0, 1)
        assert work_delta in (-1, 0, 1)
        old = self.ipos
        if input_delta:
            direction = input_delta
            if self.last_dir and self.last_dir != direction:
                self.reversals += 1
            self.last_dir = direction
            self.ipos += input_delta
            assert 0 <= self.ipos < len(self.tape)
            self.input_moves += 1
            crossed = (old < self.cut <= self.ipos) or (self.ipos < self.cut <= old)
            if crossed:
                self.crossings += 1
                self.cross_history.append(
                    (direction, state, tuple(self.heads), cache)
                )
        if work_index is not None:
            self.heads[work_index] += work_delta
            assert self.heads[work_index] >= 0
            self.max_heads[work_index] = max(
                self.max_heads[work_index], self.heads[work_index]
            )
        self.transitions += 1

    def move_input(self, target: int, state: str, cache: int | None = None) -> None:
        while self.ipos < target:
            self.step(1, state=state, cache=cache)
        while self.ipos > target:
            self.step(-1, state=state, cache=cache)

    def fetch(self, start: int) -> tuple[int | None, int | None]:
        """Fetch tensor coordinate encoded by work-head positions.

        Returns (bit, None) on success or (None, overflowing_level).  All
        temporary input/work-head motion is structurally reversed before
        return.  No move log is retained: delimiter-driven backtracking uses
        only the fixed recursive control depth k, so it compiles into finite
        state for each fixed k.
        """
        self.move_input(start, "TO_BLOCK")
        initial_heads = tuple(self.heads)

        def seek(level: int) -> tuple[int | None, int | None]:
            if level == self.k - 1:
                while self.heads[level] > 0:
                    if self.tape[self.ipos] not in "01":
                        bit, overflow = None, level
                        break
                    self.step(1, level, -1, "FETCH_LEAF")
                else:
                    if self.tape[self.ipos] not in "01":
                        bit, overflow = None, level
                    else:
                        bit, overflow = int(self.tape[self.ipos]), None

                # Return to this leaf segment's left boundary, restoring the
                # coordinate once per crossed bit.  The predecessor symbol,
                # not an auxiliary counter or move log, detects the boundary.
                while self.ipos > 0 and self.tape[self.ipos - 1] in "01":
                    self.step(-1, level, 1, "UNFETCH_LEAF")
                return bit, overflow

            sep = chr(ord("a") + level)
            outer_terminators = {chr(ord("a") + j) for j in range(level)} | {
                "^",
                "#",
                "$",
            }
            while self.heads[level] > 0:
                while self.tape[self.ipos] != sep:
                    if self.tape[self.ipos] in outer_terminators:
                        bit, overflow = None, level
                        break
                    self.step(1, state="FETCH_SCAN")
                else:
                    self.step(1, level, -1, "FETCH_DESCEND")
                    continue
                break
            else:
                bit, overflow = seek(level + 1)

            # At this point the deeper call (if any) has returned to the
            # chosen child segment's left boundary.  Scan back to this
            # level's left boundary.  Crossing this level's separator is
            # precisely the inverse of a charged decrement above; all deeper
            # symbols are traversed without changing any work head.
            while self.ipos > 0 and self.tape[self.ipos - 1] not in outer_terminators:
                crossed = self.tape[self.ipos - 1]
                self.step(-1, state="UNFETCH_SCAN")
                if crossed == sep:
                    self.step(0, level, 1, "UNFETCH_ASCEND")
            return bit, overflow

        bit, overflow = seek(0)
        assert self.ipos == start
        assert tuple(self.heads) == initial_heads
        return bit, overflow

    def reset_head(self, j: int) -> None:
        while self.heads[j] > 0:
            self.step(0, j, -1, "CARRY_RESET")

    def run(self) -> Ledger:
        reject = False
        while True:
            abit, overflow = self.fetch(self.a_start)
            if overflow is not None:
                self.reset_head(overflow)
                if overflow == 0:
                    break
                self.step(0, overflow - 1, 1, "CARRY")
                continue
            assert abit is not None
            self.move_input(self.b_start, "TO_B", abit)
            bbit, bover = self.fetch(self.b_start)
            assert bover is None and bbit is not None
            if abit & bbit:
                reject = True
                break
            self.move_input(self.a_start, "TO_A")
            self.step(0, self.k - 1, 1, "INCREMENT")
        return Ledger(
            reject=reject,
            transitions=self.transitions,
            input_moves=self.input_moves,
            reversals=self.reversals,
            crossings=self.crossings,
            work_cells=sum(x + 1 for x in self.max_heads),
            work_changes=0,
            max_work_positions=self.max_heads,
        )


def build_machine(a: int, b: int, k: int, B: int) -> PhysicalMachine:
    m = B**k
    ae = encode_tensor(bits_little(a, m), k, B)
    be = encode_tensor(bits_little(b, m), k, B)
    gap = "X" * (8 * m + 1)
    tape = "^" + ae + "#" + gap + "#" + be + "$"
    a_start = 1
    b_start = tape.rindex("#") + 1
    gap_left = tape.index("#") + 1
    cut = gap_left + len(gap) // 2
    return PhysicalMachine(tape, k, a_start, b_start, cut)


def expected_reject(a: int, b: int) -> bool:
    return bool(a & b)


def checked_run(a: int, b: int, k: int, B: int) -> tuple[Ledger, tuple]:
    machine = build_machine(a, b, k, B)
    ledger = machine.run()
    assert ledger.reject == expected_reject(a, b)
    assert ledger.work_changes == 0
    assert ledger.work_cells <= k * (B + 1)
    if not ledger.reject:
        assert ledger.crossings == 2 * (B**k)
        assert ledger.work_cells == k * (B + 1)
        assert ledger.max_work_positions == [B] * k
    return ledger, tuple(machine.cross_history)


def exhaustive_small() -> tuple[int, dict]:
    configs = [(1, B) for B in range(1, 7)] + [(2, 1), (2, 2), (3, 1)]
    cases = 0
    summaries = {}
    for k, B in configs:
        m = B**k
        local = 0
        for a in range(1 << m):
            for b in range(1 << m):
                checked_run(a, b, k, B)
                local += 1
        summaries[f"k{k}_B{B}"] = local
        cases += local
    return cases, summaries


def sampled_larger(rng: random.Random) -> tuple[int, dict]:
    plans = [(2, 3, 2000), (3, 2, 2000), (4, 2, 1000), (5, 2, 250)]
    cases = 0
    summaries = {}
    for k, B, count in plans:
        m = B**k
        for _ in range(count):
            a = rng.randrange(1 << m)
            b = rng.randrange(1 << m)
            checked_run(a, b, k, B)
        summaries[f"k{k}_B{B}"] = count
        cases += count
    return cases, summaries


def diagonal_injectivity() -> tuple[int, dict]:
    configs = [(1, 8), (2, 3), (3, 2), (4, 1)]
    total = 0
    info = {}
    for k, B in configs:
        m = B**k
        seen = set()
        for a in range(1 << m):
            b = ((1 << m) - 1) ^ a
            ledger, hist = checked_run(a, b, k, B)
            assert not ledger.reject
            assert hist not in seen
            seen.add(hist)
        assert len(seen) == 1 << m
        info[f"k{k}_B{B}"] = len(seen)
        total += len(seen)
    return total, info


def scaling_controls() -> dict:
    plans = [(1, 256), (2, 16), (3, 6), (4, 4), (5, 3)]
    out = {}
    for k, B in plans:
        m = B**k
        # a=0, b=all ones is accepting and forces every coordinate check.
        ledger, _ = checked_run(0, (1 << m) - 1, k, B)
        assert ledger.crossings == 2 * m
        assert ledger.work_cells == k * (B + 1)
        out[f"k{k}_B{B}"] = {"m": m, **asdict(ledger)}
    return out


def main() -> None:
    rng = random.Random(SEED)
    exhaustive_cases, exhaustive = exhaustive_small()
    sampled_cases, sampled = sampled_larger(rng)
    histories, history_info = diagonal_injectivity()
    scaling = scaling_controls()
    result = {
        "run_id": "KDIM-ZEROWRITE-SATURATION183",
        "seed": SEED,
        "status": "PASS",
        "scope": "tagged k-dimensional DISJ promise; not canonical exact22 or full SAT",
        "exhaustive_cases": exhaustive_cases,
        "exhaustive_by_config": exhaustive,
        "sampled_cases": sampled_cases,
        "sampled_by_config": sampled,
        "injective_diagonal_histories": histories,
        "history_configs": history_info,
        "scaling_controls": scaling,
        "proved_target": {
            "resources": "D=W=0, S=k(B+1)=Theta(k*m^(1/k)), C=2m, T=O(mN)",
            "exponent_point": "(d,s)=(0,1/k), hence d+k*s=1",
            "quantifiers": "each fixed k has one fixed finite controller and alphabet",
        },
        "limitations": [
            "hierarchically tagged easy promise, not unchanged canonical exact22",
            "host recursion has fixed depth k and represents compiled finite control",
            "no RAM/FLMV/full-SAT transfer",
            "does not fill d>0 interior tradeoff",
        ],
    }
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "raw": str(RAW),
                "runs": exhaustive_cases + sampled_cases + histories + len(scaling),
            }
        )
    )


if __name__ == "__main__":
    main()
