#!/usr/bin/env python3
"""Independent compact peer reproducer for M22-MAXDEFECT-FACTOR101.
Finite source semantics only. Not a physical FLMV time-space instrument.
Full extended local auditor SHA256:
04377166bcfdfc679f594fbf5f43ab348cb9c59ca6a347beb32c449611201caf
"""
import itertools
import random
import math
from collections import Counter

SEED = 202610241355

def graph(r):
    rng = random.Random(SEED + 101*r)
    used = [set() for _ in range(r)]
    factors = []
    for _ in range(4):
        for trial in range(5000):
            p=list(range(r)); rng.shuffle(p)
            if all(p[i] not in used[i] for i in range(r)):
                for i in range(r): used[i].add(p[i])
                factors.append(p)
                break
        else:
            raise ValueError("Failed to find disjoint matching")
    return factors

def build(r):
    parts=graph(r)
    edges=[(r+i,2*r+parts[j][i]) for j in range(4) for i in range(r)]
    clauses=[]
    for sign, block in ((1,edges[:2*r]),(-1,edges[2*r:])):
        for j,(u,v) in enumerate(block):
            clauses.append((sign,tuple(sorted((j//2,u,v)))))
    return clauses,edges

def validate(clauses,k):
    if len(clauses)!=len(set(clauses)): return False
    occ=Counter()
    for sign,t in clauses:
        if sign not in (-1,1) or len(t)!=3 or len(set(t))!=3: return False
        if min(t)<0 or max(t)>=k: return False
        for v in t: occ[(v,sign)]+=1
    return all(occ[(v,s)]==2 for v in range(k) for s in (-1,1)) and 3*len(clauses)==4*k

def sat(F,mask):
    return all(any(mask>>v&1 for v in t) if sign==1
               else any(not(mask>>v&1) for v in t)
               for sign,t in F)

def lengths(k,m):
    return [(4*(m+4*d)+2)*math.ceil(math.log2(64*(k+2*d+m+4*d+1)))
            for d in (0,1,2)]

def frontier(F,r,perm):
    cnt=Counter();seen=set();best=0;at=None
    for idx in perm:
        for v in F[idx][1]:
            if v>=r: cnt[v]+=1;seen.add(v)
        now=sum(0<cnt[v]<4 for v in range(r,3*r))
        best=max(best,now)
        if at is None and len(seen)>=r:at=(seen.copy(),now)
    assert all(cnt[v]==4 for v in range(r,3*r))
    return best,at

def main():
    for r in (4,5,6,8,12,16,24):
        F,E=build(r);k=3*r
        assert validate(F,k)
        assert len(F)==4*r
        P={t for s,t in F if s==1};Q={t for s,t in F if s==-1}
        assert len(P)==len(Q)==2*r and len(P&Q)==0
        Bleft=sum(1<<v for v in range(r,2*r))
        Bright=sum(1<<v for v in range(2*r,3*r))
        for a in (range(1<<r) if r<=8 else (0,1,(1<<r)-1)):
            assert sat(F,Bleft|a) and sat(F,Bright|a)
        if r<=5:
            models=sum(sat(F,x) for x in range(1<<k))
            assert models==({4:346,5:1304}[r])
        vals=[]
        rand=random.Random(SEED+r)
        for j in range(16):
            perm=list(range(len(F)));rand.shuffle(perm)
            mx,at=frontier(F,r,perm)
            U,live=at
            crossing=sum((u in U)!=(v in U) for u,v in E)
            assert len(U) in (r,r+1) and crossing<=4*live
            vals.append(mx)
        lens=lengths(k,len(F))
        assert lens[0]<lens[1]<lens[2]
        print("r,k,q,models,frontier_min,levels",
              r,k,2*r,models if r<=5 else "not brute-forced",min(vals),lens)
    YP=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
    YN=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
    Y=[(s,tuple(v-1 for v in t)) for s,rows in ((1,YP),(-1,YN)) for t in rows]
    assert validate(Y,6) and sum(sat(Y,x) for x in range(64))==20
    assert sat(Y,0b000111)
    paired=[(s,tuple(v-1 for v in t)) for s in (-1,1) for t in YP]
    assert validate(paired,6) and sum(sat(paired,x) for x in range(64))==18
    assert not validate(Y+Y[:1],6)
    print("PASS: all compact finite source and boundary checks; ARC/DIRECT OPEN")

if __name__=="__main__":
    main()
