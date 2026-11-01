#!/usr/bin/env python3
"""Independent compact GATE291 canonical n=6 Fourier/peeling census, stdlib only."""
from collections import Counter, defaultdict, deque
from itertools import combinations, product
import json

V = tuple(range(1, 7))
TR = tuple(combinations(V, 3))
PA = tuple(combinations(V, 2))
PAT = tuple(frozenset(Q) for Q in combinations(TR, 4)
            if all(sum(v in t for t in Q) == 2 for v in V))
assert len(PAT) == 75

def signature(P, Q):
    return (tuple(sum(a in t and b in t for t in P) +
                  sum(a in t and b in t for t in Q) for a,b in PA),
            tuple((t in P) - (t in Q) for t in TR))

def peel(P, Q):
    only_p, only_q = P - Q, Q - P
    h = {v: 2 - sum(v in t for t in only_p) for v in V}
    assert all(h[v] == 2 - sum(v in t for t in only_q) for v in V)
    R = Counter()
    for t in P & Q:
        for pair in combinations(t, 2): R[pair] += 1
    todo = deque(v for v in V if h[v] == 1)
    found = set()
    while todo:
        v = todo.popleft()
        if h[v] != 1: continue
        nbr = [u for u in V if u != v and R[tuple(sorted((u,v)))] > 0]
        assert len(nbr) == 2
        t = tuple(sorted((v, *nbr)))
        assert t in P & Q and t not in found
        found.add(t)
        for pair in combinations(t, 2):
            assert R[pair] >= 1
            R[pair] -= 1
        for u in t:
            h[u] -= 1
            if h[u] == 1: todo.append(u)
    assert all(h[v] in (0,2) for v in V)
    return found

def sat_models(P, Q):
    return sum(all(any(a[v-1] for v in t) for t in P) and
               all(any(not a[v-1] for v in t) for t in Q)
               for a in product((False,True),repeat=6))

classes = defaultdict(list)
recovered = 0
for P in PAT:
    for Q in PAT:
        classes[signature(P, Q)].append((P,Q))
        if P != Q:
            assert peel(P,Q) == P & Q
            recovered += 1
assert len(classes) == 5610
sizes = Counter(map(len,classes.values()))
assert sizes == {1:5595, 2:15}
assert recovered == 5550
assert all(P == Q for C in classes.values() if len(C)==2 for P,Q in C)
P = frozenset([(1,2,3),(1,4,5),(2,4,6),(3,5,6)])
Q = frozenset([(1,2,4),(1,3,5),(2,3,6),(4,5,6)])
assert signature(P,P)==signature(Q,Q)
assert sat_models(P,P)==sat_models(Q,Q)==18
print(json.dumps({'valid_n6':len(PAT)**2,'full_signature_classes':len(classes),
                  'singleton':sizes[1],'doubleton':sizes[2],
                  'recovered_unpaired_connected':recovered,
                  'paired_only_unrecovered':len(PAT),
                  'paired_Pasch_equal_models':18,
                  'status':'PASS; restricted, P versus NP OPEN'},indent=2))
