#!/usr/bin/env python3
"""PAIR-CAMOUFLAGE1: full pair-orbit exact-layer 3-SAT experiment."""
from __future__ import annotations
from itertools import combinations
from math import comb
import random, statistics

Q_VALUES=(20,24,28,32)
N=4000
DENSITY=3.5
BASE_SEED=8000
ORBITS=((0,0),(1,0),(1,1),(2,0),(2,1),(2,2),(3,1),(3,2),(3,3))

def gen_clause(q,rng):
    vs=rng.sample(range(q),3)
    return tuple(sorted(((v+1) if rng.getrandbits(1) else -(v+1) for v in vs),key=abs))

def gen_formula(q,t,rng):
    s=set()
    while len(s)<t: s.add(gen_clause(q,rng))
    return tuple(s)

def simplify(cs,var,val):
    tl=var if val else -var; fl=-tl; out=[]
    for c in cs:
        if tl in c: continue
        if fl in c:
            nc=tuple(x for x in c if x!=fl)
            if not nc: return None
            out.append(nc)
        else: out.append(c)
    return tuple(out)

def dpll_sat(cs):
    def rec(cs):
        while True:
            if not cs: return True
            u=next((c[0] for c in cs if len(c)==1),None)
            if u is None: break
            cs=simplify(cs,abs(u),u>0)
            if cs is None: return False
        pol={}
        for c in cs:
            for l in c: pol[abs(l)]=pol.get(abs(l),0)|(1 if l>0 else 2)
        for v,m in pol.items():
            if m in (1,2):
                z=simplify(cs,v,m==1)
                return z is not None and rec(z)
        l=min(cs,key=len)[0]; v=abs(l)
        a=simplify(cs,v,l>0)
        if a is not None and rec(a): return True
        b=simplify(cs,v,l<0)
        return b is not None and rec(b)
    return rec(tuple(cs))

def pair_vector(F):
    out={o:0 for o in ORBITS}
    for a,b in combinations(F,2):
        da={abs(x):x>0 for x in a}; db={abs(x):x>0 for x in b}
        shared=set(da)&set(db)
        key=(len(shared),sum(da[v]!=db[v] for v in shared))
        out[key]+=1
    return tuple(out[o] for o in ORBITS)

def expected_vector(q,t):
    M=8*comb(q,3)
    theta=t*(t-1)/(M*(M-1))
    ans=[]
    for s,h in ORBITS:
        n=comb(3,s)*comb(q-3,3-s)*2**(3-s)*comb(s,h)
        ans.append(M*n*theta/2)
    return tuple(ans)

def main():
    print("PAIR-CAMOUFLAGE1")
    for q in Q_VALUES:
        t=round(DENSITY*q); rng=random.Random(BASE_SEED+q)
        sat=[]; unsat=[]
        for _ in range(N):
            f=gen_formula(q,t,rng); v=pair_vector(f)
            (sat if dpll_sat(f) else unsat).append(v)
        ev=expected_vector(q,t); allv=sat+unsat
        print(f"q={q} t={t} N={N} UNSAT={len(unsat)}")
        for j,o in enumerate(ORBITS):
            ms=statistics.mean(x[j] for x in sat)
            mu=statistics.mean(x[j] for x in unsat)
            ma=statistics.mean(x[j] for x in allv)
            sd=statistics.stdev(x[j] for x in allv)
            z=(mu-ma)/sd if sd else 0.0
            print(f"orbit={o} E0={ev[j]:.8f} SATminusE0={ms-ev[j]:.8f} "
                  f"UNSATminusE0={mu-ev[j]:.8f} UminusS={mu-ms:.8f} U_z_all={z:.8f}")
    print("STATUS=PASS")
if __name__=="__main__":
    main()
