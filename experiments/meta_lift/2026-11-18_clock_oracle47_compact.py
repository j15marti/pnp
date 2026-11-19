#!/usr/bin/env python3
"""CLOCKORACLE47 compact, independently runnable finite controls."""
from functools import lru_cache
from itertools import product
import json

def value(rowbits,R,B):
    return any(all(rowbits[r*B+b] for b in range(B)) for r in range(R))

@lru_cache(None)
def frontier(R,B,mask=0,ones=0):
    N=R*B
    vals={value([(a>>i)&1 for i in range(N)],R,B)
          for a in range(1<<N) if a&mask==ones}
    if len(vals)==1:
        return frozenset({(-1,0) if True in vals else (0,-1)})
    opts=set()
    for i in range(N):
        if mask>>i&1:continue
        for left in frontier(R,B,mask|1<<i,ones):
            for right in frontier(R,B,mask|1<<i,ones|1<<i):
                pair=tuple(1+max(v[p] for v in (left,right) if v[p]>=0)
                           for p in (0,1))
                opts.add(pair)
    return frozenset(a for a in opts if not any(b!=a and all(b[p]<=a[p] for p in (0,1)) for b in opts))

def oracle_adversary(R,B,answer):
    status={}
    for i in range(R*B):
        row=i//B
        remaining_row=sum(j not in status for j in range(row*B,(row+1)*B))
        remaining_all=R*B-len(status)
        status[i]=answer if remaining_all==1 else (0 if remaining_row==1 else 1)
        if remaining_all>1:
            p=[status.get(j) for j in range(R*B)]
            assert not value([0 if x is None else x for x in p],R,B)
            assert value([1 if x is None else x for x in p],R,B)
    return value([status[i] for i in range(R*B)],R,B)

def encoded_children(bits,R,B):
    h=(R-1).bit_length()
    assert 1<<h==R
    for b in range(B):
        x=h+b+1
        clauses=[]
        for r in range(R):
            if bits[r*B+b]:continue
            mismatch=[-j-1 if r>>j&1 else j+1 for j in range(h)]
            clauses.extend((mismatch+[x],mismatch+[-x]))
        for r in range(R):
            got=False
            for xb in (0,1):
                a={j+1:(r>>j)&1 for j in range(h)}
                a[x]=xb
                if all(any(a[abs(l)]==(l>0) for l in c) for c in clauses):
                    got=True
            assert got==bool(bits[r*B+b])

if __name__=='__main__':
    comparisons=0
    for R,B in [(1,1),(2,2),(2,3),(3,2)]:
        assert frontier(R,B)==frozenset({(R*B,R*B)})
        comparisons+=1
    for R,B in [(2,2),(2,3),(4,3)]:
        for a in range(1<<(R*B)):
            encoded_children([(a>>i)&1 for i in range(R*B)],R,B)
            comparisons+=R*B
    for R,B in [(1,2),(2,3),(5,4)]:
        for ans in (False,True):
            assert oracle_adversary(R,B,ans)==ans
            comparisons+=1
    masks=[{4},{3},{1},{0,2}]
    for aa,bb in product(range(5),repeat=2):
        d=(bb-aa)%5
        assert sum(d in m for m in masks)==1
        comparisons+=1
    for omit in range(4):
        assert any(all(d not in masks[i] for i in range(4) if i!=omit) for d in range(5))
        comparisons+=1
    runs=[(1,3),(3,1)]
    assert min(t for t,s in runs)<=2 and min(s for t,s in runs)<=2
    assert not any(t<=2 and s<=2 for t,s in runs)
    comparisons+=2
    print(json.dumps({'name':'CLOCKORACLE47_compact','checks':comparisons,'failures':0,
          'scope':'oracle-evasiveness and source-gadget correctness only'}))
