#!/usr/bin/env python3
"""GATE308 restricted decision-continuation quotient; standalone stdlib."""
from itertools import product
from collections import Counter,defaultdict
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
E=(1,2,3,4,6,7,8,9)
good=[]
for a,b in product((0,1),repeat=2):
 for v in product((0,1),repeat=8):
  d=dict(zip(E,v));d[5]=a
  if all(any(b if j==0 and x==5 else d[x] for x in c) for j,c in enumerate(P)) and all(any(not d[x] for x in c) for c in N):good.append((a,b,v))
assert len(good)==140
def matrix(pattern):
 c=[0]*4
 for a,b,v in good:
  if all(p<0 or p==w for p,w in zip(pattern,v)):c[2*a+b]+=1
 return tuple(c)
def sup(c):return ''.join('1' if x else '0' for x in c)
def mul(A,B):return ''.join('1' if any(A[2*i+k]=='1' and B[2*k+j]=='1' for k in (0,1)) else '0' for i in (0,1) for j in (0,1))
def accept(A):return A[0]=='1' or A[3]=='1'
h=Counter(sup(matrix(p)) for p in product((-1,0,1),repeat=8))
assert h=={'0000':2245,'0001':281,'0011':471,'0100':186,'0101':278,'1100':852,'1101':15,'1111':2233}
monoid={'1001'}
while True:
 nxt=monoid|{mul(a,b) for a in monoid for b in h}
 if nxt==monoid:break
 monoid=nxt
assert len(monoid)==9
classes=defaultdict(list)
for a in monoid:classes[tuple(accept(mul(a,b)) for b in sorted(monoid))].append(a)
assert len(classes)==6
assert len({tuple(accept(mul(a,b)) for b in sorted(monoid)) for a in monoid if a!='1001'})+1==7
pin0=(-1,)*8
pin1=tuple(1 if x in (7,9) else -1 for x in E)
q=tuple(0 if x in (4,6,7) else -1 for x in E)
A,B,C=matrix(pin0),matrix(pin1),matrix(q)
assert (sup(A),sup(B),sup(C))==('1111','1100','0101')
integer=lambda X,Y:tuple(sum(X[2*i+k]*Y[2*k+j] for k in (0,1)) for i in (0,1) for j in (0,1))
assert sum(integer(A,C)[i] for i in (0,3))==154
assert sum(integer(B,C)[i] for i in (0,3))==0
print('PASS: 6561 patterns; 8 local supports; 9 products; 6 continuation classes; 7 DFA states; G2 SAT/UNSAT 154/0')
