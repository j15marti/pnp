#!/usr/bin/env python3
"""LSPV-2 327 compact source-authenticated signed-cubic circuit bound checker.
Run: python lspv2_327_compact.py [canonical_source.json ...]
Requires networkx. Full independent tests and circuit construction in ZIP.
"""
import json
import sys
from collections import Counter, defaultdict
import networkx as nx

Y6 = {"n": 6, "clauses": [
[1,2,3],[1,4,5],[2,4,6],[3,5,6],
[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]}
F9 = {"n": 9, "clauses": [
[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],
[-1,-2,-9],[-5,-7,-9]]}

def validate(obj):
    if type(obj) is not dict or set(obj) != {"n", "clauses"}:
        raise ValueError("invalid canonical source fields")
    n, clauses = obj["n"], obj["clauses"]
    if type(n) is not int or n < 3 or type(clauses) is not list:
        raise ValueError("invalid size or clauses")
    if len(clauses) * 3 != 4 * n:
        raise ValueError("wrong canonical clause count")
    seen = set()
    occ = Counter()
    for c in clauses:
        if not isinstance(c, list) or len(c) != 3 or any(
           type(x) is not int or x == 0 or abs(x) > n for x in c):
            raise ValueError("malformed triple")
        if len(set(map(abs, c))) != 3 or not(all(x > 0 for x in c) or all(x < 0 for x in c)):
            raise ValueError("nonproper or mixed-polarity clause")
        key = tuple(sorted(c))
        if key in seen:
            raise ValueError("duplicate original clause")
        seen.add(key)
        occ.update(c)
    if any(occ[i] != 2 or occ[-i] != 2 for i in range(1, n + 1)):
        raise ValueError("not exactly two of each sign for every variable")
    return n, clauses

def signed_cubic(clauses, n):
    outputs = {}
    for sign in (1, -1):
        nodes = [j for j, c in enumerate(clauses) if c[0] * sign > 0]
        h = nx.MultiGraph()
        h.add_nodes_from(nodes)
        for var in range(1, n + 1):
            ends = [j for j in nodes if sign * var in clauses[j]]
            assert len(ends) == 2 and ends[0] != ends[1]
            h.add_edge(*ends, key=var)
        assert len(nodes) == 2 * n // 3 and h.number_of_edges() == n
        assert all(deg == 3 for _, deg in h.degree())
        outputs[sign] = h
    return outputs

def weighted_source_matching(clauses):
    g = nx.Graph()
    g.add_nodes_from(range(len(clauses)))
    for i, a in enumerate(clauses):
        sa = set(map(abs, a))
        for j in range(i + 1, len(clauses)):
            b = clauses[j]
            sb = set(map(abs, b))
            shared = len(sa & sb)
            same = (a[0] > 0) == (b[0] > 0)
            weight = shared if same else (2 if sa == sb else 0)
            if weight:
                g.add_edge(i, j, weight=weight)
    edges = nx.max_weight_matching(g, maxcardinality=False, weight="weight")
    w = sum(g[u][v]["weight"] for u, v in edges)
    return w, sorted(tuple(sorted((u + 1, v + 1))) for u, v in edges)

def greedy_stars(clauses, n):
    incidence = defaultdict(set)
    for j, c in enumerate(clauses):
        for literal in c:
            incidence[abs(literal)].add(j)
    used = set()
    chosen = []
    for x in range(1, n + 1):
        group = incidence[x]
        assert len(group) == 4
        if not (group & used):
            chosen.append(x)
            used.update(group)
    return chosen

def run(name, obj):
    n, c = validate(obj)
    signed = signed_cubic(c, n)
    W, matching = weighted_source_matching(c)
    stars = greedy_stars(c, n)
    gates = 4 * n - 1 - W
    bound = 4 * n - 1 - 2 * ((n + 3) // 4)
    assert W >= 2 * ((n + 3) // 4)
    assert len(stars) >= (n + 8) // 9
    assert gates <= bound
    assert gates <= (4 * n - 1 - 2 * len(stars))
    return {"name": name, "n": n, "m": len(c), "signed_cubic_edges_each": n,
            "max_matching_weight": W, "matching_source_clause_ids": matching,
            "restricted_gates": gates, "shannon_upper_bound": bound,
            "disjoint_star_pivots": stars, "star_gates": 4*n-1-2*len(stars),
            "bridge_counts": {str(s): len(list(nx.bridges(nx.Graph(h)))) for s,h in signed.items()}}

if __name__ == "__main__":
    sources = [(p, json.load(open(p))) for p in sys.argv[1:]]
    if not sources:
        sources = [("Y6", Y6), ("F9", F9)]
    for name, obj in sources:
        print(json.dumps(run(name, obj), sort_keys=True))
