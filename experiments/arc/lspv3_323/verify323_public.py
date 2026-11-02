#!/usr/bin/env python3
"""Independent GATE323 core rank and same-original both-label verifier.
No producer import, no precomputed SAT labels, no semantic representative oracle.
The complete independent OBDD/SU/malformed verifier is in the user archive.
"""
from itertools import product
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-x for x in c) for c in N)
def linked():
 cs=[]
 for i in (0,1):
  for j,c in enumerate(F):
   row=[(1 if x>0 else -1)*(9*i+abs(x)) for x in c]
   if j==0:row[1]=9*(1-i)+5
   cs.append(tuple(row))
 return tuple(cs)
def holds(clauses,bits):
 return all(any(bits[abs(x)-1]==(1 if x>0 else 0) for x in c) for c in clauses)
def rank(a):
 a=[list(x) for x in a];pivot=0
 for j in range(len(a[0])):
  s=next((k for k in range(pivot,len(a)) if a[k][j]),None)
  if s is None:continue
  a[pivot],a[s]=a[s],a[pivot]
  for k in range(pivot+1,len(a)):
   if a[k][j]:a[k]=[v^w for v,w in zip(a[k],a[pivot])]
  pivot+=1
  if pivot==len(a):break
 return pivot
def assign(aa,left,bb,right,n):
 a=[0]*n
 for v,b in zip(left,aa):a[v-1]=b
 for v,b in zip(right,bb):a[v-1]=b
 return a
def countpins(H,p):
 n=max(abs(v) for c in H for v in c)
 free=[v for v in range(1,n+1) if v not in p]
 total=0
 for vals in product((0,1),repeat=len(free)):
  a=[0]*n
  for v,b in p.items():a[v-1]=b
  for v,b in zip(free,vals):a[v-1]=b
  total+=holds(H,a)
 return total
def main():
 K=[]
 for a in product((0,1),repeat=4):
  K.append([int(holds(F,assign(a,(1,2,3,4),b,(6,7,8,9),9))) for b in product((0,1),repeat=4)])
 assert rank(K)==9
 H=linked();left=(1,2,3,4,10,11,12,13);right=tuple(v for v in range(1,19) if v not in left)
 rows=[];count=0
 for a in product((0,1),repeat=8):
  row=[]
  for b in product((0,1),repeat=10):
   x=int(holds(H,assign(a,left,b,right,18)));count+=x;row.append(x)
  rows.append(row)
 assert count==4614 and rank(rows)==184 and len(set(map(tuple,rows)))==189
 A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0}
 PA={**A,**{v+9:b for v,b in A.items()}}
 PB={**B,**{v+9:b for v,b in A.items()}}
 assert (countpins(H,PA),countpins(H,PB))==(1,0)
 assert (countpins(F,{1:0,2:0,8:1,9:1}),countpins(F,{1:1,5:1,6:0,7:0,8:0,3:0}))==(2,0)
 print('PASS: local GF2 rank 9; G2 full rank 184; forward classes 189; source models 4614; same original SAT/UNSAT 1/0 and F9 2/0. P versus NP OPEN.')
if __name__=='__main__':main()
