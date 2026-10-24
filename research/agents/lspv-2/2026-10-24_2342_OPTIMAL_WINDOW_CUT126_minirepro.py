#!/usr/bin/env python3
"""OPTIMAL-WINDOW-CUT126 independent mini, standard-library Python 3."""
from collections import deque
from itertools import product
import random, json

def events(seed, motifs, unsat):
    rng=random.Random(seed); out=[("OPEN",v) for v in (1,2,3)]
    nextvar=4
    for _ in range(motifs):
        k=rng.randint(2,6); pool=list(range(nextvar,nextvar+k));nextvar+=k
        out.extend(("OPEN",v) for v in pool)
        out.extend(("CLAUSE",(1,v,pool[(i+1)%k])) for i,v in enumerate(pool))
        out.extend(("CLOSE",v) for v in pool)
    clauses=[tuple(v if mask&(1<<i) else -v for i,v in enumerate((1,2,3))) for mask in range(8)]
    out.extend(("CLAUSE", clauses[1] if mask==0 and not unsat else c) for mask,c in enumerate(clauses))
    out.extend(("CLOSE",v) for v in (3,2,1))
    return out

def widths(ev):
    active=set();seen=set();w=[0]
    for k,v in ev:
        if k=="OPEN":
            assert v not in active and v not in seen
            active.add(v);seen.add(v)
        elif k=="CLOSE":
            assert v in active;active.remove(v)
        else:
            assert len({abs(x) for x in v})==3
            assert all(abs(x) in active for x in v)
        w.append(len(active))
    assert not active
    return w

def naive(w,b):
    L=len(w)-1;d=b//2; INF=1<<(2*max(w)+L.bit_length()+3)
    dp=[INF]*(L+1);dp[0]=0
    for j in range(1,L+1):
        upper=j-1 if j==L else j-d
        for i in range(max(0,j-b),upper+1):
            dp[j]=min(dp[j],dp[i]+(1<<(w[i]+w[j])))
    return dp[L]

def optimized(w,b):
    L=len(w)-1;d=b//2;W=max(w)
    INF=1<<(2*W+L.bit_length()+3)
    ring=[INF]*(b+1);rwidth=[0]*(b+1);ring[0]=0
    buckets=[deque() for _ in range(W+1)]
    for j in range(1,L):
        i=j-d
        if i>=0 and ring[i%(b+1)]<INF:
            v=ring[i%(b+1)];q=buckets[rwidth[i%(b+1)]]
            while q and q[-1][1]>=v:q.pop()
            q.append((i,v))
        best=INF
        for k,q in enumerate(buckets):
            while q and q[0][0]<j-b:q.popleft()
            if q:best=min(best,q[0][1]+(1<<(k+w[j])))
        ring[j%(b+1)]=best;rwidth[j%(b+1)]=w[j]
    return min(ring[i%(b+1)]+(1<<(rwidth[i%(b+1)]+w[L]))
               for i in range(max(0,L-b),L))

def greedy(w,b):
    L=len(w)-1;pos=0;path=[0]
    while pos<L:
        j=min(range(min(L,pos+b//2),min(L,pos+b)+1),key=lambda x:(w[x],x))
        path.append(j);pos=j
    return path

def cost(w,path):
    return sum(1<<(w[a]+w[b]) for a,b in zip(path,path[1:]))

def sat_brute(ev):
    clauses=[c for kind,c in ev if kind=="CLAUSE"]
    n=max(abs(x) for c in clauses for x in c)
    for bits in product((0,1),repeat=n):
        if all(any(bool(bits[abs(x)-1])==(x>0) for x in c) for c in clauses):
            return True
    return False

def run():
    checked=0;best=1;worse=0
    for m in (2,3,5,8):
        for seed in range(12):
            w=widths(events(20261024+seed+100*m,m,False))
            for b in (4,6,10,14,20):
                n=naive(w,b);o=optimized(w,b);g=cost(w,greedy(w,b))
                assert n==o and o<=g
                best=max(best,g/o);worse+=g>o;checked+=1
    for seed in range(8):
        f=events(123+seed,2,False);u=events(123+seed,2,True)
        assert widths(f)==widths(u)
        assert sat_brute(f) and not sat_brute(u)
        checked+=2
    return dict(checked=checked,failed=0,max_greedy_to_optimal_ratio=best,
                optimum_strictly_better=worse,
                status="COMPUTATIONAL restricted scheduling only, no ARC edge")
if __name__=="__main__":print(json.dumps(run(),indent=2))
