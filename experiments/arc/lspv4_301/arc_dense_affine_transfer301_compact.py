#!/usr/bin/env python3
"""Compact independent restricted source and exact numerical audit; stdlib only."""
from collections import Counter
from itertools import product
from fractions import Fraction
from math import ceil,log2
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=P+[tuple(-a for a in c) for c in Q]
H=Counter(x for c in F for x in c)
assert len(set(map(tuple,map(sorted,F))))==12
assert all(H[x]==H[-x]==2 for x in range(1,10))
def truth(p):
 return all(any(p[abs(x)]==int(x>0) for x in c) for c in F)
assert sum(truth({i+1:b for i,b in enumerate(bits)}) for bits in product((0,1),repeat=9))==70
def cube(pin):
 free=[i for i in range(1,10) if i not in pin]
 covered=[c for c in F if any(abs(x) in pin and pin[abs(x)]==int(x>0) for x in c)]
 uncovered=[c for c in F if c not in covered]
 spill=Counter(x for c in covered for x in c if abs(x) in free)
 eta=sum(min(spill[x],spill[-x]) for x in free)
 pref={x:int(spill[x]<spill[-x]) for x in free if spill[x]!=spill[-x]}
 rows=[]
 for c in uncovered:
  rem=[x for x in c if abs(x) in free]
  mask=sum(1<<free.index(abs(x)) for x in rem)
  rhs=1^(len(rem)%2 if c[0]<0 else 0)
  rows.append((mask,rhs))
 for x,b in pref.items():rows.append((1<<free.index(x),b))
 sat=sum(truth({**pin,**dict(zip(free,a))}) for a in product((0,1),repeat=5))
 affine=sum(all((a_mask & sum(1<<i for i,x in enumerate(free) if a[i])).bit_count()%2==rhs for a_mask,rhs in rows) for a in product((0,1),repeat=5))
 return len(free),len(uncovered),eta,len(rows),sat,affine
assert cube({1:0,2:0,8:1,9:1})==(5,6,4,6,2,2)
assert cube({3:0,6:1,7:1,9:1})==(5,6,4,8,0,0)
for t in (1,2,4,8,16,32,64,128):
 B=ceil(log2(9*t+1));K=ceil(log2(12*t+1))
 N=2*K+36*t*(B+1)
 assert 6*t*(5*t+1)>0
 print("t N denseSAT denseUNSAT",t,N,6*t*(5*t+1),8*t*(5*t+1))
def env(c):
 f=Fraction(1);ds=[]
 for k in (1,2,3):
  f=c*f/(1+f)
  ds.append(min((1/f-c)/k,c**(-k)))
 assert ds[1]>ds[0] and ds[1]>ds[2] and c**(-4)<ds[1]
 return ds[1]
assert env(Fraction(6,5))==Fraction(23,45)
assert env(Fraction(241,200))==Fraction(11642479,23232400)
print("PASS: both coherent cubes and strict FLMV envelope; P vs NP OPEN")
