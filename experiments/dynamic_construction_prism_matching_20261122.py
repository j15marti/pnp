"""Deterministic source and projected-cycle audit. Run with Python 3."""
from functools import lru_cache
from itertools import combinations, product
import json


def family(q, switched):
    if q < 3:
        raise ValueError("prism length must be at least three")
    hub = 3 * (2*q + 1)
    edges = []
    for lobe in range(3):
        start = lobe * (2*q + 1)
        tip = start + 2*q
        for i in range(q):
            for side in (0, q):
                edges.append((start+side+i, start+side+(i+1) % q))
        edges.extend([(start, tip), (start+q, tip), (tip, hub)])
        for i in range(1, q):
            if i == 1 and switched and lobe < 2:
                edges.append((start+1+lobe*q, start+1+lobe*q+(1-2*lobe)*(2*q+1)))
            else:
                edges.append((start+i, start+q+i))
    clauses = [[] for _ in range(hub+1)]
    for name, endpoints in enumerate(edges):
        for vertex in endpoints:
            clauses[vertex].append(name)
    assert all(len(set(row)) == 3 for row in clauses)
    return edges, clauses


def reference_matching(edges, m):
    neighbors = [set() for _ in range(m)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)

    @lru_cache(None)
    def solve(mask):
        if mask == 0:
            return ()
        a = (mask & -mask).bit_length()-1
        rest = mask ^ (1 << a)
        for b in sorted(neighbors[a]):
            if rest & (1 << b):
                tail = solve(rest ^ (1 << b))
                if tail is not None:
                    return ((min(a,b), max(a,b)),) + tail
        return None
    return solve((1 << m)-1)


def cycle(values, clauses):
    path = []
    checks = []
    for bit in values:
        path.extend([1, bit, 0, 1, 0])
    for row in clauses:
        a,b,c = (values[x] for x in row)
        start = len(path)
        path.extend([1, 1-a, c, 0, 1, 0])
        for i,x in enumerate(row):
            checks.append((5*x+1, start+i, start+i+1))
    top = "AACAC"*len(values)+"AAACAC"*len(clauses)
    bottom = "AACCC"*len(values)+"AAACCC"*len(clauses)
    for i, pair in enumerate(zip(top,bottom)):
        x,y = path[i],path[(i+1)%len(path)]
        assert (x>=y if pair==('A','A') else x!=y if pair==('C','C') else (x,y)==(1,0))
    assert all(path[a]^path[b]^path[c]==0 for a,b,c in checks)
    return len(path), len(checks)


def main():
    controls = []
    for q in range(3,9):
        for switched in (False, True):
            edges, clauses = family(q,switched)
            m,v = len(clauses),len(edges)
            assert (m,v)==(6*q+4,9*q+6)
            matching = reference_matching(edges,m)
            assert (matching is not None)==switched
            if switched:
                chosen = set(matching)
                values = [int(tuple(sorted(e)) in chosen) for e in edges]
                assert all(sum(values[x] for x in row)==1 for row in clauses)
                assert cycle(values,clauses)==(5*v+6*m,3*m)
            controls.append(dict(q=q,m=m,v=v,SAT=switched,matching=matching))
    # Independent occurrence-assignment oracle on every simple cubic graph on 4 or 6 labeled vertices.
    counts = {}
    for n in (4,6):
        keys = list(combinations(range(n),2))
        accepted = 0
        for es in combinations(keys,3*n//2):
            incident = [[i for i,e in enumerate(es) if j in e] for j in range(n)]
            if any(len(row)!=3 for row in incident):
                continue
            sat = any(all(sum(bits[i] for i in row)==1 for row in incident)
                      for bits in product((0,1),repeat=len(es)))
            assert sat == (reference_matching(es,n) is not None)
            accepted += 1
        counts[n] = accepted
    print(json.dumps(dict(controls=controls,exhaustive_graph_counts=counts,
                          method="exact recursive oracle; projected SAT extensions; no native TM or blossom benchmark"),indent=2))


if __name__ == "__main__":
    main()
