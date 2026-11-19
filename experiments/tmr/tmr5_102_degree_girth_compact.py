#!/usr/bin/env python3
"""TMR-5/102 standalone critical-degree and 5-core audit, Python stdlib only."""
from collections import deque, Counter
from itertools import combinations

W = [{1,3}, {2,4}, {0,3}, {1,4}, {0,2}]
def q(h,u,v): return (u in W[h]) != (v in W[h])

def core(n, edges):
    adj = [set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v); adj[v].add(u)
    deg=[len(a) for a in adj]; alive=[True]*n
    todo=deque(i for i in range(n) if deg[i]<5); order=[]
    while todo:
        v=todo.popleft()
        if not alive[v]: continue
        assert deg[v]<5
        alive[v]=False; order.append(v)
        for u in adj[v]:
            if alive[u]:
                deg[u]-=1
                if deg[u]==4: todo.append(u)
    return adj,order,[v for v in range(n) if alive[v]]

def peel_coloring(n, edges):
    adj,order,remaining=core(n,edges)
    if remaining: return None
    colors=[-1]*n
    for v in reversed(order):
        forbidden={colors[u] for u in adj[v] if colors[u]>=0}
        colors[v]=next(k for k in range(5) if k not in forbidden)
    assert all(colors[u]!=colors[v] for u,v in edges)
    lift(n,edges,colors)
    return colors

def lift(n, edges, colors):
    assignment=colors[:]
    for u,v in edges:
        assert colors[u]!=colors[v]
        h = colors[u] if colors[v] in W[colors[u]] else colors[v]
        assignment.append(h)
    assert len(assignment)==n+len(edges)
    assert all(q(assignment[n+i],assignment[u],assignment[v])
               for i,(u,v) in enumerate(edges))

def mycielski(n, edges):
    new=set(edges)
    for u,v in edges:
        new.add(tuple(sorted((n+u,v))))
        new.add(tuple(sorted((n+v,u))))
    for u in range(n): new.add((n+u,2*n))
    return 2*n+1,sorted(new)

def moore(g):
    if g%2: return 1+5*sum(4**i for i in range((g-1)//2))
    return 2*sum(4**i for i in range(g//2))

def main():
    assert sum(q(a,b,c) for a in range(5) for b in range(5)
               for c in range(5))==60
    k6=list(combinations(range(6),2))
    assert len(core(6,k6)[2])==6
    for e in k6:
        assert peel_coloring(6,[f for f in k6 if f!=e]) is not None
    n=5
    edges=[tuple(sorted((i,(i+1)%5))) for i in range(5)]
    for _ in range(3): n,edges=mycielski(n,edges)
    assert (n,len(edges))==(47,236)
    assert len(core(n,edges)[2])==47
    deleted=Counter(len(core(n,[f for f in edges if f!=e])[2]) for e in edges)
    assert deleted==Counter({47:211,46:25}),deleted
    bip=[(u,v) for u in range(5) for v in range(5,11)]
    assert len(core(11,bip)[2])==11
    lift(11,bip,[0]*5+[1]*6)
    assert [moore(g) for g in range(3,8)]==[6,10,26,42,106]
    print({'Q_accept':60,'K6_deletions_SAT':15,'Mycielski_n':n,'Mycielski_m':len(edges),
           'Mycielski_deleted_core_counts':dict(deleted),'K5_6_core':11,
           'Moore_n_g3_to_g7':[moore(g) for g in range(3,8)]})
if __name__=='__main__': main()
