#!/usr/bin/env python3
"""Independent standard-library-only FLMV and strict22 original-source adversarial check."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
C=F(241,200);D=((C+2)/C**2-C)/2
assert D==F(11642479,23232400)>F(1,2)
# f3 explicitly derived, not computed through the main recurrence loop.
f3=C**3/(C*C+C+2)
assert D>min(2/C-C,1/C)
assert D>min((1/f3-C)/3,1/C**3)
assert D>C**(-4) # certifies every later index using d_j <= c^(-j)
P=lambda z:z**3+z*z-z-2
assert P(F(1205569,1000000))<0<P(F(1205570,1000000))
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
A=[tuple(map(int,s.split())) for s in W1.split(';')]
B=[list(c) for c in A]
assert B[7][0]==1 and B[19][0]==-1
B[7][0]=-1;B[19][0]=1
assert all(set(map(abs,a))==set(map(abs,b)) for a,b in zip(A,B))
for clauses in (A,B):
 signs=Counter(l for c in clauses for l in c)
 assert len(clauses)==20
 assert all(signs[i]==signs[-i]==2 for i in range(1,16))
def ltrue(l,mask):return ((mask>>(abs(l)-1))&1)==int(l>0)
def nt(c,mask):return sum(ltrue(l,mask) for l in c)
models=[];complement_checks=0;pair_checks=0;cube_checks=0
for clauses in (A,B):
 total=0
 for mask in range(1<<15):
  ts=[nt(c,mask) for c in clauses]
  rev=[nt(c,((1<<15)-1)^mask) for c in clauses]
  assert all(x+y==3 for x,y in zip(ts,rev))
  complement_checks+=len(clauses)
  if min(ts)>0:total+=1
 models.append(total)
 for mask,expect in [(0,[1,10,7,2]),((1<<15)-1,[2,7,10,1])]:
  ts=[nt(c,mask) for c in clauses]
  assert [ts.count(i) for i in range(4)]==expect
 for i,c in enumerate(clauses):
  S={abs(l):int(l>0) for l in c}
  U={abs(l):int(l<0) for l in c}
  assert all(S[v]==1-U[v] for v in S)
  for d in clauses[:i]:
   D={abs(l):int(l>0) for l in d}
   same=sum(D[v]==S[v] for v in S.keys()&D.keys())
   opposite=sum(D[v]!=S[v] for v in S.keys()&D.keys())
   expected={'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite}
   variables=sorted(set(map(abs,c+d)))
   seen=dict.fromkeys(expected,False)
   for flags in product((0,1),repeat=len(variables)):
    v=dict(zip(variables,flags))
    tc=sum(v[abs(l)]==int(l>0) for l in c)
    td=sum(v[abs(l)]==int(l>0) for l in d)
    if tc==3 and td==3:seen['SS']=True
    if tc==0 and td==0:seen['UU']=True
    if tc==3 and td==0:seen['US']=True
    if tc==0 and td==3:seen['SU']=True
   assert seen==expected
   pair_checks+=4
 for t in (0,1,2,4,8):
  for vals in product((0,1),repeat=t):
   a=dict(zip(range(1,t+1),vals))
   gone=sum(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in clauses)
   assert gone<=2*t
   cube_checks+=1
assert models==[0,168]
print({'status':'PASS','c':'241/200','d':str(D),'k_star':2,
       'W1_and_signed_swap_models':models,'complement_occurrences':complement_checks,
       'pair_modes':pair_checks,'cofactor_cubes':cube_checks})
