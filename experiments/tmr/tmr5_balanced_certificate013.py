#!/usr/bin/env python3
"""Independent exhaustive matcher for TMR-5 / TMR-2 balanced-mask certificate audit.
Bit order: 3 coordinates numbered 0,1,2, mask bit c is (mask>>c)&1.
Each of eight rows has three independently observable sign bits.
"""
from itertools import combinations
from math import comb
from collections import Counter
import json, time

CASES={
  'even_double':(0,0,3,3,5,5,6,6),
  'pair_projection_triple':(0,0,1,1,6,6,7,7),
  'two_quadruples':(0,0,0,0,7,7,7,7),
  'unbalanced_prior':(1,2,3,4,5,6,7,7),
  'unsat_permutation':(0,1,2,3,4,5,6,7)
}

def predicted_size6(a):
   bymask=Counter(a)
   duplicates=sum(comb(n,2) for n in bymask.values() if n>=2)
   triples=0
   for J in combinations(range(3),2):
      proj=Counter(tuple((v>>j)&1 for j in J) for v in a)
      triples+=sum(comb(n,3) for n in proj.values() if n>=3)
   return duplicates,triples,duplicates+triples

# Independent Hall perfect-matching decision using augmenting paths.
# Compute row domains by querying row-coordinate positions, then run matching.
allowed=[[[m for m in range(8) if all(((m>>c)&1)==((v>>c)&1) for c in range(3) if (qb>>c)&1)] for qb in range(8)] for v in range(8)]

def has_unsat_completion(a, positions):
   q=[0]*8
   for p in positions:
      q[p//3] |= 1<<(p%3)
   domains=[allowed[a[i]][q[i]] for i in range(8)]
   # Tight rows first is safe, and improves throughput.
   order=sorted(range(8),key=lambda i:len(domains[i]))
   assigned=[-1]*8
   def augment(i,seen):
      for m in domains[i]:
         b=1<<m
         if seen[0]&b:continue
         seen[0]|=b
         if assigned[m]<0 or augment(assigned[m],seen):
            assigned[m]=i
            return True
      return False
   for i in order:
      if not augment(i,[0]):return False
   return True

def classify(a):
   is_sat=len(set(a))<8
   balance=all(sum((m>>c)&1 for m in a)==4 for c in range(3))
   d,t,pred=predicted_size6(a)
   return {'tuple':list(a),'sat':is_sat,'balanced':balance,
           'predicted_duplicate_pair_certificates':d,
           'predicted_projection_triple_certificates':t,
           'predicted_six_certificates':pred}

def audit_case(name,a,max_k=6):
   start=time.monotonic();counts={};samples={}
   for k in range(max_k+1):
      total=0;cert=0;witness=None
      for positions in combinations(range(24),k):
         total+=1
         if not has_unsat_completion(a,positions):
            cert+=1
            if witness is None:witness=list(positions)
      counts[str(k)]={'tested':total,'certificates':cert}
      if witness is not None:samples[str(k)]=witness
   z=classify(a)
   z.update({'counts':counts,'witnesses':samples,'seconds':round(time.monotonic()-start,3)})
   return z

if __name__=='__main__':
 import sys
 names=sys.argv[1:] or ['even_double']
 result={}
 for name in names:
    a=CASES[name]
    z=audit_case(name,a)
    if z['balanced'] and z['sat']:
       assert all(z['counts'][str(k)]['certificates']==0 for k in range(6)),(name,z)
       assert z['counts']['6']['certificates']==z['predicted_six_certificates'],(name,z)
    result[name]=z
 print(json.dumps(result,indent=2,sort_keys=True))
