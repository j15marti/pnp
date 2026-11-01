#!/usr/bin/env python3
"""Independent self-contained port-gadget exhaustive census, stdlib only."""
import collections
import itertools
import json

A=range(6)
PORTS=(6,7,8)
TRIPLES=tuple(itertools.combinations(A,3))
EDGES=tuple(itertools.combinations(A,2))
FULL=(1<<64)-1

def mask(clause,positive=True):
    return sum(1<<a for a in range(64)
        if (any((a>>v)&1 for v in clause) if positive
            else any(not ((a>>v)&1) for v in clause)))

PM={t:mask(t) for t in TRIPLES}
NM={t:mask(t,False) for t in TRIPLES}
EM={t:mask(t) for t in EDGES}
SM={(i,):mask((i,)) for i in A}
NF=[r for r in itertools.combinations(TRIPLES,4)
    if all(sum(i in t for t in r)==2 for i in A)]
assert len(NF)==75
NEG=[]
for r in NF:
    m=FULL
    for t in r:
        m&=NM[t]
    NEG.append(m)

def positive():
    for r in NF:
        yield "3",(PORTS,)+r
    for single in PORTS:
        pair=tuple(p for p in PORTS if p!=single)
        for a in A:
            for e in EDGES:
                d=collections.Counter((a,)+e)
                for inner in itertools.combinations(TRIPLES,3):
                    if all(d[i]+sum(i in t for t in inner)==2 for i in A):
                        yield "21",((pair[0],pair[1],a),(single,*e))+inner
    for edges in itertools.product(EDGES,repeat=3):
        d=collections.Counter(i for e in edges for i in e)
        if any(d[i]>2 for i in A):continue
        for t,s in itertools.combinations(TRIPLES,2):
            if all(d[i]+(i in t)+(i in s)==2 for i in A):
                yield "111",tuple((PORTS[j],*e)
                    for j,e in enumerate(edges))+(t,s)

counts=collections.Counter()
hist=collections.defaultdict(collections.Counter)
for typ,rows in positive():
    states=[]
    for b in range(8):
        active=FULL
        for c in rows:
            if any(v>=6 and (b>>(v-6))&1 for v in c):continue
            fresh=tuple(v for v in c if v<6)
            active &= ({1:SM,2:EM,3:PM}[len(fresh)][fresh]
                       if fresh else 0)
        states.append(active)
    for neg in NEG:
        signature="".join("1" if (state&neg) else "0" for state in states)
        assert signature==("01111111" if typ=="3" else "11111111")
        counts[typ]+=1
        hist[typ][signature]+=1
assert dict(counts)=={"3":5625,"21":243000,"111":411750}
print(json.dumps({"counts":dict(counts),"projections":
      {k:dict(v) for k,v in hist.items()},"total":sum(counts.values()),
      "P_vs_NP":"OPEN"},indent=2,sort_keys=True))
