#!/usr/bin/env python3
"""No-producer-import F9 original-source verifier, LSPV-1 MINZERO317."""
from itertools import product,combinations
import json
C=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def truth(cl,a):
 return any(((a>>(abs(x)-1))&1)==int(x>0) for x in cl)
def covered(a,p):
 return all(((a>>(i-1))&1)==v for i,v in p.items())
def check():
 count=0;checks=0
 for a in range(512):
  count+=all(truth(c,a) for c in C)
  for c in C:
   t=sum(((a>>(abs(x)-1))&1)==int(x>0) for x in c)
   v=a^511
   u=sum(((v>>(abs(x)-1))&1)==int(x>0) for x in c)
   assert t+u==3;checks+=1
 assert count==70
 p={3:0,5:1,6:0,7:0,8:0}
 counts=[0,0];leaves=[]
 for a in range(512):
  if not covered(a,p):continue
  x=a&1;X=(a>>1)&1;Y=(a>>8)&1
  assert all(truth(c,a) for c in C)==bool((1-x)&X&Y);checks+=1
  counts[x]+=int(all(truth(c,a) for c in C))
  if x:
   bad=[j for j,c in enumerate(C) if not truth(c,a)]
   assert bad;leaves.append(bad);checks+=1
 assert counts==[2,0] and len(leaves)==8
 ext={'SS':0,'SU':0,'US':0,'UU':0}
 for i,j in combinations(range(12),2):
  for s,t in product('SU',repeat=2):
   vs=sorted(set(abs(x) for x in C[i]+C[j]))
   good=False
   for bits in product([0,1],repeat=len(vs)):
    assignment=dict(zip(vs,bits))
    def local(cl,q):
     return all(assignment[abs(x)]==(int(x>0) if q=='S' else int(x<0)) for x in cl)
    good|=local(C[i],s) and local(C[j],t)
   ext[s+t]+=int(good);checks+=1
 assert ext=={'SS':37,'SU':49,'US':49,'UU':37}
 return {'status':'PASS','no_producer_import':True,'F9_models':count,'pinned_cofactor_models':counts,'UNSAT_false_clause_leaves':len(leaves),'S_U_modes':ext,'counted_checks':checks,'P_vs_NP':'OPEN'}
if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
