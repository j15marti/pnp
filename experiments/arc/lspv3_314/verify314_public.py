#!/usr/bin/env python3
"""GATE314 separate no-producer-import mask-based checks, source grammar and SAT/UNSAT."""
from itertools import product,combinations
A={2:1,3:0,5:1,6:0,8:0};B={2:0,3:1,5:1,6:1,8:0};R={1:1,7:0}
plus=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
minus=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
def formula(t):
 rows=[]
 for i in range(t):
  for k in range(12):
   row=(plus+minus)[k];sgn=1 if k<6 else -1
   rows.append(tuple(sgn*(9*((i+1)%t)+x) if k==0 and x==1 else sgn*(9*i+x) for x in row))
 return rows
def evaluate(t,word,additional=()):
 f=formula(t);required={9*i+x:v for i,ch in enumerate(word) for x,v in (A if ch=='a' else B).items()}
 for i in additional:required.update({9*i+x:v for x,v in R.items()})
 free=[x for x in range(1,9*t+1) if x not in required];n=0
 for v in range(1<<len(free)):
  value=sum(b<<(k-1) for k,b in required.items())
  value|=sum(((v>>j)&1)<<(k-1) for j,k in enumerate(free))
  n+=all(any(((value>>(abs(z)-1))&1)==int(z>0) for z in row) for row in f)
 return n
for t in (1,2,3):
 f=formula(t);assert len(f)==12*t
 assert len(set(tuple(sorted(c)) for c in f))==len(f)
 assert all(len({abs(z) for z in c})==3 and (all(z>0 for z in c) or all(z<0 for z in c)) for c in f)
 assert all(sum(i in c for c in f)==2 and sum(-i in c for c in f)==2 for i in range(1,9*t+1))
 for word in product('ab',repeat=t):
  assert evaluate(t,word)==4**t
  for i in range(t):
   assert evaluate(t,word,(i,))==(0 if word[i]=='a' else 4**(t-1))
  assert evaluate(t,word,range(t))==int(all(x=='b' for x in word))
 print('independent',t,'PASS')
print('P versus NP OPEN')
