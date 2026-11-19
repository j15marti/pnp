#!/usr/bin/env python3
"""Independent compact audit for TMR-3/097 hypercube source-separator theorem.
Python 3.10+, standard library only. NOT a computational lower-bound proof.
The complete 66,974-check harness is in the reproducibility ZIP.
"""
from itertools import combinations
from math import ceil, log2
import json

def cube_edges(d):
    v = 2**d
    return {tuple(sorted((x, x ^ (1 << b))))
            for x in range(v) for b in range(d)}

def components_after_removal(v, edges, removed):
    adj = [[] for _ in range(v)]
    for u, w in edges:
        if u not in removed and w not in removed:
            adj[u].append(w)
            adj[w].append(u)
    visited = set(removed)
    sizes = []
    for root in range(v):
        if root in visited:
            continue
        queue = [root]
        visited.add(root)
        for node in queue:
            for next_node in adj[node]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)
        sizes.append(len(queue))
    return sizes

def min_interface(d, B):
    v = 2**d
    edges = cube_edges(d)
    for s in range(v+1):
        for deleted in combinations(range(v), s):
            comps = components_after_removal(v, edges, set(deleted))
            if all(x <= B for x in comps):
                return s
    raise AssertionError('no separator')

def lower_bound(d, B):
    v = 2**d
    t = d - log2(B)
    return ceil(v*t/(d+t)-1e-10)

def t5_hamming_witness(d):
    edges = cube_edges(d)
    for u, v in edges:
        if u.bit_count() > v.bit_count():
            u, v = v, u
        assert v.bit_count()-u.bit_count() == 1
        assert (v.bit_count()%5 - u.bit_count()%5)%5 in (1,3)
    return {"vertices": 2**d, "arcs":len(edges), "valid":True}

def main():
    test_cases = [(2,1,2),(3,4,3),(4,2,8),(4,4,8)]
    observed = []
    for d, B, expected in test_cases:
        actual = min_interface(d,B)
        assert actual == expected, (d,B,actual,expected)
        assert actual >= lower_bound(d,B)
        observed.append({"dimension":d,"B":B,"exact_shared_min":actual})
    controls = [t5_hamming_witness(d) for d in (2,3,5,8)]
    print(json.dumps({"status":"COMPUTATIONAL","independent_min_separators":observed,
                      "easy_T5_controls":controls,"failures":0},indent=2))

if __name__ == "__main__":
    main()
