#!/usr/bin/env python3
"""TMR-3/087 compact source-derived chromatic obstruction recognizer.
Standalone: python3 tmr3_t5_chromatic_core087_repo.py
Claims only ZERO for authenticated canonical Mycielski sources s>=3.
All other inputs return None, NOT SAT.
"""
from itertools import combinations
import json
import random

def myc(s):
    n=5
    edges={(min(i,(i+1)%5),max(i,(i+1)%5)) for i in range(5)}
    for _ in range(s):
        old=list(edges)
        extra=set()
        for u,v in old:
            extra.add((min(u,n+v),max(u,n+v)))
            extra.add((min(v,n+u),max(v,n+u)))
        extra.update((n+i,2*n) for i in range(n))
        edges |= extra
        n=2*n+1
    return n,edges

def authenticate(n,arcs):
    if type(n) is not int or n<5 or (n+1)%6:
        return None
    q=(n+1)//6
    if not q or q&(q-1):
        return None
    s=q.bit_length()-1
    expected_n,expected_edges=myc(s)
    if n!=expected_n or len(arcs)!=len(expected_edges):
        return None
    seen=set()
    for u,v in arcs:
        if type(u) is not int or type(v) is not int or not 0<=u<n or not 0<=v<n or u==v:
            return None
        pair=(min(u,v),max(u,v))
        if pair in seen:
            return None
        seen.add(pair)
    return s if seen==expected_edges else None

def exact_zero_certificate(n,arcs):
    s=authenticate(n,arcs)
    if s is None or s<3:
        return None
    return {'exact_count':0,'unsat':True,'chi':s+3,'source_authenticated':True}

def run():
    tests=0
    summary=[]
    for s in range(8):
        n,edges=myc(s)
        assert n==6*2**s-1
        assert len(edges)==(21*3**s-12*2**s+1)//2
        tests+=2
        deg=[0]*n
        adj=[set() for _ in range(n)]
        for u,v in edges:
            deg[u]+=1;deg[v]+=1
            adj[u].add(v);adj[v].add(u)
        assert min(deg)==s+2
        assert all(not (adj[u]&adj[v]) for u,v in edges)
        tests+=2
        rng=random.Random(87000+s)
        arcs=[(u,v) if rng.randrange(2) else (v,u) for u,v in sorted(edges)]
        assert authenticate(n,arcs)==s
        assert (exact_zero_certificate(n,arcs) is not None)==(s>=3)
        tests+=2
        reversed_arc=arcs.copy()
        reversed_arc[0]=tuple(reversed(reversed_arc[0]))
        assert authenticate(n,reversed_arc)==s
        assert authenticate(n,arcs+[(0,0)]) is None
        duplicated=arcs.copy();duplicated[0]=duplicated[1]
        assert authenticate(n,duplicated) is None
        tests+=3
        summary.append({'s':s,'n':n,'m':len(edges),'chi':s+3,
                        'min_degree':min(deg),'cycle_rank':len(edges)-n+1,
                        'exact_zero_certified':s>=3})
    n,edges=myc(3)
    assert n==47
    adj=[set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v);adj[v].add(u)
    for a,b,c in combinations(range(n),3):
        assert not (b in adj[a] and c in adj[b] and a in adj[c])
        tests+=1
    return {'experiment':'TMR3_087_COMPACT','checks':tests,'failures':0,
            'family':summary,'qualification':'CONSTRUCTIVE; NO P-vs-NP lower bound'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
