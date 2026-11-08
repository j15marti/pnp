#!/usr/bin/env python3
"""LSPV-5/444 exhaustive scope audit for LSPV-3/510 Tseitin clause essentiality."""
from __future__ import annotations

import itertools
import json
import resource
import time


def connected(n, edges):
    if n == 1:
        return True
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {0}
    stack = [0]
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def components_minus(n, edges, removed):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        if removed not in (a, b):
            adj[a].append(b)
            adj[b].append(a)
    remaining = set(range(n)) - {removed}
    out = []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        comp = {root}
        stack = [root]
        while stack:
            for w in adj[stack.pop()]:
                if w in remaining:
                    remaining.remove(w)
                    comp.add(w)
                    stack.append(w)
        out.append(comp)
    return out


def gf2_solve(num_vars, equations):
    basis = {}
    for mask, rhs in equations:
        rhs &= 1
        while mask:
            pivot = (mask & -mask).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs)
                break
            row, bit = basis[pivot]
            mask ^= row
            rhs ^= bit
        else:
            if rhs:
                return None
    assignment = [0] * num_vars
    for pivot in sorted(basis, reverse=True):
        mask, rhs = basis[pivot]
        assignment[pivot] = rhs ^ (
            sum(assignment[j] for j in range(pivot + 1, num_vars) if (mask >> j) & 1) & 1
        )
    return assignment


def brute_sat(num_vars, pins, equations):
    for bits in itertools.product((0, 1), repeat=num_vars):
        if any(bits[e] != b for e, b in pins.items()):
            continue
        if all((sum(bits[e] for e in support) & 1) == rhs for support, rhs in equations):
            return list(bits)
    return None


def audit():
    started = time.perf_counter()
    summaries = []
    total_graphs = total_charge_cases = total_deletions = total_witnesses = 0
    brute_checks = 0
    for n in range(1, 6):
        possible = [(a, b) for a in range(n) for b in range(a + 1, n)]
        n_graphs = n_charges = n_deletions = n_witnesses = 0
        for edge_mask in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if (edge_mask >> i) & 1]
            if not connected(n, edges):
                continue
            n_graphs += 1
            inc = [[i for i, e in enumerate(edges) if v in e] for v in range(n)]
            for charge_mask in range(1 << n):
                if charge_mask.bit_count() % 2 != 1:
                    continue
                charges = [(charge_mask >> v) & 1 for v in range(n)]
                n_charges += 1
                for v in range(n):
                    d = len(inc[v])
                    comps = components_minus(n, edges, v)
                    c = len(comps)
                    witnessed = 0
                    wrong_patterns = [
                        pat for pat in range(1 << d)
                        if ((pat.bit_count() & 1) != charges[v])
                    ]
                    if n >= 2:
                        assert d >= 1 and 1 <= c <= d
                        assert len(wrong_patterns) == 1 << (d - 1)
                    else:
                        assert d == c == 0 and charges[v] == 1
                        assert wrong_patterns == [0]
                    for pat in wrong_patterns:
                        pins = {edge: (pat >> j) & 1 for j, edge in enumerate(inc[v])}
                        predicted = all(
                            (sum(charges[u] for u in comp) & 1)
                            == (
                                sum(
                                    pins[e]
                                    for e, (a, b) in enumerate(edges)
                                    if (a == v and b in comp) or (b == v and a in comp)
                                )
                                & 1
                            )
                            for comp in comps
                        )
                        parity_equations = [
                            (inc[u], charges[u]) for u in range(n) if u != v
                        ]
                        equations = [(1 << e, bit) for e, bit in pins.items()] + [
                            (sum(1 << e for e in support), rhs)
                            for support, rhs in parity_equations
                        ]
                        witness = gf2_solve(len(edges), equations)
                        actual = witness is not None
                        assert actual == predicted
                        if n <= 4:
                            brute = brute_sat(len(edges), pins, parity_equations)
                            assert (brute is not None) == actual
                            brute_checks += 1
                        if actual:
                            assert all(witness[e] == bit for e, bit in pins.items())
                            assert all(
                                (sum(witness[e] for e in support) & 1) == rhs
                                for support, rhs in parity_equations
                            )
                            witnessed += 1
                            n_witnesses += 1
                        n_deletions += 1
                    assert witnessed == 1 << (d - c)
        summaries.append(
            {
                "vertices": n,
                "connected_labeled_simple_graphs": n_graphs,
                "odd_charge_cases": n_charges,
                "deleted_clause_checks": n_deletions,
                "satisfiable_deletions": n_witnesses,
            }
        )
        total_graphs += n_graphs
        total_charge_cases += n_charges
        total_deletions += n_deletions
        total_witnesses += n_witnesses

    result = {
        "experiment": "LSPV5_444_TSEITIN_DEGREE_ZERO_SCOPE",
        "status": "COMPUTATIONAL_EXHAUSTIVE_N_LE_5_PLUS_SYMBOLIC_SCOPE_REPAIR",
        "peer_claim": "[P2-L3-510] any finite connected loopless graph",
        "scope_counterexample": {
            "graph": "one vertex, no edges",
            "degree_d_v": 0,
            "components_c_v_of_G_minus_v": 0,
            "odd_charge": 1,
            "source": "one empty clause under the natural parity-CNF convention",
            "reported_intermediate_claim_1_le_c_v_le_d_v": False,
            "reported_generic_local_clause_count_2_pow_d_minus_1": "undefined as an integer count",
            "essential_clause_count": 1,
            "formula_2_pow_d_minus_c": 1,
        },
        "repair": (
            "State the generic encoding/count proof for connected loopless graphs with at least "
            "two vertices (hence every degree is positive), or separately define the degree-zero "
            "parity CNF. The final M_v=2^(d_v-c_v) formula extends to the singleton under that convention."
        ),
        "exhaustive_range": "all labeled connected simple graphs on 1..5 vertices, every odd charge vector, every local wrong pattern",
        "summaries": summaries,
        "totals": {
            "connected_graphs": total_graphs,
            "odd_charge_cases": total_charge_cases,
            "deleted_clause_checks": total_deletions,
            "satisfiable_deletions": total_witnesses,
            "independent_bruteforce_checks_n_le_4": brute_checks,
        },
        "historical_full_R_mix341": "OPEN",
        "cubic_corollary_510_2": "UNAFFECTED",
        "binary_ancestry_corollary_510_3": "UNAFFECTED_WITH_ITS_STATED_MODEL_CONDITIONS",
        "elapsed_seconds": time.perf_counter() - started,
        "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    audit()

