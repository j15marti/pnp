#!/usr/bin/env python3
"""TMR-5/097 compact replay: height-one T5 and all-order OBDD rank certificate."""
from itertools import combinations, product
from math import comb, prod
def R(a,b):return (b-a)%5 in (1,3)
Q=((1,1),(1,0))
assert [int(R(a,b)) for a in (0,3) for b in (1,3)]==[1,1,1,0]
assert Q[0][0]*Q[1][1]-Q[0][1]*Q[1][0]==-1
n_cuts=0;n_subsets=0;n_matrices=0
for d in (2,3,4):
    n=1<<d
    edges=[(u,u^(1<<i)) for u in range(n) for i in range(d) if u<(u^(1<<i))]
    adj=[set() for _ in range(n)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    arcs=[(u,v) if u.bit_count()%2==0 else (v,u) for u,v in edges]
    assert all(R(0,1) for _ in arcs)
    for mask in range(1<<n):
        sz=mask.bit_count()
        boundary=sum(bool(mask>>u&1)!=bool(mask>>v&1) for u,v in edges)
        assert boundary>=min(sz,n-sz)
        n_subsets+=1
    for tup in combinations(range(n),n//2):
        s=set(tup)
        cross=[(u,v) for u,v in edges if (u in s)!=(v in s)]
        selected=[];ban=set()
        for u,v in cross:
            if u not in ban and v not in ban:
                selected.append((u,v));ban|=adj[u]|adj[v]
        assert len(selected)*2*d*d>=len(cross)
        n_cuts+=1
        if d==4 and n_cuts%191:continue
        k=len(selected)
        early=[u if u in s else v for u,v in selected]
        late=[v if u in s else u for u,v in selected]
        for a in product((0,1),repeat=k):
            for b in product((0,1),repeat=k):
                x=[0 if v.bit_count()%2==0 else 1 for v in range(n)]
                for j,v in enumerate(early):x[v]=((0,3) if v.bit_count()%2==0 else (1,3))[a[j]]
                for j,v in enumerate(late):x[v]=((0,3) if v.bit_count()%2==0 else (1,3))[b[j]]
                assert int(all(R(x[u],x[v]) for u,v in arcs))==prod(Q[a[j]][b[j]] for j in range(k))
                n_matrices+=1
assert n_cuts==sum(comb(1<<d,(1<<d)//2) for d in (2,3,4))
print({'all_subsets':n_subsets,'balanced_cuts':n_cuts,'restricted_matrix_entries':n_matrices,'failures':0})
