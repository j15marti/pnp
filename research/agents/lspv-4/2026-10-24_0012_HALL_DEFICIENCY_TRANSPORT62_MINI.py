#!/usr/bin/env python3
"""Small independent reproducible Hall/Horn audit; no dependencies."""
import random
from collections import Counter
R=random.Random(202610241047)
def match(cnf):
    adj=[{abs(x) for x in c} for c in cnf]
    owner={}
    def aug(j,seen):
        for v in sorted(adj[j]):
            if v in seen: continue
            seen.add(v)
            if v not in owner or aug(owner[v],seen):
                owner[v]=j
                return True
        return False
    for j in range(len(cnf)):aug(j,set())
    return len(owner)
def deficiency(cnf):
    return len(cnf)-match(cnf)
def lift(cnf,n):
    out=[]
    for j,c in enumerate(cnf):
        assert len(c)==3 and len({abs(x) for x in c})==3
        s=[n+3*j+a+1 for a in range(3)]
        out.append(tuple(s))
        out.extend([(-s[a],c[a]) for a in range(3)])
    return out
def four_degree(cnf):
    d=Counter(abs(x) for c in cnf for x in c)
    return sum(x==4 for x in d.values())
tests=0
for k in range(1000):
    n=R.randint(3,10); m=R.randint(1,min(12,4*n//3))
    cnf=[]; d=Counter()
    for _ in range(15*m+20):
        if len(cnf)>=m:break
        v=R.sample(range(1,n+1),3)
        if any(d[x]>=4 for x in v):continue
        c=tuple(x if R.getrandbits(1) else -x for x in v)
        if c in cnf:continue
        cnf.append(c); d.update(v)
    if not cnf:continue
    h=four_degree(cnf)
    assert deficiency(cnf)==deficiency(lift(cnf,n))
    assert deficiency(cnf)<=h//3
    if h<=2:assert deficiency(cnf)==0
    tests+=1
# Tight sign-balanced SAT example.
C=[(-1,-2,-3),(-1,2,3),(1,-2,3),(1,2,-3)]
assert four_degree(C)==3 and deficiency(C)==1
assert deficiency(lift(C,3))==1
print({"tested_sources":tests,"tight_example_deficiency":1,"failures":0})
