#!/usr/bin/env python3
"""Compact exact signed-(2,2) raw-restriction and affine witness-cover test.
Run from the j15marti/pnp root (optional path to the canonical 198/264 source).
No source-bit oracle, no universal SAT-runtime lower bound."""
import ast,itertools,json,sys
from collections import Counter

def formula(q):
    out=[]
    for j in range(q):
        v=[3*j+i for i in (1,2,3)]
        for x in itertools.product((0,1),repeat=3):
            if sum(x)%2:
                out.append(tuple(-a if b else a for a,b in zip(v,x)))
    return out

def stats(F,n,rho):
    d=Counter((abs(l),l>0) for c in F for l in c)
    assert len(F)*3==4*n
    assert all(d[(i,True)]==d[(i,False)]==2 for i in range(1,n+1))
    touched=sum(any(abs(l) in rho for l in c) for c in F)
    removed=sum(any(abs(l) in rho and rho[abs(l)]==(l>0) for l in c) for c in F)
    remain=len(F)-removed
    untouched=len(F)-touched
    assert remain>=len(F)-2*len(rho)
    assert untouched>=len(F)-4*len(rho)
    return dict(k=len(rho),remaining=remain,untouched=untouched,satisfied=removed)

def cover(q,L):
    good=[b for b in itertools.product((0,1),repeat=3) if sum(b)%2==0]
    F=formula(q)
    prefixes=list(itertools.product(range(4),repeat=q-L))
    seen=Counter()
    for x in itertools.product(range(4),repeat=q):
        seen[x[:q-L]]+=1
    assert len(prefixes)==4**(q-L) and len(seen)==4**(q-L)
    assert all(v==4**L for v in seen.values())
    for p in prefixes:
        rho={3*j+h+1:good[a][h] for j,a in enumerate(p) for h in range(3)}
        assert stats(F,3*q,rho)['remaining']==4*L
    return dict(q=q,L=L,models=4**q,children=4**(q-L),clauses_per_child=4*L)

out={'id':'ARC-RESTRICTION-COVER118',
     'controls':[cover(q,L) for q,L in [(2,0),(3,1),(4,1),(5,2)]],
     'scaling':[stats(formula(q),3*q,{i:False for i in range(1,q+1)})
                for q in [2,8,32,128]]}
if len(sys.argv)>1:
    src='\n'.join(s for s in open(sys.argv[1]) if not s.startswith('#'))
    U=ast.literal_eval(src)
    out['strict_198_264']=[stats(U,198,{i:(i%2)==0 for i in range(1,k+1)})
                           for k in [0,12,33,66]]
print(json.dumps(out,sort_keys=True))
