"""Degree-based reduction for simple ternary shifted inequalities. Python 3.10+.

Run python degree_reduction.py to write degree_results.json. An edge (u,v,d)
forbids x[v] = x[u]+d (mod 3). Vertex IDs are 0,...,n-1, without pins.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import random


def blocks(adj, allowed):
    """Iterative Tarjan edge blocks, grouped by connected component."""
    seen, low, parent = {}, {}, {}
    for root in sorted(allowed):
        if root in seen:
            continue
        component, edge_stack, parts = {root}, [], []
        seen[root] = low[root] = len(seen)
        parent[root] = None
        stack = [(root, iter(adj[root] & allowed))]
        while stack:
            u, neighbors = stack[-1]
            v = next(neighbors, None)
            if v is not None:
                if v not in seen:
                    component.add(v)
                    parent[v] = u
                    seen[v] = low[v] = len(seen)
                    edge_stack.append((u, v))
                    stack.append((v, iter(adj[v] & allowed)))
                elif v != parent[u] and seen[v] < seen[u]:
                    edge_stack.append((u, v))
                    low[u] = min(low[u], seen[v])
                continue
            stack.pop()
            p = parent[u]
            if p is None:
                continue
            low[p] = min(low[p], low[u])
            if low[u] >= seen[p]:
                piece = []
                while True:
                    edge = edge_stack.pop()
                    piece.append(edge)
                    if edge == (p, u):
                        break
                parts.append(piece)
        yield component, parts


def clique_or_cycle(edges):
    degree = Counter(x for e in edges for x in e)
    return (2 * len(edges) == len(degree) * (len(degree) - 1)
            or all(d == 2 for d in degree.values()))


def structure(n, edges):
    adj = [set() for _ in range(n)]
    for u, v, d in edges:
        if not (0 <= u < n and 0 <= v < n and u != v and d in range(3)):
            raise ValueError('invalid simple shifted edge')
        if v in adj[u]:
            raise ValueError('parallel constraints must be normalized first')
        adj[u].add(v)
        adj[v].add(u)
    high = {v for v, row in enumerate(adj) if len(row) >= 4}
    kept, reasons = set(high), Counter()
    for comp, parts in blocks(adj, set(range(n)) - high):
        if any(len(adj[v]) < 3 for v in comp):
            reasons['degree_slack'] += len(comp)
        elif any(not clique_or_cycle(part) for part in parts):
            reasons['degree_coloring_theorem'] += len(comp)
        else:
            kept.update(comp)
    # The retained low graph consists of partial 2-trees and isolated K4s.
    # Removing a degree <=2 vertex with fill is a minor in the low graph.
    live = {v: adj[v] & kept for v in kept}
    low = kept - high
    order, width = [], 0
    while live:
        pool = low if low else live.keys()
        v = min(pool, key=lambda u: (len(live[u] & low), u)) if low else min(pool)
        neighbors = live.pop(v)
        width = max(width, len(neighbors))
        for u in neighbors:
            live[u].remove(v)
            live[u].update(neighbors - {u})
        low.discard(v)
        order.append(v)
    assert width <= max(3, len(high) + 2)
    return high, kept, order, width, dict(reasons)


def k4_balanced(edges):
    """Forbidden offsets are differences of vertex potentials exactly when balanced."""
    pot = {0: 0}
    for u, v, d in edges:
        if u == 0:
            pot[v] = d
    return all((pot[v] - pot[u]) % 3 == d for u, v, d in edges)


def assignment_oracle(n):
    assignments = list(product(range(3), repeat=n))
    all_bits = (1 << len(assignments)) - 1
    masks = {(u, v, d): sum(1 << i for i, a in enumerate(assignments)
                            if (a[v] - a[u]) % 3 != d)
             for u, v in combinations(range(n), 2) for d in range(3)}
    return assignments, all_bits, masks


def restricted_projections(assignments, bits, boundary):
    answer = set()
    while bits:
        bit = bits & -bits
        a = assignments[bit.bit_length() - 1]
        answer.add(tuple(a[v] for v in boundary))
        bits -= bit
    return answer


def verify(prefix, n, edge_lists, oracle):
    assignments, all_bits, masks = oracle
    total = unsat = dropped = 0
    for edges in edge_lists:
        high, kept, _, _, _ = structure(n, edges)
        boundary = sorted(high)
        full = reduced = all_bits
        for e in edges:
            full &= masks[e]
            if e[0] in kept and e[1] in kept:
                reduced &= masks[e]
        assert restricted_projections(assignments, full, boundary) == restricted_projections(
            assignments, reduced, boundary)
        if n == 4 and len(edges) == 6:
            assert (full == 0) == k4_balanced(edges)
        dropped += len(kept) < n
        unsat += full == 0
        total += 1
    return {'series': prefix, 'instances': total, 'unsat': unsat,
            'sat': total - unsat, 'reduced_vertex_count': dropped}


def run():
    rng = random.Random(20261104)
    p4 = list(combinations(range(4), 2))
    all4 = ([(u, v, d) for (u, v), d in zip(p4, ds) if d != 3]
            for ds in product(range(4), repeat=6))
    cases = [verify('all simple shifted graphs on four labeled vertices', 4,
                    all4, assignment_oracle(4))]
    p5 = list(combinations(range(5), 2))
    sample5 = ([(u, v, rng.randrange(3)) for i, (u, v) in enumerate(p5) if s >> i & 1]
               for s in range(1 << len(p5)) for _ in range(4))
    cases.append(verify('four seeded label draws on each of 1024 five-vertex shapes', 5,
                        sample5, assignment_oracle(5)))
    p7 = list(combinations(range(7), 2))
    sample7 = ([(u, v, rng.randrange(3)) for u, v in p7 if rng.random() < density]
               for density in (0.3, 0.55, 0.8) for _ in range(100))
    cases.append(verify('seeded seven-vertex mixed-density graphs', 7,
                        sample7, assignment_oracle(7)))
    # Compose K4 on {0,1,2,3} with a prism whose edge 4--5 is subdivided.
    # Vertex 0 is the only high vertex; its color can always extend to the prism.
    result = []
    for twisted in (False, True):
        edges = [(u,v,int(twisted and (u,v)==(1,2))) for u,v in p4]
        prism = [(0,10),(4,10),(5,10),(4,6),(5,6),(7,8),(7,9),(8,9),
                 (4,7),(5,8),(6,9)]
        edges += [(u,v,(u+2*v)%3) for u,v in prism]
        high, kept, order, width, why = structure(11, edges)
        assert high == {0} and kept == {0,1,2,3} and why == {'degree_coloring_theorem': 7}
        sat = {a[0] for a in product(range(3), repeat=11)
               if all((a[v]-a[u])%3 != d for u,v,d in edges)}
        assert sat == (set(range(3)) if twisted else set())
        result.append(dict(twisted=twisted,high=sorted(high),retained=sorted(kept),
                           width=width,discarded=why,extendible_boundary=sorted(sat),
                           graph=edges,order=order))
    data = dict(projection_checks=cases,balanced_k4={'offset_labelings':729,'unsat':27},
                attached_prism=result)
    Path(__file__).with_name('degree_results.json').write_text(json.dumps(data, indent=2)+'\n')
    print([(x['instances'],x['unsat']) for x in cases])


if __name__ == '__main__':
    run()
