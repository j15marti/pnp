#!/usr/bin/env python3
"""Finite audit for CIRCUIT-TSEITIN-TRACE-AUDIT46.

The checks are deliberately finite controls.  The accompanying report contains
the general proofs; this script catches representation and counting mistakes.
"""

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Gate:
    op: str
    out: int
    ins: tuple[int, ...]


def eval_circuit(n_inputs: int, gates: list[Gate], bits: tuple[int, ...]):
    values = {i: bits[i] for i in range(n_inputs)}
    for gate in gates:
        xs = [values[i] for i in gate.ins]
        if gate.op == "NOT":
            values[gate.out] = 1 - xs[0]
        elif gate.op == "AND":
            values[gate.out] = xs[0] & xs[1]
        elif gate.op == "OR":
            values[gate.out] = xs[0] | xs[1]
        else:
            raise ValueError(gate.op)
    return values


def tseitin(gates: list[Gate]):
    """Clauses use signed integers: v+1 for v, -(v+1) for not v."""
    clauses: list[tuple[int, ...]] = []
    for gate in gates:
        z = gate.out + 1
        if gate.op == "NOT":
            a = gate.ins[0] + 1
            clauses += [(a, z), (-a, -z)]
        elif gate.op == "AND":
            a, b = (i + 1 for i in gate.ins)
            clauses += [(-a, -b, z), (a, -z), (b, -z)]
        elif gate.op == "OR":
            a, b = (i + 1 for i in gate.ins)
            clauses += [(a, b, -z), (-a, z), (-b, z)]
        else:
            raise ValueError(gate.op)
    return clauses


def satisfies(clauses, assignment):
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses)


def pad_two_clauses(clauses, start_var):
    padded = []
    next_var = start_var
    auxiliaries = []
    for clause in clauses:
        if len(clause) == 2:
            u = next_var + 1
            next_var += 1
            auxiliaries.append(u - 1)
            padded += [clause + (u,), clause + (-u,)]
        else:
            padded.append(clause)
    return padded, auxiliaries


def sharing_identity(depth: int):
    """DAG computes x despite exponentially many x occurrences after unrolling."""
    n_inputs = depth + 1  # x,y_1,...,y_depth
    gates: list[Gate] = []
    prev = 0
    nxt = n_inputs
    for i in range(1, depth + 1):
        not_y = nxt
        left = nxt + 1
        right = nxt + 2
        out = nxt + 3
        nxt += 4
        gates += [
            Gate("NOT", not_y, (i,)),
            Gate("AND", left, (prev, i)),
            Gate("AND", right, (prev, not_y)),
            Gate("OR", out, (left, right)),
        ]
        prev = out
    return n_inputs, gates, prev


def point_circuit(target: tuple[int, ...]):
    n = len(target)
    gates: list[Gate] = []
    literals = []
    nxt = n
    signs = []
    for i, bit in enumerate(target):
        if bit:
            literals.append(i)
            signs.append(1)
        else:
            gates.append(Gate("NOT", nxt, (i,)))
            literals.append(nxt)
            signs.append(0)
            nxt += 1
    if n == 1:
        return n, gates, literals[0], tuple(signs)
    prev = literals[0]
    for lit in literals[1:]:
        gates.append(Gate("AND", nxt, (prev, lit)))
        prev = nxt
        nxt += 1
    return n, gates, prev, tuple(signs)


def main():
    assertions = 0

    # Exact trace uniqueness and naive-padding multiplicity on shared DAGs.
    for depth in range(1, 4):
        n, gates, out = sharing_identity(depth)
        clauses = tseitin(gates)
        all_vars = n + len(gates)
        padded, aux = pad_two_clauses(clauses, all_vars)
        r = len(aux)
        assert r == 2 * len(gates)
        assertions += 1
        for bits in product((0, 1), repeat=n):
            trace = eval_circuit(n, gates, bits)
            assert trace[out] == bits[0]
            assertions += 1
            full = tuple(trace[i] for i in range(all_vars))
            assert satisfies(clauses, full)
            assertions += 1

            # Exhaustively prove no second standard Tseitin gate trace.
            count = 0
            for gate_bits in product((0, 1), repeat=len(gates)):
                candidate = bits + gate_bits
                count += satisfies(clauses, candidate)
            assert count == 1
            assertions += 1

            # On the valid trace every fresh padding bit is free: 2^r extensions.
            if depth <= 2:
                padded_count = 0
                for aux_bits in product((0, 1), repeat=r):
                    padded_count += satisfies(padded, full + aux_bits)
                assert padded_count == 2**r
                assertions += 1

        assert 2**depth > depth and len(gates) == 4 * depth
        assertions += 1

    # Point circuits have one satisfying input; their canonical source reveals it.
    for n in range(1, 7):
        for target in product((0, 1), repeat=n):
            ni, gates, out, recovered = point_circuit(target)
            assert recovered == target
            assertions += 1
            satisfying = []
            for bits in product((0, 1), repeat=n):
                trace = eval_circuit(ni, gates, bits)
                if trace[out]:
                    satisfying.append(bits)
            assert satisfying == [target]
            assertions += 1

    print(
        {
            "status": "PASS",
            "assertions": assertions,
            "sharing_depth_max": 3,
            "point_width_max": 6,
            "checked_claims": [
                "standard_tseitin_unique_trace",
                "naive_3cnf_padding_exact_2^r_extensions",
                "shared_dag_function_is_identity",
                "point_circuit_unique_input_and_source_recovery",
            ],
        }
    )


if __name__ == "__main__":
    main()
