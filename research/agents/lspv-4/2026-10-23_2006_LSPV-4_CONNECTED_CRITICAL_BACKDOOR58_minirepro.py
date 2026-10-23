#!/usr/bin/env python3
"""Independent minimal exact verifier for the connected critical prism CNF.
Stdlib only; run: python3 <thisfile>. Finite audit, not asymptotic proof.
"""
from itertools import product, combinations
import math

def prism(t):
    if t < 3: raise ValueError(t)
    ed=[]
    for i in range(t):
        ed += [tuple(sorted((i,(i+1)%t))),
               tuple(sorted((t+i,t+(i+1)%t))), (i,t+i)]
    assert len(ed)==3*t and len(set(ed))==3*t
    inc=[[] for _ in range(2*t)]
    for j,(u,v) in enumerate(ed,1):
        inc[u].append(j);inc[v].append(j)
    return ed,[sorted(x) for x in inc]

def cnf(t,b):
    ed,inc=prism(t); C=[]
    for v,(x,y,z) in enumerate(inc):
        for a,c in product((0,1),repeat=2):
            d=1 ^ b[v] ^ a ^ c
            C.append(tuple(-e if bit else e for e,bit in zip((x,y,z),(a,c,d))))
    return C,ed,inc

def models(C,n):
    ans=[]
    for bits in product((0,1),repeat=n):
        if all(any((bits[abs(l)-1]==1)==(l>0) for l in clause) for clause in C):
            ans.append(bits)
    return ans

def edgecover(inc,B):
    return all(any(e in B for e in tri) for tri in inc)

tests=0
for t in (3,4):
    for parity in (0,1):
        b=[0]*(2*t);b[0]=parity
        C,ed,inc=cnf(t,b);n=3*t
        exact=models(C,n)
        assert len(exact)==(2**(t+1) if parity==0 else 0);tests+=1
        if parity:
            for i in range(len(C)):
                assert len(models(C[:i]+C[i+1:],n))==2**(t-1)
                tests+=1
        for v in range(2*t):
            b2=b.copy();b2[v]^=1
            C2,_,_=cnf(t,b2)
            changed=[i for i,(old,new) in enumerate(zip(C,C2)) if old!=new]
            assert changed==list(range(4*v,4*v+4))
            assert all(C[i][:2]==C2[i][:2] and C[i][2]==-C2[i][2] for i in changed)
            tests+=1
    _,_,inc=cnf(t,[0]*(2*t))
    for r in range(t):
        assert not any(edgecover(inc,set(S)) for S in combinations(range(1,3*t+1),r))
        tests+=1
    assert edgecover(inc,{3*i+3 for i in range(t)})
    tests+=1
print({"status":"PASS","independent_small_exact_checks":tests,
       "range":"t=3,4; exhaustive original and single-clause deletion counts",
       "larger_instances":"use full Python reproducer in conversation archive"})
