#!/usr/bin/env python3
"""No producer imports; distinct bitmask F9 checks and sharp minimax verification."""
from itertools import product,combinations
from fractions import Fraction
import json,sys
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
C=P+tuple(tuple(-x for x in c) for c in N)
count=0
def ck(x):
    global count
    count+=1
    assert x
def tc(c,w):
    return sum(bool(w&(1<<(abs(v)-1)))==(v>0) for v in c)
def good(w):
    return all(tc(c,w) for c in C)
S=[w for w in range(512) if good(w)]
ck(len(S)==70)
for i in range(1,10):
    ck(sum(i in c for c in C)==2)
    ck(sum(-i in c for c in C)==2)
for v,num in ((0,34),(1,36)):
    ck(sum(((w>>4)&1)==v for w in S)==num)
sat_pin={1:0,3:0,5:1,6:0,7:0,8:0}
unsat_pin={**sat_pin,1:1}
for pin,expected in ((sat_pin,2),(unsat_pin,0)):
    cubes=[w for w in range(512)
           if all(((w>>(k-1))&1)==v for k,v in pin.items())]
    ck(len(cubes)==8)
    ck(sum(w in S for w in cubes)==expected)
    if not expected:
        for w in cubes:ck(any(tc(c,w)==0 for c in C))
for i,j in combinations(range(12),2):
    a={abs(v):v>0 for v in C[i]};b={abs(v):v>0 for v in C[j]}
    for mode in product((0,3),repeat=2):
        possible=any(tc(C[i],w)==mode[0] and tc(C[j],w)==mode[1]
                     for w in range(512))
        contradiction=any(a[k]!=(b[k] if mode[0]==mode[1] else not b[k])
                          for k in a.keys()&b.keys())
        ck(possible==not contradiction)
for w in range(512):
    for c in C:ck(tc(c,w)+tc(c,w^511)==3)
for t in (1,2,3,4,5,8,16):
    z=Fraction(1,2**t)
    for eps in (Fraction(0),Fraction(1,10),Fraction(1,3)):
        p=(1-eps-z)/(1-z)
        ck(p+(1-p)*z==1-eps)
        ck(Fraction(t)*p==t*(1-eps/(1-z)))
        for q in range(t+1):
            # q observed pin bits: success at most 2^(-(t-q)).
            maxsuccess=Fraction(1,2**(t-q))
            ck(Fraction(q)>=t*(maxsuccess-z)/(1-z))
# Source grammar mutation controls (each is malformed).
for clauses in (C+(C[0],),((1,1,2),)+C[1:],((-1,5,6),)+C[1:],
                ((1,5,10),)+C[1:]):
    valid=(len(clauses)==12 and len(set(clauses))==12 and
           all(len(c)==3 and len({abs(x) for x in c})==3 and
               len({x>0 for x in c})==1 and
               all(1<=abs(x)<=9 for x in c) for c in clauses) and
           all(sum(x in c for c in clauses)==2 and
               sum(-x in c for c in clauses)==2 for x in range(1,10)))
    ck(not valid)
print(json.dumps({"status":"PASS","no_producer_import":True,
 "assertions":count,"models":len(S),"x5_splits":[34,36],
 "same_source_SAT_UNSAT":[2,0],"SU_modes":264,
 "complement_checks":6144,"minimax_cases":21},indent=2))
