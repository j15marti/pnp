#!/usr/bin/env python3
"""Compact exact signed-flux two-cut repro, no external libraries.
For complete U198/V198 and source-indexed controls see local full archive.
"""
from collections import Counter,defaultdict
from itertools import product
def source(cross=False):
    F=[]
    for q in (1,5):
        a,b,c,d=range(q,q+4)
        F += [[9,a,b],[a,c,d],[b,c,d],[-9,-c,-d],[-a,-b,-c],[-a,-b,-d]]
    if cross:F[0][2],F[6][1]=F[6][1],F[0][2]
    return F
def valid(F):
    n=max(abs(z) for c in F for z in c)
    s=Counter(z for c in F for z in c)
    return n%3==0 and 3*len(F)==4*n and len({tuple(sorted(c)) for c in F})==len(F) and all(s[x]==s[-x]==2 for x in range(1,n+1)) and all(len(c)==3 and len({abs(z) for z in c})==3 and (all(z>0 for z in c) or all(z<0 for z in c)) for c in F)
def components(C):
    adj=defaultdict(set)
    for cl in C:
        vs=[abs(z) for z in cl]
        for v in vs:adj[v].update(vs)
    unseen=set(adj);out=[]
    while unseen:
        todo=[min(unseen)];seen=set()
        while todo:
            x=todo.pop()
            if x in seen:continue
            seen.add(x);todo.extend(adj[x]-seen)
        unseen-=seen;out.append(seen)
    return out
def branch(F,x,value):
    kept=[];deleted=[];short=[]
    for j,c in enumerate(F):
        if any(abs(z)==x and int(z>0)==value for z in c):deleted.append(j)
        else:
            if any(abs(z)==x for z in c):short.append(j)
            kept.append([z for z in c if abs(z)!=x])
    cc=components(kept); assert len(deleted)==len(short)==2
    n=max(abs(z) for c in F for z in c)
    assert sum(len(z) for z in cc)==n-1
    for K in cc:
        a=sum(sum(abs(z) in K for z in F[j] if abs(z)!=x) for j in deleted)
        b=sum(any(abs(z) in K for z in F[j] if abs(z)!=x) for j in short)
        P=sum(c[0]>0 for c in kept if all(abs(z) in K for z in c))
        Q=sum(c[0]<0 for c in kept if all(abs(z) in K for z in c))
        if value:assert 3*P==2*len(K)-a and 3*Q-b==2*len(K)
        else:assert 3*Q==2*len(K)-a and 3*P-b==2*len(K)
        assert a+b in (3,6)
    assert len(cc)<=2 and max(map(len,cc))*2>=n-1
    return len(cc)
if __name__=="__main__":
    for cross in (False,True):
        F=source(cross);assert valid(F)
        hist=Counter(branch(F,x,v) for x in range(1,10) for v in (0,1))
        models=sum(all(any(int(z>0)==bits[abs(z)-1] for z in cl) for cl in F) for bits in product((0,1),repeat=9))
        assert models==(86 if cross else 98) and hist[2]==(1 if cross else 2)
        if cross:
            G=[[z for z in cl if abs(z)!=9] for cl in F]
            assert len(components(G))==1 and branch(F,9,1)==2
        print("T9C" if cross else "T9",models,dict(hist))
    print("PASS; restricted theorem only; P versus NP OPEN")