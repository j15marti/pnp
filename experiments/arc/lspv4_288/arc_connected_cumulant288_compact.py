#!/usr/bin/env python3
"""ARC288 compact no-adjacency extractor. Restricted product-measure moment, NOT SAT solver.
Run in the root of j15marti/pnp. Python logical source reads are counted,
but native FLMV work/index/head tape transitions are NOT instrumented.
"""
import json
from pathlib import Path
from fractions import Fraction as Q
Y = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),
     (-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def src():
    s=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt").read_text()
    return json.loads(s[s.index("[["):s.rindex("]]")+2])
def valid(F,n):
    seen=set(); pos={}; neg={}
    for c in F:
        if len(c)!=3 or any(x==0 or abs(x)>n for x in c):return False
        if len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        for x in c:
            d=pos if x>0 else neg
            d[abs(x)]=d.get(abs(x),0)+1
    return len(F)*3==4*n and all(pos.get(i)==neg.get(i)==2 for i in range(1,n+1))
def overlap(A,B):
    return any(abs(a)==abs(b) for a in A for b in B)
def p(*clauses):
    req={}
    for C in clauses:
        for z in C:
            v=abs(z); need=int(z<0)
            if v in req and req[v]!=need:return Q(0)
            req[v]=need
    return Q(1,2**len(req))
def third(F):
    m=len(F);reads=0;pair_tests=0;third_tests=0;seen_connected=0
    def get(j):
        nonlocal reads
        reads+=1
        return F[j]  # A declared source-query event, NOT a native TM instruction.
    B=Q(0); k3=Q(21*m,256)
    for i in range(m):
        A=get(i)
        for j in range(i+1,m):
            C=get(j);pair_tests+=1
            if not overlap(A,C):continue
            covariance=p(A,C)-Q(1,64)
            B+=covariance
            k3+=Q(9,2)*covariance
            for h in range(m):
                if h==i or h==j:continue
                D=get(h);third_tests+=1
                e1=overlap(A,D);e2=overlap(C,D)
                if not(e1 or e2):continue
                seen_connected+=1
                # Reuse the three records already read. Count each connected triple once.
                edges=[(i,j)]
                if e1:edges.append(tuple(sorted((i,h))))
                if e2:edges.append(tuple(sorted((j,h))))
                if (i,j)!=min(edges):continue
                joint=(p(A,C,D)-Q(1,8)*(p(A,C)+p(A,D)+p(C,D))+Q(1,256))
                k3+=6*joint
    mu=Q(m,8);k2=Q(7*m,64)+2*B
    return {"raw_third":str(mu**3+3*mu*k2+k3),"k2":str(k2),"k3":str(k3),
            "source_clause_query_events":reads,"pair_tests":pair_tests,
            "third_candidate_tests":third_tests,"compatible_edge_anchored_events":seen_connected}
if __name__=="__main__":
    U=src()
    V=[list(C) for C in U];V[1][0],V[7][0]=V[7][0],V[1][0]
    results={}
    for name,F,n in (("Y6_SAT",Y,6),("U198_UNSAT",U,198),("V198_SAT",V,198)):
        assert valid(F,n),(name,"invalid canonical target")
        results[name]=third(F)
    assert results["Y6_SAT"]["raw_third"]=="67/16"
    assert results["U198_UNSAT"]["raw_third"]=="9661629/256"
    assert results["V198_SAT"]["raw_third"]=="4830801/128"
    assert results["U198_UNSAT"]["source_clause_query_events"]==332874
    assert results["V198_SAT"]["source_clause_query_events"]==332874
    print(json.dumps(results,indent=2))
    print("Exact finite checks passed. No native FLMV execution and P versus NP OPEN.")
