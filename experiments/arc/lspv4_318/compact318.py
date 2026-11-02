#!/usr/bin/env python3
"""LSPV-4 318: direct self-contained parity/rank bit-access falsifier, valid quota sources."""
from collections import Counter
F=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
H=[(1,2),(5,3),(6,8)]+F[2:]
def ren(c,i):return tuple((1 if x>0 else -1)*(abs(x)+9*i) for x in c)
def src(r,z):
 p=[ren(H[3],i) for i in range(1,r+1)]
 q=[ren(H[0],i) for i in range(1,r+1)]
 a=p+[H[3]]+q+[x for j,x in enumerate(H) if j!=3]
 for i in range(1,r+1):a += [ren(x,i) for j,x in enumerate(H) if j not in (0,3)]
 for i in range(r):
  if z>>i&1:a[i],a[r+1+i]=a[r+1+i],a[i]
 return a
def valid(A,n):
 d=Counter(x for c in A for x in c)
 return len({tuple(sorted(c)) for c in A})==len(A) and all(
  len(c) in (2,3) and len(set(map(abs,c)))==len(c) and all(1<=abs(x)<=n for x in c)
  for c in A) and all(d[i]==d[-i]==2 for i in range(1,n+1))
def models(A,p=None):
 p=p or {};n=max(abs(x) for c in A for x in c)
 return sum(all(((z>>(j-1))&1)==v for j,v in p.items()) and all(
  any(((z>>(abs(x)-1))&1)==(x>0) for x in c) for c in A)
  for z in range(1<<n))
assert valid(F,9) and valid(H,9) and models(F)==70 and models(H)==37
p={8:0,3:0,7:0,6:0,1:1,5:1}; q=dict(p);q[8]=1
assert (models(F,q),models(F,p))==(3,0)
assert (models(H,{1:0,2:1,3:0,4:0,5:1}),models(H,{1:0,2:0,3:0,4:0,5:0}))==(6,0)
cases=flips=0
for r in range(1,10):
 for z in range(1<<r):
  A=src(r,z);n=9*(r+1);assert valid(A,n) and len(A)==13*(r+1)
  v=12*n+sum(792 if len(c)==2 else 789 for c in A[:r])+1
  assert v==12*n+789*r+3*z.bit_count()+1
  for i in range(r):
   B=src(r,z^(1<<i))
   assert {j for j in range(len(A)) if A[j]!=B[j]}=={i,r+1+i}
   v2=12*n+sum(792 if len(c)==2 else 789 for c in B[:r])+1
   assert (v&1)!=(v2&1)
   flips+=1
  cases+=1
print('PASS',{'valid_promised_sources':cases,'opposite_bit_single_pair_swaps':flips,
              'same_canonical_F9_pinned_SAT_UNSAT':(3,0),
              'same_signed_H_pinned_SAT_UNSAT':(6,0),'P_vs_NP':'OPEN'})
