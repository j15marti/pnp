#!/usr/bin/env python3
"""Standalone compact parity-moment check, independent of the full producer.
Python 3, no external packages. No native FLMV time/space claim.
"""
from collections import Counter
from math import comb

def prism(h):
    edges=[]
    for layer in (0,1):
        for i in range(h):
            edges.append(tuple(sorted((layer*h+i,layer*h+(i+1)%h))))
    edges += [(i,h+i) for i in range(h)]
    return edges

def original_clauses(edges,charges):
    adj=[[] for _ in charges]
    for i,(u,v) in enumerate(edges,1):
        adj[u].append(i);adj[v].append(i)
    clauses=[]
    for v,ls in enumerate(adj):
        for a in range(8):
            bits=[(a>>t)&1 for t in range(3)]
            if bits[0]^bits[1]^bits[2]^charges[v]:
                clauses.append(tuple(-x if bits[i] else x
                                    for i,x in enumerate(sorted(ls))))
    return clauses

def N0(formula,assignment):
    return sum(not any(((assignment>>(abs(x)-1))&1)==int(x>0)
                       for x in cl) for cl in formula)

def check(q):
    edges=prism(q//2);n=len(edges);base=[0]*q;base[0]=1
    formulas=[];hists=[]
    for label in (0,1):
        charge=base.copy();charge[1]=1-label
        F=original_clauses(edges,charge);formulas.append(F)
        assert len(F)==4*q and all(len(c)==3 for c in F)
        hist=Counter(N0(F,a) for a in range(1<<n));hists.append(hist)
        assert hist[0]==(2**(n-q+1) if label==0 else 0)
        for k in range(q+1):
            assert hist[k]==(comb(q,k)*2**(n-q+1)
                            if k%2==label else 0)
        assert N0(F,0)>0 and N0(F,(1<<n)-1)>0
    assert all(sorted(map(abs,a))==sorted(map(abs,b))
               for a,b in zip(*formulas))
    for r in range(q):
        assert sum(k**r*v for k,v in hists[0].items())==sum(
            k**r*v for k,v in hists[1].items())
    assert sum(k**q*v for k,v in hists[0].items())!=sum(
        k**q*v for k,v in hists[1].items())
    return q,n,hists[0][0],hists[1][0]

if __name__=='__main__':
    for q in (6,8,10,12):
        print('PASS',check(q))
