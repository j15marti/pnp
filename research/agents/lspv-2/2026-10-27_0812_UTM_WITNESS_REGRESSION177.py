#!/usr/bin/env python3
"""Independent W1 4-mode/prefix-gap-source witness checks for LSPV2 177.
Exhaustive 4*2^15 assignments, deterministic, no external SAT solver.
The explicit source-only witness is not an accepting SAT decider.
"""
import json, itertools
from collections import Counter
from pathlib import Path
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
A=((6,0),(11,0));B=((17,2),(9,2))


def gadget(a,b):
    clauses=[list(x) for x in W1]
    if a==0:
        for i,j in A:clauses[i][j]*=-1
    if b==0:
        for i,j in B:clauses[i][j]*=-1
    return [tuple(c) for c in clauses]

def good(C,mask):
    return all(any((((mask>>(abs(t)-1))&1)==1)==(t>0) for t in row) for row in C)

def audit(m):
    w=(20*m).bit_length()
    AA=sorted(set(j for j,_ in A));BB=sorted(set(j for j,_ in B))
    FIX=sorted(set(range(20))-set(AA)-set(BB))
    N=32+3*w+60*m*(w+1)
    G=16*m*3*(w+1)
    seen=Counter();mixed=0
    for a in itertools.product((0,1),repeat=m):
        for b in itertools.product((0,1),repeat=m):
            cs=[gadget(a[i],b[i]) for i in range(m)]
            full=[]
            for indices in (AA,FIX,BB):
                for i in range(m):
                    for c in indices:
                        full.append(tuple((abs(z)+15*i)*(1 if z>0 else -1) for z in cs[i][c]))
            assert len(full)==20*m
            pos=Counter();neg=Counter()
            for row in full:
                assert len(row)==3 and len({abs(t) for t in row})==3
                for t in row:(pos if t>0 else neg)[abs(t)]+=1
            assert all(pos[t]==neg[t]==2 for t in range(1,15*m+1))
            source_sat=all(not(a[i] and b[i]) for i in range(m))
            witness=[616 if bit==0 else 4742 for bit in a]
            def sat_word():
                for row in full:
                    if not any((bool((witness[(abs(t)-1)//15]>>((abs(t)-1)%15))&1))==(t>0) for t in row):return False
                return True
            yes=sat_word()
            assert yes==source_sat,('source printer faulty',m,a,b)
            seen['yes' if source_sat else 'no']+=1
            if any(len({x>0 for x in row})>1 for row in full):mixed+=1
    return {'m':m,'N':N,'G_bits':G,'V':15*m,'M':20*m,'width':w,'count':sum(seen.values()),
            'models_by_promise':dict(seen),'mixed_sign_instances':mixed}


def run():
    counts={};examples={}
    for a,b in itertools.product((0,1),repeat=2):
        C=gadget(a,b)
        assert len(set(C))==20
        positive=Counter();negative=Counter()
        for row in C:
            assert len(set(map(abs,row)))==3
            for v in row:(positive if v>0 else negative)[abs(v)]+=1
        assert all(positive[t]==negative[t]==2 for t in range(1,16))
        n=sum(good(C,mask) for mask in range(1<<15))
        counts[f'{a}{b}']=n
        examples[f'{a}{b}']={'616':good(C,616),'4742':good(C,4742)}
    assert counts=={'00':772,'01':272,'10':272,'11':0}
    assert examples['00']['616'] and examples['01']['616'] and examples['10']['4742']
    assert not examples['11']['616'] and not examples['11']['4742']
    by_m=[audit(m) for m in range(1,5)]
    return {'run':'UTM_WITNESS_REGRESSION177','four_modes':counts,'witness_ints':examples,
            'physical_source_controls':by_m,'total_tested_modes':131072,
            'caveat':'Alice-only witness generation is not a sound acceptance or UNSAT proof. All formulas are proper signed exact22, not clause monotone.',
            'exact_gap_form':'G=48*m*(w+1), w=bitlength(20m); physical encoding LENGTH N=32+3w+60m(w+1).',
            'P_vs_NP':'OPEN'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='utm_witness177.json');args=ap.parse_args()
    out=run();Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'four_modes':out['four_modes'],'by_m':out['physical_source_controls']},indent=2))