#!/usr/bin/env python3
"""Reproduce VARIABLE_LENGTH_SATURATION238, restricted exact two-stage bit-probe model.

python3 2026-10-29_2017_LSPV-2_VARIABLE_LENGTH_SATURATION238_repro.py
All exhaustive loops have <=32768 iterations except 4096 parity source/query tests.
No external solver, network, oracle, or guessed SAT answer is used.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import combinations, product
from math import comb, log2
from time import perf_counter
import hashlib, json, tracemalloc

RUN_ID='VARIABLE_LENGTH_SATURATION238'
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]


def parity(v):return v.bit_count()&1


def volume(b,q):return sum(comb(b,j) for j in range(min(q,b)+1))


def cap_saturation(b,q):
    v=volume(b,q)
    strength=min(2*q,b)
    certified_cap=v-(int(strength>0 and v%(1<<strength)!=0))
    return {'b':b,'q':q,'v':v,'strength':strength,
            'saturation_divisor':1<<strength,'cap':certified_cap,
            'reason':'exact saturation forces orthogonal array' if certified_cap<v else 'volume bound only'}


@dataclass
class Counters:
    source_reads:int=0
    summary_writes:int=0
    summary_reads:int=0
    mask_reads:int=0
    source_query_probes:int=0
    xor_ops:int=0
    address_ops:int=0
    failed_attempts:int=0


def encode_6(a, meter):
    """Two independent triples with coordinates 1,2,3, store one parity each.
    Raw basis coordinates are still present in the immutable source.
    """
    meter.source_reads+=6
    s=[]
    for g in (0,1):
        t=(a>>(3*g))&7
        v=parity(t)
        meter.xor_ops+=2
        s.append(v)
        meter.summary_writes+=1
    return tuple(s)


def query_6(a,mask,s,meter):
    """All source addresses computed from query mask alone; one per triple."""
    value=0
    addresses=[]
    for g in (0,1):
        w=(mask>>(3*g))&7
        meter.mask_reads+=3
        # labels of three coordinates are binary 01,10,11
        c=((w&1)!=0) ^ (((w>>2)&1)!=0)
        d=(((w>>1)&1)!=0) ^ (((w>>2)&1)!=0)
        label=int(c)+2*int(d)
        meter.xor_ops+=2
        if w&4:
            value ^= s[g]; meter.summary_reads+=1;meter.xor_ops+=1
        if label:
            addr=3*g+label-1
            source_bit=(a>>addr)&1
            value^=source_bit
            meter.source_query_probes+=1
            meter.address_ops+=1;meter.xor_ops+=1
            if label==3:
                value ^= s[g];meter.summary_reads+=1;meter.xor_ops+=1
            addresses.append(addr)
    return value,addresses


def sat_cnf(clauses,assignment):
    return all(any(((assignment>>(abs(l)-1))&1)==(l>0) for l in cl) for cl in clauses)


def parity3_clauses(rhs=0):
    return [tuple(-i if bits[i-1] else i for i in (1,2,3))
            for bits in product((0,1), repeat=3) if sum(bits)%2!=rhs]


def assert_strict22(clauses):
    n=max(abs(l) for cl in clauses for l in cl)
    assert all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in clauses)
    assert {abs(l) for cl in clauses for l in cl}==set(range(1,n+1))
    for v in range(1,n+1):
        assert sum(l==v for cl in clauses for l in cl)==2
        assert sum(l==-v for cl in clauses for l in cl)==2
    neighbors={i:set() for i in range(1,n+1)}
    for cl in clauses:
        names=set(map(abs,cl))
        for v in names:neighbors[v].update(names-{v})
    seen={1};stack=[1]
    while stack:
        for v in neighbors[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    assert len(seen)==n
    return n


def model_count(n,clauses,eqs):
    count=0;tests=0
    for a in range(1<<n):
        tests+=1
        if sat_cnf(clauses,a) and all(parity(a&mask)==rhs for mask,rhs in eqs):count+=1
    return {'n':n,'assignment_tests':tests,'models':count,'sat':bool(count)}


@dataclass
class FactRecord:
    fact: str
    target: str
    state: str
    provenance: str
    certificate: str
    score_name: str
    information_value: float
    score_discovery_source_tests: int
    acquisition_cost: int
    certificate_verification_cost: int
    application_cost: int


def contextual_score(target, known, added, observation_world):
    """Exact finite projected-support ambiguity potential, no witness free to solver.
    Source rows are authenticated against test-world solely for finite examples.
    The score itself enumerates every possible source twice, with explicit charge.
    """
    assert all(parity(observation_world&mask)==rhs for mask,rhs in known+added)
    def outcomes(rows):
        out=set();tests=0
        for a in range(1<<3):
            tests+=1
            if all(parity(a&mask)==rhs for mask,rhs in rows):out.add(parity(a&target))
        return out,tests
    before,c0=outcomes(known)
    after,c1=outcomes(known+added)
    assert before and after
    gain=log2(len(before))-log2(len(after))
    return FactRecord(' & '.join(f'(mask={mask:03b},rhs={rhs})|_v' for mask,rhs in added),
       f'parity target mask={target:03b}', f'known={known}',
       'authenticated source equation for finite test; no answer bit gifted',
       'test-world row agreement plus enumerated logical consistency',
       'projected-support ambiguity log2 distinct outcomes',gain,c0+c1,
       len(added),len(added),len(added))


def independent_saturation_control():
    """An independent 22-member subset has full quadratic evaluation rank,
    but fails orthogonality. This is a control, not enumeration of all fibers.
    """
    from fractions import Fraction
    S=[a for a in range(64) if a.bit_count()<=2]
    masks=[m for m in range(64) if m.bit_count()<=2]
    assert len(S)==len(masks)==22
    P=[[1 if parity(a&m)==0 else -1 for m in masks] for a in S]
    def exact_rank(M):
        M=[[Fraction(x) for x in row] for row in M]
        r=0
        for c in range(len(M[0])):
            j=next((j for j in range(r,len(M)) if M[j][c]),None)
            if j is None:continue
            M[j],M[r]=M[r],M[j];pivot=M[r][c]
            for k in range(c,len(M[0])):M[r][k]/=pivot
            for i in range(r+1,len(M)):
                if not M[i][c]:continue
                fac=M[i][c]
                for k in range(c,len(M[0])):M[i][k]-=fac*M[r][k]
            r+=1
        return r
    rank=exact_rank(P)
    G=[[sum(P[a][i]*P[a][j] for a in range(22)) for j in range(22)] for i in range(22)]
    off=sum(G[i][j]!=0 for i in range(22) for j in range(22) if i!=j)
    assert rank==22 and off>0 and any(G[i][i]!=22 for i in range(22)) is False
    # Exactly 22 points cannot be OA strength 4 because 16 does not divide 22.
    return {'set':'Hamming ball radius 2 in F_2^6','points':22,
            'degree2_eval_rank':rank,'nonzero_offdiag_gram':off,
            'certified_orthogonal_array_possible':False}


def run():
    tic=perf_counter();tracemalloc.start()
    table=[]
    for q in (1,2,3):
        for b in range(max(1,q),33):
            item=cap_saturation(b,q)
            fixed_lb=max(0,b-(item['v'].bit_length()-1))
            badL=fixed_lb-1
            if badL>=0:
                labels=(1<<(badL+1))-1
                if labels*item['v']>=1<<b and labels*item['cap']<1<<b:
                    table.append({**item,'fixed_length_lb':fixed_lb,
                                  'nonprefix_max_len_ruled_out':badL,
                                  'old_count':labels*item['v'],
                                  'new_count':labels*item['cap'],
                                  'required_sources':1<<b})
    assert any(t['b']==6 and t['q']==2 and t['old_count']==66 and t['new_count']==63 for t in table)
    result_count=0;query_probe_hist={0:0,1:0,2:0};meter=Counters()
    for a in range(64):
        s=encode_6(a,meter)
        for mask in range(64):
            before=meter.source_query_probes
            got,addresses=query_6(a,mask,s,meter)
            used=meter.source_query_probes-before
            assert used==len(addresses) and used<=2
            assert got==parity(mask&a)
            query_probe_hist[used]+=1;result_count+=1
    assert result_count==4096
    sat_controls={}
    for name,n,clauses,eqs,expected in [
        ('2SAT_SAT',2,[(1,2),(-1,2)],[],True),
        ('2SAT_UNSAT',1,[(1,),(-1,)],[],False),
        ('XOR_SAT',3,[],[(0b111,0)],True),
        ('XOR_UNSAT',3,[],[(0b111,0),(0b111,1)],False),
        ('MIXED_SAT',2,[(1,2)],[(0b11,1)],True),
        ('MIXED_UNSAT',2,[(1,),(2,)],[(0b11,1)],False),
        ('STRICT22_SAT',3,parity3_clauses(0),[],True),
        ('STRICT22_UNSAT',15,W1,[],False),
    ]:
        if name.startswith('STRICT22'): assert_strict22(clauses)
        entry=model_count(n,clauses,eqs)
        assert entry['sat']==expected,(name,entry)
        sat_controls[name]=entry
    world=0b000
    one=contextual_score(0b011,[],[(0b101,0)],world)
    two=contextual_score(0b011,[],[(0b110,0)],world)
    join=contextual_score(0b011,[(0b101,0)],[(0b110,0)],world)
    duplicate=contextual_score(0b011,[(0b101,0),(0b110,0)],[(0b101,0)],world)
    assert (one.information_value,two.information_value,join.information_value,duplicate.information_value)==(0,0,1,0)
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    out={'run_id':RUN_ID,'status':'PROVED/EXACT restricted theorem; finite controls COMPUTATIONAL',
         'theorem':{'b':6,'q':2,'v':22,'saturation_divisor':16,
                    'max_fiber':21,'number_nonprefix_strings_max_len_1':3,
                    'impossible_source_coverage':63,'required_sources':64,
                    'minimum_nonprefix_max_length':2,
                    'matching_fixed_summary_bits':2},
         'improved_counting_examples':table,
         'finite_controls':{'all_source_query_pairs_6':result_count,
                    'probe_histogram':query_probe_hist,'two_probe_meter':asdict(meter),
                    'hamming_ball_22':independent_saturation_control(),
                    'sat_cnf_xor_controls':sat_controls,
                    'contextual_value':{'individual1':asdict(one),'individual2':asdict(two),
                                        'joint_increment':asdict(join),'duplicate':asdict(duplicate)}},
         'measurement':{'wall_seconds':round(perf_counter()-tic,5),
                        'tracemalloc_peak_bytes':peak,'measurement_scope':'Python observational, one run'},
         'limitations':'No native RAM/UTM bit-time claim; SAT grammar not preserved in parity source; finite checks not proof.'}
    canonical=json.dumps(out,sort_keys=True,separators=(',',':'))
    out['sha256_canonical_without_digest']=hashlib.sha256(canonical.encode()).hexdigest()
    from pathlib import Path
    target=Path(__file__).with_name('2026-10-29_2017_LSPV-2_VARIABLE_LENGTH_SATURATION238_raw.json')
    target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','theorem':out['theorem'],'exhaustive_parity_tests':result_count,
                      'strict22_sat_unsat':[sat_controls['STRICT22_SAT']['models'],
                                            sat_controls['STRICT22_UNSAT']['models']],
                      'improved_bq_pairs':[(r['b'],r['q']) for r in table],
                      'file':str(target),'digest':out['sha256_canonical_without_digest'],
                      'time_s':out['measurement']['wall_seconds']},indent=2))

if __name__=='__main__':run()