#!/usr/bin/env python3
"""Finite gate audit for reversible compute-copy-uncompute.

The accompanying report proves the all-circuit statement symbolically.  This
program exhaustively checks the gate embedding and bounded hostile controls;
it does not promote finite observations into an asymptotic SAT theorem.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path


OUT = Path("results/raw/review/2026-10-13_reversible_compute_uncompute.json")


def gate_value(op, values):
    if op == "CONST0":
        return 0
    if op == "CONST1":
        return 1
    if op == "BUF":
        return values[0]
    if op == "NOT":
        return 1 ^ values[0]
    if op == "AND":
        return values[0] & values[1]
    if op == "OR":
        return values[0] | values[1]
    if op == "XOR":
        return values[0] ^ values[1]
    if op == "XNOR":
        return 1 ^ values[0] ^ values[1]
    raise ValueError(op)


def apply_gate(state, gate):
    op, srcs, target = gate
    out = list(state)
    out[target] ^= gate_value(op, [state[i] for i in srcs])
    return tuple(out)


class Circuit:
    def __init__(self, n):
        self.n = n
        self.gates = []

    def add(self, op, *srcs):
        target = self.n + len(self.gates)
        self.gates.append((op, tuple(srcs), target))
        return target


def and_all(c, wires):
    if not wires:
        return c.add("CONST1")
    cur = c.add("BUF", wires[0])
    for w in wires[1:]:
        cur = c.add("AND", cur, w)
    return cur


def or_all(c, wires):
    if not wires:
        return c.add("CONST0")
    cur = c.add("BUF", wires[0])
    for w in wires[1:]:
        cur = c.add("OR", cur, w)
    return cur


def family_circuit(n, family):
    c = Circuit(n)
    x = list(range(n))
    if family == "trivial_yes":
        out = c.add("CONST1")
    elif family == "one_bit":
        out = c.add("BUF", x[0])
    elif family == "2SAT":
        nx0 = c.add("NOT", x[0])
        a = c.add("OR", x[0], x[1 % n])
        b = c.add("OR", nx0, x[2 % n])
        out = c.add("AND", a, b)
    elif family == "Horn":
        nx0 = c.add("NOT", x[0])
        nx1 = c.add("NOT", x[1 % n])
        a = c.add("OR", nx0, nx1)
        b = c.add("OR", a, x[2 % n])
        out = c.add("AND", b, x[3 % n])
    elif family == "affine_Tseitin":
        cur = c.add("BUF", x[0])
        for w in x[1:]:
            cur = c.add("XOR", cur, w)
        out = c.add("NOT", cur)
    elif family == "bounded_treewidth":
        eqs = [c.add("XNOR", x[i], x[i + 1]) for i in range(n - 1)]
        out = and_all(c, eqs)
    elif family == "independent_product":
        mid = max(1, n // 2)
        left = or_all(c, x[:mid])
        right = or_all(c, x[mid:] or x[:1])
        out = c.add("AND", left, right)
    elif family == "clean_core_proxy":
        a = or_all(c, [x[0], x[1 % n], x[2 % n]])
        b = or_all(c, [x[1 % n], x[2 % n], x[3 % n]])
        out = c.add("AND", a, b)
    else:
        raise ValueError(family)
    return c, out


def add_wrapper(c, output, wrapper):
    x0 = 0
    if wrapper == "DIRECT":
        return output
    if wrapper == "DEAD":
        c.add("NOT", x0)
        c.add("XOR", x0, output)
        return output
    if wrapper == "COPY":
        c.add("BUF", x0)
        return output
    if wrapper == "DELAY":
        z = c.add("CONST0")
        c.add("XOR", z, z)
        return output
    if wrapper == "INTERP":
        a = c.add("BUF", x0)
        c.add("BUF", a)
        return output
    if wrapper == "RECOMP":
        c.add("BUF", output)
        c.add("BUF", output)
        return output
    raise ValueError(wrapper)


def ordinary_eval(c, output, inp):
    state = tuple(inp) + (0,) * len(c.gates)
    for gate in c.gates:
        state = apply_gate(state, gate)
    return state[output]


def reversible_run(c, output, inp):
    start = tuple(inp) + (0,) * len(c.gates)
    state = start
    trace = [state]
    for gate in c.gates:
        state = apply_gate(state, gate)
        trace.append(state)
    answer = state[output]
    copied_output = answer  # CNOT into a fresh zero output bit.
    for gate in reversed(c.gates):
        state = apply_gate(state, gate)
        trace.append(state)
    return copied_output, state, trace


def check_gate_bijections():
    checks = 0
    specs = {
        "CONST0": 0, "CONST1": 0, "BUF": 1, "NOT": 1,
        "AND": 2, "OR": 2, "XOR": 2, "XNOR": 2,
    }
    for op, arity in specs.items():
        images = set()
        for bits in itertools.product((0, 1), repeat=arity + 1):
            src = bits[:arity]
            target = bits[-1]
            image = src + (target ^ gate_value(op, src),)
            images.add(image)
            checks += 1
        assert len(images) == 2 ** (arity + 1)
        checks += 1
    return checks


def main():
    start_time = time.perf_counter()
    families = [
        "trivial_yes", "one_bit", "2SAT", "Horn", "affine_Tseitin",
        "bounded_treewidth", "independent_product", "clean_core_proxy",
    ]
    wrappers = ["DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP"]
    encodings = ["direct", "reversed", "complemented", "padded"]
    checks = check_gate_bijections()
    rows = []
    for n in range(1, 9):
        for family in families:
            for wrapper in wrappers:
                c, output = family_circuit(n, family)
                output = add_wrapper(c, output, wrapper)
                for encoding in encodings:
                    for raw in itertools.product((0, 1), repeat=n):
                        if encoding == "direct":
                            inp = raw
                        elif encoding == "reversed":
                            inp = tuple(reversed(raw))
                        elif encoding == "complemented":
                            inp = tuple(1 ^ b for b in raw)
                        else:
                            inp = raw  # padding is charged but semantically unused.
                        expected = ordinary_eval(c, output, inp)
                        answer, restored, trace = reversible_run(c, output, inp)
                        assert answer == expected
                        checks += 1
                        assert restored == tuple(inp) + (0,) * len(c.gates)
                        checks += 1
                        assert len(trace) == 2 * len(c.gates) + 1
                        checks += 1
                rows.append({
                    "n": n,
                    "family": family,
                    "wrapper": wrapper,
                    "ordinary_gates": len(c.gates),
                    "reversible_internal_steps": 2 * len(c.gates),
                    "answer_copy_steps": 1,
                    "ancilla_bits": len(c.gates),
                    "logical_merges": 0,
                    "final_garbage_bits": 0,
                    "padding_bits_when_selected": n,
                })

    # Smallest nonconstant case: one input bit, one BUF gate, one copied output.
    c, output = family_circuit(1, "one_bit")
    witness = []
    for bit in (0, 1):
        answer, restored, trace = reversible_run(c, output, (bit,))
        witness.append({"input": bit, "answer": answer, "restored": list(restored), "trace": [list(s) for s in trace]})
    assert [w["answer"] for w in witness] == [0, 1]
    checks += 1

    result = {
        "run_id": "REVUNCOMP1",
        "status": "COMPUTATIONAL finite audit; symbolic gate theorem is separate",
        "enumeration": {"n_min": 1, "n_max": 8, "families": families, "wrappers": wrappers, "encodings": encodings},
        "checks": checks,
        "smallest_counterexample": witness,
        "cost_identity": {
            "ordinary_gate_count": "G",
            "reversible_internal_steps": "2G",
            "answer_copy_steps": 1,
            "ancilla_bits": "G",
            "logical_merges": 0,
            "final_garbage_bits": 0,
        },
        "rows": rows,
        "limitations": [
            "finite circuit instances only",
            "physical heat and initialization are outside the logical gate model",
            "clean_core_proxy is a hostile representation control, not an NP-hardness claim",
        ],
        "elapsed_seconds": time.perf_counter() - start_time,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks": checks, "rows": len(rows), "elapsed_seconds": result["elapsed_seconds"], "output": str(OUT)}))


if __name__ == "__main__":
    main()
