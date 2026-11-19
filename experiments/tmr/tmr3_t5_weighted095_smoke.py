#!/usr/bin/env python3
"""TMR-3/095: compact exact witness and physical-criticality red-team checks."""
from itertools import product

def ok(x, E):
    return all((x[v] - x[u]) % 5 in (1, 3) for u, v in E)

def witness(n, E):
    A = set(E)
    adj = [set() for _ in range(n)]
    for u, v in A:
        adj[u].add(v)
        adj[v].add(u)
    seen = set()
    out = [0] * n
    for root in range(n):
        if root in seen:
            continue
        order = [(root, None)]
        seen.add(root)
        for u, _ in order:
            for v in sorted(adj[u]):
                if v not in seen:
                    seen.add(v)
                    order.append((v, u))
        color = {root: 0}
        def dfs(i):
            if i == len(order):
                return color.copy()
            v, p = order[i]
            ds = (1, 3) if (p, v) in A else (-1, -3)
            for d in ds:
                color[v] = (color[p] + d) % 5
                if all((color[b] - color[a]) % 5 in (1, 3)
                       for a, b in A if a in color and b in color):
                    got = dfs(i+1)
                    if got is not None:
                        return got
            del color[v]
            return None
        values = dfs(1)
        if values is None:
            return None
        for i, c in values.items():
            out[i] = c
    assert ok(out, A)
    return tuple(out)

def pin_cycle(k):
    arcs = []
    for i in range(k):
        u, v, w = i, (i+1) % k, k+i
        arcs += [(u,v), (u,w), (w,v)]
    return arcs

def test():
    H = [(0,2),(0,3),(4,0),(1,2),(3,1),(1,4)]
    assert witness(5,H) is None
    for e in H:
        x = witness(5,[f for f in H if f!=e])
        assert x is not None and not ok(x,H)
    for k in range(3,10):
        E = pin_cycle(k)
        assert (witness(2*k,E) is not None) == (k%5 == 0)
        sat_after = [witness(2*k,[f for f in E if f!=e]) is not None for e in E]
        assert (k%5 == 0) or not all(sat_after)
        if k==3: assert sum(sat_after)==6
        if k==6: assert sum(sat_after)==0
    for n in range(2,6):
        pairs = [(a,b) for a in range(n) for b in range(a+1,n)]
        for pat in product((0,1,2), repeat=len(pairs)):
            E = [((a,b) if state==1 else (b,a))
                 for (a,b),state in zip(pairs,pat) if state]
            expected = any(ok(x,E) for x in product(range(5),repeat=n))
            x = witness(n,E)
            assert (x is not None) == expected
    print("PASS: original-edge critical deletion, modular counterexample, exhaustive n<=5")

if __name__=="__main__":
    test()
