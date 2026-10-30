#!/usr/bin/env python3
"""Independent standard-library-only exhaustive W1/W1' and H1 controls."""
from collections import Counter
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
F=[tuple(map(int,c.split())) for c in W1.split(';')]
G=[list(c) for c in F]
assert G[7][0]==1 and G[19][0]==-1
G[7][0]=-1;G[19][0]=1
def true(l,a): return ((a>>(abs(l)-1))&1)==int(l>0)
def hist(A,a):
 t=[sum(true(l,a) for l in c) for c in A]
 return [t.count(k) for k in range(4)]
def signed22(A):
 ct=Counter(l for c in A for l in c)
 return len(A)==20 and all(ct[v]==ct[-v]==2 for v in range(1,16))
assert signed22(F) and signed22(G)
assert all(set(map(abs,c))==set(map(abs,d)) for c,d in zip(F,G))
assert hist(F,0)==hist(G,0)==[1,10,7,2]
assert hist(F,(1<<15)-1)==hist(G,(1<<15)-1)==[2,7,10,1]
models=[0,0]
for i,A in enumerate((F,G)):
 for a in range(1<<15):
  if all(any(true(l,a) for l in c) for c in A):models[i]+=1
  assert hist(A,a)==hist(A,((1<<15)-1)^a)[::-1]
  for v in range(1,16):
   assert any(true(l,a) for c in A for l in c if abs(l)==v)
assert models==[0,168]
assert all(any(true(l,97) for l in c) for c in G)
H=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]
def nfalse(a):return sum(not any(true(l,a) for l in c) for c in H)
assert nfalse(0)==nfalse(63)==1
assert all(nfalse(1<<i)==nfalse(63^(1<<i))==1 for i in range(6))
assert [nfalse(a) for a in [0,1,9,41]]==[1,1,1,0]
print({'status':'PASS','models_W1_W1prime':models,'signed22':True,'shared_unsigned_scopes':True,'H1_flips':[1,4,6]})
