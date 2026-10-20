#!/usr/bin/env python3
"""SCHUR-CONTROL1: matched-random-code control for Schur-square dimension over GF(2). P vs NP OPEN."""
import random, json, itertools
def rank(rows):
    basis={}
    for r in rows:
        while r:
            h=r.bit_length()-1
            if h in basis: r^=basis[h]
            else: basis[h]=r;break
    return len(basis)
def sq(G): return rank([a&b for a,b in itertools.combinations_with_replacement(G,2)])
def rm(r,m):
    pts=range(1<<m); G=[]
    for S in itertools.chain.from_iterable(itertools.combinations(range(m),d) for d in range(r+1)):
        v=0
        for p in pts:
            if all((p>>i)&1 for i in S): v|=1<<p
        G.append(v)
    return G
out={}
for r,m in ((1,4),(1,5),(1,6),(2,5),(2,6)):
    G=rm(r,m);k=rank(G);n=1<<m
    rng=random.Random(20261020+10*r+m)
    rs=[sq([rng.getrandbits(n) for _ in range(k)]) for _ in range(200)]
    assert sq(G)==rank(rm(min(2*r,m),m))  # RM(r)^{*2}=RM(2r)
    out[f"RM({r},{m})"]=dict(n=n,k=k,sq_structured=sq(G),sq_random_min=min(rs),sq_random_max=max(rs),
        generic_bound=min(n,k*(k+1)//2))
print(json.dumps(out,indent=1))
