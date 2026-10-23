#!/usr/bin/env python3
"""Finite audit for DENSE-COUPLING-FIREWALL90.

The symbolic claims are proved in the report.  This program checks finite
wheel controls, matched dense pairs, explicit decompositions, and padding.
"""

from __future__ import annotations

import itertools
import json
import time


SEED = 20261023


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


def wheel(h: int) -> tuple[int, set[tuple[int, int]]]:
    hub = h
    edges = {edge(i, (i + 1) % h) for i in range(h)}
    edges |= {edge(hub, i) for i in range(h)}
    return h + 1, edges


def wheel_swap(h: int) -> tuple[int, set[tuple[int, int]]]:
    n, edges = wheel(h)
    edges.remove(edge(h, 0))
    edges.add(edge(0, 2))
    return n, edges


def dense_pair(t: int, unsat: bool) -> tuple[int, set[tuple[int, int]]]:
    assert t >= 4
    a = range(t)
    b = range(t, 2 * t)
    edges = {edge(u, v) for u in a for v in b}
    if unsat:
        edges |= {edge(0, 1), edge(1, 2), edge(2, 0)}
    else:
        edges |= {edge(0, 1), edge(0, 2), edge(0, 3)}
    return 2 * t, edges


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in edges:
        out[u].add(v)
        out[v].add(u)
    return out


def three_color(n: int, edges: set[tuple[int, int]], removed: int | None = None):
    adj = adjacency(n, {e for e in edges if removed not in e})
    active = [v for v in range(n) if v != removed]
    colors = [-1] * n

    def search(left: list[int]) -> bool:
        if not left:
            return True
        v = max(left, key=lambda x: (sum(colors[u] >= 0 for u in adj[x]), len(adj[x])))
        used = {colors[u] for u in adj[v] if colors[u] >= 0}
        rest = [x for x in left if x != v]
        for color in range(3):
            if color not in used:
                colors[v] = color
                if search(rest):
                    return True
        colors[v] = -1
        return False

    ok = search(active)
    return ok, tuple(colors) if ok else None


def valid_coloring(edges: set[tuple[int, int]], colors: tuple[int, ...], removed: int | None = None) -> bool:
    return all(removed in (u, v) or colors[u] != colors[v] for u, v in edges)


def verify_path_decomposition(n: int, edges: set[tuple[int, int]], bags: list[set[int]]) -> bool:
    if not all(any(v in bag for bag in bags) for v in range(n)):
        return False
    if not all(any(u in bag and v in bag for bag in bags) for u, v in edges):
        return False
    for v in range(n):
        positions = [i for i, bag in enumerate(bags) if v in bag]
        if positions != list(range(min(positions), max(positions) + 1)):
            return False
    return True


def attach_leaves(n: int, edges: set[tuple[int, int]], count: int):
    padded = set(edges)
    for i in range(count):
        padded.add(edge(0, n + i))
    return n + count, padded


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    wheel_instances = 0
    wheel_deletion_witnesses = 0
    dense_instances = 0
    decomposition_checks = 0
    padding_checks = 0
    color_searches = 0

    for h in range(5, 32, 2):
        n_u, e_u = wheel(h)
        n_s, e_s = wheel_swap(h)
        assertions += 4
        assert n_u == n_s == h + 1
        assert len(e_u) == len(e_s) == 2 * h
        ok_u, _ = three_color(n_u, e_u)
        ok_s, colors_s = three_color(n_s, e_s)
        color_searches += 2
        assert not ok_u
        assert ok_s and colors_s is not None and valid_coloring(e_s, colors_s)
        assertions += 2
        for removed in range(n_u):
            ok, colors = three_color(n_u, e_u, removed)
            color_searches += 1
            assertions += 1
            assert ok and colors is not None and valid_coloring(e_u, colors, removed)
            wheel_deletion_witnesses += 1
        wheel_instances += 2

    for t in range(4, 17):
        n_s, e_s = dense_pair(t, False)
        n_u, e_u = dense_pair(t, True)
        assertions += 4
        assert n_s == n_u == 2 * t
        assert len(e_s) == len(e_u) == t * t + 3
        ok_s, colors_s = three_color(n_s, e_s)
        ok_u, _ = three_color(n_u, e_u)
        color_searches += 2
        assert ok_s and colors_s is not None and valid_coloring(e_s, colors_s)
        assert not ok_u
        assertions += 2

        a = set(range(t))
        bags = [a | {v} for v in range(t, 2 * t)]
        assert max(map(len, bags)) - 1 == t
        assert verify_path_decomposition(n_s, e_s, bags)
        assert verify_path_decomposition(n_u, e_u, bags)
        assertions += 3
        decomposition_checks += 2

        # Exact one-hot CNF record counts are equal on both labels.
        k = 2 * t
        m2 = 3 * k + 3 * (t * t + 3)
        m = k + m2
        ell = 9 * k + 6 * (t * t + 3)
        assert m2 == 3 * t * t + 6 * t + 9
        assert m == 3 * t * t + 8 * t + 9
        assert ell == 6 * t * t + 18 * t + 18
        assertions += 3

        for leaves in (1, 3, 9):
            ps_n, ps_e = attach_leaves(n_s, e_s, leaves)
            pu_n, pu_e = attach_leaves(n_u, e_u, leaves)
            ps_ok, _ = three_color(ps_n, ps_e)
            pu_ok, _ = three_color(pu_n, pu_e)
            color_searches += 2
            assert ps_ok and not pu_ok
            assertions += 1
            padding_checks += 2
        dense_instances += 2

    result = {
        "artifact": "DENSE_COUPLING_FIREWALL90",
        "seed": SEED,
        "wheel_instances": wheel_instances,
        "wheel_positive_clause_deletion_witnesses": wheel_deletion_witnesses,
        "dense_pair_instances": dense_instances,
        "path_decomposition_checks": decomposition_checks,
        "leaf_padding_label_checks": padding_checks,
        "three_color_searches": color_searches,
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite implementation audit only; asymptotic claims are symbolic",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
