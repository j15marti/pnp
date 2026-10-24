#!/usr/bin/env python3
"""Peer mini: independent SAT/factor enumeration, degree-two signed cardinality CSP.
Finite verification only. ARC-EDGE-90 and P versus NP remain OPEN.
"""
from itertools import combinations, product
from collections import defaultdict

def sat(n,cs):
    return any(all(lo<=sum((a[v] if s==1 else 1-a[v]) for v,s in lits)<=hi
                   for lits,lo,hi in cs) for a in product((0,1),repeat=n))

def factor(n,cs):
    occ=defaultdict(list); bounds={('C',j):(lo,hi) for j,(_,lo,hi) in enumerate(cs)}
    for j,(lits,_,_) in enumerate(cs):
        assert len(lits)==len({v for v,_ in lits})
        for v,s in lits:occ[v].append((j,s))
    edges=[]
    for v in range(n):
        x=occ[v]; assert len(x)<=2
        if len(x)==1:
            a,_=x[0];bounds[('L',v)]=(0,1);edges.append((('C',a),('L',v)))
        elif len(x)==2:
            (a,sa),(b,sb)=x; assert a!=b
            if sa==sb:edges.append((('C',a),('C',b)))
            else:
                bounds[('Q',v)]=(1,1)
                edges += [(('C',a),('Q',v)),(('C',b),('Q',v))]
    for picked in product((0,1),repeat=len(edges)):
        d={p:0 for p in bounds}
        for bit,(a,b) in zip(picked,edges):
            if bit:d[a]+=1;d[b]+=1
        if all(lo<=d[p]<=hi for p,(lo,hi) in bounds.items()):return True
    return False

checks=0
pairs=list(combinations(range(4),2))
inc=[[i for i,p in enumerate(pairs) if j in p] for j in range(4)]
for target in (1,2):
    good=[([(v,1) for v in inc[j]],target,target) for j in range(4)]
    bad=[(list(lits),lo,hi) for lits,lo,hi in good]
    v,_=bad[1][0][0];bad[1][0][0]=(v,-1)
    assert sat(6,good) and factor(6,good);checks+=2
    assert not sat(6,bad) and not factor(6,bad);checks+=2
for signs in product((-1,1),repeat=6):
    for a in range(4):
        for b in range(4):
            cs=[([(v,signs[v]) for v in range(3)],a,a),
                ([(v,signs[v+3]) for v in range(3)],b,b)]
            assert sat(3,cs)==factor(3,cs);checks+=1
print({'status':'COMPUTATIONAL PASS; ARC-EDGE-90 OPEN', 'cases':1032,'assertions':checks})
