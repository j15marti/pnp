#!/usr/bin/env python3
"""CROSSTAUTO-FORGET320 compact reproducer; no external dependencies.
The full independent verifier, proof leaves and native-like ledgers are in the run archive.
"""
from itertools import product
from collections import Counter

P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
N=((1,2,4),(1,3,5),(2,4,6),(3,5,6))

def make(t):
    out=[]
    for i in range(t):
        b=6*i; nxt=6*((i+1)%t)
        for j,C in enumerate(P):
            out.append(tuple(sorted(nxt+6 if j==2 and v==6 else b+v for v in C)))
        for C in N: out.append(tuple(-v for v in sorted(b+k for k in C)))
    return out

def valid(F):
    n=max(abs(v) for C in F for v in C)
    counts=Counter(l for C in F for l in C)
    return (3*len(F)==4*n and n%3==0 and len({tuple(sorted(C)) for C in F})==len(F)
        and all(len(C)==3 and len({abs(v) for v in C})==3
                and (all(v>0 for v in C) or all(v<0 for v in C)) for C in F)
        and all(counts[i]==counts[-i]==2 for i in range(1,n+1)))

def evalf(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in C) for C in F)

def ticket(F,x):
    pos=[C for C in F if x in C]; neg=[C for C in F if -x in C]
    return len(pos)==len(neg)==2 and all(
        bool((set(map(abs,A))-{x})&(set(map(abs,B))-{x}))
        for A in pos for B in neg)

def test(t):
    F=make(t); assert valid(F)
    pivots=[6*i+1 for i in range(t)]
    assert all(ticket(F,x) for x in pivots)
    H=[C for C in F if all(abs(l) not in pivots for l in C)]
    if t>3: return {"t":t,"n":6*t,"m":len(F),"eliminated":t,"remaining":len(H)}
    rest=[v for v in range(1,6*t+1) if v not in pivots]
    cs=0;mc=0
    for bv in product((0,1),repeat=len(rest)):
        z=dict(zip(rest,bv)); h=evalf(H,z)
        count=sum(evalf(F,{**z,**dict(zip(pivots,bx))})
                    for bx in product((0,1),repeat=t))
        assert h==(count>0)
        cs+=int(h); mc+=count
    return {"t":t,"n":6*t,"m":len(F),"eliminated":t,
            "remaining":len(H),"satisfying_boundary_states":cs,
            "original_models":mc}

if __name__=="__main__":
    for k in (1,2,3,4,8,16):print(test(k))
