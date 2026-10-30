#!/usr/bin/env python3
"""Independent exact K4 signed NAE cylinder verifier. Stdlib only.
Exhaust all 4096 signed incidence sources; no dependency on producer.
"""
from itertools import combinations
from fractions import Fraction
import json
E=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
G=((-1,2,5),(1,-3,-4),(-1,3,4),(1,-2,-5))
def tv(l,a):
 x=(a>>(abs(l)-1))&1
 return x if l>0 else 1-x
def models(F):
 return [a for a in range(64) if all(any(tv(l,a) for l in c) for c in F)]
def signed_source(s):
 C=[[] for _ in range(4)]
 for e,(u,v) in enumerate(E):
  C[u].append((e+1)*(-1 if (s>>(2*e))&1 else 1))
  C[v].append((e+1)*(-1 if (s>>(2*e+1))&1 else 1))
 return [tuple(c) for c in C]+[tuple(-l for l in c) for c in C]
maxp={1:Fraction(0),2:Fraction(0),3:Fraction(0)}
frequency={}
for sign in range(4096):
 F=signed_source(sign)
 A=models(F);n=len(A)
 frequency[n]=frequency.get(n,0)+1
 assert n>=18
 for h in (1,2,3):
  upper=0
  for S in combinations(range(6),h):
   buckets={}
   for a in A:
    key=tuple((a>>v)&1 for v in S)
    buckets[key]=buckets.get(key,0)+1
   upper=max(upper,max(buckets.values()))
  q=Fraction(upper,n)
  maxp[h]=max(maxp[h],q)
  assert q<={1:Fraction(1,2),2:Fraction(2,5),3:Fraction(3,10)}[h]
assert frequency=={18:512,20:3072,24:512},frequency
base=signed_source(0)
assert len(models(base))==18
assert len(models(base+G))==0
assert all(models(base+G[:i]+G[i+1:]) for i in range(4))
print(json.dumps({"PASS":True,"source_signings":4096,
 "support_max_comparisons":12288,"model_distribution":frequency,
 "max_pattern_probabilities":{str(s):str(maxp[s]) for s in (1,2,3)},
 "four_extra_unsat":True,"all_three_subsets_sat":True},indent=2,sort_keys=True))
