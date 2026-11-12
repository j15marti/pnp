#!/usr/bin/env python3
"""LSPV-1/601 exhaustive two-variable strict signed RES reference control.
No historical /386 or full R_mix341 SOURCE acceptance claimed. No dependencies.
"""
import json
from itertools import product
from collections import deque,Counter

C=tuple(sorted(
 {(sign*i,) for i in (1,2) for sign in (-1,1)}
 | {tuple(sorted((a,b*2),key=lambda x:(abs(x),x)))
    for a in (-1,1) for b in (-1,1)},
 key=lambda t:(len(t),t)))

def next_clauses(K):
 out={}
 for A in K:
  for B in K:
   for p in A:
    if -p not in B:continue
    D=tuple(sorted((set(A)-{p})|(set(B)-{-p}),key=lambda x:(abs(x),x)))
    if D in K or any(-x in D for x in D):continue
    out.setdefault(D,(A,B,p))
 return out

def shortest(S):
 Q=deque([(frozenset(S),())]);seen={frozenset(S)}
 while Q:
  K,P=Q.popleft()
  for D,(A,B,p) in next_clauses(K).items():
   T=P+((A,B,p,D),)
   if not D:return len(T),T
   J=K|{D}
   if J not in seen:seen.add(J);Q.append((J,T))
 return None,None

def brute(K,d):
 if () in K:return True
 if not d:return False
 return any(brute(K|{D},d-1) for D in next_clauses(K))

def sat(S):
 return any(all(any(((v>0)==bool(b[abs(v)-1])) for v in D) for D in S)
            for b in product((0,1),repeat=2))

def main():
 hist=Counter();example={}
 for mask in range(1<<len(C)):
  S=frozenset(D for i,D in enumerate(C) if mask>>i&1)
  w,trace=shortest(S)
  assert (w is None)==sat(S),(mask,w)
  if w is None:continue
  hist[w]+=1
  for j in range(w):assert not brute(S,j),(mask,j)
  assert brute(S,w),(mask,w)
  example.setdefault(w,dict(source_mask=mask,source=[list(D) for D in sorted(S)],
     derivation=[dict(left=list(a),right=list(b),pivot=p,conclusion=list(c))
                 for a,b,p,c in trace]))
 assert hist==Counter({1:112,2:48,3:1}),hist
 print(json.dumps(dict(result='LSPV-1/601',scope='2-variable declared RES only, not historical R_mix341',
   exhaustive=True,seed=None,variables=2,
   clause_universe=[list(D) for D in C],total_source_subsets=256,
   sat=256-sum(hist.values()),unsat=sum(hist.values()),
   minimum_paid_RES_histogram={str(k):hist[k] for k in sorted(hist)},
   tests='independent 4-row truth table, un-memoized ordered proof DFS and shortest-set BFS',
   examples={str(k):example[k] for k in sorted(example)},
   native_checker_OS_executed=False,
   open_ids=['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3']),indent=2,sort_keys=True))
if __name__=='__main__':main()
