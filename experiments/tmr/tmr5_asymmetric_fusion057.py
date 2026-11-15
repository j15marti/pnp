#!/usr/bin/env python3
"""Independent TMR-5 audit: directed zero-closure and asymmetric cheap fusion.

A laboratory AND-obligation protocol, NOT a SAT solver or physical Turing machine.
All checks use exact rational fractions. No third-party packages.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
import heapq, json

checks = 0
edges_seen = 0

def graph(n, mode):
    states = [("".join(z), t) for z in product('ULRD', repeat=n) for t in (0, 1)]
    edges = {s: [] for s in states}
    for z, t in states:
        a = (z,t)
        edges[a].append(((z, 1-t), 0, 'TAG'))
        for i,c in enumerate(z):
            if c == 'U':
                for v in 'LR':
                    edges[a].append(((z[:i]+v+z[i+1:],t), 0, 'CHOOSE_'+v))
            elif c in 'LR':
                edges[a].append(((z[:i]+'D'+z[i+1:],t), 1, 'DISCHARGE'))
        if z != 'D'*n:
            edges[a].append((a,1,'NOP'))
            if mode == 'all':
                edges[a].append((('D'*n,t),1,'FUSE_ALL'))
            if mode == 'free':
                edges[a].append((('D'*n,t),0,'FREE_GOAL'))
            if mode == 'Ronly' and z == 'R'*n:
                edges[a].append((('D'*n,t),1,'FUSE_R'))
    return edges

def zero_closure(edges, s):
    reach={s}; pending=[s]
    while pending:
        x=pending.pop()
        for y,w,_ in edges[x]:
            if w==0 and y not in reach:
                reach.add(y);pending.append(y)
    return reach

def q(z,g,i):
    return sum((2*g if c in 'UR' else F(0)) +
               (2*i if c in 'UL' else F(0)) for c in z)

def pot(edges, weights):
    g,i=weights
    return {s:min(q(v[0],g,i) for v in zero_closure(edges,s)) for s in edges}

def shortest(edges,start):
    pq=[(0,start)];dist={start:0}
    while pq:
        d,s=heapq.heappop(pq)
        if d!=dist[s]:continue
        if s[0] and set(s[0])=={'D'}:return d
        for nxt,w,_ in edges[s]:
            if d+w<dist.get(nxt,10**9):
                dist[nxt]=d+w;heapq.heappush(pq,(d+w,nxt))
    raise AssertionError('goal unreachable')

def admissible(edges,h):
    global checks,edges_seen
    bad=[]
    for s,rows in edges.items():
        for t,w,r in rows:
            edges_seen+=1;checks+=1
            if h[s]-h[t]>w:bad.append((s,t,w,r,str(h[s]-h[t])))
    for s in edges:
        if set(s[0])=={'D'}:
            checks+=1
            assert h[s]==0
    return bad

results=[]
for n in range(1,5):
    for mode in ('base','Ronly','all','free'):
        edges=graph(n,mode)
        weights={'base':(F(1,2),F(1,2)),
                 'Ronly':(F(1,2*n),F(1,2)),
                 'all':(F(1,2*n),F(1,2*n)),
                 'free':(F(1,2),F(1,2))}[mode]
        h=pot(edges,weights)
        bad=admissible(edges,h)
        assert not bad, (n,mode,bad[:2]);checks+=1
        init=('U'*n,0)
        exact=shortest(edges,init)
        expected={'base':n,'Ronly':1,'all':1,'free':0}[mode]
        assert exact==expected and h[init]==expected;checks+=1
        if n>=2 and mode=='Ronly':
            old=pot(edges,(F(1,2),F(1,2)))
            violations=[(s,t,r,str(old[s]-old[t])) for s,rows in edges.items()
                        for t,w,r in rows if old[s]-old[t]>w]
            assert violations and any(r=='FUSE_R' for _,_,r,_ in violations);checks+=1
        else: violations=[]
        # Exact rational grid is an independent finite check of claimed cones.
        candidates=sorted({F(0),F(1,2*n),F(1,4),F(1,2),F(3,4),F(1)})
        for g in candidates:
            for i in candidates:
                hh=pot(edges,(g,i))
                ok=all(hh[s]-hh[t]<=w for s,rows in edges.items() for t,w,_ in rows)
                bound={'base':(F(1,2),F(1,2)),
                       'Ronly':(F(1,2*n),F(1,2)),
                       'all':(F(1,2*n),F(1,2*n))}.get(mode)
                if bound is not None:
                    assert ok==(g<=bound[0] and i<=bound[1]),(n,mode,g,i,ok)
                else:
                    assert ok
                checks+=1
        results.append(dict(n=n,mode=mode,states=len(edges),edges=sum(map(len,edges.values())),
                            lambda_gamma=str(weights[0]),lambda_interface=str(weights[1]),
                            initial_potential=str(h[init]),shortest_paid_work=exact,
                            old_half_weight_violations=len(violations)))

print(json.dumps(dict(tag='TMR5_ASYMFUS057',status='COMPUTATIONAL independent exact-rational audit',
    checks=checks,edges_verified=edges_seen,failures=0,results=results,
    theorem='Ronly cone: 0<=gamma<=1/(2n), 0<=interface<=1/2; initial h(U^n)=1',
    smallest_paid_fusion_counterexample='n=2: free U^2 -> R^2, paid FUSE_R one step, old half weights charge 2',
    gap='NOT SAT; no physical machine or arbitrary-decider bridge; superpoly initial gap OPEN'),indent=2,sort_keys=True))
