#!/usr/bin/env python3
from itertools import combinations
def phi(k,b,relax=False):
 if any(not any(b[i*k+j] for j in range(k)) for i in range(k+1)):return False
 for i,ip in combinations(range(k+1),2):
  if relax and (i,ip)==(0,1):continue
  if any(b[i*k+j] and b[ip*k+j] for j in range(k)):return False
 return True
def sentinel(k,b):
 return {'nvars':len(b)+1,'clauses':[[1,i+2 if z else -(i+2)] for i,z in enumerate(b)]}
if __name__=='__main__':
 results=[]
 for k in (1,2,3):
  cnt=0;wrong=0
  for val in range(1<<(k*(k+1))):
   w=[val>>i&1 for i in range(k*(k+1))]
   src=sentinel(k,w)
   assert len(src['clauses'])==len(w)
   assert all(len(c)==2 and c[0]==1 and abs(c[1])>1 for c in src['clauses'])
   assert not phi(k,w)
   wrong+=int(phi(k,w,True));cnt+=1
  results.append((k,cnt,wrong))
 print({'status':'PASS','k_count_relaxed_wrong_rejections':results})
