#!/usr/bin/env python3
"""Independent F9 complete-input and all-9!-order reduced-OBDD audit, stdlib."""
from functools import lru_cache
import json
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
n=9;U=(1<<n)-1
def sat(a):return all(any(bool(a>>(abs(v)-1)&1)==(v>0) for v in c) for c in F)
f=[int(sat(a)) for a in range(512)]
def subset_values(S):
 out=[0]
 for i in range(9):
  if (S>>i)&1:out += [a|(1<<i) for a in out[:]]
 return out
cost={}
for S in range(512):
 rem=U^S;rv=[i for i in range(9) if (rem>>i)&1];forms=set()
 for a in subset_values(S):
  b=0
  for k,extra in enumerate(subset_values(rem)):
   if f[a|extra]:b|=1<<k
  forms.add(b)
 for j in rv:
  jj=rv.index(j);co=0
  for bm in forms:
   if any(((bm>>k)&1)!=((bm>>(k|(1<<jj)))&1) for k in range(1<<len(rv)) if not (k>>jj)&1):co+=1
  cost[S,j]=co
@lru_cache(None)
def best(S):
 if S==U:return 0,1,0,1
 arr=[]
 for j in range(n):
  if (S>>j)&1:continue
  mn,cmn,mx,cmx=best(S|(1<<j))
  arr.append((cost[S,j]+mn,cmn,cost[S,j]+mx,cmx))
 lo=min(x[0] for x in arr);hi=max(x[2] for x in arr)
 return lo,sum(x[1] for x in arr if x[0]==lo),hi,sum(x[3] for x in arr if x[2]==hi)
def source_private(a):
 vals=[];g=0
 for c in F:
  w=[bool(a>>(abs(v)-1)&1)==(v>0) for v in c]
  vals.append((w[0] or w[1] or w[2],2));g+=2
 while len(vals)>1:
  nextv=[]
  for i in range(0,len(vals),2):
   if i+1>=len(vals):nextv.append(vals[i]);continue
   (x,d),(y,e)=vals[i:i+2];nextv.append((x and y,max(d,e)+1));g+=1
  vals=nextv
 return vals[0][0],g,vals[0][1]
assert all(source_private(a)==(bool(f[a]),35,6) for a in range(512))
mn,cmn,mx,cmx=best(0)
natural=sum(cost[(1<<j)-1,j] for j in range(n))
assert (sum(f),mn,cmn,natural,mx,cmx)==(70,52,72,66,80,48)
print(json.dumps(dict(run="F9_OBDD_AUDIT333",model_count=70,private_gates=35,private_depth=6,
 truth_rows=512,minimum_nodes=mn,minimum_order_count=cmn,natural_nodes=natural,
 maximum_nodes=mx,maximum_order_count=cmx,subsets=512,orders=362880),indent=2))
