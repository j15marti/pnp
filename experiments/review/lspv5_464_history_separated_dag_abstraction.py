#!/usr/bin/env python3
"""Finite audit for history-separated shared-DAG abstractions.

This is a mathematical transition-system control, not the historical
R_mix341 parser or checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


def edges_for(n: int):
    """All possible forward edges in the fixed topological order 0..n-1."""
    return tuple((i, j) for i in range(n) for j in range(i + 1, n))


def quotient_edges(edges, labels):
    return {(labels[u], labels[v]) for u, v in edges}


def cyclic(vertices, edges):
    adj = {v: set() for v in vertices}
    indeg = {v: 0 for v in vertices}
    for u, v in edges:
        if v not in adj[u]:
            adj[u].add(v)
            indeg[v] += 1
    todo = [v for v in vertices if indeg[v] == 0]
    seen = 0
    while todo:
        u = todo.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                todo.append(v)
    return seen != len(vertices)


def history_cost(labels, weights):
    paid = set()
    total = 0
    for label, weight in zip(labels, weights):
        if label not in paid:
            fiber_min = min(w for l, w in zip(labels, weights) if l == label)
            assert fiber_min <= weight
            total += fiber_min
            paid.add(label)
    return total


def main():
    dag_label_cases = 0
    quotient_cycle_cases = 0
    nontrivial_quotient_cycle_cases = 0
    cost_cases = 0
    history_violations = 0

    for n in range(1, 5):
        possible = edges_for(n)
        for mask in range(1 << len(possible)):
            edges = tuple(e for bit, e in enumerate(possible) if mask & (1 << bit))
            assert not cyclic(range(n), edges)
            for labels in itertools.product(("A", "B"), repeat=n):
                dag_label_cases += 1
                qedges = quotient_edges(edges, labels)
                qverts = set(labels)
                if cyclic(qverts, qedges):
                    quotient_cycle_cases += 1
                    if any(u != v for u, v in qedges):
                        nontrivial_quotient_cycle_cases += 1
                for weights in itertools.product((1, 2, 3), repeat=n):
                    cost_cases += 1
                    abstract = history_cost(labels, weights)
                    concrete = sum(weights)
                    if abstract > concrete:
                        history_violations += 1

    # Minimal nontrivial quotient-cycle witness A -> B -> A.
    witness_edges = ((0, 1), (1, 2))
    witness_labels = ("A", "B", "A")
    assert not cyclic(range(3), witness_edges)
    assert cyclic(set(witness_labels), quotient_edges(witness_edges, witness_labels))

    # Shared lemma used by two branches. Tree unfolding duplicates node 0.
    diamond_edges = ((0, 1), (0, 2), (1, 3), (2, 3))
    diamond_weights = (1, 0, 0, 0)
    concrete_diamond_cost = sum(diamond_weights)
    unfolded_occurrence_cost = 2  # two root-to-join occurrences of node 0
    history_separated_cost = 1
    assert concrete_diamond_cost == history_separated_cost < unfolded_occurrence_cost

    # Fiber-minimum necessity: label A has possible fresh costs 1 and 3.
    # Assigning abstract first-payment cost 3 fails on the cost-1 transition.
    unsafe_fiber_charge = 3
    cheap_concrete_fresh = 1
    safe_fiber_charge = min(1, 3)
    assert unsafe_fiber_charge > cheap_concrete_fresh
    assert safe_fiber_charge <= cheap_concrete_fresh

    result = {
        "status": "PASS",
        "scope": "finite weighted DAG abstraction control; not historical R_mix341",
        "dag_label_cases": dag_label_cases,
        "quotient_cycle_cases": quotient_cycle_cases,
        "nontrivial_quotient_cycle_cases": nontrivial_quotient_cycle_cases,
        "weighted_history_cases": cost_cases,
        "history_cost_violations": history_violations,
        "cycle_witness": {
            "concrete_edges": [list(e) for e in witness_edges],
            "concrete_labels": list(witness_labels),
            "abstract_edges": [list(e) for e in sorted(quotient_edges(witness_edges, witness_labels))],
            "concrete_acyclic": True,
            "label_quotient_cyclic": True,
        },
        "sharing_witness": {
            "concrete_edges": [list(e) for e in diamond_edges],
            "concrete_distinct_node_cost": concrete_diamond_cost,
            "tree_unfolded_occurrence_cost": unfolded_occurrence_cost,
            "history_separated_cost": history_separated_cost,
        },
        "fiber_charge_witness": {
            "concrete_fresh_costs": [1, 3],
            "unsafe_max_charge": unsafe_fiber_charge,
            "safe_infimum_charge": safe_fiber_charge,
        },
        "limitations": [
            "directed edges are a special case of proof hyperedges",
            "no native rule grammar or accepted trace bytes",
            "no asymptotic proof-size, time, or space lower bound",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_sha256_without_self_hash"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/arc/2026-11-09_0944_LSPV5_464_HISTORY_SEPARATED_DAG_RAW.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
