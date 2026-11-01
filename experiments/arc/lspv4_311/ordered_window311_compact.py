#!/usr/bin/env python3
"""LSPV-4 311: exact sharp cyclic-window theorem, standalone compact check."""
from collections import Counter
from itertools import product
import json
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
PINS={'A':{2:1,6:0,7:1,9:1},'B':{1:0,3:0,6:0},
      'C':{4:0,6:0},'D':{1:0,3:0}}
def local(pins):
  M=[[0,0],[0,0]]
  for a,b in product((0,1),repeat=2):
    for bits in product((0,1),repeat=8):
      v=dict(zip((1,2,3,4,6,7,8,9),bits));v[5]=a
      if any(v[x]!=y for x,y in pins.items()):continue
      if all(any((b if j==0 and x==5 else v[x])==1 for x in c) for j,c in enumerate(P)) and all(any(v[x]==0 for x in c) for c in N):M[a][b]+=1
  return M
def mul(A,B):return [[sum(A[i][j]*B[j][h] for j in (0,1)) for h in (0,1)] for i in (0,1)]
def prod(s,m):
  x=[[1,0],[0,1]]
  for c in s:x=mul(x,m[c])
  return x
def hist(s,r):return Counter(tuple(s[(i+j)%len(s)] for j in range(r)) for i in range(len(s)))
m={c:local(p) for c,p in PINS.items()}
assert m=={'A':[[0,2],[0,0]],'B':[[0,0],[0,10]],'C':[[3,9],[0,3]],'D':[[0,0],[8,18]]}
assert local({})==[[34,47],[23,36]]
results=[]
for k in (0,1,2,3,4,5,8,16):
  s=''.join(x+'C'*k for x in 'ABCBDC');u=''.join(x+'C'*k for x in 'ABDCBC')
  assert len(s)==len(u)==6*(k+1)
  assert all(hist(s,r)==hist(u,r) for r in range(1,2*k+3))
  assert hist(s,2*k+3)!=hist(u,2*k+3)
  S=prod(s,m);U=prod(u,m)
  assert S[0][0]+S[1][1]==14400*3**(6*k)
  assert U[0][0]+U[1][1]==0
  for q in (2,3):
    PS=prod(s*q,m);PU=prod(u*q,m)
    assert PS[0][0]+PS[1][1]==(14400*3**(6*k))**q
    assert PU[0][0]+PU[1][1]==0
  results.append({'k':k,'block_count':len(s),'equal_windows_through':2*k+2,
                  'first_mismatch':2*k+3,'sat_models':str(S[0][0]+S[1][1]),'unsat_models':0})
print(json.dumps({'status':'PASS','LSPV4_311':results,'P_vs_NP':'OPEN'},indent=2))
