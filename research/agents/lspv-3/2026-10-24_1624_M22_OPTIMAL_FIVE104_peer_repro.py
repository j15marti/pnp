#!/usr/bin/env python3
"""M22-OPTIMAL-FIVE104 independent concise standard-library reproducer."""
from itertools import combinations
from collections import Counter
from json import dumps

V=tuple(range(6))
T=tuple(combinations(V,3))
H=tuple(frozenset(x) for x in combinations(T,4)
        if all(sum(v in t for t in x)==2 for v in V))
def complement(e):return tuple(v for v in V if v not in e)
def opposite(A):return frozenset(complement(e) for e in A)
def sat(P,Q,w):return all(set(c)&set(w) for c in P) and all(not set(c)<=set(w) for c in Q)
def ext(u,v):return [A for A in H if u in A and v in A]
assert len(H)==75
hist=Counter();qhist=Counter()
for P in H:
 for Q in H:
  hist[sum(sat(P,Q,w) for w in T)]+=1
  qhist[len(P-Q)]+=1
  for v in V:
   for bit in (False,True):
    W=tuple(w for w in T if (v in w)==bit)[:5]
    assert len(W)==5 and any(sat(P,Q,w) for w in W)
# Construct an unpaired M22 source falsifying ANY four prescribed balanced words.
for W in combinations(T,4):
 pairs=((W[0],W[1],(W[2],W[3])),
        (W[0],W[2],(W[1],W[3])),
        (W[0],W[3],(W[1],W[2])))
 u,v,(w,z)=next((a,b,other) for a,b,other in pairs
          if len(set(a)&set(b))<=1 or len(set(other[0])&set(other[1]))<=1) if any(
          len(set(a)&set(b))<=1 or len(set(other[0])&set(other[1]))<=1
          for a,b,other in pairs) else pairs[0]
 if len(set(w)&set(z))==2 and len(set(u)&set(v))<=1:
  u,v,w,z=w,z,u,v
 P=opposite(ext(u,v)[0])
 Q=next((B for B in ext(w,z) if B!=P),None)
 assert Q is not None and P!=Q and all(not sat(P,Q,x) for x in W)
pairs=Counter()
for a,b in combinations(T,2):
 r=len(set(a)&set(b));pairs[r]+=1
 assert len(ext(a,b))=={2:1,1:3,0:9}[r]
print(dumps({'families':len(H),'sources':len(H)**2,'target_sources':len(H)**2-len(H),
             'balanced_models':dict(sorted(hist.items())), 'defect_q':dict(sorted(qhist.items())),
             'pair_intersections':dict(sorted(pairs.items())),
             'four_sets_with_target_defeaters':4845,'zero_failures':True},sort_keys=True))
