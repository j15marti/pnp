#!/usr/bin/env python3
"""LSPV-2 CUBIC-FACTOR-PORT288, compact independent exhaustive reproducer.
Pure stdlib. Restricted six-variable valid canonical target; P versus NP OPEN.
Full independent 198-variable UNSAT and physical tape verification is in ZIP.
"""
from itertools import combinations, product
from collections import Counter
T=list(combinations(range(1,7),3))
F=[q for q in combinations(T,4) if all(sum(v in c for c in q)==2 for v in range(1,7))]
assert len(F)==75
def witness(P,Q,t):
    return all(any(v in t for v in c) for c in P) and all(not set(c)<=t for c in Q)
def matching_pairs(P):
    return [a for a in combinations(range(1,7),2) if all(set(a)&set(c) for c in P)]
counts=Counter();types=Counter();pin_checks=0
for P in F:
    p=matching_pairs(P)
    assert len(p) in (3,5)
    types[len(p)]+=1
    assert any(len(set().union(*map(set,t)))==6 for t in combinations(p,3))
    for Q in F:
        q=matching_pairs(Q)
        h=sum(tuple(v for v in range(1,7) if v not in c) in Q for c in P)
        models=[frozenset(t) for k in range(7) for t in combinations(range(1,7),k) if witness(P,Q,set(t))]
        assert len(models)==12+h+len(p)+len(q)
        assert sum(len(m)==2 for m in models)==len(p)
        assert sum(len(m)==3 for m in models)==12+h
        assert sum(len(m)==4 for m in models)==len(q)
        for i,j in combinations(range(1,7),2):
            for a,b in product((0,1),repeat=2):
                candidates=[m for m in models if (i in m)==a and (j in m)==b]
                assert candidates
                wanted=2 if a==b==0 else 4 if a==b==1 else 3
                assert any(len(m)==wanted for m in candidates)
                pin_checks+=1
        counts[len(models)]+=1
assert types=={3:30,5:45}
assert counts=={18:450,19:240,20:1080,21:1440,22:1650,24:720,26:45}
assert pin_checks==337500
print({"PASS":True,"families":len(F),"formulas":sum(counts.values()),"two_pin":pin_checks,"model_histogram":dict(counts),"P_versus_NP":"OPEN"})
