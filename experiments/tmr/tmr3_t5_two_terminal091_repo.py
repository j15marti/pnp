#!/usr/bin/env python3
"""TMR-3/091: exact T5 five-residue transfer. Run with python3, no dependencies."""
from itertools import product

def beat(a,b):
    return (b-a)%5 in (1,3)

def edge_vector(reverse=False):
    return tuple(int(beat(d,0) if reverse else beat(0,d)) for d in range(5))

def series(left,right):
    return tuple(sum(left[a]*right[(d-a)%5] for a in range(5)) for d in range(5))

def parallel(left,right):
    return tuple(left[d]*right[d] for d in range(5))

def count_unpinned(vector):
    return 5*sum(vector)

def biclique_vector(p):
    if p<2: raise ValueError("two distinct left terminals need p>=2")
    return (3*2**(p-1)-2,0,2**(p-2),2**(p-2),0)

def bouquet_count(k,p):
    if k<1: raise ValueError("requires at least one module")
    return count_unpinned(tuple(x**k for x in biclique_vector(p)))

def source_bouquet(k,p):
    arcs=[]; nxt=2
    for _ in range(k):
        left=[0,1]+list(range(nxt,nxt+p-2)); nxt+=p-2
        right=list(range(nxt,nxt+p)); nxt+=p
        arcs.extend((u,v) for u in left for v in right)
    return nxt,arcs

def brute(n,arcs,fixed=None):
    fixed=dict(fixed or {})
    colors=[-1]*n
    for v,c in fixed.items(): colors[v]=c
    adj=[[] for _ in range(n)]
    for u,v in arcs:
        if u==v:return 0
        adj[u].append((v,True));adj[v].append((u,False))
    def valid(v,c):
        return all(colors[w]<0 or (beat(c,colors[w]) if direct else beat(colors[w],c))
                   for w,direct in adj[v])
    if any(not valid(v,c) for v,c in fixed.items()):return 0
    def dfs():
        best=None;choices=None
        for v in range(n):
            if colors[v]>=0:continue
            opts=[c for c in range(5) if valid(v,c)]
            if not opts:return 0
            if choices is None or len(opts)<len(choices):best=v;choices=opts
        if best is None:return 1
        z=0
        for c in choices:
            colors[best]=c; z+=dfs(); colors[best]=-1
        return z
    return dfs()

if __name__=="__main__":
    checks=0
    assert edge_vector()==(0,1,0,1,0); checks+=1
    assert edge_vector(True)==(0,0,1,0,1); checks+=1
    for p in range(2,5):
        n,arcs=source_bouquet(1,p)
        for d,v in enumerate(biclique_vector(p)):
            assert brute(n,arcs,{0:0,1:d})==v
            checks+=1
    for k in range(1,4):
        for p in range(2,5):
            n,arcs=source_bouquet(k,p)
            if n<=16:
                assert brute(n,arcs)==bouquet_count(k,p)
                checks+=1
    for a,b in product((False,True),repeat=2):
        E1=[(1,0)] if a else [(0,1)]
        E2=[(1,2)] if b else [(2,1)]
        assert count_unpinned(series(edge_vector(a),edge_vector(b)))==brute(3,E1+E2)
        E3=[(1,0)] if b else [(0,1)]
        assert count_unpinned(parallel(edge_vector(a),edge_vector(b)))==brute(2,E1+E3)
        checks+=2
    assert brute(1,[(0,0)])==0;checks+=1
    assert brute(2,[(0,1),(1,0)])==0;checks+=1
    print("TMR-3/091 compact checks passed:",checks)
    print("B(20,8):",bouquet_count(20,8))
