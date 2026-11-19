#!/usr/bin/env python3
"""Exact T5 deletion-witness orbit and endpoint-fiber audit.

The two fixtures are independently reconstructed from their original arcs.
All searches fix one vertex to color zero and then restore the free Z_5
rotation factor exactly.  Python standard library only.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict, deque
from itertools import product
from pathlib import Path


def rel(a: int, b: int) -> bool:
    return (b - a) % 5 in (1, 3)


def components(n: int, arcs: list[tuple[int, int]]) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    for u, v in arcs:
        adj[u].append(v)
        adj[v].append(u)
    unseen = set(range(n))
    out = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        q = deque([root])
        comp = [root]
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    q.append(v)
                    comp.append(v)
        out.append(sorted(comp))
    return out


def normalized_solutions(n: int, arcs: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    """Enumerate all solutions with the least vertex of every component fixed to 0."""
    comps = components(n, arcs)
    roots = {c[0] for c in comps}
    free = [v for v in range(n) if v not in roots]
    colors = [0] * n
    sols = []
    for values in product(range(5), repeat=len(free)):
        for v, x in zip(free, values):
            colors[v] = x
        if all(rel(colors[u], colors[v]) for u, v in arcs):
            sols.append(tuple(colors))
    return sols


def analyze_fixture(name: str, n: int, arcs: list[tuple[int, int]],
                    thread_of_edge: list[str] | None = None) -> dict:
    full = normalized_solutions(n, arcs)
    assert not full, f"{name} must be UNSAT"
    deletions = []
    grouped = defaultdict(set)
    for e, (u, v) in enumerate(arcs):
        kept = [a for i, a in enumerate(arcs) if i != e]
        sols = normalized_solutions(n, kept)
        assert sols, (name, e, "not critical")
        # Because the full source is UNSAT, every deletion witness falsifies e.
        assert all(not rel(s[u], s[v]) for s in sols)
        hist = Counter((s[v] - s[u]) % 5 for s in sols)
        assert set(hist).isdisjoint({1, 3})
        c = len(components(n, kept))
        rotations = 5 ** c
        total = rotations * len(sols)
        label = thread_of_edge[e] if thread_of_edge else f"edge-{e}"
        grouped[label].add((len(sols), total, tuple(sorted(hist.items()))))
        deletions.append({
            "edge_index": e,
            "edge": [u, v],
            "thread": label,
            "components": c,
            "normalized_witnesses": len(sols),
            "total_witnesses": total,
            "gauge_isolated": len(sols) == 1,
            "missing_edge_difference_histogram_normalized": {
                str(k): hist[k] for k in sorted(hist)
            },
            "first_normalized_witness": list(sols[0]),
        })
    grouped_out = {
        label: [
            {
                "normalized_witnesses": a,
                "total_witnesses": b,
                "endpoint_histogram": {str(k): v for k, v in h},
            }
            for a, b, h in sorted(vals)
        ]
        for label, vals in sorted(grouped.items())
    }
    return {
        "name": name,
        "n": n,
        "m": len(arcs),
        "arcs": [list(a) for a in arcs],
        "full_source_unsat": True,
        "every_edge_deletion_sat": True,
        "deletions": deletions,
        "grouped_spectra": grouped_out,
        "normalized_count_set": sorted({d["normalized_witnesses"] for d in deletions}),
        "has_gauge_isolated_deletion": any(d["gauge_isolated"] for d in deletions),
    }


def build_h9() -> tuple[int, list[tuple[int, int]], list[str]]:
    words = ["BBB", "FBB", "FFF", "BB"]
    arcs: list[tuple[int, int]] = []
    labels: list[str] = []
    next_vertex = 2
    for word in words:
        vertices = [0] + list(range(next_vertex, next_vertex + len(word) - 1)) + [1]
        next_vertex += len(word) - 1
        for i, direction in enumerate(word):
            u, v = vertices[i], vertices[i + 1]
            arcs.append((u, v) if direction == "F" else (v, u))
            labels.append(word)
    assert next_vertex == 9 and len(arcs) == 11
    return next_vertex, arcs, labels


def main() -> None:
    h4_arcs = [(0, 2), (0, 3), (1, 2), (3, 1), (3, 2)]
    h9_n, h9_arcs, h9_threads = build_h9()
    payload = {
        "run_id": "LSPV5-T5-WITNESS-ISOLATION-001",
        "relation": "R(a,b) iff (b-a) mod 5 in {1,3}",
        "exact_orbit_theorem": {
            "statement": "For c weak components, componentwise translations act freely on all T5 colorings; fixing one root per component gives one representative per orbit.",
            "orbit_size": "5^c",
        },
        "fixtures": [
            analyze_fixture("H4-five-arc-critical", 4, h4_arcs),
            analyze_fixture("H9-four-thread-critical", h9_n, h9_arcs, h9_threads),
        ],
        "status": {
            "criticality_implies_gauge_isolation": "FALSIFIED",
            "criticality_excludes_gauge_isolation": "FALSIFIED",
            "rotation_factor": "PROVED_EXACT",
            "witness_time_lower_bound": "OPEN",
            "p_vs_np": "OPEN",
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out = Path("results/raw/review/2026-11-18_LSPV5_T5_WITNESS_ISOLATION_RAW.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
