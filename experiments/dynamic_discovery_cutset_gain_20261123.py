"""Exact cutset-conditioned gain decision and independent exhaustive checks."""
from itertools import combinations, product
import json


def solve(q, edges, gains):
    representative = list(range(q))

    def root(v):
        while representative[v] != v:
            v = representative[v]
        return v

    cut = set()
    chords = 0
    for u, v in edges:
        a, b = root(u), root(v)
        if a == b:
            cut.add(u)
            chords += 1
        else:
            representative[a] = b
    cut = sorted(cut)
    adjacency = [[] for _ in range(q)]
    for (u, v), g in zip(edges, gains):
        adjacency[u].append((v, g))
        adjacency[v].append((u, -g % 3))
    forest = set(range(q)) - set(cut)
    parent = {}
    order = []
    for v in sorted(forest):
        if v in parent:
            continue
        parent[v] = None
        stack = [v]
        while stack:
            u = stack.pop()
            order.append(u)
            for w, _ in adjacency[u]:
                if w in forest and w not in parent:
                    parent[w] = u
                    stack.append(w)
                elif w in forest and parent[u] != w:
                    assert parent.get(w) == u
    attempts = 0
    for labels in product(range(3), repeat=len(cut)):
        attempts += 1
        fixed = dict(zip(cut, labels))
        if any((fixed[u]-fixed[v]) % 3 == g for (u,v),g in zip(edges,gains)
               if u in fixed and v in fixed):
            continue
        allowed = {}
        for u in reversed(order):
            allowed[u] = {a for a in range(3)
                          if all((a-fixed[v]) % 3 != g for v,g in adjacency[u]
                                 if v in fixed)
                          and all(any((a-b) % 3 != g for b in allowed[v])
                                  for v,g in adjacency[u] if parent.get(v) == u)}
        if all(allowed[u] for u in order if parent[u] is None):
            return True, len(cut), chords, attempts
    return False, len(cut), chords, attempts


def main():
    results = []
    for q, edges in [(5,list(combinations(range(4),2))+[(3,4)]),
                     (4,[(0,1),(1,2),(2,3)]), (3,[])]:
        checked = sat = max_attempts = 0
        for gains in product(range(3), repeat=len(edges)):
            actual,s,r,attempts = solve(q,edges,gains)
            expected = any(all((x[u]-x[v]) % 3 != g
                               for (u,v),g in zip(edges,gains))
                           for x in product(range(3),repeat=q))
            assert actual == expected
            assert s <= r and attempts <= 3**s
            checked += 1
            sat += actual
            max_attempts = max(max_attempts,attempts)
        results.append(dict(q=q,k=len(edges),checked=checked,sat=sat,
                            unsat=checked-sat,cutset_size=s,cycle_rank=r,
                            max_attempts=max_attempts))
    print(json.dumps(results,sort_keys=True))


if __name__ == '__main__':
    main()
