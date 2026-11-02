#!/usr/bin/env python3
"""LSPV-4 331 compact source-checked equal-count cofactor verifier (stdlib)."""
import json
from collections import Counter
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def good(f,n):
 if n%3 or len(f)*3!=4*n:return False
 seen=set();hist=Counter()
 for c in f:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)) or any(abs(x)>n or not x for x in c):return False
  t=tuple(sorted(c))
  if t in seen:return False
  seen.add(t)
  for x in c:hist[abs(x),x>0]+=1
 return all(hist[i,s]==2 for i in range(1,n+1) for s in (True,False))
def sat(f,a):return all(any(bool(a>>(abs(v)-1)&1)==(v>0) for v in c) for c in f)
def count(f,n,p):return sum(sat(f,a) and all(v<0 or (a>>i&1)==v for i,v in enumerate(p)) for a in range(1<<n))
def hist(f,p):
 h=Counter()
 for c in f:
  covered=any(p[abs(v)-1]>=0 and p[abs(v)-1]==int(v>0) for v in c)
  w=sum(p[abs(v)-1]<0 for v in c)
  h['covered' if covered else str(w)]+=1
 return (h['covered'],h['0'],h['1'],h['2'],h['3'])
assert good(Z,6) and good(F,9) and count(Z,6,[-1]*6)==18 and count(F,9,[-1]*9)==70
p0=(0,-1,-1,-1,-1,-1);p1=(1,-1,-1,-1,-1,-1)
assert count(Z,6,p0)==count(Z,6,p1)==9 and hist(Z,p0)==hist(Z,p1)==(2,0,0,2,4)
a=set(z>>1 for z in range(64) if (z&1)==0 and sat(Z,z));b=set(z>>1 for z in range(64) if (z&1)==1 and sat(Z,z))
assert len(a&b)==4 and len(a-b)==len(b-a)==5
f0=(0,0,0,-1,-1,1,-1,-1,-1);f1=(1,0,0,-1,-1,1,-1,-1,-1)
assert count(F,9,f0)==1 and count(F,9,f1)==0 and hist(F,f0)==hist(F,f1)==(6,0,2,2,2)
D=Z+tuple(tuple((1 if x>0 else -1)*(abs(x)+6) for x in c) for c in Z)
assert good(D,12)
q0=p0+(-1,)*6;q1=p1+(-1,)*6
assert count(D,12,q0)==count(D,12,q1)==162
assert count(D,12,q0[:9]+(0,0,0))==count(D,12,q1[:9]+(0,0,0))==0
assert all(not good(f,n) for f,n in [(Z+(Z[0],),6),(((1,-2,3),)+Z[1:],6),(((1,1,3),)+Z[1:],6),(Z[:-1],6),((((1,2,7),)+Z[1:]),6)])
print(json.dumps({'source':'valid Z6/F9 originals','z6_models':18,'z6_sibling_models':[9,9], 'z6_intersection':4, 'z6_directional_only':[5,5], 'z6_unsigned_hist':[2,0,0,2,4],'f9_sibling_models':[1,0],'f9_unsigned_hist':[6,0,2,2,2],'disjoint_z6_sibling_models':[162,162],'disjoint_z6_pinned_unsat':[0,0],'status':'COMPUTATIONAL controls + symbolic coNP-hard promise theorem; P vs NP OPEN'},indent=2))
