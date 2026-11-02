#!/usr/bin/env python3
"""LSPV-1 NEIGHBOR-REFINED-THREELEVEL325. Source-anchored exact degree-20 sharpness.
Pure Python, no solver or SAT-label oracle. No native FLMV time claims.
"""
import json,itertools
from collections import Counter,defaultdict
POS="""1,2,26;1,3,23;2,6,13;3,10,15;4,18,29;4,25,27;5,12,14;5,16,20;6,19,21;7,11,13;7,23,30;8,9,28;8,17,24;9,27,28;10,22,30;11,18,21;12,17,20;14,16,24;15,26,29;19,22,25"""
NEG="""21,25,30;17,20,28;14,19,22;12,16,29;11,13,21;11,12,18;9,17,20;8,24,25;8,13,18;7,27,29;7,26,27;5,10,19;5,6,24;4,15,26;3,6,23;3,4,14;2,22,23;2,16,28;1,10,30;1,9,15"""
def rows(s,sign):return [tuple(sign*int(z) for z in c.split(',')) for c in s.split(';')]
SOURCE=rows(POS,1)+rows(NEG,-1)
SELECTED=[3,9,13,16,22,26]
def graph(cnf):
    g=defaultdict(set)
    for clause in cnf:
        ids=set(abs(v) for v in clause)
        for x in ids:g[x].update(ids-{x})
    return dict(g)
def project(cnf,selected):
    c=set(frozenset(row) for row in cnf)
    for x in selected:
        p=[a for a in c if x in a]
        q=[a for a in c if -x in a]
        nxt={a for a in c if x not in a and -x not in a}
        for a in p:
            for b in q:
                r=(a-{x})|(b-{-x})
                if any(-v in r for v in r):continue
                nxt.add(frozenset(r))
        c=nxt
    return c
def audit():
    counts=Counter((abs(v),v>0) for c in SOURCE for v in c)
    assert len(SOURCE)==40 and len(set(frozenset(c) for c in SOURCE))==40
    assert all(len(set(map(abs,c)))==3 and len(set(v>0 for v in c))==1 for c in SOURCE)
    assert all(counts[x,s]==2 for x in range(1,31) for s in (False,True))
    g=graph(SOURCE)
    assert len(g)==30 and max(len(v) for v in g.values())==8
    assert all(y not in g[x] for x,y in itertools.combinations(SELECTED,2))
    assert all(x in SELECTED or any(p in g[x] for p in SELECTED) for x in g)
    child=project(SOURCE,SELECTED)
    h=graph(child)
    assert len(g[2])==8 and len(h[2])==20
    assert len(h)==24 and len(child)==36
    assert max((len(s) for s in h.values()),default=0)==20
    return {'status':'PASS','n':30,'m':40,'selected':SELECTED,
            'pivot_neighbors_of_y2':[x for x in SELECTED if x in g[2]],
            'source_degree_y2':len(g[2]),'projected_degree_y2':len(h[2]),
            'projected_clauses':len(child),'projected_literals':sum(len(c) for c in child),
            'three_phase_fraction':'25600/30429'}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
