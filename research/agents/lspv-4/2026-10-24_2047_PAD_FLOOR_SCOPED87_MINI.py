#!/usr/bin/env python3
"""Independent compact checks for PAD-FLOOR-SCOPED87; stdlib only.
Full event serialization auditor and complete raw results are in the
downloadable archive linked by the report/handoff.
"""
import json

def width(n,m):
    return max(1,(64*(n+m+1)-1).bit_length())

def bitlen(n,m):
    return (2+4*n+4*m)*width(n,m)

def floor(n,m,B):
    assert bitlen(n,m)<=B
    lo,hi=0,1
    while bitlen(n+3*hi,m+hi)<B: hi*=2
    while lo+1<hi:
        md=(lo+hi)//2
        if bitlen(n+3*md,m+md)>=B: hi=md
        else: lo=md
    return hi,bitlen(n+3*hi,m+hi)

def sat(clauses,assignment):
    return all(any(assignment[abs(t)-1] if t>0 else not assignment[-t-1]
                   for t in c) for c in clauses)

def models(clauses,n):
    return sum(sat(clauses,tuple((a>>i)&1 for i in range(n)))
               for a in range(1<<n))

def source(is_sat):
    v=[]
    for b in range(7 if is_sat else 8):
        v.append(tuple(i+1 if not b&(1<<i) else -(i+1)
                       for i in range(3)))
    return v

checks=0
for is_sat in (False,True):
    base=source(is_sat)
    assert models(base,3)==int(is_sat);checks+=1
    for p in (0,1,2):
        clauses=list(base)
        for j in range(p):
            clauses.append((4+3*j,5+3*j,6+3*j))
        assert models(clauses,3+3*p)==int(is_sat)*7**p;checks+=1
    for exponent in (12,16,20,32,48,64,96,160):
        B=1<<exponent
        g,L=floor(3,len(base),B)
        assert B<=L<=2*B+128*(exponent+1);checks+=1
        if g:
            assert bitlen(3+3*(g-1),len(base)+(g-1))<B
            checks+=1
        assert width(3+3*g,len(base)+g)>0;checks+=1
print(json.dumps({"run":"PAD-FLOOR-SCOPED87-MINI",
                  "status":"PASS","checks":checks,
                  "scope":"numerical floors and small independent SAT/UNSAT counts",
                  "NOT":"the unavailable HEREDITARY-SCOPED10 compiler"}))
