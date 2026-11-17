#!/usr/bin/env python3
"""TMR-3/070: exact T5 count via canonical directed independent twin classes.
UTF-8 whitespace format: n m then exactly m pairs of integer endpoints.
Prototype caps protect finite tests, not part of mathematical bound.
"""
from itertools import product
from collections import Counter
import hashlib
import json
import random
import sys

D = {1, 3}
MASKS = tuple(m for m in range(1, 32) if m.bit_count() <= 2)
COLORS = {m: tuple(a for a in range(5) if m & (1 << a)) for m in MASKS}
COMPAT = {(a, b): all((y-x) % 5 in D for x in COLORS[a] for y in COLORS[b]) for a in MASKS for b in MASKS}


def parse_source(s):
    ts = s.split()
    if len(ts) < 2 or any(not x.isascii() or not x.isdecimal() for x in ts):
        raise ValueError('invalid token')
    n, m = map(int, ts[:2])
    if n > 100000 or m > 1000000 or len(ts) != 2 + 2*m:
        raise ValueError('invalid length')
    arcs = []
    for j in range(m):
        a,b=map(int,ts[2+2*j:4+2*j])
        if a >= n or b >= n: raise ValueError('endpoint out of range')
        arcs.append((a,b))
    return n, arcs


def normalize(n, arcs):
    if n < 0 or any(a < 0 or b < 0 or a >= n or b >= n for a,b in arcs):
        raise ValueError('endpoint out of range')
    E=set(arcs)
    if any(a == b or (b,a) in E for a,b in E):
        return None
    return E


def count_quotient(n, arcs, metadata=False):
    E=normalize(n, arcs)
    if E is None: return (0, {'reason':'loop_or_antiparallel'}) if metadata else 0
    outs=[set() for _ in range(n)]
    ins=[set() for _ in range(n)]
    for a,b in E:
        outs[a].add(b); ins[b].add(a)
    d={}
    for v in range(n):
        d.setdefault((tuple(sorted(outs[v])),tuple(sorted(ins[v]))),[]).append(v)
    groups=sorted((tuple(g) for g in d.values()),key=lambda g:g[0])
    isolated=sum(len(g) for g in groups if len(outs[g[0]])+len(ins[g[0]]) == 0)
    groups=[g for g in groups if len(outs[g[0]])+len(ins[g[0]]) > 0]
    q=len(groups)
    group_of={v:i for i,g in enumerate(groups) for v in g}
    qedges={(group_of[a],group_of[b]) for a,b in E}
    assert all(i != j for i,j in qedges)
    # Genuine complete bipartite source quotient, verified during testing.
    assert all((a,b) in E for i,j in qedges for a in groups[i] for b in groups[j])
    prior=[[] for _ in range(q)]
    for i,j in qedges:
        if i>j: prior[i].append((j, False)) # i -> j, comparator COMPAT[current, previous]
        else: prior[j].append((i, True))  # i -> j, comparator COMPAT[previous, current]
    states=[None]*q
    attempts=0
    visited=0
    def solve(i, weight):
        nonlocal attempts, visited
        visited+=1
        if i==q: return weight
        total=0
        for m in MASKS:
            attempts+=1
            k=m.bit_count()
            w=1 if k==1 else (1 << len(groups[i])) - 2
            if w==0: continue
            if all((COMPAT[states[j],m] if before else COMPAT[m,states[j]]) for j,before in prior[i]):
                states[i]=m
                total+=solve(i+1,weight*w)
        states[i]=None
        return total
    count=5**isolated * solve(0,1)
    meta={'n':n,'m':len(E),'q':q,'isolated_vertices':isolated,'group_sizes':[len(g) for g in groups], 'states_visited':visited,'mask_attempts':attempts}
    return (count,meta) if metadata else count


def brute(n, arcs):
    E=normalize(n,arcs)
    if E is None: return 0
    return sum(all((x[v]-x[u])%5 in D for u,v in E) for x in product(range(5), repeat=n))


def kbip(a,b):
    return a+b,[(i,a+j) for i in range(a) for j in range(b)]


def run():
    random.seed(202611171424)
    total=0
    stats=Counter()
    for n in range(0,5):
        # All choices of each ordered pair: no arc, forward, backward.
        pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
        for z in product((0,1,2),repeat=len(pairs)):
            arcs=[(u,v) if t==1 else (v,u) for (u,v),t in zip(pairs,z) if t]
            expected=brute(n,arcs)
            actual=count_quotient(n,arcs)
            assert actual==expected,(n,arcs,actual,expected)
            stats['exhaustive_orientations']+=1;total+=1
    for n in range(0,7):
        for _ in range(40):
            arcs=[]
            for u in range(n):
                for v in range(n):
                    if random.random() < .22: arcs.append((u,v))
            if arcs and random.random()<.3: arcs.append(random.choice(arcs))
            actual=count_quotient(n,arcs)
            expected=brute(n,arcs)
            assert actual==expected,(n,arcs,actual,expected)
            stats['random_digraphs']+=1;total+=1
    for a in range(1,7):
        for b in range(1,7):
            n,arcs=kbip(a,b)
            actual=count_quotient(n,arcs)
            expected=5*((1<<a)+(1<<b)-2)
            assert actual==expected,(a,b,actual,expected)
            assert count_quotient(n,[(v,u) for u,v in arcs])==expected
            stats['bipartite_reversal_cases']+=1;total+=1
    for a,b in ((120,120),(3,120),(50,90),(1,100)):
        n,arcs=kbip(a,b)
        actual,meta=count_quotient(n,arcs,True)
        assert actual==5*((1<<a)+(1<<b)-2)
        assert meta['q']==2
        stats['large_dense_blowups']+=1;total+=1
    bad=['-1 0','2 1 0','1 1 0 1','2 1 a 1','3 2 0 1 2','2 0 xx','0 1 0 0']
    for s in bad:
        try: parse_source(s);assert False,s
        except ValueError: pass
        stats['bad_sources']+=1;total+=1
    n,arcs=parse_source('3 2 0 1 0 2')
    assert count_quotient(n,arcs)==brute(n,arcs)
    stats['valid_sources']+=1;total+=1
    assert len(MASKS)==15
    assert all(not COMPAT[a,b] for a in MASKS for b in MASKS if a.bit_count()==b.bit_count()==2)
    stats['compatibility_checks']=2;total+=2
    result={'revision':'tmr3-t5-directed-twins-070-v1','seed':202611171424,'cases':total,'breakdown':dict(sorted(stats.items())),'errors':0,'sample_K_120_120':str(5*((1<<120)+(1<<120)-2)),'example_K_3_120':str(5*((1<<3)+(1<<120)-2)),'max_q_large':2}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':run()
