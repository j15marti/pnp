#!/usr/bin/env python3
"""Strict-C migration and selector adversary for the 3-lift Mycielski graph.

This script does not import Q witnesses. It reconstructs tail colorings and
strict-C private heads, checks every source clause, and runs the supplied
orientation/capacity/distance filters on the resulting C source.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
import time
import tracemalloc
from collections import Counter, deque
from pathlib import Path

WIN = ({1, 3}, {2, 4}, {0, 3}, {1, 4}, {0, 2})
SEED = 202611190056


def R(a: int, b: int) -> bool:
    return b in WIN[a]


def C(a: int, b: int, c: int) -> bool:
    return (R(a, b) and R(b, c) and R(c, a)) or (
        R(a, c) and R(c, b) and R(b, a)
    )


def Q(a: int, b: int, c: int) -> bool:
    return R(a, b) != R(a, c)


def edge(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def graph(level: int) -> tuple[int, list[tuple[int, int]]]:
    if level == 0:
        return 5, sorted({edge(i, (i + 1) % 5) for i in range(5)})
    n, old = graph(level - 1)
    out = set(old)
    for a, b in old:
        out.add(edge(a, n + b))
        out.add(edge(b, n + a))
    for i in range(n):
        out.add((n + i, 2 * n))
    return 2 * n + 1, sorted(out)


def deletion_coloring(level: int, omitted: tuple[int, int]) -> list[int]:
    omitted = edge(*omitted)
    n, edges = graph(level)
    assert omitted in edges
    if level == 0:
        adjacency = [[] for _ in range(n)]
        for a, b in edges:
            if (a, b) != omitted:
                adjacency[a].append(b)
                adjacency[b].append(a)
        colors = [-1] * n
        colors[0] = 0
        stack = [0]
        while stack:
            a = stack.pop()
            for b in adjacency[a]:
                if colors[b] < 0:
                    colors[b] = 1 - colors[a]
                    stack.append(b)
        return colors
    old_n, old_edges = graph(level - 1)
    extra = level + 1
    a, b = omitted
    if b < old_n:
        colors = deletion_coloring(level - 1, (a, b))
        repeated = colors[a]
        return colors + [extra if x == repeated else x for x in colors] + [repeated]
    if b == 2 * old_n:
        i = a - old_n
        incident = next(e for e in old_edges if i in e)
        colors = deletion_coloring(level - 1, incident)
        originals, shadows = list(colors), list(colors)
        originals[i] = shadows[i] = extra
        return originals + shadows + [extra]
    j, i = a, b - old_n
    colors = deletion_coloring(level - 1, (i, j))
    originals = list(colors)
    originals[i] = extra
    return originals + colors + [extra]


def girth(n: int, edges: list[tuple[int, int]]) -> int | None:
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    best = n + 1
    for root in range(n):
        distance = [-1] * n
        parent = [-1] * n
        distance[root] = 0
        queue = deque([root])
        while queue:
            a = queue.popleft()
            for b in adjacency[a]:
                if distance[b] < 0:
                    distance[b] = distance[a] + 1
                    parent[b] = a
                    queue.append(b)
                elif parent[a] != b and parent[b] != a:
                    best = min(best, distance[a] + distance[b] + 1)
    return None if best == n + 1 else best


def strict_head(a: int, b: int) -> int:
    """Return the first h completing the directed triangle C(h,a,b)."""
    for h in range(5):
        if C(h, a, b):
            return h
    raise AssertionError("distinct tails must have a strict-C private head")


def load_filters(path: Path):
    spec = importlib.util.spec_from_file_location("strict_filters", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> dict:
    started = time.perf_counter()
    counters = Counter()
    n, edges = graph(3)
    assert n == 47 and len(edges) == 236
    clauses = [(n + i, a, b) for i, (a, b) in enumerate(edges)]

    # Direct local relation firewall.
    relation = {
        "C": sum(C(*row) for row in itertools.product(range(5), repeat=3)),
        "Q": sum(Q(*row) for row in itertools.product(range(5), repeat=3)),
        "P": sum(
            R(row[0], row[1]) and R(row[0], row[2])
            for row in itertools.product(range(5), repeat=3)
        ),
    }
    assert relation == {"C": 30, "Q": 60, "P": 20}

    witnesses = []
    selector_histogram = Counter()
    for omitted, omitted_edge in enumerate(edges):
        colors = deletion_coloring(3, omitted_edge)
        counters["deletion_tail_constructions"] += 1
        assert len(colors) == n and max(colors) < 5
        bad = []
        for i, (a, b) in enumerate(edges):
            counters["tail_edge_checks"] += 1
            if colors[a] == colors[b]:
                bad.append(i)
        assert bad == [omitted]
        selector_histogram[omitted] += 1

        assignment = list(colors)
        for a, b in edges:
            counters["head_reconstructions"] += 1
            assignment.append(strict_head(colors[a], colors[b]) if colors[a] != colors[b] else 0)
        failed = []
        for i, (h, a, b) in enumerate(clauses):
            counters["strict_C_clause_checks"] += 1
            if not C(assignment[h], assignment[a], assignment[b]):
                failed.append(i)
        assert failed == [omitted]
        witnesses.append(
            {
                "omitted_clause": omitted,
                "omitted_edge": omitted_edge,
                "unique_refutable_block": omitted,
                "assignment": assignment,
            }
        )

    # The user-supplied full filters are run on the entire 283-variable source.
    package = Path("strict_inputs/package/t5_strict_research")
    filters = load_filters(package / "analyze_parity_obstructions.py")
    capacity = filters.orientation_capacity_filter(n + len(edges), "C", clauses)
    distance = filters.triangle_distance_filter(n + len(edges), clauses)
    assert capacity == (True, None) and distance == (True, None)

    # Revalidate the finite catalogue rather than repeating its million-set grid.
    supplied = json.loads((package / "results/parity_obstruction_results.json").read_text())
    catalogue = []
    for result in supplied["results"]:
        if result["relation"] != "C":
            continue
        for orbit in result["minimal_residual_orbits"]:
            deletion_checks = 0
            for item in orbit["single_clause_deletion_witnesses"]:
                assignment = item["assignment"]
                deleted = item["deleted_clause_index"]
                for i, clause in enumerate(orbit["clauses"]):
                    counters["catalogue_C_clause_checks"] += 1
                    assert C(*(assignment[v] for v in clause)) == (i != deleted)
                    deletion_checks += 1
            catalogue.append(
                {
                    "variable_count": result["variable_count"],
                    "clauses": orbit["clauses"],
                    "orbit_size": orbit["orbit_size"],
                    "deletion_C_checks": deletion_checks,
                    "capacity_filter": filters.orientation_capacity_filter(
                        result["variable_count"], "C", orbit["clauses"]
                    ),
                    "distance_filter": filters.triangle_distance_filter(
                        result["variable_count"], orbit["clauses"]
                    ),
                }
            )
    assert len(catalogue) == 5

    # The full formula is UNSAT by the standard Mycielski theorem: chi=6.
    # Every deletion witness above is direct and does not rely on this theorem.
    # Selector consequence: no row-independent proper subset of blocks covers
    # these rows, since row e has unique rejecting block e.
    positions = list(range(len(edges)))
    fixed_order_costs = [positions.index(w["unique_refutable_block"]) + 1 for w in witnesses]
    assert sorted(fixed_order_costs) == list(range(1, len(edges) + 1))

    old_q = Path("evidence/unpacked/t5_exact_one/redteam/mycielski_fixture.json")
    q_data = json.loads(old_q.read_text())
    assert q_data["source_graph_vertices"] == n
    assert [tuple(x) for x in q_data["clauses"]] == clauses
    # Compare only tail colorings; Q heads are not reused.
    tail_matches = 0
    for new, old in zip(witnesses, q_data["deletion_witnesses"]):
        if new["assignment"][:n] == old["assignment"][:n]:
            tail_matches += 1
    assert tail_matches == len(edges)

    return {
        "status": "PASS",
        "seed": SEED,
        "relation_counts": relation,
        "source": {
            "construction": "three Mycielski lifts of C5; one private strict-C head per edge",
            "tail_vertices": n,
            "source_edges": len(edges),
            "total_variables": n + len(edges),
            "strict_C_clauses": len(clauses),
            "source_graph_girth": girth(n, edges),
            "constraint_incidence_girth": 2 * girth(n, edges),
            "chromatic_number_certificate": "Mycielski raises chi(C5)=3 by one at each of three lifts",
            "unsat": True,
            "clause_minimal": True,
        },
        "clauses": clauses,
        "full_filters": {"orientation_capacity": capacity, "pentagon_distance": distance},
        "minimal_catalogue_recheck": catalogue,
        "selector_adversary": {
            "rows": len(witnesses),
            "distinct_unique_refutable_blocks": len(selector_histogram),
            "fixed_source_order_min_checks": min(fixed_order_costs),
            "fixed_source_order_max_checks": max(fixed_order_costs),
            "fixed_source_order_mean_checks": sum(fixed_order_costs) / len(fixed_order_costs),
            "scope": "Rejects row-independent fixed-block subsets/orders; not a lower bound on source-aware selectors.",
        },
        "Q_migration_firewall": {
            "historical_Q_tail_colorings_matched": tail_matches,
            "historical_Q_heads_reused": False,
            "strict_C_heads_reconstructed": len(edges) * len(edges),
        },
        "counters": dict(counters),
        "deletion_witnesses": witnesses,
        "wall_seconds_before_serialization": time.perf_counter() - started,
    }


if __name__ == "__main__":
    tracemalloc.start()
    result = main()
    result["python_tracemalloc_peak_bytes"] = tracemalloc.get_traced_memory()[1]
    result["peak_scope"] = (
        "Whole producer through result construction, including imported filters and all retained witnesses; "
        "excludes JSON serialization and interpreter/import baseline. Not a machine-independent space bound."
    )
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
