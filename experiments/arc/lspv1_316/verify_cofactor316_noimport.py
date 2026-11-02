#!/usr/bin/env python3
"""Independent original-source truth-mask verifier for LSPV-1 cofactor316.
Does not import the 2SAT producer or use its implication-SCC algorithm.
"""
from itertools import product
from collections import Counter

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def sat(F,a):
    return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in F)

def other_clauses(F,p,x):
    ans=[]
    for c in F:
        if x in tuple(map(abs,c)):continue
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):continue
        ans.append(tuple(l for l in c if abs(l) not in p))
    return ans

def up_unsat(cnf):
    a={}
    while True:
        changed=False
        for c in cnf:
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            rem=[l for l in c if abs(l) not in a]
            if not rem:return True
            if len(rem)==1:
                l=rem[0];k=abs(l);v=int(l>0)
                if k in a and a[k]!=v:return True
                if k not in a:a[k]=v;changed=True
        if not changed:return False

def old_cert(F,p,x):
    H=other_clauses(F,p,x)
    for c in F:
        if x not in tuple(map(abs,c)):continue
        rem=tuple(l for l in c if abs(l)!=x)
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in rem):continue
        v=tuple(l for l in rem if abs(l) not in p)
        if not up_unsat(H+[(-l,) for l in v]):return False
    return True

def count(F):
    n=max(abs(l) for c in F for l in c)
    truths={k for k in range(1<<n) if sat(F,[(k>>j)&1 for j in range(n)])}
    totals=Counter()
    for x in range(1,n+1):
        other=[i for i in range(1,n+1) if i!=x]
        mismatch={k for k in range(1<<n) if not(k&(1<<(x-1))) and
                  ((k in truths)!=((k|(1<<(x-1))) in truths))}
        for state in product((None,0,1),repeat=n-1):
            pins={i:v for i,v in zip(other,state) if v is not None}
            if any(len(c)>2 for c in other_clauses(F,pins,x)):
                totals["unresolved"]+=1;continue
            totals["eligible"]+=1
            def agrees(k):
                return all(((k>>(i-1))&1)==v for i,v in pins.items())
            unequal=any(agrees(k) for k in mismatch)
            totals["DEPENDENT" if unequal else "INDEPENDENT"]+=1
            if not unequal:
                if old_cert(F,pins,x):totals["up_certified"]+=1
                else:
                    totals["new_not_up"]+=1
                    if any(agrees(k) for k in truths):totals["new_nonvacuous"]+=1
    totals["models_root"]=len(truths)
    return dict(totals)

if __name__=="__main__":
    expected={
      "F9":{"eligible":46912,"INDEPENDENT":23086,"DEPENDENT":23826,
            "unresolved":12137,"up_certified":19993,"new_not_up":3093,
            "new_nonvacuous":23,"models_root":70},
      "Y6":{"eligible":1300,"INDEPENDENT":344,"DEPENDENT":956,
            "unresolved":158,"up_certified":324,"new_not_up":20,
            "new_nonvacuous":0,"models_root":20}}
    for name,F in (("F9",F9),("Y6",Y6)):
        got=count(F)
        assert got==expected[name],(name,got,expected[name])
        print(name,got)
    # Nonvacuous same-original strictness control
    p={4:1,5:0,6:1,7:0,8:0}
    for x in (0,1):
        model=[]
        for a,b,c in product((0,1),repeat=3):
            z={**p,1:x,2:a,3:b,9:c}
            if sat(F9,[z[i] for i in range(1,10)]):model.append((a,b,c))
        assert model==[(0,1,1)]
    assert not old_cert(F9,p,1)
    # Complete original signed S/U pair compatibility
    ss=Counter()
    for i in range(12):
        for j in range(i+1,12):
            for mode in ("SS","SU","US","UU"):
                d={};ok=True
                for clause,t in ((F9[i],mode[0]),(F9[j],mode[1])):
                    for l in clause:
                        val=int((l>0)==(t=="S"));v=abs(l)
                        if v in d and d[v]!=val:ok=False
                        d[v]=val
                ss[mode]+=int(ok)
    assert dict(ss)=={"SS":37,"SU":49,"US":49,"UU":37}
    for a in product((0,1),repeat=9):
        for c in F9:
            t=sum(a[abs(l)-1]==int(l>0) for l in c)
            t2=sum((1-a[abs(l)-1])==int(l>0) for l in c)
            assert t+t2==3
    print("PASS, independent original-source truth-table / UP tests")
