#!/usr/bin/env python3
"""LSPV-2/423 independent source-cofactor count replay, no SAT oracle.
Usage: python experiments/arc/lspv2_423_cofactor_transfer.py
Standard library only; finite checks are not a native FLMV time-space audit.
"""
from itertools import combinations,product
import random,json
SEED=42320261105
def graph(name):
 if name=="K4":
  n=4;e=list(combinations(range(4),2))
 elif name=="cube":
  n=8;e=[(a,b) for a,b in combinations(range(8),2) if (a^b).bit_count()==1]
 elif name=="Petersen":
  n=10;e=[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(i+5,(i+2)%5+5) for i in range(5)]
 elif name=="Heawood":
  n=14;e=[(p,i+7) for i in range(7) for p in (i,(i+1)%7,(i+3)%7)]
 else:raise ValueError(name)
 e=sorted({tuple(sorted(z)) for z in e})
 assert len(e)*2==3*n
 assert all(sum(v in a for a in e)==3 for v in range(n))
 return n,e
def source(n,edges,odd):
 rows=[]
 for v in range(n):
  ids=[j for j,e in enumerate(edges,1) if v in e]
  assert len(ids)==3
  for bits in product(range(2),repeat=3):
   if (sum(bits)%2)!=(int(odd) if v==0 else 0):
    rows.append(tuple(j if b==0 else -j for j,b in zip(ids,bits)))
 assert len(rows)==4*n
 return rows
def reduce(rows,a):
 remaining=0;overlap=0;occ=0;empty=0
 for row in rows:
  t=sum(int(l>0)==a[abs(l)] for l in row if abs(l) in a)
  occ+=t;overlap+=max(0,t-1)
  if t==0:
   remaining+=1
   if all(abs(l) in a for l in row):empty+=1
 return remaining,overlap,occ,empty
def states(m,d):
 for k in range(min(m,d)+1):
  for keys in combinations(range(1,m+1),k):
   for values in product(range(2),repeat=k):yield dict(zip(keys,values))
def check(name):
 n,edges=graph(name);m=len(edges);rng=random.Random(SEED+3*n)
 tested=0;max_overlap=0
 for odd in (False,True):
  rows=source(n,edges,odd)
  for eid in range(1,m+1):
   assert sum(eid in row for row in rows)==4
   assert sum(-eid in row for row in rows)==4
  depth={"K4":m,"cube":4,"Petersen":3,"Heawood":2}[name]
  all_states=list(states(m,depth))
  if name=="Heawood":
   for _ in range(300):
    keys=rng.sample(range(1,m+1),rng.randrange(3,min(11,m)+1))
    all_states.append({i:rng.randrange(2) for i in keys})
  for a in all_states:
   c,omega,tr,empty=reduce(rows,a)
   k=len(a)
   assert tr==4*k and c==4*n-4*k+omega and c>=4*n-4*k
   for v in range(n):
    block=rows[v*4:v*4+4]
    d=3-sum(abs(l) in a for l in block[0])
    rr=[tuple(l for l in row if abs(l) not in a) for row in block
        if not any((int(l>0)==a[abs(l)]) for l in row if abs(l) in a)]
    if d>0:
     assert len(rr)==2**(d-1) and all(len(z)==d for z in rr)
    else:assert len(rr) in (0,1) and all(len(z)==0 for z in rr)
   tested+=1;max_overlap=max(max_overlap,omega)
  chosen=[];used=set()
  for i,(u,v) in enumerate(edges,1):
   if not used.intersection((u,v)):
    chosen.append(i);used.update((u,v))
   if len(chosen)>=3:break
  a={i:i%2 for i in chosen};c,omega,tr,empty=reduce(rows,a)
  assert omega==0 and c==4*n-4*len(a)
  if odd:
   for j in range(min(2**m,16)):
    a={i:(j>>(i-1))&1 for i in range(1,m+1)}
    assert reduce(rows,a)[3]>0
  else:assert reduce(rows,{i:0 for i in range(1,m+1)})[3]==0
 return {"graph":name,"vertices":n,"checked_partial_states":tested,"max_overlap":max_overlap}
if __name__=="__main__":
 r=[check(n) for n in ("K4","cube","Petersen","Heawood")]
 assert sum(x["checked_partial_states"] for x in r)==31944
 print(json.dumps({"status":"PASS","seed":SEED,"state_checks":31944,"graphs":r}))
