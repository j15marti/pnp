#!/usr/bin/env python3
"""Independent control for ARC-HEAD-SHADOW-GATE256.
Standard-library only. Exhaustive move-path equivalence, source labels, FLMV.
"""
from fractions import Fraction
from itertools import product
from math import ceil, log2
import json
checks=0
def check(condition, message):
    global checks
    checks+=1
    if not condition: raise AssertionError(message)
def state(m, p, word, cap=None):
    if cap is not None: p=min(p,m+cap+1)
    for step in word:
        if step==0:
            if cap is None or p<m+cap+1: p=max(0,p-1)
        else:
            p+=1
            if cap is not None: p=min(p,m+cap+1)
    return '1' if p<m else '_'
for m in (1,2,3,8,16):
    for r in range(1,9):
        for p in range(m+2*r+4):
            for moves in range(r+1):
                for seq in product((0,1),repeat=moves):
                    check(state(m,p,seq)==state(m,p,seq,cap=r),
                          ("bounded exact",m,r,p,seq))
for r in (1,2,3,7,15,31,63,127):
    m=32
    for u in range(r+1):
        for v in range(u+1,r+1):
            path=(0,)*(u+1)
            check(state(m,m+u,path)=='1' and state(m,m+v,path)=='_',
                  ("distinguished",r,u,v))
    check(2**(ceil(log2(r+1))-1)<r+1<=2**ceil(log2(r+1)),
          ("state bits",r))
for m in (1,3,15):
    for cap in range(1,9):
        p=m+cap+3;seq=(0,)*(cap+4)
        check(state(m,p,seq)=='1' and state(m,p,seq,cap=cap)=='_',
              ("expired cap",m,cap))
def envelope(c):
    f=Fraction(1);power=Fraction(1);best=Fraction(0);kbest=0
    for k in range(1,100):
        f=c*f/(1+f);power/=c
        value=min((1/f-c)/k,power)
        if value>best:best=value;kbest=k
        if power/c<best:return best,kbest,k
    raise AssertionError("uncertified tail")
for c,d,k in ((Fraction(6,5),Fraction(23,45),2),
              (Fraction(241,200),Fraction(11642479,23232400),2),
              (Fraction(7,5),Fraction(949,5145),3)):
    ans,index,last=envelope(c)
    check((ans,index)==(d,k),("FLMV",c,ans,index,last))
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
F=[tuple(map(int,x.split())) for x in W1.split(';')]
G=[list(c) for c in F]
check(G[7][0]==1 and G[19][0]==-1,"original source")
G[7][0]=-1;G[19][0]=1
def count(A):
    models=0
    for a in range(1<<15):
        sat=True
        for c in A:
            if not any(((a>>(abs(l)-1))&1)==int(l>0) for l in c):
                sat=False;break
        models+=sat
    return models
check(count(F)==0,"W1 UNSAT")
check(count(G)==168,"W1 sign swap SAT")
print(json.dumps({"status":"PASS","independent_assertions":checks,
 "all_bounded_move_paths":True,"r_plus_one_states_pairwise_distinct":True,
 "strict_FLMV_exact":True,"matched_W1_model_counts":[0,168]},sort_keys=True))
