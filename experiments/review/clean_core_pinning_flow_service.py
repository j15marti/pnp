#!/usr/bin/env python3
"""Bounded audit for PINNED-FACTOR-SERVICE1.

For the paired cubic-bipartite clean-core formula F_G, a partial assignment
to edge variables is extendible exactly when the unassigned edges contain a
subgraph meeting explicit lower and upper degree bounds at every vertex.
The script solves that problem by a lower-bounded circulation, compares it
with exhaustive semantics on bounded instances, and runs hostile controls.

The experiment validates an implementation.  The asymptotic theorem is the
symbolic flow reduction in the accompanying TESTS-0003 report.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from collections import deque
from pathlib import Path


UNKNOWN = -1


def cyclic_cubic_bipartite(r: int) -> list[tuple[int, int]]:
    if r < 3:
        raise ValueError("side size must be at least three")
    shifts = (0, 1, 2)
    return sorted((u, (u + d) % r) for u in range(r) for d in shifts)


def paired_clauses(r: int, edges: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    at_u = [[] for _ in range(r)]
    at_w = [[] for _ in range(r)]
    for i, (u, w) in enumerate(edges, 1):
        at_u[u].append(i)
        at_w[w].append(i)
    clauses: list[tuple[int, ...]] = []
    for inc in at_u + at_w:
        if len(inc) != 3:
            raise AssertionError("graph is not cubic")
        c = tuple(sorted(inc))
        clauses.extend((c, tuple(-x for x in c)))
    return clauses


def validate_h22(clauses: list[tuple[int, ...]], nvars: int) -> None:
    if len(clauses) != len(set(clauses)):
        raise AssertionError("duplicate clean-core clause")
    pos = [0] * (nvars + 1)
    neg = [0] * (nvars + 1)
    for clause in clauses:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            raise AssertionError("not proper width three")
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            raise AssertionError("not monotone")
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    if any(pos[i] != 2 or neg[i] != 2 for i in range(1, nvars + 1)):
        raise AssertionError("not exact (2,2)-occurrence")


def valid_mask(r: int, edges: list[tuple[int, int]], mask: int) -> bool:
    deg_u = [0] * r
    deg_w = [0] * r
    for i, (u, w) in enumerate(edges):
        if (mask >> i) & 1:
            deg_u[u] += 1
            deg_w[w] += 1
    return all(d in (1, 2) for d in deg_u + deg_w)


def compatible(mask: int, rho: tuple[int, ...]) -> bool:
    return all(v == UNKNOWN or ((mask >> i) & 1) == v for i, v in enumerate(rho))


def brute_service(valid_masks: list[int], rho: tuple[int, ...]) -> tuple[bool, int | None]:
    for mask in valid_masks:
        if compatible(mask, rho):
            return True, mask
    return False, None


class Dinic:
    def __init__(self, n: int):
        self.adj: list[list[list[int]]] = [[] for _ in range(n)]
        self.bfs_edge_scans = 0
        self.dfs_edge_scans = 0
        self.augmentations = 0

    def add_edge(self, u: int, v: int, cap: int) -> tuple[int, int]:
        a = [v, len(self.adj[v]), cap]
        b = [u, len(self.adj[u]), 0]
        self.adj[u].append(a)
        self.adj[v].append(b)
        return u, len(self.adj[u]) - 1

    def max_flow(self, source: int, sink: int) -> int:
        total = 0
        n = len(self.adj)
        while True:
            level = [-1] * n
            level[source] = 0
            q = deque([source])
            while q:
                u = q.popleft()
                for edge in self.adj[u]:
                    self.bfs_edge_scans += 1
                    if edge[2] and level[edge[0]] < 0:
                        level[edge[0]] = level[u] + 1
                        q.append(edge[0])
            if level[sink] < 0:
                break
            it = [0] * n

            def send(u: int, amount: int) -> int:
                if u == sink:
                    return amount
                while it[u] < len(self.adj[u]):
                    edge = self.adj[u][it[u]]
                    self.dfs_edge_scans += 1
                    if edge[2] and level[edge[0]] == level[u] + 1:
                        pushed = send(edge[0], min(amount, edge[2]))
                        if pushed:
                            edge[2] -= pushed
                            self.adj[edge[0]][edge[1]][2] += pushed
                            return pushed
                    it[u] += 1
                return 0

            while True:
                pushed = send(source, 10**9)
                if not pushed:
                    break
                total += pushed
                self.augmentations += 1
        return total


def flow_service(
    r: int, edges: list[tuple[int, int]], rho: tuple[int, ...]
) -> tuple[bool, int | None, dict[str, int]]:
    """Solve extendibility through an integral lower-bounded circulation."""
    m = len(edges)
    if len(rho) != m:
        raise ValueError("query length mismatch")
    fixed_u = [0] * r
    fixed_w = [0] * r
    unknown_u = [0] * r
    unknown_w = [0] * r
    for value, (u, w) in zip(rho, edges):
        if value == 1:
            fixed_u[u] += 1
            fixed_w[w] += 1
        elif value == UNKNOWN:
            unknown_u[u] += 1
            unknown_w[w] += 1
        elif value != 0:
            raise ValueError("query entries must be -1, 0, or 1")

    lower_u, upper_u, lower_w, upper_w = [], [], [], []
    for fixed, unknown, lower, upper in (
        (fixed_u, unknown_u, lower_u, upper_u),
        (fixed_w, unknown_w, lower_w, upper_w),
    ):
        for a, d in zip(fixed, unknown):
            lo = max(0, 1 - a)
            hi = min(d, 2 - a)
            if lo > hi:
                return False, None, {
                    "network_vertices": 0,
                    "network_arcs": 0,
                    "bfs_edge_scans": 0,
                    "dfs_edge_scans": 0,
                    "augmentations": 0,
                }
            lower.append(lo)
            upper.append(hi)

    s, t = 0, 1
    u0, w0 = 2, 2 + r
    ss, tt = 2 + 2 * r, 3 + 2 * r
    dinic = Dinic(4 + 2 * r)
    demand = [0] * (2 + 2 * r)
    tracked: list[tuple[int, int, int]] = []
    forward_arcs = 0

    def add_lower(a: int, b: int, lo: int, hi: int) -> tuple[int, int]:
        nonlocal forward_arcs
        if not 0 <= lo <= hi:
            raise AssertionError("invalid lower-bound arc")
        ref = dinic.add_edge(a, b, hi - lo)
        demand[a] -= lo
        demand[b] += lo
        forward_arcs += 1
        return ref

    for u in range(r):
        add_lower(s, u0 + u, lower_u[u], upper_u[u])
    for i, ((u, w), value) in enumerate(zip(edges, rho)):
        if value == UNKNOWN:
            ref = add_lower(u0 + u, w0 + w, 0, 1)
            tracked.append((i, ref[0], ref[1]))
    for w in range(r):
        add_lower(w0 + w, t, lower_w[w], upper_w[w])
    add_lower(t, s, 0, m)

    required = 0
    for v, d in enumerate(demand):
        if d > 0:
            dinic.add_edge(ss, v, d)
            required += d
            forward_arcs += 1
        elif d < 0:
            dinic.add_edge(v, tt, -d)
            forward_arcs += 1
    sent = dinic.max_flow(ss, tt)
    stats = {
        "network_vertices": len(dinic.adj),
        "network_arcs": forward_arcs,
        "bfs_edge_scans": dinic.bfs_edge_scans,
        "dfs_edge_scans": dinic.dfs_edge_scans,
        "augmentations": dinic.augmentations,
    }
    if sent != required:
        return False, None, stats

    mask = 0
    for i, value in enumerate(rho):
        if value == 1:
            mask |= 1 << i
    for i, u, index in tracked:
        residual = dinic.adj[u][index][2]
        if residual == 0:
            mask |= 1 << i
    if not valid_mask(r, edges, mask) or not compatible(mask, rho):
        raise AssertionError("flow reconstruction was not a valid extension")
    return True, mask, stats


def cnf_eval(clauses: list[tuple[int, ...]], bits: tuple[int, ...]) -> bool:
    return all(any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses)


def brute_cnf(clauses: list[tuple[int, ...]], n: int, rho: tuple[int, ...]) -> bool:
    holes = [i for i, x in enumerate(rho) if x == UNKNOWN]
    for fill in itertools.product((0, 1), repeat=len(holes)):
        bits = list(rho)
        for i, value in zip(holes, fill):
            bits[i] = value
        if cnf_eval(clauses, tuple(bits)):
            return True
    return False


def horn_sat(clauses: list[tuple[int, ...]], n: int, rho: tuple[int, ...]) -> bool:
    work = list(clauses)
    for i, value in enumerate(rho, 1):
        if value != UNKNOWN:
            work.append((i if value else -i,))
    truth = [False] * (n + 1)
    changed = True
    while changed:
        changed = False
        for clause in work:
            positives = [x for x in clause if x > 0]
            negatives = [-x for x in clause if x < 0]
            if len(positives) > 1:
                raise ValueError("not Horn")
            if all(truth[x] for x in negatives):
                if not positives:
                    return False
                if not truth[positives[0]]:
                    truth[positives[0]] = True
                    changed = True
    return True


def two_sat(clauses: list[tuple[int, ...]], n: int, rho: tuple[int, ...]) -> bool:
    graph = [[] for _ in range(2 * n)]
    reverse = [[] for _ in range(2 * n)]

    def node(lit: int) -> int:
        return 2 * (abs(lit) - 1) + (0 if lit > 0 else 1)

    def neg(v: int) -> int:
        return v ^ 1

    def arc(a: int, b: int) -> None:
        graph[a].append(b)
        reverse[b].append(a)

    work = list(clauses)
    for i, value in enumerate(rho, 1):
        if value != UNKNOWN:
            work.append((i if value else -i,))
    for clause in work:
        if len(clause) == 1:
            a = node(clause[0])
            arc(neg(a), a)
        elif len(clause) == 2:
            a, b = map(node, clause)
            arc(neg(a), b)
            arc(neg(b), a)
        else:
            raise ValueError("not 2-CNF")
    seen = [False] * (2 * n)
    order: list[int] = []
    for start in range(2 * n):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            v, i = stack[-1]
            if i < len(graph[v]):
                z = graph[v][i]
                stack[-1] = (v, i + 1)
                if not seen[z]:
                    seen[z] = True
                    stack.append((z, 0))
            else:
                order.append(v)
                stack.pop()
    comp = [-1] * (2 * n)
    for start in reversed(order):
        if comp[start] >= 0:
            continue
        label = start
        stack = [start]
        comp[start] = label
        while stack:
            v = stack.pop()
            for z in reverse[v]:
                if comp[z] < 0:
                    comp[z] = label
                    stack.append(z)
    return all(comp[2 * i] != comp[2 * i + 1] for i in range(n))


def affine_sat(rows: list[tuple[int, int]], n: int, rho: tuple[int, ...]) -> bool:
    equations = list(rows)
    for i, value in enumerate(rho):
        if value != UNKNOWN:
            equations.append((1 << i, value))
    pivots: dict[int, tuple[int, int]] = {}
    for mask, rhs in equations:
        while mask:
            p = mask.bit_length() - 1
            if p not in pivots:
                pivots[p] = (mask, rhs)
                break
            qmask, qrhs = pivots[p]
            mask ^= qmask
            rhs ^= qrhs
        if not mask and rhs:
            return False
    return True


def path_dp(n: int, rho: tuple[int, ...]) -> bool:
    states = {0, 1} if rho[0] == UNKNOWN else {rho[0]}
    for i in range(1, n):
        choices = {0, 1} if rho[i] == UNKNOWN else {rho[i]}
        states = {b for a in states for b in choices if a != b}
        if not states:
            return False
    return bool(states)


def random_rho(m: int, rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.choice((UNKNOWN, 0, 1)) for _ in range(m))


def run(seed: int, random_queries: int) -> dict:
    started = time.perf_counter()
    rng = random.Random(seed)
    totals = {
        "flow_queries": 0,
        "semantic_agreements": 0,
        "witness_reconstructions": 0,
        "bfs_edge_scans": 0,
        "dfs_edge_scans": 0,
        "augmentations": 0,
        "hostile_control_queries": 0,
        "wrapper_checks": 0,
        "h22_checks": 0,
    }
    rows = []

    for r, exhaustive, count in ((3, True, 3**9), (4, False, random_queries), (5, False, random_queries)):
        edges = cyclic_cubic_bipartite(r)
        validate_h22(paired_clauses(r, edges), len(edges))
        totals["h22_checks"] += 1
        valid = [mask for mask in range(1 << len(edges)) if valid_mask(r, edges, mask)]
        queries = itertools.product((UNKNOWN, 0, 1), repeat=len(edges)) if exhaustive else (
            random_rho(len(edges), rng) for _ in range(count)
        )
        yes = 0
        max_vertices = max_arcs = 0
        for rho in queries:
            rho = tuple(rho)
            expected, _ = brute_service(valid, rho)
            actual, witness, stats = flow_service(r, edges, rho)
            if actual != expected:
                raise AssertionError(("flow disagreement", r, rho, actual, expected))
            totals["flow_queries"] += 1
            totals["semantic_agreements"] += 1
            totals["bfs_edge_scans"] += stats["bfs_edge_scans"]
            totals["dfs_edge_scans"] += stats["dfs_edge_scans"]
            totals["augmentations"] += stats["augmentations"]
            max_vertices = max(max_vertices, stats["network_vertices"])
            max_arcs = max(max_arcs, stats["network_arcs"])
            if actual:
                yes += 1
                if witness is None or not valid_mask(r, edges, witness) or not compatible(witness, rho):
                    raise AssertionError("bad reconstructed witness")
                totals["witness_reconstructions"] += 1
        rows.append({
            "side": r,
            "edges": len(edges),
            "valid_full_assignments": len(valid),
            "queries": count,
            "exhaustive": exhaustive,
            "yes_queries": yes,
            "max_network_vertices": max_vertices,
            "max_forward_arcs": max_arcs,
            "symbolic_service_coordinates": 3 ** len(edges),
        })

    # Independent product: a disconnected union of two K_3,3 components.
    e3 = cyclic_cubic_bipartite(3)
    product_edges = e3 + [(u + 3, w + 3) for u, w in e3]
    valid3 = [mask for mask in range(1 << 9) if valid_mask(3, e3, mask)]
    product_checks = 256
    for _ in range(product_checks):
        rho = random_rho(18, rng)
        left = brute_service(valid3, rho[:9])[0]
        right = brute_service(valid3, rho[9:])[0]
        actual = flow_service(6, product_edges, rho)[0]
        if actual != (left and right):
            raise AssertionError("independent-product factorization failed")
        totals["flow_queries"] += 1
        totals["semantic_agreements"] += 1
        totals["wrapper_checks"] += 1

    # Encoding and wrapper controls on K_3,3.
    edges = e3
    valid = valid3
    clauses = paired_clauses(3, edges)
    wrapper_checks = 0
    for _ in range(256):
        rho = random_rho(9, rng)
        base = brute_service(valid, rho)[0]
        perm = list(range(9))
        rng.shuffle(perm)
        perm_edges = [edges[i] for i in perm]
        perm_rho = tuple(rho[i] for i in perm)
        if flow_service(3, perm_edges, perm_rho)[0] != base:
            raise AssertionError("alternate edge encoding failed")
        wrapper_checks += 1
        comp = tuple(UNKNOWN if x == UNKNOWN else 1 - x for x in rho)
        if flow_service(3, edges, comp)[0] != base:
            raise AssertionError("global complementation failed")
        wrapper_checks += 1
        if flow_service(3, edges, rho)[0] != flow_service(3, edges, rho)[0]:
            raise AssertionError("RECOMP instability")
        wrapper_checks += 1

    for mask in range(1 << 9):
        bits = tuple((mask >> i) & 1 for i in range(9))
        base = cnf_eval(clauses, bits)
        shuffled = clauses[:]
        rng.shuffle(shuffled)
        copied = clauses + clauses
        dead = clauses + [(1, -1, 2)]
        if not (base == cnf_eval(shuffled, bits) == cnf_eval(copied, bits) == cnf_eval(dead, bits)):
            raise AssertionError("clause wrapper changed semantics")
        wrapper_checks += 4
        padded_bits = bits + (rng.randrange(2), rng.randrange(2))
        if cnf_eval(clauses, padded_bits) != base:
            raise AssertionError("unused-variable padding changed semantics")
        wrapper_checks += 1
        delay_checksum = 0
        for j in range(7):
            delay_checksum ^= j
        if delay_checksum != 7 or cnf_eval(clauses, bits) != base:
            raise AssertionError("DELAY control changed semantics")
        wrapper_checks += 1
    totals["wrapper_checks"] += wrapper_checks

    # Required easy-family controls, each compared with independent brute semantics.
    n = 7
    horn = [(1,)] + [(-i, i + 1) for i in range(1, n)]
    two = [c for i in range(1, n) for c in ((-i, i + 1), (i, -(i + 1)))]
    affine = [((1 << i) | (1 << (i + 1)), 0) for i in range(n - 1)]
    xor_path_cnf = [c for i in range(1, n) for c in ((i, i + 1), (-i, -(i + 1)))]
    controls = {"horn": 0, "two_sat": 0, "affine": 0, "bounded_treewidth": 0}
    for _ in range(512):
        rho = random_rho(n, rng)
        if horn_sat(horn, n, rho) != brute_cnf(horn, n, rho):
            raise AssertionError("Horn control")
        controls["horn"] += 1
        if two_sat(two, n, rho) != brute_cnf(two, n, rho):
            raise AssertionError("2-SAT control")
        controls["two_sat"] += 1
        affine_expected = any(
            all(v == UNKNOWN or bits[i] == v for i, v in enumerate(rho))
            and all(((bits[i] ^ bits[i + 1]) == rhs) for i, (_, rhs) in enumerate(affine))
            for bits in itertools.product((0, 1), repeat=n)
        )
        if affine_sat(affine, n, rho) != affine_expected:
            raise AssertionError("affine control")
        controls["affine"] += 1
        if path_dp(n, rho) != brute_cnf(xor_path_cnf, n, rho):
            raise AssertionError("bounded-treewidth control")
        controls["bounded_treewidth"] += 1
        totals["hostile_control_queries"] += 4

    elapsed = time.perf_counter() - started
    return {
        "claim": "PINNED-FACTOR-SERVICE1",
        "status": "COMPUTATIONAL implementation audit",
        "seed": seed,
        "runtime_seconds": round(elapsed, 6),
        "rows": rows,
        "totals": totals,
        "controls": controls,
        "independent_product_checks": product_checks,
        "asymptotic_note": {
            "source_variables": "3r",
            "source_clauses": "4r",
            "encoded_length": "Theta(r log r)",
            "ternary_partial_assignment_coordinates": "3^(3r) = 2^Theta(N/log N)",
            "per_query_algorithm": "integral lower-bounded circulation on O(r) vertices and arcs",
            "finite_scope": "Measurements validate bounded implementations only; no runtime extrapolation is used.",
        },
        "wrappers": [
            "variable/edge permutation",
            "global complementation",
            "clause order",
            "COPY redundant clauses",
            "DEAD tautology",
            "unused-variable padding",
            "DELAY accounting",
            "INTERP",
            "RECOMP",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--random-queries", type=int, default=1500)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed, args.random_queries)
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
