#!/usr/bin/env python3
"""LSPV-4 319: independently executable checkpoint-rank source test, Python stdlib."""
import math
from collections import Counter
F=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
H=[(1,2),(5,3),(6,8)]+F[2:]
def ren(c,i):return tuple((1 if x>0 else -1)*(abs(x)+9*i) for x in c)
def src(r,z):
 a=[ren(H[3],i) for i in range(1,r+1)]+[H[3]]+[ren(H[0],i) for i in range(1,r+1)]
 a += [x for j,x in enumerate(H) if j!=3]
 for i in range(1,r+1):a += [ren(x,i) for j,x in enumerate(H) if j not in (0,3)]
 for i in range(r):
  if (z>>i)&1:a[i],a[r+1+i]=a[r+1+i],a[i]
 return a
def quota(C,n):
 D=Counter(x for c in C for x in c)
 return len({tuple(sorted(c)) for c in C})==len(C) and all(len(c) in (2,3) and
 len({abs(x) for x in c})==len(c) for c in C) and all(D[i]==D[-i]==2 for i in range(1,n+1))
def models(C,p):
 return sum(all(((a>>(k-1))&1)==v for k,v in p.items()) and
 all(any(((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in C) for a in range(512))
assert quota(F,9) and quota(H,9)
s={8:1,3:0,7:0,6:0,1:1,5:1};u=dict(s);u[8]=0
assert (models(F,{}),models(H,{}),models(F,s),models(F,u))==(70,37,3,0)
cases=flips=queries=probes=0
for r in range(1,10):
 m=13*(r+1);n=9*(r+1)
 for z in range(1<<r):
  C=src(r,z);assert quota(C,n) and len(C)==m
  bits=[int(len(c)==2) for c in C]
  assert sum(bits[:r])==z.bit_count()
  for B in set((1,2,4,8,16,32,64,math.ceil(math.sqrt(m*math.ceil(math.log2(m+1)))))):
   checkpoints={0:0};v=0
   for i,b in enumerate(bits,1):
    v+=b
    if i%B==0 and i<m:checkpoints[i]=v
   assert (len(checkpoints)-1)==(m-1)//B
   for j in range(m):
    base=(j//B)*B
    rank=checkpoints[base]+sum(bits[base:j])
    assert 12*n+789*j+3*rank+1==12*n+789*j+3*sum(bits[:j])+1
    queries+=1;probes+=j-base
  for i in range(r):
   O=src(r,z^(1<<i))
   assert {j for j in range(m) if C[j]!=O[j]}=={i,r+1+i}
   assert (sum(len(c)==2 for c in C[:r])-sum(len(c)==2 for c in O[:r])) in (-1,1)
   flips+=1
  cases+=1
assert (cases,flips,queries,probes)==(1022,8194,958308,8616486)
print("PASS",{"sources":cases,"flips":flips,"rank_queries":queries,"source_width_probes":probes,
              "same_F9_pinned_SAT_UNSAT":(3,0),"P_vs_NP":"OPEN"})
