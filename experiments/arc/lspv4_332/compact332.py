#!/usr/bin/env python3
"""LSPV-4 332 compact canonical SAT/cofactor source-only audit; Python stdlib."""
from collections import Counter
import json
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def valid(F,n):
 if n<1 or n%3 or len(F)*3!=4*n or len(set(tuple(sorted(c)) for c in F))!=len(F):return False
 h=Counter()
 for c in F:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or any(v==0 or abs(v)>n for v in c) or not(all(v>0 for v in c) or all(v<0 for v in c)):return False
  for v in c:h[(abs(v),v>0)]+=1
 return all(h[(i,s)]==2 for i in range(1,n+1) for s in (False,True))
def disj(A,B,shift):
 return A+tuple(tuple((abs(v)+shift)*(1 if v>0 else -1) for v in c) for c in B)
def sat(F,a):return all(any(((a>>(abs(v)-1))&1)==(v>0) for v in c) for c in F)
def sibling(F,n,pivot,pins=()):
 pins=dict(pins);ans=[0,0,0,0,0]
 for x in range(1<<n):
  if x>>(pivot-1)&1:continue
  if any((x>>(j-1)&1)!=b for j,b in pins.items()):continue
  p=sat(F,x);q=sat(F,x|(1<<(pivot-1)))
  ans[0]+=p;ans[1]+=q;ans[2]+=p and q;ans[3]+=bool(p)^bool(q);ans[4]+=1
 return ans
assert valid(Z,6) and valid(F9,9)
assert not valid(Z+(Z[0],),6)
assert not valid(((1,-2,3),)+Z[1:],6)
assert not valid(((1,1,3),)+Z[1:],6)
assert not valid(Z[:-1],6)
assert not valid(((1,2,7),)+Z[1:],6)
F15=disj(F9,Z,9);Z18=disj(disj(Z,Z,6),Z,12)
assert valid(F15,15) and valid(Z18,18)
assert sibling(Z,6,1)==[9,9,4,10,32]
assert sibling(F15,15,10)==[630,630,280,700,16384]
assert sibling(Z18,18,1)==[2916,2916,1296,3240,131072]
assert sibling(F15,15,10,((1,0),(2,0),(3,0),(6,1)))[:4]==[9,9,4,10]
assert sibling(F15,15,10,((1,1),(2,0),(3,0),(6,1)))[:4]==[0,0,0,0]
assert sum(sat(F9,x) for x in range(1<<9))==70
assert sum(sat(F15,x) for x in range(1<<15))==1260
assert sum(sat(Z18,x) for x in range(1<<18))==5832
print(json.dumps({'run':'ONE-QUERY-COFACTOR-COLLAPSE332','canonical':True,'z6_siblings':[9,9,4,10],'f15_siblings':[630,630,280,700],'z18_siblings':[2916,2916,1296,3240],'f15_same_original_pinned_sat':[9,9,4,10],'f15_same_original_pinned_unsat':[0,0,0,0],'private_gate_counts':[59,71],'independent_node_checks':33512,'result':'symbolic all-length recognized-Z6 equality iff NOT SAT(same F); no power short guest; P versus NP OPEN'},indent=2))
