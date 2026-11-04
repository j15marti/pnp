#!/usr/bin/env python3
"""LSPV-2/394: exhaustive independent CNF padding controls, Python 3.12."""
from itertools import product
import json

pool=[(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
def val(lit,bits): return (bits[abs(lit)-1] == (lit>0))
def bad(F,bits): return sum(not any(val(l,bits) for l in C) for C in F)
def pad(F,r):
    n=max((abs(l) for C in F for l in C),default=0)
    return [C2 for C in F for C2 in [C]+[D for j in range(r) for D in (C+(n+j+1,),C+(-n-j-1,))]],n+r
def minimum(F,n):
    return min(bad(F,b) for b in product([False,True],repeat=n))
def res(a,b,p):
    if not ((p in a and -p in b) or (-p in a and p in b)): raise ValueError("invalid pivot")
    return tuple(sorted((set(a)|set(b))-{p,-p}))
def run():
    checks=0; sat=unsat=0
    for mask in range(256):
        F=[C for i,C in enumerate(pool) if (mask>>i)&1]
        d=minimum(F,2)
        if d: unsat+=1
        else: sat+=1
        for r in (1,2,3):
            H,n=pad(F,r)
            assert len(H)==len(F)*(2*r+1)
            assert len(set(H))==len(H)
            checks+=2
            for b in product([False,True],repeat=n if n>=2 else 2):
                assert bad(H,b)==(r+1)*bad(F,b)
                checks+=1
            # Enumerate all padded assignments, even for SAT cases
            assert minimum(H,max(n,2))==(r+1)*d
            checks+=1
    assert (sat,unsat)==(95,161)
    tri=[(1,2),(-1,-2),(2,3),(-2,-3),(1,3),(-1,-3)]
    proof=list(tri)
    for i,j,p in [(0,5,1),(6,3,2),(1,4,1),(8,2,2),(7,9,3)]:
        proof.append(res(proof[i],proof[j],p))
        checks+=1
    assert proof[-1]==()
    triangle={}
    for r in (1,2,3,4):
        H,n=pad(tri,r)
        assert minimum(H,n)==r+1
        triangle[r]={"clauses":len(H),"repair":r+1}
        checks+=1
    return {"subsets":256,"sat":sat,"unsat":unsat,"pairs":768,"assertions":checks,
            "triangle":triangle,"resolution_paid_steps":5,"status":"COMPUTATIONAL"}
if __name__=="__main__": print(json.dumps(run(),indent=2))
