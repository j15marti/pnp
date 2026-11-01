#!/usr/bin/env python3
"""GATE305 independent finite source verifier. Does not import compact305.py.
Original-source brute force; sign-quota, complement and S/U pair tests."""
from itertools import product,combinations
from collections import Counter
P9=['156','238','135','469','247','789'];N9=['468','167','234','358','129','579']
P6=['123','145','246','356'];N6=['124','136','235','456']
def parse(P,N):
 return [tuple(int(c) for c in row) for row in P]+[tuple(-int(c) for c in row) for row in N]
def new(t):
 F=[list(C) for C in parse(P9,N9)];A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0};j=0;v=1
 for k in range(t):
  off=len(F);s=9+6*k
  F.extend([[x+s if x>0 else x-s for x in C] for C in parse(P6,N6)])
  for x,b in ((2,0),(3,1),(4,1),(6,0)):A[x+s]=B[x+s]=b
  assert v in F[j] and s+3 in F[off]
  F[j][F[j].index(v)]=s+3;F[off][F[off].index(s+3)]=v
  j=off+1;v=s+4
 return list(map(tuple,F)),A,B
def valid(F):
 if not F or any(len(C)!=3 or len({abs(l) for l in C})!=3 or len({l>0 for l in C})!=1 for C in F):return False
 n=max(abs(l) for C in F for l in C);co=Counter((abs(l),l>0) for C in F for l in C)
 return len(F)*3==4*n and len({tuple(sorted(C)) for C in F})==len(F) and all(co[i,0]==co[i,1]==2 for i in range(1,n+1))
def brute(F,p):
 n=max(abs(l) for C in F for l in C);free=[v for v in range(1,n+1) if v not in p];result=0
 for xs in product([0,1],repeat=len(free)):
  a=dict(p);a.update(zip(free,xs))
  if all(any(a[abs(l)]==(l>0) for l in C) for C in F):result+=1
 return result
def pair_modes(F):
 checked=0
 for C,D in combinations(F,2):
  for cs,ds in product((0,1),repeat=2):
   forces={};compatible=True
   for l in C:forces[abs(l)]=int(l>0) if cs else int(l<0)
   for l in D:
    v=abs(l);want=int(l>0) if ds else int(l<0)
    if v in forces and forces[v]!=want:compatible=False
    forces[v]=want
   vs=sorted(set(abs(l) for l in C+D));exists=False
   for bits in product([0,1],repeat=len(vs)):
    a=dict(zip(vs,bits))
    e=sum(a[abs(l)]==(l>0) for l in C)
    f=sum(a[abs(l)]==(l>0) for l in D)
    if (e==3 if cs else e==0) and (f==3 if ds else f==0):exists=True;break
   assert exists==compatible
   checked+=1
 return checked
assert valid(parse(P9,N9)) and valid(parse(P6,N6))
for t in (0,1,2,4):
 F,A,B=new(t);assert valid(F)
 assert brute(F,A)==4**t and brute(F,B)==0
 assert all(any(abs(l) in A and A[abs(l)]==(l>0) for l in C) for C in F[12:])
 print('independent source t=',t,'n=',9+6*t,'SAT=',4**t,'UNSAT=',0)
assert pair_modes(parse(P9,N9))==264 and pair_modes(parse(P6,N6))==112
for malformed in ([],[(1,1,2)],[(1,2,-3)],[(1,2,3)],[(1,2,3),(1,2,3)]):
 assert not valid(malformed)
print('PASS: independent finite BOTH-label, 376 S/U modes, malformed, P vs NP OPEN')
