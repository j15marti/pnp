#!/usr/bin/env python3
"""SIMPLECOVER76 ten-vertex parallel-edge source audit. Standard library only."""
import itertools, json
from collections import Counter

def example():
    E=[]
    for i in range(3):
        a,b,c=3*i+1,3*i+2,3*i+3
        E += [(a,b),(a,b),(a,c),(b,c),(0,c)]
    return E

def lift(E):
    V=10; q=len(E); C=[[] for _ in range(V)]
    for j,(u,v) in enumerate(E):
        C[u].append(j+1); C[v].append(-j-1)
    for j in range(q):
        x=j+1; y=q+j+1; z=q+(j+1)%q+1
        C += [[y,-z,x],[y,-z,-x]]
    return C

def matching_size(E):
    for k in range(len(E)//2,-1,-1):
        for subset in itertools.combinations(range(len(E)),k):
            endpoints=[u for i in subset for u in E[i]]
            if len(set(endpoints))==2*k:return k
    raise AssertionError

def mincover(E):
    for k in range(len(E)+1):
        for subset in itertools.combinations(range(len(E)),k):
            if len({v for i in subset for v in E[i]})==10:return k
    raise AssertionError

def check():
    E=example();C=lift(E);n=30;m=len(C)
    assert len(E)==15 and m==40 and 4*n==3*m
    assert all(len(c)==len(set(map(abs,c)))==3 for c in C)
    assert len({tuple(sorted(c)) for c in C})==len(C)
    counts=Counter(v for cl in C for v in cl)
    assert all(counts[v]==counts[-v]==2 for v in range(1,n+1))
    pairs=[]
    for i,j in itertools.combinations(range(m),2):
        a={abs(v):v>0 for v in C[i]}
        b={abs(v):v>0 for v in C[j]}
        if a.keys()==b.keys() and sum(a[v]!=b[v] for v in a)==1:pairs.append((i,j))
    assert len(pairs)==15 and all(i>=10 for p in pairs for i in p)
    nu=matching_size(E);tau=mincover(E)
    assert nu==4 and tau==6 and tau==10-nu
    assert 9*nu<4*10-1  # no Haxell-Scott SIMPLE graph transfer
    witness=None
    for bits in range(1<<len(E)):
        truth={j+1: bool(bits>>j&1) for j in range(len(E))}
        if all(any(truth[abs(v)]==(v>0) for v in cl) for cl in C[:10]):
            witness=truth;break
    assert witness is not None
    witness.update({15+j+1:False for j in range(15)})
    assert all(any(witness[abs(v)]==(v>0) for v in cl) for cl in C)
    assert not any(t and not t for t in (False,True))
    return dict(n=n,m=m,pairs=len(pairs),delta=10,nu=nu,min_cover=tau,
                valid_exact_2_2=True,source_sat=True,
                false_simple_bound=(5*10+1)//9)
if __name__=="__main__":print(json.dumps(check(),indent=2,sort_keys=True))
