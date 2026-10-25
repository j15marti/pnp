#!/usr/bin/env python3
"""Compact exact M22 chain + two-level existential projection audit."""
from itertools import product
P=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
M=[(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def source(p):
    clauses=[]
    for i in range(p):
        o=6*i
        for c in P+M:
            clauses.append(tuple((1 if z>0 else -1)*(abs(z)+o) for z in c))
    for i in range(p-1):
        j=8*i+1;k=8*i+8
        a=list(clauses[j]);b=list(clauses[k])
        a[a.index(6*i+1)]=6*(i+1)+1
        b[b.index(6*(i+1)+1)]=6*i+1
        clauses[j]=tuple(a);clauses[k]=tuple(b)
    return tuple(clauses)
def projection(F,inside):
    I=set(inside)
    H=[c for c in F if any(abs(v) in I for v in c)]
    G=[c for c in F if not any(abs(v) in I for v in c)]
    B=sorted({abs(v) for c in H for v in c}-I)
    factors=[]
    for clause in H:
        vs=tuple(sorted({abs(v) for v in clause}))
        good=set()
        for z in product((0,1),repeat=len(vs)):
            a=dict(zip(vs,z))
            if any(a[abs(v)]==(v>0) for v in clause):good.add(z)
        factors.append((vs,good))
    maximum=0
    for v in sorted(I):
        picked=[(vs,s) for vs,s in factors if v in vs]
        factors=[(vs,s) for vs,s in factors if v not in vs]
        if not picked:continue
        vs=tuple(sorted(set().union(*(set(a) for a,_ in picked))-{v}))
        maximum=max(maximum,len(vs)+1)
        good=set()
        for z in product((0,1),repeat=len(vs)):
            a=dict(zip(vs,z))
            for d in (0,1):
                a[v]=d
                if all(tuple(a[x] for x in u) in s for u,s in picked):
                    good.add(z);break
        factors.append((vs,good))
    nogoods=[]
    for z in product((0,1),repeat=len(B)):
        a=dict(zip(B,z))
        if not all(tuple(a[x] for x in vs) in s for vs,s in factors):
            nogoods.append(tuple(-v if a[v] else v for v in B))
    return tuple(G+nogoods),maximum,len(B),len(nogoods)
def two(p):
    F=source(p)
    for q in (p-max(2,int(p**.5)),p-max(1,int(p**.25))):
        active={abs(z) for c in F for z in c}
        I={v for v in active if (v-1)//6<q}
        I-={abs(v) for c in F if any((abs(z)-1)//6>=q for z in c)
                           for v in c if (abs(v)-1)//6<q}
        if q>0:I-={6*(q-1)+j for j in (1,2,3)}
        F,w,b,n=projection(F,I)
        yield (len(F),w,b,n)
if __name__=="__main__":
    assert len(source(256))==2048
    assert list(two(256))==[(133,7,5,2),(37,7,5,2)]
    assert list(two(512))==[(181,7,5,2),(37,7,5,2)]
    print("PASS",list(two(256)),list(two(512)))
