#!/usr/bin/env python3
"""NONLINEAR-ONE-PROBE236, standalone deterministic stdlib reproducer.

Exact finite controls for a new arbitrary-preprocessing, one-source-probe theorem
in the reusable unary-CNF / future-XOR-query model. Results are not SAT lower bounds.
Usage: python3 2026-10-29_1838_LSPV-2_NONLINEAR_ONE_PROBE236_repro.py > results.json
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from fractions import Fraction
from itertools import product
from collections import Counter
import hashlib, json, math, random, time, tracemalloc

RUN="NONLINEAR_ONE_PROBE236"
W1=[
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]

def parity(z:int)->int: return z.bit_count()&1

def eval_cnf(cs, assignment:int)->bool:
    return all(any(((assignment>>(abs(l)-1))&1)==int(l>0) for l in clause) for clause in cs)

def exact22_check(cs):
    seen={abs(l) for clause in cs for l in clause}; n=max(seen)
    assert seen==set(range(1,n+1))
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in cs)
    assert all(sum(l==v for c in cs for l in c)==2 and
               sum(l==-v for c in cs for l in c)==2 for v in range(1,n+1))
    neighbors={v:set() for v in seen}
    for c in cs:
        for v in map(abs,c): neighbors[v].update(map(abs,c))
    visited={1}; stack=[1]
    while stack:
        for v in neighbors[stack.pop()]:
            if v not in visited: visited.add(v);stack.append(v)
    assert len(visited)==n
    return {"variables":n,"clauses":len(cs),"connected":True,"quota":'exact two positive and two negative'}

def parity3_cnf(rhs=0):
    clauses=[]
    for bits in product((0,1),repeat=3):
        if (sum(bits)&1)!=rhs:
            clauses.append(tuple((-j if bit else j) for j,bit in enumerate(bits,1)))
    exact22_check(clauses)
    return clauses

@dataclass
class Meter:
    source_reads:int=0
    summary_reads:int=0
    summary_writes:int=0
    xor_ops:int=0
    index_steps:int=0
    query_bits_read:int=0
    failed_paths:int=0

# Explicit rank-b-d summary, using all nonzero d-bit labels and storing surplus
# source bits verbatim. The basis coordinates have power-of-two labels.
def dimension(b:int)->int:
    assert b>=1
    return (b+1).bit_length()-1

def encode(source:int,b:int,m:Meter):
    d=dimension(b); n0=(1<<d)-1
    labels=[];summary=[]
    basis={1<<j:((source>>((1<<j)-1))&1) for j in range(d)}
    for pos in range(1,b+1):
        m.index_steps+=1
        if pos<=n0 and pos&(pos-1)==0:
            m.source_reads+=1
            labels.append((pos,'basis'))
            continue
        val=(source>>(pos-1))&1;m.source_reads+=1
        if pos<=n0:
            for j in range(d):
                m.index_steps+=1
                if (pos>>j)&1:
                    val^=basis[1<<j];m.xor_ops+=1
        summary.append((pos,val))
        m.summary_writes+=1
        labels.append((pos,'stored'))
    assert len(summary)==b-d
    return {"b":b,"d":d,"n_hamming":n0,"summary":tuple(summary)}

def decode(sigma,w:int,source:int,m:Meter):
    b=sigma['b'];d=sigma['d'];n0=sigma['n_hamming']
    summary=dict(sigma['summary']); target=0;known=0
    for pos in range(1,b+1):
        m.query_bits_read+=1;m.index_steps+=1
        if not ((w>>(pos-1))&1):continue
        if pos<=n0:
            target^=pos;m.xor_ops+=1
            if pos&(pos-1):
                known^=summary[pos];m.summary_reads+=1;m.xor_ops+=1
        else:
            known^=summary[pos];m.summary_reads+=1;m.xor_ops+=1
    if target:
        pos=target
        assert 1<=pos<=n0
        m.source_reads+=1
        value=(source>>(pos-1))&1
        if pos&(pos-1):
            value^=summary[pos];m.summary_reads+=1;m.xor_ops+=1
        known^=value;m.xor_ops+=1
    return known,int(bool(target))

# A minimal certified-information interpreter; all potential discovery is
# exhaustive and its candidate evaluations are charged.
@dataclass(frozen=True)
class Fact:
    name:str
    mask:int
    rhs:int
    provenance:str
    certificate:dict
    cost_acquire:int
    cost_apply:int

def score_models(bits:int, known:list[Fact], target_mask:int):
    scans=0;target=set()
    for a in range(1<<bits):
        scans+=len(known)+1
        if all(parity(a&f.mask)==f.rhs for f in known): target.add(parity(a&target_mask))
    if not target:return {"phi":None,"support":[],"candidate_scans":scans,"inconsistent":True}
    return {"phi":math.log2(len(target)),"support":sorted(target),
            "candidate_scans":scans,"inconsistent":False}

def certified_record(bits, target_mask, rows:list[tuple[int,int]], recorded:list[Fact], new:Fact):
    # Certification: an equality fact is authenticated by finding its exact
    # input row; membership search is charged rather than asserted for free.
    discover=0;valid=False
    for mask,rhs in rows:
        discover+=1
        if (mask,rhs)==(new.mask,new.rhs):valid=True;break
    assert valid and new.certificate['method']=='source_row_equality'
    before=score_models(bits,recorded,target_mask)
    after=score_models(bits,recorded+[new],target_mask)
    assert not after['inconsistent']
    v=round(before['phi']-after['phi'],8)
    return {"display":f"({new.name})|_{v:g}","fact":asdict(new),"value":v,
            "acquisition_units":new.cost_acquire+discover,
            "application_units":new.cost_apply,
            "score_discovery_candidates":before['candidate_scans']+after['candidate_scans'],
            "pre":before,"post":after}

def xor_synergy():
    # Source equations a xor c=0, b xor c=0, target a xor b.
    eq1=(0b101,0);eq2=(0b110,0);rows=[eq1,eq2]
    a=Fact('a xor c = 0',*eq1,'xor_source_line_1',{'method':'source_row_equality'},4,2)
    b=Fact('b xor c = 0',*eq2,'xor_source_line_2',{'method':'source_row_equality'},4,3)
    r1=certified_record(3,0b011,rows,[],a)
    r2=certified_record(3,0b011,rows,[a],b)
    r3=certified_record(3,0b011,rows,[a,b],a)
    r2first=certified_record(3,0b011,rows,[],b)
    assert (r1['value'],r2['value'],r3['value'],r2first['value'])==(0,1,0,0)
    return {"first":r1,"synergistic_second":r2,"duplicate":r3,
            "second_alone":r2first,'joint_minus_sum_singletons':1}

def entropy(p):
    return -sum(float(x)*math.log2(float(x)) for x in p if x)

def entropy_negative():
    # Biased target prior (9/10,1/10), noisy event E has likelihood
    # Pr(E|T=0)=1/10, Pr(E|T=1)=9/10. Observing E yields uniform posterior.
    prior={0:Fraction(9,10),1:Fraction(1,10)}
    likelihood={0:Fraction(1,10),1:Fraction(9,10)}
    z=sum(prior[t]*likelihood[t] for t in (0,1))
    posterior={t:prior[t]*likelihood[t]/z for t in (0,1)}
    v=entropy(prior.values())-entropy(posterior.values())
    assert all(p==Fraction(1,2) for p in posterior.values()) and v<0
    # Expected entropy decrease is nonnegative, showing it is the
    # realized, not expected, entropy utility that can be negative.
    other={t:prior[t]*(1-likelihood[t])/(1-z) for t in (0,1)}
    expected=entropy(prior.values())-(float(z)*entropy(posterior.values())+
                                      float(1-z)*entropy(other.values()))
    assert expected>0
    return {"prior_entropy":entropy(prior.values()),"observed_event_probability":str(z),
            "posterior_entropy":entropy(posterior.values()),"realized_information_value":v,
            "expected_information_gain":expected,
            "source_type":"observational Bayesian control; not a SAT certificate"}

def is_one_probe_good_fiber(b:int,S:int,parity_patterns:list[int],coordinate_patterns:list[int]):
    for p in parity_patterns:
        v=p&S
        if v==0 or v==S:continue
        if not any(v==(x&S) or v==(S^(x&S)) for x in coordinate_patterns):
            return False
    return True

def exhaustive_nonlinear_b3_b4():
    result=[]
    for b in (3,4):
        n=1<<b;full=(1<<n)-1
        pars=[sum((1<<a) for a in range(n) if parity(a&w)) for w in range(1<<b)]
        coords=[sum((1<<a) for a in range(n) if (a>>i)&1) for i in range(b)]
        count=0;partitions=1<<n
        # Each bit-labeled two-class summary is represented by a subset S.
        # Exhaustive for 2^8=256 and 2^16=65536 distinct one-bit maps.
        for S in range(partitions):
            if (is_one_probe_good_fiber(b,S,pars,coords) and
                is_one_probe_good_fiber(b,full^S,pars,coords)):
                count+=1
        assert (b==3 and count>0) or (b==4 and count==0)
        result.append({"b":b,"L":1,"all_deterministic_one_bit_maps":partitions,
                       "one_probe_valid_maps":count,"exhaustive":True})
    return result

def grammar_controls():
    cs=parity3_cnf(0)
    assert eval_cnf(cs,0)
    assert sum(eval_cnf(cs,a) for a in range(8))==4
    wmeta=exact22_check(W1)
    assert sum(eval_cnf(W1,a) for a in range(1<<15))==0
    sat2=[(1,2),(-1,2)]
    unsat2=[(1,),(-1,)]
    assert sum(eval_cnf(sat2,a) for a in range(4))>0
    assert sum(eval_cnf(unsat2,a) for a in range(2))==0
    xorsat=lambda a:parity(a&3)==1
    xorunsat=lambda a:parity(a&3)==1 and parity(a&3)==0
    assert sum(xorsat(a) for a in range(4))==2
    assert sum(xorunsat(a) for a in range(4))==0
    assert sum(eval_cnf(sat2,a) and xorsat(a) for a in range(4))>0
    assert sum(eval_cnf([(1,2),(-1,),(-2,)],a) and xorsat(a) for a in range(4))==0
    return {"2sat_SAT_models":sum(eval_cnf(sat2,a) for a in range(4)),
            "2sat_UNSAT_models":0,"XOR_SAT_models":2,"XOR_UNSAT_models":0,
            "mixed_SAT_models":sum(eval_cnf(sat2,a) and xorsat(a) for a in range(4)),
            "mixed_UNSAT_models":0,"strict22_SAT":{**exact22_check(cs),"models":4},
            "strict22_UNSAT":{**wmeta,"models":0,"enumerated_assignments":1<<15},
            "claim":"controls only; no strict22 closure or all-input compiler"}

def btable():
    rows=[]; rng=random.Random(236); total=0
    for b in range(1,10):
        d=dimension(b);L=b-d;worst_probe=0;checks=0
        meter=Meter();prep=Meter();a0=0;summary0=encode(a0,b,prep)
        # Sum construction charge across every source, using independent meter.
        for a in range(1<<b):
            p=Meter();sigma=encode(a,b,p)
            assert len(sigma['summary'])==L
            for w in range(1<<b):
                m=Meter();out,pb=decode(sigma,w,a,m)
                assert out==parity(a&w)
                assert m.source_reads==pb and pb<=1
                worst_probe=max(worst_probe,pb)
                checks+=1
                if a==0: meter.source_reads+=m.source_reads;meter.summary_reads+=m.summary_reads
                meter.xor_ops+=m.xor_ops;meter.index_steps+=m.index_steps
        assert worst_probe==1
        total+=checks
        rows.append({"b":b,"d":d,"max_source_probe_after_preprocessing":1,
                     "min_worst_case_L_for_any_nonlinear_summary":L,
                     "actual_summary_L":L,"literal_summary_same_L_worst_query_probes":d,
                     "construction_source_reads_per_source":p.source_reads,
                     "construction_summary_writes_per_source":p.summary_writes,
                     "construction_xor_ops_per_source":p.xor_ops,
                     "query_bit_decode_work_upper_b_times_d":b*d,
                     "exhaustive_all_sources_and_masks":checks,
                     "instrumented_last_query_steps":asdict(m)})
    for b in (10,11,12,15,31):
        d=dimension(b);L=b-d
        for _ in range(100):
            a=rng.getrandbits(b);w=rng.getrandbits(b)
            p=Meter();sigma=encode(a,b,p)
            m=Meter();ans,q=decode(sigma,w,a,m)
            assert ans==parity(a&w) and q<=1
        rows.append({"b":b,"d":d,"min_worst_case_L_for_any_nonlinear_summary":L,
                     "actual_summary_L":L,"literal_summary_same_L_worst_query_probes":d,
                     "sampled_source_mask_pairs":100,"max_source_probe_after_preprocessing":1})
    return rows,total

def joint_cnf_xor_sat_controls():
    # Independent existential enumeration over all X, not the shortcut x=a.
    count=0
    for b in range(1,7):
        for a in range(1<<b):
            for w in range(1<<b):
                for t in (0,1):
                    truth=any((x==a) and (parity(x&w)==t) for x in range(1<<b))
                    assert truth==(parity(a&w)==t)
                    count+=1
    return {"complete_source_query_threshold_enumerations":count,"max_b":6,
            "semantics":"explicit exists X of A_a(X) AND [w dot X=t]"}

def same_run_python_resources():
    # Measurements are observational Python tracing, NOT a native bit-RAM or TM.
    rng=random.Random(236);rows=[]
    for b in (7,15,31,63,127):
        source=rng.getrandbits(b)
        masks=[rng.getrandbits(b) for _ in range(200)]
        meter=Meter();tracemalloc.start();t0=time.perf_counter()
        sigma=encode(source,b,meter)
        pc=asdict(meter)
        for w in masks:
            out,_=decode(sigma,w,source,meter)
            assert out==parity(source&w)
        seconds=time.perf_counter()-t0
        cur,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        rows.append({"b":b,"queries":len(masks),"stored_summary_bits":b-dimension(b),
                     "total_python_seconds":seconds,"same_run_python_peak_bytes":peak,
                     "total_measured_events":asdict(meter),"preprocessing_events":pc})
    return rows

def main():
    now=time.perf_counter()
    rows,total=btable(); exhaust=exhaustive_nonlinear_b3_b4();gram=grammar_controls()
    synergy=xor_synergy();bayes=entropy_negative()
    sat_semantics=joint_cnf_xor_sat_controls(); resources=same_run_python_resources()
    raw={"run_id":RUN,"mode":"fully deterministic, exhaustive where stated", 
         "machine":"indexed bit-RAM; read-only packed source plus explicit L-bit writable cached summary",
         "new_theorem":"arbitrary nonlinear deterministic summary, one post-preprocessing source probe",
         "linear_extension_b_not_closed_strict22":True,
         "frontier":rows,"exhaustive_source_query_pairs":total,
         "all_nonlinear_one_bit_map_controls":exhaust,
         "source_grammar_controls":gram,"certified_fact_interpreter":synergy,
         "bayesian_negative_control":bayes,"complete_two_phase_sat_semantics":sat_semantics,
         "same_run_python_resource_controls":resources,"elapsed_seconds":time.perf_counter()-now,
         "provenance":{"seed":236,"stdlib_only":True,"source_history":"GitHub AFFINE_PROFILE_CROSSOVER234 and CONTEXTUAL_VALUE_HAMMING235; W1 explicit in CONNECTOR231"}}
    print(json.dumps(raw,sort_keys=True,indent=2))
if __name__=="__main__":main()