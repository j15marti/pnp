#!/usr/bin/env python3
"""Small stdlib reproducer of two restricted signed-hypergraph identities.
Not a general SAT solver, hereditary compressor, or native FLMV experiment.
"""
from itertools import combinations, product
from collections import Counter

gray=(0,1,3,2)
P15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=P15+[tuple(-x for x in c) for c in N15]

def state(F,p):
 n=max(abs(l) for c in F for l in c);out=0;s=0
 def push(a):
  nonlocal s,out
  out|=a<<s;s+=2
 for v in range(1,n+1):push(0 if v not in p else (1 if p[v]==0 else 2))
 for c in F:
  t=sum(abs(l) in p and p[abs(l)]==int(l>0) for l in c)
  u=sum(abs(l) not in p for l in c)
  push(gray[t]);push(gray[u]);push(1 if t else 2 if not u else 0)
 return out

def trace(F,a,order):
 p={};z=state(F,p);total=0
 for v in order:
  p[v]=a[v];q=state(F,p);total+=(z^q).bit_count();z=q
 return total

def models(F,p={}):
 free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in p]
 for bits in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  if all(any(a[abs(l)]==int(l>0) for l in c) for c in F):yield a

def gate(F,p,cycles):
 uncovered=[j for j,c in enumerate(F) if not any(abs(l) in p and p[abs(l)]==int(l>0) for l in c)]
 free=[v for v in range(1,16) if v not in p]
 covered=set(range(len(F)))-set(uncovered);s=Counter()
 for j in covered:
  for l in F[j]:
   if abs(l) not in p:s[abs(l),l>0]+=1
 for tri in cycles:
  vs=Counter()
  assert len(set(tri))==3 and all(j in uncovered for j in tri)
  for j in tri:
   rest=[abs(l) for l in F[j] if abs(l) not in p]
   assert len(rest)==2
   vs.update(rest)
  assert len(vs)==3 and set(vs.values())=={2}
 assert len({j for c in cycles for j in c})==3*len(cycles)
 eta=sum(min(s[v,True],s[v,False]) for v in free)
 delta=2*len(free)-len(uncovered)-eta-len(cycles)
 return delta

trips=list(combinations(range(1,7),3))
sets=[s for s in combinations(trips,4) if all(sum(v in c for c in s)==2 for v in range(1,7))]
assert len(sets)==75
cases=0
for P in sets:
 for N in sets:
  F=list(P)+[tuple(-x for x in c) for c in N]
  for a in ({v:0 for v in range(1,7)},{v:v%2 for v in range(1,7)}):
   for order in (list(range(1,7)),list(range(6,0,-1))):
    assert trace(F,a,order)==50
    cases+=1
assert cases==22500
pU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
pS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
assert gate(F15,pU,[(0,1,11),(2,3,14)])==-1
assert gate(F15,pS,[(1,10,11),(2,3,14)])==0
assert sum(1 for _ in models(F15,pU))==0
assert sum(1 for _ in models(F15,pS))==2
assert sum(1 for _ in models(F15))==1032
assert trace(F15,next(models(F15)),list(range(1,16)))==125
assert trace(F15,{v:0 for v in range(1,16)},list(range(1,16)))==125
print({'canonical_n6':75**2,'complete_traces':cases,'F15_models':1032,'cube_models':[0,2], 'gray_F15':125,'P_vs_NP':'OPEN'})
