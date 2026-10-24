#!/usr/bin/env python3
"""SCOPE-CLIQUE-FIREWALL88 independent compact verifier.
Checks both labels, source-name intervals, and disjoint padding.
All-input ARC-EDGE-90 remains OPEN. Standard library only.
"""
from itertools import product
from math import comb
import json

def family(p, sat):
    a,b,c=p+1,p+2,p+3
    head=[(i,j,a) for i in range(1,p+1) for j in range(i+1,p+1)]
    core=[]
    for s in product((1,-1),repeat=3):
        cl=tuple(s[i]*(a,b,c)[i] for i in range(3))
        core.append((-a,b,c) if sat and s==(1,1,1) else cl)
    return head+core

def models(f,n):
    return sum(all(any(bits[abs(l)-1]==(l>0) for l in cl) for cl in f)
               for bits in product((0,1),repeat=n))

def width(order):
    first,last={},{}
    for j,cl in enumerate(order):
        for v in map(abs,cl):
            first.setdefault(v,j);last[v]=j
    return max(sum(first[v]<=j<=last[v] for v in first)
               for j in range(len(order)))

def bitlen(p,g=0):
    n=p+3+3*g;m=comb(p,2)+8+g
    h=(64*(n+m+1)-1).bit_length()
    return (2+4*n+4*m)*h

def run():
    checks=0;rows=[]
    for p in range(2,13):
        for sat in (False,True):
            f=family(p,sat)
            assert len(f)==comb(p,2)+8;checks+=1
            assert len({abs(v) for cl in f for v in cl})==p+3;checks+=1
            for order in [f,f[::-1],f[comb(p,2):]+f[:comb(p,2)]]:
                assert width(order)>=p+1;checks+=1
            X=range(1,p+2)
            assert all(any({i,j}.issubset(set(map(abs,cl))) for cl in f)
                       for i in X for j in X if i<j);checks+=1
            if p<=8:
                assert models(f,p+3)==(p+1 if sat else 0);checks+=1
            assert bitlen(p,p**3)>bitlen(p);checks+=1
            if p<=4:
                for g in (1,2):
                    tail=[(p+4+3*t,p+5+3*t,p+6+3*t) for t in range(g)]
                    assert models(f+tail,p+3+3*g)==(p+1 if sat else 0)*7**g
                    checks+=1
            rows.append([p,'SAT' if sat else 'UNSAT',p+1,bitlen(p)])
    print(json.dumps({'run':'SCOPE-CLIQUE-FIREWALL88-MINI',
                      'status':'PASS','checks':checks,'cases':len(rows),
                      'first':rows[0],'last':rows[-1],
                      'arc':'OPEN','p_vs_np':'OPEN'}))
if __name__=='__main__':run()
