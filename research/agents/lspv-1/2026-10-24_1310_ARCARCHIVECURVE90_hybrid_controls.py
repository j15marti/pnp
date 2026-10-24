#!/usr/bin/env python3
"""Finite SAT/UNSAT controls, not an unrestricted SAT lower bound.

Paid observed grammar: 2SAT -> SCC, sound complementary ternary pairs ->
SCC, otherwise exhaustive exact fallback. Python standard library.
"""
import json, random
from itertools import product

def eval_formula(formula,bits):
    return all(any(bits[abs(v)-1]==(v>0) for v in c) for c in formula)
def brute(formula,n):
    for j,bits in enumerate(product((False,True),repeat=n),1):
        if eval_formula(formula,bits): return True,j
    return False,2**n
def two_sat(formula,n):
    edges=[[] for _ in range(2*n)];rev=[[] for _ in range(2*n)]
    def idx(v):return 2*(abs(v)-1)+(0 if v>0 else 1)
    def edge(a,b):
        u,v=idx(-a),idx(b);edges[u].append(v);rev[v].append(u)
    for c in formula:
        if not c:return False
        if len(c)>2:raise ValueError("nonbinary")
        a,b=(c[0],c[0]) if len(c)==1 else c
        edge(a,b);edge(b,a)
    seen=set();order=[]
    def dfs(u):
        seen.add(u)
        for v in edges[u]:
            if v not in seen:dfs(v)
        order.append(u)
    for u in range(2*n):
        if u not in seen:dfs(u)
    comp=[-1]*(2*n)
    def rdfs(u,k):
        comp[u]=k
        for v in rev[u]:
            if comp[v]<0:rdfs(v,k)
    k=0
    for u in reversed(order):
        if comp[u]<0:rdfs(u,k);k+=1
    return all(comp[2*i]!=comp[2*i+1] for i in range(n))
def contract(formula):
    rem=list(formula);new=[];paired=0
    while rem:
        c=rem.pop(0)
        if len(c)<=2:new.append(c);continue
        if len(c)!=3:return None,paired
        target=None
        for j,d in enumerate(rem):
            if len(d)!=3:continue
            common=set(c)&set(d)
            if len(common)==2 and len(set(c)-common)==1 and len(set(d)-common)==1:
                a=next(iter(set(c)-common));b=next(iter(set(d)-common))
                if a==-b:target=(j,tuple(sorted(common)));break
        if target is None:return None,paired
        j,short=target
        rem.pop(j);new.append(short);paired+=1
    return new,paired
def hybrid(formula,n):
    if all(len(c)<=2 for c in formula):
        return two_sat(formula,n),"SCC"
    projected,pairs=contract(formula)
    if projected is not None:
        return two_sat(projected,n),"PAIR_TO_SCC"
    return brute(formula,n)[0],"EXACT_FALLBACK"

def parity_quartet(rhs):
    return [[(i+1)*(-1 if b else 1) for i,b in enumerate(bits)]
            for bits in product((0,1),repeat=3)
            if (sum(1-b for b in bits)%2)!=rhs]

cases=[("2sat_yes",2,[[1,2],[-1,2]]),
       ("2sat_no",1,[[1],[-1]]),
       ("pair_yes",3,[[1,2,3],[1,2,-3]]),
       ("pair_no",3,[[1,2,3],[1,2,-3],[-1],[-2]]),
       ("all_8_no",3,[[((i+1)*(-1 if b else 1)) for i,b in enumerate(bits)]
                           for bits in product((0,1),repeat=3)]),
       ("xor_even",3,parity_quartet(0)),
       ("xor_odd",3,parity_quartet(1))]
rng=random.Random(20261024)
for i in range(100):
    n=rng.randrange(2,8);m=rng.randrange(1,15);form=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1), min(n,rng.randrange(1,4)))
        form.append([v if rng.randrange(2) else -v for v in vs])
    cases.append((f"random_{i}",n,form))
counts={};labels={"SAT":0,"UNSAT":0}
for name,n,form in cases:
    expected,attempts=brute(form,n)
    actual,rule=hybrid(form,n)
    assert expected==actual,(name,n,form)
    counts[rule]=counts.get(rule,0)+1
    labels["SAT" if expected else "UNSAT"]+=1
assert counts=={"SCC":35,"PAIR_TO_SCC":5,"EXACT_FALLBACK":67}
assert labels=={"SAT":46,"UNSAT":61}
print(json.dumps({"run":"ARCARCHIVECURVE90","status":"COMPUTATIONAL",
                  "seed":20261024,"checked_cases":len(cases),
                  "labels":labels,"rule_counts":counts,
                  "scope":"Restricted finite adaptive portfolio, no all-decider coverage"},indent=2))
