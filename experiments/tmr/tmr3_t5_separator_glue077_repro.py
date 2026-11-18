#!/usr/bin/env python3
"""Readable TMR-3/077 repro. Complete fixed-budget b=1,t=2 separator solver;
all-input exact 2^(n-c) fallback. No network or optional dependencies.
Run `python tmr3_t5_separator_glue077_repro.py` for audit,
or `python ... < graph.json` for a graph with {"n":4,"arcs":[[0,3],[1,3],[2,3]]}.
"""
from itertools import combinations, product
import json, random, sys
R = lambda a,b: ((b-a)%5 in (1,3))
W = lambda xs: sum(all(R(x,z) for x in xs) for z in range(5))

def fallback(n,edges):
    # One root per weak component can be fixed to 0 by Z5 rotation.
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append((v,(1,3))); adj[v].append((u,(-1,-3)))
    seen=set(); total=1
    for root in range(n):
        if root in seen: continue
        seen.add(root); queue=[root]; parent={root:-1}; delta={}
        for u in queue:
            for v,d in adj[u]:
                if v not in seen:
                    seen.add(v); parent[v]=u; delta[v]=d; queue.append(v)
        order=queue[1:]; local=[(u,v) for u,v in edges if u in parent and v in parent]
        valid=0
        for bits in product((0,1),repeat=len(order)):
            x={root:0}
            for v,k in zip(order,bits): x[v]=(x[parent[v]]+delta[v][k])%5
            valid+=all(R(x[u],x[v]) for u,v in local)
        total*=5*valid
    return total

def solve(n,arcs):
    if type(n)!=int or n<0: raise ValueError('invalid n')
    edges=set()
    for pair in arcs:
        if not isinstance(pair,(tuple,list)) or len(pair)!=2: raise ValueError('invalid arc')
        u,v=pair
        if type(u)!=int or type(v)!=int or not (0<=u<n and 0<=v<n):
            raise ValueError('invalid arc endpoint')
        edges.add((u,v))
    edges=tuple(sorted(edges))
    if any(u==v or (v,u) in edges for u,v in edges): return 0, 'structural-zero'
    incoming=[set() for _ in range(n)]; outgoing=[set() for _ in range(n)]
    for u,v in edges: incoming[v].add(u); outgoing[u].add(v)
    hubs=tuple(v for v in range(n) if not incoming[v]); H=set(hubs)
    sinks=[v for v in range(n) if incoming[v]]
    if all(not outgoing[v] and len(incoming[v])==3 and incoming[v]<=H for v in sinks):
        triples=[tuple(sorted(incoming[v])) for v in sinks] # retain duplicate triples
        for s in range(2):
            for S in combinations(hubs,s):
                SS=set(S); rest=set(hubs)-SS; parent={v:v for v in rest}
                def find(v):
                    while v!=parent[v]: parent[v]=parent[parent[v]]; v=parent[v]
                    return v
                for e in triples:
                    q=[v for v in e if v not in SS]
                    for v in q[1:]: parent[find(v)]=find(q[0])
                roots={v:find(v) for v in rest}
                groups={}
                for v,r in roots.items(): groups.setdefault(r,[]).append(v)
                blocks=[]; globals=[]
                for e in triples:
                    q=[v for v in e if v not in SS]
                    if not q: globals.append(e)
                    else:
                        r=roots[q[0]]
                        if any(roots[v]!=r for v in q): raise AssertionError('cross-component triple')
                        blocks.append((r,e))
                selected=[]
                for r,B in sorted(groups.items()):
                    E=[e for j,e in blocks if j==r]
                    cover=next((C for k in range(3) for C in combinations(sorted(B),k)
                                if all(len(set(e)&(SS|set(C)))>=2 for e in E)),None)
                    if cover is None: break
                    selected.append((B,E,cover))
                else:
                    count=0
                    for sx in product(range(5),repeat=len(S)):
                        colors=dict(zip(S,sx)); z=1
                        for e in globals: z*=W([colors[v] for v in e])
                        for B,E,C in selected:
                            local=0; free=[v for v in B if v not in C]
                            for cx in product(range(5),repeat=len(C)):
                                colors.update(zip(C,cx)); f=1
                                for e in E:
                                    if all(v in colors for v in e):
                                        f*=W([colors[v] for v in e])
                                for v in free:
                                    vv=0
                                    for a in range(5):
                                        colors[v]=a
                                        q=1
                                        for e in E:
                                            if v in e: q*=W([colors[u] for u in e])
                                        vv+=q
                                    colors.pop(v,None)
                                    f*=vv
                                local+=f
                                for v in C: colors.pop(v,None)
                            z*=local
                        count+=z
                    return count,'separator-gluing'
    return fallback(n,edges),'forest-fallback'

def family(r):
    arcs=[]
    for i in range(r):
        b,c,v=1+3*i,2+3*i,3+3*i
        for j,e in enumerate(((0,b,v),(0,c,v),(b,c,v))):
            sink=1+3*r+3*i+j
            arcs.extend((u,sink) for u in e)
    return 1+6*r,arcs

def test():
    rng=random.Random(202611172021); checks=0
    for n in range(7):
        for _ in range(14):
            arcs=[(u,v) for u in range(n) for v in range(n)
                  if u!=v and rng.random()<.12]
            got,_=solve(n,arcs)
            brute=sum(all(R(x[u],x[v]) for u,v in arcs)
                      for x in product(range(5),repeat=n))
            assert got==brute; checks+=1
    for k in range(3,7):
        for _ in range(12):
            q=rng.randrange(5)
            triples=[tuple(rng.sample(range(k),3)) for i in range(q)]
            arcs=[(v,k+i) for i,e in enumerate(triples) for v in e]
            ref=sum(__import__('functools').reduce(lambda a,b:a*b,
                    (W([x[v] for v in e]) for e in triples),1)
                    for x in product(range(5),repeat=k))
            z,_=solve(k+q,arcs); assert z==ref; checks+=1
    for r in (1,2,3,5,10,40):
        n,arcs=family(r); z,way=solve(n,arcs)
        assert z==5*28**r and way=='separator-gluing'; checks+=1
    return {'checks':checks,'failures':0,'r40':str(solve(*family(40))[0])}

if __name__=='__main__':
    g=json.load(sys.stdin) if not sys.stdin.isatty() and not sys.stdin.closed and sys.stdin.buffer.peek(1) else None
    print(json.dumps({'count':str(solve(g['n'],g['arcs'])[0])} if g else test(),sort_keys=True))
