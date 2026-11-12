"""Independent exhaustive structural audit of automatic separator discovery.

All undirected graphs on 0 through 5 labeled vertices are checked. The audit
validates decomposition semantics directly, without the factored SAT solver.
"""

from pathlib import Path
from itertools import combinations
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "separator_decomp.py"
sys.path.insert(0, str(SOURCE.parent))
from separator_decomp import discover_decomposition, _articulations


def components(graph, removed=()):
    remaining = set(graph) - set(removed)
    result = []
    while remaining:
        start = next(iter(remaining))
        remaining.remove(start)
        group, pending = {start}, [start]
        while pending:
            for neighbor in graph[pending.pop()] & remaining:
                remaining.remove(neighbor)
                group.add(neighbor)
                pending.append(neighbor)
        result.append(group)
    return result


def encode_graph(n, graph):
    # Tautologies retain isolated vertices without adding logical restrictions.
    clauses = [(v + 1, -(v + 1)) for v in range(n)]
    clauses += [(u + 1, v + 1) for u, v in combinations(range(n), 2) if v in graph[u]]
    # Include every clique of size >=3 as one affine factor, to test complete
    # factor coverage rather than only edge coverage. This changes no scope edge.
    equations = []
    for size in range(3, n + 1):
        for vertices in combinations(range(n), size):
            if all(v in graph[u] for u, v in combinations(vertices, 2)):
                equations.append((sum(1 << v for v in vertices), 0))
    return clauses, equations


def validate(n, graph, clauses, equations, decomposition, bound):
    bags = [set(bag) for bag in decomposition["bags"]]
    assert all(len(bag) == len(set(bag)) for bag in decomposition["bags"])
    assert set().union(*bags) == set(range(n))
    adjacency = [set() for _ in bags]
    parents = list(range(len(bags)))
    def root(x):
        while parents[x] != x:
            x = parents[x]
        return x
    seen_edges = set()
    for a, b in decomposition["edges"]:
        assert 0 <= a < len(bags) and 0 <= b < len(bags) and a != b
        pair = tuple(sorted((a, b)))
        assert pair not in seen_edges
        seen_edges.add(pair)
        aa, bb = root(a), root(b)
        assert aa != bb, "Cycle in output decomposition"
        parents[aa] = bb
        adjacency[a].add(b)
        adjacency[b].add(a)
        assert len(bags[a] & bags[b]) <= bound
    for variable in range(n):
        containing = {i for i, bag in enumerate(bags) if variable in bag}
        reached = {next(iter(containing))}
        pending = list(reached)
        while pending:
            for neighbor in adjacency[pending.pop()] & containing - reached:
                reached.add(neighbor)
                pending.append(neighbor)
        assert reached == containing, "Running intersection failed"
    for u, v in combinations(range(n), 2):
        if v in graph[u]:
            assert any({u, v} <= bag for bag in bags)
    for clause in clauses:
        scope = {abs(lit) - 1 for lit in clause}
        assert any(scope <= bag for bag in bags)
    for mask, _ in equations:
        scope = {v for v in range(n) if (mask >> v) & 1}
        assert any(scope <= bag for bag in bags), "An entire affine scope lacks a containing bag"


def main():
    started = time.perf_counter()
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    graphs = decompositions = articulation_checks = 0
    maximum_bags = maximum_splits = 0
    counts_by_n = {}
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        count = 0
        for mask in range(1 << len(pairs)):
            graph = {v: set() for v in range(n)}
            for index, (u, v) in enumerate(pairs):
                if (mask >> index) & 1:
                    graph[u].add(v)
                    graph[v].add(u)
            expected = {v for v in graph if len(components(graph, [v])) > len(components(graph))}
            counters = dict.fromkeys(("articulation_passes", "articulation_edge_scans", "articulation_vertex_visits"), 0)
            assert _articulations(graph, counters) == expected
            articulation_checks += 1
            clauses, equations = encode_graph(n, graph)
            for bound in (1, 2):
                result = discover_decomposition(n, clauses, equations, max_separator=bound, candidate_cap=None)
                validate(n, graph, clauses, equations, result, bound)
                maximum_bags = max(maximum_bags, len(result["bags"]))
                maximum_splits = max(maximum_splits, result["discovery_counters"]["split_nodes"])
                decompositions += 1
            graphs += 1
            count += 1
        counts_by_n[n] = count

    selected = [
        (6, [(i, i + 1) for i in range(5)], "path"),
        (6, [(i, (i + 1) % 6) for i in range(6)], "cycle"),
        (5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)], "two_triangles_one_anchor"),
        (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)], "disconnected_triangles"),
    ]
    configurations = [
        {"candidate_cap": 0}, {"candidate_cap": 1}, {"max_splits": 0},
        {"max_splits": 1}, {"candidate_cap": 0, "max_splits": 1},
        {"candidate_cap": 1, "max_splits": 1}, {"max_separator": 0},
    ]
    cap_controls = []
    for n, edges, name in selected:
        graph = {v: set() for v in range(n)}
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        clauses, equations = encode_graph(n, graph)
        for configuration in configurations:
            result = discover_decomposition(n, clauses, equations, **configuration)
            validate(n, graph, clauses, equations, result, configuration.get("max_separator", 2))
            counters = result["discovery_counters"]
            if "candidate_cap" in configuration:
                assert counters["separator_candidates"] <= configuration["candidate_cap"]
            if "max_splits" in configuration:
                assert counters["split_nodes"] <= configuration["max_splits"]
            if configuration.get("max_splits") == 0:
                assert len(result["bags"]) == 1 and set(result["bags"][0]) == set(range(n))
            cap_controls.append({"graph": name, "configuration": configuration,
                                 "bags": result["bags"], "edges": result["edges"],
                                 "split_nodes": counters["split_nodes"],
                                 "separator_candidates": counters["separator_candidates"],
                                 "budget_fallbacks": counters["budget_fallbacks"]})
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    report = {"status": "all assertions passed", "runtime_seconds": time.perf_counter() - started,
              "source_sha256": source_hash, "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "graphs_checked": graphs, "counts_by_vertex_number": counts_by_n,
              "articulation_checks": articulation_checks, "uncapped_decompositions_checked": decompositions,
              "maximum_observed_bags": maximum_bags, "maximum_observed_splits": maximum_splits,
              "cap_controls_checked": len(cap_controls), "cap_controls": cap_controls,
              "scope": "All output forests, running intersections, factor coverage, and adhesion bounds verified independently."}
    (HERE / "discovery_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "cap_controls"}, indent=2))


if __name__ == "__main__":
    main()
