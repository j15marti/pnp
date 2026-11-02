#!/usr/bin/env python3
"""Exact F9 decision-only vs explicit-witness query control (Python stdlib)."""
from fractions import Fraction
from itertools import product,combinations
from collections import Counter
import json,sys
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
C=P+tuple(tuple(-x for x in c) for c in M)
def tcount(c,a):
    return sum(a[abs(v)-1]==(1 if v>0 else 0) for v in c)
def sat(a):
    return all(tcount(c,a)>0 for c in C)
def valid(cls,n):
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 or
           len({v>0 for v in c})!=1 or
           any(not(1<=abs(v)<=n) for v in c) for c in cls):return False
    if len({tuple(sorted(c)) for c in cls})!=len(cls):return False
    cnt=Counter((abs(v),v>0) for c in cls for v in c)
    return all(cnt[i,b]==2 for i in range(1,n+1) for b in (0,1))
A=[x for x in product((0,1),repeat=9) if sat(x)]
assert valid(C,9) and len(A)==70
buckets={v:[a for a in A if a[4]==v] for v in (0,1)}
assert [len(buckets[v]) for v in (0,1)]==[34,36]
W={v:buckets[v][0] for v in (0,1)}
for t in range(1,5):
    F=tuple(tuple((1 if v>0 else -1)*(abs(v)+9*k) for v in c)
            for k in range(t) for c in C)
    assert valid(F,9*t)
    for b in product((0,1),repeat=t):
        w=tuple(x for bit in b for x in W[bit])
        assert all(w[9*k+4]==bit for k,bit in enumerate(b))
        assert all(any(w[abs(v)-1]==(v>0) for v in c) for c in F)
S={1:0,3:0,5:1,6:0,7:0,8:0};U=dict(S);U[1]=1
def extensions(p):
    return sum(all(a[i-1]==v for i,v in p.items()) for a in A)
assert (extensions(S),extensions(U))==(2,0)
modes=0
for i,j in combinations(range(12),2):
    d1={abs(v):v>0 for v in C[i]};d2={abs(v):v>0 for v in C[j]}
    for z1,z2 in product((0,3),repeat=2):
        actual=any(tcount(C[i],a)==z1 and tcount(C[j],a)==z2
                   for a in product((0,1),repeat=9))
        impossible=any(d1[k]!=(d2[k] if z1==z2 else not d2[k])
                       for k in d1.keys()&d2.keys())
        assert actual==not impossible;modes+=1
for a in product((0,1),repeat=9):
    ca=tuple(1-x for x in a)
    assert all(tcount(c,a)+tcount(c,ca)==3 for c in C)
sharp=[]
for t in (1,2,3,4,5,8,16):
    for eps in (Fraction(0),Fraction(1,10),Fraction(1,3)):
        z=Fraction(1,2**t);p=(1-eps-z)/(1-z)
        assert p+(1-p)*z==1-eps
        assert all(1-Fraction(1,2**u)>=(1-z)*Fraction(u,t)
                   for u in range(t+1))
        sharp.append(dict(t=t,epsilon=str(eps),minimax_expected_queries=str(t*p),
                          exact_query_all_probability=str(p)))
assert modes==264
out=dict(claim="DECISION-WITNESS-MINIMAX313",scope="promised external F9 block pins",
         original_F9_models=70,model_counts_by_x5={"0":34,"1":36},
         explicit_witness_templates={str(v):list(W[v]) for v in (0,1)},
         same_original_SAT_cube=S,same_original_UNSAT_cube=U,
         SAT_completions=2,UNSAT_completions=0,
         original_S_U_pair_modes=modes,complement_identities=6144,
         global_zero_ones_truth_status=[6,0,0,6],
         randomized_minimax_cases=sharp,
         exact_decision_pin_queries=0,exact_explicit_witness_pin_queries="t",
         randomized_minimax="t*(1-epsilon/(1-2**(-t)))",
         limitations="restricted external-pin promise, not all-input or FLMV")
print(json.dumps(out,indent=2,sort_keys=True))
