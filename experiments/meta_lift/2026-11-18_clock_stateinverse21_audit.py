#!/usr/bin/env python3
"""Finite controls for CLOCKSTATEINVERSE21. No asymptotic or PH claim is tested.
Input is an N-bit string, N a power of 2. Time-inhomogeneous transition
schedule is represented as schedule[time][state][input_bit].
"""
import json, random, itertools, datetime
from functools import lru_cache

SEED = 202611180713
rng = random.Random(SEED)
stats = {"stationary_cases":0,"inhomogeneous_cases":0,"product_cases":0,
         "endpoint_checks":0,"exhaustive_reach_checks":0,"canonical_bit_checks":0,
         "hostile_cases":0,"failures":0}


def run(schedule, word, start=0):
    s=start
    for i,b in enumerate(word):
        s=schedule[i][s][b]
    return s


def canonical_factory(schedule, start=0):
    N=len(schedule)
    assert N and (N&(N-1)) == 0
    Q=len(schedule[0]); n=N.bit_length()-1
    @lru_cache(None)
    def reach(a,k,p,q):
        if k == 0:
            return schedule[a][p][0] == q or schedule[a][p][1] == q
        half=1<<(k-1)
        return any(reach(a,k-1,p,r) and reach(a+half,k-1,r,q) for r in range(Q))
    @lru_cache(None)
    def mid(a,k,p,q):
        assert k>0 and reach(a,k,p,q)
        half=1<<(k-1)
        return next(r for r in range(Q) if reach(a,k-1,p,r) and reach(a+half,k-1,r,q))
    def bit(target,i):
        assert 0<=i<N and reach(0,n,start,target)
        a=0; p=start; q=target
        for k in range(n,0,-1):
            r=mid(a,k,p,q)
            half=1<<(k-1)
            if i < a+half:
                q=r
            else:
                a+=half; p=r
        return 0 if schedule[a][p][0]==q else 1
    def make(target):
        return tuple(bit(target,i) for i in range(N))
    return reach,make,bit


def random_schedule(N,Q):
    return [tuple((rng.randrange(Q),rng.randrange(Q)) for _ in range(Q)) for _ in range(N)]


def test(schedule, words, label):
    N=len(schedule); Q=len(schedule[0]); n=N.bit_length()-1
    reach,make,bit=canonical_factory(schedule)
    words=list(words)
    endpoints={run(schedule,w) for w in words}
    for q in endpoints:
        assert reach(0,n,0,q)
        g=make(q)
        assert run(schedule,g)==q
        stats["endpoint_checks"]+=1
        for i in range(N):
            assert bit(q,i)==g[i]
            stats["canonical_bit_checks"]+=1
    for w in words:
        q=run(schedule,w)
        g=make(q)
        assert run(schedule,g)==q
        stats[label]+=1
        stats["endpoint_checks"]+=1
    # Independent brute force all paths on small N
    if N<=8:
        possible={run(schedule,w) for w in itertools.product((0,1),repeat=N)}
        for q in range(Q):
            assert reach(0,n,0,q)==(q in possible)
            stats["exhaustive_reach_checks"]+=1

# All 2-state stationary machines, N=8, all 256 sources.
for trans in itertools.product(range(2),repeat=4):
    tab=tuple((trans[2*s],trans[2*s+1]) for s in range(2))
    test([tab]*8,itertools.product((0,1),repeat=8),"stationary_cases")

# Random address-sensitive transition programs, all inputs on N=8.
for _ in range(90):
    test(random_schedule(8,3),itertools.product((0,1),repeat=8),"inhomogeneous_cases")

# Larger N with random inputs. This exercises layered midpoint indexing.
for _ in range(20):
    test(random_schedule(16,4),(tuple(rng.randrange(2) for _ in range(16)) for _ in range(100)),"inhomogeneous_cases")

# Two independently time-varying streamers represented by one product state.
for _ in range(20):
    A=random_schedule(8,2);B=random_schedule(8,2)
    product=[]
    for t in range(8):
        product.append(tuple(tuple(2*A[t][s//2][b]+B[t][s%2][b] for b in range(2)) for s in range(4)))
    reach,make,bit=canonical_factory(product)
    for w in itertools.product((0,1),repeat=8):
        u=run(A,w);v=run(B,w)
        q=run(product,w)
        assert q == 2*u+v
        g=make(q)
        assert run(A,g)==u and run(B,g)==v
        stats["product_cases"]+=1
        stats["endpoint_checks"]+=2

# Time-dependent equality recognizer as a hostile boundary: output 1 only on h.
h=(1,0,1,1,0,1,0,0)
compare=[]
for t in range(8):
    # state 1 means all prior bits agreed. state 0 is rejecting sink.
    compare.append(((0,0),tuple(int(b==h[t]) for b in (0,1))))
reach,make,bit=canonical_factory(compare,start=1)
assert run(compare,h,start=1)==1
assert run(compare,tuple(0 for _ in range(8)),start=1)==0
assert make(1)==h
assert sum(run(compare,w,start=1)==1 for w in itertools.product((0,1),repeat=8))==1
stats["hostile_cases"]+=256

out={"name":"CLOCKSTATEINVERSE21", "seed":SEED,
     "scope":"finite semantic reference for conditional PH/PSPACE preimage theorem",
     "stats":stats,"status":"COMPUTATIONAL; no complexity collapse simulated",
     "limitations":["all finite controls operate on explicitly represented transition tables",
       "not a test of P=NP or P=PSPACE", "no near-linear CHMY machine reduction",
       "theorem requires output factorization through terminal state and source-independent transition program"]}
path='/mnt/data/2026-11-18_CLOCKSTATEINVERSE21_raw.json'
with open(path,'w',encoding='utf8') as f:json.dump(out,f,indent=2,sort_keys=True)
print(json.dumps(out,indent=2))
