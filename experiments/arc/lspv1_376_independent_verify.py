#!/usr/bin/env python3
"""Independent all-256 three-variable semantic quotient controls, no JS imports."""
import json
from itertools import product
def run():
 checks=0
 def ck(q):
  nonlocal checks
  checks+=1
  assert q
 def members(m):return frozenset(a for a in range(8) if m>>a&1)
 def blockers(m):return [tuple(-(i+1) if (a>>i)&1 else i+1 for i in range(3)) for a in range(8) if not m>>a&1]
 def clause(c,a):return any((bool((a>>(abs(l)-1))&1) if l>0 else not bool((a>>(abs(l)-1))&1)) for l in c)
 for m in range(256):
  b=blockers(m)
  ck(len(b)==8-len(members(m)))
  for a in range(8):ck(all(clause(c,a) for c in b)==(a in members(m)))
 good=bad=imp=0
 for s in range(256):
  S=members(s)
  for q in range(256):
   Q=members(q)
   allowed=S.issubset(Q)
   ck(allowed==all(a not in S or a in Q for a in range(8)))
   if allowed:
    good+=1
    for c in blockers(q):
     ck(all(clause(c,a) for a in S))
     imp+=1
   else:
    bad+=1
    ck(any(a in S and a not in Q for a in range(8)))
   ck(members(s&q)==S.intersection(Q))
 ck(good==6561 and bad==58975)
 edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
 def k4(charges):
  return sum(all((sum((mask>>j)&1 for j,e in enumerate(edges) if v in e)%2)==charges[v] for v in range(4)) for mask in range(64))
 ck(k4((1,0,0,0))==0);ck(k4((0,0,0,0))==8)
 return dict(run_id='LSPV1_ROOT_EXTENSIONAL_SEMANTIC_QUOTIENT376',checks=checks,functions=256,semantic_pairs=65536,legal=good,illegal=bad,implied_basis_clauses=imp,k4_odd_models=0,k4_even_models=8,method='independent direct set enumeration',status='PASS')
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
