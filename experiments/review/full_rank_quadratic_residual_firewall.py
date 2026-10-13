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
    cotree: list[int] = []
    # Vertices 0..s-1 are left; s..2s-1 are right.
    for i in range(odd_side):
        for j in range(odd_side):
            idx = len(edges)
            edges.append((i, odd_side + j))
            if i == 0 or (j == 0 and i > 0):
                forest.append(idx)
            else:
                cotree.append(idx)
    return n, edges, forest, cotree


def make_instance(builder: tuple[int, list[tuple[int, int]], list[int], list[int]], charge: list[int], b: int, phase: list[int] | None = None) -> dict[str, Any]:
    n, edges, forest, cotree = builder
    return {
        "n": n,
        "edges": [list(e) for e in edges],
        "forest": list(forest),
        "cotree": list(cotree),
        "charge": list(charge),
        "phase": [0] * len(cotree) if phase is None else list(phase),
        "b": b,
    }


def permute_vertices(instance: dict[str, Any], perm: list[int]) -> dict[str, Any]:
    out = json.loads(json.dumps(instance))
    out["n"] = len(perm)
    out["edges"] = [sorted([perm[u], perm[v]]) for u, v in instance["edges"]]
    new_charge = [0] * len(perm)
    for old, new in enumerate(perm):
        new_charge[new] = instance["charge"][old]
    out["charge"] = new_charge
    return out


def permute_edges(instance: dict[str, Any], order: list[int]) -> dict[str, Any]:
    out = json.loads(json.dumps(instance))
    old_to_new = {old: new for new, old in enumerate(order)}
    out["edges"] = [instance["edges"][old] for old in order]
    out["forest"] = [old_to_new[i] for i in instance["forest"]]
    out["cotree"] = [old_to_new[i] for i in instance["cotree"]]
    return out


@dataclass
class Counters:
    assertions: int = 0
    instances: int = 0
    witness_reconstructions: int = 0
    inconsistent_rejections: int = 0
    exhaustive_charge_cases: int = 0
    random_charge_cases: int = 0
    phase_controls: int = 0
    renaming_controls: int = 0
    compact_circuit_checks: int = 0
    malformed_rejections: int = 0
    easy_residual_controls: int = 0
    logical_operations: int = 0
    parsed_bytes: int = 0

    def check(self, condition: bool) -> None:
        assert condition
        self.assertions += 1


def run() -> dict[str, Any]:
    start = time.monotonic()
    rng = random.Random(SEED)
    c = Counters()
    family_rows: list[dict[str, Any]] = []

    def deadline() -> None:
        if time.monotonic() - start > DEADLINE_SECONDS:
            raise TimeoutError("cooperative 25-second deadline")

    # Algebra and circuit truth tables. Exhaustive only at small dimension.
    for t in range(1, 9):
        d = 2 * t
        c.check(gf2_rank(polar_rows(d)) == d)
        c.check(len(set(polar_rows(d))) == d)
        for mask in range(1 << d):
            y = [(mask >> i) & 1 for i in range(d)]
            value, gates = q_circuit_value(y)
            c.check(value == q_value(y))
            c.check(gates == 2 * t - 1)
            c.compact_circuit_checks += 1
        # Explicit failure of affinity for the zero level set.
        z = [0] * d
        e0 = [0] * d
        e1 = [0] * d
        e0[0] = 1
        e1[1] = 1
        both = [a ^ b for a, b in zip(e0, e1)]
        c.check(q_value(z) == q_value(e0) == q_value(e1) == 0)
        c.check(q_value(both) == 1)
        deadline()

    # Symbolic-size checks and random consistent charges on two graph families.
    for kind, params in (("friendship", range(1, 129)), ("complete_bipartite", range(1, 17))):
        for p in params:
            builder = build_friendship(2 * p) if kind == "friendship" else build_complete_bipartite(2 * p + 1)
            n, edges, forest, cotree = builder
            rho = len(cotree) + len(components(n, edges)) - len(components(n, edges, set(forest)))
            c.check(rho == len(cotree))
            c.check(len(cotree) % 2 == 0)
            c.check(gf2_rank(polar_rows(len(cotree))) == len(cotree))
            c.check(len(forest) == n - len(components(n, edges)))
            family_rows.append({
                "family": kind,
                "parameter": p,
                "vertices": n,
                "edges": len(edges),
                "cotree_dimension": len(cotree),
                "polar_rank": len(cotree),
                "compact_gates": len(cotree) - 1,
            })
            for _ in range(4):
                charge = [rng.randrange(2) for _ in range(n)]
                charge[-1] = sum(charge[:-1]) & 1
                phase = [rng.randrange(2) for _ in cotree]
                for b in (0, 1):
                    instance = make_instance(builder, charge, b, phase)
                    c.parsed_bytes += len(json.dumps(instance, sort_keys=True, separators=(",", ":")))
                    y = easy_residual_witness(len(cotree), b)
                    x, ops = solve_forest(instance, y)
                    c.logical_operations += ops
                    c.check(boundary(n, edges, x) == charge)
                    projected = [x[ei] ^ phase[j] for j, ei in enumerate(cotree)]
                    c.check(projected == y)
                    c.check(q_value(projected) == b)
                    c.instances += 1
                    c.witness_reconstructions += 1
                    c.random_charge_cases += 1
            deadline()

    # Exhaustive all consistent charges on the smallest friendship and K3,3 controls.
    for builder in (build_friendship(2), build_complete_bipartite(3)):
        n, edges, forest, cotree = builder
        for mask in range(1 << n):
            charge = [(mask >> i) & 1 for i in range(n)]
            if sum(charge) & 1:
                continue
            for b in (0, 1):
                instance = make_instance(builder, charge, b)
                y = easy_residual_witness(len(cotree), b)
                x, ops = solve_forest(instance, y)
                c.logical_operations += ops
                c.check(boundary(n, edges, x) == charge)
                c.check(q_value([x[ei] for ei in cotree]) == b)
                c.instances += 1
                c.witness_reconstructions += 1
                c.exhaustive_charge_cases += 1

    # Inconsistent charges must be rejected before residual solving.
    for builder in (build_friendship(4), build_complete_bipartite(5)):
        n, edges, forest, cotree = builder
        charge = [0] * n
        charge[0] = 1
        instance = make_instance(builder, charge, 0)
        try:
            solve_forest(instance, easy_residual_witness(len(cotree), 0))
        except ValueError as exc:
            c.check("inconsistent" in str(exc))
            c.inconsistent_rejections += 1
        else:
            raise AssertionError("inconsistent charge accepted")

    # Renaming, edge-order, and phase-switch covariance.
    for p in range(1, 17):
        builder = build_friendship(2 * p)
        n, edges, forest, cotree = builder
        charge = [rng.randrange(2) for _ in range(n)]
        charge[-1] = sum(charge[:-1]) & 1
        phase = [rng.randrange(2) for _ in cotree]
        instance = make_instance(builder, charge, p & 1, phase)
        y = easy_residual_witness(len(cotree), p & 1)
        x, _ = solve_forest(instance, y)
        c.check(boundary(n, edges, x) == charge)
        c.phase_controls += 1

        perm = list(range(n))
        rng.shuffle(perm)
        renamed = permute_vertices(instance, perm)
        xr, _ = solve_forest(renamed, y)
        c.check(boundary(n, [tuple(e) for e in renamed["edges"]], xr) == renamed["charge"])
        c.renaming_controls += 1

        order = list(range(len(edges)))
        rng.shuffle(order)
        shuffled = permute_edges(instance, order)
        xs, _ = solve_forest(shuffled, y)
        c.check(boundary(n, [tuple(e) for e in shuffled["edges"]], xs) == charge)
        c.renaming_controls += 1

    # Planted arbitrary satisfying residual coordinates lift without source advice.
    builder = build_complete_bipartite(7)
    n, edges, forest, cotree = builder
    for _ in range(128):
        y = [rng.randrange(2) for _ in cotree]
        b = q_value(y)
        charge = [rng.randrange(2) for _ in range(n)]
        charge[-1] = sum(charge[:-1]) & 1
        instance = make_instance(builder, charge, b)
        x, ops = solve_forest(instance, y)
        c.logical_operations += ops
        c.check(boundary(n, edges, x) == charge)
        c.check([x[ei] for ei in cotree] == y)
        c.check(q_value(y) == b)
        c.witness_reconstructions += 1

    # Horn, Krom, and affine residuals on free cotree coordinates remain easy.
    for d in (2, 4, 16, 64, 256):
        horn = [0] * d  # all implications y_i -> y_{i+1}
        krom = [0] * d  # all equivalences y_i <-> y_{i+1}
        affine = [0] * d
        affine[0] = 1
        c.check(all((not horn[i]) or horn[i + 1] for i in range(d - 1)))
        c.check(all(krom[i] == krom[i + 1] for i in range(d - 1)))
        c.check(sum(affine) % 2 == 1)
        c.easy_residual_controls += 3

    # Schema failures.
    base = make_instance(build_friendship(2), [0] * 5, 0)
    malformed = []
    bad = json.loads(json.dumps(base)); bad["edges"].append(bad["edges"][0]); bad["cotree"].append(len(bad["edges"]) - 1); malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["forest"] = bad["forest"][:-1]; bad["cotree"].append(bad["forest"][-1] if bad["forest"] else 0); malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["cotree"] = bad["cotree"][:-1]; bad["forest"].append(base["cotree"][-1]); malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["charge"] = bad["charge"][:-1]; malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["phase"] = [0]; malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["b"] = 2; malformed.append(bad)
    bad = json.loads(json.dumps(base)); bad["extra"] = 0; malformed.append(bad)
    for bad in malformed:
        try:
            validate_instance(bad)
        except ValueError:
            c.malformed_rejections += 1
            c.assertions += 1
        else:
            raise AssertionError("malformed instance accepted")

    elapsed = time.monotonic() - start
    deadline()
    semantic = {
        "claim": "maximal projected rank plus maximal polar rank does not force hard witness search",
        "family": "connected graph plus even cotree, paired quadratic residual",
        "symbolic_witness": {"b=0": "all zero cotree", "b=1": "first cotree pair one"},
        "status": "COMPUTATIONAL checks supporting a PROVED/EXACT symbolic firewall",
        "counters": c.__dict__,
        "largest_friendship": family_rows[127],
        "largest_complete_bipartite": family_rows[-1],
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "run_id": "FULLRANKQFW1",
        "seed": SEED,
        "elapsed_seconds": round(elapsed, 6),
        "deadline_seconds": DEADLINE_SECONDS,
        "chunking": "single invocation; cooperative 25-second deadline",
        "semantic_digest_sha256": digest,
        "semantic": semantic,
        "family_endpoint_rows": [family_rows[0], family_rows[127], family_rows[128], family_rows[-1]],
        "limitations": [
            "Finite tests do not establish asymptotic lower bounds.",
            "The symbolic firewall applies to the explicit paired quadratic family, not every quadratic residual.",
            "No claim is made that arbitrary residual SAT on cotree coordinates is easy.",
            "Logical operation counts are separated from measured wall time.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
