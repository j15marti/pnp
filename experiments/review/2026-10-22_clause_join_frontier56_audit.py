#!/usr/bin/env python3
"""Finite audit for SOURCE-JOIN-COHERENCE56.

This checks only finite identities and a concrete WRAPPER root.  It does not
claim a complexity-class separation.
"""

from fractions import Fraction
from itertools import product
import json
import math
import random


ROOT_CLAUSES = [
    (-12, -1, 13), (-10, 1, 9), (-9, -2, 11), (-8, -1, 6),
    (-6, 1, 8), (-4, 1, 3), (-4, 2, 5), (-2, 6, 7),
    (-2, 10, 11), (-2, 12, 13), (-1, 10, 11), (-1, 13, 14),
    (1, 4, 5), (2, 3, 5), (2, 6, 8), (2, 13, 14),
    (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14),
]


def literal_value(lit, values):
    bit = values[abs(lit)]
    return bit if lit > 0 else 1 - bit


def clause_value(clause, values):
    return any(literal_value(lit, values) for lit in clause)


def formula_value(clauses, values):
    return all(clause_value(clause, values) for clause in clauses)


def brute_count(clauses):
    variables = sorted({abs(lit) for clause in clauses for lit in clause})
    count = 0
    for bits in product((0, 1), repeat=len(variables)):
        values = dict(zip(variables, bits))
        count += formula_value(clauses, values)
    return count


def satisfying_local_rows(clause):
    rows = []
    for bits in product((0, 1), repeat=3):
        values = {abs(clause[j]): bits[j] for j in range(3)}
        if clause_value(clause, values):
            rows.append(bits)
    return rows


def coherent_local_count(clauses):
    """Enumerate local rows, enforcing equality on every source occurrence."""
    rows = [satisfying_local_rows(c) for c in clauses]
    count = 0
    for chosen in product(*rows):
        source = {}
        coherent = True
        for clause, bits in zip(clauses, chosen):
            for lit, bit in zip(clause, bits):
                var = abs(lit)
                if var in source and source[var] != bit:
                    coherent = False
                    break
                source[var] = bit
            if not coherent:
                break
        count += coherent
    return count


def frontier_count(clauses, order):
    """Exact #SAT by a fixed clause ordering and live-source frontier."""
    remaining_vars = []
    suffix = set()
    for idx in reversed(order):
        suffix = suffix | {abs(x) for x in clauses[idx]}
        remaining_vars.append(set(suffix))
    remaining_vars.reverse()

    seen = set()
    before = ()
    table = {(): 1}
    max_frontier = 0
    max_states = 1
    for pos, idx in enumerate(order):
        clause = clauses[idx]
        cvars = {abs(x) for x in clause}
        new_vars = sorted(cvars - seen)
        after_seen = seen | cvars
        future = remaining_vars[pos + 1] if pos + 1 < len(order) else set()
        after = tuple(sorted(after_seen & future))
        next_table = {}
        for key, multiplicity in table.items():
            base = dict(zip(before, key))
            for new_bits in product((0, 1), repeat=len(new_vars)):
                values = dict(base)
                values.update(zip(new_vars, new_bits))
                if clause_value(clause, values):
                    projected = tuple(values[v] for v in after)
                    next_table[projected] = next_table.get(projected, 0) + multiplicity
        table = next_table
        seen = after_seen
        before = after
        max_frontier = max(max_frontier, len(after))
        max_states = max(max_states, len(table))
    return table.get((), 0), max_frontier, max_states


def greedy_order(clauses):
    remaining = set(range(len(clauses)))
    seen = set()
    order = []
    while remaining:
        choices = []
        for idx in remaining:
            future = set().union(*(
                ({abs(x) for x in clauses[j]} for j in remaining if j != idx)
            )) if len(remaining) > 1 else set()
            cvars = {abs(x) for x in clauses[idx]}
            width = len((seen | cvars) & future)
            choices.append((width, idx))
        _, idx = min(choices)
        order.append(idx)
        seen |= {abs(x) for x in clauses[idx]}
        remaining.remove(idx)
    return order


def blocker_formula():
    """Eight clauses, each false on exactly one assignment to x1,x2,x3."""
    clauses = []
    for forbidden in product((0, 1), repeat=3):
        clauses.append(tuple((i + 1) if bit == 0 else -(i + 1)
                             for i, bit in enumerate(forbidden)))
    return clauses


def build_cnf_circuit(clauses, shared_negations):
    """Return a deterministic fan-in-2 circuit as (gates, output wire)."""
    n = max(abs(lit) for clause in clauses for lit in clause)
    gates = []
    neg_cache = {}

    def add_gate(op, a, b=None):
        wire = n + len(gates) + 1
        gates.append((wire, op, a, b))
        return wire

    def literal_wire(lit):
        if lit > 0:
            return lit
        var = -lit
        if shared_negations and var in neg_cache:
            return neg_cache[var]
        wire = add_gate("NOT", var)
        if shared_negations:
            neg_cache[var] = wire
        return wire

    clause_wires = []
    for clause in clauses:
        a, b, c = (literal_wire(x) for x in clause)
        clause_wires.append(add_gate("OR", add_gate("OR", a, b), c))
    out = clause_wires[0]
    for wire in clause_wires[1:]:
        out = add_gate("AND", out, wire)
    return gates, out


def eval_circuit(n, gates, output, source):
    values = {i: source[i] for i in range(1, n + 1)}
    trace = []
    for wire, op, a, b in gates:
        if op == "NOT":
            value = 1 - values[a]
        elif op == "OR":
            value = values[a] | values[b]
        elif op == "AND":
            value = values[a] & values[b]
        else:
            raise AssertionError(op)
        values[wire] = value
        trace.append(value)
    return values[output], tuple(trace)


def main():
    assertions = 0
    for clause in ROOT_CLAUSES:
        assert len(clause) == 3
        assert len({abs(x) for x in clause}) == 3
        assert len(satisfying_local_rows(clause)) == 7
        assertions += 3

    root_sat = brute_count(ROOT_CLAUSES)
    natural = list(range(len(ROOT_CLAUSES)))
    greedy = greedy_order(ROOT_CLAUSES)
    natural_count, natural_width, natural_states = frontier_count(ROOT_CLAUSES, natural)
    greedy_count, greedy_width, greedy_states = frontier_count(ROOT_CLAUSES, greedy)
    assert natural_count == root_sat
    assert greedy_count == root_sat
    assertions += 2

    occurrences = 3 * len(ROOT_CLAUSES)
    variables = {abs(x) for c in ROOT_CLAUSES for x in c}
    spanning_tree_joins = occurrences - len(variables)
    assert spanning_tree_joins == 46
    assertions += 1

    blocker = blocker_formula()
    assert brute_count(blocker) == 0
    assert coherent_local_count(blocker) == 0
    assert math.isclose(float(Fraction(63**8, 64**8)), 0.881626435, rel_tol=1e-9)
    assertions += 3

    rng = random.Random(560022)
    random_cases = 160
    for _ in range(random_cases):
        n = rng.choice((3, 4, 5))
        m = rng.choice((1, 2, 3, 4))
        clauses = []
        for _ in range(m):
            vars_ = rng.sample(range(1, n + 1), 3)
            clauses.append(tuple(v if rng.getrandbits(1) else -v for v in vars_))
        assert coherent_local_count(clauses) == brute_count(clauses)
        assertions += 1

    shared_gates, shared_out = build_cnf_circuit(ROOT_CLAUSES, True)
    copied_gates, copied_out = build_cnf_circuit(ROOT_CLAUSES, False)
    accepting_shared = 0
    accepting_copied = 0
    trace_seen = {}
    for bits in product((0, 1), repeat=14):
        source = {i + 1: bits[i] for i in range(14)}
        formula = int(formula_value(ROOT_CLAUSES, source))
        shared_value, shared_trace = eval_circuit(14, shared_gates, shared_out, source)
        copied_value, copied_trace = eval_circuit(14, copied_gates, copied_out, source)
        assert shared_value == formula
        assert copied_value == formula
        assert trace_seen.setdefault(bits, shared_trace) == shared_trace
        accepting_shared += shared_value
        accepting_copied += copied_value
        assertions += 3
    assert accepting_shared == root_sat == accepting_copied
    assertions += 1

    m = len(ROOT_CLAUSES)
    t = math.ceil(math.log(2 * m, 8))
    local_acceptance = Fraction((8**t - 1)**m, 8**(t * m))
    assert local_acceptance >= Fraction(1, 2)
    assertions += 1

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "root": {
            "clauses": m,
            "variables": len(variables),
            "occurrences": occurrences,
            "spanning_tree_equality_joins": spanning_tree_joins,
            "global_satisfying_assignments": root_sat,
            "unjoined_local_satisfying_tuples": 7**m,
            "local_sampler_t": t,
            "local_sampler_probability_exact": f"{local_acceptance.numerator}/{local_acceptance.denominator}",
            "local_sampler_probability": float(local_acceptance),
            "natural_frontier": {
                "width": natural_width,
                "peak_states": natural_states,
                "count": natural_count,
            },
            "greedy_frontier": {
                "order_zero_based": greedy,
                "width": greedy_width,
                "peak_states": greedy_states,
                "count": greedy_count,
            },
            "circuit": {
                "shared_negation_gates": len(shared_gates),
                "copied_negation_gates": len(copied_gates),
                "accepting_sources_shared": accepting_shared,
                "accepting_sources_copied": accepting_copied,
                "unique_trace_per_fixed_source": True,
            },
        },
        "unsat_blocker": {
            "clauses": 8,
            "global_satisfying_assignments": 0,
            "coherent_local_tuples": 0,
            "unjoined_local_tuples": 7**8,
            "t_2_local_acceptance_exact": f"{63**8}/{64**8}",
            "t_2_local_acceptance": float(Fraction(63**8, 64**8)),
        },
        "random_coherence_cases": random_cases,
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
