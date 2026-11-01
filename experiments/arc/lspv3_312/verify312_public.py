#!/usr/bin/env python3
"""Independent no-import original-source verifier for GATE312.
Does not import the producer; checks same valid F9 original with direct tuples.
"""
from itertools import product,combinations
P=[{1,5,6},{2,3,8},{1,3,5},{4,6,9},{2,4,7},{7,8,9}]
M=[{4,6,8},{1,6,7},{2,3,4},{3,5,8},{1,2,9},{5,7,9}]
SRC=[(set(x),sign) for sign,rows in ((1,P),(0,M)) for x in rows]
def satisfies(a):return all(any(a[x-1]==sign for x in vs) for vs,sign in SRC)
def extends(a,p):return all(a[i-1]==v for i,v in p.items())
def fibers(models,p):return [sum(extends(a,p) and a[6]==v for a in models) for v in (0,1)]
def no_empty(p):
    return all(any(x not in p or p[x]==sign for x in vs) for vs,sign in SRC)
def verify():
    checks=0
    def ck(x):
        nonlocal checks
        checks+=1
        assert x,checks
    models=[a for a in product((0,1),repeat=9) if satisfies(a)]
    ck(len(models)==70)
    p={1:1,2:0,3:0};q={1:1,2:1,3:0};r={6:1}
    states=[p,q,p|r,q|r]
    for s,expected in zip(states,((4,4),(4,4),(0,0),(2,0))):
        ck(tuple(fibers(models,s))==expected)
        ck(no_empty(s))
    # Independently replay source-clause unit deductions.
    z=dict(p|r)
    for j,x,bit in [(2,8,1),(8,7,0),(5,4,1)]:
        v,s=SRC[j-1]
        ck(x in v and x not in z and bit==s)
        ck(all(k in z and z[k]!=s for k in v-{x}))
        z[x]=bit
    v,s=SRC[6]
    ck(all(k in z and z[k]!=s for k in v))
    for a in product((0,1),repeat=9):
        if extends(a,p|r):ck(not satisfies(a))
        b=tuple(1-x for x in a)
        for v,s in SRC:
            ck(sum(a[k-1]==s for k in v)+sum(b[k-1]==s for k in v)==3)
    # 264 source clause-pair extreme compatibility identities.
    for (i,(a,asgn)),(j,(b,bsgn)) in combinations(enumerate(SRC),2):
        for u,v in product((0,1),repeat=2):
            compatible=all(x not in b or (asgn if u else 1-asgn)==(bsgn if v else 1-bsgn)
                           for x in a&b)
            brute=any(all(t[k-1]==(asgn if u else 1-asgn) for k in a)
                       and all(t[k-1]==(bsgn if v else 1-bsgn) for k in b)
                       for t in product((0,1),repeat=9))
            ck(compatible==brute)
    ck(sum(1 for x in product((0,1),repeat=9) if extends(x,p|r))==32)
    counts=[0,0]
    for digits in product((-1,0,1),repeat=9):
        pin={i+1:v for i,v in enumerate(digits) if v>=0}
        counts[0 if any(extends(a,pin) for a in models) else 1]+=1
    ck(counts==[10508,9175])
    # Y6 standalone same-sign canonical source (20 models).
    YP=["123","145","246","356"]; YM=["124","136","235","456"]
    Y=[tuple(int(x) for x in v) for v in YP]+[tuple(-int(x) for x in v) for v in YM]
    ck(sum(all(any(a[abs(x)-1]==int(x>0) for x in cl) for cl in Y)
           for a in product((0,1),repeat=6))==20)
    print({"status":"PASS","checks":checks,"F9":70,"four_counts":[8,8,0,2],
           "source_UP":[2,8,5,7],"cubes_SAT_UNSAT":counts,"Y6":20,
           "P_vs_NP":"OPEN"})
if __name__=="__main__":verify()
