#!/usr/bin/env python3
"""Exact Gaussian-subset counterexample and same-function circuit census."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


NAMES = ("a", "b", "t", "c", "d")
TARGET = (1, 1, 0, 0, 0)
XOR_ROWS = ((0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 0), (4, 0, 1))


def parity_rhs(row):
    return TARGET[row[0]] ^ TARGET[row[1]] ^ TARGET[row[2]]


def forbidden_clause(values, variables):
    # Signed 1-based literal tuple false exactly on the supplied assignment.
    return tuple((v + 1) if values[i] == 0 else -(v + 1) for i, v in enumerate(variables))


def xor3_cnf(row, rhs):
    clauses = []
    for a in range(8):
        vals = tuple((a >> i) & 1 for i in range(3))
        if (vals[0] ^ vals[1] ^ vals[2]) != rhs:
            clauses.append(forbidden_clause(vals, row))
    return tuple(clauses)


def and_cnf():
    # t=a AND b; c,d are proper-clause pads.
    return ((-1, -2, 3), (1, -3, 4), (1, -3, -4), (2, -3, 5), (2, -3, -5))


def clause_sat(clause, assignment):
    return any((assignment[abs(l)-1] == 1) if l > 0 else (assignment[abs(l)-1] == 0) for l in clause)


def formula_sat(clauses, assignment):
    return all(clause_sat(c, assignment) for c in clauses)


def gf2_rank(rows, ncols):
    xs = [sum(1 << c for c in row) for row in rows]
    rank = 0
    for col in range(ncols):
        pivot = next((i for i in range(rank, len(xs)) if (xs[i] >> col) & 1), None)
        if pivot is None:
            continue
        xs[rank], xs[pivot] = xs[pivot], xs[rank]
        for i in range(len(xs)):
            if i != rank and ((xs[i] >> col) & 1):
                xs[i] ^= xs[rank]
        rank += 1
    return rank


class Circuit:
    MOS = {"INV": 2, "OR2": 6, "AND2": 6, "XOR2": 16}

    def __init__(self, n_inputs=5):
        self.n_inputs = n_inputs
        self.gates = []
        self.output = None

    def add(self, op, *args):
        name = f"g{len(self.gates)}"
        self.gates.append((name, op, args))
        return name

    def reduce(self, op, wires):
        wires = list(wires)
        while len(wires) > 1:
            nxt = []
            for i in range(0, len(wires), 2):
                nxt.append(self.add(op, wires[i], wires[i+1]) if i + 1 < len(wires) else wires[i])
            wires = nxt
        return wires[0]

    def values(self, assignment):
        env = {f"x{i}": assignment[i] for i in range(self.n_inputs)}
        for name, op, args in self.gates:
            xs = [env[x] for x in args]
            env[name] = {"INV": lambda: 1-xs[0], "OR2": lambda: xs[0] | xs[1], "AND2": lambda: xs[0] & xs[1], "XOR2": lambda: xs[0] ^ xs[1]}[op]()
        return env

    def depth(self):
        dep = {f"x{i}": 0 for i in range(self.n_inputs)}
        for name, _, args in self.gates:
            dep[name] = 1 + max(dep[x] for x in args)
        return dep[self.output]

    def census(self):
        fanout = Counter()
        for _, _, args in self.gates:
            fanout.update(args)
        fanout[self.output] += 1  # primary output sink
        buffers = sum(max(0, d-2) for d in fanout.values())
        counts = Counter(op for _, op, _ in self.gates)
        g = len(self.gates)
        p_in = sum(len(args) for _, _, args in self.gates)
        p_out = g
        gray = [i ^ (i >> 1) for i in range(1 << self.n_inputs)]
        toggles = 0
        prev = None
        for a in gray:
            assignment = tuple((a >> i) & 1 for i in range(self.n_inputs))
            vals = self.values(assignment)
            now = tuple(vals[name] for name, _, _ in self.gates)
            if prev is not None:
                toggles += sum(x != y for x, y in zip(prev, now))
            prev = now
        mos = sum(self.MOS[op] for _, op, _ in self.gates)
        return {
            "gate_types": dict(counts), "G": g, "P_in": p_in, "P_out": p_out,
            "E_including_output_sink": p_in + 1, "W": self.n_inputs + g,
            "max_fanout_pin_loads": max(fanout.values()), "fanout2_buffers": buffers,
            "nominal_MOS": mos, "nominal_MOS_with_buffers": mos + 4*buffers,
            "depth": self.depth(), "Gray_gate_output_toggles": toggles,
            "routed_wirelength": None, "placed_area": None, "transistor_nets": None,
            "measured_energy": None,
        }


def raw_circuit(clauses):
    c = Circuit()
    inv = [c.add("INV", f"x{i}") for i in range(5)]
    sats = []
    for clause in clauses:
        wires = [(f"x{abs(l)-1}" if l > 0 else inv[abs(l)-1]) for l in clause]
        sats.append(c.reduce("OR2", wires))
    c.output = c.reduce("AND2", sats)
    return c


def macro_circuit():
    c = Circuit()
    sats = []
    for row in XOR_ROWS:
        q = c.add("XOR2", f"x{row[0]}", f"x{row[1]}")
        p = c.add("XOR2", q, f"x{row[2]}")
        sats.append(p if parity_rhs(row) == 1 else c.add("INV", p))
    h = c.add("AND2", "x0", "x1")
    e = c.add("XOR2", h, "x2")
    sats.append(c.add("INV", e))
    c.output = c.reduce("AND2", sats)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    xor_clauses = tuple(cl for row in XOR_ROWS for cl in xor3_cnf(row, parity_rhs(row)))
    nonlinear = and_cnf()
    full = xor_clauses + nonlinear
    failures = []
    if len(set(full)) != 25:
        failures.append(f"clause_distinctness:{len(set(full))}")
    if gf2_rank(XOR_ROWS, 5) != 5:
        failures.append("xor_rank")

    xor_models, full_models = [], []
    for a in range(32):
        assignment = tuple((a >> i) & 1 for i in range(5))
        if formula_sat(xor_clauses, assignment):
            xor_models.append(assignment)
        if formula_sat(full, assignment):
            full_models.append(assignment)
    if xor_models != [TARGET]:
        failures.append(f"xor_models:{xor_models}")
    if full_models:
        failures.append(f"full_models:{full_models}")

    raw, macro = raw_circuit(full), macro_circuit()
    circuit_mismatches = 0
    for a in range(32):
        assignment = tuple((a >> i) & 1 for i in range(5))
        expected = int(formula_sat(full, assignment))
        for circ in (raw, macro):
            if circ.values(assignment)[circ.output] != expected:
                circuit_mismatches += 1
    if circuit_mismatches:
        failures.append(f"circuit_mismatches:{circuit_mismatches}")

    raw_c = raw.census()
    macro_c = macro.census()
    result = {
        "artifact": "GAUSSIAN-NONLINEAR-GUARD9",
        "status": "PASS" if not failures else "FAIL",
        "variables": list(NAMES),
        "xor_matrix_rows": [[NAMES[i] for i in row] for row in XOR_ROWS],
        "xor_rhs": [parity_rhs(row) for row in XOR_ROWS],
        "xor_rank_GF2": gf2_rank(XOR_ROWS, 5),
        "proper_XOR_clauses": len(xor_clauses),
        "proper_AND_clauses": len(nonlinear),
        "distinct_proper_clauses": len(set(full)),
        "xor_only_models": [list(x) for x in xor_models],
        "full_models": [list(x) for x in full_models],
        "specialist_brief_discrepancy": "An invertible five-equation XOR system has one full five-variable extension, not four. The brief's simultaneous 'uniquely require' and '4 XOR-only extensions' claims cannot both hold without an unstated projection.",
        "primitive_library": "INV=2, OR2=6, AND2=6, XOR2=16, BUF2=4 nominal MOS",
        "raw_proper_CNF_evaluator": raw_c,
        "recovered_macro_evaluator": macro_c,
        "same_function_checks": 64,
        "source_recognition_lemma": {
            "statement": "An exact deterministic recognizer accepting one length-L word and rejecting every Hamming-distance-one neighbor must query all L positions on the accepted word.",
            "control_literal_tokens_L": 75,
            "MACRO9_d7_literal_tokens": 19722,
            "MACRO9_d7_single_literal_mutations_reported": 64,
            "status": "PROVED decision-tree adversary; the shared MACRO9 mutation suite does not cover all positions",
        },
        "failures": failures,
    }
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
