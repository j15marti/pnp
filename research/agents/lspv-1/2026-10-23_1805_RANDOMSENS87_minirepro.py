#!/usr/bin/env python3
"""RANDOMSENS87 compact exact verifier. Python 3 standard library only.
Full 30609-check audit: see report/local accompanying package.
No imported 198/264 UNSAT certificate is independently re-proved here.
"""
from itertools import product
import json
NCOINS=120
CHECKS=0
def ck(ok):
    global CHECKS
    CHECKS+=1
    assert ok

def policy(bits,coin,epsilon_numerator):
    if coin<epsilon_numerator: return False,0
    if coin<2*epsilon_numerator: return True,0
    for j,b in enumerate(bits):
        if not b: return False,j+1
    return True,len(bits)

def cnf_eval(F,assignment):
    return all(any((assignment[abs(l)-1] if l>0 else not assignment[abs(l)-1]) for l in C) for C in F)

def chain(bits):
    q=len(bits);z0=1;u=q+2;v=q+3
    F=[(z0,u),(z0,-u),(-(q+1),v),(-(q+1),-v)]
    F += [(-i,i+1 if b else -(i+1)) for i,b in enumerate(bits,1)]
    return F,q+3

report=[]
for p in (1,2,4,8,16,32,64):
    x=[1]*p
    for e in (0,12,30,40):
        all_queries=0;all_errors=0;one_errors=0
        for coin in range(NCOINS):
            label,q=policy(x,coin,e)
            all_queries+=q;all_errors+=not label
            ck(q==p if coin>=2*e else q==0)
            for i in range(p):
                y=x.copy();y[i]=0
                label2,q2=policy(y,coin,e)
                one_errors+=label2
                ck((not label2) if coin<e or coin>=2*e else label2)
                ck(q2==(i+1) if coin>=2*e else q2==0)
        ck(all_queries==(NCOINS-2*e)*p)
        ck(all_errors==e)
        ck(one_errors==e*p)
        report.append(dict(p=p,eps=f"{e}/{NCOINS}",expected_query=all_queries/NCOINS,
                           per_input_error=e/NCOINS))
chain_cases=0
for q in range(1,8):
    for b in product((0,1),repeat=q):
        F,n=chain(b)
        if q<=5:
            brute=any(cnf_eval(F,a) for a in product((False,True),repeat=n))
            ck(brute== (not all(b)))
        # Source-local implication-chain theorem independently checked above
        # only for q<=5; q=6,7 counts as construction and grammar checks.
        ck(len(F)==q+4 and n==q+3)
        chain_cases+=1
quartet=[
    tuple(i+1 if ((mask>>i)&1)==0 else -(i+1) for i in range(3))
    for mask in range(8) if mask.bit_count()%2
]
ck(len(quartet)==4)
for i in (1,2,3):
    ck(sum(i in C for C in quartet)==2)
    ck(sum(-i in C for C in quartet)==2)
ck(sum(cnf_eval(quartet,a) for a in product((False,True),repeat=3))==4)
result=dict(run='RANDOMSENS87',checks=CHECKS,failed=0,
            chain_2sat_patterns=chain_cases,eps_exact_sample_distributions=report,
            status='restricted source-query theorem only; P versus NP OPEN')
print(json.dumps(result,sort_keys=True,indent=2))
