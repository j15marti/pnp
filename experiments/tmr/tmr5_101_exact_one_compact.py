#!/usr/bin/env python3
"""TMR-5/101 executable independent T5 exact-one critical-family checks.

Standard library only. Run: python3 tmr5_101_exact_one_compact.py
Fixed relation Q(h,u,v)=R(h,u) XOR R(h,v), self comparisons false.
No claims of general SAT lower bounds.
"""
from collections import deque
from itertools import combinations, product
import json

W = ({1, 3}, {2, 4}, {0, 3}, {1, 4}, {0, 2})

def Q(x, y, z):
    return (y in W[x]) != (z in W[x])

def pair(a, b):
    return (a, b) if a < b else (b, a)

def graphs(L):
    n = L
    edges = sorted({pair(i, (i+1) % L) for i in range(L)})
    hist = [(n, edges)]
    for level in range(3):
        new_edges = set(edges)
        for u, v in edges:
            new_edges.add(pair(u, n+v))
            new_edges.add(pair(v, n+u))
        for u in range(n):
            new_edges.add(pair(n+u, 2*n))
        n = 2*n+1
        edges = sorted(new_edges)
        hist.append((n, edges))
    return hist

def deletion_colors(hist, level, omitted):
    n, edges = hist[level]
    if level == 0:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            if (u, v) != omitted:
                adj[u].append(v)
                adj[v].append(u)
        colors = [-1]*n
        colors[0] = 0
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if colors[v] < 0:
                    colors[v] = 1-colors[u]
                    queue.append(v)
        assert -1 not in colors
        assert colors[omitted[0]] == colors[omitted[1]]
        return colors
    old_n, old_edges = hist[level-1]
    a, b = omitted
    extra = level+1
    if b < old_n:
        c = deletion_colors(hist, level-1, omitted)
        r = c[a]
        return c + [extra if x == r else x for x in c] + [r]
    if b == 2*old_n:
        i = a-old_n
        incident = next(edge for edge in old_edges if i in edge)
        c = deletion_colors(hist, level-1, incident)
        ans = c.copy()+c.copy()+[extra]
        ans[i] = ans[old_n+i] = extra
        return ans
    i = b-old_n
    j = a
    c = deletion_colors(hist, level-1, pair(i, j))
    assert c[i] == c[j]
    ans = c.copy()+c.copy()+[extra]
    ans[i] = extra
    return ans

def bipartite(n, clauses, head=None):
    adj = [[] for _ in range(n)]
    for h, a, b in clauses:
        if head is None or h == head:
            adj[a].append(b)
            adj[b].append(a)
    colors = [-1]*n
    for start in range(n):
        if colors[start] >= 0:
            continue
        colors[start] = 0
        todo = [start]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if colors[v] < 0:
                    colors[v] = 1-colors[u]
                    todo.append(v)
                elif colors[v] == colors[u]:
                    return False
    return True

def four_variable_census():
    scopes = [(h, a, b) for h in range(4)
              for a, b in combinations([x for x in range(4) if x != h], 2)]
    masks = []
    for h, a, b in scopes:
        masks.append(sum(1 << i for i, t in
                         enumerate(product(range(5), repeat=4))
                         if Q(t[h], t[a], t[b])))
    solutions = [(1 << 625)-1]*4096
    for subset in range(1, 4096):
        bit = subset & -subset
        solutions[subset] = solutions[subset ^ bit] & masks[bit.bit_length()-1]
    feasible_unsat = minimal = 0
    sample = None
    for subset in range(4096):
        if solutions[subset]:
            continue
        chosen = [scopes[i] for i in range(12) if subset >> i & 1]
        if not bipartite(4, chosen) or not all(
                bipartite(4, chosen, h) for h in range(4)):
            continue
        feasible_unsat += 1
        if all(solutions[subset ^ (1 << i)] for i in range(12)
               if subset >> i & 1):
            minimal += 1
            assert len(chosen) == 6
            if sample is None:
                sample = {"clauses": chosen, "deletion_counts": [
                    solutions[subset ^ (1 << i)].bit_count()
                    for i in range(12) if subset >> i & 1]}
    assert (feasible_unsat, minimal) == (63, 36)
    return {"systems": 4096, "bipartite_parity_UNSAT": feasible_unsat,
            "minimal_six_clauses": minimal, "sample": sample}

def main():
    result = {"four_variable": four_variable_census(), "critical": []}
    for L in (5, 7, 9):
        hist = graphs(L)
        n, edges = hist[3]
        m = len(edges)
        assert n == 8*L+7 and m == 46*L+6
        checks = 0
        for omitted_index, omitted in enumerate(edges):
            c = deletion_colors(hist, 3, omitted)
            assert len(c) == n and max(c) < 5
            assert c[omitted[0]] == c[omitted[1]]
            for i, (u, v) in enumerate(edges):
                assert (c[u] != c[v]) == (i != omitted_index)
                h = c[u] if c[v] in W[c[u]] else c[v]
                assert Q(h, c[u], c[v]) == (i != omitted_index)
                checks += 1
        # Matched-scope P is SAT: assign original vertices A=0,
        # private heads C=2, since C beats A.
        assert 0 in W[2]
        result["critical"].append({"L": L, "vertices": n,
                                   "Q_variables": n+m, "Q_clauses": m,
                                   "verified_deletions": m,
                                   "Q_predicate_checks": checks,
                                   "old_P_status": "SAT"})
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
