#!/usr/bin/env python3
"""Independent mask-based verifier of finite NAE-energy invariance and strict22 SAT/UNSAT twin; stdlib only."""
from collections import Counter
from itertools import combinations
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
F=[tuple(map(int,c.split())) for c in W1.split(';')]
T={0,1,2,4,7,9,12,14,16,17}
G=[tuple(-l if j in T else l for l in c) for j,c in enumerate(F)]
assert len(F)==len(G)==20
assert len(set(F))==len(F) and len(set(G))==len(G)
assert all(set(map(abs,c))==set(map(abs,d)) for c,d in zip(F,G))
def connected(Q):
 n=15;seen={1};stack=[1];clauses_seen=set()
 while stack:
  v=stack.pop()
  for j,c in enumerate(Q):
   if any(abs(l)==v for l in c):
    clauses_seen.add(j)
    for l in c:
     if abs(l) not in seen:seen.add(abs(l));stack.append(abs(l))
 return len(seen)==n and len(clauses_seen)==len(Q)
assert connected(F) and connected(G)
for Q in (F,G):
 c=Counter(l for C in Q for l in C)
 assert all(c[i]==c[-i]==2 for i in range(1,16))
assert all(sum(i in F[j] for j in T)==sum(-i in F[j] for j in T)==1 for i in range(1,16))

def bitmasks(C):
 var=sum(1<<(abs(l)-1) for l in C)
 u=sum(1<<(abs(l)-1) for l in C if l<0)
 return var,u,var^u

Fbits=list(map(bitmasks,F));Gbits=list(map(bitmasks,G))
models=[0,0];ehist=Counter();minE=100
for mask in range(32768):
 unf=sum((mask&v)==u for v,u,s in Fbits)
 allf=sum((mask&v)==s for v,u,s in Fbits)
 ung=sum((mask&v)==u for v,u,s in Gbits)
 allg=sum((mask&v)==s for v,u,s in Gbits)
 assert unf+allf==ung+allg
 assert unf==sum(((mask^32767)&v)==s for v,u,s in Fbits) # independent complement identity
 models[0]+=int(unf==0);models[1]+=int(ung==0)
 ehist[unf+allf]+=1;minE=min(minE,unf+allf)
assert models==[0,270]
assert minE==2
assert all((26&v)!=u for v,u,s in Gbits)
assert ehist==Counter({2:672,3:3008,4:7840,5:10176,6:7136,7:3136,8:736,9:64})

def four(C,D):
 s=[]
 for modeA,modeB in [('S','S'),('S','U'),('U','S'),('U','U')]:
  demands={};ok=True
  for clause,mode in ((C,modeA),(D,modeB)):
   for l in clause:
    val=int(l>0)==(mode=='S')
    if abs(l) in demands and demands[abs(l)]!=val:ok=False
    demands[abs(l)]=val
  s.append(ok)
 return tuple(s)
fourF=Counter();fourG=Counter();different=0
for i,j in combinations(range(20),2):
 u=four(F[i],F[j]);v=four(G[i],G[j]);fourF[u]+=1;fourG[v]+=1;different+=int(u!=v)
assert fourF==fourG and different==26
print({'result':'PASS','models':models,'n':15,'m':20,'distinct':True,'strict22':True,'balanced_phase_set':sorted(T),'all_complete_assignments_checked_per_source':32768,'min_E':minE,'E_counts':dict(ehist),'indexed_pair_modes_different':different,'pair_histograms_same':True,'witness_mask':26})
