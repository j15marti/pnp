#!/usr/bin/env python3
"""Bounded audit for the BALMIXFW1 support-repair firewall.

Constructs a connected 6-regular YES/NO pair on nine vertices, verifies
matched coarse invariants and 1-WL, and exhibits a polynomial separator
that survives relabeling, equal-size independent products, and any compiler
image with a polynomial-time left inverse.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from collections import Counter, deque
from pathlib import Path


Graph = tuple[frozenset[int], ...]


def empty_graph(n: int) -> list[set[int]]:
    return [set() for _ in range(n)]


def freeze(g: list[set[int]]) -> Graph:
    return tuple(frozenset(x) for x in g)


def add_edge(g: list[set[int]], u: int, v: int) -> None:
    assert u != v
    g[u].add(v)
    g[v].add(u)


def k333() -> Graph:
    g = empty_graph(9)
    part = [0] * 3 + [1] * 3 + [2] * 3
    for u in range(9):
        for v in range(u + 1, 9):
            if part[u] != part[v]:
                add_edge(g, u, v)
    return freeze(g)


def complement_c9() -> Graph:
    g = empty_graph(9)
    cycle_edges = {
        tuple(sorted((i, (i + 1) % 9))) for i in range(9)
    }
    for u in range(9):
        for v in range(u + 1, 9):
            if (u, v) not in cycle_edges:
                add_edge(g, u, v)
    return freeze(g)


def edges(g: Graph) -> list[tuple[int, int]]:
    return [(u, v) for u in range(len(g)) for v in g[u] if u < v]


def components(g: Graph) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for s in range(len(g)):
        if s in seen:
            continue
        seen.add(s)
        q = deque([s])
        comp: list[int] = []
        while q:
            u = q.popleft()
            comp.append(u)
            for v in g[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        out.append(sorted(comp))
    return out


def induced(g: Graph, vs: list[int]) -> Graph:
    pos = {v: i for i, v in enumerate(vs)}
    return tuple(
        frozenset(pos[w] for w in g[v] if w in pos)
        for v in vs
    )


def diameter(g: Graph) -> int:
    assert len(components(g)) == 1
    best = 0
    for s in range(len(g)):
        dist = [-1] * len(g)
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    q.append(v)
        best = max(best, max(dist))
    return best


def triangle_count(g: Graph) -> int:
    return sum(
        1
        for a in range(len(g))
        for b in range(a + 1, len(g))
        if b in g[a]
        for c in range(b + 1, len(g))
        if c in g[a] and c in g[b]
    )


def color_refinement_histories(g: Graph) -> list[list[int]]:
    colors = [0] * len(g)
    hist = [sorted(Counter(colors).values())]
    while True:
        signatures = [
            (colors[u], tuple(sorted(colors[v] for v in g[u])))
            for u in range(len(g))
        ]
        table = {sig: i for i, sig in enumerate(sorted(set(signatures)))}
        nxt = [table[sig] for sig in signatures]
        hist.append(sorted(Counter(nxt).values()))
        if nxt == colors:
            return hist
        colors = nxt


def three_coloring(g: Graph) -> list[int] | None:
    n = len(g)
    color = [-1] * n

    def search(colored: int) -> bool:
        if colored == n:
            return True
        candidates = [u for u in range(n) if color[u] < 0]
        u = max(
            candidates,
            key=lambda x: (len({color[v] for v in g[x] if color[v] >= 0}), len(g[x])),
        )
        forbidden = {color[v] for v in g[u] if color[v] >= 0}
        for c in range(3):
            if c not in forbidden:
                color[u] = c
                if search(colored + 1):
                    return True
                color[u] = -1
        return False

    return color.copy() if search(0) else None


def matrix_trace_powers(g: Graph, max_power: int = 6) -> list[int]:
    n = len(g)
    a = [[1 if j in g[i] else 0 for j in range(n)] for i in range(n)]
    p = [row[:] for row in a]
    out = []
    for _ in range(max_power):
        out.append(sum(p[i][i] for i in range(n)))
        p = [
            [sum(p[i][k] * a[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)
        ]
    return out


def relabel(g: Graph, perm: list[int]) -> Graph:
    out = empty_graph(len(g))
    for u, v in edges(g):
        add_edge(out, perm[u], perm[v])
    return freeze(out)


def copies(g: Graph, count: int) -> Graph:
    n = len(g)
    out = empty_graph(n * count)
    for i in range(count):
        off = i * n
        for u, v in edges(g):
            add_edge(out, off + u, off + v)
    return freeze(out)


def component_triangle_signature(g: Graph) -> list[tuple[int, int]]:
    return sorted((len(vs), triangle_count(induced(g, vs))) for vs in components(g))


def source_separator(g: Graph) -> str:
    sig = component_triangle_signature(g)
    if sig and all(x == (9, 27) for x in sig):
        return "YES_SUPPORT"
    if sig and all(x == (9, 30) for x in sig):
        return "NO_SUPPORT"
    return "UNKNOWN"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=20261013)
    parser.add_argument("--permutations", type=int, default=128)
    parser.add_argument("--max-copies", type=int, default=12)
    args = parser.parse_args()

    started = time.perf_counter()
    rng = random.Random(args.seed)
    gy = k333()
    gn = complement_c9()
    assertions = 0

    def check(condition: bool) -> None:
        nonlocal assertions
        assertions += 1
        assert condition

    common = {
        "vertices": len(gy),
        "edges": len(edges(gy)),
        "degree_multiset": sorted(len(x) for x in gy),
        "component_sizes": sorted(len(x) for x in components(gy)),
        "diameter": diameter(gy),
        "one_wl_histories": color_refinement_histories(gy),
    }
    check(common["vertices"] == len(gn) == 9)
    check(common["edges"] == len(edges(gn)) == 27)
    check(common["degree_multiset"] == sorted(len(x) for x in gn) == [6] * 9)
    check(common["component_sizes"] == sorted(len(x) for x in components(gn)) == [9])
    check(common["diameter"] == diameter(gn) == 2)
    check(common["one_wl_histories"] == color_refinement_histories(gn))

    cy = three_coloring(gy)
    cn = three_coloring(gn)
    check(cy is not None)
    check(cn is None)
    check(all(cy[u] != cy[v] for u, v in edges(gy)))
    check(triangle_count(gy) == 27)
    check(triangle_count(gn) == 30)
    check(source_separator(gy) == "YES_SUPPORT")
    check(source_separator(gn) == "NO_SUPPORT")

    relabel_checks = 0
    for count in range(1, args.max_copies + 1):
        for label, base, expected in (
            ("yes", gy, "YES_SUPPORT"),
            ("no", gn, "NO_SUPPORT"),
        ):
            product = copies(base, count)
            check(sorted(len(vs) for vs in components(product)) == [9] * count)
            check(sorted(len(x) for x in product) == [6] * (9 * count))
            check(source_separator(product) == expected)
            for _ in range(args.permutations):
                perm = list(range(len(product)))
                rng.shuffle(perm)
                shuffled = relabel(product, perm)
                check(source_separator(shuffled) == expected)
                relabel_checks += 1

    # Component-local compiler counts cited in BALMIXFW1 for 6-regular sources.
    compiled_counts = {
        "variables_per_source_vertex": 4572,
        "clauses_per_source_vertex": 6096,
        "yes_nine_vertex_component": {"variables": 41148, "clauses": 54864},
        "no_nine_vertex_component": {"variables": 41148, "clauses": 54864},
    }
    check(4572 * 9 == compiled_counts["yes_nine_vertex_component"]["variables"])
    check(6096 * 9 == compiled_counts["yes_nine_vertex_component"]["clauses"])
    check(
        compiled_counts["yes_nine_vertex_component"]
        == compiled_counts["no_nine_vertex_component"]
    )

    result = {
        "run_id": "REDTEAM-STRENGTHEN11",
        "seed": args.seed,
        "parameters": {
            "permutations_per_label_per_copy_count": args.permutations,
            "max_copies": args.max_copies,
        },
        "status": "COMPUTATIONAL",
        "pair": {
            "yes": "K_{3,3,3}",
            "no": "complement(C_9)",
            "common_invariants": common,
            "three_colorable": {"yes": True, "no": False},
            "triangles": {"yes": triangle_count(gy), "no": triangle_count(gn)},
            "closed_walk_traces_1_to_6": {
                "yes": matrix_trace_powers(gy),
                "no": matrix_trace_powers(gn),
            },
        },
        "compiler_arithmetic": compiled_counts,
        "separator": "decode if necessary, split components, count triangles per 9-vertex component",
        "relabel_checks": relabel_checks,
        "assertions": assertions,
        "limitations": [
            "Finite validation does not prove average-case hardness or an unrestricted lower bound.",
            "The pair evades component-size and 1-WL separators but is deliberately separated by triangle count.",
            "Compiler-image separation uses the existing polynomial-time decoder theorem as a premise.",
        ],
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    digest_input = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(digest_input).hexdigest()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
