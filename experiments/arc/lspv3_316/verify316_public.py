#!/usr/bin/env python3
"""GATE316 independent original-clause verifier, NO producer imports."""
from collections import Counter,defaultdict
from itertools import product
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
def connect(t):
 out=[];pins={}
 for z in range(t):
  out.extend([[(1 if v>0 else -1)*(abs(v)+6*z) for v in r] for r in Y])
  pins[6*z+3]=0;pins[6*z+4]=1
 for z in range(t-1):
  i,j=8*z+5,8*(z+1)+6
  out[i][0],out[j][2]=out[j][2],out[i][0]
 return out,pins
def legal(F):
 n=max(abs(v) for r in F for v in r);f=Counter(v for r in F for v in r)
 return len(F)*3==4*n and len(set(tuple(sorted(r)) for r in F))==len(F) and all(len(r)==3 and len(set(map(abs,r)))==3 and (min(r)>0 or max(r)<0) for r in F) and all(f[i]==f[-i]==2 for i in range(1,n+1))
def count(F,p):
 n=max(abs(v) for r in F for v in r);free=[x for x in range(1,n+1) if x not in p]
 total=0
 for bitvec in product((0,1),repeat=len(free)):
  a=p.copy();a.update(zip(free,bitvec))
  total+=all(any(a[abs(v)]==int(v>0) for v in row) for row in F)
 return total
def stats(F,p):
 n=max(abs(v) for r in F for v in r);free=[i for i in range(1,n+1) if i not in p]
 cov=[];openrows=[]
 for j,row in enumerate(F):
  if any(abs(v) in p and p[abs(v)]==int(v>0) for v in row):cov.append(j)
  else:openrows.append((j,[v for v in row if abs(v) not in p]))
 u=len(openrows);e=2*len(free)-u
 eta=sum(min(sum(x in F[j] for j in cov),sum(-x in F[j] for j in cov)) for x in free)
 imb=sum(abs(sum(x in F[j] for j in cov)-sum(-x in F[j] for j in cov)) for x in free)
 u1=sum(len(r)==1 for j,r in openrows);u3=sum(len(r)==3 for j,r in openrows)
 assert 2*(e-eta)==imb+u3-u1
 return e,eta,u1,u3,openrows
if __name__=="__main__":
 for t in (1,2,3,4,8,16):
  F,p=connect(t);assert legal(F)
  e,eta,u1,u3,rows=stats(F,p)
  assert (e,eta,u1,u3)==(4*t,4*t,0,0)
  if t<=3:assert count(F,p)==4**t
  # Each connected component of the residual must obey opposite-value edges.
  adj=defaultdict(set)
  for j,row in rows:
   a,b=map(abs,row);adj[a].add(b);adj[b].add(a)
  seen={};nc=0
  for x in sorted(set(range(1,6*t+1))-set(p)):
   if x in seen:continue
   seen[x]=0;q=[x]
   for v in q:
    for w in adj[v]:
     if w not in seen:seen[w]=1-seen[v];q.append(w)
     else:assert seen[w]!=seen[v]
   nc+=1
  assert nc==2*t
 for name,p,z in (("SAT",{3:1,4:0,6:0,8:0,9:1},2),("UNSAT",{1:1,3:1,4:0,5:1,8:0},0)):
  assert legal(F9) and count(F9,p)==z
  e,eta,u1,u3,rows=stats(F9,p)
  assert e==eta and not(u1 or u3)
 assert count(F9,{})==70
 print("GATE316 INDEPENDENT CHECK PASS, restricted only, P versus NP OPEN")
