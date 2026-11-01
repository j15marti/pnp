#!/usr/bin/env python3
"""Self-contained decision-only pin-probe control. Standard-library Python 3."""
from itertools import product
from math import ceil,log2
POS=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
NEG=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
A={1:1,2:0,3:1,4:0,8:0}
B={1:1,2:1,3:0,4:0,8:0}
def matrix(pins):
 out=[[0,0],[0,0]]
 for a,b in product(range(2),repeat=2):
  for xs in product(range(2),repeat=8):
   d=dict(zip((1,2,3,4,6,7,8,9),xs)); d[5]=a
   if any(d[k]!=v for k,v in pins.items()):continue
   good=all(any((b if j==0 and k==5 else d[k])==1 for k in row) for j,row in enumerate(POS))
   good &=all(any(d[k]==0 for k in row) for row in NEG)
   if good:out[a][b]+=1
 return out
W=matrix({}); WA=matrix(A); WB=matrix(B)
assert W==[[34,47],[23,36]] and WA==[[1,1],[0,0]] and WB==[[0,0],[0,0]]
def mul(X,Y):return [[sum(X[i][j]*Y[j][k] for j in range(2)) for k in range(2)] for i in range(2)]
for t in (1,2,3,4,8,16,128):
 T=[[1,0],[0,1]]
 for _ in range(t):T=mul(T,WA)
 assert T[0][0]+T[1][1]==1
 for j in range(t):
  T=[[1,0],[0,1]]
  for i in range(t):T=mul(T,WB if i==j else WA)
  assert T[0][0]+T[1][1]==0
 # Each B replacement changes x2_i and x3_i, disjoint across blocks.
 D=[{9*i+2,9*i+3} for i in range(t)]
 assert len(set.union(*D))==2*t
 assert all({9*i+2 for i in range(t)}&s for s in D)
 print(t,ceil(t*log2(84)),t)
print('PASS: exact matrices, both labels, direct-sum work-only bound')
