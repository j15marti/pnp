#!/usr/bin/env python3
"""ARC213: Exhaustive signed 3-clause to 2SAT plus disjoint XOR3 verification.
No external SAT oracle; no random seed; source and output bytes both counted.
"""
from itertools import product
import json

def lit(l,x):
    return x[abs(l)-1] if l>0 else not x[abs(l)-1]
def satclause(c,x):
    return any(lit(l,x) for l in c)
def gadget(c,x,y):
    return all(lit(c[i],x) or y[i] for i in range(3)) and sum(y)%2==0
def ext(c,x):
    return [y for y in product((0,1),repeat=3) if gadget(c,x,y)]
def sat(F):
    return any(all(satclause(c,x) for c in F)
               for x in product((0,1),repeat=3))

clauses=[tuple((i+1)*s[i] for i in range(3))
         for s in product((-1,1),repeat=3)]
count=dict(local_truth_rows=0,subset_checks=0,original_assignments=0,
           full_aux_checks=0,nonempty_aux_witnesses=0)
for c in clauses:
    for x in product((0,1),repeat=3):
        witnesses=ext(c,x)
        assert bool(witnesses)==satclause(c,x)
        count['nonempty_aux_witnesses']+=len(witnesses)
        for y in product((0,1),repeat=3):
            assert gadget(c,x,y)==(y in witnesses)
            count['local_truth_rows']+=1

falsepositive=0
for mask in range(256):
    F=[c for i,c in enumerate(clauses) if mask&(1<<i)]
    projection=False
    for x in product((0,1),repeat=3):
        assert all(bool(ext(c,x)) for c in F)==all(satclause(c,x) for c in F)
        projection|=all(bool(ext(c,x)) for c in F)
        count['original_assignments']+=1
    assert projection==sat(F)
    if F and not sat(F):
        falsepositive+=1  # binary-only SAT (y=1), XOR-only SAT (y=0)
    count['subset_checks']+=1
assert falsepositive==1
assert not sat(clauses)
for i in range(8):
    assert sat(clauses[:i]+clauses[i+1:])

for F in [clauses[:1],clauses[:2],clauses[:3],clauses[4:7]]:
    for x in product((0,1),repeat=3):
        projected=False
        for ys in product((0,1),repeat=3*len(F)):
            projected|=all(gadget(c,x,ys[3*i:3*i+3])
                           for i,c in enumerate(F))
            count['full_aux_checks']+=1
        assert projected==all(satclause(c,x) for c in F)

pivot={}
for t in range(1,5):
    pivot[t]=0
    for zbits in product((0,1),repeat=4*t):
        A=[zbits[2*i] or zbits[2*i+1] for i in range(t)]
        B=[zbits[2*t+2*i] or zbits[2*t+2*i+1] for i in range(t)]
        direct=any(all(z or a for a in A) and
                   all((not z) or b for b in B) for z in (0,1))
        assert direct==all(a or b for a in A for b in B)==(all(A) or all(B))
        pivot[t]+=1
assert sum(pivot.values())==69904

F=clauses
source='p cnf 3 8\n'+''.join(' '.join(map(str,c))+' 0\n' for c in F)
aux=4
out='p mixed 27 24 8\n'
for c in F:
    for i in range(3):
        out+=f'c {c[i]} {aux+i} 0\n'
    out+=f'x {aux} {aux+1} {aux+2} = 0\n'
    aux+=3
assert (len(source),len(out))==(86,352)
assert count==dict(local_truth_rows=512,subset_checks=256,
                   original_assignments=2048,full_aux_checks=8768,
                   nonempty_aux_witnesses=104)
result={'status':'PASS','counts':count,'pivot_checks':pivot,
        'pivot_total':69904,'independent_relaxations_false_positive':falsepositive,
        'unsat_8_clauses':True,'drop_any_one_is_sat':True,
        'binary_only_sat':True,'xor_only_sat':True,'joint_mixed_unsat':True,
        'source_bytes':len(source),'mixed_bytes':len(out),
        'limitations':['COMPUTATIONAL only; mathematical theorem has separate proof',
                       'Python counts are not TM steps',
                       'No unrestricted SAT lower bound or compressor']}
print(json.dumps(result,sort_keys=True,indent=2))
