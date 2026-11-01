#!/usr/bin/env python3
"""Compact independent recomputation of MULTIPIN-SIGNED-FLUX306.
Full producer, no-import verifier and 338770-check trace: reproducibility ZIP.
No general computational hardness conclusion follows.
"""
from itertools import product
from collections import Counter
POS=((1,6,7),(1,2,3),(2,4,5),(3,4,5),(6,8,9),(7,8,9))
NEG=((2,8,9),(1,2,3),(1,4,5),(3,4,5),(6,7,8),(6,7,9))
F=tuple(POS)+tuple(tuple(-x for x in c) for c in NEG)
def valid(F,n):
 if len(F)*3!=n*4:return False
 counts=Counter(v for clause in F for v in clause)
 return (len(set(tuple(sorted(c)) for c in F))==len(F)
         and all(len(c)==3 and len(set(map(abs,c)))==3
                 and (all(x>0 for x in c) or all(x<0 for x in c))
                 and all(1<=abs(x)<=n for x in c) for c in F)
         and all(counts[x]==counts[-x]==2 for x in range(1,n+1)))
def audit(F,n,p):
 assert valid(F,n)
 free={x for x in range(1,n+1) if x not in p}
 adj={x:set() for x in free}; tagged=[]
 for j,c in enumerate(F):
  sat=any(abs(x) in p and p[abs(x)]==int(x>0) for x in c)
  rem={abs(x) for x in c if abs(x) in free}
  if not sat:
   for x in rem:adj[x]|=rem-{x}
  tagged.append((j,c,sat,rem))
 groups=[]
 while adj:
  x=next(iter(adj));todo=[x];C=set()
  while todo:
   y=todo.pop()
   if y not in adj:continue
   C.add(y);todo.extend(adj.pop(y))
  groups.append(C)
 rows=[]
 for C in groups:
  A={'+':0,'-':0}; H={'+':0,'-':0}; U={'+':0,'-':0}
  for _,clause,sat,rem in tagged:
   s='+' if clause[0]>0 else '-'
   if sat:A[s]+=len(C&rem)
   elif rem&C:
    assert rem<=C
    U[s]+=1;H[s]+=3-len(rem)
  v=len(C)
  assert all(3*U[s]-H[s]==2*v-A[s] for s in ['+','-'])
  bp=A['+']+H['-'];bm=A['-']+H['+']
  assert bp-bm==3*(U['-']-U['+'])
  rows.append((C,bp,bm))
 return rows
def sat_count(F,n,p):
 rest=[x for x in range(1,n+1) if x not in p]
 return sum(all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
  for vs in product((0,1),repeat=len(rest))
  for a in [{**p,**dict(zip(rest,vs))}])
def main():
 assert valid(F,9)
 assert not valid(F[:-1],9)
 assert not valid(F[:-1]+(F[0],),9)
 p={6:1,7:1,8:0,9:0}
 r=audit(F,9,p)
 assert r==[({1,2,3,4,5},1,1)],r
 assert sat_count(F,9,p)==14
 checked=0
 for state in product((0,1,2),repeat=9):
  p={i+1:x for i,x in enumerate(state) if x!=2}
  rr=audit(F,9,p)
  if p:
   assert len(rr)<=3*len(p)
   assert sum(b+c for _,b,c in rr)<=6*len(p)
   assert all(b+c>=2 for _,b,c in rr)
   if len(set(p.values()))==1:
    assert len(rr)<=2*len(p)
    assert all(b+c>=3 for _,b,c in rr)
  checked+=1
 print({'all_pin_states':checked,'mixed_boundary':(1,1),
        'pinned_models':14,'theorem':'restricted exact','P_vs_NP':'OPEN'})
if __name__=='__main__':main()
