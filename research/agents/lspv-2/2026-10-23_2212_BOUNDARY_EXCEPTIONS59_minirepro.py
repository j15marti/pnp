#!/usr/bin/env python3
"""BOUNDARY-EXCEPTIONS59 independent minimal reproduction; Python stdlib only."""
from collections import Counter
from itertools import product
from random import Random

def canon(c): return tuple(sorted(c,key=lambda x:abs(x)))
def sat(F,a): return all(any(a[abs(l)]==(l>0) for l in c) for c in F)
def vars_(F): return sorted({abs(l) for c in F for l in c})
def valid22(F):
    count=Counter(l for c in F for l in c)
    return all(len(c)==3 and len({abs(l) for l in c})==3 for c in F) and (
       len({frozenset(c) for c in F})==len(F)) and all(
       count[v]==2 and count[-v]==2 for v in vars_(F))
def pair(F):
    index={frozenset(c):i for i,c in enumerate(F)}
    B=[];T=[];used=set()
    for i,c in enumerate(F):
        if i in used:continue
        partners=[]
        for lit in c:
            x=frozenset(-lit if x==lit else x for x in c)
            if x in index:partners.append(index[x])
        assert len(partners)<=1
        if partners:
            j=partners[0];used|={i,j}
            B.append(canon(set(c)&set(F[j])))
        else:
            T.append(c);used.add(i)
    return B,T
def k4():
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    inc=[[] for _ in range(4)]
    for i,(a,b) in enumerate(edges,1):inc[a].append(i);inc[b].append(i)
    return [tuple(row) for row in inc]+[tuple(-x for x in row) for row in inc]
def delta2():
    return [(1,2,4),(1,2,-4),(-2,3,5),(-2,3,-5),
            (-1,-3,6),(-1,-3,-6),(4,5,6),(-4,-5,-6)]
def outcome_rate(B,T):
    endpoints={}
    for i,(x,y) in enumerate(B):
        assert abs(x) not in endpoints and abs(y) not in endpoints
        endpoints[abs(x)]=(i,x); endpoints[abs(y)]=(i,y)
    counts=Counter(l for c in T for l in c)
    for v,(i,lit) in endpoints.items():
        assert counts[lit]==0 and counts[-lit]==2
    for v in vars_(T):
        if v not in endpoints:assert counts[v]==counts[-v] and counts[v] in (1,2)
    assert len(vars_(T))<=3*len(T)//2
    others=sorted(set(vars_(T))-set(endpoints))
    d=len(B)+len(others);success=0
    for row in product((False,True),repeat=d):
        a={}
        for i,(x,y) in enumerate(B):
            a[abs(x)]=row[i] if x>0 else not row[i]
            a[abs(y)]=(not row[i]) if y>0 else row[i]
        for j,v in enumerate(others):a[v]=row[len(B)+j]
        if sat(T,a):success+=1
    return success,2**d
def kernel(delta,P,seed):
    r=Random(seed)
    B=[(2*j+1,2*j+2) for j in range(P)]
    tok=[-v for v in range(1,2*P+1) for _ in range(2)]
    for j in range((3*delta-4*P)//2):
        v=2*P+j+1;tok += [v,-v]
    assert len(tok)==3*delta
    for _ in range(5000):
        r.shuffle(tok);T=[tuple(tok[j:j+3]) for j in range(0,len(tok),3)]
        if all(len({abs(l) for l in c})==3 for c in T) and len(set(T))==delta:
            return B,T
    raise AssertionError("source generation failed")
def run():
    F=delta2();assert valid22(F);B,T=pair(F)
    assert len(B)==3 and len(T)==2
    for bits in product((False,True),repeat=6):
        a=dict(zip(range(1,7),bits))
        assert sat(F,a)==sat(B+T,a)
    G=k4();assert valid22(G);B2,T2=pair(G)
    assert len(B2)==0 and len(T2)==8
    s,total=outcome_rate([],T2);assert 64*s>=total
    checks=0
    for delta in (2,4,6,8):
        for P in range(3*delta//4+1):
            b,t=kernel(delta,P,1000+delta*100+P)
            good,all_=outcome_rate(b,t)
            assert good>0
            assert 64*good>=all_ if delta==8 else 8*good>=(8-delta)*all_
            checks+=1
    print(dict(verified_sources=2,abstract_kernel_cases=checks,
               k4_delta8_successes=s,k4_distribution_size=total,
               status="computational controls, not asymptotic hardness"))
if __name__=="__main__":run()
