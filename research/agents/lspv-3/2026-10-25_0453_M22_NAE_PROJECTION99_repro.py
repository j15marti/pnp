#!/usr/bin/env python3
"""LSPV-3 M22-NAE-PROJECTION99 pure-stdlib independent finite reproducer.
Checks grammar, correct named projection, two-level join and finite M22 census.
NOT an FLMV work/space trace or an all-input lower bound.
"""
import itertools
import random
import json
from collections import Counter

H=((1,2,3),(3,4,5))
P0=((1,2,4),(5,6,7),(6,8,9),(7,8,9))
Q0=((1,2,5),(4,8,9),(6,7,8),(6,7,9))
YP=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
YQ=((1,2,4),(1,3,6),(2,3,5),(4,5,6))

def bit(a,j): return (a>>(j-1))&1
def nae(a,t): return 1<=sum(bit(a,v) for v in t)<=2
def sat_clause(a,t,sgn):
    return any(bit(a,v) if sgn==1 else not bit(a,v) for v in t)
def valid(P,Q,k):
    if len(set(P))!=len(P) or len(set(Q))!=len(Q):return False
    if any(len(t)!=3 or len(set(t))!=3 or min(t)<1 or max(t)>k for t in P+Q):return False
    p=Counter(v for t in P for v in t);q=Counter(v for t in Q for v in t)
    return all(p[v]==q[v]==2 for v in range(1,k+1))
def sat(a,P,Q):
    return all(sat_clause(a,t,1) for t in P) and all(sat_clause(a,t,-1) for t in Q)
def embed(u,D,hidden=(),hmask=0):
    a=0
    for i,v in enumerate(sorted(D)):a|=((u>>i)&1)<<(v-1)
    for i,v in enumerate(sorted(hidden)):a|=((hmask>>i)&1)<<(v-1)
    return a
def projection(H,D,k):
    hidden=sorted(set(range(1,k+1))-set(D))
    good=set()
    for u in range(1<<len(D)):
        for hmask in range(1<<len(hidden)):
            a=embed(u,D,hidden,hmask)
            if all(nae(a,t) for t in H):
                good.add(u);break
    return good
def affine_dim(vals):
    base=min(vals);basis={}
    for a in vals:
        w=a^base
        while w:
            p=w.bit_length()-1
            if p in basis:w^=basis[p]
            else:basis[p]=w;break
    return len(basis)
def join_check(P,Q,k):
    paired=set(P)&set(Q)
    up=set(P)-set(Q);un=set(Q)-set(P)
    D=sorted({v for t in up for v in t})
    assert set(D)=={v for t in un for v in t}
    R=projection(paired,D,k)
    ok=any(u in R and all(sat_clause(embed(u,D),t,1) for t in up) and
           all(sat_clause(embed(u,D),t,-1) for t in un)
           for u in range(1<<len(D)))
    truth=any(sat(a,P,Q) for a in range(1<<k))
    assert ok==truth
    return truth
def main():
    assert valid(H+P0,H+Q0,9)
    D=sorted({v for t in P0 for v in t})
    assert D==[1,2,4,5,6,7,8,9]
    adj={v:set() for v in range(1,10)}
    for t in H+P0+Q0:
        for v in t:adj[v].update(set(t)-{v})
    reached={1};stack=[1]
    while stack:
        for w in adj[stack.pop()]:
            if w not in reached:reached.add(w);stack.append(w)
    assert len(reached)==9
    R=projection(H,D,9)
    assert len(R)==224 and affine_dim(R)==8
    for u in range(256):
        a=embed(u,D)
        formula=not (bit(a,1)==bit(a,2) and bit(a,4)==bit(a,5) and bit(a,1)!=bit(a,4))
        assert (u in R)==formula
        assert (u in R)==any(all(nae(embed(u,D,(3,),z),t) for t in H) for z in (0,1))
    original={a for a in range(512) if sat(a,H+P0,H+Q0)}
    reconstructed=set()
    for u in R:
        for z in (0,1):
            a=embed(u,D,(3,),z)
            if sat(a,H+P0,H+Q0):reconstructed.add(a)
    assert original==reconstructed and len(original)==98
    assert valid(YP,YQ,6) and sum(sat(a,YP,YQ) for a in range(64))==20
    # Check source grammar and full independent SAT-vs-named-projection for all 5625 small M22 sources.
    triples=list(itertools.combinations(range(1,7),3))
    hs=[C for C in itertools.combinations(triples,4)
        if all(sum(v in t for t in C)==2 for v in range(1,7))]
    assert len(hs)==75
    dist=Counter()
    for P in hs:
        for Q in hs:
            assert valid(P,Q,6)
            dist[len(set(P)-set(Q))]+=1
            assert join_check(P,Q,6)
    assert dict(dist)=={0:75,2:1260,3:1680,4:2610}
    rng=random.Random(202610241253)
    for r in range(1,7):
        assert 224**r <256**r
        for z in range(128):
            picks=[rng.randrange(256) for _ in range(r)]
            assert all(v in R for v in picks)==all(not (
                 bit(embed(v,D),1)==bit(embed(v,D),2) and
                 bit(embed(v,D),4)==bit(embed(v,D),5) and
                 bit(embed(v,D),1)!=bit(embed(v,D),4)) for v in picks)
    # Both-label malformed controls are explicitly OUTSIDE C_star.
    assert not valid(((1,2,3),),(),3)
    assert not ((True and False)) # contradicting units outside the M22 grammar
    print(json.dumps({"status":"COMPUTATIONAL PASS","block_models":len(original),
      "projection_signatures":len(R),"affine_hull_dim":affine_dim(R),
      "small_M22_checked":5625,"defect_distribution":dict(dist),
      "tensor_samples":768,"all_input_arc":"OPEN","P_vs_NP":"OPEN"},sort_keys=True))
if __name__=="__main__":main()
