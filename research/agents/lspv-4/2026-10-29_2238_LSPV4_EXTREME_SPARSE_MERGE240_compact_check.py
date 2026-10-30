#!/usr/bin/env python3
"""LSPV4-240 compact strict22 clause-extreme theorem checker. Stdlib only.
See the full downloaded 14.5kB reproducer for source-indexed SAT/UNSAT DPLL work.
"""
import itertools, collections
T=((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3))
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
def parse(s):
 return [tuple(map(int,c.split())) for c in s.split(';')]
def t(c,a):
 return sum(int(a[abs(z)-1]==int(z>0)) for z in c)
def modes(c,d):
 a={abs(z):z>0 for z in c}; b={abs(z):z>0 for z in d}
 same=[v for v in a.keys()&b.keys() if a[v]==b[v]]
 opp=[v for v in a.keys()&b.keys() if a[v]!=b[v]]
 return {'SS':not opp,'SU':not same,'US':not same,'UU':not opp,'same':same,'opposite':opp}
def model_count(F):
 n=max(abs(z) for c in F for z in c)
 return sum(all(t(c,[(mask>>i)&1 for i in range(n)])>0 for c in F) for mask in range(1<<n))
def main():
 for r in (1,2,4,8):
  F=[tuple((abs(z)+3*i)*(1 if z>0 else -1) for z in c) for i in range(r) for c in T]
  n=3*r;cnt=collections.Counter(z for c in F for z in c)
  assert all(cnt[v]==cnt[-v]==2 for v in range(1,n+1))
  mixed=0;non_taut=0
  for c,d in itertools.combinations(F,2):
   q=modes(c,d)
   if q['same'] and q['opposite']:
    mixed+=1
    assert not any(q[s] for s in ('SS','SU','US','UU'))
   for v in q['opposite']:
    a=set(c)-{v if v in c else -v}
    b=set(d)-{v if v in d else -v}
    R=a|b
    if not any(-z in R for z in R):non_taut+=1
  assert mixed==2*n and non_taut==0
  if r<=4:assert model_count(F)==4**r
  print('tight product',r,'variables',n,'mixed_pairs',mixed,'non_taut',non_taut)
 for name,s,want in [('W1_UNSAT15',W1,0),('SAT15',S,861)]:
  F=parse(s)
  assert model_count(F)==want
  print(name,'model_count',want)
 c,d=(1,2,3),(1,-2,4)
 q=modes(c,d)
 assert not any(q[s] for s in ('SS','SU','US','UU'))
 assert all(not (t(c,[0,y,0,0])>0 and t(d,[0,y,0,0])>0) for y in (0,1))
 print('PASS: exact tight obstruction, polarity, SAT/UNSAT models and RUP forbidden cube')
if __name__=='__main__':main()
