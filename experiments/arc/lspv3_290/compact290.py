#!/usr/bin/env python3
"""GATE290 minimal independent Pasch-trade reproducer; stdlib only."""
from itertools import combinations, product
from fractions import Fraction
P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,5),(2,3,6),(4,5,6))
A=P+tuple(tuple(-v for v in row) for row in Q)
B=Q+tuple(tuple(-v for v in row) for row in Q)
def cost(F,a):
 return sum(not any(a[abs(x)-1]==int(x>0) for x in row) for row in F)
def mean(F,p):
 matching=[a for a in product((0,1),repeat=6) if all(a[i-1]==v for i,v in p.items())]
 return Fraction(sum(cost(F,a) for a in matching),len(matching))
def pair_counts(F):
 return {ij:sum(all(x in tuple(map(abs,row)) for x in ij) for row in F) for ij in combinations(range(1,7),2)}
assert pair_counts(A)==pair_counts(B)
for F in (A,B):
 assert len(set(map(tuple,F)))==8
 assert all(sum(i in row for row in F)==sum(-i in row for row in F)==2 for i in range(1,7))
for a in product((0,1),repeat=6):
 z=[1-2*x for x in a]
 assert 8*(cost(A,a)-cost(B,a))==(z[2]-z[3])*(z[0]-z[5])*(z[1]-z[4])
nseed=0
for k in (0,1,2):
 for ix in combinations(range(1,7),k):
  for val in product((0,1),repeat=k):
   p=dict(zip(ix,val))
   assert mean(A,p)==mean(B,p)
   nseed+=1
assert nseed==73
ma=sum(cost(A,a)==0 for a in product((0,1),repeat=6))
mb=sum(cost(B,a)==0 for a in product((0,1),repeat=6))
assert (ma,mb)==(22,18)
assert cost(A,(1,1,1,0,0,0))==0 and cost(B,(1,1,1,0,0,0))==1
print({"status":"PASS","pair_seed_tests":nseed,"complete_rows":64,"SAT_models_A":ma,"SAT_models_B":mb,"P_vs_NP":"OPEN"})
