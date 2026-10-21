#!/usr/bin/env python3
"""Finite controls for PARSIMONIOUS-CIRCUIT-3CNF47.

The general result is a truth-table exclusion proof.  These exhaustive tests
catch variable-order, repeated-wire, gate-sharing, and counting errors.
"""

from dataclasses import dataclass
from itertools import product
import json


@dataclass(frozen=True)
class Gate:
    op: str
    out: int
    ins: tuple[int, ...]


def exclusion_cnf(vars3, allowed):
    """Proper 3-CNF whose satisfying rows are exactly allowed."""
    assert len(vars3) == 3 and len(set(vars3)) == 3
    allowed = set(allowed)
    clauses = []
    for row in product((0, 1), repeat=3):
        if row not in allowed:
            # This clause is false exactly on row.
            clauses.append(tuple(v + 1 if bit == 0 else -(v + 1)
                                 for v, bit in zip(vars3, row)))
    return clauses


def sat(clauses, assignment):
    return all(any(assignment[abs(lit) - 1] == (lit > 0)
                   for lit in clause) for clause in clauses)


def eval_circuit(n_inputs, gates, bits):
    val = {i: bits[i] for i in range(n_inputs)}
    for gate in gates:
        xs = [val[i] for i in gate.ins]
        if gate.op == "NOT":
            val[gate.out] = 1 - xs[0]
        elif gate.op == "AND":
            val[gate.out] = xs[0] & xs[1]
        elif gate.op == "OR":
            val[gate.out] = xs[0] | xs[1]
        else:
            raise ValueError(gate.op)
    return val


def relation_gadget(interface_vars, legal_rows, next_var):
    """Pad a q<=3 relation to three distinct vars with uniquely-zero pads."""
    interface_vars = tuple(interface_vars)
    q = len(interface_vars)
    assert 1 <= q <= 3 and len(set(interface_vars)) == q
    pads = tuple(range(next_var, next_var + (3 - q)))
    vars3 = interface_vars + pads
    allowed = {tuple(row) + (0,) * len(pads) for row in legal_rows}
    return exclusion_cnf(vars3, allowed), next_var + len(pads), pads


def circuit_to_unique_3cnf(n_inputs, gates, output):
    next_var = n_inputs + len(gates)
    clauses = []
    pads = []
    for gate in gates:
        if gate.op == "NOT":
            a = gate.ins[0]
            legal = {(0, 1), (1, 0)}  # (a,z)
            cs, next_var, ps = relation_gadget((a, gate.out), legal, next_var)
        elif gate.ins[0] == gate.ins[1]:
            # AND(a,a)=OR(a,a)=a: use the binary equality relation.
            a = gate.ins[0]
            legal = {(0, 0), (1, 1)}  # (a,z)
            cs, next_var, ps = relation_gadget((a, gate.out), legal, next_var)
        else:
            a, b = gate.ins
            if gate.op == "AND":
                legal = {(x, y, x & y) for x, y in product((0, 1), repeat=2)}
            elif gate.op == "OR":
                legal = {(x, y, x | y) for x, y in product((0, 1), repeat=2)}
            else:
                raise ValueError(gate.op)
            cs, next_var, ps = relation_gadget((a, b, gate.out), legal, next_var)
        clauses.extend(cs)
        pads.extend(ps)

    # Force output=1, and uniquely force both fresh pads to zero.
    cs, next_var, ps = relation_gadget((output,), {(1,)}, next_var)
    clauses.extend(cs)
    pads.extend(ps)
    return clauses, next_var, tuple(pads)


def sharing_identity(depth):
    n = depth + 1
    gates = []
    prev = 0
    nxt = n
    for i in range(1, depth + 1):
        ny, left, right, out = nxt, nxt + 1, nxt + 2, nxt + 3
        nxt += 4
        gates.extend([
            Gate("NOT", ny, (i,)),
            Gate("AND", left, (prev, i)),
            Gate("AND", right, (prev, ny)),
            Gate("OR", out, (left, right)),
        ])
        prev = out
    return n, gates, prev


def point_circuit(target):
    n = len(target)
    gates = []
    literals = []
    nxt = n
    for i, bit in enumerate(target):
        if bit:
            literals.append(i)
        else:
            gates.append(Gate("NOT", nxt, (i,)))
            literals.append(nxt)
            nxt += 1
    if n == 1:
        return n, gates, literals[0]
    prev = literals[0]
    for lit in literals[1:]:
        gates.append(Gate("AND", nxt, (prev, lit)))
        prev = nxt
        nxt += 1
    return n, gates, prev


def extension_count(n, gates, output, bits):
    clauses, total_vars, _ = circuit_to_unique_3cnf(n, gates, output)
    count = 0
    for rest in product((0, 1), repeat=total_vars - n):
        count += sat(clauses, bits + rest)
    return count, clauses, total_vars


def main():
    assertions = 0
    assignments = 0

    # Local gadget truth tables, including repeated-input normalization.
    local_specs = [
        ((0, 1, 2), {(x, y, x & y) for x, y in product((0, 1), repeat=2)}),
        ((0, 1, 2), {(x, y, x | y) for x, y in product((0, 1), repeat=2)}),
        ((0, 1), {(0, 1), (1, 0)}),
        ((0, 1), {(0, 0), (1, 1)}),
        ((0,), {(1,)}),
    ]
    for interface, legal in local_specs:
        clauses, total, _ = relation_gadget(interface, legal, max(interface) + 1)
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
        assertions += 1
        for row in product((0, 1), repeat=len(interface)):
            count = 0
            for pad in product((0, 1), repeat=total - len(interface)):
                count += sat(clauses, row + pad)
                assignments += 1
            assert count == (1 if row in legal else 0)
            assertions += 1

    # Shared DAGs: parsimonious projection despite reuse of the prior gate.
    for depth in (1, 2):
        n, gates, out = sharing_identity(depth)
        clauses, total, _ = circuit_to_unique_3cnf(n, gates, out)
        formula_models = 0
        circuit_accepts = 0
        for bits in product((0, 1), repeat=n):
            expected = eval_circuit(n, gates, bits)[out]
            count, _, _ = extension_count(n, gates, out, bits)
            assignments += 2 ** (total - n)
            assert count == expected
            assertions += 1
            formula_models += count
            circuit_accepts += expected
        assert formula_models == circuit_accepts == 2**depth
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
        assertions += 2

    # Explicit repeated-wire gates.
    repeat_gates = [Gate("AND", 1, (0, 0)), Gate("OR", 2, (1, 1))]
    for bit in ((0,), (1,)):
        count, clauses, _ = extension_count(1, repeat_gates, 2, bit)
        assert count == bit[0]
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
        assertions += 2

    # Point circuits: one 3-CNF model, exactly the source-revealed target.
    for n in range(1, 4):
        for target in product((0, 1), repeat=n):
            ni, gates, out = point_circuit(target)
            total_models = 0
            accepting_inputs = []
            for bits in product((0, 1), repeat=n):
                count, _, total = extension_count(ni, gates, out, bits)
                assignments += 2 ** (total - n)
                if count:
                    accepting_inputs.append(bits)
                total_models += count
                assert count in (0, 1)
                assertions += 1
            assert accepting_inputs == [target]
            assert total_models == 1
            assertions += 2

    result = {
        "status": "PASS",
        "assertions": assertions,
        "assignments_checked": assignments,
        "sharing_depth_max": 2,
        "point_width_max": 3,
        "claims": [
            "proper_3cnf_local_relations_have_exact_legal_rows",
            "unique_auxiliary_extension",
            "composed_reduction_is_parsimonious_on_input_witnesses",
            "gate_sharing_and_repeated_wires_preserved",
            "point_circuit_has_one_formula_model",
        ],
        "global_status": {"P_vs_NP": "OPEN", "P_vs_RP": "OPEN"},
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
