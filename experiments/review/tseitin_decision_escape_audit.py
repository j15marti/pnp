#!/usr/bin/env python3
"""Exact finite audit for BISECTION-DECISION-DECOUPLING7.

This script distinguishes three objects:
  * a canonical Tseitin parity system on a connected graph,
  * a one-bit satisfiability decision from the charge vector, and
  * a declared NAND2/INV implementation of that charge parity.

It does not model physical routing or arbitrary SAT algorithms.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def connected(n: int, edges: list[tuple[int, int]]) -> bool:
    seen = {0}
    stack = [0]
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def gf2_consistent(n: int, edges: list[tuple[int, int]], charges: tuple[int, ...]) -> bool:
    """Gaussian elimination on Bx=c, with one column per undirected edge."""
    rows = []
    for v in range(n):
        mask = 0
        for j, (a, b) in enumerate(edges):
            if v == a or v == b:
                mask ^= 1 << j
        rows.append(mask | (charges[v] << len(edges)))

    pivot_row = 0
    for col in range(len(edges)):
        pivot = next((r for r in range(pivot_row, n) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for r in range(n):
            if r != pivot_row and ((rows[r] >> col) & 1):
                rows[r] ^= rows[pivot_row]
        pivot_row += 1

    coeff_mask = (1 << len(edges)) - 1
    return not any((row & coeff_mask) == 0 and ((row >> len(edges)) & 1) for row in rows)


def exhaustive_graph_audit(max_n: int = 5) -> dict[str, int]:
    graphs = 0
    systems = 0
    failures = 0
    for n in range(2, max_n + 1):
        possible = list(itertools.combinations(range(n), 2))
        for graph_mask in range(1 << len(possible)):
            edges = [e for j, e in enumerate(possible) if (graph_mask >> j) & 1]
            if not connected(n, edges):
                continue
            graphs += 1
            for charges in itertools.product((0, 1), repeat=n):
                systems += 1
                expected = sum(charges) % 2 == 0
                actual = gf2_consistent(n, edges, charges)
                failures += expected != actual
    return {"connected_graphs": graphs, "charge_systems": systems, "failures": failures}


def charge_circuit(vertex_count: int) -> dict[str, int]:
    if vertex_count < 2 or vertex_count & (vertex_count - 1):
        raise ValueError("vertex_count must be a power of two at least 2")
    xor_macros = vertex_count - 1
    nand2 = 4 * xor_macros
    inv = 1
    gates = nand2 + inv
    p_in = 2 * nand2 + inv
    p_out = gates
    return {
        "vertex_charge_inputs": vertex_count,
        "xor2_macros": xor_macros,
        "nand2_gates": nand2,
        "inv_gates": inv,
        "G_total": gates,
        "P_input_terminal_incidences": p_in,
        "P_output_terminal_incidences": p_out,
        "E_source_sink_edges_including_output": p_in + 1,
        "W_distinct_signal_nets": vertex_count + gates,
        "max_fanout_pin_loads": 2,
        "fanout_buffers": 0,
        "static_nominal_MOS": 4 * nand2 + 2 * inv,
        "logic_depth_NAND_levels": 3 * (vertex_count.bit_length() - 1) + 1,
    }


def main() -> None:
    finite = exhaustive_graph_audit(5)
    circuit = charge_circuit(128)
    expected = {
        "G_total": 509,
        "P_input_terminal_incidences": 1017,
        "P_output_terminal_incidences": 509,
        "E_source_sink_edges_including_output": 1018,
        "W_distinct_signal_nets": 637,
        "max_fanout_pin_loads": 2,
        "fanout_buffers": 0,
        "static_nominal_MOS": 2034,
        "logic_depth_NAND_levels": 22,
    }
    count_failures = {k: {"expected": v, "actual": circuit[k]} for k, v in expected.items() if circuit[k] != v}
    result = {
        "run": "BISECTION_DECISION_DECOUPLING7",
        "timestamp_kst": "2026-10-19 12:48",
        "theorem_test": finite,
        "declared_library": {"NAND2": {"nominal_MOS": 4}, "INV": {"nominal_MOS": 2}},
        "charge_circuit_v128": circuit,
        "count_failures": count_failures,
        "source_schema_check": {
            "reported": {"vertices": 128, "variables": 960, "clauses": 2560, "literal_records": 7680, "variable_occurrence_claim": 8},
            "standard_direct_Q7_parity_CNF": {
                "vertices": 128,
                "edge_variables": 7 * 128 // 2,
                "clauses": 128 * (2 ** (7 - 1)),
                "literal_records": 7 * 128 * (2 ** (7 - 1)),
                "edge_variable_occurrences": 2 * (2 ** (7 - 1)),
            },
            "matches_standard_direct_encoding": False,
            "disposition": "QUARANTINE until the auxiliary-variable and clause construction is published",
        },
        "streaming_charge_decider": {
            "source_reads_charge_bits": 128,
            "output_writes": 1,
            "cache_reads": 0,
            "replay_reads": 0,
            "max_live_writable_bits_including_8_bit_index": 9,
        },
        "not_measured": {
            "physical_routing": None,
            "actual_transistor_nets": None,
            "energy": None,
            "arbitrary_cnf_recognition_cost": None,
        },
        "status": "PASS_THEOREM_AND_CIRCUIT; SOURCE_SCHEMA_QUARANTINED" if finite["failures"] == 0 and not count_failures else "FAIL",
        "scope": "exact connected-graph parity theorem and declared implementation upper bound; P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-19_1248_BISECTION_DECISION_DECOUPLING7.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
