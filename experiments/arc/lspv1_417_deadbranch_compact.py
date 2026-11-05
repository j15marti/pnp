#!/usr/bin/env python3
from itertools import combinations
def php(k,w,relaxed=False):
 for i in range(k+1):
  if not any(w[i*k+j] for j in range(k)): return False
 for i,ii in combinations(range(k+1),2):
  if relaxed and (i,ii)==(0,1):continue
  for j in range(k):
   if w[i*k+j] and w[ii*k+j]:return False
 return True
def sentinel(k,w):
 return {'nvars':len(w)+1,'clauses':[[1]]+[[1,-1,i+2 if b else -(i+2)] for i,b in enumerate(w)]}
if __name__=='__main__':
 rows=[]
 for k in (1,2,3):
  tot=1<<(k*(k+1));bad=0
  for z in range(tot):
   w=[(z>>j)&1 for j in range(k*(k+1))]
   assert not php(k,w)
   assert len(sentinel(k,w)['clauses'])==len(w)+1
   bad+=php(k,w,True)
  rows.append((k,tot,bad))
 print({'status':'PASS','k_instances_relaxed_false_rejects':rows,'B3':'OPEN'})
