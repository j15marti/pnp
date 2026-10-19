#!/usr/bin/env python3
"""Exact audit for UNIQUE-FASTFORWARD-FIREWALL10.

Builds the ripple-carry CNF for x_{t+1}=x_t+1 mod 2^m, x_0=0.
Checks the explicit fast-forward assignment, propagation uniqueness, and a
single indexed witness for both state and carry variables.
"""

from __future__ import annotations

import itertools
import json
import math


def add_xor(clauses, z, a, b):
    # z <-> a xor b
    clauses.extend([
        (a, b, -z), (-a, -b, -z),
        (a, -b, z), (-a, b, z),
    ])


def add_and(clauses, z, a, b):
    # z <-> a and b
    clauses.extend([(-a, -b, z), (a, -z), (b, -z)])


def build(m):
    T = 1 << m
    names = []
    def new(name):
        names.append(name)
        return len(names)
    x = [[new(("x", t, j)) for j in range(m)] for t in range(T)]
    c = [[new(("c", t, j)) for j in range(m + 1)] for t in range(T - 1)]
    clauses = []
    for j in range(m):
        clauses.append((-x[0][j],))
    for t in range(T - 1):
        clauses.append((c[t][0],))
        for j in range(m):
            add_xor(clauses, x[t + 1][j], x[t][j], c[t][j])
            add_and(clauses, c[t][j + 1], x[t][j], c[t][j])
    return T, names, x, c, clauses


def expected(name):
    kind, t, j = name
    if kind == "x":
        return (t >> j) & 1
    if j == 0:
        return 1
    return int((t & ((1 << j) - 1)) == ((1 << j) - 1))


def sat(clauses, assignment):
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in cl) for cl in clauses)


def unit_propagate(clauses):
    a = {}
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            undecided = []
            satisfied = False
            for lit in cl:
                v = abs(lit)
                if v in a:
                    if a[v] == (lit > 0):
                        satisfied = True
                        break
                else:
                    undecided.append(lit)
            if satisfied:
                continue
            assert undecided, "conflict during propagation"
            if len(undecided) == 1:
                lit = undecided[0]
                v, val = abs(lit), lit > 0
                if v in a:
                    assert a[v] == val
                else:
                    a[v] = val
                    changed = True
    return a


def indexed_witness(kind, t, j):
    if kind == "x":
        return (t >> j) & 1
    if j == 0:
        return 1
    return int(all((t >> r) & 1 for r in range(j)))


def gate_bound(m):
    # Binary j, shared equality decoders, shared prefix ANDs, two muxes,
    # and a final type selector. Binary fan-in AND/OR/NOT library.
    ell = math.ceil(math.log2(m + 1))
    equality = ell + (m + 1) * (ell - 1)
    return equality + 5 * m + 2


def exhaustive_count(num_vars, clauses):
    count = 0
    for bits in itertools.product((False, True), repeat=num_vars):
        a = {i + 1: bits[i] for i in range(num_vars)}
        count += int(sat(clauses, a))
    return count


def main():
    cases = []
    assertions = 0
    indexed_bits = 0
    for m in range(1, 11):
        T, names, x, c, clauses = build(m)
        assignment = {i + 1: bool(expected(name)) for i, name in enumerate(names)}
        assert sat(clauses, assignment); assertions += 1
        forced = unit_propagate(clauses)
        assert len(forced) == len(names); assertions += 1
        assert forced == assignment; assertions += 1
        for i, name in enumerate(names, 1):
            assert indexed_witness(*name) == int(assignment[i])
            assertions += 1
            indexed_bits += 1
        # Direct serial state control.
        state = 0
        for t in range(T):
            assert state == t
            assertions += 1
            state = (state + 1) % T
        cases.append({
            "m": m, "T": T, "variables": len(names),
            "clauses": len(clauses), "gate_upper_bound": gate_bound(m),
            "all_variables_forced_by_unit_propagation": True,
        })

    exhaustive = {}
    for m in (1, 2):
        _, names, _, _, clauses = build(m)
        exhaustive[str(m)] = exhaustive_count(len(names), clauses)
        assert exhaustive[str(m)] == 1; assertions += 1

    out = {
        "run": "UNIQUE_FASTFORWARD_FIREWALL10",
        "date_kst": "2026-10-20 08:48",
        "model": "binary-fanin AND/OR/NOT indexed witness; ripple-carry CNF",
        "theorem_status": "PROVED explicit family; COMPUTATIONAL audit",
        "family": "unique tableau x_0=0, x_(t+1)=x_t+1 mod 2^m, T=2^m",
        "shared_witness": "W(kind,t,j) gives state bit or carry bit",
        "shared_witness_gate_bound": "ceil(log2(m+1))+(m+1)(ceil(log2(m+1))-1)+5m+2 = O(m log m)",
        "source_description": "uniform local clause generator poly(m); explicit transition",
        "indexed_bits_checked": indexed_bits,
        "assertions": assertions,
        "exhaustive_satisfying_assignment_counts": exhaustive,
        "cases": cases,
        "implication": "uniqueness and exponential history length do not imply shared-witness circuit hardness",
        "actual_diagonal_family_resolved": False,
        "P_vs_NP": "OPEN",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
