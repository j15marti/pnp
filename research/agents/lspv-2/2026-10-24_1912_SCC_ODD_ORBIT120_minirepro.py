#!/usr/bin/env python3
"""SCC-ODD-ORBIT120: exact 2-CNF plus one parity check. Python stdlib.
A uniform restricted constructive algorithm, NOT an unrestricted SAT contraction.
"""
from collections import defaultdict, Counter
from itertools import product
from random import Random
import json

def graph(n, clauses):
    G=[[] for _ in range(2*n)]; R=[[] for _ in range(2*n)]
    def ix(x): return 2*(abs(x)-1)+(x<0)
    for cl in clauses:
        a,b=(cl[0],cl[0]) if len(cl)==1 else cl
        for u,v in ((ix(a)^1,ix(b)),(ix(b)^1,ix(a))):
            G[u].append(v); R[v].append(u)
    return G,R

def components(G,R):
    seen=set();order=[]
    for root in range(len(G)):
        if root in seen: continue
        seen.add(root);todo=[(root,0)]
        while todo:
            v,k=todo[-1]
            if k==len(G[v]): order.append(v);todo.pop();continue
            w=G[v][k];todo[-1]=(v,k+1)
            if w not in seen: seen.add(w);todo.append((w,0))
    co=[-1]*len(G);j=0
    for root in reversed(order):
        if co[root]>=0:continue
        co[root]=j;todo=[root]
        while todo:
            v=todo.pop()
            for w in R[v]:
                if co[w]<0:co[w]=j;todo.append(w)
        j+=1
    return co

def check(a,clauses):
    return all(any(a[abs(x)-1]==int(x>0) for x in c) for c in clauses)

def solve2(n,clauses,extra=()):
    G,R=graph(n,list(clauses)+[(x,) for x in extra]);co=components(G,R)
    if any(co[2*i]==co[2*i+1] for i in range(n)):return None,co,G
    a=[int(co[2*i]>co[2*i+1]) for i in range(n)]
    assert check(a,clauses) and all(a[abs(x)-1]==int(x>0) for x in extra)
    return a,co,G

def parity(a,mask):return sum(a[i] for i in mask)%2

def decide(n,clauses,mask,rhs):
    charges=Counter();charges['scc_calls']+=1
    a,co,G=solve2(n,clauses)
    if a is None:return False,None,'B-UNSAT',dict(charges)
    if parity(a,mask)==rhs:return True,a,'BASE-WITNESS',dict(charges)
    groups=defaultdict(list)
    key=lambda i:tuple(sorted((co[2*i],co[2*i+1])))
    for i in range(n):groups[key(i)].append(i)
    for grp,ids in groups.items():
        if len(set(ids)&set(mask))%2==0:continue
        charges['candidate_checks']+=1;charges['scc_calls']+=1
        i=ids[0];lit=(i+1) if not a[i] else -(i+1)
        b,_,_=solve2(n,clauses,(lit,))
        if b is None:continue
        reps={co[v]:v for v in range(2*n)}
        def value(c,sol):
            v=reps[c]
            return sol[v//2] if v%2==0 else 1-sol[v//2]
        D={c for c in reps if not value(c,a) and value(c,b)}
        edges={c:set() for c in D};indeg={c:0 for c in D}
        for u,ws in enumerate(G):
            cu=co[u]
            if cu not in D:continue
            for v in ws:
                cv=co[v]
                if cv in D and cv!=cu and cv not in edges[cu]:
                    edges[cu].add(cv);indeg[cv]+=1
        ready=[c for c in D if indeg[c]==0];topo=[]
        while ready:
            c=ready.pop();topo.append(c)
            for v in edges[c]:
                indeg[v]-=1
                if not indeg[v]:ready.append(v)
        assert len(topo)==len(D),'Condensation is acyclic'
        t=a[:]
        for c in reversed(topo):
            ids=groups[key(reps[c]//2)]
            for k in ids:t[k]^=1
            charges['group_flips']+=1
            assert check(t,clauses)
            if parity(t,mask)==rhs:return True,t,'ODD-SCC-ORBIT',dict(charges)
        raise AssertionError('Odd-weight flexible SCC flip must change parity')
    return False,None,'PARITY-FIXED',dict(charges)

def brute(n,B,mask,rhs):
    return any(check(x,B) and parity(x,mask)==rhs for x in product((0,1),repeat=n))

if __name__=='__main__':
    rng=Random(202610241912);out=Counter();last=None
    for n in range(1,8):
        pool=[(s*i,) for i in range(1,n+1) for s in (-1,1)]
        pool += [(s*i,t*j) for i in range(1,n+1) for j in range(i+1,n+1)
                          for s in (-1,1) for t in (-1,1)]
        for trial in range(300):
            B=[rng.choice(pool) for _ in range(rng.randrange(3*n+3))]
            mask=tuple(i for i in range(n) if rng.randrange(2));rhs=rng.randrange(2)
            yes,w,route,c=decide(n,B,mask,rhs)
            assert yes==brute(n,B,mask,rhs)
            assert not yes or (w is not None and check(w,B) and parity(w,mask)==rhs)
            out[route]+=1;out['tests']+=1;out['SCC_calls']+=c['scc_calls']
    for n in (16,64,128,256):
        eq=[cl for i in range(1,n) for cl in ((-i,i+1),(i,-(i+1)))]
        for rhs in (0,1):
            y,w,r,c=decide(n,eq,tuple(range(n)),rhs)
            assert y==(rhs==0);out['large_eq']+=1
        imp=[(-i,i+1) for i in range(1,n)]
        for rhs in (0,1):
            y,w,r,c=decide(n,imp,tuple(range(n)),rhs)
            assert y;out['large_imp']+=1
    print(json.dumps({'run':'SCC-ODD-ORBIT120','status':'COMPUTATIONAL',
                      'counts':dict(out),'failures':0,'P_versus_NP':'OPEN'},sort_keys=True))
