#!/usr/bin/env python3
"""Finite audit for the complete total virtual-input interface.

This is not a native FLMV implementation and proves no SAT running-time bound.
It checks that a total logical-symbol accessor (including blank symbols outside
the encoded interval) is observationally identical to a physical read-only
input for exhaustive and seeded guest traces, including far jumps and later
ordinary-move re-entry.  It also exhibits failures of sticky-OOB and
valid-domain-only substitutes on the same SAT and UNSAT sources.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path


SEED = 1448226
OPS = ("L", "R", "READ", "J0", "JEND", "JFAR", "J2FAR")


def formula_length(formula: list[list[int]]) -> int:
    return 16 + 27 * len(formula)


def uint8_bits(value: int) -> str:
    assert 0 <= value < 256
    return f"{value:08b}"


def literal_bits(lit: int) -> str:
    assert 1 <= abs(lit) < 256
    return ("1" if lit < 0 else "0") + uint8_bits(abs(lit))


def physical_encoding(formula: list[list[int]], nvars: int) -> str:
    assert len(formula) < 256 and nvars < 256
    assert all(len(c) == 3 for c in formula)
    return uint8_bits(nvars) + uint8_bits(len(formula)) + "".join(
        literal_bits(lit) for clause in formula for lit in clause
    )


class LocalAccessor:
    """Exact length plus total symbol function, without storing the child."""

    def __init__(self, formula: list[list[int]], nvars: int):
        self.formula = formula
        self.nvars = nvars
        self.length = formula_length(formula)
        self.calls = 0
        self.in_range_calls = 0
        self.source_literal_probes = 0
        self.address_arithmetic = 0

    def symbol(self, index: int) -> str:
        self.calls += 1
        self.address_arithmetic += 1
        if index < 0 or index >= self.length:
            return "_"
        self.in_range_calls += 1
        if index < 8:
            return uint8_bits(self.nvars)[index]
        if index < 16:
            return uint8_bits(len(self.formula))[index - 8]
        q = index - 16
        record, offset = divmod(q, 9)
        clause, slot = divmod(record, 3)
        lit = self.formula[clause][slot]
        self.source_literal_probes += 1
        return literal_bits(lit)[offset]


def physical_symbol(bits: str, index: int) -> str:
    return bits[index] if 0 <= index < len(bits) else "_"


def sat_label(formula: list[list[int]], nvars: int) -> tuple[bool, int]:
    models = 0
    for mask in range(1 << nvars):
        if all(any(((mask >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)
                   for lit in clause) for clause in formula):
            models += 1
    return models > 0, models


@dataclass(eq=True)
class GuestState:
    head: int = 0
    reads: int = 0
    moves: int = 0
    jumps: int = 0
    checksum: int = 0
    blank_reads: int = 0
    work_mask: int = 0
    halted: bool = False


def jump_target(op: str, m: int) -> int:
    return {
        "J0": 0,
        "JEND": m - 1,
        "JFAR": m + 3,
        "J2FAR": 2 * m + 5,
    }[op]


def run_trace(symbol, m: int, trace: tuple[str, ...]) -> GuestState:
    state = GuestState()
    for op in trace:
        if state.halted:
            break
        if op == "L":
            state.head = max(0, state.head - 1)
            state.moves += 1
        elif op == "R":
            state.head += 1
            state.moves += 1
        elif op == "READ":
            bit = symbol(state.head)
            state.reads += 1
            if bit == "_":
                state.blank_reads += 1
                code = 2
            else:
                code = int(bit)
            # Guest-visible control and work state depend on every read.
            state.checksum = (state.checksum * 5 + code + state.head) % 65521
            state.work_mask ^= (code + 1) << (state.reads % 13)
        elif op.startswith("J"):
            state.head = jump_target(op, m)
            state.jumps += 1
        else:
            raise AssertionError(op)
    return state


def sticky_accessor(bits: str):
    oob = False

    def symbol(index: int) -> str:
        nonlocal oob
        if oob:
            return "_"
        if 0 <= index < len(bits):
            return bits[index]
        oob = True
        return "_"

    return symbol


def valid_only_accessor(bits: str):
    def symbol(index: int) -> str:
        if not 0 <= index < len(bits):
            raise IndexError(index)
        return bits[index]

    return symbol


def head_bound_checks() -> int:
    checks = 0
    for s in range(1, 13):
        for t in (0, 1, 2, 7, 31, 127, 1023):
            start = (1 << s) - 1
            maximum = start + t
            bound = s + math.ceil(math.log2(t + 1)) + 1
            assert max(1, maximum.bit_length()) <= bound
            checks += 1
    return checks


def audit_case(name: str, formula: list[list[int]], nvars: int) -> dict:
    bits = physical_encoding(formula, nvars)
    accessor = LocalAccessor(formula, nvars)
    assert len(bits) == accessor.length
    for index in range(-4, len(bits) + 5):
        assert accessor.symbol(index) == physical_symbol(bits, index)

    exhaustive = 0
    for length in range(6):
        for trace in itertools.product(OPS, repeat=length):
            p = run_trace(lambda i: physical_symbol(bits, i), len(bits), trace)
            v = run_trace(accessor.symbol, len(bits), trace)
            assert p == v
            exhaustive += 1

    rng = random.Random(SEED + len(formula))
    randomized = 0
    for _ in range(5000):
        trace = tuple(rng.choice(OPS) for _ in range(20))
        assert run_trace(lambda i: physical_symbol(bits, i), len(bits), trace) == run_trace(
            accessor.symbol, len(bits), trace
        )
        randomized += 1

    # Read blank three cells beyond the end, move left four times, then read m-1.
    reentry = ("JFAR", "READ", "L", "L", "L", "L", "READ")
    physical = run_trace(lambda i: physical_symbol(bits, i), len(bits), reentry)
    virtual = run_trace(accessor.symbol, len(bits), reentry)
    sticky = run_trace(sticky_accessor(bits), len(bits), reentry)
    assert physical == virtual
    assert sticky != physical
    valid_only_failed = False
    try:
        run_trace(valid_only_accessor(bits), len(bits), ("JFAR", "READ"))
    except IndexError:
        valid_only_failed = True
    assert valid_only_failed

    label, models = sat_label(formula, nvars)
    return {
        "name": name,
        "nvars": nvars,
        "clauses": len(formula),
        "encoded_bits": len(bits),
        "SAT": label,
        "models": models,
        "exhaustive_traces": exhaustive,
        "seeded_traces": randomized,
        "trace_max_length": 20,
        "total_accessor": {
            "calls": accessor.calls,
            "in_range_calls": accessor.in_range_calls,
            "out_of_range_calls": accessor.calls - accessor.in_range_calls,
            "source_literal_probes": accessor.source_literal_probes,
            "address_arithmetic_events": accessor.address_arithmetic,
        },
        "reentry_trace": list(reentry),
        "reentry_physical_state": asdict(physical),
        "reentry_virtual_state": asdict(virtual),
        "sticky_state": asdict(sticky),
        "sticky_matches_physical": sticky == physical,
        "valid_domain_only_failed_on_oob": valid_only_failed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    sat_formula = [[1, 2, 3], [-1, 2, 3]]
    # All eight falsifying sign patterns: every assignment falsifies one clause.
    unsat_formula = []
    for mask in range(8):
        unsat_formula.append([
            -v if (mask >> (v - 1)) & 1 else v for v in (1, 2, 3)
        ])

    cases = [
        audit_case("proper_3cnf_SAT", sat_formula, 3),
        audit_case("all_sign_patterns_UNSAT", unsat_formula, 3),
    ]
    assert cases[0]["SAT"] and not cases[1]["SAT"]
    result = {
        "id": "ARC-TOTAL-VIRTUAL-INPUT-RECONCILIATION226",
        "date": "2026-10-30",
        "seed": SEED,
        "scope": "finite interface audit; not native FLMV timing and not a SAT contraction",
        "claim_tested": "exact total logical input accessor equals a physical read-only input under jumps, ordinary moves, out-of-range blanks, and re-entry",
        "operation_alphabet": list(OPS),
        "head_bound_checks": head_bound_checks(),
        "cases": cases,
        "totals": {
            "same_state_traces": sum(c["exhaustive_traces"] + c["seeded_traces"] for c in cases),
            "exhaustive_traces": sum(c["exhaustive_traces"] for c in cases),
            "seeded_traces": sum(c["seeded_traces"] for c in cases),
            "sticky_counterexamples": sum(not c["sticky_matches_physical"] for c in cases),
            "valid_domain_only_counterexamples": sum(c["valid_domain_only_failed_on_oob"] for c in cases),
        },
        "limitations": [
            "Host-language states and event counts are not FLMV native TM steps.",
            "No power-short SAT child is constructed.",
            "Finite trace agreement does not prove the general simulation theorem.",
            "The symbolic theorem requires exact length, complete ordinary encoding, and charged accessor costs.",
        ],
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
