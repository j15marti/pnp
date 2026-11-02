#!/usr/bin/env python3
"""LSPV-1 CONNECTED-FOUR-DEFECT-FACTOR315: independent structural reproducer.
This tests canonical structure and source witnesses, NOT a polynomial blossom implementation.
For full independently implemented 64-branch MILP verification see reproducibility archive.
P versus NP OPEN.
"""
from collections import Counter,defaultdict
from itertools import product
import hashlib,json

K6P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
K6=K6P+tuple(tuple(-v for v in c) for c in K6P)
PS={1:1,3:0,5:0,6:1}
PU={1:0,3:0,5:0,6:1}

def grammar(F):
    if not F or any(len(c)!=3 or len({abs(x) for x in c})!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)) for c in F):return False
    n=max(abs(x) for c in F for x in c)
    counts=Counter(x for c in F for x in c)
    return 3*len(F)==4*n and len({tuple(sorted(c)) for c in F})==len(F) and all(counts[i]==counts[-i]==2 for i in range(1,n+1))

def sat(F,a):return all(any((x>0)==bool(a[abs(x)]) for x in c) for c in F)

def k6_models(p):
    return [dict(zip(range(1,7),v)) for v in product((0,1),repeat=6) if all(v[i-1]==b for i,b in p.items()) and sat(K6,dict(zip(range(1,7),v)))]

def grid(k):
    def port(i,j,s):return (i%k,j%k,s)
    edges=set();yes=set()
    for i in range(k):
        for j in range(k):
            N,E,S,W=[port(i,j,s) for s in "NESW"]
            for a,b,on in ((N,E,1),(E,S,0),(S,W,1),(W,N,0),(E,port(i,j+1,"W"),0),(S,port(i+1,j,"N"),0)):
                edge=tuple(sorted((a,b)))
                assert edge not in edges
                edges.add(edge)
                if on:yes.add(edge)
    ordered=sorted(edges)
    inc=defaultdict(list)
    for idx,edge in enumerate(ordered,1):
        for v in edge:inc[v].append(idx)
    P=tuple(tuple(sorted(inc[v])) for v in sorted(inc))
    F=P+tuple(tuple(-v for v in c) for c in P)
    witness={i:int(edge in yes) for i,edge in enumerate(ordered,1)}
    assert grammar(F) and sat(F,witness)
    return F,witness

def connected(F):
    G=defaultdict(set)
    for c in F:
        ss=set(map(abs,c))
        for x in ss:G[x]|=ss-{x}
    seen={1};todo=[1]
    while todo:
        u=todo.pop()
        for v in G[u]-seen:seen.add(v);todo.append(v)
    return len(seen)==len(G)

def source(k):
    assert k>=4 and k%2==0
    F,a=grid(k);n=len(a)
    e=next(x for x in F[0] if not a[x])
    local=tuple(tuple((1 if x>0 else -1)*(abs(x)+n) for x in c) for c in K6)
    C=tuple(n+3 if x==e else x for x in F[0])
    D=tuple(e if x==n+3 else x for x in local[3])
    H=(C,)+F[1:]+local[:3]+(D,)+local[4:]
    assert grammar(H) and connected(H)
    yes=k6_models(PS)
    assert len(yes)==3 and k6_models(PU)==[]
    a.update({n+i:v for i,v in yes[0].items()})
    assert a[e]==0 and sat(H,a)
    P={tuple(sorted(c)) for c in H if c[0]>0}
    M={tuple(sorted(-z for z in c)) for c in H if c[0]<0}
    U=P^M;B={x for c in U for x in c}
    assert len(U)==4 and len(B)==6
    pin={n+i:v for i,v in PU.items()}
    assert all(any(abs(z) not in pin or bool(pin[abs(z)])==(z>0) for z in c) for c in H)
    free=[i for i in range(1,7) if i not in PU]
    leaves=[]
    for bits in product((0,1),repeat=len(free)):
        b={**PU,**dict(zip(free,bits))}
        fail=[j for j,c in enumerate(K6) if j!=3 and not any((z>0)==bool(b[abs(z)]) for z in c)]
        assert fail
        leaves.append(fail[0])
    assert leaves==[0,1,0,6]
    return dict(k=k,n=len(a),m=len(H),unpaired=len(U),boundary=len(B),
                paired=len(P&M),delta=2*len(a)-len(H),
                tw_floor=(k-2)/2,verified_witness=True,
                same_original_unsat_four_leaves=leaves)

if __name__=="__main__":
    x=[source(k) for k in (4,6,8)]
    assert [v["n"] for v in x]==[102,222,390]
    print(json.dumps({"status":"RESTRICTED_COMPUTATIONAL_P_VS_NP_OPEN",
                      "cases":x,"note":"Exact source verification, not native FLMV or general g,f-factor code."},indent=2))
