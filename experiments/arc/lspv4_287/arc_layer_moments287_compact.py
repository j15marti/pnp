#!/usr/bin/env python3
"""Compact ARC287. For U/V checks place U_source.json, V_witness.json from ZIP here."""
import math,json
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction as Q
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def sat(F,a):
 return all(any((a[abs(z)-1]==1)==(z>0) for z in C) for C in F)
def sig(F):
 s=Counter()
 for i,A in enumerate(F):
  for B in F[i+1:]:
   signs=''.join(sorted(('+' if A[0]>0 else '-')+('+' if B[0]>0 else '-')))
   overlap=len(set(map(abs,A)) & set(map(abs,B)))
   s[(signs,overlap)]+=1
 return s
def fall(a,k):
 return math.prod(range(a-k+1,a+1)) if 0<=k<=a else 0
def mean(n,w,r):
 m=4*n//3
 return Q(m*math.comb(3,r)*(fall(w,r)*fall(n-w,3-r)+fall(n-w,r)*fall(w,3-r)),2*fall(n,3))
assert sum(sat(Y,a) for a in product((0,1),repeat=6))==20
for w in range(7):
 layer=[a for a in product((0,1),repeat=6) if sum(a)==w]
 for r in range(4):
  observed=Q(sum(sum(sum((a[abs(z)-1]==1)==(z>0) for z in C)==r for C in Y) for a in layer),len(layer))
  assert observed==mean(6,w,r)
for c,want in [(Q(6,5),Q(23,45)),(Q(241,200),Q(11642479,23232400))]:
 f=Q(1);ds=[]
 for k in range(1,4):
  f=c*f/(f+1);ds.append(min((1/f-c)/k,c**(-k)))
 assert ds[1]==want and ds[1]>max(ds[0],ds[2],c**(-4))
p=Path(__file__).resolve().parent
if (p/'U_source.json').exists():
 U=json.loads((p/'U_source.json').read_text())
 V=[C[:] for C in U];V[1][0],V[7][0]=V[7][0],V[1][0]
 h=sig(U);assert h==sig(V) and sum(h.values())==34716
 assert h[('++',0)]==8471 and h[('+-',1)]==780 and h[('--',2)]==22
 if (p/'V_witness.json').exists():
  a=json.loads((p/'V_witness.json').read_text())
  assert len(a)==198 and sat(V,a)
 print('U/V exact sign-overlap signature collision PASS; source UNSAT certificate in full ZIP')
else:print('Y6 all 7 layer means + exact FLMV tail PASS; place U_source.json alongside for U/V')
print('P versus NP OPEN. This is not a universal ARC contractor.')
