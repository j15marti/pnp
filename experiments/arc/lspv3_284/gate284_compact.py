#!/usr/bin/env python3
"""LSPV-3 GATE284 compact independently runnable source-class control.

Full six-source producer, independent verifier, U198/V198 original fixtures,
raw checkpoint XOR, and resource ledger are in the verified GATE284 ZIP.
This small runner audits the exact edge-cover and consistency statement on Y6.
Requires networkx. The edge-cover theorem is classical, not new.
"""
from itertools import combinations
from collections import Counter
import networkx as nx

Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
    [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
def valid_m22(F,n):
    if 3*len(F)!=4*n:return False
    counts={i:[0,0] for i in range(1,n+1)}
    seen=set()
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        if not (all(z>0 for z in C) or all(z<0 for z in C)):return False
        if any(z==0 or abs(z)>n for z in C):return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key)
        for z in C:counts[abs(z)][z<0]+=1
    return all(x==[2,2] for x in counts.values())
def false_ids(F,a):
    return [j for j,C in enumerate(F) if all(bool(a>>(abs(z)-1)&1)!=(z>0) for z in C)]
def matching_rho(F,a,free=None):
    ids=false_ids(F,a)
    G=nx.Graph()
    G.add_nodes_from(ids)
    occ={}
    for j in ids:
        vv=[abs(z) for z in F[j] if free is None or abs(z) in free]
        if not vv:return None,len(ids),0
        for i in vv:occ.setdefault(i,[]).append(j)
    for ii,js in occ.items():
        if len(js)>2:raise ValueError("source is not strict 2P2N")
        if len(js)==2:G.add_edge(js[0],js[1])
    nu=len(nx.max_weight_matching(G,maxcardinality=True))
    return len(ids)-nu,len(ids),nu
def brute_rho(F,a,n):
    U=false_ids(F,a)
    for size in range(n+1):
        for S in combinations(range(1,n+1),size):
            if all(any(abs(z) in S for z in F[j]) for j in U):return size
    raise AssertionError("no cover")
def ball(F,n,seed,r,with_matching):
    stats={'nodes':0,'matching_calls':0,'source_clause_upper_probes':0,
           'last_assignment':None}
    def walk(i,a,d):
        stats['nodes']+=1
        if d>r:return False
        if with_matching:
            k,U,nu=matching_rho(F,a,set(range(i+1,n+1)))
            stats['matching_calls']+=1
            stats['source_clause_upper_probes']+=3*len(F)+3*U
            if k is None or d+k>r:return False
        else:
            stats['source_clause_upper_probes']+=3*len(F)
            if any(all(abs(z)<=i for z in C) and
                   all(bool(a>>(abs(z)-1)&1)!=(z>0) for z in C) for C in F):
                return False
        if i==n:
            if not false_ids(F,a):
                stats['last_assignment']=a
                return True
            return False
        return walk(i+1,a,d) or walk(i+1,a^(1<<i),d+1)
    stats['SAT_in_ball']=walk(0,seed,0)
    return stats
def main():
    F=Y6;n=6
    assert valid_m22(F,n)
    assert not valid_m22(F+[F[0]],n)
    models=[a for a in range(1<<n) if not false_ids(F,a)]
    assert len(models)==20
    for a in range(1<<n):
        exact=matching_rho(F,a)[0]
        assert exact==brute_rho(F,a,n)
        assert all(abs(exact-matching_rho(F,a^(1<<i))[0])<=1 for i in range(n))
        assert exact<=min((a^b).bit_count() for b in models)
    for r in [1,2,3]:
        expected=any(b.bit_count()<=r for b in models)
        p=ball(F,n,0,r,False)
        q=ball(F,n,0,r,True)
        assert p['SAT_in_ball']==q['SAT_in_ball']==expected
        print('radius',r,'baseline',p,'matching',q)
    print('PASS: Y6 64/64 exact covers, 384 adjacent Lipschitz edges, 20 valid models')
if __name__=='__main__':main()
