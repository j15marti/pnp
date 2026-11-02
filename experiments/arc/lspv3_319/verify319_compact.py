#!/usr/bin/env python3
"""No-import independent verifier of GATE319 F9/G2 cofactor claims."""
from itertools import product
from collections import Counter
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=tuple(P)+tuple(tuple(-x for x in row) for row in N)
def good(cnf,n):
 if len(cnf)*3!=n*4:return False
 ct=Counter();seen=set()
 for c in cnf:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or any(not(0<abs(x)<=n) for x in c) or len(set(x>0 for x in c))!=1:return False
  sig=tuple(sorted(c))
  if sig in seen:return False
  seen.add(sig)
  for x in c:ct[x]+=1
 return all(ct[i]==ct[-i]==2 for i in range(1,n+1))
def v(cnf,a):
 for j,c in enumerate(cnf):
  if not any(a[abs(x)]==int(x>0) for x in c):return 0,j
 return 1,None
def enum(cnf,n,pins):
 free=tuple(i for i in range(1,n+1) if i not in pins)
 count=0;dead=Counter()
 for bits in product((0,1),repeat=len(free)):
  a=dict(pins);a.update(zip(free,bits))
  sat,j=v(cnf,a);count+=sat
  if not sat:dead[j]+=1
 return count,dead
assert good(F,9)
assert not good(F+(F[0],),9) and not good(((1,1,2),)+F[1:],9)
assert enum(F,9,{})[0]==70
p={1:0,3:0,5:1,6:0,7:0,8:0};q=dict(p);q[1]=1
assert enum(F,9,p)[0]==2 and enum(F,9,q)[0]==0
# Independent F9 signed S/U extreme compatibility.
su=Counter()
for i in range(12):
 for j in range(i+1,12):
  for s,t in product((0,1),repeat=2):
   desired={};ok=True
   for c,k in ((F[i],s),(F[j],t)):
    for x in c:
     b=int((x>0)==bool(k));z=abs(x)
     if z in desired and desired[z]!=b:ok=False
     desired[z]=b
   if ok:su['S' if s else 'U','S' if t else 'U']+=1
assert sorted(su.values())==[37,37,49,49]
# Every source-clause frontier collision must agree for all suffix contexts.
checks=0
for order in (tuple(range(1,10)),tuple(range(9,0,-1))):
 for k in range(10):
  prefix=order[:k];suffix=order[k:];seen={}
  X=set(prefix)
  frontier=[j for j,c in enumerate(F) if set(map(abs,c))&X and set(map(abs,c))-X]
  for bits in product((0,1),repeat=k):
   a=dict(zip(prefix,bits));dead=any(all(abs(x) in X for x in c) and not any(a[abs(x)]==int(x>0) for x in c) for c in F)
   mask=tuple(any(a[abs(x)]==int(x>0) for x in F[j] if abs(x) in X) for j in frontier)
   vector=[]
   for tail in product((0,1),repeat=len(suffix)):
    b=dict(a);b.update(zip(suffix,tail));vector.append(v(F,b)[0]);checks+=1
   sig=(dead,mask)
   if sig in seen:assert seen[sig]==vector
   else:seen[sig]=vector
# Connected same-original source, check every assignment independently.
G=[]
for block in range(2):
 for j,c in enumerate(P):
  row=[9*block+x for x in c]
  if j==0:row[0]=9*((block+1)%2)+1
  G.append(tuple(row))
 for c in N:G.append(tuple(-9*block-x for x in c))
assert good(G,18)
assert enum(G,18,{})[0]==3878
print({'verified':True,'source_SAT':2,'source_UNSAT':0,'F9_models':70,'G2_models':3878,'F9_su_modes':sum(su.values()),'suffix_tests':checks})
