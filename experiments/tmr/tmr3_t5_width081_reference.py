#!/usr/bin/env python3
"""TMR-3/081: exact source-conditioned width T5 counter (standard library)."""
from itertools import product

D = {1, 3}
Q = range(5)

def beat(a, b):
    return (b-a) % 5 in D

def construct(n, edges):
    edges = sorted(set(edges))
    if n < 0 or any(u < 0 or v < 0 or u >= n or v >= n for u, v in edges):
        raise ValueError('invalid source')
    source = set(edges)
    if any(u == v or (v, u) in source for u, v in edges):
        return None
    inc = [[] for _ in range(n)]
    out = [[] for _ in range(n)]
    for u, v in edges:
        inc[v].append(u)
        out[u].append(v)
    sinks = {v for v in range(n) if not out[v] and len(inc[v]) <= 3}
    hubs = set(range(n)) - sinks
    fac, base = [], 1
    for v in sorted(sinks):
        scope = tuple(sorted(inc[v]))
        if not scope:
            base *= 5
            continue
        table = {x: sum(all(beat(a, z) for a in x) for z in Q)
                 for x in product(Q, repeat=len(scope))}
        fac.append((scope, table))
    for u, v in edges:
        if v in sinks:
            continue
        scope = tuple(sorted((u, v)))
        table = {x: int(beat(dict(zip(scope, x))[u], dict(zip(scope, x))[v]))
                 for x in product(Q, repeat=2)}
        fac.append((scope, table))
    return hubs, fac, base

def adjacency(verts, factors):
    adj = {v: set() for v in verts}
    for scope, _ in factors:
        for v in scope:
            adj[v].update(set(scope)-{v})
    return adj

def components(adj):
    left = set(adj)
    ans = []
    while left:
        comp, stack = set(), [min(left)]
        while stack:
            u = stack.pop()
            if u not in left:
                continue
            left.remove(u)
            comp.add(u)
            stack.extend(adj[u] & left)
        ans.append(comp)
    return ans

def minfill(adj):
    g = {u: set(vs) for u, vs in adj.items()}
    order, width = [], 0
    while g:
        def key(v):
            ns = sorted(g[v])
            fill = sum(w not in g[u] for j, u in enumerate(ns) for w in ns[j+1:])
            return fill, len(ns), v
        v = min(g, key=key)
        ns = list(g[v])
        width = max(width, len(ns))
        for u in ns:
            g[u].update(set(ns)-{u})
            g[u].remove(v)
        del g[v]
        order.append(v)
    return order, width

def choose_cut(hubs, fac, budget):
    if budget < 0:
        raise ValueError('negative width')
    adj = adjacency(hubs, fac)
    comps = components(adj)
    anchors = {min(comp) for comp in comps}
    cut = set(anchors)
    while True:
        remaining = {u: adj[u]-cut for u in hubs-cut}
        order, width = minfill(remaining)
        if width <= budget:
            return cut, anchors, order, width, len(comps)
        cut.add(min(remaining, key=lambda u: (-len(remaining[u]), u)))

def evaluate(factors, fixed, order):
    fs = []
    for scope, table in factors:
        rest = tuple(v for v in scope if v not in fixed)
        new = {}
        for xs in product(Q, repeat=len(rest)):
            a = dict(fixed)
            a.update(zip(rest, xs))
            new[xs] = table[tuple(a[v] for v in scope)]
        fs.append((rest, new))
    for v in order:
        bucket = [(s, t) for s, t in fs if v in s]
        fs = [(s, t) for s, t in fs if v not in s]
        if not bucket:
            fs.append(((), {(): 5}))
            continue
        rest = tuple(sorted(set().union(*(set(s) for s, _ in bucket))-{v}))
        table = {}
        for xs in product(Q, repeat=len(rest)):
            a = dict(zip(rest, xs))
            summand = 0
            for cv in Q:
                a[v] = cv
                p = 1
                for s, t in bucket:
                    p *= t[tuple(a[u] for u in s)]
                    if not p:
                        break
                summand += p
            table[xs] = summand
        fs.append((rest, table))
    if any(s for s, _ in fs):
        raise AssertionError('incomplete elimination')
    result = 1
    for _, t in fs:
        result *= t[()]
    return result

def count(n, edges, budget=2):
    model = construct(n, edges)
    if model is None:
        return 0, {'zero': True}
    hubs, fac, base = model
    cut, anchors, order, width, c = choose_cut(hubs, fac, budget)
    choices = sorted(cut-anchors)
    total = 0
    for xs in product(Q, repeat=len(choices)):
        fixed = {v: 0 for v in anchors}
        fixed.update(zip(choices, xs))
        total += evaluate(fac, fixed, order)
    return base * 5**c * total, {'width': width, 'cut': len(cut),
                                  'free_cut': len(choices), 'assignments': 5**len(choices),
                                  'surviving_vertices': len(hubs), 'components': c}

def wheel(r):
    if r < 4:
        raise ValueError('wheel rim size >=4')
    return 2*r+1, [(u, r+1+i) for i in range(r)
                    for u in (0, i+1, 1+(i+1)%r)]

def brute(n, arcs):
    src = set(arcs)
    return sum(all(beat(x[u], x[v]) for u, v in src)
               for x in product(Q, repeat=n))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--wheel', type=int, default=10)
    p.add_argument('--budget', type=int, default=1)
    p.add_argument('--test', action='store_true')
    a = p.parse_args()
    if a.test:
        for r in (4, 5):
            n, arcs = wheel(r)
            for budget in (0, 1, 2, 3):
                assert count(n, arcs, budget)[0] == 5*(3**r+1)
                if r == 4:
                    assert count(n, arcs, budget)[0] == brute(n, arcs)
        for r in (6, 10, 80):
            n, arcs = wheel(r)
            for budget in (1, 2):
                assert count(n, arcs, budget)[0] == 5*(3**r+1)
        print('14 wheel comparisons passed')
    else:
        n, arcs = wheel(a.wheel)
        z, meta = count(n, arcs, a.budget)
        print('count =', z)
        print('metadata =', meta)
