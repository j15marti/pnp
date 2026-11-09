#!/usr/bin/env python3
"""Independent source-support oracle for LSPV-1/538, distinct SIDE_TABLE calculus."""
from itertools import combinations, product
import json


def graph_edges(name):
    if name == "K4":
        return list(combinations(range(4), 2))
    if name == "prism3":
        return [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
    if name == "cube":
        return [(v, v ^ (1 << bit)) for v in range(8) for bit in range(3) if v < (v ^ (1 << bit))]
    raise ValueError(name)


def make_source(name, odd):
    edges = graph_edges(name)
    h = max(max(edge) for edge in edges) + 1
    source = []
    for vertex in range(h):
        incident = [i for i, edge in enumerate(edges) if vertex in edge]
        assert len(incident) == 3
        for bits in product((0, 1), repeat=3):
            if sum(bits) % 2 != (int(odd and vertex == 0)):
                source.append((incident, bits))
    return h, len(edges), source


def falsified(c, assignment):
    indices, bits = c
    return all((assignment >> i) & 1 == b for i, b in zip(indices, bits))


def check_graph(name):
    h, n, odd = make_source(name, True)
    _, _, even = make_source(name, False)
    sole = [None] * len(odd)
    cover = set()
    sat_even = 0
    for a in range(1 << n):
        violated = [j for j, c in enumerate(odd) if falsified(c, a)]
        assert violated, "odd formula must be UNSAT"
        cover.add(violated[0])
        if len(violated) == 1:
            sole[violated[0]] = a
        if not any(falsified(c, a) for c in even):
            sat_even += 1
    assert len(cover) == len(odd)
    assert all(x is not None for x in sole)
    assert sat_even == (1 << (n - h + 1))
    return {"graph": name, "h": h, "n": n, "m": len(odd),
            "odd_satisfying_assignments": 0,
            "even_satisfying_assignments": sat_even,
            "essential_source_witnesses": len(sole),
            "table_used_source_count": len(cover),
            "syntactic_parents": 1,
            "effective_source_fanin": len(odd)}


if __name__ == "__main__":
    result = {"status": "PASS", "method": "independent Python enumerate per-clause exclusive violation",
              "scope": "distinct SIDE_TABLE hypothetical calculus", "data": [check_graph(x) for x in ("K4", "prism3", "cube")],
              "historical_checker_executed": False}
    print(json.dumps(result, indent=2))
