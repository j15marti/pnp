#!/usr/bin/env python3
"""ARC-POSITIVE-SCOPE301 compact no-dependency source-faithful Y6 falsifier.
Exact GF(2) rows, positive-delta ticket phases, and independent truth table.
Full exhaustive Y6/F9 verifier is in the signed reproducibility archive.
"""
from itertools import product
from collections import Counter
import json
F=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P={5:0,6:1}

def sat(a):
 return all(any(a[abs(l)]==int(l>0) for l in C) for C in F)

def row(C,idx):
 m=0;r=1
 for l in C:m^=1<<idx[abs(l)];r^=int(l<0)
 return m,r

def affine_solutions(rows,free):
 return [bits for bits in product((0,1),repeat=len(free))
  if all((sum(bits[i] for i in range(len(free)) if m>>i&1)&1)==b for m,b in rows)]

def main():
 n=6;counts=Counter(l for C in F for l in C)
 assert all(counts[x]==counts[-x]==2 for x in range(1,n+1))
 assert len({tuple(sorted(C)) for C in F})==8
 free=tuple(v for v in range(1,n+1) if v not in P)
 ids={v:i for i,v in enumerate(free)}
 U={j:tuple(l for l in C if abs(l) not in P) for j,C in enumerate(F)
    if not any(abs(l) in P and P[abs(l)]==int(l>0) for l in C)}
 assert list(U)==[0,1,4,5]
 eta=sum(min(sum(v in F[j] for j in range(8) if j not in U),
             sum(-v in F[j] for j in range(8) if j not in U)) for v in free)
 delta=2*len(free)-len(U)-eta
 assert (eta,delta)==(3,1)
 base=[row(C,ids) for C in U.values()]
 assert tuple(a^b for a,b in [(0,0)])==(0,)
 assert __import__('functools').reduce(lambda a,b:a^b,(m for m,r in base),0)==0
 assert __import__('functools').reduce(lambda a,b:a^b,(r for m,r in base),0)==1
 assert affine_solutions(base,free)==[]
 # Each admissible ticket spends exactly delta=1, and only its committed
 # clause obtains a non-default row; rows for other clauses remain default.
 branches=0;found=set();consistency=[]
 for chosen,C in U.items():
  for k in range(len(C)):
   if len(C)==2 and k>0:continue
   if len(C)==3:
    lit_truth=tuple(int(i!=k) for i in range(3))
   else:
    lit_truth=(1,1)
   designated=[(1<<ids[abs(l)],v^int(l<0)) for l,v in zip(C,lit_truth)]
   rows=[row(D,ids) for j,D in U.items() if j!=chosen]+designated
   sols=affine_solutions(rows,free)
   branches+=1;consistency.append(len(sols))
   for bs in sols:
    a=dict(P);a.update(zip(free,bs))
    assert sat(a)
    assert bs not in found
    found.add(bs)
 truth={bs for bs in product((0,1),repeat=len(free))
  if sat({**P,**dict(zip(free,bs))})}
 assert found==truth and branches==8 and len(found)==6
 witness=(0,0,1,1,0,1)
 assert sat(dict(enumerate(witness,1)))
 assert sum(dict(enumerate(witness,1))[abs(l)]==int(l>0) for l in F[4])==2
 print(json.dumps({'status':'PASS','source':'Y6 canonical M22','free':free,
  'pin':P,'eta':eta,'delta':delta,'uncovered_original_clause_ids':list(U),
  'unsafe_default_parity_row_xor':[0,1],'unsafe_default_parity_solutions':0,
  'fully_committed_ticket_branches':branches,'branch_model_counts':consistency,
  'union_models':len(found),'brute_models':len(truth),'witness':witness,
  'status_scope':'restricted positive delta only; no ARC/FLMV conclusion'},sort_keys=True))
if __name__=='__main__':main()
