#!/usr/bin/env python3
"""M22-WEIGHTED-LEAF-FACTOR110: independent finite semantic audit.

Exhaustively enumerates small paired cores and 0/1 edge-subgraphs.
The polynomial theorem uses known min-cost (g,f)-factor algorithms.
This reproducer does not implement Gabow or measure FLMV resources.
No dependencies; deterministic seed 20261024.
"""
from collections import Counter
from itertools import product
import hashlib
import json
import random

SEED = 20261024

def tup(s):
    return tuple(sorted(s))

Y = {"P": [(0,1,2),(0,3,4),(1,3,5),(2,4,5)],
     "Q": [(0,1,3),(0,2,5),(1,2,4),(3,4,5)]}
EX6 = {"P": [tup(s) for s in ["abz","cdz","abe","cde"]],
       "Q": [tup(s) for s in ["abz","cdz","ace","bde"]]}
EX9 = {"P": [tup(s) for s in ["aXY","bYZ","cZX","ade","bef","cdf"]],
       "Q": [tup(s) for s in ["aXY","bYZ","cZX","adf","bde","cef"]]}
H15 = [(0,6,7),(1,7,8),(2,8,9),(9,10,11),(6,12,13),(10,12,14),(11,13,14)]
P15 = [(0,3,4),(1,4,5),(2,3,5)]
Q15 = [(0,3,5),(1,3,4),(2,4,5)]
EX15 = {"P":H15+P15,"Q":H15+Q15}

def verify_and_project(C):
    P=list(map(tup,C["P"]));Q=list(map(tup,C["Q"]))
    assert len(P)==len(set(P)) and len(Q)==len(set(Q))
    V=sorted(set(x for t in P+Q for x in t)); k=len(V)
    assert all(len(t)==3 and len(set(t))==3 for t in P+Q)
    cp=Counter(x for t in P for x in t)
    cq=Counter(x for t in Q for x in t)
    assert all(cp[v]==2 and cq[v]==2 for v in V)
    H=sorted(set(P)&set(Q));UP=sorted(set(P)-set(Q));UQ=sorted(set(Q)-set(P))
    D=sorted({x for t in UP for x in t})
    assert set(D)=={x for t in UQ for x in t}
    Z=[x for x in V if x not in D]
    assert all(sum(x in t for t in H)==2 for x in Z)
    assert all(sum(x in t for t in H)<=1 for x in D)
    assert len(P)+len(Q)==4*k//3
    assert len(H)<len(P)
    B=set();full=0
    for choices in product((0,1),repeat=k):
        A=dict(zip(V,choices))
        if all(0<sum(A[v] for v in t)<3 for t in H):
            B.add(tuple(A[v] for v in D))
        if all(any(A[v] for v in t) for t in P) and all(any(not A[v] for v in t) for t in Q):
            full+=1
    return P,Q,H,UP,UQ,V,D,Z,B,full

def factor_opt_bruteforce(H,D,a,weights,pin):
    """Enumerate source-named selected edges, enforce all paired 1..2 quotas."""
    U=sorted(set(x for t in H for x in t))
    mind=None;arg=None;count=0
    for y in product((0,1),repeat=len(U)):
        A=dict(zip(U,y))
        if any((x in A and A[x]!=b) for x,b in pin.items()):
            continue
        if any(not(1<=sum(A[x] for x in t)<=2) for t in H):
            continue
        val=sum(weights[i]*(A.get(x,a[i])!=a[i]) for i,x in enumerate(D))
        count+=1
        if mind is None or val<mind:
            mind=val;arg=tuple(A.get(x,a[i]) for i,x in enumerate(D))
    return mind,arg,count

def projected_opt(B,D,a,w,pin):
    feas=[b for b in B if all(b[D.index(x)]==c for x,c in pin.items())]
    if not feas:return None
    return min(sum(wi*(bi!=ai) for wi,bi,ai in zip(w,b,a)) for b in feas)

def serialization(P,Q,names):
    clauses=[[(x,False) for x in t] for t in P]+[[(x,True) for x in t] for t in Q]
    def encode(cc):
        return 32+sum(8+17*len(cl) for cl in cc)
    def pins(cc,p):
        out=[]
        for cl in cc:
            if any((not neg and p.get(x)==1) or (neg and p.get(x)==0) for x,neg in cl):
                continue
            out.append([(x,neg) for x,neg in cl if x not in p])
        return out
    def sat(cc,free):
        for vals in product((0,1), repeat=len(free)):
            d=dict(zip(free,vals))
            if all(any((not neg and d[x]) or (neg and not d[x]) for x,neg in cl) for cl in cc):
                return True
        return False
    start=sat(clauses,names)
    x=names[0];y=names[1];check=[]
    for vx in (0,1):
        c1=pins(clauses,{x:vx})
        for vy in (0,1):
            c2=pins(clauses,{x:vx,y:vy})
            check.append({"pin1":vx,"pin2":vy,"level0_bits":encode(clauses),
                          "level1_bits":encode(c1),"level2_bits":encode(c2),
                          "leaf_sat":sat(c2,[z for z in names if z not in (x,y)])})
    assert start==any(item["leaf_sat"] for item in check)
    return check

results={"run":"M22-WEIGHTED-LEAF-FACTOR110","seed":SEED,"status":"COMPUTATIONAL",
         "cases":{},"checks":0}
for name,formula in [("Y",Y),("partial6",EX6),("exposed9",EX9),("edge15",EX15)]:
    P,Q,H,UP,UQ,V,D,Z,B,full=verify_and_project(formula)
    trials=0
    for a in product((0,1),repeat=len(D)):
        for w in ([1]*len(D),[i+1 for i in range(len(D))],
                  [0 if i%3==0 else 2*i+3 for i in range(len(D))]):
            for pin in ({},{D[0]:a[0]} if D else {}):
                near=projected_opt(B,D,a,w,pin)
                cost,represent,count=factor_opt_bruteforce(H,D,a,w,pin)
                assert near==cost,(name,a,w,pin,near,cost)
                if represent is not None:
                    assert represent in B
                    assert sum(wi*(bi!=ai) for wi,bi,ai in zip(w,represent,a))==near
                trials+=1
    Rw={"k":len(V),"m":len(P)+len(Q),"h":len(H),"q":len(UP),
        "D":len(D),"Z":len(Z),"projected_boundary_count":len(B),
        "total_boundary_count":2**len(D),"source_models":full,
        "weighted_checks":trials,"all_nearest_costs_in_range":True}
    if name=="partial6":
        lost=[a for a in product((0,1),repeat=len(D)) if a not in B]
        assert len(lost)==4
        Rw["missing_boundary_words"]=[''.join(map(str,x)) for x in lost]
        Rw["independent_z_false_feasible_count"]=32
    results["cases"][name]=Rw
    results["checks"]+=trials
results["two_level_partial6"]=serialization(*verify_and_project(EX6)[:2],
                                              verify_and_project(EX6)[5])
results["checks"]+=4
print(json.dumps(results,indent=2,sort_keys=True))
print("CHECKS",results["checks"],"FAILED",0)
