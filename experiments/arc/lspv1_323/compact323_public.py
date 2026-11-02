#!/usr/bin/env python3
"""LSPV-1 323: three exact source-ID DP batches, polarity-squared audit."""
from itertools import product,combinations
from collections import Counter
import json,math
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
P6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
N6=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
PA=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
NA=[(1,5,9),(2,6,7),(3,4,8),(1,6,8),(2,4,9),(3,5,7)]
def source(p,n):return tuple(tuple(c) for c in p)+tuple(tuple(-x for x in c) for c in n)
def norm(c):
 s=set(c)
 return None if any(-x in s for x in s) else tuple(sorted(s,key=lambda x:(abs(x),x<0)))
def canonical(cs):return tuple(sorted(set(t for c in cs if (t:=norm(c)) is not None),key=lambda c:(len(c),tuple((abs(x),x<0) for x in c))))
def graph(cs):
 g={abs(x):set() for c in cs for x in c}
 for c in cs:
  for a,b in combinations(map(abs,c),2):g[a].add(b);g[b].add(a)
 return g
def greedy(g):
 ans=[];blocked=set()
 for x in sorted(g):
  if x not in blocked:ans.append(x);blocked|={x}|g[x]
 return ans
def dp(cs,I):
 assert all(sum(abs(l) in I for l in c)<=1 for c in cs)
 keep=[c for c in cs if all(abs(l) not in I for l in c)];out=list(keep)
 for x in I:
  pos=[c for c in cs if x in c]; neg=[c for c in cs if -x in c]
  for a,b in product(pos,neg):out.append(tuple(v for v in a if v!=x)+tuple(v for v in b if v!=-x))
 return canonical(out)
def models(n,cs):
 return {a for a in range(1<<n) if all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in c) for c in cs)}
def signed_bound(cs):
 q=Counter((abs(l),int(l>0)) for c in cs for l in c)
 return max(q.values(),default=0)
def run(name,n,original):
 assert len(original)*3==4*n and len(set(map(norm,original)))==len(original)
 assert all(Counter((abs(l),int(l>0)) for c in original for l in c)[(x,s)]==2 for x in range(1,n+1) for s in (0,1))
 sat=models(n,original);cs=canonical(original);rows=[]
 for r in range(3):
  p=2**(2**r);w=2+2**r;g=graph(cs)
  assert signed_bound(cs)<=p and max(map(len,cs),default=0)<=w
  I=greedy(g);assert len(I)>=math.ceil(len(g)/(1+2*p*(w-1)))
  cs=dp(cs,I);remain=sorted(graph(cs))
  proj={tuple((a>>(x-1))&1 for x in remain) for a in sat}
  after={tuple(b) for b in product((0,1),repeat=len(remain)) if all(any(b[remain.index(abs(l))]==int(l>0) for l in c) for c in cs)}
  assert proj==after
  rows.append({'round':r+1,'pivots':I,'remaining':len(remain),'clauses':len(cs),'max_width':max(map(len,cs),default=0)})
 return {'source':name,'models':len(sat),'stages':rows,'first_private_gate_saving':4*len(rows[0]['pivots'])}
F9=source(P9,N9);Y6=source(P6,N6);A9=source(PA,NA)
if __name__=='__main__':
 out=[run('F9',9,F9),run('Y6',6,Y6),run('A9',9,A9)]
 p={1:0,3:0,5:1,6:0,7:0,8:0}
 sats=models(9,F9)
 assert sum(all(((a>>(v-1))&1)==z for v,z in p.items()) for a in sats)==2
 assert sum(all(((a>>(v-1))&1)==z for v,z in {**p,1:1}.items()) for a in sats)==0
 assert 2048*9*25*161==2415*8*24*160
 print(json.dumps({'status':'PASS','bound_v3_over_n':'2048/2415','cases':out},indent=2))
