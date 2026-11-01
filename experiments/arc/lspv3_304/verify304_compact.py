#!/usr/bin/env python3
"""GATE304 no-producer-import independent F9 SAT/UNSAT and polarity-gate verifier.
Full 21,870-state independent verifier resides in reproducibility archive."""
from itertools import product,combinations
from collections import defaultdict,Counter
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=P+[tuple(-x for x in c) for c in Q]
s=Counter((abs(v),v>0) for C in F for v in C)
assert all(s[i,sgn]==2 for i in range(1,10) for sgn in (0,1))
assert len(set(tuple(sorted(c)) for c in F))==len(F)
models=[v for v in product((0,1),repeat=9)
        if all(any(v[abs(x)-1]==int(x>0) for x in C) for C in F)]
assert len(models)==70
checked=0
for z in product((0,1,2),repeat=9):
 a={i:v for i,v in enumerate(z,1) if v!=2}
 a1=sum(a.values());a0=len(a)-a1
 cp=cn=0
 hpos=defaultdict(int);hneg=defaultdict(int);un=0;edges=[]
 for j,C in enumerate(F):
  if any(abs(x) in a and a[abs(x)]==int(x>0) for x in C):
   cp+=C[0]>0;cn+=C[0]<0
   for x in C:
    if abs(x) not in a:
     if x>0:hpos[abs(x)]+=1
     else:hneg[abs(x)]+=1
  else:
   un+=1;free=[abs(x) for x in C if abs(x) not in a]
   if len(free)==2:edges.append((j,free))
 tri=set()
 for e in combinations(edges,3):
  deg=Counter(x for _,vs in e for x in vs)
  if len(deg)==3 and set(deg.values())=={2}:tri.add(tuple(sorted(k for k,_ in e)))
 used=set();nu=0
 for E in sorted(tri):
  if not used.intersection(E):used.update(E);nu+=1
 eta=sum(min(hpos[i],hneg[i]) for i in set(hpos)|set(hneg))
 t=len(a);delta=2*(9-t)-un-eta-nu
 floor_old=6-2*t-(2*t//3)
 pin_d=max(0,(2*a1+2)//3-2*a0,(2*a0+2)//3-2*a1)
 assert delta>=floor_old+abs(cp-cn)>=floor_old+pin_d
 assert cp>=((2*a1+2)//3) and cn>=((2*a0+2)//3)
 assert cp<=2*a1 and cn<=2*a0 and eta<=2*min(cp,cn)
 if t==1:assert delta==6
 if a0==0 or a1==0:
  assert eta==0
  assert delta>=6-2*t+(2*t+2)//3-(2*t//3)
 checked+=1
assert checked==19683
A={1:1,2:0,3:1,4:0,8:0}
B={1:1,2:1,3:0,4:0,8:0}
num=lambda p:sum(all(w[k-1]==v for k,v in p.items()) for w in models)
assert num(A)==1 and num(B)==0
for i,j in combinations(range(len(F)),2):
 X,Y=F[i],F[j]
 u={abs(x):x>0 for x in X};v={abs(x):x>0 for x in Y}
 common=set(u)&set(v)
 predicted=[not any(u[k]!=v[k] for k in common),not any(u[k]==v[k] for k in common)]
 variables=sorted(set(u)|set(v));seen=set()
 for bits in product((0,1),repeat=len(variables)):
  w=dict(zip(variables,bits))
  if all(w[abs(x)]==(x>0) for x in X):xs=1
  elif all(w[abs(x)]!=(x>0) for x in X):xs=0
  else:continue
  if all(w[abs(y)]==(y>0) for y in Y):ys=1
  elif all(w[abs(y)]!=(y>0) for y in Y):ys=0
  else:continue
  seen.add((xs,ys))
 assert [(1,1) in seen,(1,0) in seen]==predicted
 assert (((0,0) in seen)==predicted[0]) and (((0,1) in seen)==predicted[1])
print("INDEPENDENT PASS F9 coherent cubes",checked,"SAT/UNSAT controls",num(A),num(B),"pair modes",264,"P vs NP OPEN")
