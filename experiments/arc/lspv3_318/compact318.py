#!/usr/bin/env python3
"""GATE318 compact reproducer. Stdlib only. P versus NP OPEN."""
from itertools import product
from collections import Counter

POS9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
NEG9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=tuple(POS9)+tuple(tuple(-z for z in c) for c in NEG9)

def canonical(F):
    if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3
                    or len({z>0 for z in c})!=1 for c in F): return False
    n=max(abs(z) for c in F for z in c)
    q=Counter((abs(z),z>0) for c in F for z in c)
    return len(F)*3==4*n and len({tuple(sorted(c)) for c in F})==len(F) and all(q[i,False]==q[i,True]==2 for i in range(1,n+1))

def C(t):
    F=[]
    for i in range(t):
        x,a,b,c,d,e=range(6*i+1,6*i+7); en=6*((i+1)%t)+6
        F += [(x,a,b),(x,c,d),(a,c,en),(b,d,e),
              (-x,-a,-c),(-x,-b,-d),(-a,-c,-e),(-b,-d,-e)]
    return tuple(F)

def zero(R,x):
    P=[c for c in R if x in c]; N=[c for c in R if -x in c]
    for c in P:
        for d in N:
            a=[v for v in c if v!=x]; b=[v for v in d if v!=-x]
            if not any(-v in b for v in a): return False
    return True

def kernel(R, reverse=False):
    R=list(R); piv=[]
    while True:
        eligible=[x for x in sorted({abs(v) for c in R for v in c},reverse=reverse) if zero(R,x)]
        if not eligible:return R,piv
        x=eligible[0]; piv.append(x)
        R=[c for c in R if x not in c and -x not in c]

def count(F,p):
    n=max(abs(z) for c in F for z in c)
    free=[i for i in range(1,n+1) if i not in p]
    return sum(all(any((v>0)==bool(a[abs(v)]) for v in c) for c in F)
        for t in product((0,1),repeat=len(free))
        for a in [{**p,**dict(zip(free,t))}])

def dp(R,x):
    P=[c for c in R if x in c]; N=[c for c in R if -x in c]
    Q={frozenset(c) for c in R if x not in c and -x not in c}
    for p in P:
        for n in N:
            z=frozenset(set(p)-{x}|(set(n)-{-x}))
            if not any(-l in z for l in z):Q.add(z)
    return [tuple(z) for z in Q]

def torus(k):
    inc={}; idx=0
    def edge(u,v):
        nonlocal idx
        idx+=1
        inc.setdefault(u,[]).append(idx);inc.setdefault(v,[]).append(idx)
    for i in range(k):
        for j in range(k):
            for a,b in ((0,1),(1,2),(2,3),(3,0)):
                edge((i,j,a),(i,j,b))
            edge((i,j,1),(i,(j+1)%k,3))
            edge((i,j,2),((i+1)%k,j,0))
    P=[tuple(inc[v]) for v in sorted(inc)]
    return tuple(P)+tuple(tuple(-z for z in c) for c in P)

assert canonical(F9)
assert count(F9,{})==70
assert count(F9,{1:1,2:0,5:1,6:1})==1
assert count(F9,{8:0,3:0,7:0,6:0,1:1,5:1})==0
sizes=[len(F9)]; R=list(F9)
for x in (1,2,9):
    R=dp(R,x); sizes.append(len(R))
assert sizes==[12,11,10,11]
for t in (1,2,3,4,8,16):
    F=C(t);assert canonical(F)
    K,piv=kernel(F); assert len(K)==0
    assert len(kernel(F,reverse=True)[0])==0
    # Independent explicit 3t witness-free projection sequence.
    Q=list(F)
    for i in range(t):
        for x in (6*i+1,6*i+2,6*i+3):
            assert zero(Q,x)
            Q=[c for c in Q if x not in c and -x not in c]
    assert not Q
for k in (4,6,8):
    F=torus(k);assert canonical(F)
    K,piv=kernel(F);assert not piv and len(K)==len(F)
print({"status":"PASS","C_t":"all clauses eliminated in 3t tickets",
       "torus":"k=4,6,8 zero eligible pivots","F9_DP_growth":sizes,
       "F9_both_labels":(1,0),"P_vs_NP":"OPEN"})
