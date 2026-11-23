"""Run from repository root with Python 3; uses two existing Construction checkers."""
from itertools import product
import json

from dynamic_construction_join_palette_20261122 import encode, recover
from dynamic_construction_triangle_bundle_20261122 import expand

GAIN = [None, (0,0,0,0,0), (1,1,0,0,0), (2,0,1,0,0),
        (2,2,0,0,0), (1,2,1,0,0), (0,1,1,0,0), (1,0,0,0,0)]


def mask(gains):
    result = 0
    for d, u, v in product(range(3), repeat=3):
        differences = (d-u, d-v, -u, -v, u-v)
        if all(x % 3 != g for x, g in zip(differences, gains)):
            result |= 1 << d
    return result


def graph(left, right):
    m = len(left)
    edges = {}
    for i, pair in enumerate(zip(left, right)):
        t = 1 + 9*i
        labels = []
        for wanted in pair:
            labels.extend((wanted, wanted) if wanted else (1, 2))
        for j, label in enumerate(labels):
            u = t + 1 + 2*j
            v = u + 1
            endpoints = [(0,u), (0,v), (t,u), (t,v), (u,v)]
            edges.update(zip(endpoints, GAIN[label]))
        if i:
            w = 9*m + i
            edges[t-9,w] = edges[t,w] = 0
    return 10*m, edges


def adjacent(q, edges):
    adj = [[] for _ in range(q)]
    for (u, v), gain in edges.items():
        adj[u].append((v, gain))
        adj[v].append((u, -gain))
    return adj


def connected_after_deletion(adj, removed):
    stack = [int(removed == 0)]
    seen = set()
    while stack:
        u = stack.pop()
        if u != removed and u not in seen:
            seen.add(u)
            stack.extend(v for v, _ in adj[u])
    return len(seen) + 1 == len(adj)


def color_decision(adj):
    colors = {0: 0}
    def visit():
        if len(colors) == len(adj):
            return True
        choices = []
        for u, neighbors in enumerate(adj):
            if u not in colors:
                forbidden = {(colors[v]+g) % 3 for v,g in neighbors if v in colors}
                choices.append((3-len(forbidden), u, sorted(set(range(3))-forbidden)))
        _, u, allowed = min(choices)
        for color in allowed:
            colors[u] = color
            if visit():
                return True
            del colors[u]
        return False
    return visit()


def main():
    masks = [mask(x) for x in GAIN[1:]]
    assert masks == list(range(1, 8))
    sizes = {}
    for m in (1, 2, 3):
        vectors = list(product(range(8), repeat=m))
        signatures = {bytes(all(a & b for a,b in zip(left,right)) for right in vectors)
                      for left in vectors}
        sizes[m] = len(signatures)
        assert sizes[m] == 7**m + 1
    cases = [((a,), (b,)) for a,b in product(range(8), repeat=2)]
    cases += [((a,7), (b,1)) for a,b in product(range(8), repeat=2)]
    verdicts = [0, 0]
    for left, right in cases:
        m = len(left)
        q, edges = graph(left, right)
        adj = adjacent(q, edges)
        decision = color_decision(adj)
        assert decision == all(a & b for a,b in zip(left,right))
        verdicts[int(decision)] += 1
        p = {uv: tuple((a+g) % 3 for a in range(3)) for uv,g in edges.items()}
        h, expanded = expand(q,p)
        n, rows = encode(h, expanded)
        assert (q,len(edges),n,len(rows)) == (10*m,22*m-2,528*m-18,408*m-18)
        assert recover(n,list(reversed(rows))) == (h,expanded)
    for m in range(1,6):
        q, edges = graph([7]*m, [7]*m)
        adj = adjacent(q,edges)
        assert all(connected_after_deletion(adj,v) for v in range(q))
    print(json.dumps(dict(diamond_masks=masks, distinct_rows=sizes,
                          graph_source_cases=len(cases), unsat=verdicts[0], sat=verdicts[1],
                          vertex_deletion_sizes=[1,2,3,4,5]), indent=2))


if __name__ == "__main__":
    main()
