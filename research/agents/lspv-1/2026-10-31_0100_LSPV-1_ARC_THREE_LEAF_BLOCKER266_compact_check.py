#!/usr/bin/env python3
"""Standalone independent compact checker, source-only depth-two resolution."""
from itertools import combinations, product
import json
def norm(c):
 return tuple(sorted(set(c),key=lambda z:(abs(z),z<0)))
def steps(a,b):
 for p in set(map(abs,a)) & set(map(abs,b)):
  if (p in a and -p in b) or (-p in a and p in b):
   c=norm(tuple(v for v in a+b if abs(v)!=p))
   if not any(-v in c for v in c):yield c
def derived(F):
 F=list(map(norm,F));R=set()
 for i,j in combinations(range(len(F)),2):
  for a in steps(F[i],F[j]):
   R.add(a)
   for k in range(len(F)):
    if k in (i,j):continue
    R.update(steps(a,F[k]))
 return R
def sat(F,a):
 return all(any(a[abs(v)-1]==int(v>0) for v in c) for c in F)
def fullmodels(F,n):
 return [a for a in product((0,1),repeat=n) if sat(F,a)]
def blockers(F,n):
 R=derived(F);M=fullmodels(F,n);checks=0
 for clause in R:
  assert len(clause)<=5
  for a in M:assert any(a[abs(v)-1]!=int(v<0) for v in clause);checks+=1
 for rho in product((-1,0,1),repeat=n):
  direct=any(all(rho[abs(v)-1]==int(v<0) for v in clause) for clause in R)
  if direct:
   assert all(any(rho[i]!=-1 and rho[i]!=a[i] for i in range(n)) for a in M)
  checks+=1
 return checks,len(R),len(M)
all8=[tuple((-i-1 if a[i] else i+1) for i in range(3)) for a in product((0,1),repeat=3)]
checks=0
for mask in range(256):
 F=[c for i,c in enumerate(all8) if mask>>i & 1]
 v,r,m=blockers(F,3);checks+=v
 assert (m==0)==(mask==255)
C=[(1,2,3),(-1,4,5),(-2,6,7)]
R=derived(C);assert (3,4,5,6,7) in R
R1=set()
for a,b in combinations(C,2):R1.update(steps(a,b))
assert not any(all(abs(v) in {3,4,5,6,7} and v>0 for v in q) for q in R1)
assert len(fullmodels(C,7))>0
assert tuple() not in derived(all8)
print(json.dumps({"status":"PASS","all_sign_clause_subsets":256,"checks":checks,"chain_strict_gain":True,"H8_no_empty_three_leaf":True},sort_keys=True))
