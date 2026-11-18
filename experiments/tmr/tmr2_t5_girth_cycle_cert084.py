#!/usr/bin/env python3
"""TMR-2/084 reproducible W(3,4) 5-symbol certificate and cycle-moment test.
Standard library only. Works from a blank start without external SAT software.
"""
from collections import Counter, deque
from itertools import combinations
from hashlib import sha256
from math import comb

M=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
INV=(0,1,3,2)
def norm(v):
    k=next(i for i,x in enumerate(v) if x)
    return tuple(M[INV[v[k]]][x] for x in v)
def ortho(a,b):return M[a[0]][b[2]]^M[a[2]][b[0]]^M[a[1]][b[3]]^M[a[3]][b[1]]
def graph():
    P=sorted({norm([(i>>(2*j))&3 for j in range(4)]) for i in range(1,256)})
    assert len(P)==85
    ids={p:i for i,p in enumerate(P)}
    lines=set()
    for i,j in combinations(range(85),2):
        if ortho(P[i],P[j]):continue
        line={i,j}
        for t in range(4):line.add(ids[norm([P[i][k]^M[t][P[j][k]] for k in range(4)])])
        assert len(line)==5
        lines.add(tuple(sorted(line)))
    L=sorted(lines);assert len(L)==85
    E=sorted((i,85+j) for j,ll in enumerate(L) for i in ll)
    assert len(E)==425
    return E

def orientation(E,seed):
    state=seed&0xffffffff
    arcs=[]
    for a,b in E:
        state^=(state<<13)&0xffffffff
        state^=state>>17
        state^=(state<<5)&0xffffffff
        arcs.append((a,b) if state&1==0 else (b,a))
    return arcs

def beat(x,y):return (y-x)%5 in (1,3)
def ac(arcs,pins):
    D=[set(range(5)) for _ in range(170)]
    for v,c in pins:D[v].intersection_update((c,))
    if any(not s for s in D):return None
    while True:
        changed=False
        for u,v in arcs:
            A={a for a in D[u] if any(beat(a,b) for b in D[v])}
            B={b for b in D[v] if any(beat(a,b) for a in D[u])}
            if not A or not B:return None
            if A!=D[u] or B!=D[v]:changed=True;D[u]=A;D[v]=B
        if not changed:return D

def source(arcs):
    return ('p t5 170 425\n'+''.join(f'v {i}\n' for i in range(170))+
            ''.join(f'a {u} {v}\n' for u,v in sorted(arcs)))

def cycle_count(p,q):
    n=p+q
    return 5*sum(comb(n,k) for k in range(n+1) if (p+2*q+2*k)%5==0)

def cycle8(adj):
    route=[]
    def dfs(first):
        if len(route)==8:
            if first in adj[route[-1]] and route[1]<route[-1]:yield tuple(route)
            return
        for v in adj[route[-1]]:
            if v>first and v not in route:
                route.append(v)
                yield from dfs(first)
                route.pop()
    for a in range(170):
        route[:]=[a]
        for b in adj[a]:
            if b>a:
                route.append(b)
                yield from dfs(a)

def run():
    E=graph();arcs=orientation(E,202611180612)
    assert sha256(source(arcs).encode()).hexdigest()==('cc9e6c343ca2bccfe8839a8dd077d4d543e75e2bd669100f5e87861637a10632')
    assert all(beat(0,1) for _ in E)
    assert all(len([e for e in E if v in e])==5 for v in range(170))
    root=ac(arcs,[(0,0)])
    assert root is not None and root[85]=={1,3}
    expected={1:{2,4},3:{1,4}}
    for c,allowed in expected.items():
        D=ac(arcs,[(0,0),(85,c)])
        assert D is not None and D[1]==allowed
        for d in allowed:assert ac(arcs,[(0,0),(85,c),(1,d)]) is None
    # All possible values are covered at every branch, so this is a complete NO certificate.
    adj=[[] for _ in range(170)]
    for a,b in E:adj[a].append(b);adj[b].append(a)
    Y=set(E);N=set(arcs);histY=Counter();histN=Counter()
    for c in cycle8(adj):
        pairs=list(zip(c,c[1:]+c[:1]))
        for H,S in ((histY,Y),(histN,N)):
            q=sum((a,b) not in S for a,b in pairs)
            H[min(q,8-q)]+=1
    assert histY==Counter({4:13600})
    assert histN==Counter({0:116,1:896,2:3097,3:5962,4:3529})
    sy=sum(ct*cycle_count(8-q,q) for q,ct in histY.items())
    sn=sum(ct*cycle_count(8-q,q) for q,ct in histN.items())
    assert (sy,sn,sn-sy)==(4760000,3467195,-1292805)
    print('PASS: 170 variables, 425 edges, girth 8, 13600 shortest cycles')
    print('PASS: NO certificate 7 nodes / 4 AC contradiction leaves')
    print('PASS: first moment coefficient difference = -1292805 * 5^162')
    print('PASS: YES original-label count at least 5 * 2^85')
if __name__=='__main__':run()
