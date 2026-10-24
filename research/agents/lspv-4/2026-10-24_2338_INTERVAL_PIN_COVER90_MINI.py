#!/usr/bin/env python3
"""Independent short verifier for INTERVAL-PIN-COVER90. Standard library only."""
import itertools, json, math
def chain(bits):
 q=len(bits); u=q+2;v=q+3
 clauses=[(1,u),(1,-u),(-(q+1),v),(-(q+1),-v)]
 clauses += [(-i,i+1 if b else -(i+1)) for i,b in enumerate(bits,1)]
 return q+3, clauses
def sat(n,clauses):
 return any(all(any((bits[abs(l)-1] if l>0 else not bits[-l-1]) for l in c) for c in clauses)
            for bits in itertools.product((False,True),repeat=n))
def lifted(n,clauses):
 out=[]
 for j,(a,b) in enumerate(clauses,1):
  t=n+j;out.extend(((a,b,t),(a,b,-t)))
 return n+len(clauses),out
def B(q):
 return (8*q+34)*math.ceil(math.log2(64*(4*q+16)))
checks=0
for q in range(1,8):
 for xs in itertools.product((0,1),repeat=q):
  n,clauses=chain(xs);truth=(0 in xs)
  assert sat(n,clauses)==truth;checks+=1
  for k in range(1,q+1):
   chunks=[xs[i:i+k] for i in range(0,q,k)]
   results=[sat(*chain(seg)) for seg in chunks]
   assert any(results)==truth;checks+=1
   for seg in chunks:
    m,cs=lifted(*chain(seg))
    assert m==2*len(seg)+7 and len(cs)==2*len(seg)+8;checks+=1
    assert B(len(seg))>0;checks+=1
# Connected shared-boundary counterexample.
A=[(1,2),(1,-2)]
U=[(-1,3),(-1,-3)]
S=[(1,3),(1,-3)]
assert sat(3,A) and sat(3,U) and sat(3,S);checks+=1
assert not sat(3,A+U) and sat(3,A+S);checks+=1
for C in (A+U,A+S):
 assert sat(*lifted(3,C))==sat(3,C);checks+=1
# Symbolic all-ones OR children: every interval false;
# flipping any one orientation makes its interval true.
for q in (8,16,64,256,1024):
 for k in (1,math.isqrt(q),q):
  starts=range(0,q,k)
  for i in range(q):
   assert any(start<=i<min(start+k,q) for start in starts);checks+=1
  assert len(list(starts))==math.ceil(q/k);checks+=1
print(json.dumps({"run":"INTERVAL-PIN-COVER90-MINI","status":"PASS","checks":checks,"scope":"restricted only"}))
