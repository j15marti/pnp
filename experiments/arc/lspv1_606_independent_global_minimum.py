#!/usr/bin/env python3
"""LSPV-1/606 independently implemented OS-process control for BSEM/RES minima.
Usage: python3 experiments/arc/lspv1_606_independent_global_minimum.py
REFERENCE clause calculi only, not a historical R_mix341 accepted-byte checker.
"""
from collections import deque, Counter
from itertools import product
n=2
clauses=[frozenset((i+1 if v==1 else -(i+1)) for i,v in enumerate(option) if v) for option in product((0,1,-1),repeat=n)]
clauses=sorted(set(clauses),key=lambda c:(len(c),tuple(sorted(c))))
assert len(clauses)==9 and frozenset() in clauses
nonempty=[c for c in clauses if c]
assert len(nonempty)==8
def holds(c,a):
    return any((a[abs(lit)-1]==(lit>0)) for lit in c)
def sem(a,b,c):
    return all(not (holds(a,v) and holds(b,v)) or holds(c,v) for v in product((False,True),repeat=n))
def res(a,b):
    out=set()
    for lit in a:
        if -lit in b:
            c=(a-{lit})|(b-{-lit})
            if not any(-x in c for x in c):out.add(frozenset(c))
    return out
def shortest(source,operator):
    first=frozenset(source)
    q=deque([(first,0)])
    seen={first}
    while q:
        state,d=q.popleft()
        if frozenset() in state:return d
        candidates=set()
        for a in state:
            for b in state:
                if operator=='RES':candidates|=res(a,b)
                else:candidates.update(c for c in clauses if sem(a,b,c))
        for c in candidates-state:
            nxt=frozenset(set(state)|{c})
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt,d+1))
    return None
cnt=Counter()
for mask in range(256):
    F=[c for i,c in enumerate(nonempty) if mask>>i&1]
    sat=any(all(holds(c,v) for c in F) for v in product((False,True),repeat=n))
    a,b=shortest(F,'RES'),shortest(F,'BSEM')
    assert a==b and ((a is None)==sat),(mask,a,b,sat)
    cnt['sat' if sat else 'unsat']+=1
    if not sat:cnt[f'W{a}']+=1
control=0
for a in clauses:
 for b in clauses:
  for c in clauses:
   if not sem(a,b,c):continue
   for u in clauses:
    if not u<=a:continue
    for v in clauses:
     if not v<=b:continue
     control+=1
     assert u<=c or v<=c or any(r<=c for r in res(u,v)),(a,b,c,u,v)
assert control==2393,control
print({'source_subsets':256,'counts':dict(cnt),'semantic_strengthening_controls':control,'mismatches':0,'implementation':'independent Python 3 OS process'})
