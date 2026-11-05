#!/usr/bin/env python3
"""Exact one-public-bit projection for two ternary factors per positive 1-in-3 clause.
Exhaustive all subsets of distinct triples at n=4 and n=5; no dependencies or randomness.
"""
import itertools
import json

R={(0,0,0),(0,1,1),(1,0,1)}

def onein3(n,clauses):
    for bits in itertools.product((0,1),repeat=n):
        if all(sum(bits[v] for v in c)==1 for c in clauses):
            return bits
    return None

def projected(n,clauses):
    # Enumerate ACTUAL ternary relation gates, not the one-in-three oracle.
    outputs=set()
    for t in (0,1):
        for bits in itertools.product((0,1),repeat=n):
            if all(any((bits[a],bits[b],s) in R and (s,bits[c],t) in R
                       for s in (0,1)) for a,b,c in clauses):
                outputs.add(t)
                break
    return sorted(outputs)

def valid(n,clauses):
    return all(len(c)==3 and len(set(c))==3 and min(c)>=0 and max(c)<n
               for c in clauses)

counts={}
samples=[]
checks=0
for n in (4,5):
    edges=list(itertools.combinations(range(n),3))
    count={'only0':0,'with1':0}
    for mask in range(1<<len(edges)):
        clauses=[c for j,c in enumerate(edges) if mask>>j&1]
        assert valid(n,clauses);checks+=1
        out=projected(n,clauses)
        witness=onein3(n,clauses)
        assert out==([0,1] if witness is not None else [0]);checks+=1
        assert 0 in out;checks+=1
        count['with1' if 1 in out else 'only0']+=1
        if n==4 and mask in (0,1,15):
            samples.append({'n':n,'mask':mask,'clauses':clauses,
                            'projection':out,'t1_witness':witness})
    counts[n]=count
quad=list(itertools.combinations(range(4),3))
assert projected(4,quad)==[0];checks+=1
assert projected(4,[quad[0]])==[0,1];checks+=1
assert 1 in projected(4,[quad[0]]);checks+=1
assert projected(4,[quad[0]])!=[0];checks+=1
for n,clauses in [(4,[(0,0,1)]),(4,[(0,1,4)]),(4,[(0,1)]),(0,[(0,1,2)])]:
    try: good=valid(n,clauses)
    except (ValueError,TypeError): good=False
    assert not good;checks+=1
assert counts[4]=={'only0':1,'with1':15}
assert counts[5]=={'only0':548,'with1':476}
print(json.dumps({'format':'LSPV1-422-producer','counts':counts,
                  'samples':samples,'assertions':checks},sort_keys=True))
