#!/usr/bin/env python3
"""Compact independent signed-extreme verification; full DPLL/raw in ZIP."""
from itertools import combinations, product
from random import Random
import json
SEED=20261029

def value(C,a):
    return sum(int(a[abs(l)]==int(l>0)) for l in C)

def target(C,e):
    return {abs(l):e^int(l<0) for l in C}

def pair(C,D,e,f):
    a=target(C,e)
    for i,v in target(D,f).items():
        if i in a and a[i]!=v:return False
        a[i]=v
    return True

def balanced(F):
    adj=[[] for _ in F]
    for j,k in combinations(range(len(F)),2):
        for a in F[j]:
            for b in F[k]:
                if abs(a)==abs(b):
                    d=int(a<0)^int(b<0)
                    adj[j].append((k,d));adj[k].append((j,d))
    labels={}
    for j in range(len(F)):
        if j in labels:continue
        labels[j]=0;q=[j]
        for u in q:
            for v,d in adj[u]:
                if v not in labels:labels[v]=labels[u]^d;q.append(v)
                elif labels[v]!=(labels[u]^d):return False
    return True

def brute(F,n):
    return [{i:(w>>(i-1))&1 for i in range(1,n+1)} for w in range(1<<n)]

def extrema(F,n):
    m=len(F);words=brute(F,n)
    minmid=min(sum(value(C,a) in (1,2) for C in F) for a in words)
    maxsat=max(sum(value(C,a)==3 for C in F) for a in words)
    maxtot=max((len(J) for z in range(m+1) for J in combinations(range(m),z)
        if all(not any(l in F[j] and -l in F[k] for l in F[j])
          for j,k in combinations(J,2))),default=0)
    minrm=min((len(J) for z in range(m+1) for J in combinations(range(m),z)
        if balanced([C for j,C in enumerate(F) if j not in J])),default=m)
    assert (maxsat,minmid)==(maxtot,minrm)
    return maxsat,minmid

def run():
    rng=Random(SEED);n=5
    clauses=[tuple(s*v for s,v in zip(signs,vs))
      for vs in combinations(range(1,n+1),3)
      for signs in product((-1,1),repeat=3)]
    pair_checks=0
    for C,D in combinations(clauses,2):
        for e,f in product((0,1),repeat=2):
            observed=any(value(C,a)==3*e and value(D,a)==3*f
                         for a in brute((C,D),n))
            assert observed==pair(C,D,e,f)
            pair_checks+=1
    graph_checks=0;exact_checks=0
    for _ in range(700):
        F=rng.sample(clauses,rng.randint(1,5))
        oracle=any(all(value(C,a) in (0,3) for C in F) for a in brute(F,n))
        assert balanced(F)==oracle
        graph_checks+=1
    for _ in range(240):
        F=rng.sample(clauses,rng.randint(1,8))
        extrema(F,n);exact_checks+=1
    triangle=[(1,-3,4),(-1,2,5),(-2,3,6)]
    assert not balanced(triangle)
    assert all(pair(triangle[j],triangle[k],0,1)
       for j,k in combinations(range(3),2))
    assert all(all(value(C,{i:v for i in range(1,7)})>0 for C in triangle)
       for v in (0,1))
    mixed=[(1,2,3),(1,2,-3),(-1,-2,-3)]
    assert all(not pair(mixed[0],mixed[1],e,f)
       for e,f in product((0,1),repeat=2))
    assert all(value(C,{1:1,2:0,3:0})>0 for C in mixed)
    print(json.dumps({'seed':SEED,'pair_checks':pair_checks,
         'balanced_graph_checks':graph_checks,'exact_extrema_checks':exact_checks,
         'mixed_pair_all_four_extremes_infeasible_but_SAT':True,
         'odd_triangle_pairwise_SU_feasible_global_extremes_impossible_but_SAT':True,
         'proof_status':'COMPUTATIONAL controls of elementary symbolic theorems'},indent=2))
if __name__=='__main__':run()
