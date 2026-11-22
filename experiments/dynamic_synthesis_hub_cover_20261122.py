"""Degree-cover residual solver and independent finite oracle. Python 3 standard library.

Run: python experiments/dynamic_synthesis_hub_cover_20261122.py
Imports the pinned Construction graph-star encoder/recognizer in this directory.
No polynomial claim is made for the oracle.
"""
import json
import random
from collections import Counter
from itertools import combinations, permutations, product
from dynamic_construction_join_palette_20261122 import encode, recover
from dynamic_construction_triangle_bundle_20261122 import expand

P = tuple(permutations(range(3)))
SIGN = {p: sum(p[i] > p[j] for i, j in combinations(range(3), 2)) % 2 for p in P}
STATS = Counter()

def compatible(u, f, v, g, match):
    if u > v:
        u, f, v, g = v, g, u, f
    p = match.get((u, v))
    return p is None or all(f[a] != g[p[a]] for a in range(3))

def blocks(vertices, adj):
    """Tarjan edge blocks, including bridges; isolated vertices handled separately."""
    depth, low, stack, out = {}, {}, [], []
    def visit(v, parent):
        depth[v] = low[v] = len(depth)
        for u in sorted(adj[v]):
            if u == parent:
                continue
            if u not in depth:
                stack.append((v, u))
                visit(u, v)
                low[v] = min(low[v], low[u])
                if low[u] >= depth[v]:
                    edges = []
                    while True:
                        edge = stack.pop()
                        edges.append(edge)
                        if edge == (v, u):
                            break
                    out.append(edges)
            elif depth[u] < depth[v]:
                stack.append((v, u))
                low[v] = min(low[v], depth[u])
    for v in sorted(vertices):
        if v not in depth:
            visit(v, None)
    return out

def exceptional(block):
    degree = Counter(x for e in block for x in e)
    size = len(degree)
    return len(block) == size*(size-1)//2 or all(d == 2 for d in degree.values())

def eliminate(vertices, adj, lists, match):
    """Exact Boolean variable elimination on clique/cycle block graphs."""
    graph = {v: set(adj[v]) for v in vertices}
    factors = [((v,), {(p,) for p in lists[v]}) for v in vertices]
    for u in vertices:
        for v in adj[u]:
            if u < v:
                factors.append(((u, v), {(f,g) for f in lists[u] for g in lists[v]
                                          if compatible(u,f,v,g,match)}))
    while graph:
        choices = [v for v in graph if len(graph[v]) <= 2 or
                   (len(graph[v]) <= 3 and all(b in graph[a] for a,b in combinations(graph[v],2)))]
        assert choices, 'GDP block elimination invariant failed'
        v = min(choices)
        neighbors = tuple(sorted(graph[v]))
        STATS['max_elimination_width'] = max(STATS['max_elimination_width'],len(neighbors))
        picked = [(s,t) for s,t in factors if v in s]
        factors = [(s,t) for s,t in factors if v not in s]
        table = set()
        for row in product(*(lists[u] for u in neighbors)):
            a = dict(zip(neighbors,row))
            for color in lists[v]:
                a[v] = color
                if all(tuple(a[u] for u in scope) in values for scope,values in picked):
                    table.add(row)
                    break
        if not table:
            return False
        factors.append((neighbors,table))
        for a,b in combinations(neighbors,2):
            graph[a].add(b)
            graph[b].add(a)
        for u in neighbors:
            graph[u].remove(v)
        del graph[v]
    return all(() in table for scope,table in factors)

def residual(vertices, lists, match):
    adj = {v:set() for v in vertices}
    for u,v in match:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    assert all(len(lists[v]) >= len(adj[v]) for v in vertices)
    unseen = set(vertices)
    while unseen:
        root = min(unseen)
        component, todo = {root}, [root]
        unseen.remove(root)
        while todo:
            for v in adj[todo.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    todo.append(v)
        if any(not exceptional(b) for b in blocks(component,adj)):
            STATS['non_GDP_components_accepted'] += 1
            continue
        STATS['GDP_components_decided'] += 1
        if not eliminate(component,adj,lists,match):
            return False
    return True

def solve(q, match):
    adj = [set() for _ in range(q)]
    for u,v in match:
        adj[u].add(v)
        adj[v].add(u)
    signs = {}
    for root in range(q):
        if root in signs:
            continue
        signs[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v in sorted(adj[u]):
                z = signs[u] ^ SIGN[match[min(u,v),max(u,v)]]
                if v in signs:
                    if signs[v] != z:
                        return False
                else:
                    signs[v] = z
                    todo.append(v)
    lists = {v: tuple(p for p in P if SIGN[p] == signs[v]) for v in range(q)}
    hubs = tuple(v for v in range(q) if len(adj[v]) >= 4)
    rest = set(range(q))-set(hubs)
    for row in product(*(lists[v] for v in hubs)):
        fixed = dict(zip(hubs,row))
        if any(not compatible(u,fixed[u],v,fixed[v],match) for u,v in combinations(hubs,2)):
            continue
        remaining = {v: tuple(f for f in lists[v] if all(compatible(u,g,v,f,match)
                       for u,g in fixed.items())) for v in rest}
        if residual(rest,remaining,match):
            return True
    return False

def oracle(q, match):
    """Independent six-permutation backtracking, with no parity or DP theorem."""
    chosen = {}
    def dfs(v):
        if v == q:
            return True
        for f in P:
            if all(compatible(u,g,v,f,match) for u,g in chosen.items()):
                chosen[v] = f
                if dfs(v+1):
                    return True
                del chosen[v]
        return False
    return dfs(0)

def relabel(q, match, rng):
    labels = [rng.choice(P) for _ in range(q)]
    result = {}
    for (u,v),p in match.items():
        perm = [0]*3
        for a in range(3):
            perm[labels[u][a]] = labels[v][p[a]]
        result[u,v] = tuple(perm)
    return result

def main():
    rng = random.Random(3241122)
    counts = Counter()
    cases = []
    # Every labeled five-vertex graph with at most one vertex of degree >=4.
    pairs = list(combinations(range(5),2))
    for mask in range(1 << len(pairs)):
        edges = [e for i,e in enumerate(pairs) if mask >> i & 1]
        degrees = Counter(v for e in edges for v in e)
        if sum(d >= 4 for d in degrees.values()) <= 1:
            for mode in range(3):
                match = {e: (P[0] if mode == 0 else rng.choice(P if mode == 1 else (P[0],P[3],P[4]))) for e in edges}
                cases.append(('all_q5',5,relabel(5,match,rng)))
    # Wheel over an odd/even rim: one high-degree hub, reduced cycle lists.
    for rim in (4,5,6):
        edges = sorted({tuple(sorted((i,(i+1)%rim))) for i in range(rim)} | {(i,rim) for i in range(rim)})
        for mode in range(24):
            match = {e: P[0] if mode == 0 else rng.choice((P[0],P[3],P[4])) for e in edges}
            cases.append(('wheels',rim+1,relabel(rim+1,match,rng)))
    half = set(combinations(range(4),2))-{(0,1)} | {(0,4),(1,4)}
    bridge = sorted(half | {(u+5,v+5) for u,v in half} | {(4,9)})
    for mode in range(12):
        match = {e: rng.choice((P[0],P[3],P[4])) for e in bridge}
        cases.append(('cubic_bridge',10,relabel(10,match,rng)))
    for q in (6,7):
        for mode in range(24):
            match = {e:rng.choice((P[0],P[3],P[4])) for e in combinations(range(q),2) if rng.randrange(2)}
            cases.append(('multiple_hubs',q,relabel(q,match,rng)))
    cases.append(('all_hubs_K5',5,{e:P[0] for e in combinations(range(5),2)}))
    for name,q,match in cases:
        prediction,actual = solve(q,match),oracle(q,match)
        assert prediction == actual, (name,q,match,prediction,actual)
        h,edges = expand(q,match)
        n,rows = encode(h,edges)
        assert recover(n,[r[::-1] for r in rows[::-1]]) == (h,edges)
        assert n == 33*q+9*len(match) and len(rows) == 21*q+9*len(match)
        counts[name+('_SAT' if actual else '_UNSAT')] += 1
    # Independently certify both labels and the need for specific residual covers.
    controls = {}
    controls['empty_isolated_list'] = residual({0},{0:()}, {})
    assert controls['empty_isolated_list'] is False
    for rim in (4,5,6):
        match = {tuple(sorted((i,(i+1)%rim))):P[0] for i in range(rim)}
        match.update({(i,rim):P[0] for i in range(rim)})
        controls['identity_wheel_'+str(rim)] = solve(rim+1,match)
        assert controls['identity_wheel_'+str(rim)] == (rim % 2 == 0)
    print(json.dumps({'status':'PASS','seed':3241122,'cases':len(cases),'counts':dict(sorted(counts.items())),
                      'branch_counts':dict(STATS),'controls':controls,
                      'scope':'finite semantic and source-roundtrip checks, not native tape or asymptotic proof'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
