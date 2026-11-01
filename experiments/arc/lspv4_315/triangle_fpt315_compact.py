#!/usr/bin/env python3
"""Finite self-contained, no external packages. NOT the polynomial simple-graph oracle."""
from collections import defaultdict
from itertools import product,combinations
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
M=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=P+[tuple(-x for x in c) for c in M]
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def edges(C,vals):
 out=[]
 for j,c in enumerate(C):
  if any((z>0)==bool(vals[abs(z)-1]) for z in c if vals[abs(z)-1]!=-1):continue
  f=[abs(z) for z in c if vals[abs(z)-1]==-1]
  if not f:return None
  if len(f)==2:out.append((j,*f))
 return out
def triangles(E):
 t=[]
 for rows in combinations(E,3):
  ct={}
  for j,u,v in rows:
   ct[u]=ct.get(u,0)+1;ct[v]=ct.get(v,0)+1
  if len(ct)==3 and sorted(ct.values())==[2,2,2]:t.append(tuple(sorted(z[0] for z in rows)))
 return sorted(t)
def optimal(tris):
 best=0
 for bits in product((0,1),repeat=len(tris)):
  selected=[tris[i] for i,b in enumerate(bits) if b]
  names=[x for tri in selected for x in tri]
  if len(names)==len(set(names)):best=max(best,len(selected))
 return best
def fpt(E):
 pair={}
 for j,u,v in E:
  k=tuple(sorted((u,v)));pair[k]=min(j,pair.get(k,j))
 rep=set(pair.values());extras=set(j for j,_,_ in E)-rep
 T=triangles(E);X=[t for t in T if set(t)&extras]
 assert len(X)<=4*len(extras)
 best=0
 for bits in product((0,1),repeat=len(X)):
  Q=[X[i] for i,b in enumerate(bits) if b]
  used=[j for t in Q for j in t]
  if len(set(used))<len(used):continue
  simple=[t for t in T if set(t)<=rep and not set(t)&set(used)]
  best=max(best,len(Q)+optimal(simple))
 return best,len(extras),optimal([t for t in T if set(t)<=rep])
if __name__=='__main__':
 for name,C,n in [('F9',F,9),('Y6',Y,6)]:
  counts={'cubes':0,'admissible':0,'parallel':0,'gain':0,'max_d':0}
  for x in product((-1,0,1),repeat=n):
   counts['cubes']+=1;E=edges(C,x)
   if E is None:continue
   nu,d,nu0=fpt(E)
   assert nu==optimal(triangles(E))
   counts['admissible']+=1;counts['parallel']+=int(d>0)
   counts['gain']+=int(nu>nu0);counts['max_d']=max(counts['max_d'],d)
  print(name,counts)
  if name=='F9':assert counts=={'cubes':19683,'admissible':12683,'parallel':1535,'gain':3,'max_d':2}
  if name=='Y6':assert counts=={'cubes':729,'admissible':545,'parallel':77,'gain':0,'max_d':2}
 p={1:1,4:0,5:1,8:0}
 E=edges(F,tuple(p.get(i,-1) for i in range(1,10)))
 assert fpt(E)==(2,1,1)
 print('PASS: exact source-ID FPT reduction checked against all 20,412 coherent cubes')
