#!/usr/bin/env python3
"""Independent compact exact-rational conditional ARC audit.
This is NOT an implementation of a universal SAT compiler or native FLMV ledger.
Full policy/DPLL/SU reproducer and raw JSON in local ARC_ALTERNATING_FLMV_GATE1 bundle.
"""
from fractions import Fraction as F
from itertools import product,combinations
from random import Random
def stage(alpha,gamma,lam,sigma):return (F(alpha),F(gamma),F(lam),F(sigma))
U=stage('28/25','31/50','1/2','1/2')
V=stage('23/20','27/50','1/2','3/4')
def comp(outer,inner):
 a,g,l,s=outer;b,h,m,t=inner
 return (max(a,g+l*b),g+l*h,l*m,max(s,l*t))
def fixed(p):
 a,g,l,s=p
 return (max(a,g/(1-l)),s)
def iterate(p,kl):
 a,g,l,s=p;k,z=kl
 return (max(a,g+l*k),max(s,l*z))
def flmv(c):
 f=F(1);best=F(-1);best_k=0
 for k in range(1,100):
  f=c*f/(1+f)
  d=min((1/f-c)/k,1/c**k)
  if d>best:best,best_k=d,k
  if best>0 and 1/c**(k+1)<best:return best,best_k
 raise AssertionError("no certified tail")
W=comp(U,V);R=comp(V,U)
assert W==(F(239,200),F(89,100),F(1,4),F(1,2))
assert R==(F(23,20),F(17,20),F(1,4),F(3,4))
assert fixed(U)==(F(31,25),F(1,2))
assert fixed(V)==(F(23,20),F(3,4))
assert fixed(W)==(F(239,200),F(1,2))
assert fixed(R)==(F(23,20),F(3,4))
assert flmv(F(6,5))==(F(23,45),2)
assert flmv(F(31,25))[0]==F(10417,24025)
assert flmv(F(23,20))[0]==F(13033,21160)
for k,z in [(2,1),(4,3),(10,8),(100,50)]:
 cur=F(k),F(z)
 for j in range(20):
  if cur[0]<F(6,5) and cur[1]<F(23,45):break
  cur=iterate(W,cur)
 assert j<20
 print('exponents',k,z,'composites',j,'end',*[str(x) for x in cur])
# Direct truth table and every indexed S/U pair, no independent occurrence variables
def sat(c,a):return all(any(a[abs(l)-1]==(l>0) for l in z) for z in c)
def truth(c):
 n=max(abs(l) for z in c for l in z)
 return any(sat(c,a) for a in product([False,True],repeat=n))
def audit(c):
 n=max(abs(l) for z in c for l in z)
 S=[{abs(l):l>0 for l in z} for z in c]
 U=[{v:not bit for v,bit in row.items()} for row in S]
 for j,h in combinations(range(len(c)),2):
  a,b=S[j],S[h]
  opp=any(a[v]!=b[v] for v in a.keys()&b.keys())
  same=any(a[v]==b[v] for v in a.keys()&b.keys())
  assert all(a[v]==b[v] for v in a.keys()&b.keys())== (not opp)
  assert all(a[v]!=b[v] for v in a.keys()&b.keys())== (not same)
  assert all(U[j][v]==U[h][v] for v in a.keys()&b.keys())== (not opp)
  assert all(a[v]==U[h][v] for v in a.keys()&b.keys())== (not same)
 for bits in [tuple([False]*n),tuple([True]*n)]:
  inv=tuple(not b for b in bits)
  for z in c:
   def cnt(v):return sum(v[abs(l)-1]==(l>0) for l in z)
   assert cnt(bits)+cnt(inv)==len(z)
 return truth(c)
sources={
 'two_sat_yes':((1,2),(-1,2)),
 'two_sat_no':((1,),(-1,)),
 'horn_yes':((-1,2),(1,),(-2,3)),
 'horn_no':((1,),(2,),(3,),(-1,-2,-3)),
 'xor_yes':tuple(tuple((i+1) if b==0 else -(i+1) for i,b in enumerate(a))
                  for a in product([0,1],repeat=3) if sum(a)%2==1),
 'xor_no':tuple(tuple((i+1) if b==0 else -(i+1) for i,b in enumerate(a))
                 for a in product([0,1],repeat=3)),
}
for key,c in sources.items():
 result=audit(c)
 assert result==key.endswith('yes')
 print('source',key,'SAT',result)
rng=Random(202610301100)
yes=no=0
for _ in range(350):
 n=rng.randint(3,6);m=rng.randint(1,15);clauses=[]
 for __ in range(m):
  k=rng.randint(1,3);ids=rng.sample(range(1,n+1),k)
  clauses.append(tuple(v if rng.randrange(2) else -v for v in ids))
 if audit(clauses):yes+=1
 else:no+=1
print('random total',yes+no,'SAT',yes,'UNSAT',no)
print('conditional arithmetic and finite semantic controls PASS; P versus NP OPEN')
