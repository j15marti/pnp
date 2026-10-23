#!/usr/bin/env python3
"""SOUND-EXTENSION67 minimal standard-library proof-system quickcheck.
Finite testing only. Asymptotic regular-resolution lower bounds are cited.
"""
from itertools import combinations,product

def graph(name):
    if name=="K4": return 4,list(combinations(range(4),2))
    if name=="prism":
        return 6,[(i,(i+1)%3) for i in range(3)]+[(i+3,(i+1)%3+3) for i in range(3)]+[(i,i+3) for i in range(3)]
    raise ValueError(name)

def make_tseitin(g,edges,charge):
    inc=[[] for _ in range(g)]
    for z,(u,v) in enumerate(edges,1):
        inc[u].append(z); inc[v].append(z)
    assert all(len(x)==3 for x in inc)
    cnf=[]
    for v,tri in enumerate(inc):
        tri=sorted(tri)
        for a in product((0,1),repeat=3):
            if sum(a)%2!=charge[v]:
                cnf.append(tuple(-z if bit else z for z,bit in zip(tri,a)))
    return cnf

def recognize(cnf):
    if not cnf or len(cnf)%4:return False
    g=len(cnf)//4
    inc={}; edges=[]; charges=[]
    for v in range(g):
        block=cnf[4*v:4*v+4]
        if any(len(c)!=3 or len({abs(l) for l in c})!=3 for c in block):return False
        tri=tuple(sorted(abs(l) for l in block[0]))
        if any(tuple(sorted(abs(l) for l in c))!=tri for c in block):return False
        wrong={tuple(int(next(l for l in c if abs(l)==z)<0) for z in tri) for c in block}
        ch=[b for b in (0,1) if wrong=={a for a in product((0,1),repeat=3) if sum(a)%2!=b}]
        if len(ch)!=1:return False
        charges.append(ch[0])
        for z in tri:inc.setdefault(z,[]).append(v)
    if len(inc)!=3*g//2 or set(inc)!=set(range(1,3*g//2+1)):return False
    if any(len(q)!=2 or q[0]==q[1] for q in inc.values()):return False
    edges=[tuple(sorted(q)) for q in inc.values()]
    if len(set(edges))!=len(edges):return False
    adj=[set() for _ in range(g)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    seen={0};pending=[0]
    for u in pending:
        for v in adj[u]:
            if v not in seen: seen.add(v);pending.append(v)
    return len(seen)==g and sum(charges)%2==1

def resolution_verify(cnf,steps):
    lines=[set(c) for c in cnf]
    for i,j,p in steps:
        if not (0<=i<len(lines) and 0<=j<len(lines) and p):return False
        a,b=lines[i],lines[j]
        if p in a and -p in b:s=(a-{p})|(b-{-p})
        elif -p in a and p in b:s=(a-{-p})|(b-{p})
        else:return False
        if any(-u in s for u in s):return False
        lines.append(s)
    return bool(steps) and not lines[-1]

def resolution_proof(cnf):
    lines=[set(c) for c in cnf];seen={frozenset(c) for c in lines};steps=[]
    while True:
        changed=False
        for i in range(len(lines)):
            for j in range(i+1,len(lines)):
                for p in sorted(lines[i],key=lambda x:(abs(x),x)):
                    if -p not in lines[j]:continue
                    s=(lines[i]-{p})|(lines[j]-{-p})
                    if any(-x in s for x in s):continue
                    if frozenset(s) in seen:continue
                    seen.add(frozenset(s)); lines.append(s);steps.append((i,j,p));changed=True
                    if not s:return steps
        if not changed:raise AssertionError("no refutation")

def models(n,cnf):
    return sum(all(any(bits[abs(l)-1]==(l>0) for l in c) for c in cnf) for bits in product((0,1),repeat=n))

if __name__=="__main__":
    for name in ("K4","prism"):
        g,edges=graph(name)
        for parity in (0,1):
            f=make_tseitin(g,edges,(parity,)+(0,)*(g-1))
            assert recognize(f)==bool(parity)
            assert models(len(edges),f)==(0 if parity else 2**(len(edges)-g+1))
            bad=list(f);bad[0]=(-bad[0][0],)+bad[0][1:]
            assert not recognize(bad)
    cnf=[tuple(-i if b else i for i,b in enumerate(bits,1)) for bits in product((0,1),repeat=3)]
    assert models(3,cnf)==0 and not recognize(cnf)
    proof=resolution_proof(cnf)
    assert resolution_verify(cnf,proof)
    corrupt=list(proof);corrupt[-1]=(corrupt[-1][0],corrupt[-1][1],999)
    assert not resolution_verify(cnf,corrupt)
    print({"paired_cases":4,"resolution_steps":len(proof),"failures":0})
