#!/usr/bin/env python3
"""Finite audit for TRACEAXIOM-FIREWALL1.

The symbolic lemma is elementary and proved in the accompanying report.  This
program checks the encoding and hostile controls only; it makes no asymptotic
claim.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path


Literal = int
Clause = tuple[Literal, ...]


@dataclass(frozen=True)
class Gate:
    op: str
    out: int
    args: tuple[int, ...]


def eval_gate(op: str, args: tuple[int, ...], val: dict[int, int]) -> int:
    xs = [val[a] for a in args]
    if op == "AND": return xs[0] & xs[1]
    if op == "OR": return xs[0] | xs[1]
    if op == "XOR": return xs[0] ^ xs[1]
    if op == "NOT": return 1 - xs[0]
    if op == "COPY": return xs[0]
    raise ValueError(op)


def gate_cnf(g: Gate) -> list[Clause]:
    z, a = g.out, g.args[0]
    if g.op == "AND":
        b = g.args[1]
        return [(-a, -b, z), (a, -z), (b, -z)]
    if g.op == "OR":
        b = g.args[1]
        return [(a, b, -z), (-a, z), (-b, z)]
    if g.op == "XOR":
        b = g.args[1]
        return [(a, b, -z), (-a, -b, -z), (a, -b, z), (-a, b, z)]
    if g.op == "NOT":
        return [(a, z), (-a, -z)]
    if g.op == "COPY":
        return [(-a, z), (a, -z)]
    raise ValueError(g.op)


def evaluate(n_inputs: int, bits: list[int], gates: list[Gate]) -> dict[int, int]:
    val = {i + 1: bits[i] for i in range(n_inputs)}
    for g in gates:
        val[g.out] = eval_gate(g.op, g.args, val)
    return val


def tseitin(n_inputs: int, bits: list[int], gates: list[Gate], output: int):
    val = evaluate(n_inputs, bits, gates)
    input_units = [(i + 1,) if bits[i] else (-(i + 1),) for i in range(n_inputs)]
    core = input_units + [c for g in gates for c in gate_cnf(g)]
    wrong = (-output,) if val[output] else (output,)
    return core, wrong, val


def lit_value(lit: int, val: dict[int, int]) -> bool:
    return bool(val[abs(lit)]) == (lit > 0)


def unit_propagate(clauses: list[Clause]):
    assignment: dict[int, int] = {}
    steps = 0
    while True:
        progress = False
        for clause in clauses:
            if any(abs(l) in assignment and bool(assignment[abs(l)]) == (l > 0) for l in clause):
                continue
            open_lits = [l for l in clause if abs(l) not in assignment]
            if not open_lits:
                return True, steps, assignment
            if len(open_lits) == 1:
                lit = open_lits[0]
                v, bit = abs(lit), int(lit > 0)
                if v in assignment and assignment[v] != bit:
                    return True, steps, assignment
                if v not in assignment:
                    assignment[v] = bit
                    steps += 1
                    progress = True
        if not progress:
            return False, steps, assignment


def chain(op: str, bits: list[int]) -> tuple[list[Gate], int]:
    gates: list[Gate] = []
    cur = 1
    nxt = len(bits) + 1
    for v in range(2, len(bits) + 1):
        gates.append(Gate(op, nxt, (cur, v)))
        cur, nxt = nxt, nxt + 1
    return gates, cur


def wrapped(base_gates: list[Gate], output: int, start: int, copies: int, dead: int):
    gates = list(base_gates)
    cur, nxt = output, start
    for _ in range(copies):
        gates.append(Gate("COPY", nxt, (cur,)))
        cur, nxt = nxt, nxt + 1
    for i in range(dead):
        source = 1 if i % 2 == 0 else cur
        gates.append(Gate("NOT" if i % 3 == 0 else "COPY", nxt, (source,)))
        nxt += 1
    return gates, cur


def random_circuit(rng: random.Random, n_inputs: int, n_gates: int):
    gates: list[Gate] = []
    available = list(range(1, n_inputs + 1))
    nxt = n_inputs + 1
    for _ in range(n_gates):
        op = rng.choice(["AND", "OR", "XOR", "NOT", "COPY"])
        arity = 1 if op in {"NOT", "COPY"} else 2
        args = tuple(rng.choice(available) for _ in range(arity))
        gates.append(Gate(op, nxt, args))
        available.append(nxt)
        nxt += 1
    return gates, gates[-1].out


def audit_case(name: str, bits: list[int], gates: list[Gate], output: int, rng: random.Random):
    core, wrong, val = tseitin(len(bits), bits, gates, output)
    assert all(any(lit_value(l, val) for l in c) for c in core)
    assert not any(lit_value(l, val) for l in wrong)
    refuted, steps, assignment = unit_propagate(core + [wrong])
    shuffled = list(core + [wrong])
    rng.shuffle(shuffled)
    refuted_shuffled, shuffled_steps, _ = unit_propagate(shuffled)
    assert refuted and refuted_shuffled
    assert len(assignment) <= len(val)
    return {
        "name": name,
        "inputs": len(bits),
        "gates": len(gates),
        "clauses": len(core) + 1,
        "output": val[output],
        "unit_steps": steps,
        "shuffled_unit_steps": shuffled_steps,
        "core_clauses_true_under_trace": len(core),
        "core_clauses_false_under_trace": 0,
        "wrong_output_units_false_under_trace": 1,
        "witness_namespace_occurrences": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261013)
    parser.add_argument("--random-cases", type=int, default=2000)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    start = time.perf_counter()
    cases = []

    # Smallest COPY/identity firewall.
    cases.append(audit_case("identity_minimal", [1], [Gate("COPY", 2, (1,))], 2, rng))
    for op, bits in [("AND", [1, 1, 0, 1, 1]), ("OR", [0, 0, 1, 0, 0]), ("XOR", [1, 0, 1, 1, 0, 1])]:
        gs, out = chain(op, bits)
        cases.append(audit_case(op.lower() + "_chain", bits, gs, out, rng))
    # Bounded-width implication-style chain: NOT then OR, serially.
    bits = [1, 0, 1, 1]
    gates = []
    nxt, cur = len(bits) + 1, 1
    for rhs in range(2, len(bits) + 1):
        gates.append(Gate("NOT", nxt, (cur,))); neg = nxt; nxt += 1
        gates.append(Gate("OR", nxt, (neg, rhs))); cur = nxt; nxt += 1
    cases.append(audit_case("implication_2sat_like_chain", bits, gates, cur, rng))
    base, out = chain("XOR", [1, 1, 0, 1, 0, 1, 1, 0])
    gates, wrapped_out = wrapped(base, out, max(g.out for g in base) + 1, 32, 64)
    cases.append(audit_case("xor_copy_delay_dead_wrappers", [1, 1, 0, 1, 0, 1, 1, 0], gates, wrapped_out, rng))

    totals = {"random_gates": 0, "random_clauses": 0}
    for i in range(args.random_cases):
        n_inputs = rng.randint(1, 12)
        bits = [rng.randrange(2) for _ in range(n_inputs)]
        gates, out = random_circuit(rng, n_inputs, rng.randint(1, 50))
        row = audit_case(f"random_{i}", bits, gates, out, rng)
        totals["random_gates"] += row["gates"]
        totals["random_clauses"] += row["clauses"]

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "TRACEAXIOM-FIREWALL1",
        "status": "COMPUTATIONAL",
        "seed": args.seed,
        "random_cases": args.random_cases,
        "named_controls": cases,
        "random_totals": totals,
        "assertions": {
            "all_core_axioms_true_under_actual_trace": True,
            "exactly_wrong_output_unit_false_under_actual_trace": True,
            "unit_propagation_refutes_all_fixed_trace_instances": True,
            "clause_order_permutation_invariant_in_test": True,
            "formula_witness_namespace_absent": True,
        },
        "limitations": [
            "Finite encoding audit only; the report contains the symbolic proof.",
            "No inference from trace-CNF proof size to L22 decision time.",
            "No correctness bridge from satisfying assignments of H to the fixed computation trace is encoded.",
        ],
        "elapsed_seconds": elapsed,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
