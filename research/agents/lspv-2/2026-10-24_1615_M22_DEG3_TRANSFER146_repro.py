#!/usr/bin/env python3
"""M22-DEG3-TRANSFER146: exact small finite validator. Not Jain et al's solver."""
import json
import math
from collections import Counter
from itertools import product

P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
F=tuple(P)+tuple(tuple(-v for v in c) for c in Q)

def sat(cnf,model):
    return all(any((l>0)==bool(model[abs(l)]) for l in c) for c in cnf)

def degree(cnf):
    return max(Counter(abs(v) for c in cnf for v in c).values(),default=0)

def restrict(cnf,assign):
    return tuple(tuple(l for l in c if abs(l) not in assign)
                 for c in cnf if not any(abs(l) in assign and
                 ((l>0)==bool(assign[abs(l)])) for l in c))

def split(cnf,k):
    x=[list(c) for c in cnf]
    for i in range(1,k+1):
        v=k+i
        hits=[c for c in x if i in c]
        assert len(hits)==2
        for c in hits: c[c.index(i)]=v
        x.append([-v,i])
    return tuple(tuple(c) for c in x)

def bits(cnf):
    names=sorted({abs(l) for c in cnf for l in c})
    n,m=len(names),len(cnf)
    w=max(1,math.ceil(math.log2(n+1)))
    h=max(1,math.ceil(math.log2(n+m+2)))
    return 1+2*h+sum(3+len(c)*(w+1) for c in cnf)

def main():
    assert len(F)==8 and len(set(F))==8 and degree(F)==4
    for v in range(1,7):
        assert sum(v in c for c in F)==2 and sum(-v in c for c in F)==2
    assert any(tuple(-v for v in c) not in F for c in F)
    original=0
    for a in product((0,1),repeat=6):
        if sat(F,(0,)+a):original+=1
    assert original==20
    G=split(F,6)
    assert len(G)==14 and degree(G)==3
    projected=0
    for a in product((0,1),repeat=12):
        if sat(G,(0,)+a):
            projected+=1
            assert sat(F,(0,)+a[:6])
    assert projected==44
    for a in product((0,1),repeat=6):
        if sat(F,(0,)+a):
            assert sat(G,(0,)+a+a)
    grandchildren=[]
    for a,b in product((0,1),repeat=2):
        C1=restrict(G,{1:a})
        C2=restrict(C1,{2:b})
        assert degree(C1)<=3 and degree(C2)<=3
        answer=any(sat(C2,{**{v:x for v,x in zip(range(3,13),rest)},
                            0:0}) for rest in product((0,1),repeat=10))
        expected=any(sat(F,(0,a,b)+rest) for rest in product((0,1),repeat=4))
        assert answer==expected
        grandchildren.append({"branch":f"{a}{b}","bits":bits(C2),
                               "maxdegree":degree(C2),"sat":answer})
    assert [r["bits"] for r in grandchildren]==[169,174,174,187]
    assert not any(sat(((1,),(-1,)),(0,i)) for i in (0,1))
    base=1.1199**2
    threshold=math.log(base,3)
    assert abs(threshold-0.2061498797611215)<1e-12
    result={"id":"M22-DEG3-TRANSFER146","Y":{"n":6,"m":8,"bits":bits(F),"models":original},
            "G":{"n":12,"m":14,"bits":bits(G),"maxdegree":3,"models":projected},
            "children":grandchildren,"base":base,"q_over_k_crossover":threshold,
            "random_seed":None,"scope":"bruteforce finite; not Jain solver; not FLMV machine"}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
