#!/usr/bin/env python3
"""Compact independent reproduction of the central one-sided projection theorem.
Full typed policy producer, verifier and raw controls are in TYPED-TRANSACTION260 archive."""
from itertools import product
def holds(F,a):
 return all(any((a[abs(l)-1]==1)==(l>0) for l in C) for C in F)
def project(E,n,ny,a):
 return any(holds(E,tuple(a)+tuple(y)) for y in product((0,1),repeat=ny))
def cube(a,r):
 return all(v==2 or a[i]==v for i,v in enumerate(r))
def check(F,E,n,ny):
 X=list(product((0,1),repeat=n))
 cover=all(not holds(F,a) or project(E,n,ny,a) for a in X)
 unsat_export=True;clause_export=True
 ds=[()]+[(s*i,) for i in range(1,n+1) for s in (-1,1)]
 for r in product((0,1,2),repeat=n):
  fam=[a for a in X if cube(a,r)]
  Fsat=any(holds(F,a) for a in fam)
  Esat=any(project(E,n,ny,a) for a in fam)
  if Fsat and not Esat:unsat_export=False
  for D in ds:
   e_implies=all(any((a[abs(l)-1]==1)==(l>0) for l in D) for a in fam if project(E,n,ny,a))
   f_implies=all(any((a[abs(l)-1]==1)==(l>0) for l in D) for a in fam if holds(F,a))
   if e_implies and not f_implies:clause_export=False
 assert cover==unsat_export==clause_export
 return cover
if __name__=="__main__":
 F=[(1,2,3)]
 assert check(F,[],3,0)
 assert not check(F,F+[(-1,),(-2,),(-3,)],3,0)
 # auxiliary y=x1 via clauses y->x1 and x1->y; pointwise faithful
 assert check(F,F+[(-4,1),(4,-1)],3,1)
 # nonextendible projected source under-assumption despite root SAT
 assert not check(F,F+[(4,),(-4,1)],3,1)
 print("PASS: one-sided COVER iff UNSAT-EXPORT iff guarded CLAUSE-EXPORT")
