#!/usr/bin/env python3
"""OBLIVIOUS-SORT143 finite reproducibility. Fixed topology, exact source labels.
Run: python3 OBLIVIOUS_SORT143_repro.py --output OBLIVIOUS_SORT143_results.json
Only high-level record traffic is counted, NOT primitive-bit machine time.
"""
import argparse
import itertools
import json
import random
from collections import Counter

def topology(p):
    assert p>=2 and (p&(p-1))==0
    stages=[]
    for r in range(1,p.bit_length()):
        for h in range(r-1,-1,-1):
            step=1<<h
            layer=[(i,i^step,(i&(1<<r))==0)
                   for i in range(p) if i<(i^step)]
            assert len(layer)==p//2
            assert sorted(t for i,j,_ in layer for t in (i,j))==list(range(p))
            stages.append(layer)
    return stages

def sort_oblivious(rows,stat=None):
    p=2
    while p<len(rows):p*=2
    a=list(rows)+[(1,0,-1,0)]*(p-len(rows))
    for layer in topology(p):
        old=a[:]
        for i,j,up in layer:
            u,v=old[i],old[j]
            if (u[:2]>v[:2]) if up else (u[:2]<v[:2]):u,v=v,u
            a[i],a[j]=u,v
            if stat is not None:
                stat['record_reads']+=2
                stat['record_writes_including_unchanged']+=2
                stat['record_comparisons']+=1
    return a

def verify_occurrence_witness(clauses,y,stat=None):
    occ=[lit for c in clauses for lit in c]
    assert len(occ)==len(y)
    if any(l==0 for l in occ):return False
    s=sort_oblivious([(0,abs(l),i,y[i]) for i,l in enumerate(occ)],stat)
    if any(a[0]==b[0]==0 and a[1]==b[1] and a[3]!=b[3]
           for a,b in zip(s,s[1:])):return False
    p=0
    for c in clauses:
        if not any(y[p+j] if lit>0 else not y[p+j] for j,lit in enumerate(c)):
            return False
        p+=len(c)
    return True

def named_sat(F):
    keys=sorted({abs(l) for c in F for l in c})
    models=[]
    for bits in itertools.product((0,1),repeat=len(keys)):
        a=dict(zip(keys,bits))
        if all(any(a[abs(l)] if l>0 else not a[abs(l)] for l in c) for c in F):
            models.append(a)
    return models

def run(seed=202610241545):
    rng=random.Random(seed)
    checks=Counter();record=Counter();cases=[]
    for p in (2,4,8,16,32,64):
        network=topology(p)
        for layer in network:
            for i,j,up in layer:
                assert i^j and (i^j).bit_count()==1
                assert any(ii==i and jj==j and uu==up for ii,jj,uu in layer)
                checks['local_address_inverse_checks']+=1
        for _ in range(60):
            rows=[(0,rng.randrange(1,2*p+1),i,rng.randrange(2))
                  for i in range(p)]
            result=sort_oblivious(rows)
            assert [r[:2] for r in result]==sorted(r[:2] for r in rows)
            checks['sort_trials']+=1
    examples={
      'sat_small':[(1,2,3),(-1,2,3)],
      'unsat_unit':[(1,),(-1,)],
      'unsat_three_all_signs':[
        tuple(s*(j+1) for j,s in enumerate(v))
        for v in itertools.product((-1,1),repeat=3)],
      'affine_xor_2':[(1,2),(-1,-2)],
      'horn_easy':[(1,2,3),(-1,2,3),(-2,3,1)],
      'M22_fixture_Y':[
        (1,2,3),(1,4,5),(2,4,6),(3,5,6),
        (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
    }
    for name,F in examples.items():
        models=named_sat(F)
        L=sum(len(c) for c in F)
        if L<=12:
            good=sum(bool(verify_occurrence_witness(F,y))
                     for y in itertools.product((0,1),repeat=L))
            assert good==len(models)
            checks['exhaustive_occurrence_assignments']+=2**L
        if models:
            sample=models[0]
            occvals=[sample[abs(l)] for c in F for l in c]
            assert verify_occurrence_witness(F,occvals)
            checks['true_source_assignment_checked']+=1
        for _ in range(160):
            local=[rng.randrange(2) for _ in range(L)]
            flag=verify_occurrence_witness(F,local,record)
            if flag:
                names={}
                for lit,v in zip((x for c in F for x in c),local):
                    assert abs(lit) not in names or names[abs(lit)]==v
                    names[abs(lit)]=v
                assert all(any(names[abs(l)] if l>0 else not names[abs(l)]
                               for l in c) for c in F)
            checks['random_witness_checks']+=1
        p=2
        while p<L:p*=2
        cases.append({'name':name,'occurrences':L,'sat':bool(models),
                      'sort_depth':len(topology(p))})
    checks['total_assertion_groups']=sum(checks.values())
    return {'run_id':'OBLIVIOUS-SORT143','seed':seed,
            'category_counts':dict(checks),'record_counters':dict(record),
            'cases':cases,'status':'COMPUTATIONAL',
            'limits':'No Tseitin-gate enumeration or physical bit trace'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--seed',type=int,default=202610241545)
    args=parser.parse_args()
    data=run(args.seed)
    with open(args.output,'w') as f:json.dump(data,f,sort_keys=True,indent=2)
    print(json.dumps(data,sort_keys=True,indent=2))
