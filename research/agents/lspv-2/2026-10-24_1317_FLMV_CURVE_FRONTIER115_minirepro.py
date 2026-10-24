#!/usr/bin/env python3
"""FLMV-CURVE-FRONTIER115: minimal source and exact-rational audit.
Full extended source and raw audit are in the local research package.
Standard library only. Python >=3.10. No arbitrary SAT lower bound claimed.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter
from math import ceil, log2
from random import Random
import json

SEED=202610241317

def beta(c):
    return ((c+2)/c**2-c)/2

def construct(h, unsat):
    edges=list(combinations(range(1,h+1),2))
    M=len(edges); a,b,c,d=(h+M+i for i in range(1,5))
    family=[(x,y,h+i+1) for i,(x,y) in enumerate(edges)]
    rows=[tuple((-v if mask & (1<<i) else v) for i,v in enumerate((a,b,c))) for mask in range(8)]
    core=rows if unsat else rows[:7]+[(a,b,d)]
    return family+core+[(1,a,d)],family,rows

def recognize(clauses):
    if not clauses:return "UNKNOWN"
    n=max(abs(l) for C in clauses for l in C)
    h=n-len(clauses)+5
    if h<3:return "UNKNOWN"
    sat,edge,rows=construct(h,False)
    if n!=h+len(edge)+4 or len(clauses)!=len(sat):return "UNKNOWN"
    d=Counter(clauses)
    for c in edge:
        if d[c]!=1:return "UNKNOWN"
        del d[c]
    a,b,c,_=(h+len(edge)+i for i in range(1,5))
    connector=(1,a,h+len(edge)+4)
    if d[connector]!=1:return "UNKNOWN"
    del d[connector]
    if d==Counter(rows):return "UNSAT"
    if d==Counter(rows[:7]+[(a,b,h+len(edge)+4)]):return "SAT"
    return "UNKNOWN"

def width_lower(h):
    M=h*(h-1)//2
    return next(w for w in range(h+1) if w*(w-1)//2>=M//2)

def run():
    rng=Random(SEED)
    tests=0;table=[]
    assert beta(Q(241,200))==Q(11642479,23232400);tests+=1
    assert beta(Q(6,5))==Q(23,45);tests+=1
    for h in [3,4,5,8,16,32,64,128,256]:
        sat,edge,rows=construct(h,False)
        unsat,_,_=construct(h,True)
        assert recognize(sat)=="SAT" and recognize(unsat)=="UNSAT";tests+=2
        n=max(abs(l) for C in sat for l in C);m=len(sat)
        assert n==h+len(edge)+4 and m==len(edge)+9;tests+=1
        assert all(len(set(map(abs,C)))==3 for C in sat+unsat);tests+=1
        assert all(any(l>0 for l in C) for C in sat);tests+=1
        M=len(edge);rank=width_lower(h)
        samples=[]
        es=set(edge)
        for run_id in range(15):
            arr=list(sat if run_id%2==0 else unsat)
            rng.shuffle(arr)
            seen=0;early=Counter()
            for C in arr:
                if C in es:
                    early[C[0]]+=1; early[C[1]]+=1;seen+=1
                    if seen==M//2:break
            w=sum(0<early[x]<h-1 for x in range(1,h+1))
            assert w>=rank;tests+=1
            assert recognize(arr)==("SAT" if run_id%2==0 else "UNSAT");tests+=1
            samples.append(w)
        record_w=ceil(log2(64*(n+m+1)));N=(4*m+2)*record_w
        table.append([h,n,m,N,rank,min(samples),round(log2(N),4)])
    # Route arithmetic; these statements are conditional on genuine successors.
    routes=[]
    for K in (2,4,8,32,128,1024):
        t=s=Q(K);j=0
        while not (t<Q(241,200) and s<=Q(1,2)):
            t=max(Q(11,10),Q(3,5)+t/2)
            s=max(Q(1,2),s/2)
            j+=1
        assert t<Q(241,200) and s<beta(Q(241,200)); tests+=1
        routes.append([K,j,str(t),str(s)])
    print(json.dumps({"id":"FLMV-CURVE-FRONTIER115-MINI","seed":SEED,
        "checks_passed":tests,"failures":0,
        "cols":["h","n","m","N_bit","proved_w","sampled_min_w","log2_N"],
        "cases":table,"conditional_finite_routes":routes},indent=2))

if __name__=="__main__":run()
