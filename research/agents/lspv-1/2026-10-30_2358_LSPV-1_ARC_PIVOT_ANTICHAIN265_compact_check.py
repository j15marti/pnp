#!/usr/bin/env python3
"""Independent source-indexed original-pair blocker checker (Python 3, stdlib)."""
from itertools import product
def src():
 h=[tuple((i+1)*(-1 if k>>i&1 else 1) for i in range(3)) for k in range(8)]
 return [('H7 SAT',[c for j,c in enumerate(h) if j!=2]),
         ('H8 UNSAT',h),
         ('extremes incompatible SAT',[(1,2,3),(1,-2,-3)]),
         ('forced-x SAT',[(1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3)]),
         ('XOR SAT',[h[j] for j in (1,2,4,7)]),
         ('2SAT SAT',[(1,2),(-1,2),(-2,3)])]
def truth(l,a): return a[abs(l)-1]==int(l>0)
def sat(F,a): return all(any(truth(l,a) for l in c) for c in F)
def false(c,r): return all(r[abs(l)-1]!=-1 and r[abs(l)-1]==int(l<0) for l in c)
def main():
 counts=dict(sources=0,SAT=0,UNSAT=0,pair_modes=0,cube_pivot=0,complement_checks=0)
 for name,F in src():
  n=max(abs(l) for c in F for l in c)
  all_a=list(product((0,1),repeat=n))
  models=[a for a in all_a if sat(F,a)]
  counts['sources']+=1
  counts['SAT' if models else 'UNSAT']+=1
  for a in all_a:
   comp=tuple(1-v for v in a)
   for c in F:
    assert sum(truth(l,a) for l in c)+sum(truth(l,comp) for l in c)==len(c)
    counts['complement_checks']+=1
  for j,C in enumerate(F):
   for k,D in enumerate(F):
    if j>=k: continue
    same=any(l in D for l in C)
    opposite=any(-l in D for l in C)
    for left,right in product('SU',repeat=2):
     need={};ok=True
     for c,mode in ((C,left),(D,right)):
      for lit in c:
       x=abs(lit);v=int(lit>0) if mode=='S' else int(lit<0)
       if x in need and need[x]!=v:ok=False
       need[x]=v
     actual=ok and any(all(a[x-1]==v for x,v in need.items()) for a in all_a)
     assert actual==(not (opposite if left==right else same))
     counts['pair_modes']+=1
  for rho in product((-1,0,1),repeat=n):
   available=any(all(v==-1 or v==a[i] for i,v in enumerate(rho)) for a in models)
   for pivot in range(1,n+1):
    if rho[pivot-1]!=-1:continue
    pos=any(pivot in c and false([l for l in c if l!=pivot],rho) for c in F)
    neg=any(-pivot in c and false([l for l in c if l!=-pivot],rho) for c in F)
    derived=False
    for C in F:
     if pivot not in C:continue
     for D in F:
      if -pivot not in D:continue
      R=(set(C)-{pivot})|(set(D)-{-pivot})
      if any(-l in R for l in R):continue
      derived=derived or false(R,rho)
    assert (pos and neg)==derived
    if derived:assert not available
    counts['cube_pivot']+=1
  print(name,'SAT' if models else 'UNSAT',len(models))
 print('PASS',counts)
if __name__=='__main__':main()
