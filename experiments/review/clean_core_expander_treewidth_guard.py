#!/usr/bin/env python3
"""Finite regression for CLEANCORE-EXPANDER-GUARD1.

The symbolic theorem is proved in the accompanying report.  This script only
checks bounded instances: the cubic-bipartite-to-CNF map, H_{2,2} incidence,
the perfect-matching witness, the line-graph primal graph, the regular-line-
graph Laplacian spectrum identity, exact small treewidth, and wrapper controls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from functools import lru_cache
from pathlib import Path

import numpy as np


def cyclic_cubic_bipartite(r: int) -> list[tuple[int, int]]:
    if r < 3:
        raise ValueError("r must be at least 3")
    return sorted((u, (u + shift) % r) for u in range(r) for shift in (0, 1, 2))


def random_cubic_bipartite(r: int, rng: random.Random) -> list[tuple[int, int]]:
    """Union of three edge-disjoint random perfect matchings."""
    base = list(range(r))
    for _ in range(10_000):
        perms: list[list[int]] = []
        used: set[tuple[int, int]] = set()
        ok = True
        for _colour in range(3):
            p = base[:]
            rng.shuffle(p)
            if any((u, p[u]) in used for u in base):
                ok = False
                break
            perms.append(p)
            used.update((u, p[u]) for u in base)
        if ok and connected_bipartite(r, sorted(used)):
            return sorted(used)
    raise RuntimeError("failed to sample a simple connected cubic bipartite graph")


def connected_bipartite(r: int, edges: list[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(2 * r)]
    for u, w in edges:
        adj[u].append(r + w)
        adj[r + w].append(u)
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for z in adj[v]:
            if z not in seen:
                seen.add(z)
                stack.append(z)
    return len(seen) == 2 * r


def perfect_matching(r: int, edges: list[tuple[int, int]]) -> set[tuple[int, int]]:
    adj = [[] for _ in range(r)]
    for u, w in edges:
        adj[u].append(w)
    mate = [-1] * r

    def augment(u: int, seen: set[int]) -> bool:
        for w in adj[u]:
            if w in seen:
                continue
            seen.add(w)
            if mate[w] == -1 or augment(mate[w], seen):
                mate[w] = u
                return True
        return False

    for u in range(r):
        if not augment(u, set()):
            raise AssertionError("regular bipartite graph lacked a perfect matching")
    return {(u, w) for w, u in enumerate(mate)}


def formula_from_graph(r: int, edges: list[tuple[int, int]]):
    edge_to_var = {e: i + 1 for i, e in enumerate(edges)}
    at_u = [[] for _ in range(r)]
    at_w = [[] for _ in range(r)]
    for e, var in edge_to_var.items():
        u, w = e
        at_u[u].append(var)
        at_w[w].append(var)
    clauses: list[tuple[int, int, int]] = []
    for incidence in at_u + at_w:
        inc = tuple(sorted(incidence))
        if len(inc) != 3:
            raise AssertionError("graph is not cubic")
        clauses.append(inc)
        clauses.append(tuple(-x for x in inc))
    return sorted(clauses), edge_to_var


def eval_formula(clauses, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)


def validate_h22(clauses, nvars: int) -> None:
    if len(clauses) != len(set(clauses)):
        raise AssertionError("duplicate clause")
    pos = [0] * (nvars + 1)
    neg = [0] * (nvars + 1)
    for clause in clauses:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            raise AssertionError("not proper width three")
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            raise AssertionError("clause is not monotone")
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    if any(pos[v] != 2 or neg[v] != 2 for v in range(1, nvars + 1)):
        raise AssertionError("not exactly (2,2)-occurrence")


def primal_edges(clauses) -> set[tuple[int, int]]:
    ans: set[tuple[int, int]] = set()
    for clause in clauses:
        vs = sorted(abs(x) - 1 for x in clause)
        for i in range(3):
            for j in range(i + 1, 3):
                ans.add((vs[i], vs[j]))
    return ans


def line_edges(edges: list[tuple[int, int]]) -> set[tuple[int, int]]:
    ans: set[tuple[int, int]] = set()
    for i, e in enumerate(edges):
        for j in range(i + 1, len(edges)):
            f = edges[j]
            if e[0] == f[0] or e[1] == f[1]:
                ans.add((i, j))
    return ans


def laplacian_spectrum(n: int, edges: set[tuple[int, int]]) -> np.ndarray:
    mat = np.zeros((n, n), dtype=float)
    for u, v in edges:
        mat[u, u] += 1.0
        mat[v, v] += 1.0
        mat[u, v] -= 1.0
        mat[v, u] -= 1.0
    return np.linalg.eigvalsh(mat)


def bipartite_edges_as_graph(r: int, edges: list[tuple[int, int]]) -> set[tuple[int, int]]:
    return {(u, r + w) for u, w in edges}


def exact_treewidth(n: int, edges: set[tuple[int, int]]) -> int:
    """Subset DP using the order-independent torso after eliminating a set."""
    base = [0] * n
    for u, v in edges:
        base[u] |= 1 << v
        base[v] |= 1 << u
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def degree_after(mask: int, v: int) -> int:
        # Vertices reachable from v through eliminated internal vertices.
        reached = 1 << v
        frontier = base[v] & mask
        seen_elim = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            if seen_elim & bit:
                continue
            seen_elim |= bit
            z = bit.bit_length() - 1
            reached |= base[z] & ~mask
            frontier |= base[z] & mask & ~seen_elim
        return (reached & (full ^ mask) & ~(1 << v)).bit_count()

    inf = n + 1
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        here = dp[mask]
        if here == inf:
            continue
        remaining = full ^ mask
        bits = remaining
        while bits:
            bit = bits & -bits
            bits ^= bit
            v = bit.bit_length() - 1
            nxt = mask | bit
            width = max(here, degree_after(mask, v))
            if width < dp[nxt]:
                dp[nxt] = width
    return dp[full]


def semantic_wrapper_checks(clauses, assignment, rng: random.Random) -> int:
    checks = 0
    shuffled = list(clauses)
    rng.shuffle(shuffled)
    assert eval_formula(shuffled, assignment)
    checks += 1

    variables = sorted(assignment)
    permuted = variables[:]
    rng.shuffle(permuted)
    rename = dict(zip(variables, permuted))
    renamed_clauses = [tuple((1 if lit > 0 else -1) * rename[abs(lit)] for lit in c) for c in clauses]
    renamed_assignment = {rename[v]: val for v, val in assignment.items()}
    assert eval_formula(renamed_clauses, renamed_assignment)
    checks += 1

    complemented = [tuple(-lit for lit in c) for c in clauses]
    comp_assignment = {v: not val for v, val in assignment.items()}
    assert eval_formula(complemented, comp_assignment)
    assert set(complemented) == set(clauses)
    checks += 2

    copied = list(clauses) + list(clauses)
    assert eval_formula(copied, assignment)
    checks += 1
    return checks


def run(max_exact_side: int, sample_sides: list[int], seed: int) -> dict:
    started = time.perf_counter()
    rng = random.Random(seed)
    rows = []
    totals = {
        "instances": 0,
        "h22_checks": 0,
        "matching_witness_checks": 0,
        "primal_line_graph_checks": 0,
        "spectral_identity_checks": 0,
        "exact_treewidth_instances": 0,
        "wrapper_checks": 0,
    }
    cases = [(r, "cyclic", cyclic_cubic_bipartite(r)) for r in range(3, max(sample_sides) + 1)]
    cases += [(r, "sampled", random_cubic_bipartite(r, rng)) for r in sample_sides]
    for r, kind, edges in cases:
        clauses, edge_to_var = formula_from_graph(r, edges)
        validate_h22(clauses, len(edges))
        totals["h22_checks"] += 1

        matching = perfect_matching(r, edges)
        assignment = {var: e in matching for e, var in edge_to_var.items()}
        assert len(matching) == r and eval_formula(clauses, assignment)
        totals["matching_witness_checks"] += 1

        p_edges = primal_edges(clauses)
        l_edges = line_edges(edges)
        assert p_edges == l_edges
        totals["primal_line_graph_checks"] += 1

        g_spec = laplacian_spectrum(2 * r, bipartite_edges_as_graph(r, edges))
        l_spec = laplacian_spectrum(3 * r, l_edges)
        gap_g = float(g_spec[1])
        gap_l = float(l_spec[1])
        if not math.isclose(gap_g, gap_l, rel_tol=1e-8, abs_tol=1e-8):
            raise AssertionError((r, kind, gap_g, gap_l))
        totals["spectral_identity_checks"] += 1

        tw = None
        if r <= max_exact_side:
            tw = exact_treewidth(3 * r, l_edges)
            spectral_floor = (3 * r * gap_l / (4.0 + gap_l)) - 1.0
            if tw + 1e-8 < spectral_floor:
                raise AssertionError((r, kind, tw, spectral_floor))
            totals["exact_treewidth_instances"] += 1

        wrappers = semantic_wrapper_checks(clauses, assignment, rng)
        totals["wrapper_checks"] += wrappers
        totals["instances"] += 1
        rows.append({
            "side_size": r,
            "kind": kind,
            "graph_vertices": 2 * r,
            "formula_variables": 3 * r,
            "formula_clauses": 4 * r,
            "algebraic_connectivity_graph": gap_g,
            "algebraic_connectivity_primal": gap_l,
            "exact_primal_treewidth": tw,
            "perfect_matching_size": len(matching),
        })

    # Independent-product control: conjunction preserves easy witnesses while
    # treewidth is the maximum, not the sum, across components.
    # Keep the exact subset-DP product check bounded (18 primal vertices).
    left = cyclic_cubic_bipartite(3)
    right = cyclic_cubic_bipartite(3)
    left_line = line_edges(left)
    right_line = {(u + len(left), v + len(left)) for u, v in line_edges(right)}
    product_tw = exact_treewidth(len(left) + len(right), left_line | right_line)
    component_tw = max(exact_treewidth(len(left), left_line), exact_treewidth(len(right), line_edges(right)))
    assert product_tw == component_tw

    return {
        "claim_id": "CLEANCORE-EXPANDER-GUARD1",
        "status": "COMPUTATIONAL finite audit supporting a separate PROVED/EXACT theorem",
        "seed": seed,
        "parameters": {"max_exact_side": max_exact_side, "sample_sides": sample_sides},
        "totals": totals,
        "independent_product": {"exact_treewidth": product_tw, "component_max": component_tw},
        "rows": rows,
        "limitations": [
            "Finite cyclic and sampled graphs do not prove an expander family.",
            "The asymptotic family uses the cited existence of cubic bipartite expanders and a symbolic spectral/treewidth proof.",
            "High primal treewidth is not a lower bound on arbitrary SAT computation.",
            "The tested family is an easy satisfiable subclass, not all of the NP-complete clean core.",
        ],
        "runtime_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exact-side", type=int, default=5)
    parser.add_argument("--sample-sides", default="6,8,10")
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument(
        "--output",
        default="results/raw/review/2026-10-11_clean_core_expander_treewidth_guard.json",
    )
    args = parser.parse_args()
    sample_sides = [int(x) for x in args.sample_sides.split(",") if x]
    result = run(args.max_exact_side, sample_sides, args.seed)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["code_sha256"] = source_hash
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
