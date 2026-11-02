#!/usr/bin/env python3
"""GATE318 no-producer-import independent control checker. Stdlib only."""
from itertools import product,combinations
from collections import Counter
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-v for v in c) for c in M)
def sat(F,a):return all(any((l>0)==bool(a[abs(l)]) for l in c) for c in F)
def count(F,p):
 n=max(abs(v) for c in F for v in c)
 free=[v for v in range(1,n+1) if v not in p]
 return sum(sat(F,{**p,**dict(zip(free,t))}) for t in product((0,1),repeat=len(free)))
assert count(F,{})==70
assert count(F,{1:1,2:0,5:1,6:1})==1
assert count(F,{8:0,3:0,7:0,6:0,1:1,5:1})==0
checks=0
for i,j in combinations(range(len(F)),2):
 p,q=F[i],F[j]
 same=bool(set(p)&set(q));opposite=bool(set(p)&{-v for v in q})
 for sa,sb,expected in ((1,1,not opposite),(1,0,not same),(0,1,not same),(0,0,not opposite)):
  need={};ok=True
  for clause,target in ((p,sa),(q,sb)):
   for l in clause:
    val=int((l>0)==bool(target))
    if abs(l) in need and need[abs(l)]!=val:ok=False
    need[abs(l)]=val
  assert ok==expected;checks+=1
assert checks==264
def C1():
 return ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
         (-1,-2,-4),(-1,-3,-5),(-2,-4,-6),(-3,-5,-6))
C=C1()
assert count(C,{2:0,4:0,3:1,5:0})==1
assert count(C,{2:0,4:0,3:1,5:1})==0
assert count(C,{})==22
# For all 32 assignments of (a,b,c,d,e), zero-cross x-projection is exact.
H=tuple(c for c in C if 1 not in c and -1 not in c)
for bits in product((0,1),repeat=5):
 a=dict(zip((2,3,4,5,6),bits))
 assert sat(H,a)==(sat(C,{**a,1:0}) or sat(C,{**a,1:1}))
# Independently test exact F9 DP projection after each of pivots 1,2,9.
now=[frozenset(c) for c in F];elapsed=[]
for x in (1,2,9):
 plus=[c for c in now if x in c];minus=[c for c in now if -x in c]
 new={c for c in now if x not in c and -x not in c}
 for a in plus:
  for b in minus:
   r=(a-{x})|(b-{-x})
   if not any(-v in r for v in r):new.add(r)
 now=list(new);elapsed.append(x)
 rest=sorted({abs(v) for c in now for v in c})
 for v in product((0,1),repeat=len(rest)):
  a=dict(zip(rest,v))
  h=all(any((l>0)==bool(a[abs(l)]) for l in c) for c in now)
  source=any(sat(F,{**a,**dict(zip(elapsed,u))}) for u in product((0,1),repeat=len(elapsed)))
  assert h==source
print({"status":"PASS","F9_source_S_U_modes":checks,"C1_both_labels":(1,0),
       "F9_DP_counts":"12-11-10-11","P_vs_NP":"OPEN"})
