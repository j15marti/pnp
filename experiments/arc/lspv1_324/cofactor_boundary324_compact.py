#!/usr/bin/env python3
"""LSPV-1 324: source-certified exact cofactors, sensitivity, binary gate bounds.
Standalone standard-library check; does not import the long-form producer.
All truth-table operations are OFFLINE diagnostics, not free solver primitives.
"""
from itertools import product
from collections import Counter
from math import ceil, log2
import json

G6=((1,2,3),(1,2,4),(3,5,6),(4,5,6))
F9P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))

def source(n, pos, neg):
    c=tuple((s, tuple(t)) for s, group in ((1,pos),(-1,neg)) for t in group)
    assert len(c)*3==4*n and len(set((s,tuple(sorted(t))) for s,t in c))==len(c)
    assert all(len(set(t))==3 and all(1<=x<=n for x in t) for _,t in c)
    assert all(sum(x in t for p,t in c if p==s)==2
               for x in range(1,n+1) for s in (-1,1))
    return c

def holds(c, a):
    return all(any(bool(a[x-1])==(s==1) for x in t) for s,t in c)

def cofactor_boundary(n,c):
    truth={bits:holds(c,bits) for bits in product((0,1),repeat=n)}
    sats=[a for a in truth if truth[a]]
    by_var=[0]*n
    distribution=Counter()
    for a in sats:
        critical=[]
        buckets=[0]*4
        for s,t in c:
            buckets[sum(a[x-1]==(s==1) for x in t)]+=1
        assert buckets[0]==0 and buckets[1]==len(c)//2+buckets[3]
        for i in range(n):
            b=a[:i]+(1-a[i],)+a[i+1:]
            if not truth[b]:
                critical.append(i)
                by_var[i]+=1
        assert len(critical)>=n//3
        distribution[len(critical)]+=1
    # Independent pair-of-cofactors count, without a witness.
    miter_counts=[]
    for i in range(n):
        count=0
        for z in product((0,1),repeat=n-1):
            x0=z[:i]+(0,)+z[i:]
            x1=z[:i]+(1,)+z[i:]
            count+=truth[x0]!=truth[x1]
        miter_counts.append(count)
    assert miter_counts==by_var
    assert sum(by_var)==sum(k*v for k,v in distribution.items())
    assert sum(by_var)>=(n//3)*len(sats)
    return dict(n=n,m=len(c),sat=len(sats),boundary=sum(by_var),
                per_pivot=by_var,minimum_sensitivity=min(distribution) if sats else None,
                sensitivity_distribution=dict(sorted(distribution.items())),
                source_private_gates=3*len(c)-1,
                source_private_depth=2+ceil(log2(len(c))))

def pin_models(n,c,p):
    return sum(holds(c,a) and all(a[i-1]==v for i,v in p.items())
               for a in product((0,1),repeat=n))

def main():
    g=source(6,G6,G6)
    f=source(9,F9P,F9N)
    out={"G6":cofactor_boundary(6,g),"F9":cofactor_boundary(9,f)}
    assert (out["G6"]["sat"],out["G6"]["boundary"])==(26,76)
    assert (out["F9"]["sat"],out["F9"]["boundary"])==(70,402)
    assert pin_models(6,g,{1:0,2:0,3:1})==3
    assert pin_models(6,g,{1:0,2:0,3:0})==0
    assert pin_models(9,f,{1:0,3:0,5:1,6:0,7:0,8:0})==2
    assert pin_models(9,f,{1:1,3:0,5:1,6:0,7:0,8:0})==0
    w=(0,0,1,1,0,0)
    assert holds(g,w)
    assert sum(not holds(g,w[:i]+(1-w[i],)+w[i+1:]) for i in range(6))==2
    print(json.dumps(out,indent=2))
if __name__=="__main__":
    main()
