#!/usr/bin/env python3
"""Independent exhaustive audit of the LSPV-1/528 pair-defect extension claim.

The graph is two copies of K4 with one edge deleted in each, joined by two
cross edges.  It is simple, connected and cubic, but {0,1} is a nonadjacent
two-vertex cut.  We enumerate all F_3 edge-label assignments and compare the
pair-defect compatibility blocks with the connected-residual prediction.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from collections import Counter, defaultdict, deque
from pathlib import Path

P = 3
VERTICES = tuple(range(8))
EDGES = (
    (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
    (4, 6), (4, 7), (5, 6), (5, 7), (6, 7),
    (0, 4), (1, 5),
)


def components(vertices, edges, deleted=()):
    live = set(vertices) - set(deleted)
    adj = {v: [] for v in live}
    for a, b in edges:
        if a in live and b in live:
            adj[a].append(b)
            adj[b].append(a)
    out = []
    while live:
        root = min(live)
        q = deque([root])
        live.remove(root)
        comp = []
        while q:
            v = q.popleft()
            comp.append(v)
            for w in adj[v]:
                if w in live:
                    live.remove(w)
                    q.append(w)
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out))


def signs(edges, orientation):
    """Return signed vertex-edge incidence for a supplied orientation bit vector."""
    inc = {v: [] for v in VERTICES}
    for i, (a, b) in enumerate(edges):
        tail, head = (a, b) if orientation[i] == 0 else (b, a)
        inc[tail].append((i, 1))
        inc[head].append((i, -1))
    return inc


def divergence(labels, incidence):
    return tuple(sum(s * labels[e] for e, s in incidence[v]) % P for v in VERTICES)


def local_tuple(labels, incidence, v):
    return tuple(labels[e] for e, _ in sorted(incidence[v]))


def enumerate_blocks(charges, orientation):
    sigma = sum(charges) % P
    assert sigma != 0
    incidence = signs(EDGES, orientation)
    pairs = list(itertools.combinations(VERTICES, 2))
    target_to_pair = {}
    for u, v in pairs:
        target = list(charges)
        target[u] = (target[u] + sigma) % P
        target[v] = (target[v] + sigma) % P
        target_to_pair[tuple(target)] = (u, v)

    block_pairs = {pair: set() for pair in pairs}
    witness = {}
    assignment_count = 0
    for labels in itertools.product(range(P), repeat=len(EDGES)):
        assignment_count += 1
        pair = target_to_pair.get(divergence(labels, incidence))
        if pair is None:
            continue
        u, v = pair
        key = (local_tuple(labels, incidence, u), local_tuple(labels, incidence, v))
        block_pairs[pair].add(key)
        witness.setdefault((pair, key), labels)
    return incidence, block_pairs, witness, assignment_count


def expected_block_size(u, v, comps):
    return 27 if (u, v) in EDGES or (v, u) in EDGES or len(comps) > 1 else 81


def run_control(name, charges, orientation, full=False):
    incidence, blocks, witnesses, assignment_count = enumerate_blocks(charges, orientation)
    pair_rows = []
    for pair in sorted(blocks):
        u, v = pair
        comps = components(VERTICES, EDGES, pair)
        adjacent = (u, v) in EDGES or (v, u) in EDGES
        actual = len(blocks[pair])
        expected = expected_block_size(u, v, comps)
        if actual != expected:
            raise AssertionError((name, pair, actual, expected, comps))
        pair_rows.append({
            "pair": list(pair),
            "adjacent": adjacent,
            "residual_components": [list(c) for c in comps],
            "block_edges": actual,
            "expected": expected,
        })

    cut = next(row for row in pair_rows if row["pair"] == [0, 1])
    if cut["adjacent"] or cut["residual_components"] != [[2, 3], [4, 5, 6, 7]]:
        raise AssertionError(cut)
    if cut["block_edges"] != 27:
        raise AssertionError(cut)

    result = {
        "name": name,
        "charges": list(charges),
        "sigma": sum(charges) % P,
        "orientation_bits": list(orientation),
        "assignments_enumerated": assignment_count,
        "cut_pair_0_1": cut,
        "block_size_histogram": dict(sorted(Counter(r["block_edges"] for r in pair_rows).items())),
    }
    if full:
        result["pairs"] = pair_rows
        result["cut_pair_witnesses"] = [
            {
                "local_0": list(k[0]),
                "local_1": list(k[1]),
                "edge_labels": list(witnesses[((0, 1), k)]),
            }
            for k in sorted(blocks[(0, 1)])
        ]
    return result, blocks


def main():
    started = time.time()
    if len(set(EDGES)) != len(EDGES) or any(a == b for a, b in EDGES):
        raise AssertionError("graph is not simple")
    degrees = Counter(v for e in EDGES for v in e)
    if set(degrees.values()) != {3} or set(degrees) != set(VERTICES):
        raise AssertionError(degrees)
    if components(VERTICES, EDGES) != (VERTICES,):
        raise AssertionError("graph is disconnected")

    base_charges = (1,) + (0,) * 7
    zero = (0,) * len(EDGES)
    reverse = (1,) * len(EDGES)
    mixed = tuple(i % 2 for i in range(len(EDGES)))
    base, base_blocks = run_control("base", base_charges, zero, full=True)
    reverse_result, reverse_blocks = run_control("reverse_all", base_charges, reverse)
    mixed_result, mixed_blocks = run_control("mixed_orientation", base_charges, mixed)

    if {p: len(x) for p, x in base_blocks.items()} != {p: len(x) for p, x in reverse_blocks.items()}:
        raise AssertionError("reverse orientation changed block counts")
    if {p: len(x) for p, x in base_blocks.items()} != {p: len(x) for p, x in mixed_blocks.items()}:
        raise AssertionError("mixed orientation changed block counts")

    charge_controls = []
    for charged in VERTICES:
        charges = tuple(1 if v == charged else 0 for v in VERTICES)
        result, _ = run_control(f"charge_at_{charged}", charges, zero)
        charge_controls.append(result)

    # Build the 72-vertex compatibility graph from the exact blocks.
    local_rows = {}
    for v in VERTICES:
        inc = signs(EDGES, zero)
        target = (base_charges[v] + 1) % P
        rows = sorted(t for t in itertools.product(range(P), repeat=3)
                      if sum(s * x for x, (_, s) in zip(t, sorted(inc[v]))) % P == target)
        if len(rows) != 9:
            raise AssertionError((v, rows))
        local_rows[v] = rows
    node_id = {(v, t): 9 * v + i for v in VERTICES for i, t in enumerate(local_rows[v])}
    degrees_h = [0] * 72
    edges_h = set()
    for (u, v), block in base_blocks.items():
        for tu, tv in block:
            a, b = node_id[(u, tu)], node_id[(v, tv)]
            edge = (min(a, b), max(a, b))
            edges_h.add(edge)
    for a, b in edges_h:
        degrees_h[a] += 1
        degrees_h[b] += 1

    # Hostile input controls.
    malformed_edges = EDGES[:-1]
    malformed_degrees = Counter(v for e in malformed_edges for v in e)
    if set(malformed_degrees.values()) == {3}:
        raise AssertionError("non-cubic hostile control was not detected")
    corrupt_local = (0, 0, 0)
    inc0 = sorted(signs(EDGES, zero)[0])
    corrupt_valid = sum(s * x for x, (_, s) in zip(corrupt_local, inc0)) % P == 2
    if corrupt_valid:
        raise AssertionError("corrupt local tuple was accepted")
    accepted_cut_pair = ((0, 0, 2), (0, 0, 1))
    rejected_cut_pair = ((0, 0, 2), (0, 1, 0))
    if accepted_cut_pair not in base_blocks[(0, 1)] or rejected_cut_pair in base_blocks[(0, 1)]:
        raise AssertionError("explicit cut-pair controls failed")

    payload = {
        "schema": "LSPV5-455-pair-defect-2cut-audit-v1",
        "status": "PROVED_RESTRICTED_PLUS_EXHAUSTIVE_CONTROL",
        "graph": {
            "vertices": list(VERTICES),
            "edges": [list(e) for e in EDGES],
            "edge_count": len(EDGES),
            "degrees": {str(v): degrees[v] for v in VERTICES},
            "components": [list(c) for c in components(VERTICES, EDGES)],
            "cut_pair": [0, 1],
            "cut_components": [list(c) for c in components(VERTICES, EDGES, (0, 1))],
        },
        "strict_3cnf": {
            "boolean_variables": 3 * len(EDGES),
            "edge_alo_clauses": len(EDGES),
            "vertex_forbidden_clauses": 18 * len(VERTICES),
            "total_clauses": len(EDGES) + 18 * len(VERTICES),
            "all_width": 3,
            "certified_unsat_reason": "sum of vertex charges is nonzero in F3",
            "proof_size_hardness": "not claimed for this finite non-expander control",
        },
        "base": base,
        "orientation_controls": [reverse_result, mixed_result],
        "charge_location_controls": charge_controls,
        "compatibility_graph": {
            "vertices": 72,
            "edges": len(edges_h),
            "degree_histogram": dict(sorted(Counter(degrees_h).items())),
            "regular_degree_predicted_by_528_under_3connectivity": 9 * len(VERTICES) - 27,
            "regular": len(set(degrees_h)) == 1,
        },
        "hostile_controls": {
            "deleted_edge_rejected_as_cubic": True,
            "deleted_edge_degree_histogram": dict(sorted(Counter(malformed_degrees.values()).items())),
            "corrupt_local_tuple_rejected": True,
            "accepted_cut_local_pair": [list(x) for x in accepted_cut_pair],
            "rejected_cut_local_pair": [list(x) for x in rejected_cut_pair],
            "cut_component_2_3_boundary_condition": "x02+x03+x12+x13=0 mod 3",
            "accepted_boundary_sum": 0,
            "rejected_boundary_sum": 1,
        },
        "claim": {
            "proved_restricted": "For this graph, the nonadjacent cut pair (0,1) has only 27 compatible local pairs, not J9's 81; connected-residual nonadjacent pairs have 81.",
            "analytic_reason": "After fixing the two local tuples, each component of G-{u,v} must have zero residual signed charge; when there are two components this adds one independent compatibility equation.",
            "scope": "The 3-vertex-connectivity assumption in P2-L1-528 cannot be dropped to connected cubic graphs for its J9 block and regular spectrum conclusion.",
            "does_not_claim": "No full R_mix341 lower bound, B3 bridge, asymptotic hardness, or P-versus-NP result.",
        },
        "resource_ledger": {
            "python_edge_assignments_per_run": 3 ** len(EDGES),
            "python_full_runs": 11,
            "logical_inference_nodes": 0,
            "elapsed_seconds": round(time.time() - started, 6),
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256_without_hash_field"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/arc/2026-11-09_0115_LSPV5_455_PAIR_DEFECT_2CUT_RAW.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "cut_block_edges": base["cut_pair_0_1"]["block_edges"],
        "block_size_histogram": base["block_size_histogram"],
        "compatibility_degree_histogram": payload["compatibility_graph"]["degree_histogram"],
        "regular": payload["compatibility_graph"]["regular"],
        "raw": str(out),
        "sha256": payload["payload_sha256_without_hash_field"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
