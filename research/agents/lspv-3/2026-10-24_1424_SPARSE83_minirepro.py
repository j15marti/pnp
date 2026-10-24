#!/usr/bin/env python3
"""SPARSE83 compact peer reproducer. Full 3,178-check audit is a separate local artifact.
Source-generated finite-support tree join; stdlib only, deterministic, no random seeds.
"""
from itertools import product
from math import comb, ceil, log2
import json

checks=0
def ck(c):
    global checks
    checks += 1
    if not c: raise AssertionError(checks)

def states(k,pin=False):
    a=[(0,)*k]
    a += [tuple(int(i==j) for i in range(k)) for j in range(k)]
    return a[1:2] if pin else a

def compat(a,b,eta):
    return (a[0]^b[0])==eta and a[1:]==b[1:]

def join(k, eta):
    q=len(eta)+1
    reached={a:None for a in states(k,True)}
    backs=[]
    for i, e in enumerate(eta):
        layer={}
        for b in states(k,pin=(i+2==q)):
            for a in reached:
                if compat(a,b,e):
                    layer[b]=a
                    break
        backs.append(layer)
        reached=layer
    if not reached:return False,None
    x=next(iter(reached))
    path=[x]
    for layer in reversed(backs):
        x=layer[x]
        path.append(x)
    path.reverse()
    ck(path[0]==(1,)+(0,)*(k-1) and path[-1]==path[0])
    ck(all(compat(path[i],path[i+1],eta[i]) for i in range(len(eta))))
    return True,path

def brute(k,eta):
    q=len(eta)+1
    for row in product(states(k),repeat=q):
        if row[0] not in states(k,True) or row[-1] not in states(k,True):continue
        if all(compat(row[i],row[i+1],eta[i]) for i in range(q-1)):
            return True
    return False

def counts(q,k,h):
    L=k+h
    n=2*q*L+2*q+q*comb(k,2)+2*k*(q-1)+4
    m=4*q*L+2*q*comb(k,2)+4*k*(q-1)+8
    w=ceil(log2(64*(n+m+1)))
    return n,m,(4*m+2)*w

sat=unsat=0
for q in range(2,7):
    for k in range(2,7):
        for bits in product((0,1),repeat=q-1):
            got,witness=join(k,bits)
            expected=(sum(bits)%2==0)
            ck(got==expected)
            ck(got==brute(k,bits) if q<=4 and k<=4 else True)
            if got:sat+=1
            else:unsat+=1
            if witness:ck(witness[0][0]==1)
for k in range(2,39):
    ck(len(states(k))==k+1)
for q in range(2,15):
    for k in range(2,25):
        for h in (1,2,5):
            n,m,N=counts(q,k,h)
            ck(n>0 and m>0 and N>4*m)
n,m,N=counts(128,128,64)
print(json.dumps({"run_id":"SPARSE83_MINI","checks":checks,"SAT":sat,
"UNSAT":unsat,"large_counts":{"n":n,"m":m,"N":N},
"scope":"COMPUTATIONAL; compact peer test, distinct from full 3178-check audit"},sort_keys=True))
