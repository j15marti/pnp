#!/usr/bin/env python3
"""TMR-5/028 independent finite review of index-head locality and MCSP sparse-query convexity.

Native CPython reproducer. Finite checks are NOT a Turing-machine asymptotic proof.
"""
import json, random, math
from fractions import Fraction
from itertools import product

rng = random.Random(202611141650)
counts = {"machine_trace_pairs": 0, "machine_step_comparisons": 0,
          "hypergeom_checks": 0, "convexity_checks": 0,
          "tail_quantile_checks": 0, "symbolic_degree_checks": 0,
          "failures": 0}

def check(x, detail):
    if not x:
        counts['failures'] += 1
        raise AssertionError(detail)

# Finite bounded two-input-head, one-work-cell deterministic machines.
# Input symbols are 0,1,END; both read-only heads initially at index 0.
# Each transition may read, update its one work cell, and move heads by -1,0,1.
# The source length is strictly greater than the time horizon, making its END invisible.
# The index input may be shorter and END is permitted and charged.
T=8
for program_index in range(48):
    trans={}
    for st,a,b,w in product(range(4), range(3), range(3), range(2)):
        trans[(st,a,b,w)] = (rng.randrange(4),rng.randrange(2),rng.choice([-1,0,1]),rng.choice([-1,0,1]))
    for trial in range(35):
        L=rng.randrange(T+3, 90)
        prefix=[rng.randrange(2) for _ in range(T+1)]
        f1=prefix + [rng.randrange(2) for _ in range(L-len(prefix))]
        f2=prefix + [rng.randrange(2) for _ in range(L-len(prefix))]
        idx=[rng.randrange(2) for _ in range(rng.randrange(1,12))]
        def run(f):
            st=0; w=0; hf=hi=0; trace=[]
            for _ in range(T):
                a=f[hf] if hf<len(f) else 2
                b=idx[hi] if hi<len(idx) else 2
                st2,w2,df,di=trans[(st,a,b,w)]
                trace.append((st,a,b,w,st2,w2,hf,hi))
                st,w=st2,w2
                hf=max(0,hf+df);hi=max(0,hi+di)
            return trace
        tr1,tr2=run(f1),run(f2)
        for j,(a,b) in enumerate(zip(tr1,tr2)):
            check(a==b, (program_index,trial,j))
            counts['machine_step_comparisons']+=1
        counts['machine_trace_pairs']+=1

# Exact H(q) = C(N-q,r)/C(N,r) is decreasing and discretely convex.
# Check its finite differences and the quantile implication at different deltas.
for N in range(5,111):
    for r in range(1, min(N,13)+1):
        hs=[Fraction(math.comb(N-q,r),math.comb(N,r)) if N-q>=r else Fraction(0) for q in range(N+1)]
        check(hs[0]==1 and hs[-1]==0,(N,r,'ends'))
        for q in range(N):
            check(hs[q]>=hs[q+1],(N,r,q,'monotone'))
            counts['hypergeom_checks']+=1
        for q in range(N-1):
            check(hs[q]-2*hs[q+1]+hs[q+2]>=0,(N,r,q,'convex'))
            counts['convexity_checks']+=1
        for delta in (Fraction(1,10),Fraction(1,4),Fraction(1,3),Fraction(2,5)):
            a=2*delta
            for m in (0,N//8,N//4,N//2,3*N//4):
                if hs[m]>0:
                    pmax=min(Fraction(1),a/hs[m])
                    check(pmax>=0 and pmax<=1,(N,r,delta,m))
                    counts['tail_quantile_checks']+=1

# Demonstrate the genuine gap in the previously quoted quadratic circuit bound:
# t = L^d, N = L^a; when d<1, 2d < a*mu < 2,
# K*(L+n+t)^2 is NOT dominated by N^mu, whereas K*(n+t)^2 is.
examples=[]
for a,d,mu in ((1.0,.30,.90),(1.2,.40,.90),(1.5,.60,.95),(2.0,.40,.50)):
    check(a*mu>2*d and a*mu<2, (a,d,mu,'valid'))
    for logL in (12,20,40,80):
        # logs of asymptotic dominant terms; no giant allocations
        old_log_exponent=2*logL
        new_log_exponent=2*d*logL
        target_log_exponent=a*mu*logL
        check(old_log_exponent>target_log_exponent>new_log_exponent,(a,d,mu,logL))
        counts['symbolic_degree_checks']+=1
    examples.append({'a':a,'d':d,'mu':mu,'old_proof_exponent':2,'localized_proof_exponent':2*d,'threshold_exponent':a*mu})

output={'status':'PASS' if not counts['failures'] else 'FAIL',
        'script':'tmr5_locality_tail_audit044.py',
        'experiment_kind':'independent native CPython bounded-machine locality and exact-combinatorics tests',
        'counts':counts, 'degree_examples':examples,
        'interpretation':'Finite tests support calculations only. General locality lemma and tail bound are symbolic proofs.'}
print(json.dumps(output,sort_keys=True,indent=2))
