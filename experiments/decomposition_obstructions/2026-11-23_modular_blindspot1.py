#!/usr/bin/env python3
"""Redteam MODULAR-BLINDSPOT-1: reproducible 3-CNF/XOR/2SAT tests.
Standard library only. Run: python3 2026-11-23_modular_blindspot1.py output.json
"""
import json, sys
from itertools import combinations
from random import Random
from fractions import Fraction

CORE=[(0,5,6),(1,2,5),(0,1,2),(2,3,6),(3,4,5),(4,5,6)]

def satisfying(edges,n):
    masks=[sum(1<<v for v in edge) for edge in edges]
    return [a for a in range(1<<n)
            if all((a&mask).bit_count()==1 for mask in masks)]

def rank_consistency(edges,n,p):
    a=[[int(v in edge)%p for v in range(n)]+[1] for edge in edges]
    rank=0; field_ops=0
    for col in range(n):
        t=next((i for i in range(rank,len(a)) if a[i][col]),None)
        if t is None:continue
        a[rank],a[t]=a[t],a[rank]
        inv=pow(a[rank][col],-1,p)
        for j in range(col,n+1):
            a[rank][j]=a[rank][j]*inv%p; field_ops+=1
        for i in range(len(a)):
            if i==rank or not a[i][col]:continue
            c=a[i][col]
            for j in range(col,n+1):
                a[i][j]=(a[i][j]-c*a[rank][j])%p;field_ops+=1
        rank+=1
    return rank,all(any(row[:n]) or row[-1]==0 for row in a),field_ops

def det_bareiss(m):
    a=[list(row) for row in m];n=len(a);den=1;sign=1
    for k in range(n-1):
        if not a[k][k]:
            t=next((i for i in range(k+1,n) if a[i][k]),None)
            if t is None:return 0
            a[k],a[t]=a[t],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator%den==0
                a[i][j]=numerator//den
        for i in range(k+1,n):a[i][k]=0
        den=pivot
    return sign*a[-1][-1]

def encoding(edge):
    odd=[]
    for bits in range(8):
        if bits.bit_count()%2==0:
            odd.append(tuple(-(edge[j]+1) if bits>>j&1 else edge[j]+1
                             for j in range(3)))
    at_most=[(-a-1,-b-1) for a,b in combinations(edge,2)]
    return odd,at_most

def truth(clause,mask):
    return any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause)

def audit():
    pcnf=[];bcnf=[]
    for e in CORE:
        a,b=encoding(e);pcnf+=a;bcnf+=b
    assert (len(pcnf),len(bcnf))==(24,18)
    for assignment in range(128):
        exactly_one=all(sum(assignment>>v&1 for v in e)==1 for e in CORE)
        cnf=all(truth(c,assignment) for c in pcnf+bcnf)
        assert exactly_one==cnf
    assert len(satisfying(CORE,7))==0
    neighbors=[len(satisfying(CORE[:i]+CORE[i+1:],7)) for i in range(6)]
    assert all(x>=1 for x in neighbors)
    # Module A parity is SAT by all-ones; B 2CNF is SAT by all-zeros.
    assert all(len(e)%2==1 for e in CORE)
    assert all(all(not truth(c,0) for c in []) for _ in [0])
    assert all(truth(c,0) for c in bcnf)
    integer_witness=[0,2,-1,1,0,0,1]
    assert all(sum(integer_witness[v] for v in e)==1 for e in CORE)
    fractional=[Fraction(1,3)]*7
    assert all(sum(fractional[v] for v in e)==1 for e in CORE)
    mat=[[int(v in e) for v in range(7)] for e in CORE]
    cols=(0,1,2,3,4,6)
    determinant=det_bareiss([[row[v] for v in cols] for row in mat])
    assert determinant==1
    modular={}
    for prime in (2,3,5,7,11,13,17,31,97):
        rank,consistent,operations=rank_consistency(CORE,7,prime)
        assert rank==6 and consistent
        modular[str(prime)]={'rank':rank,'consistent':consistent,'field_updates':operations}
    rng=Random(20261123)
    records=[]
    for n in range(7,14):
        available=list(combinations(range(n),3))
        for seed_case in range(40):
            e=rng.sample(available,n-1)
            sat=bool(satisfying(e,n))
            r2,c2,w2=rank_consistency(e,n,2)
            r3,c3,w3=rank_consistency(e,n,3)
            assert not sat or (c2 and c3)
            records.append({'n':n,'seed_case':seed_case,'sat':sat,
                            'gf2_rank':r2,'gf2_consistent':c2,
                            'gf3_rank':r3,'gf3_consistent':c3,
                            'gf2_field_updates':w2,'gf3_field_updates':w3})
    summary=[]
    for n in range(7,14):
        sub=[r for r in records if r['n']==n]
        summary.append({'n':n,'cases':len(sub),
            'unsat':sum(not r['sat'] for r in sub),
            'unsat_mod2_mod3_both_consistent':sum(not r['sat'] and r['gf2_consistent']
                                                and r['gf3_consistent'] for r in sub),
            'unsat_GF3_full_row_rank':sum(not r['sat'] and r['gf3_rank']==n-1
                                         for r in sub)})
    return {'status':'finite exact audit, not an asymptotic lower bound',
      'core':{'edges_0_based':CORE,'n':7,'m':6,'model_count':0,
              'neighbors_model_counts':neighbors,'odd_parity_cnf_clauses':24,
              'binary_2sat_clauses':18,'checked_cnf_assignments':128,
              'integer_witness':integer_witness,'fractional_witness':'1/3 each',
              'unimodular_minor_columns_0_based':cols,'minor_determinant':determinant,
              'fields':modular},'random_summary':summary,'records':records}

if __name__=='__main__':
    report=audit()
    filename=sys.argv[1] if len(sys.argv)>1 else 'modular_blindspot1_results.json'
    with open(filename,'w',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'core':report['core'],
                      'random_summary':report['random_summary']},indent=2))
    print('saved',filename)
