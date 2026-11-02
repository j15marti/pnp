#!/usr/bin/env python3
"""GATE314 compact check: connected canonical F9 splice, identical first marginals, two-pin divergence."""
from itertools import product
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
M=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
p={2:1,3:0,5:1,6:0,8:0};q={2:0,3:1,5:1,6:1,8:0};r={1:1,7:0}
def H(t):
 c=[]
 for i in range(t):
  for j,row in enumerate(P):c.append(tuple(9*((i+1)%t)+(x) if j==0 and x==1 else 9*i+x for x in row))
  for row in M:c.append(tuple(-(9*i+x) for x in row))
 return c
def pins(word):return {9*i+x:b for i,s in enumerate(word) for x,b in (p if s=='p' else q).items()}
def count(F,t,pa):
 free=[x for x in range(1,9*t+1) if x not in pa]
 ans=0
 for v in product((0,1),repeat=len(free)):
  a={**pa,**dict(zip(free,v))}
  ans+=all(any(a[abs(z)]==int(z>0) for z in row) for row in F)
 return ans
for t in (1,2,3):
 F=H(t);assert len(F)==12*t and len(set(map(tuple,map(sorted,F))))==12*t
 assert all(sum(x in row for row in F)==2 and sum(-x in row for row in F)==2 for x in range(1,9*t+1))
 for bits in product('pq',repeat=t):
  word=''.join(bits);a=pins(word)
  assert count(F,t,a)==4**t
  for i in range(t):
   for x,marg in [(1,(3,1)),(4,(1,3)),(7,(2,2)),(9,(2,2))]:
    assert [count(F,t,{**a,9*i+x:v}) for v in (0,1)]==[z*4**(t-1) for z in marg]
   assert count(F,t,{**a,**{9*i+x:v for x,v in r.items()}})==(0 if word[i]=='p' else 4**(t-1))
  assert count(F,t,{**a,**{9*i+x:v for i in range(t) for x,v in r.items()}})==int(word=='q'*t)
 print('H'+str(t),'PASS',2**t,'profile words, 9t vars, 12t clauses')
print('Restricted only. P versus NP OPEN.')
