#!/usr/bin/env python3
from itertools import product
from collections import Counter
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
K=(1,2,3,4,8)
X=(0,0,0,0,1);Y=(0,0,0,1,1);C=(0,0,1,0,1)
def matrix(pin):
 o=[[0,0],[0,0]]
 for a,b in product((0,1),repeat=2):
  for bits in product((0,1),repeat=8):
   d=dict(zip((1,2,3,4,6,7,8,9),bits));d[5]=a
   if any(d[k]!=v for k,v in pin.items()):continue
   if all(any((b if j==0 and v==5 else d[v])==1 for v in row) for j,row in enumerate(P)) and all(any(d[v]==0 for v in row) for row in M):o[a][b]+=1
 return o
def mul(A,B):
 return [[sum(A[i][k]*B[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)]
def tr(A):return A[0][0]+A[1][1]
m={v:matrix(dict(zip(K,v))) for v in product((0,1),repeat=5)}
A,B,D,U=m[X],m[Y],m[C],matrix({})
assert (A,B,D,U)==([[0,0],[1,1]],[[0,0],[0,3]],[[2,3],[0,0]],[[34,47],[23,36]])
assert [tr(mul(A,U)),tr(mul(B,U)),tr(mul(A,D)),tr(mul(B,D))]==[83,108,3,0]
assert len({tuple(int(x>0) for row in y for x in row) for y in m.values()})==6
print("PASS: current SAT 83/108, same-context SAT/UNSAT 3/0, six support classes")
