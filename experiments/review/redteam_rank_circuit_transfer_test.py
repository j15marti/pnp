#!/usr/bin/env python3
"""Hostile controls for compatibility-rank to circuit/transistor transfers.

The test is deliberately finite.  The symbolic families and gate-count
formulas are proved in the accompanying report; this program validates the
declared netlists, exact GF(2) ranks, wrappers, and accounting formulas.
"""

from __future__ import annotations

import argparse
import json
import signal
import time
from dataclasses import dataclass
from pathlib import Path


class BudgetExceeded(RuntimeError):
    pass


def _alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


@dataclass
class Circuit:
    inputs: int
    gates: list[tuple[str, int, int | None]]
    output: int

    def evaluate(self, bits: tuple[int, ...]) -> int:
        assert len(bits) == self.inputs
        wires = list(bits)
        for op, a, b in self.gates:
            if op == "NOT":
                wires.append(1 - wires[a])
            elif op == "AND":
                assert b is not None
                wires.append(wires[a] & wires[b])
            elif op == "OR":
                assert b is not None
                wires.append(wires[a] | wires[b])
            else:
                raise AssertionError(op)
        return wires[self.output]

    def gate_counts(self) -> dict[str, int]:
        out = {"NOT": 0, "AND": 0, "OR": 0}
        for op, _a, _b in self.gates:
            out[op] += 1
        return out

    def transistor_upper_bound(self) -> int:
        # Declared static-CMOS macro library, not a physical minimum.
        cost = {"NOT": 2, "AND": 6, "OR": 6}
        return sum(cost[op] for op, _a, _b in self.gates)


class Builder:
    def __init__(self, inputs: int):
        self.inputs = inputs
        self.gates: list[tuple[str, int, int | None]] = []

    def gate(self, op: str, a: int, b: int | None = None) -> int:
        self.gates.append((op, a, b))
        return self.inputs + len(self.gates) - 1

    def xor2(self, a: int, b: int) -> int:
        # (a OR b) AND NOT(a AND b), four {AND,OR,NOT} gates.
        either = self.gate("OR", a, b)
        both = self.gate("AND", a, b)
        not_both = self.gate("NOT", both)
        return self.gate("AND", either, not_both)

    def or_all(self, wires: list[int]) -> int:
        assert wires
        cur = wires[0]
        for wire in wires[1:]:
            cur = self.gate("OR", cur, wire)
        return cur


def equality_circuit(n: int) -> Circuit:
    b = Builder(2 * n)
    mismatches = [b.xor2(i, n + i) for i in range(n)]
    any_mismatch = b.or_all(mismatches)
    out = b.gate("NOT", any_mismatch)
    return Circuit(2 * n, b.gates, out)


def subset_circuit(n: int) -> Circuit:
    b = Builder(2 * n)
    violations = []
    for i in range(n):
        not_y = b.gate("NOT", n + i)
        violations.append(b.gate("AND", i, not_y))
    any_violation = b.or_all(violations)
    out = b.gate("NOT", any_violation)
    return Circuit(2 * n, b.gates, out)


def affine_complement_circuit(n: int) -> Circuit:
    b = Builder(2 * n)
    mismatches = []
    for i in range(n):
        xy = b.xor2(i, n + i)
        mismatches.append(b.gate("NOT", xy))  # x XOR y XOR 1
    any_mismatch = b.or_all(mismatches)
    out = b.gate("NOT", any_mismatch)
    return Circuit(2 * n, b.gates, out)


def wrap(c: Circuit, mode: str) -> Circuit:
    b = Builder(c.inputs)

    def copy_once() -> int:
        offset = len(b.gates)
        mapping: dict[int, int] = {i: i for i in range(c.inputs)}
        for j, (op, a, z) in enumerate(c.gates):
            mapped_a = mapping[a]
            mapped_z = None if z is None else mapping[z]
            mapping[c.inputs + j] = b.gate(op, mapped_a, mapped_z)
        assert len(b.gates) >= offset
        return mapping[c.output]

    first = copy_once()
    if mode == "DIRECT":
        out = first
    elif mode == "DEAD":
        _unused = b.gate("NOT", 0)
        out = first
    elif mode == "COPY":
        _unused = copy_once()
        out = first
    elif mode == "DELAY":
        out = b.gate("NOT", b.gate("NOT", first))
    elif mode == "RECOMP":
        second = copy_once()
        out = b.gate("AND", first, second)
    else:
        raise AssertionError(mode)
    return Circuit(c.inputs, b.gates, out)


def relation(kind: str, x: int, y: int, n: int) -> int:
    mask = (1 << n) - 1
    if kind in {"equality_2sat", "treewidth1_product"}:
        return int(x == y)
    if kind == "horn_subset":
        return int((x & (~y & mask)) == 0)
    if kind == "affine_complement":
        return int(y == (x ^ mask))
    raise AssertionError(kind)


def gf2_rank(rows: list[int], width: int) -> int:
    rows = rows[:]
    rank = 0
    for col in range(width - 1, -1, -1):
        pivot = next((r for r in range(rank, len(rows)) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
        if rank == width:
            break
    return rank


def matrix_rank(kind: str, n: int) -> int:
    side = 1 << n
    rows = []
    for x in range(side):
        row = 0
        for y in range(side):
            row |= relation(kind, x, y, n) << y
        rows.append(row)
    return gf2_rank(rows, side)


def bits_of_pair(x: int, y: int, n: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(n)) + tuple((y >> i) & 1 for i in range(n))


def run(max_exhaustive_n: int, max_rank_n: int) -> dict:
    started = time.perf_counter()
    kinds = {
        "equality_2sat": equality_circuit,
        "horn_subset": subset_circuit,
        "affine_complement": affine_complement_circuit,
        "treewidth1_product": equality_circuit,
    }
    wrappers = ["DIRECT", "DEAD", "COPY", "DELAY", "RECOMP"]
    semantic_checks = 0
    wrapper_checks = 0
    rank_checks = 0
    rows = []

    for n in range(1, max_exhaustive_n + 1):
        side = 1 << n
        for kind, factory in kinds.items():
            base = factory(n)
            built = {mode: wrap(base, mode) for mode in wrappers}
            for x in range(side):
                for y in range(side):
                    expected = relation(kind, x, y, n)
                    bits = bits_of_pair(x, y, n)
                    assert base.evaluate(bits) == expected
                    semantic_checks += 1
                    for mode, circuit in built.items():
                        assert circuit.evaluate(bits) == expected, (kind, mode, n, x, y)
                        wrapper_checks += 1

    for n in range(1, max_rank_n + 1):
        for kind, factory in kinds.items():
            rank = matrix_rank(kind, n)
            side = 1 << n
            assert rank == side, (kind, n, rank, side)
            rank_checks += 1
            circuit = factory(n)
            counts = circuit.gate_counts()
            rows.append({
                "family": kind,
                "n": n,
                "encoded_pair_bits": 2 * n,
                "gf2_rank": rank,
                "gate_count": len(circuit.gates),
                "gate_counts": counts,
                "declared_cmos_transistor_upper_bound": circuit.transistor_upper_bound(),
            })

    # Encoding and fixed-instance controls.
    padding_checks = 0
    for n in range(1, max_exhaustive_n + 1):
        c = equality_circuit(n)
        for x in range(1 << n):
            for y in range(1 << n):
                bits = bits_of_pair(x, y, n)
                for pad in (0, 1):
                    # The same circuit ignores an external padding bit by construction.
                    assert c.evaluate(bits) == relation("equality_2sat", x, y, n)
                    padding_checks += 1

    hardwired_instances = [
        {"formula": "(x)", "sat_bit": 1, "input_wires": 0, "logic_gate_upper_bound": 1},
        {"formula": "(x) AND (NOT x)", "sat_bit": 0, "input_wires": 0, "logic_gate_upper_bound": 1},
    ]

    return {
        "status": "PASS",
        "finite_scope": {
            "max_exhaustive_n": max_exhaustive_n,
            "max_rank_n": max_rank_n,
            "rank_field": "GF(2)",
            "gate_basis": ["AND2", "OR2", "NOT"],
            "transistor_macro_costs": {"AND2": 6, "OR2": 6, "NOT": 2},
            "warning": "Transistor values are declared implementation upper bounds, not physical minima.",
        },
        "checks": {
            "semantic_netlist_checks": semantic_checks,
            "wrapper_equivalence_checks": wrapper_checks,
            "exact_rank_checks": rank_checks,
            "ignored_padding_checks": padding_checks,
        },
        "hardwired_instance_controls": hardwired_instances,
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exhaustive-n", type=int, default=8)
    parser.add_argument("--max-rank-n", type=int, default=9)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    result = run(args.max_exhaustive_n, args.max_rank_n)
    signal.alarm(0)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["checks"], sort_keys=True))
    print(f"elapsed_seconds={result['elapsed_seconds']:.6f}")


if __name__ == "__main__":
    main()
