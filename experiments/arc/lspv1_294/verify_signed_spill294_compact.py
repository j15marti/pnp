#!/usr/bin/env python3
"""No-import independent bitmask and source-clause certificate checker, ARC294."""
from collections import Counter
from itertools import product
import json
F=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
   (7,11,13),(8,12,14),(9,13,15),(10,14,15),
   (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
   (-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),
   (-10,-7,-15))
U=(-1,)*6+(0,0,0,0,1,1,1,1,0)
S=(-1,)*6+(1,0,0,0,1,1,1,1,0)
CYCLES_U=((1,2,12),(3,4,15))
CYCLES_S=((2,11,12),(3,4,15))

def holds(mask):
    return all(any(bool(mask & (1<<(abs(x)-1)))==(x>0) for x in c) for c in F)

def matches(mask,p):
    return all(v<0 or bool(mask & (1<<i))==bool(v) for i,v in enumerate(p))

def source_grammar():
    c=Counter(x for clause in F for x in clause)
    return len(F)==20 and len({tuple(sorted(row)) for row in F})==20 and all(
        len(row)==3 and len({abs(x) for x in row})==3 and (all(x>0 for x in row) or all(x<0 for x in row))
        for row in F) and all(c[i]==c[-i]==2 for i in range(1,16))

def residual(p):
    result=[];covered=[]
    for j,c in enumerate(F,1):
        if any(p[abs(x)-1]==int(x>0) for x in c):covered.append((j,c))
        else:result.append((j,tuple(x for x in c if p[abs(x)-1]<0)))
    return result,covered

def check(p,cycles):
    R,covered=residual(p)
    assert not any(len(c)<2 for j,c in R)
    f=p.count(-1);u=len(R);e=2*f-u
    spill=Counter(x for j,c in covered for x in c if p[abs(x)-1]<0)
    eta=sum(min(spill[i],spill[-i]) for i in range(1,16) if p[i-1]<0)
    r3=sum(len(c)==3 for j,c in R)
    h=sum(spill.values())
    Delta=sum(abs(spill[i]-spill[-i]) for i in range(1,16) if p[i-1]<0)
    assert 4*f==sum(len(c) for _,c in R)+h
    assert 2*e==r3+h and 2*(e-eta)==r3+Delta
    edges={j:set(map(abs,c)) for j,c in R if len(c)==2}
    used=set()
    for cycle in cycles:
        assert len(cycle)==3 and not set(cycle)&used
        used.update(cycle)
        assert all(j in edges for j in cycle)
        a,b,d=(edges[j] for j in cycle)
        assert len(a&b)==len(b&d)==len(a&d)==1
        assert len(a|b|d)==3
    return e,eta,r3,len(cycles)

def main():
    assert source_grammar()
    models=[x for x in range(1<<15) if holds(x)]
    assert len(models)==1032 and not holds(0) and not holds((1<<15)-1)
    assert sum(matches(x,U) for x in models)==0
    assert sum(matches(x,S) for x in models)==2
    assert check(U,CYCLES_U)==(2,1,1,2)
    assert check(S,CYCLES_S)==(3,1,1,2)
    counters=Counter()
    for anchor in (U,S):
        free=[i for i,v in enumerate(anchor) if v==-1]
        for values in product((-1,0,1),repeat=len(free)):
            q=list(anchor)
            for i,v in zip(free,values):q[i]=v
            ok=any(matches(x,q) for x in models)
            counters['states']+=1
            counters['SAT' if ok else 'UNSAT']+=1
    assert counters==Counter({'states':1458,'UNSAT':1362,'SAT':96})
    print(json.dumps({'status':'PASS','models':1032,'cube_counts':dict(counters),
        'U':{'e':2,'eta':1,'cycles':2,'UNSAT':True},
        'S':{'e':3,'eta':1,'cycles':2,'SAT_witnesses':2},
        'scope':'finite same-source bitmask check; P versus NP OPEN'},sort_keys=True))
if __name__=='__main__':main()
