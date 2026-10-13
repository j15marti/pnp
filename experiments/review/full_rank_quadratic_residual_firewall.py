#!/usr/bin/env python3
"""Finite audit for the full-rank quadratic residual firewall.

The symbolic claim checked here is elementary: if C is the cotree of a
spanning forest and |C|=2t, then q(y)=sum_i y[2i]y[2i+1] has full polar rank
2t, while q(y)=b has the explicit witness 0 (b=0) or (1,1,0,...,0)
(b=1).  Every cotree assignment extends uniquely through a consistent
Tseitin system by a leaf-to-root forest solve.

This program independently checks the algebra, reconstruction, compact
circuit evaluation, input validation, renaming/phase controls, and two graph
families.  It does not infer asymptotic runtime from measured timing.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable


SEED = 202610132036
DEADLINE_SECONDS = 25.0


def gf2_rank(rows: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def components(n: int, edges: list[tuple[int, int]], use: set[int] | None = None) -> list[list[int]]:
    adj = [[] for _ in range(n)]
    allowed = range(len(edges)) if use is None else use
    for ei in allowed:
        u, v = edges[ei]
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    out: list[list[int]] = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        comp = []
        stack = [root]
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        out.append(comp)
    return out


def boundary(n: int, edges: list[tuple[int, int]], x: list[int]) -> list[int]:
    c = [0] * n
    for bit, (u, v) in zip(x, edges):
        if bit:
            c[u] ^= 1
            c[v] ^= 1
    return c


def even_on_components(n: int, edges: list[tuple[int, int]], charge: list[int]) -> bool:
    return all(sum(charge[v] for v in comp) % 2 == 0 for comp in components(n, edges))


def validate_instance(instance: dict[str, Any]) -> None:
    required = {"n", "edges", "forest", "cotree", "charge", "phase", "b"}
    if set(instance) != required:
        raise ValueError("schema")
    n = instance["n"]
    edges = instance["edges"]
    forest = instance["forest"]
    cotree = instance["cotree"]
    charge = instance["charge"]
    phase = instance["phase"]
    b = instance["b"]
    if not isinstance(n, int) or n < 1 or not isinstance(edges, list):
        raise ValueError("header")
    if not isinstance(b, int) or b not in (0, 1):
        raise ValueError("b")
    parsed_edges = []
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError("edge")
        u, v = edge
        if not isinstance(u, int) or not isinstance(v, int) or not (0 <= u < v < n):
            raise ValueError("edge-domain")
        parsed_edges.append((u, v))
    if len(set(parsed_edges)) != len(parsed_edges):
        raise ValueError("duplicate-edge")
    m = len(parsed_edges)
    for name, indices in (("forest", forest), ("cotree", cotree)):
        if not isinstance(indices, list) or any(not isinstance(i, int) or not (0 <= i < m) for i in indices):
            raise ValueError(name)
        if len(set(indices)) != len(indices):
            raise ValueError(name + "-duplicate")
    if set(forest).intersection(cotree) or set(forest).union(cotree) != set(range(m)):
        raise ValueError("partition")
    if len(cotree) == 0 or len(cotree) % 2:
        raise ValueError("cotree-parity")
    if not isinstance(charge, list) or len(charge) != n or any(x not in (0, 1) for x in charge):
        raise ValueError("charge")
    if not isinstance(phase, list) or len(phase) != len(cotree) or any(x not in (0, 1) for x in phase):
        raise ValueError("phase")

    # Forest must have exactly one less edge per component and be acyclic.
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for ei in forest:
        u, v = parsed_edges[ei]
        ru, rv = find(u), find(v)
        if ru == rv:
            raise ValueError("forest-cycle")
        parent[ru] = rv
    graph_cc = len(components(n, parsed_edges))
    if len(forest) != n - graph_cc:
        raise ValueError("forest-size")
    forest_cc = len(components(n, parsed_edges, set(forest)))
    if forest_cc != graph_cc:
        raise ValueError("forest-components")


def solve_forest(instance: dict[str, Any], residual_y: list[int]) -> tuple[list[int], int]:
    """Return x and a conservative logical-operation count."""
    validate_instance(instance)
    n = instance["n"]
    edges = [tuple(e) for e in instance["edges"]]
    forest = instance["forest"]
    cotree = instance["cotree"]
    charge = list(instance["charge"])
    phase = instance["phase"]
    if len(residual_y) != len(cotree):
        raise ValueError("residual length")
    if not even_on_components(n, edges, charge):
        raise ValueError("inconsistent charge")

    x = [0] * len(edges)
    ops = 0
    # Residual uses y_j = x_{cotree[j]} XOR phase_j.
    for j, ei in enumerate(cotree):
        x[ei] = residual_y[j] ^ phase[j]
        if x[ei]:
            u, v = edges[ei]
            charge[u] ^= 1
            charge[v] ^= 1
            ops += 2

    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei in forest:
        u, v = edges[ei]
        adj[u].append((v, ei))
        adj[v].append((u, ei))
        ops += 2

    seen = [False] * n
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        parent = [-1] * n
        parent_edge = [-1] * n
        order = [root]
        for u in order:
            for v, ei in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    parent[v] = u
                    parent_edge[v] = ei
                    order.append(v)
                    ops += 1
        for v in reversed(order[1:]):
            bit = charge[v]
            x[parent_edge[v]] = bit
            if bit:
                charge[parent[v]] ^= 1
                ops += 1
            charge[v] = 0
        if charge[root] != 0:
            raise AssertionError("component parity was not discharged")
    return x, ops


def q_value(y: list[int]) -> int:
    return sum(y[i] & y[i + 1] for i in range(0, len(y), 2)) & 1


def q_circuit_value(y: list[int]) -> tuple[int, int]:
    products = [y[i] & y[i + 1] for i in range(0, len(y), 2)]
    if not products:
        raise ValueError("empty residual")
    value = products[0]
    gates = len(products)
    for term in products[1:]:
        value ^= term
        gates += 1
    return value, gates


def easy_residual_witness(dimension: int, b: int) -> list[int]:
    if dimension <= 0 or dimension % 2:
        raise ValueError("dimension")
    y = [0] * dimension
    if b:
        y[0] = y[1] = 1
    return y


def polar_rows(dimension: int) -> list[int]:
    rows = []
    for i in range(dimension):
        rows.append(1 << (i ^ 1))
    return rows


def build_friendship(two_t: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    if two_t <= 0 or two_t % 2:
        raise ValueError("need an even number of triangles")
    n = 1 + 2 * two_t
    edges: list[tuple[int, int]] = []
    forest: list[int] = []
    cotree: list[int] = []
    for j in range(two_t):
        a, b = 1 + 2 * j, 2 + 2 * j
        for e, in_tree in [((0, a), True), ((a, b), True), ((0, b), False)]:
            e = tuple(sorted(e))
            idx = len(edges)
            edges.append(e)
            (forest if in_tree else cotree).append(idx)
    return n, edges, forest, cotree


def build_complete_bipartite(odd_side: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    if odd_side < 3 or odd_side % 2 == 0:
        raise ValueError("odd side >=3")
    n = 2 * odd_side
    edges: list[tuple[int, int]] = []
    forest: list[int] = []
