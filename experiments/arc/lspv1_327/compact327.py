#!/usr/bin/env python3
"""LSPV-1 327: exact iterative Davis-Putnam on genuine canonical originals.
This is a reproducible finite checker, not an FLMV machine benchmark.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import json

F9_POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
Y6_POS=((1,2,3),(1,4,5),(2,4,6),(3,5,6))

def source(p,n):
    return tuple(tuple(c) for c in p)+tuple(tuple(-v for v in c) for c in n)

def grammar(f):
    if not f:return False
    names={abs(x) for c in f for x in c}
    if names != set(range(1,len(names)+1)):return False
    if len({tuple(sorted(c)) for c in f})!=len(f):return False
    counts=Counter((abs(x),x>0) for c in f for x in c)
    return all(len(c)==3 and len({abs(x) for x in c})==3
        and len({x>0 for x in c})==1 for c in f) and all(
        counts[i,False]==counts[i,True]==2 for i in names)

def norm(rows):
    out=set()
    for c in rows:
        s=set(c)
        if any(-v in s for v in s):continue
        if not s:return ((),)
        out.add(tuple(sorted(s)))
    return tuple(sorted(out,key=lambda x:(len(x),x)))

def stats(f):
    adj={abs(x):set() for c in f for x in c}
    cnt=Counter((abs(x),x>0) for c in f for x in c)
    for c in f:
        ids={abs(x) for x in c}
        for x in ids:adj[x].update(ids-{x})
    return {"v":len(adj),"m":len(f),"d":max(map(len,adj.values()),default=0),
            "p":max(cnt.values(),default=0),"w":max(map(len,f),default=0)},adj

def independent(f):
    _,adj=stats(f)
    live=set(adj);picked=[]
    while live:
        x=min(live);picked.append(x);live.difference_update(adj[x]|{x})
    return picked

def eliminate(f,chosen):
    for x in chosen:
        plus=[set(c)-{x} for c in f if x in c]
        minus=[set(c)-{-x} for c in f if -x in c]
        remain=[c for c in f if x not in c and -x not in c]
        remain.extend(tuple(a|b) for a,b in product(plus,minus))
        f=norm(remain)
    return f

def satisfies(f,a):
    return all(any(((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in f)

def bound_rows(k=7):
    p,w,d=2,3,8
    fraction=Fraction(1)
    rows=[]
    for r in range(k):
        fraction*=Fraction(d,d+1)
        rows.append(dict(r=r,P=p,w=w,D=d,numerator=fraction.numerator,
                         denominator=fraction.denominator,exponent=float(fraction)))
        d=d+2*p*(p*(w-1)-1);p=p*p;w=2*(w-1)
    return rows

def run():
    cases={"F9":source(F9_POS,F9_NEG),"Y6":source(Y6_POS,Y6_POS)}
    results={}
    bounds=bound_rows()
    for label,f in cases.items():
        assert grammar(f)
        n=len({abs(x) for c in f for x in c})
        models=sum(satisfies(f,a) for a in range(1<<n))
        assert models=={"F9":70,"Y6":18}[label]
        current=norm(f);traces=[]
        for r in range(4):
            before,_=stats(current)
            assert before["p"]<=bounds[r]["P"] and before["w"]<=bounds[r]["w"]
            assert before["d"]<=bounds[r]["D"]
            pivots=independent(current)
            after=eliminate(current,pivots)
            st,_=stats(after)
            assert st["p"]<=bounds[r+1]["P"] and st["d"]<=bounds[r+1]["D"]
            assert st["w"]<=bounds[r+1]["w"]
            # Complete existential continuation truth, with original input names.
            eliminated=sorted(set(range(1,n+1))-{abs(x) for c in after for x in c})
            surviving=sorted(set(range(1,n+1))-set(eliminated))
            for a in range(1<<len(surviving)):
                base=sum(((a>>i)&1)<<(v-1) for i,v in enumerate(surviving))
                expected=False
                for bits in range(1<<len(eliminated)):
                    x=base|sum(((bits>>j)&1)<<(v-1) for j,v in enumerate(eliminated))
                    if satisfies(f,x):expected=True;break
                assert satisfies(after,base)==expected
            traces.append(dict(round=r,pivots=pivots,output=st))
            current=after
        results[label]=dict(n=n,m=len(f),models=models,steps=traces,
                            forward_source_private_gates=3*len(f)-1)
    print(json.dumps(dict(status="PASS",theorem="P versus NP OPEN",
        A3="640/763",A4="1687040/2012031",
        A4_float=float(Fraction(1687040,2012031)),
        bounds=bounds,cases=results),indent=2))
if __name__=="__main__":run()
