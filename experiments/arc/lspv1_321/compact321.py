#!/usr/bin/env python3
"""LSPV-1 SOURCE-DISJOINT-BATCH-PROJECTION321: compact self-contained producer.
All source-variable IDs and clause provenance remain explicit.
No third-party SAT solver; exhaustive truth tables for n <= 15.
"""
from itertools import product
from collections import Counter
import json
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),
    (-2,-3,-5),(-4,-5,-6))
F15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
     (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
     (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
     (-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
     (-9,-10,-14),(-10,-7,-15))
H15=F9+tuple(tuple((abs(v)+9)*(1 if v>0 else -1) for v in c) for c in Y6)

def grammar(F,n):
    q=Counter(v for c in F for v in c)
    return (3*len(F)==4*n and len(set(tuple(sorted(c)) for c in F))==len(F)
        and all(len(c)==3 and len(set(map(abs,c)))==3
                and (all(v>0 for v in c) or all(v<0 for v in c))
                and all(1<=abs(v)<=n for v in c) for c in F)
        and all(q[v]==q[-v]==2 for v in range(1,n+1)))

def norm(c):
    s=set(c)
    return None if any(-v in s for v in s) else tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def truth(F,word):
    return all(any(bool(word & (1<<(abs(v)-1))) == (v>0) for v in c) for c in F)

def batch(F,n):
    assert grammar(F,n)
    adj={x:set() for x in range(1,n+1)}
    for c in F:
        v=set(map(abs,c))
        for x in v:adj[x].update(v-{x})
    assert max(len(t) for t in adj.values())<=8
    remain=set(adj);I=[]
    while remain:
        x=min(remain);I.append(x);remain.difference_update({x}|adj[x])
    assert len(I)>= (n+8)//9
    live=[(norm(c),('source',j)) for j,c in enumerate(F)
          if not any(abs(v) in I for v in c)]
    taut=0
    for x in I:
        pos=[(j,c) for j,c in enumerate(F) if x in c]
        neg=[(j,c) for j,c in enumerate(F) if -x in c]
        assert len(pos)==len(neg)==2
        for a,A in pos:
            for b,B in neg:
                C=norm(tuple(v for v in A if v!=x)+tuple(v for v in B if v!=-x))
                if C is None:taut+=1
                else:live.append((C,('resolve',x,a,b)))
    dedup={}
    for c,proof in live:dedup.setdefault(c,proof)
    assert len(dedup)<=len(F)
    assert sum(len(c) for c in dedup)<=3*len(F)+4*len(I)
    return I,list(dedup),dedup,taut

def run(name,F,n):
    I,out,proof,taut=batch(F,n)
    rest=[x for x in range(1,n+1) if x not in I]
    good=0
    for z in product((0,1),repeat=len(rest)):
        base=sum(v<<(x-1) for x,v in zip(rest,z))
        actual=any(truth(F,base|sum(v<<(x-1) for x,v in zip(I,b)))
                   for b in product((0,1),repeat=len(I)))
        got=truth(out,base)
        assert actual==got
        good+=got
    return dict(source=name,n=n,m=len(F),source_models=sum(truth(F,x) for x in range(1<<n)),
                independent_pivots=I,projected_models=good,output_clauses=len(out),
                output_literal_records=sum(len(c) for c in out),
                resolution_candidates=4*len(I),tautology_candidates=taut,
                source_private_gates=3*len(F)-1,
                projected_source_private_gates=sum(len(c) for c in out)-1,
                row_count=1<<len(rest))
if __name__=='__main__':
    sources=[('Y6',Y6,6),('F9',F9,9),('F15',F15,15),('H15',H15,15)]
    print(json.dumps([run(*record) for record in sources],indent=2))
