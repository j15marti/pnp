#!/usr/bin/env python3
"""GATE332 public finite reproducer: source-acquired best OBDD block order."""
from functools import lru_cache
from collections import Counter
import random
POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=POS+tuple(tuple(-x for x in c) for c in NEG)

def valid(cs,n):
    if len(cs)*3!=4*n:return False
    p=Counter();q=Counter(); seen=set()
    for c in cs:
        if len(c)!=3 or any(type(x)!=int or not 1<=abs(x)<=n for x in c):return False
        if len(set(map(abs,c)))!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for x in c:(p if x>0 else q)[abs(x)]+=1
    return all(p[i]==q[i]==2 for i in range(1,n+1))

def sat(cs,m):
    return all(any(bool(m&(1<<(abs(x)-1)))==(x>0) for x in c) for c in cs)

def components(cs,n):
    a=[set() for _ in range(n+1)]
    for c in cs:
        t=set(map(abs,c))
        for v in t:a[v].update(t-{v})
    done=set();out=[]
    for v in range(1,n+1):
        if v in done:continue
        q=[v];done.add(v)
        for x in q:
            for y in sorted(a[x]):
                if y not in done:done.add(y);q.append(y)
        out.append(sorted(q))
    return out

def local_best(cs,ids):
    b=len(ids); idx={v:i+1 for i,v in enumerate(ids)}
    local=[tuple((1 if x>0 else -1)*idx[abs(x)] for x in c) for c in cs if abs(c[0]) in idx]
    truth=[sat(local,x) for x in range(1<<b)]
    costs={}
    for S in range(1<<b):
        pinned=[i for i in range(b) if S&(1<<i)]
        remain=[i for i in range(b) if not S&(1<<i)]
        tail=[sum(((a>>j)&1)<<v for j,v in enumerate(remain)) for a in range(1<<len(remain))]
        signatures=set()
        for a in range(1<<len(pinned)):
            fixed=sum(((a>>j)&1)<<v for j,v in enumerate(pinned))
            signatures.add(sum(int(truth[fixed|v])<<j for j,v in enumerate(tail)))
        for j,v in enumerate(remain):
            step=1<<j
            costs[S,v]=sum(any(((sig>>a)^(sig>>(a|step)))&1 for a in range(1<<len(remain)) if not a&step) for sig in signatures)
    @lru_cache(None)
    def dp(S):
        if S==(1<<b)-1:return (0,())
        options=[]
        for v in range(b):
            if not S&(1<<v):
                future=dp(S|(1<<v));options.append((costs[S,v]+future[0],(v,)+future[1]))
        return min(options)
    score,order=dp(0)
    return score,[ids[v] for v in order]

def bdd_nodes(cs,n,order):
    truth=[]
    for a in range(1<<n):
        mask=sum(((a>>j)&1)<<(v-1) for j,v in enumerate(order))
        truth.append(sat(cs,mask))
    nodes={}
    def rec(depth,vec):
        if all(v==vec[0] for v in vec):return int(vec[0])
        lo=rec(depth+1,vec[::2]);hi=rec(depth+1,vec[1::2])
        if lo==hi:return lo
        key=(depth,lo,hi)
        if key not in nodes:nodes[key]=len(nodes)+2
        return nodes[key]
    rec(0,truth)
    return len(nodes)

def run(t):
    n=9*t;rng=random.Random(332+t);perm=list(range(1,n+1));rng.shuffle(perm)
    cs=[tuple((1 if x>0 else -1)*perm[9*i+abs(x)-1] for x in c) for i in range(t) for c in F9]
    rng.shuffle(cs)
    assert valid(cs,n)
    parts=components(cs,n);acquired=[local_best(cs,p) for p in parts]
    order=sum((o for _,o in acquired),[])
    return cs,order,sum(s for s,_ in acquired)

if __name__=='__main__':
    assert valid(F9,9)
    cs,o,s=run(1)
    assert s==52 and bdd_nodes(cs,9,o)==52
    cs,o,s=run(2)
    assert s==104 and bdd_nodes(cs,18,o)==104
    assert sum(sat(cs,a) for a in range(1<<18))==4900
    assert not valid(F9+(F9[0],),9)
    print({'F9':52,'renamed_F9_squared':104,'bad_cut_rank_squared':196,'source_models_squared':4900,'order_acquired':o})
