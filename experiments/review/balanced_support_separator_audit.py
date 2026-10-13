#!/usr/bin/env python3
"""Bounded audit of a naive balanced YES/NO source for the L22 compiler.

The two source ensembles have identical vertex/edge/degree statistics:
  YES: 7r disjoint K_{3,3,3};
  NO:  9r disjoint K_7.
They are nevertheless separated in linear time by component sizes, even after
vertex relabelling.  The component-local compiler bookkeeping is checked
symbolically.  This is a finite audit, not an asymptotic lower bound.
"""

from __future__ import annotations

import json
import random
import time
from collections import Counter, deque
from pathlib import Path


def complete_graph(offset: int, size: int):
    return [(offset + i, offset + j) for i in range(size) for j in range(i + 1, size)]


def complete_tripartite(offset: int):
    parts = [[offset + 3 * p + i for i in range(3)] for p in range(3)]
    edges = []
    for p in range(3):
        for q in range(p + 1, 3):
            edges.extend((u, v) for u in parts[p] for v in parts[q])
    return edges, parts


def source_instance(kind: str, r: int):
    edges = []
    coloring = {}
    if kind == "yes":
        for c in range(7 * r):
            local, parts = complete_tripartite(9 * c)
            edges.extend(local)
            for colour, part in enumerate(parts):
                for vertex in part:
                    coloring[vertex] = colour
        n = 63 * r
    elif kind == "no":
        for c in range(9 * r):
            edges.extend(complete_graph(7 * c, 7))
        n = 63 * r
    else:
        raise ValueError(kind)
    return n, edges, coloring


def permute(n, edges, rng):
    p = list(range(n))
    rng.shuffle(p)
    return [(p[u], p[v]) for u, v in edges]


def graph_stats(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n or 0 <= v < u < n
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    sizes = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        q = deque([root])
        size = 0
        while q:
            u = q.popleft()
            size += 1
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    q.append(v)
        sizes.append(size)
    return {
        "n": n,
        "m": len(edges),
        "degree_histogram": dict(sorted(Counter(map(len, adj)).items())),
        "component_sizes": sorted(sizes),
    }


def support_separator(stats):
    sizes = stats["component_sizes"]
    n = stats["n"]
    if stats["m"] != 3 * n or stats["degree_histogram"] != {6: n}:
        return None
    if sizes and all(s == 9 for s in sizes) and 9 * len(sizes) == n:
        return "yes"
    if sizes and all(s == 7 for s in sizes) and 7 * len(sizes) == n:
        return "no"
    return None


def target_counts(source_vertices):
    # For a 6-regular source component, e=3h.  The audited compiler identities
    # are v=1008h+1188e and M=1344h+1584e.
    h = source_vertices
    e = 3 * h
    return {
        "variables": 1008 * h + 1188 * e,
        "clauses": 1344 * h + 1584 * e,
    }


def target_signature(kind, r):
    h, count = (9, 7 * r) if kind == "yes" else (7, 9 * r)
    local = target_counts(h)
    return {
        "component_count": count,
        "component_variables": local["variables"],
        "component_clauses": local["clauses"],
        "total_variables": count * local["variables"],
        "total_clauses": count * local["clauses"],
    }


def audit():
    started = time.perf_counter()
    rng = random.Random(202610131252)
    assertions = 0
    records = []
    for r in range(1, 9):
        yes_n, yes_edges, yes_coloring = source_instance("yes", r)
        no_n, no_edges, _ = source_instance("no", r)
        assert yes_n == no_n == 63 * r
        assertions += 1
        # Explicit proper colouring witness for the YES source.
        assert all(yes_coloring[u] != yes_coloring[v] for u, v in yes_edges)
        assertions += 1
        # Each NO component contains K7, hence is not 3-colourable.
        assert len(no_edges) == 189 * r
        assertions += 1
        for seed in range(32):
            ystats = graph_stats(yes_n, permute(yes_n, yes_edges, rng))
            nstats = graph_stats(no_n, permute(no_n, no_edges, rng))
            assert ystats["n"] == nstats["n"]
            assert ystats["m"] == nstats["m"] == 189 * r
            assert ystats["degree_histogram"] == nstats["degree_histogram"] == {6: 63 * r}
            assert support_separator(ystats) == "yes"
            assert support_separator(nstats) == "no"
            assertions += 5
        ys = target_signature("yes", r)
        ns = target_signature("no", r)
        assert ys["total_variables"] == ns["total_variables"] == 288036 * r
        assert ys["total_clauses"] == ns["total_clauses"] == 384048 * r
        assert (ys["component_count"], ys["component_variables"], ys["component_clauses"]) == (7 * r, 41148, 54864)
        assert (ns["component_count"], ns["component_variables"], ns["component_clauses"]) == (9 * r, 32004, 42672)
        assertions += 4
        records.append({"r": r, "source_n": 63 * r, "source_m": 189 * r,
                        "yes_target": ys, "no_target": ns})

    # Hostile off-support control: the circulant C_14(1,2,3) is 6-regular,
    # has m=3n, and has neither all-7 nor all-9 component sizes.
    n = 14
    off_edges = sorted({tuple(sorted((u, (u + d) % n))) for u in range(n) for d in (1, 2, 3)})
    off = graph_stats(n, off_edges)
    assert off["degree_histogram"] == {6: 14}
    assert support_separator(off) is None
    assertions += 2

    return {
        "run_id": "BALMIXFW1",
        "status": "COMPUTATIONAL",
        "seed": 202610131252,
        "r_values": list(range(1, 9)),
        "permutations_per_kind_per_r": 32,
        "assertions": assertions,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "source_invariant": "same n=63r, m=189r, and all degrees 6",
        "separator": "connected-component sizes: all 9 => YES support; all 7 => NO support",
        "compiler_identity": "component-local; v=4572h and M=6096h for a 6-regular source component",
        "off_support_control": off,
        "records": records,
        "interpretation": "A balanced mixture of these supports is trivial on its promise support; this does not yield a polynomial decider for L22.",
    }


if __name__ == "__main__":
    out = audit()
    path = Path("results/raw/review/2026-10-13_1252_balanced_support_separator.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("run_id", "status", "assertions", "elapsed_seconds", "separator")}, sort_keys=True))
