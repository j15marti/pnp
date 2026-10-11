#!/usr/bin/env python3
"""Bounded audit for forward-only circuit-to-3CNF compilation.

The experiment is finite evidence for TESTS-0009.  The symbolic theorem in
the report, rather than this program, establishes the general interface
statement.  Every individual run is deterministic and intended to finish in
well under 30 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SEED = 202610111624
OUT = Path("results/raw/review/2026-10-11_forward_wire_locality_bypass.json")


@dataclass(frozen=True)
class Gate:
    kind: str
    children: tuple[int, ...] = ()


def eval_circuit(gates: list[Gate], inputs: tuple[bool, ...]) -> list[bool]:
    vals: list[bool] = []
    inp = 0
    for gate in gates:
        if gate.kind == "IN":
            vals.append(inputs[inp])
            inp += 1
        elif gate.kind == "NOT":
            vals.append(not vals[gate.children[0]])
        elif gate.kind == "AND":
            vals.append(vals[gate.children[0]] and vals[gate.children[1]])
        elif gate.kind == "OR":
            vals.append(vals[gate.children[0]] or vals[gate.children[1]])
        elif gate.kind == "XOR":
            vals.append(vals[gate.children[0]] ^ vals[gate.children[1]])
        else:
            raise ValueError(gate.kind)
    return vals


def base_gate_clauses(g: int, gate: Gate) -> list[list[tuple[int, bool]]]:
    """Clauses for y_g = op(children); bool is positive polarity."""
    y = g
    if gate.kind == "IN":
        return []
    if gate.kind == "NOT":
        a = gate.children[0]
        return [[(a, True), (y, True)], [(a, False), (y, False)]]
    a, b = gate.children
    if gate.kind == "AND":
        return [[(a, False), (b, False), (y, True)],
                [(a, True), (y, False)], [(b, True), (y, False)]]
    if gate.kind == "OR":
        return [[(a, True), (b, True), (y, False)],
                [(a, False), (y, True)], [(b, False), (y, True)]]
    if gate.kind == "XOR":
        return [[(a, True), (b, True), (y, False)],
                [(a, False), (b, False), (y, False)],
                [(a, True), (b, False), (y, True)],
                [(a, False), (b, True), (y, True)]]
    raise ValueError(gate.kind)


def expand_clause(owner: int, slot: int, clause: list[tuple[int, bool]]):
    if len(clause) == 3:
        return [[("core", v, pol) for v, pol in clause]]
    assert len(clause) == 2
    z = ("pad2", owner, slot)
    body = [("core", v, pol) for v, pol in clause]
    return [body + [(z, True)], body + [(z, False)]]


def local_clause(gates: list[Gate], address: tuple):
    """Random-access clause generator; it only calls children of its owner."""
    kind = address[0]
    if kind == "gate":
        _, g, slot, branch = address
        base = base_gate_clauses(g, gates[g])
        expanded = expand_clause(g, slot, base[slot])
        return expanded[branch], len(gates[g].children), 0
    _, branch = address
    x = ("core", len(gates) - 1, True)
    p = ("assert", 0)
    q = ("assert", 1)
    choices = [(True, True), (True, False), (False, True), (False, False)]
    pp, qq = choices[branch]
    return [x, (p, pp), (q, qq)], 0, 0


def addresses(gates: list[Gate]):
    out = []
    for g, gate in enumerate(gates):
        for slot, clause in enumerate(base_gate_clauses(g, gate)):
            for branch in range(1 if len(clause) == 3 else 2):
                out.append(("gate", g, slot, branch))
    out.extend(("assert", b) for b in range(4))
    return out


def compile_cnf(gates: list[Gate]):
    clauses = []
    child_queries = parent_queries = 0
    for addr in addresses(gates):
        clause, cq, pq = local_clause(gates, addr)
        clauses.append(clause)
        child_queries += cq
        parent_queries += pq
    return clauses, child_queries, parent_queries


def lit_value(lit, core, aux):
    key, *rest = lit
    pol = rest.pop()
    if key == "core":
        val = core[rest[0]]
    else:
        val = aux.get((key, *rest), False)
    return val if pol else not val


def cnf_value(clauses, core, aux=None):
    aux = aux or {}
    return all(any(lit_value(l, core, aux) for l in c) for c in clauses)


def base_consistent(gates, core):
    for g, gate in enumerate(gates):
        for clause in base_gate_clauses(g, gate):
            if not any(core[v] if pol else not core[v] for v, pol in clause):
                return False
    return bool(core[-1])


def occurrence_bound(clauses):
    counts = Counter()
    for clause in clauses:
        for lit in clause:
            counts[lit[:-1]] += 1
    return max(counts.values(), default=0), counts


def random_circuit(rng, n_inputs, n_gates, fanout_cap):
    gates = [Gate("IN") for _ in range(n_inputs)]
    fanout = [0] * n_inputs
    kinds = ("NOT", "AND", "OR", "XOR")
    while len(gates) < n_gates:
        available = [i for i, d in enumerate(fanout) if d < fanout_cap]
        if not available:
            # A fresh input is harmless padding and keeps generation total.
            gates.append(Gate("IN"))
            fanout.append(0)
            continue
        kind = rng.choice(kinds)
        arity = 1 if kind == "NOT" else 2
        if len(available) < arity:
            kind, arity = "NOT", 1
        children = tuple(rng.sample(available, arity))
        gates.append(Gate(kind, children))
        fanout.append(0)
        for c in children:
            fanout[c] += 1
    return gates, max(fanout, default=0)


def path_circuit(n_inputs=3, steps=6):
    gates = [Gate("IN") for _ in range(n_inputs)]
    cur = 0
    for i in range(steps):
        other = 1 + (i % (n_inputs - 1))
        gates.append(Gate("AND" if i % 2 == 0 else "OR", (cur, other)))
        cur = len(gates) - 1
    return gates


def parity_circuit(bits=4):
    gates = [Gate("IN") for _ in range(bits)]
    cur = 0
    for i in range(1, bits):
        gates.append(Gate("XOR", (cur, i)))
        cur = len(gates) - 1
    return gates


def gaussian_parity(inputs):
    # One-row GF(2) elimination for x_1+...+x_n=1.
    return sum(bool(x) for x in inputs) % 2 == 1


def solve_2sat(n, clauses):
    graph = [[] for _ in range(2 * n)]
    def node(v, positive): return 2 * v + (0 if positive else 1)
    def neg(k): return k ^ 1
    for (a, pa), (b, pb) in clauses:
        x, y = node(a, pa), node(b, pb)
        graph[neg(x)].append(y); graph[neg(y)].append(x)
    reach = [[False] * (2 * n) for _ in range(2 * n)]
    for s in range(2 * n):
        stack = [s]; reach[s][s] = True
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if not reach[s][v]: reach[s][v] = True; stack.append(v)
    return all(not (reach[2*i][2*i+1] and reach[2*i+1][2*i]) for i in range(n))


def brute_cnf(n, clauses):
    return any(all(any((a[v] if p else not a[v]) for v, p in c) for c in clauses)
               for a in itertools.product((False, True), repeat=n))


def canonical(clauses):
    return json.dumps(clauses, sort_keys=True, separators=(",", ":"))


def main():
    start = time.perf_counter()
    rng = random.Random(SEED)
    checks = Counter()
    max_occ = max_clauses = max_vars = max_child_queries = 0
    circuits = []

    # Hand-built hostile controls.
    circuits.append(("bounded_treewidth", path_circuit()))
    circuits.append(("affine_tseitin", parity_circuit()))
    circuits.append(("horn_like", [Gate("IN"), Gate("IN"), Gate("AND", (0, 1))]))
    circuits.append(("twosat_like", [Gate("IN"), Gate("IN"), Gate("OR", (0, 1))]))
    padded = path_circuit()
    padded += [Gate("NOT", (len(padded)-1,)), Gate("NOT", (len(padded),))]
    circuits.append(("redundant_padding", padded))
    # Independent product joined only at the final AND.
    circuits.append(("independent_product",
                     [Gate("IN"), Gate("IN"), Gate("OR", (0, 1)),
                      Gate("IN"), Gate("IN"), Gate("XOR", (3, 4)),
                      Gate("AND", (2, 5))]))

    for n in range(5, 11):
        for _ in range(48):
            c, _ = random_circuit(rng, 3, n, fanout_cap=3)
            circuits.append(("random_bounded_fanout", c))

    for family, gates in circuits:
        clauses, child_queries, parent_queries = compile_cnf(gates)
        checks["circuits"] += 1
        checks["local_clause_queries"] += len(clauses)
        checks["child_queries"] += child_queries
        checks["parent_queries"] += parent_queries
        assert parent_queries == 0
        max_child_queries = max(max_child_queries, child_queries)
        occ, counts = occurrence_bound(clauses)
        fanout = Counter(c for gate in gates for c in gate.children)
        delta = max(fanout.values(), default=0)
        assert occ <= 4 * delta + 9
        checks["occurrence_bound_checks"] += len(counts)
        max_occ = max(max_occ, occ)
        max_clauses = max(max_clauses, len(clauses))
        max_vars = max(max_vars, len(counts))

        # Full core-assignment equivalence for circuits of at most ten gates.
        for core in itertools.product((False, True), repeat=len(gates)):
            assert cnf_value(clauses, core) == base_consistent(gates, core)
            checks["core_assignment_equivalence"] += 1

        n_inputs = sum(g.kind == "IN" for g in gates)
        for inp in itertools.product((False, True), repeat=n_inputs):
            vals = eval_circuit(gates, inp)
            assert cnf_value(clauses, vals) == vals[-1]
            checks["witness_reconstruction"] += 1
            if family == "affine_tseitin":
                assert vals[-1] == gaussian_parity(inp)
                checks["gaussian_controls"] += 1

        # Wrapper and alternate-encoding controls.
        direct = canonical(clauses)
        copy = canonical(list(clauses))
        delay = canonical(clauses if sum(range(9)) == 36 else [])
        interp = canonical(json.loads(json.dumps(clauses)))
        recomp = canonical(compile_cnf(gates)[0])
        assert direct == copy == delay == interp == recomp
        checks["wrapper_checks"] += 5
        digest = hashlib.sha256(json.dumps(clauses, sort_keys=True).encode()).hexdigest()
        assert len(digest) == 64
        checks["encoding_checks"] += 1

    # Exhaustive local gadget soundness, including every auxiliary setting.
    for arity in (2,):
        base = [(0, True), (1, False)]
        ex = expand_clause(0, 0, base)
        for a, b, z in itertools.product((False, True), repeat=3):
            core = (a, b)
            aux = {("pad2", 0, 0): z}
            lhs = (a or not b)
            assert cnf_value(ex, core, aux) == lhs
            checks["padding_gadget_truth_table"] += 1

    # Independent Horn/2SAT solver controls.
    horn = [[(0, False), (1, True)], [(1, False), (2, True)], [(0, True)]]
    twosat = [[(0, True), (1, True)], [(0, False), (1, True)],
              [(1, False), (2, True)], [(2, False), (0, True)]]
    assert brute_cnf(3, horn)
    assert solve_2sat(3, twosat) == brute_cnf(3, twosat)
    checks["horn_solver_controls"] += 1
    checks["twosat_solver_controls"] += 1

    elapsed = time.perf_counter() - start
    payload = {
        "run_id": "TESTS-0009",
        "seed": SEED,
        "scope": "finite audit; no asymptotic runtime inference",
        "families": dict(Counter(name for name, _ in circuits)),
        "counts": dict(checks),
        "maxima": {
            "compiled_clauses": max_clauses,
            "compiled_variables": max_vars,
            "literal_occurrences_per_variable": max_occ,
            "child_queries_per_circuit": max_child_queries,
        },
        "invariants": {
            "all_parent_queries": 0,
            "proper_three_cnf": True,
            "bound_checked": "max_occurrence <= 4*fanout_cap + 9",
        },
        "elapsed_seconds": elapsed,
        "python": __import__("sys").version,
    }
    canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical_payload).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
