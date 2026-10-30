#!/usr/bin/env python3
"""Strict signed-(2,2) and wide-source preprocessing hostile controls.
Independent finite source labels; output materialization retained only in
verifier. All source IDs remain authenticated and no oracle routes claimed.
"""
import itertools,json,random,time
from collections import Counter
from virtual_sort_emitter import (Source,VirtualSort,source_models,reference_materialize,
                                  evaluate_clause,source_extremes,selected_work_baseline,properize)
from independent_checker import extend_witness

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'

def parse(s):return tuple(tuple(int(x) for x in row.split()) for row in s.split(';'))

def strict22(S):
    signed=Counter(lit for C in S.clauses for lit in C)
    return (S.m*3==S.n*4 and
            all(signed[x]==signed[-x]==2 for x in range(1,S.n+1)))

def properize_wide(clauses,n):
    """Source-indexed Tseitin split and unit/binary padding for width<=5.
    Source clauses can be 1..5 literals with distinct variables."""
    result=[];provenance=[];newvar=n
    for j,cl in enumerate(clauses,1):
        row=list(cl)
        assert 1<=len(row)<=5 and len({abs(x) for x in row})==len(row)
        raw=[]
        if len(row)<=3:raw.append(tuple(row))
        else:
            while len(row)>3:
                newvar+=1;z=newvar
                raw.append((row[0],row[1],z))
                row=[-z]+row[2:]
            raw.append(tuple(row))
        for seq,r in enumerate(raw):
            if len(r)==3:
                result.append(r);provenance.append((j,seq,0))
            elif len(r)==2:
                newvar+=1;z=newvar
                for k,C in enumerate(properize(r,(z,))):
                    result.append(C);provenance.append((j,seq,k))
            elif len(r)==1:
                p,q=newvar+1,newvar+2;newvar+=2
                for k,C in enumerate(properize(r,(p,q))):
                    result.append(C);provenance.append((j,seq,k))
    assert len(result)==len(provenance)
    return Source(tuple(result),newvar),provenance

def label(clauses,n):
    for bits in itertools.product((0,1),repeat=n):
        if all(any(bits[abs(l)-1]==int(l>0) for l in C) for C in clauses):
            return True
    return False


def pair_modes_local(src):
    tested=0
    for j in range(src.m):
        for k in range(j):
            C,D=src.clauses[j],src.clauses[k]
            S_C={abs(z):int(z>0) for z in C};S_D={abs(z):int(z>0) for z in D}
            for a,b in itertools.product((0,1),repeat=2):
                q={x:(v if a else 1-v) for x,v in S_C.items()}
                r={x:(v if b else 1-v) for x,v in S_D.items()}
                predicted=all(q[x]==r[x] for x in q.keys()&r.keys())
                union=sorted(q.keys()|r.keys())
                brute=any(all(bits[union.index(x)]==v for x,v in q.items()) and
                          all(bits[union.index(x)]==v for x,v in r.items())
                          for bits in itertools.product((0,1),repeat=len(union)))
                assert predicted==brute
                tested+=1
    return tested


def do_case(name,S,expected=None,rng=None):
    start=time.perf_counter()
    models=source_models(S)
    if expected is not None:assert bool(models)==expected
    e=VirtualSort(S)
    rows,reff=reference_materialize(S)
    assert len(rows)==e.m
    assert all(emitted==e.clause(i) for i,emitted in enumerate(rows))
    pair_checks=pair_modes_local(S)
    rng=rng or random.Random(1900)
    num_probe=min(3000,e.bits)
    sample=[0,1,2,3,e.bits-1,e.bits//2,e.bits//3]+[rng.randrange(e.bits) for _ in range(num_probe)]
    for addr in sample:
        if addr<4: expected_bit=(0,1,1,0)[addr]
        elif addr<4+e.wh:expected_bit=(e.n>>(e.wh-1-addr+4))&1
        elif addr<4+2*e.wh:expected_bit=(e.m>>(e.wh-1-(addr-4-e.wh)))&1
        else:
            c,tail=divmod(addr-4-2*e.wh,3*(1+e.wb))
            p,f=divmod(tail,1+e.wb)
            z=rows[c][p]
            expected_bit=int(z>0) if f==0 else (abs(z)>>(e.wb-f))&1
        assert e.bit(addr)==expected_bit
    witness_checked=False
    if models:
        bits=models[0]
        per_occ=[bits[abs(S.literal(r//3,r%3))-1] for r in range(e.L)]
        witness,final=extend_witness(e,per_occ)
        assert all(evaluate_clause(C,witness) for C in rows)
        witness_checked=True
    base=selected_work_baseline(S)
    assert base['SAT']==bool(models)
    return {'source':name,'source_n':S.n,'source_m':S.m,'strict_signed22':strict22(S),
            'source_model_count_exhaustive':len(models),'source_sat':bool(models),
            'materialized_clause_matches':len(rows),'bit_queries_verified':len(sample),
            'S_U_pair_mode_checks':pair_checks,
            'witness_fully_checked':witness_checked,'output_bits':e.bits,
            'baseline_DPLL_nodes':base['nodes'],'baseline_DPLL_literal_tests':base['literal_tests'],
            'elapsed_s':round(time.perf_counter()-start,5)}


def main():
    rng=random.Random(202610301310)
    W=Source(parse(W1),15);T=Source(parse(S15),15)
    assert strict22(W) and strict22(T)
    assert [tuple(sorted(map(abs,c))) for c in W.clauses]==[
           tuple(sorted(map(abs,c))) for c in T.clauses]
    high_sat=[(1,2,3,4,5),(1,)]
    high_unsat=[(1,2,3,4,5),(1,),(-1,)]
    hs,hs_prov=properize_wide(high_sat,5)
    hu,hu_prov=properize_wide(high_unsat,5)
    assert label(high_sat,5) and not label(high_unsat,5)
    assert label(hs.clauses,hs.n) and not label(hu.clauses,hu.n)
    cases=[do_case('W1_UNSAT',W,False,rng),do_case('S15_SAME_UNSIGNED_SUPPORT_SAT',T,True,rng),
           do_case('WIDE5_SAT_properized',hs,True,rng),
           do_case('WIDE5_UNSAT_properized',hu,False,rng)]
    return {'advanced_controls':'PASS','case_count':len(cases),
            'total_materialized_clause_checks':sum(q['materialized_clause_matches'] for q in cases),
            'total_output_bit_probes':sum(q['bit_queries_verified'] for q in cases),
            'total_S_U_pair_mode_checks':sum(q['S_U_pair_mode_checks'] for q in cases),
            'highwidth_preprocessing':{'SAT_source_clauses':list(map(list,high_sat)),
                    'UNSAT_source_clauses':list(map(list,high_unsat)),
                    'SAT_exact3_source_clause_provenance':hs_prov,
                    'UNSAT_exact3_source_clause_provenance':hu_prov,
                    'note':'This auxiliary wide-to-proper3 preparation is materialized and charged separately; no polylog indexed accessor for this conversion is claimed.'},
            'cases':cases}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))