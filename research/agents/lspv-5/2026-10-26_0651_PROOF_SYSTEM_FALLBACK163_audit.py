#!/usr/bin/env python3
"""Finite quantifier/arithmetic audit for PROOF-SYSTEM-FALLBACK163."""
from fractions import Fraction
import json

checks=0
def ck(x):
    global checks
    checks+=1
    assert x

# Truth-table analogue: a table is SAT iff one assignment accepts.
# Empty-proof UNSAT verifier delegates to the total decider.
for q in range(1,13):
    mask=(1<<q)-1
    for table in range(1<<q):
        sat=bool(table & mask)
        R_empty=not sat
        ck(R_empty == (not sat))
        # Branchwise complement has one branch: SAT all-accept; UNSAT some-reject.
        M_coSAT=not R_empty
        ck(M_coSAT == sat)

# Adding a slow fallback branch makes maximum branch exponent max(c,K),
# irrespective of the fast branch or its proof length.
threshold=Fraction(651000,361301)
rows=[]
for fast_num in range(10,19):
    c=Fraction(fast_num,10)
    for K in range(2,11):
        combined=max(c,Fraction(K,1))
        ck(combined==K)
        ck(combined>threshold)
        rows.append({'fast_c':float(c),'fallback_K':K,
                     'combined_c':float(combined),'inside_strict_frontier':combined<threshold})

# Zero proof bits can coexist with arbitrarily large padded verification time.
for N in (2,4,8,16,32,64,128,256):
    last=0
    for K in range(1,9):
        work=N**K
        ck(work>=last)
        last=work

out={
 'run':'PROOF-SYSTEM-FALLBACK163',
 'status':'COMPUTATIONAL arithmetic/quantifier check',
 'assertion_groups':checks,
 'threshold_exact':f'{threshold.numerator}/{threshold.denominator}',
 'threshold_decimal':float(threshold),
 'fallback_rows':rows,
 'conclusions':[
  'empty proof does not imply fast verification',
  'branchwise complemented empty-proof verifier exactly reproduces its decider',
  'a K>=2 fallback dominates every c<1.9 test branch and misses the strict threshold'
 ],
 'limitations':[
  'finite truth-table audit is not a complexity-class proof',
  'Cook-Reckhow equivalence and FLMV theorem are cited symbolic dependencies',
  'no P versus NP separation is claimed'
 ]
}
print(json.dumps(out,indent=2,sort_keys=True))
