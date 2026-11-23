"""Run from the repository with python experiments/dynamic_discovery_planar_girth_20261123.py."""
import json
from itertools import combinations
from random import Random

from dynamic_construction_join_palette_20261122 import encode, recover
from dynamic_construction_triangle_bundle_20261122 import PERMS, expand, parity


def chain(length):
    edges = set()
    previous = None
    next_id = 0
    for _ in range(length):
        ids = list(previous or ())
        ids.extend(range(next_id, next_id + 20 - len(ids)))
        next_id = max(ids) + 1
        rings = (range(5), range(5, 15), range(15, 20))
        local = [(ring[i], ring[(i + 1) % len(ring)]) for ring in rings for i in range(len(ring))]
        for i in range(5):
            local.extend([(i, 5 + 2*i), (15+i, 6 + 2*i)])
        edges.update(tuple(sorted((ids[a], ids[b]))) for a, b in local)
        previous = ids[15:17]
    return next_id, sorted(edges)


def neighbors(q, edges):
    adj = [set() for _ in range(q)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def check_structure(adj):
    vertices = set(range(len(adj)))
    for u, v in combinations(vertices, 2):
        common = adj[u] & adj[v]
        assert len(common) <= 1 and (v not in adj[u] or not common)
    for removed in vertices:
        start = min(vertices - {removed})
        seen, stack = {start}, [start]
        while stack:
            new = adj[stack.pop()] - seen - {removed}
            seen.update(new)
            stack.extend(new)
        assert seen == vertices - {removed}


def balanced(q, match):
    adj = [[] for _ in range(q)]
    for (u, v), p in match.items():
        s = parity(p)
        adj[u].append((v, s))
        adj[v].append((u, s))
    signs = {0: 0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v, s in adj[u]:
            expected = signs[u] ^ s
            if v in signs:
                if signs[v] != expected:
                    return False
            else:
                signs[v] = expected
                stack.append(v)
    assert len(signs) == q
    return True


def readback(q, match):
    h, edges = expand(q, match)
    n, rows = encode(h, edges)
    observed = recover(n, [row[::-1] for row in rows[::-1]])
    assert observed == (h, edges)
    groups = {}
    for x, y in observed[1]:
        u, a = divmod(x, 3)
        v, b = divmod(y, 3)
        if u != v:
            groups.setdefault((u,v), []).append((a,b))
    recovered = {edge: tuple(b for a,b in sorted(pairs)) for edge,pairs in groups.items()}
    assert recovered == match
    return n, len(rows), recovered


def main():
    rng = Random(324)
    results = []
    for length in (1, 2, 4, 8):
        q, edges = chain(length)
        adj = neighbors(q, edges)
        check_structure(adj)
        hubs = sum(len(row) > 3 for row in adj)
        assert (q, len(edges), hubs) == (18*length+2, 29*length+1, 2*(length-1))
        assert min(map(len, adj)) == 3
        for _ in range(8):
            witness = [rng.choice(PERMS) for _ in range(q)]
            match = {}
            for u, v in edges:
                legal = [p for p in PERMS if all(witness[u][i] != witness[v][p[i]] for i in range(3))]
                assert len(legal) == 2
                match[u,v] = rng.choice(legal)
            n, m, recovered = readback(q, match)
            assert balanced(q, recovered)
            assert all(witness[u][i] != witness[v][p[i]] for (u,v),p in recovered.items() for i in range(3))
            edge = edges[0]
            a,b,c = match[edge]
            match[edge] = (b,a,c)
            _, _, mutant = readback(q, match)
            assert not balanced(q, mutant)
        bits = n + 2 + 2*((m+1).bit_length()-1) + 3*m*n.bit_length()
        results.append(dict(copies=length, vertices=q, edges=len(edges), hubs=hubs,
                            n=n, m=m, N=bits, sat=8, unsat=8))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
