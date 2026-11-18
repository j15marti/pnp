#!/usr/bin/env python3
"""TMR-3/094 exact small T5 critical-witness and pinning smoke tests."""
import itertools
R={(a,b) for a in range(5) for b in range(5) if (b-a)%5 in (1,3)}
H=[(0,2),(0,3),(4,0),(1,2),(3,1),(1,4)]
def models(n,edges):
    for tail in itertools.product(range(5),repeat=n-1):
        x=(0,)+tail
        if all((x[u],x[v]) in R for u,v in edges): yield x
def check_critical():
    assert not next(models(5,H),None)
    counts=[]
    for e in H:
        M=list(models(5,[a for a in H if a!=e]))
        assert M
        assert all((x[e[1]]-x[e[0]])%5 in (0,2,4) for x in M)
        counts.append(len(M))
    return counts
def check_pin():
    for a in range(5):
        for b in range(5):
            W=[w for w in range(5) if (a,b) in R and (a,w) in R and (w,b) in R]
            assert len(W)==(1 if b==(a+1)%5 else 0)
            if W: assert W==[(a+3)%5]
def check_threads():
    rel={}
    for L in (1,2,3):
        for f in range(L+1):
            domain=[(1,3)]*f+[(2,4)]*(L-f)
            observed={sum(combo)%5 for combo in itertools.product(*domain)}
            formula={(2*L-f+2*j)%5 for j in range(L+1)}
            assert observed==formula
            rel[L,f]=frozenset(observed)
    assert len(set(rel.values()))==9
    v=list(rel.values());maxir=0
    for mask in range(1,2**9):
        J=[i for i in range(9) if mask>>i&1]
        S=set.intersection(*(set(v[i]) for i in J))
        if all(set.intersection(*(set(v[j]) for j in J if j!=i))!=S for i in J if len(J)>1):
            maxir=max(maxir,len(J))
    assert maxir==4
    return maxir
if __name__=="__main__":
    check_pin()
    print("critical deleted-arc rooted counts:",check_critical())
    print("short-thread maximum irredundant:",check_threads())
    print("PASS: all assertions")
