#!/usr/bin/env python3
"""LSPV-1 321 independent original-source referee: no producer imports."""
from collections import Counter
from itertools import permutations
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
F15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15)]
H15=F9+[tuple((abs(x)+9)*(1 if x>0 else -1) for x in c) for c in Y6]
def sat(cs,b):
 return all(any(((b>>(abs(x)-1))&1)==int(x>0) for x in c) for c in cs)
def norm(c):
 z=set(c)
 return None if any(-v in z for v in z) else tuple(sorted(z,key=lambda x:(abs(x),x<0)))
def elim(cs,x):
 p=[c for c in cs if x in c];q=[c for c in cs if -x in c]
 r=[norm(c) for c in cs if x not in c and -x not in c]
 r.extend(norm([v for v in a if v!=x]+[v for v in b if v!=-x]) for a in p for b in q)
 return sorted(set(c for c in r if c is not None))
def check(cs,n,expected):
 q=Counter(v for c in cs for v in c)
 assert len(cs)*3==4*n and all(q[x]==q[-x]==2 for x in range(1,n+1))
 adj={x:set() for x in range(1,n+1)}
 for c in cs:
  for x in map(abs,c):adj[x].update({abs(y) for y in c if abs(y)!=x})
 assert max(map(len,adj.values()))<=8
 remain=set(adj);I=[]
 while remain:
  x=min(remain);I.append(x);remain-=({x}|adj[x])
 assert len(I)>= (n+8)//9
 outputs=[]
 for order in permutations(I):
  r=cs
  for x in order:r=elim(r,x)
  outputs.append(set(r))
 assert all(s==outputs[0] for s in outputs)
 G=list(outputs[0]);R=[x for x in range(1,n+1) if x not in I]
 assert len(G)<=len(cs) and sum(map(len,G))<=3*len(cs)+4*len(I)
 models=0
 for b in range(1<<len(R)):
  mask=sum(((b>>j)&1)<<(x-1) for j,x in enumerate(R))
  good=any(sat(cs,mask|sum(((z>>j)&1)<<(x-1) for j,x in enumerate(I))) for z in range(1<<len(I)))
  assert good==sat(G,mask);models+=good
 assert models==expected
 print(n,I,len(G),sum(map(len,G)),models,'PASS')
for cs,n,m in ((Y6,6,16),(F9,9,48),(F15,15,571),(H15,15,768)):check(cs,n,m)
p={3:0,5:1,6:0,7:0,8:0}
for x,count in ((0,2),(1,0)):
 pins=dict(p);pins[1]=x
 assert sum(sat(F9,a) and all(((a>>(v-1))&1)==b for v,b in pins.items()) for a in range(512))==count
print('SAME ORIGINAL SAT2/UNSAT0 PASS. P vs NP OPEN.')
