#!/usr/bin/env python3
"""T5 H24: exhaustive core certificate plus independent original-arc deletion witnesses."""
from itertools import product
W = (1,1,0,2,1,2,1,1,0,1,1,1,2,2,2,1)
PAIRS = [(i,j) for i in range(4) for j in range(4,8)]
WORDS = ('FF','FB','BB')
R = lambda a,b: (b-a)%5 in (1,3)
SUPPORT = ({1,2,4},{0,2,3},{1,3,4})
arcs = []
for k,((u,v),t) in enumerate(zip(PAIRS,W)):
    m=8+k
    for x,y,c in ((u,m,WORDS[t][0]),(m,v,WORDS[t][1])):
        arcs.append((x,y) if c=='F' else (y,x))
assert len(arcs)==32

counts=[0]*17
for tail in product(range(5),repeat=7):
    a=(0,)+tail
    bad=[k for k,((u,v),t) in enumerate(zip(PAIRS,W))
         if (a[v]-a[u])%5 not in SUPPORT[t]]
    if not bad: counts[0]+=1
    if len(bad)==1: counts[bad[0]+1]+=1
assert counts==[0,14,4,1,6,15,10,11,4,21,15,9,14,9,11,20,1],counts

# Uses ONLY original arcs, not the precomputed endpoint supports.
def witness(deleted):
    active=[(u,v) for e,(u,v) in enumerate(arcs) if e!=deleted]
    deg=[0]*24
    for u,v in active: deg[u]+=1;deg[v]+=1
    calls=[0]
    def rec(dom):
        calls[0]+=1
        changed=True
        while changed:
            changed=False
            for u,v in active:
                du={x for x in dom[u] if any(R(x,y) for y in dom[v])}
                dv={y for y in dom[v] if any(R(x,y) for x in du)}
                if not du or not dv: return None
                if du!=dom[u]: dom[u]=du;changed=True
                if dv!=dom[v]: dom[v]=dv;changed=True
        todo=[u for u in range(24) if len(dom[u])>1]
        if not todo:
            a=[next(iter(d)) for d in dom]
            assert all(R(a[u],a[v]) for u,v in active)
            return a
        v=min(todo,key=lambda u:(len(dom[u]),-deg[u],u))
        for c in sorted(dom[v]):
            ds=[d.copy() for d in dom];ds[v]={c}
            x=rec(ds)
            if x is not None: return x
        return None
    d=[set(range(5)) for _ in range(24)];d[0]={0}
    return rec(d),calls[0]

no,calls=witness(-1)
assert no is None
assert calls==23,calls
max_calls=0
for e in range(32):
    a,calls=witness(e)
    assert a is not None
    assert all(e==k or R(a[u],a[v]) for k,(u,v) in enumerate(arcs))
    assert not R(a[arcs[e][0]],a[arcs[e][1]])
    max_calls=max(max_calls,calls)
assert max_calls==31,max_calls
print("H24: 24 vertices, 32 arcs, girth 8, UNSAT, all 32 deletions SAT")
print("Anchored thread-deletion counts:",counts[1:])
print("Independent original-arc AC3 H UNSAT calls:",23,"max deletion calls:",max_calls)
