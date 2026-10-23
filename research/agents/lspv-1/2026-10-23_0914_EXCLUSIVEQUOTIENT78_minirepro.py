#!/usr/bin/env python3
"""EXCLUSIVEQUOTIENT78 independent mini-reproduction, standard library only.
Tests exhaustive small original SAT, projected binary interface and quotient SAT.
The asymptotic threshold imports Zhang-Peitl-Szeider SAT2024 and is not numerically proved.
"""
from collections import Counter, defaultdict
from itertools import product

def truth(C,a): return any(a[abs(x)]==(x>0) for x in C)
def sat(F,a): return all(truth(c,a) for c in F)
def exists(F,n): return any(sat(F,dict(enumerate(bits,1))) for bits in product((False,True),repeat=n))

def reduce(F):
    n=max(abs(x) for C in F for x in C)
    occ=Counter(x for C in F for x in C)
    assert all(occ[i]==occ[-i]==2 for i in range(1,n+1))
    assert all(len(set(map(abs,C)))==3 for C in F)
    assert len(F)==len({tuple(sorted(C)) for C in F})
    D={frozenset(C):i for i,C in enumerate(F)}
    used=set();B=[];T=[]
    for i,C in enumerate(F):
        if i in used: continue
        pairs=[(D[frozenset((set(C)-{x})|{-x})],x) for x in C if frozenset((set(C)-{x})|{-x}) in D]
        assert len(pairs)<=1
        used.add(i)
        if pairs:
            j,x=pairs[0];used.add(j);B.append(tuple(y for y in C if y!=x))
        else:T.append(C)
    U={abs(x) for C in T for x in C}
    incid=defaultdict(list)
    for i,C in enumerate(B):
        for x in C: incid[abs(x)].append((i,x))
    adj=defaultdict(list)
    for x,E in incid.items():
        if x not in U:
            assert len(E)==2 and E[0][1]==-E[1][1]
            i,_=E[0];j,_=E[1];assert i!=j
            adj[i].append(j);adj[j].append(i)
        else: assert len(E)==1
    seen=set();P=[]
    for i in range(len(B)):
        if i in seen:continue
        stack=[i];seen.add(i);nodes=[]
        while stack:
            v=stack.pop();nodes.append(v)
            for j in adj[v]:
                if j not in seen:seen.add(j);stack.append(j)
        endpoints=[x for j in nodes for x in B[j] if abs(x) in U]
        if endpoints:
            assert len(endpoints)==2
            P.append(tuple(endpoints))
    mapping={};z=0
    for L,R in P:
        z+=1
        mapping[abs(L)]=(z,L<0)
        mapping[abs(R)]=(z,R>0)
    for x in sorted(U):
        if x not in mapping:z+=1;mapping[x]=(z,False)
    Q=[]
    for C in T:
        D=[]
        for lit in C:
            j,flip=mapping[abs(lit)]
            D.append(-j if (flip != (lit<0)) else j)
        if len({abs(x) for x in D})<3:
            assert any(-x in D for x in D)
        else:Q.append(tuple(D))
    qocc=Counter(x for C in Q for x in C)
    assert all(cnt<=2 for cnt in qocc.values())
    return len(B),len(T),len(P),Q,z

S=[
 (5,-2,3),(1,-4,-3),(-1,2,6),(-1,2,-6),
 (1,-5,6),(4,-5,-6),(-4,5,3),(-2,4,-3)]
T=[
 (1,-5,3),(1,-2,-3),(-1,2,6),(-1,2,-6),
 (4,-2,6),(4,-5,-6),(-4,5,3),(-4,5,-3)]
for name,F in (("mixed-path",S),("tautology-drop",T)):
    p,d,P,Q,z=reduce(F)
    assert exists(F,6)==exists(Q,z)
    print(name,dict(n=6,m=8,p=p,delta=d,paths=P,quotient_clauses=len(Q),quotient_coordinates=z,SAT=exists(F,6)))
print("PASS: source-coherent quotient mini-check. Complexity separation remains OPEN.")
