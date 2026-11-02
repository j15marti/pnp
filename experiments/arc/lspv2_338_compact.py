#!/usr/bin/env python3
"""LSPV-2 GRID338 compact reproducibility check. Python >=3.10; no dependencies.
This constructs an explicit canonical family, not a universal SAT solver.
Full independent verifier and source/circuit controls are in the dated run archive.
"""
import json, math
from collections import Counter

def make(q):
    assert q >= 3 and q % 3 == 0
    n=q*q; k=n//3
    edges=[]
    for i in range(k):
        edges.extend([(i,(i+1)%k),(k+i,k+(i+1)%k),(i,k+i)])
    lookup={frozenset(e):j for j,e in enumerate(edges)}
    cv=list(range(k))+list(range(2*k-1,k-1,-1))
    cycle=[lookup[frozenset((cv[i],cv[(i+1)%(2*k)]))] for i in range(2*k)]
    spare=set(range(n))-set(cycle)
    chosen={}
    for e in spare:
        if e%3==2: v=e//3
        else: v=edges[e][0]
        assert v not in chosen
        chosen[v]=e
    path=[]
    for i,v in enumerate(cv):
        if v in chosen: path.append(chosen[v])
        path.append(cycle[i])
    assert len(path)==n and len(set(path))==n
    for a,b in zip(path,path[1:]):
        assert set(edges[a]) & set(edges[b])
    posmap={e:i+1 for i,e in enumerate(path)}
    negmap={e:(i%q)*q+(i//q)+1 for i,e in enumerate(path)}
    P=[[] for _ in range(2*k)]; M=[[] for _ in range(2*k)]
    for e,(a,b) in enumerate(edges):
        for v in (a,b):
            P[v].append(posmap[e]);M[v].append(-negmap[e])
    F=[sorted(c) for c in P]+[sorted(c,key=abs) for c in M]
    ring=[3*i+j for i in range(k) for j in range(3)]
    return F,[posmap[e] for e in ring],[negmap[e] for e in ring]

def valid(F,n):
    if len(F)*3!=4*n:return False
    counts=Counter()
    keys=set()
    for c in F:
        if len(c)!=3 or any(type(x)!=int or x==0 or abs(x)>n for x in c):return False
        if len(set(map(abs,c)))!=3 or len(set(x>0 for x in c))!=1:return False
        key=tuple(sorted(c))
        if key in keys:return False
        keys.add(key);counts.update(c)
    return all(counts[i]==counts[-i]==2 for i in range(1,n+1))

def frontier(F,order,sign=0):
    S=set();maximum=0
    for v in order:
        S.add(v)
        maximum=max(maximum,sum(0<sum(abs(x) in S for x in c)<3
            for c in F if not sign or (c[0]>0)==(sign>0)))
    return maximum

def evaluate(F,assignment):
    return all(any(assignment[abs(x)-1]==(x>0) for x in c) for c in F)

def check(q):
    F,po,no=make(q);n=q*q
    assert valid(F,n)
    wp=frontier(F,po,1);wn=frontier(F,no,-1)
    assert wp<=6 and wn<=6
    for r in range(q):
        for c in range(q):
            a=r*q+c+1
            if c+1<q:
                assert any(x[0]>0 and a in x and a+1 in x for x in F)
            if r+1<q:
                assert any(x[0]<0 and -a in x and -(a+q) in x for x in F)
    witness=[bool((r+c)%2) for r in range(q) for c in range(q)]
    if q%2:assert evaluate(F,witness)
    return dict(q=q,n=n,m=len(F),signed_widths=[wp,wn],
        proven_joint_width_lower_bound=(q+1)//2,
        checkerboard_is_sat=evaluate(F,witness),
        private_fanin2_gates=3*len(F)-1)

if __name__=="__main__":
    print(json.dumps([check(q) for q in [3,6,9,12,15,24,36]],indent=2))
