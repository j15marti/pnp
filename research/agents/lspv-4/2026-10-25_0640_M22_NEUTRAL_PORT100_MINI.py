#!/usr/bin/env python3
"""M22-NEUTRAL-PORT100: portable independent checker, stdlib only."""
from itertools import product
from collections import Counter
import json
P=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Q=[(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
Y=P+Q
H=P+[tuple(-v for v in c) for c in P]
checks=0
def ok(x):
 global checks
 checks+=1
 assert x
def sat(F,a):
 return all(any(a[abs(x)-1] if x>0 else not a[-x-1] for x in C) for C in F)
def models(F,k):
 return sum(sat(F,a) for a in product((0,1),repeat=k))
def valid(F):
 s=set()
 c=Counter()
 for C in F:
  if len(C)!=3 or len({abs(v) for v in C})!=3:return False
  if not(all(v>0 for v in C) or all(v<0 for v in C)):return False
  z=tuple(sorted(C))
  if z in s:return False
  s.add(z)
  for v in C:c[(abs(v),v>0)]+=1
 return bool(F) and all(c[(v,True)]==c[(v,False)]==2 for v,_ in c)
def unpaired(F):
 s={tuple(sorted(C)) for C in F}
 return valid(F) and any(tuple(sorted(-v for v in C)) not in s for C in F)
def gadget(ports,k,negative=False):
 x,y,z=ports
 a,b,c,d,e,f=range(k+1,k+7)
 G=[(a,y,z),(x,b,c),(a,d,e),(b,d,f),(c,e,f),
    (-a,-b,-d),(-a,-c,-f),(-b,-c,-e),(-d,-e,-f)]
 return [tuple(-v for v in C) for C in G] if negative else G
def repair(F,k,j):
 C=F[j]
 G=gadget(tuple(abs(v) for v in C),k,C[0]<0)
 O=F[:j]+F[j+1:]+G
 ok(valid(O) and unpaired(O))
 return O,k+6
ok(valid(Y) and valid(H))
ok(unpaired(Y) and not unpaired(H))
ok(models(Y,6)==20 and models(H,6)==18)
Ptable=[];Ntable=[]
for sgn in (False,True):
 row=[]
 G=gadget((1,2,3),3,sgn)
 for o in product((0,1),repeat=3):
  sols=[f for f in product((0,1),repeat=6) if sat(G,o+f)]
  ok(bool(sols))
  row.append(len(sols))
 if sgn:Ntable=row
 else:Ptable=row
ok(Ptable==[6,16,16,16,10,23,23,23])
ok(Ntable==list(reversed(Ptable)))
single=0
for F in (Y,H):
 for j,C in enumerate(F):
  G,n=repair(F,6,j)
  count=models(G,n)
  table=Ntable if C[0]<0 else Ptable
  expected=0
  for a in product((0,1),repeat=6):
   if sat(F[:j]+F[j+1:],a):
    bits=tuple(a[abs(v)-1] for v in C)
    idx=bits[0]*4+bits[1]*2+bits[2]
    expected+=table[idx]
  ok(count==expected)
  single+=1
pairs=0
for i in range(8):
 for j in range(8):
  if i==j:continue
  F,k=repair(Y,6,i)
  j2=j if j<i else j-1
  F,k=repair(F,k,j2)
  ok(k==18 and len(F)==24)
  pairs+=1
masks=0
for mask in range(1,256):
 retained=[C for j,C in enumerate(Y) if not (mask>>j)&1]
 additions=[]
 d=0
 for j,C in enumerate(Y):
  if (mask>>j)&1:
   additions+=gadget(tuple(abs(v) for v in C),6+6*d,C[0]<0)
   d+=1
 O=retained+additions
 ok(valid(O) and unpaired(O))
 ok(len(O)==8+8*d)
 masks+=1
for k in (6,9,12,198,204,512,1023):
 if k%3:continue
 m=4*k//3
 for d in (1,2,10):
  w=k.bit_length();kk=k+6*d;ww=kk.bit_length()
  N=lambda K,M:3*K.bit_length()+2+3*M*(K.bit_length()+1)
  ok(N(kk,m+8*d)-N(k,m)==3*(m+1)*(ww-w)+24*d*(ww+1))
  ok(N(kk,m+8*d)>N(k,m))
print(json.dumps({"run":"M22-NEUTRAL-PORT100-MINI","checks":checks,
 "status":"PASS","Y_models":20,"H_models":18,
 "port_counts_positive":Ptable,"port_counts_negative":Ntable,
 "single_repairs":single,"two_level_ordered_pairs":pairs,
 "nonempty_deletion_masks":masks,
 "scope":"original clause-deletion and type-only repair, not a SAT all-input contraction"},indent=2))
