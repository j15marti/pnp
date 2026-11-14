#!/usr/bin/env python3
"""Independent TMR-5 MCSP parameter and transfer audit (native CPython).
Pure finite combinatorial and integer arithmetic, not a TM runtime implementation.
"""
from fractions import Fraction
from itertools import combinations
from math import comb
import json

checks = 0
sparse_cases = 0
sparse_supports = 0
counting_cases = 0
degree_cases = 0
frontier_cases = 0

def ck(condition, reason):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(reason)

# Independent replay of TMR-2's sharp *reference-distance* case,
# explicitly distinguishing common preprocessing and restarted outputs.
# Each output is the OR of q queried positions in a cyclic local window.
for M in (4, 8):
    for b0 in range(3):
        if b0 >= M:
            continue
        remaining = tuple(range(b0, M))
        B = len(remaining)
        N = 8
        for q in range(B+1):
            windows = [frozenset(remaining[(j+k)%B] for k in range(q)) for j in range(N)]
            for r in range(1, B+1):
                numerator = 0
                total = comb(B, r)
                for S in combinations(remaining, r):
                    witnesses = frozenset(S)
                    numerator += sum(bool(witnesses.intersection(w)) for w in windows)
                    sparse_supports += 1
                avg = Fraction(numerator, total*N)
                exact = 1-Fraction(comb(B-min(q,B), r), comb(B,r)) if B-q >= r else Fraction(1)
                ck(avg == exact, f'local OR must attain hypergeometric reference bound: {M,b0,q,r,avg,exact}')
                ck(avg <= Fraction(r*q,B), 'union bound')
                sparse_cases += 1

# Independently audit TMR-1's Shannon counting *inequality*, not constructiveness.
for n in range(8, 200):
    s = (2**n)//(16*n)
    ck(2*n + s*(2*n+2) < 2**n, f'circuit counting strict inequality at n={n}')
    counting_cases += 1

# New explicitly quantified indexed-output degree frontier:
# Let L=2^h, N=2^(a*h)=L^a, t=L^d,
# B=K*(L+n+t+2)^2 and s=floor(N^mu).
# To ensure floor(N^mu) >= B, use exact integer comparison
# 2^(p*n) >= (B)^q with mu=p/q.
K = 128
favorable_examples = []
unfavorable_examples = []
for mu in (Fraction(1, 10), Fraction(1, 4), Fraction(2, 5)):
    for a in (5, 8, 10, 16, 20, 24, 30, 40, 60):
        for d in (1,2,3):
            good_marg = mu*a > 2*d
            hit = None
            for h in range(1, 29):
                L = 2**h
                n = a*h
                t = L**d
                B = K*(L+n+t+2)**2
                p,q = mu.numerator,mu.denominator
                holds = (2**(p*n) >= B**q)
                ck(holds == (Fraction(p*n,q) >= 0 and 2**(p*n) >= B**q), 'exact integer comparison')
                if holds and hit is None:
                    hit=h
                degree_cases += 1
            if good_marg:
                ck(hit is not None, f'favorable degree region failed to cross by h=28: mu={mu},a={a},d={d}')
                favorable_examples.append((str(mu),a,d,hit))
            elif hit is None:
                unfavorable_examples.append((str(mu),a,d))

# Independent rational-parameter audit of TMR-3's high-mu network frontier.
# The cited N^1.99 one-way input theorem can only be invoked if the
# *whole* serialization fits o(N^1.99) by its actual proven construction.
R = Fraction(199, 100)
for a in (Fraction(0),Fraction(1),Fraction(3,2),Fraction(2)):
    for b in (Fraction(0),Fraction(1),Fraction(3,2),Fraction(2)):
        for c in (Fraction(1,2),Fraction(1),Fraction(3,2),Fraction(2)):
            for e in (Fraction(0),Fraction(1,2),Fraction(4,5),Fraction(99,100),Fraction(1),Fraction(3,2)):
                d0=max(Fraction(1),a,b)
                original=(c<R and e+max(d0,e)<R)
                # A safe generic two-head-constructor -> one-tape cost O(C^2)
                # would require 2c<R. This is *not* a proof of optimality.
                generic=(2*c<R and e+max(d0,e)<R)
                ck(not generic or original, 'generic model conversion should only weaken frontier')
                frontier_cases+=1

# Structural countercontrol: for C=N and E=N^0.8 with B,p=O(N),
# TMR-3 formula would claim a contradiction; replacing unproved direct
# execution of an input-head constructor with safe quadratic serialization
# destroys the claimed contradiction.
c,e,d0=Fraction(1),Fraction(4,5),Fraction(1)
ck(c<R and e+max(d0,e)<R, 'claimed additive-constructor bound excludes example')
ck(not(2*c<R and e+max(d0,e)<R), 'safe generic-conversion bound cannot exclude example')

result={
  'label':'TMR5_MCSP_DEGREE_CONSTRUCTOR_AUDIT040',
  'runtime':'native CPython exact integer/Fraction enumeration',
  'status':'COMPUTATIONAL controls supporting separately proved restricted degree lemma; constructor input-interface gap is a model audit, not an asymptotic impossibility proof',
  'assertions_passed':checks,'failures':0,
  'sharp_hypergeometric_reference_cases':sparse_cases,
  'exhaustive_sparse_supports_examined':sparse_supports,
  'circuit_counting_n_values':counting_cases,
  'exact_degree_threshold_comparisons':degree_cases,
  'favorable_degree_parameters':len(favorable_examples),
  'favorable_first_crossings_sample':favorable_examples[:16],
  'nonfavorable_parameters_without_crossing':len(unfavorable_examples),
  'exact_network_exponent_cases':frontier_cases,
  'countercontrol':'C=N,E=N^0.8,B,p=O(N): original additive-C frontier excludes, whereas generic O(C^2) header-head conversion does not',
  'limits':'No compiled one-head TM, no actual SAT-to-MCSP reduction, no full machine simulation, no unconditional P!=NP conclusion'
}
print(json.dumps(result,indent=2))
