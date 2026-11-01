#!/usr/bin/env python3
"""GATE305 compact connected canonical M22 both-label and dual-IE check.
Classic clause inclusion-exclusion, not a new general SAT algorithm."""
from itertools import product
from collections import Counter
F9p=['156','238','135','469','247','789']
F9n=['468','167','234','358','129','579']
Yp=['123','145','246','356'];Yn=['124','136','235','456']
def source(P,N):return [tuple(map(int,c)) for c in P]+[tuple(-int(x) for x in c) for c in N]
def chain(t):
 F=[list(c) for c in source(F9p,F9n)];A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0};last=(0,1)
 for i in range(t):
  shift=9+6*i;off=len(F)
  F.extend([[x+shift if x>0 else x-shift for x in C] for C in source(Yp,Yn)])
  for x,b in ((2,0),(3,1),(4,1),(6,0)):A[shift+x]=B[shift+x]=b
  j,x=last;F[j][F[j].index(x)]=shift+3;F[off][F[off].index(shift+3)]=x
  last=(off+1,shift+4)
 return [tuple(c) for c in F],A,B
def valid(F):
 n=max(abs(l) for C in F for l in C);o=Counter((abs(l),l>0) for C in F for l in C)
 return all(len(C)==3 and len({abs(l) for l in C})==3 and len({l>0 for l in C})==1 for C in F) and len({tuple(sorted(C)) for C in F})==len(F) and all(o[i,True]==o[i,False]==2 for i in range(1,n+1))
def count(F,p):
 n=max(abs(l) for C in F for l in C);free=n-len(p)
 R=[tuple(l for l in C if abs(l) not in p) for C in F if not any(abs(l) in p and p[abs(l)]==(l>0) for l in C)]
 total=0
 for pick in product((False,True),repeat=len(R)):
  fixed={};ok=True
  for use,C in zip(pick,R):
   if use:
    for lit in C:
     v=abs(lit);bit=int(lit<0)
     if v in fixed and fixed[v]!=bit:ok=False;break
     fixed[v]=bit
   if not ok:break
  if ok:total+=(-1 if sum(pick)&1 else 1)*(1<<(free-len(fixed)))
 return total,len(R)
for t in (0,1,2,4,8,16,32,64):
 F,A,B=chain(t);assert valid(F);ca,qa=count(F,A);cb,qb=count(F,B)
 assert (ca,cb,qa,qb)==(4**t,0,5,5)
 print('t=',t,'n=',9+6*t,'free=',4+2*t,'q=',qa,'SAT_models=',ca,'UNSAT_models=',cb)
print('PASS: restricted, both-label, P versus NP OPEN')
