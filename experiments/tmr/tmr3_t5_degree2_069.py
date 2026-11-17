#!/usr/bin/env python3
"""TMR-3/069: exact five-symbol CSP count by charged degree<=2 elimination.
Canonical test source: line 'n m' followed by precisely m ordered arcs (u,v).
No third-party packages; finite audit is computational, theorem is symbolic.
"""
from itertools import product
from collections import deque
import json, random, hashlib
from pathlib import Path

D = (1, 3)
REV = tuple((-i) % 5 for i in range(5))


def parse(text):
    tokens = text.split()
    if len(tokens) < 2 or any(not t.isascii() or not t.isdecimal() for t in tokens):
        raise ValueError('bad source token')
    n, m = map(int, tokens[:2])
    if n > 100000 or m > 1000000 or len(tokens) != 2 + 2*m:
        raise ValueError('bad source length')
    edges = []
    for j in range(m):
        u, v = map(int, tokens[2+2*j:4+2*j])
        if u >= n or v >= n:
            raise ValueError('bad source vertex')
        edges.append((u,v))
    return n, edges


def normalize(n, arcs):
    if n < 0 or any(u < 0 or v < 0 or u >= n or v >= n for u,v in arcs):
        raise ValueError('bad graph')
    edges = set(arcs)
    if any(u == v or (v,u) in edges for u,v in edges):
        return None
    return sorted(edges)


def mat_oriented(edges, a, b):
    k = (min(a,b), max(a,b))
    p = edges[k]
    return p if a < b else tuple(p[(-d)%5] for d in range(5))


def count_t5(n, arcs, order='min'):
    arcs = normalize(n, arcs)
    if arcs is None: return 0, dict(reason='loop_or_antiparallel')
    factors = {}
    for u,v in arcs:
        p = tuple(int((d if u < v else -d) % 5 in D) for d in range(5))
        factors[min(u,v), max(u,v)] = p
    active = set(range(n))
    scalar = 1
    elims = [0,0,0]
    max_bits = 1
    # All factors have form W_ab(x_b-x_a). Elimination preserves this form.
    while True:
        nbr = {v:set() for v in active}
        for a,b in factors:
            nbr[a].add(b); nbr[b].add(a)
        opts = [v for v in active if len(nbr[v]) <= 2]
        if not opts: break
        low = min(len(nbr[v]) for v in opts)
        opts = [v for v in opts if len(nbr[v]) == low]
        v = (min if order=='min' else max)(opts)
        ns = sorted(nbr[v]); degree=len(ns)
        elims[degree] += 1
        if degree == 0:
            scalar *= 5
        elif degree == 1:
            u=ns[0]
            scalar *= sum(mat_oriented(factors,u,v))
            del factors[min(u,v),max(u,v)]
        else:
            a,b=ns
            f=mat_oriented(factors,a,v)
            g=mat_oriented(factors,v,b)
            h=tuple(sum(f[s]*g[(d-s)%5] for s in range(5)) for d in range(5))
            del factors[min(a,v),max(a,v)]
            del factors[min(b,v),max(b,v)]
            key=(a,b)
            if key in factors:
                h=tuple(x*y for x,y in zip(h,factors[key]))
            factors[key]=h
            max_bits=max(max_bits,*(w.bit_length() for w in h))
        active.remove(v)
        max_bits=max(max_bits,scalar.bit_length())
        if not scalar:
            return 0, dict(eliminations=elims, residual=len(active), max_bits=max_bits)
    vertices=sorted(active)
    components=[]
    todo=set(active)
    while todo:
        root=min(todo); todo.remove(root)
        stack=[root]; cc=[root]
        while stack:
            a=stack.pop()
            for u,v in factors:
                z=v if u==a else (u if v==a else None)
                if z in todo:
                    todo.remove(z);stack.append(z);cc.append(z)
        components.append(sorted(cc))
    anchors={cc[0] for cc in components}
    free=[v for v in vertices if v not in anchors]
    reduced_sum=0
    for values in product(range(5),repeat=len(free)):
        color={v:0 for v in anchors}
        color.update(zip(free,values))
        term=1
        for (a,b),w in factors.items():
            term*=w[(color[b]-color[a])%5]
            if term==0:break
        reduced_sum+=term
    answer=scalar*5**len(components)*reduced_sum
    return answer, dict(eliminations=elims, residual=len(vertices), residual_edges=len(factors),
                        anchors=len(components), enumerated=5**len(free),
                        max_bits=max(max_bits,answer.bit_length()),scalar=scalar)


def brute(n,arcs):
    norm=normalize(n,arcs)
    if norm is None:return 0
    count=0
    for coloring in product(range(5),repeat=n):
        if all((coloring[v]-coloring[u])%5 in D for u,v in norm):count+=1
    return count


def k2k(k):
    return k+2, [(0,i) for i in range(2,k+2)]+[(1,i) for i in range(2,k+2)]


def audit(seed=202611171324):
    rng=random.Random(seed)
    tests=0; maxbits=0; maxres=0
    for n in range(0,8):
        for j in range(28 if n<=5 else 15):
            arcs=[]
            for u in range(n):
                for v in range(u+1,n):
                    t=rng.randrange(6)
                    if t==0:arcs.append((u,v))
                    elif t==1:arcs.append((v,u))
                    elif t==2:arcs.extend(((u,v),(v,u)))
                    elif t==3:arcs.extend(((u,v),(u,v)))
            if n and j%11==0:arcs.append((0,0))
            b=brute(n,arcs)
            c,stat=count_t5(n,arcs,order='min')
            d,_=count_t5(n,arcs,order='max')
            rev=[(v,u) for u,v in arcs]
            e,_=count_t5(n,rev,order='max')
            assert c==b==d==e,(n,arcs,b,c,d,e)
            tests+=1;maxbits=max(maxbits,stat.get('max_bits',0)); maxres=max(maxres,stat.get('residual',0))
    special={}
    known=[('directed_triangle',3,[(0,1),(1,2),(2,0)],15),
           ('transitive_triangle',3,[(0,1),(1,2),(0,2)],5),
           ('directed_5cycle',5,[(i,(i+1)%5) for i in range(5)],10),
           ('empty',0,[],1), ('isolated_4',4,[],625),
           ('opposite',2,[(0,1),(1,0)],0),('loop',1,[(0,0)],0)]
    for name,n,es,exp in known:
        got,_=count_t5(n,es)
        assert got==exp,(name,got,exp)
        special[name]=got;tests+=1
    for k in list(range(1,18))+[30,50,80,120]:
        n,es=k2k(k)
        got,stat=count_t5(n,es)
        expected=5*2**k+10
        assert got==expected,(k,got,expected)
        special[f'K2_{k}']={'count':got,'eliminations':stat['eliminations'],
                           'residual':stat['residual'],'prior_forest_exponent':n-1,'cycle_rank':k-1}
        tests+=1
    malformed=['','1','2 a','2 1 0','2 1 0 2','2 1 0 1 garbage','-1 0','1 0 0 0']
    for s in malformed:
        try:parse(s);raise AssertionError('invalid input accepted')
        except ValueError:pass
        tests+=1
    src='3 3\n0 1\n1 2\n2 0\n'
    n,es=parse(src)
    assert count_t5(n,es)[0]==15;tests+=1
    return dict(revision='tmr3-t5-degree2-069-v1',seed=seed,random_graphs=tests-(len(known)+21+len(malformed)+1),
                assertions=tests,failures=0,max_intermediate_bits=maxbits,
                max_random_residual=maxres,special=special)

if __name__=='__main__':
    result=audit()
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
