#!/usr/bin/env python3
"""Solve mixed additive constraints over Z/3Z using only the standard library.

python shift_solver.py solve instance.json       # use "-" to read stdin
python shift_solver.py test --output results.json

An instance has {"vertices": 3, "edges": [[0, 1, "fixed", 2], [1, 2, "forbid", 0]]}.
Each edge [u, v, kind, c] constrains x[v]-x[u] modulo 3 to equal or differ
from c. Vertex IDs range from 0 to vertices-1. Parallel edges and loops are allowed.
"""

import argparse
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys


# Bit d in a mask allows difference d. Precompute shifts and edge reversals.
SHIFT = [
    [sum(1 << ((d + k) % 3) for d in range(3) if mask & (1 << d))
     for k in range(3)]
    for mask in range(8)
]
NEG = [sum(1 << (-d % 3) for d in range(3) if mask & (1 << d))
       for mask in range(8)]


class Potentials:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.offset = [0] * n  # x[i]-x[parent[i]]

    def find(self, i):
        p = self.parent[i]
        if p != i:
            root, up = self.find(p)
            self.offset[i] = (self.offset[i] + up) % 3
            self.parent[i] = root
        return self.parent[i], self.offset[i]

    def join(self, u, v, d):
        a, p = self.find(u)
        b, q = self.find(v)
        shift = (d + p - q) % 3  # x[b]-x[a]
        if a == b:
            return shift == 0
        if self.size[a] < self.size[b]:
            a, b, shift = b, a, -shift % 3
        self.parent[b] = a
        self.offset[b] = shift
        self.size[a] += self.size[b]
        return True


def contract(n, constraints, stats):
    uf = Potentials(n)
    while True:
        stats["contraction_passes"] += 1
        for u, v, mask in constraints:
            if mask in (1, 2, 4) and not uf.join(u, v, mask.bit_length() - 1):
                return None
        pairs = {}
        for u, v, mask in constraints:
            a, p = uf.find(u)
            b, q = uf.find(v)
            mask = SHIFT[mask][(p - q) % 3]
            if a == b:
                if not mask & 1:
                    return None
                continue
            if a > b:
                a, b, mask = b, a, NEG[mask]
            pair = (a, b)
            pairs[pair] = pairs.get(pair, 7) & mask
            if pairs[pair] == 0:
                return None
        if not any(mask in (1, 2, 4) for mask in pairs.values()):
            return uf, pairs
        constraints = [(u, v, mask) for (u, v), mask in pairs.items()]


def component_dp(vertices, graph, stats):
    # Input-ID order on the contracted graph. Each component can be translated
    # so its first vertex has state 0. Retain only assigned vertices with a
    # neighbor still to come. Histories reconstruct one satisfying assignment.
    ordered = sorted(vertices)
    last = {u: max(graph[u], default=u) for u in ordered}
    frontier = ()
    states = {(): None}
    histories = []
    for index, v in enumerate(ordered):
        positions = {u: i for i, u in enumerate(frontier)}
        checks = [(positions[u], graph[u][v]) for u in graph[v] if u < v]
        keep = [(u, i) for u, i in positions.items() if last[u] > v]
        keep_v = last[v] > v
        next_frontier = tuple(u for u, _ in keep) + ((v,) if keep_v else ())
        stats["peak_frontier_vertices"] = max(stats["peak_frontier_vertices"],
                                             len(next_frontier))
        following = {}
        for state in states:
            base = tuple(state[i] for _, i in keep)
            for x in ((0,) if index == 0 else range(3)):
                stats["candidate_extensions"] += 1
                if all(mask & (1 << ((x - state[i]) % 3)) for i, mask in checks):
                    key = base + ((x,) if keep_v else ())
                    if key not in following:
                        following[key] = (state, x)
        stats["retained_states_sum"] += len(following)
        stats["peak_frontier_states"] = max(stats["peak_frontier_states"], len(following))
        if not following:
            return None
        histories.append(following)
        states, frontier = following, next_frontier
    state = ()
    answer = {}
    for v, layer in zip(reversed(ordered), reversed(histories)):
        state, answer[v] = layer[state]
    return answer


def solve(n, edges):
    if type(n) is not int or n < 0:
        raise ValueError("vertices must be a nonnegative integer")
    constraints = []
    for u, v, kind, c in edges:
        if any(type(i) is not int or not 0 <= i < n for i in (u, v)):
            raise ValueError("invalid vertex ID")
        if type(c) is not int or kind not in ("fixed", "forbid"):
            raise ValueError("expected a fixed or forbid edge with an integer offset")
        bit = 1 << (c % 3)
        constraints.append((u, v, bit if kind == "fixed" else 7 ^ bit))
    stats = dict(vertices=n, edges=len(constraints), contraction_passes=0,
                 contracted_vertices=None, contracted_pairs=None, processed_components=0,
                 peak_frontier_vertices=0, peak_frontier_states=0,
                 retained_states_sum=0, candidate_extensions=0)
    no = {"satisfiable": False, "assignment": None, "stats": stats}
    reduced = contract(n, constraints, stats)
    if reduced is None:
        return no
    uf, pairs = reduced
    roots = [uf.find(v) for v in range(n)]
    graph = {u: {} for u, _ in roots}
    for (u, v), mask in pairs.items():
        graph[u][v] = mask
        graph[v][u] = NEG[mask]
    stats.update(contracted_vertices=len(graph), contracted_pairs=len(pairs))
    seen = set()
    coloring = {}
    for root in graph:
        if root in seen:
            continue
        stats["processed_components"] += 1
        vertices, stack = [], [root]
        seen.add(root)
        while stack:
            u = stack.pop()
            vertices.append(u)
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        values = component_dp(vertices, graph, stats)
        if values is None:
            return no
        coloring.update(values)
    assignment = [(coloring[u] + p) % 3 for u, p in roots]
    return {"satisfiable": True, "assignment": assignment, "stats": stats}


def check(assignment, edges):
    return all((((assignment[v] - assignment[u] - c) % 3 == 0) == (kind == "fixed"))
               for u, v, kind, c in edges)


def verify_case(n, edges, expected):
    result = solve(n, edges)
    if result["satisfiable"] != expected or (expected and not check(result["assignment"], edges)):
        raise AssertionError((n, edges, expected, result))
    return result["stats"]


def chain_instance(count, close_k4):
    # Each logical vertex has two copies connected by a fixed shift. Residual
    # edges join vertices at distance 1 or 2, requiring different logical colors.
    # Requiring the last four to form a K4 makes the instance unsatisfiable.
    offsets = [(v * 7 + 1) % 3 for v in range(count)]
    edges = [(2*v, 2*v+1, "fixed", offsets[v]) for v in range(count)]
    pairs = [(v, v+d) for v in range(count) for d in (1, 2) if v+d < count]
    if close_k4:
        pairs.append((count-4, count-1))
    rng = random.Random(9284)
    for u, v in pairs:
        a, b = rng.randrange(2), rng.randrange(2)
        edges.append((2*u+a, 2*v+b, "forbid", (b*offsets[v]-a*offsets[u]) % 3))
    return edges


def selftest():
    pairs = list(combinations(range(4), 2))
    labels = [None] + [(k, c) for k in ("fixed", "forbid") for c in range(3)]
    # The independent oracle tabulates all 3^4 assignments without symmetry fixing.
    assignments = list(product(range(3), repeat=4))
    universe = (1 << len(assignments)) - 1
    truth = []
    choices = []
    for u, v in pairs:
        edges = [None] + [(u, v, *label) for label in labels[1:]]
        choices.append(edges)
        truth.append([universe] + [sum(1 << i for i, x in enumerate(assignments)
                                       if check(x, [edge])) for edge in edges[1:]])
    sat = total = 0
    for instance in product(range(7), repeat=len(pairs)):
        solutions = universe
        edges = []
        for j, label in enumerate(instance):
            solutions &= truth[j][label]
            if label:
                edges.append(choices[j][label])
        verify_case(4, edges, bool(solutions))
        sat += bool(solutions)
        total += 1
    rng = random.Random(4683)
    random_sat = 0
    for _ in range(500):
        n = rng.randint(1, 6)
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice(("fixed", "forbid")),
                  rng.randint(-7, 7)) for _ in range(rng.randrange(18))]
        expected = any(check(x, edges) for x in product(range(3), repeat=n))
        verify_case(n, edges, expected)
        random_sat += expected
    verify_case(0, [], True)
    # Parallel exclusions force a shift, which creates a second forced shift
    # only after its endpoints have been contracted.
    cascade = [(0, 1, "forbid", 0), (1, 0, "forbid", 2),
               (0, 2, "forbid", 0), (1, 2, "forbid", 0)]
    cascade_stats = verify_case(3, cascade, True)
    if cascade_stats["contraction_passes"] != 3:
        raise AssertionError(cascade_stats)
    examples = {}
    for size in (20, 200, 2000):
        for close in (False, True):
            edges = chain_instance(size, close)
            stats = verify_case(2*size, edges, not close)
            examples[f"triangle_chain_{size}" + ("_K4" if close else "")] = {
                "satisfiable": not close, **stats}
    # A tree of paths 0--middle--leaf has 2^k independent middle colors
    # after the root color is fixed. Processing each leaf immediately can
    # forget its middle color before the next middle vertex is assigned.
    order_examples = {}
    for k in (4, 8, 12):
        for grouped in (False, True):
            edges = []
            for i in range(k):
                mid, leaf = (i+1, i+k+1) if grouped else (2*i+1, 2*i+2)
                edges.extend([(0, mid, "forbid", 0), (mid, leaf, "forbid", 0)])
            stats = verify_case(2*k+1, edges, True)
            expected_peak = 2**k if grouped else 2
            if stats["peak_frontier_states"] != expected_peak:
                raise AssertionError(stats)
            order_examples[f"{k}_arms_" + ("grouped" if grouped else "interleaved")] = stats
    return {
        "exhaustive_four_vertices": dict(instances=total, satisfiable=sat,
                                         unsatisfiable=total-sat, disagreements=0,
                                         assignments_per_oracle=81),
        "seeded_multigraphs": dict(instances=500, satisfiable=random_sat,
                                   unsatisfiable=500-random_sat, disagreements=0, seed=4683),
        "empty_graph": "passed", "forced_shift_cascade": cascade_stats,
        "structured_examples": examples, "tree_order_comparison": order_examples,
        "metric_notes": {"retained_states_sum": "Distinct states per completed DP layer, summed, excluding initial empty tuples.",
                         "candidate_extensions": "Candidate choices checked before edge filtering or state deduplication.",
                         "peak_frontier_states": "Maximum distinct retained states in a completed layer."}}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subs = parser.add_subparsers(dest="command", required=True)
    sp = subs.add_parser("solve", help="solve a JSON instance")
    sp.add_argument("instance")
    tp = subs.add_parser("test", help="run exhaustive, randomized and structured tests")
    tp.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "solve":
        data = json.loads(sys.stdin.read() if args.instance == "-" else Path(args.instance).read_text())
        result = solve(data["vertices"], data["edges"])
    else:
        result = selftest()
    report = json.dumps(result, indent=2)
    if args.command == "test" and args.output:
        args.output.write_text(report + "\n")
    else:
        print(report)


if __name__ == "__main__":
    main()
