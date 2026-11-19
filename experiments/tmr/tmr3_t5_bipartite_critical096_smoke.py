#!/usr/bin/env python3
"""TMR-3/096: standalone exact T5 SAT witness audit of a physically critical
31-vertex directed graph (girth eight, bipartite underlying, DAG).
Stdlib only. Full 80-vertex incidence generator and independent MILP
crosscheck are in the separately supplied reproducibility archive.
"""
from collections import deque

N=31
ARCS=[(15,27),(12,24),(6,28),(4,26),(12,17),(0,19),(12,19),
(7,19),(16,4),(24,1),(28,9),(5,20),(2,26),(22,5),(12,30),
(30,6),(20,13),(18,10),(22,9),(17,14),(24,11),(10,29),
(16,3),(18,9),(2,28),(2,27),(26,11),(10,21),(1,25),
(15,21),(1,23),(22,14),(9,23),(20,0),(17,15),(8,25),
(18,7),(8,27),(13,25),(3,19),(4,29),(29,13)]
F=[sum(1<<((a+d)%5) for d in (1,3)) for a in range(5)]
B=[sum(1<<((a-d)%5) for d in (1,3)) for a in range(5)]
FW=[0]*32; BW=[0]*32
for mask in range(32):
    for a in range(5):
        if mask & (1<<a):
            FW[mask] |= F[a]
            BW[mask] |= B[a]

def sat(edges):
    nbr=[[] for _ in range(N)]
    for u,v in edges:
        nbr[u].append((v,False))
        nbr[v].append((u,True))
    nodes=[0]
    def dfs(dom):
        nodes[0]+=1
        q=deque(range(N)); inq=[True]*N
        while q:
            u=q.popleft();inq[u]=False
            for v,reverse in nbr[u]:
                new=dom[v] & (BW[dom[u]] if reverse else FW[dom[u]])
                if new==0:return None
                if new !=dom[v]:
                    dom[v]=new
                    if not inq[v]:q.append(v);inq[v]=True
        pending=[v for v in range(N) if dom[v].bit_count()>1]
        if not pending:
            return [m.bit_length()-1 for m in dom]
        v=min(pending,key=lambda u:(dom[u].bit_count(),-len(nbr[u]),u))
        mask=dom[v]
        while mask:
            bit=mask&-mask;mask-=bit
            child=dom.copy();child[v]=bit
            out=dfs(child)
            if out is not None:return out
        return None
    d=[31]*N;d[0]=1
    return dfs(d),nodes[0]

def check(edges,x):
    return (x is not None and len(x)==N
            and all(0<=a<5 for a in x)
            and all((x[v]-x[u])%5 in (1,3) for u,v in edges))

def main():
    assert len(ARCS)==42 and len(set(ARCS))==42
    assert sat(ARCS)[0] is None, 'Full H must be UNSAT'
    totals=0
    for i,(u,v) in enumerate(ARCS):
        rest=ARCS[:i]+ARCS[i+1:]
        x,nodes=sat(rest)
        assert check(rest,x), ('Deletion not SAT',i)
        assert (x[v]-x[u])%5 in (0,2,4), ('Deleted edge not violated',i)
        totals+=nodes
    print('TMR-3/096: UNSAT source, 42/42 exact SAT deletion witnesses verified')
    print('DFS recursion nodes across deletions:',totals,'(implementation-specific)')
    assert totals==707
    print('COMPUTATIONAL control only; P versus NP remains OPEN')

if __name__=='__main__':
    main()
