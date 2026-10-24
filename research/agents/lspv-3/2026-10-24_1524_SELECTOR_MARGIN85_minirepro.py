#!/usr/bin/env python3
"""SELECTOR-ARC-MARGIN85: compact independently reproducible checks.
This program is finite arithmetic/semantics only, not an all-input SAT algorithm.
"""
from fractions import Fraction as Q
from itertools import product
import json

checks=0
def ck(cond,message):
    global checks
    checks+=1
    if not cond: raise AssertionError(message)

def curve(c):
    return ((c+2)/c**2-c)/2

def half_forbidden(t):
    return t>1 and (t**3+t**2-t-2)<0

def iterate(K,mu):
    x=Q(K)
    for j in range(97):
        if half_forbidden(x):return j
        x=max(Q(11,10),Q(3,5)+mu+x/2)
    return None

def sat_bruteforce(cnf,n):
    for x in product((0,1),repeat=n):
        if all(any(x[abs(v)-1]==(1 if v>0 else 0) for v in cl) for cl in cnf):
            return True
    return False

def selected(cnf,n):
    # Two fast sound SAT-only witness trials followed by charged exact fallback.
    for guess in ((0,)*n,(1,)*n):
        if all(any(guess[abs(v)-1]==(1 if v>0 else 0) for v in cl) for cl in cnf):
            return True
    return sat_bruteforce(cnf,n)

def main():
    ck(curve(Q(241,200))==Q(11642479,23232400),"FLMV fraction")
    a=Q(12055,10000); b=Q(12056,10000)
    p=lambda t:t**3+t**2-t-2
    ck(p(a)<0<p(b),"critical root bracket")
    stats=[]
    for mu in (Q(0),Q(1,1000),Q(1,500),Q(1,400),Q(1,256),Q(1,100)):
        fixed=Q(6,5)+2*mu
        for K in (2,4,16,100):
            j=iterate(K,mu)
            ck((j is not None)==half_forbidden(fixed),"finite entry criterion")
            stats.append(dict(mu=str(mu),K=K,fixed=str(fixed),iteration=j))
    sat=unsat=0
    for q in range(2,8):
        for eta in product((0,1),repeat=q):
            for endpoint in (0,1):
                cnf=[[1],[q+1 if endpoint else -(q+1)]]
                for i,e in enumerate(eta,1):
                    if e: cnf.extend([[i,i+1],[-i,-(i+1)]])
                    else:cnf.extend([[-i,i+1],[i,-(i+1)]])
                expected=(endpoint==(1^(sum(eta)%2)))
                ck(sat_bruteforce(cnf,q+1)==expected,"independent exact parity-chain label")
                ck(selected(cnf,q+1)==expected,"sound adaptive selector")
                sat+=int(expected);unsat+=int(not expected)
    ck(sat==unsat==252,"matched control balance")
    clauses=[tuple((-1 if ((mask>>j)&1) else 1)*(j+1) for j in range(3)) for mask in range(8)]
    proper_sat=proper_unsat=0
    for bits in product((0,1),repeat=8):
        cnf=[clauses[i] for i in range(8) if bits[i]]
        ans=sat_bruteforce(cnf,3)
        ck(selected(cnf,3)==ans,"8-clause proper3CNF catalogue")
        proper_sat+=int(ans);proper_unsat+=int(not ans)
    print(json.dumps({"id":"SELECTOR-ARC-MARGIN85-mini","status":"COMPUTATIONAL finite controls","checks":checks,"matched_chain_SAT":sat,"matched_chain_UNSAT":unsat,"three_variable_SAT":proper_sat,"three_variable_UNSAT":proper_unsat,"discrepancies":0,"recurrence_samples":stats},indent=2))
if __name__=="__main__":main()
