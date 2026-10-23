#!/usr/bin/env python3
"""CAPACITY70: independent, stdlib-only flow and witness replay quickcheck."""
from collections import deque
from itertools import product

def flow_sign(edges, assignment, budgets=None, t=None):
    n = len(assignment)
    m = len(edges)
    r = len(edges[0])
    assert all(len(e) == r and len(set(e)) == r for e in edges)
    deg = [sum(v in e for e in edges) for v in range(n)]
    if budgets is None:
        assert all(d % 2 == 0 for d in deg)
        budgets = [d // 2 for d in deg]
    c = [budgets[v] if assignment[v] else deg[v]-budgets[v] for v in range(n)]
    if t is None: t = r // 2
    V = m+n+2
    src, sink = 0, V-1
    G = [[] for _ in range(V)]
    incident = {}
    def add(u, v, cap):
        a = [v, cap, len(G[v])]
        b = [u, 0, len(G[u])]
        G[u].append(a)
        G[v].append(b)
        return a
    for j, edge in enumerate(edges):
        add(src, 1+j, t)
        for v in edge:
            incident[(j, v)] = add(1+j, m+1+v, 1)
    for v in range(n):
        add(m+1+v, sink, c[v])
    value = 0
    while True:
        dist = [-1]*V
        dist[src] = 0
        queue = deque([src])
        while queue:
            u = queue.popleft()
            for v, cap, _ in G[u]:
                if cap and dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        if dist[sink] < 0: break
        it = [0]*V
        def aug(u, lim):
            if u == sink: return lim
            while it[u] < len(G[u]):
                arc = G[u][it[u]]
                v, cap, reverse = arc
                if cap and dist[v] == dist[u]+1:
                    pushed = aug(v, min(lim, cap))
                    if pushed:
                        arc[1] -= pushed
                        G[v][reverse][1] += pushed
                        return pushed
                it[u] += 1
            return 0
        while True:
            pushed = aug(src, 10**9)
            if not pushed: break
            value += pushed
    if value < m*t: return None
    good = {loc for loc, arc in incident.items() if arc[1] == 0}
    for v in range(n):
        inc = [(j,v) for j, e in enumerate(edges) if v in e]
        extra = c[v]-sum((j,v) in good for (j,_) in inc)
        assert extra >= 0
        for loc in inc:
            if extra and loc not in good:
                good.add(loc)
                extra -= 1
        assert extra == 0
    signs = [[1 if ((j,v) in good) == bool(assignment[v]) else -1
              for v in e] for j,e in enumerate(edges)]
    plus = [0]*n
    minus = [0]*n
    for e, sign in zip(edges, signs):
        truecount = 0
        for v, s in zip(e, sign):
            if s == 1: plus[v] += 1
            else: minus[v] += 1
            truecount += ((s == 1) == bool(assignment[v]))
        assert truecount >= t
    assert plus == budgets
    assert [plus[v]+minus[v] for v in range(n)] == deg
    return signs

def main():
    families = {
      "cycle2": [(0,1),(1,2),(2,3),(3,0)],
      "tetra3": [(0,1,2),(0,3,4),(1,3,5),(2,4,5)],
      "cube3": [(a,2+b,4+c) for a,b,c in product((0,1),repeat=3)],
      "quad4": [(0,1,2,3),(0,1,4,5),(2,3,6,7),(4,5,6,7)],
      "five4": [tuple(v for v in range(5) if v != omit) for omit in range(5)],
    }
    tests = 0
    for name, edges in families.items():
        n = max(max(e) for e in edges)+1
        for assignment in product((0,1), repeat=n):
            assert flow_sign(edges,assignment) is not None
            tests += 1
    singleton = [(0,1,2)]
    assert flow_sign(singleton,(1,1,1),[0,0,0],t=1) is None
    assert flow_sign(singleton,(1,1,1),[1,0,0],t=1) is not None
    assert flow_sign(singleton,(1,1,1),[1,1,0],t=1) is not None
    print({"verified_assignments":tests,"hostile_cases":3,"errors":0})
if __name__ == "__main__": main()
