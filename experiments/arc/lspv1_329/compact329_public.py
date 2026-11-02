#!/usr/bin/env python3
"""LSPV-1 329. Self-contained source-disjoint existential projection audit."""
from itertools import combinations,product
from collections import Counter
import json
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
Z=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
BP=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
BN=[(1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7)]
def make(p,n):return list(p)+[tuple(-z for z in c) for c in n]
def truth(c,a):return any(a[abs(z)-1]==(z>0) for z in c)
def cnf(F,a):return all(truth(c,a) for c in F)
def audit(F):
    n=max(abs(z) for c in F for z in c);m=len(F)
    assert 3*m==4*n and len({tuple(sorted(c)) for c in F})==m
    q=Counter((abs(z),z>0) for c in F for z in c)
    assert all(q[v,b]==2 for v in range(1,n+1) for b in (False,True))
    assert all(len(c)==3 and len({abs(z) for z in c})==3 and all(z*c[0]>0 for z in c) for c in F)
    adj={v:set() for v in range(1,n+1)}
    for c in F:
        for z in c:adj[abs(z)].update(abs(t) for t in c if abs(t)!=abs(z))
    I=[];blocked=set()
    for v in range(1,n+1):
        if v not in blocked:I.append(v);blocked.add(v);blocked.update(adj[v])
    assert len(I)>= (n+8)//9 and all(v not in adj[u] for u,v in combinations(I,2))
    rem=[v for v in range(1,n+1) if v not in I]
    unaffected=[c for c in F if not any(abs(z) in I for z in c)]
    clauses=unaffected[:]
    for v in I:
        pp=[tuple(z for z in c if abs(z)!=v) for c in F if v in c]
        nn=[tuple(z for z in c if abs(z)!=v) for c in F if -v in c]
        assert len(pp)==len(nn)==2
        clauses += [u+w for u,w in product(pp,nn)]
    assert len(clauses)==m and sum(map(len,clauses))==3*m+4*len(I)
    valid=0
    for bits in product((False,True),repeat=len(rem)):
        fixed=dict(zip(rem,bits));a=[False]*n
        for v,b in fixed.items():a[v-1]=b
        fac=all(truth(c,a) for c in unaffected)
        for v in I:
            pos=[tuple(z for z in c if abs(z)!=v) for c in F if v in c]
            neg=[tuple(z for z in c if abs(z)!=v) for c in F if -v in c]
            fac &= (all(truth(c,a) for c in pos) or all(truth(c,a) for c in neg))
        raw=cnf(clauses,a)
        exists=False
        for ib in product((False,True),repeat=len(I)):
            for v,b in zip(I,ib):a[v-1]=b
            exists |= cnf(F,a)
        assert fac==raw==exists
        valid+=int(fac)
    g=3*m-4*len(I)-1
    return dict(n=n,m=m,batch=I,projected_models=valid,
                source_models=sum(cnf(F,b) for b in product((False,True),repeat=n)),
                factored_gates=g,raw_CNF_gates=3*m+4*len(I)-1,gate_gap=8*len(I))
F9=make(P9,N9);Z6=make(Z,Z);B9=make(BP,BN)
H15=F9+[tuple((abs(z)+9)*(1 if z>0 else -1) for z in c) for c in Z6]
results={k:audit(f) for k,f in [('F9',F9),('Z6',Z6),('B9',B9),('H15',H15)]}
assert [results[k]['source_models'] for k in ('F9','Z6','B9','H15')]==[70,18,18,1260]
print(json.dumps(results,indent=2,sort_keys=True))
