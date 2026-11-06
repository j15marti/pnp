#!/usr/bin/env python3
"""LSPV-3/458: reproducible random-3CNF width-3 Resolution local-closure audit.

Original distribution: m=8n independent uniformly signed proper 3-clauses
on n ambient labels, with replacement. Pure native strict Resolution only.
For full hostile controls and independent Node checker see archived ZIP in report.
"""
import collections
import itertools
import json
import math
import random
import time

def source(n, seed):
    rng = random.Random(seed)
    return [tuple(x if rng.randrange(2) else -x
                  for x in sorted(rng.sample(range(1, n+1), 3)))
            for _ in range(8*n)]

def support(c):
    return tuple(sorted(map(abs, c)))

def keys(c):
    return tuple(itertools.combinations(support(c), 2))

def resolve(a, b):
    aa = {abs(x):x for x in a}
    bb = {abs(x):x for x in b}
    out=set()
    for p in aa.keys() & bb.keys():
        if aa[p] != -bb[p]:
            continue
        c = (set(a) | set(b)) - {aa[p],bb[p]}
        if any(-x in c for x in c):
            continue
        out.add(tuple(sorted(c, key=lambda x:(abs(x),x))))
    return out

def count(f):
    idx=collections.defaultdict(list)
    for i,c in enumerate(f):
        for k in keys(c):
            idx[k].append(i)
    candidates=set()
    for ids in idx.values():
        candidates.update(itertools.combinations(ids, 2))
    equal=0
    first=[]
    for i,j in sorted(candidates):
        if support(f[i]) == support(f[j]):
            equal+=1
        for r in resolve(f[i], f[j]):
            if len(r)==3:
                first.append((i,j,r))
    occurrence=collections.Counter()
    for i,j,_ in first:
        occurrence[i]+=1
        occurrence[j]+=1
    shared=sum(math.comb(v,2) for v in occurrence.values() if v>=2)
    chain=0
    for i,j,r in first:
        candidates=set()
        for p in keys(r):
            candidates.update(idx.get(p,()))
        for k in candidates - {i,j}:
            if any(len(z)<=3 for z in resolve(r,f[k])):
                chain+=1
    pair_index=collections.defaultdict(list)
    for a,(_,_,r) in enumerate(first):
        for p in keys(r):
            pair_index[p].append(a)
    second_candidates=set()
    for ids in pair_index.values():
        second_candidates.update(itertools.combinations(ids,2))
    cross=0
    for u,v in second_candidates:
        i,j,r=first[u]
        k,l,s=first[v]
        if len({i,j,k,l})==4 and any(len(z)<=3 for z in resolve(r,s)):
            cross+=1
    return dict(equal_support=equal, first_width3=len(first),
                shared_first_source_pairs=shared,
                second_first_plus_source=chain,
                second_disjoint_first_pairs=cross)

def expectation(n):
    c=math.comb(n,3)
    m=8*n
    p=3*(n-3)/(2*c)
    q=p+3/(8*c)
    return dict(first_width3=math.comb(m,2)*p,
                equal_support=math.comb(m,2)/c,
                shared_first_source_pairs=m*math.comb(m-1,2)*p*p,
                second_first_plus_source=math.comb(m,2)*(m-2)*p*q,
                second_disjoint_first_pairs=3*math.comb(m,4)*p*p*q)

def main():
    start=time.perf_counter()
    rows=[]
    for n in (128,512,2048,8192):
        for seed in (11,23,37):
            f=source(n,seed)
            rows.append(dict(n=n,seed=seed,observed=count(f),
                             expected=expectation(n)))
    print(json.dumps(dict(run="LSPV3/458",scope="strict width-three RES",
                          rows=rows,seconds=round(time.perf_counter()-start,3)),
                     sort_keys=True,indent=2))

if __name__=="__main__":
    main()
