#!/usr/bin/env python3
"""Independent no-import verifier of sign-squared DP bound and A9 gate lower bound."""
from itertools import product,combinations
from fractions import Fraction
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
A=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(-1,-5,-9),(-2,-6,-7),(-3,-4,-8),(-1,-6,-8),(-2,-4,-9),(-3,-5,-7))
def truth(cs,a):return all(any((a[abs(l)] if isinstance(a,dict) else a[abs(l)-1])==int(l>0) for l in c) for c in cs)
def cnf(c):
 a=set(c)
 return None if any(-x in a for x in a) else frozenset(a)
def elim(cs,x):
 p=[set(c) for c in cs if x in c];q=[set(c) for c in cs if -x in c]
 out={frozenset(c) for c in cs if x not in c and -x not in c}
 for a in p:
  for b in q:
   c=cnf((a-{x})|(b-{-x}))
   if c is not None:out.add(c)
 return tuple(out)
def get_adj(cs):
 d={abs(z):set() for c in cs for z in c}
 for c in cs:
  for x,y in combinations((abs(z) for z in c),2):d[x].add(y);d[y].add(x)
 return d
def greedy(cs):
 g=get_adj(cs);chosen=[]
 for x in sorted(g):
  if all(x!=v and x not in g[v] for v in chosen):chosen.append(x)
 return chosen
def verify(cs,n,expected):
 orig={a for a in product((0,1),repeat=n) if truth(cs,a)}
 assert len(orig)==expected
 for phase in range(3):
  adj=get_adj(cs);I=greedy(cs);bound=1+2*(2**(2**phase))*(1+2**phase)
  assert len(I)*bound>=len(adj)
  for x in I:cs=elim(cs,x)
  alive=sorted(get_adj(cs));observed={tuple(a[v-1] for v in alive) for a in orig}
  computed={b for b in product((0,1),repeat=len(alive)) if truth(cs,{v:b[j] for j,v in enumerate(alive)})}
  assert observed==computed
 return len(alive)
assert Fraction(8,9)*Fraction(24,25)*Fraction(160,161)==Fraction(2048,2415)
assert Fraction(2048,2415)<Fraction(64,75)*Fraction(320,321)
assert verify(F,9,70)==4 and verify(A,9,18)==6
pins={1:0,3:0,5:1,6:0,7:0,8:0}
models=[a for a in product((0,1),repeat=9) if truth(F,a)]
assert sum(all(a[v-1]==b for v,b in pins.items()) for a in models)==2
assert sum(all(a[v-1]==b for v,b in {**pins,1:1}.items()) for a in models)==0
faces=[c for c in A if 1 in c or -1 in c]
other=list(range(2,10))
def local(b):
 val=dict(zip(other,b));is_true=lambda l:val[abs(l)]==int(l>0)
 return all(any(is_true(l) for l in c if abs(l)!=1) for c in faces if 1 in c) or all(any(is_true(l) for l in c if abs(l)!=1) for c in faces if -1 in c)
table={b:local(b) for b in product((0,1),repeat=8)}
for i in range(8):assert any(table[b]!=table[b[:i]+(1-b[i],)+b[i+1:]] for b in table)
print('PASS independent: F9 70, A9 18, F9 SAT/UNSAT 2/0, three projections, 256 A9 factor inputs, 2048/2415, local gate min 7')
