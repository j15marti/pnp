#!/usr/bin/env python3
"""Reproducible restricted Q<=2 parity-query frontier and contextual fact interpreter.

Run: python3 2026-10-29_1912_LSPV-2_TWO_PROBE_NONLINEAR_FRONTIER237_repro.py
No SAT algorithm generality is implied. Python memory and timing are observational.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from itertools import product
import hashlib
import json
import math
import random
import time
import tracemalloc

RUN_ID = "TWO_PROBE_NONLINEAR_FRONTIER237"
SEED = 237
# Independently published 15-variable connected strict (2+,2-)-CNF UNSAT control.
W1 = [
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]


def parity(value: int) -> int:
    return value.bit_count() & 1


def sat_cnf(clauses, model):
    return all(any(((model >> (abs(lit)-1)) & 1) == (lit > 0) for lit in clause) for clause in clauses)


def strict22(clauses):
    n=max(abs(lit) for cl in clauses for lit in cl)
    assert {abs(lit) for cl in clauses for lit in cl} == set(range(1,n+1))
    assert all(len(cl)==3 and len(set(map(abs,cl)))==3 for cl in clauses)
    for v in range(1,n+1):
        assert sum(lit==v for cl in clauses for lit in cl)==2
        assert sum(lit==-v for cl in clauses for lit in cl)==2
    seen={1};todo=[1]
    adj={i:set() for i in range(1,n+1)}
    for cl in clauses:
        for v in map(abs,cl): adj[v].update(map(abs,cl))
    while todo:
        for u in adj[todo.pop()]:
            if u not in seen: seen.add(u);todo.append(u)
    assert len(seen)==n
    return {"n":n,"m":len(clauses),"strict22":True,"connected":True}


def parity3_clauses(rhs=0):
    return [tuple((-i if bits[i-1] else i) for i in (1,2,3))
            for bits in product((0,1),repeat=3) if (sum(bits)&1)!=rhs]


@dataclass
class Meter:
    prep_source_reads: int = 0
    prep_xors: int = 0
    summary_writes: int = 0
    query_mask_reads: int = 0
    summary_reads: int = 0
    query_source_probes: int = 0
    last_query_source_probes: int = 0
    query_xors: int = 0
    index_ops: int = 0


def layout(m):
    return 2 * ((1<<m)-1)


def encode_two_probe(source:int, m:int, meter:Meter):
    """Encode b=2(2^m-1) source bits, each group as nonzero m-bit labels.

    Stored bit is x_z XOR sum of basis x_{2^j} for all nonbasis z.
    Basis raw bits are not kept in the summary.
    """
    h=(1<<m)-1
    corrections={}
    for group in range(2):
        basis={1<<j: (source>>(group*h + (1<<j)-1))&1 for j in range(m)}
        meter.prep_source_reads += m
        for z in range(1,h+1):
            meter.index_ops+=1
            if z&(z-1)==0: continue
            val=(source>>(group*h+z-1))&1
            meter.prep_source_reads+=1
            for j in range(m):
                if z&(1<<j): val^=basis[1<<j];meter.prep_xors+=1
            corrections[(group,z)]=val
            meter.summary_writes+=1
    assert len(corrections)==layout(m)-2*m
    assert meter.prep_source_reads==layout(m)
    return corrections


def decode_two_probe(source:int, mask:int, m:int, corrections:dict, meter:Meter):
    h=(1<<m)-1
    targets=[0,0]; known=0;addresses=[]; probes_this_query=0
    for group in range(2):
        for z in range(1,h+1):
            meter.query_mask_reads+=1
            meter.index_ops+=1
            if (mask>>(group*h+z-1))&1:
                targets[group]^=z;meter.query_xors+=1
                if z&(z-1):
                    known^=corrections[(group,z)];meter.summary_reads+=1;meter.query_xors+=1
    for group,target in enumerate(targets):
        if target:
            bit_index=group*h+target-1
            addresses.append(bit_index)
            known^=(source>>bit_index)&1;meter.query_source_probes+=1;probes_this_query+=1;meter.query_xors+=1
            if target&(target-1):
                known^=corrections[(group,target)];meter.summary_reads+=1;meter.query_xors+=1
    meter.last_query_source_probes=probes_this_query
    assert probes_this_query<=2
    return known, addresses


def projection_facts(n, clauses, xor_equations, result):
    """Finite independent SAT evaluator; descendant controls not relabeled strict22."""
    witnesses=0
    for assignment in range(1<<n):
        if sat_cnf(clauses,assignment) and all(parity(assignment&mask)==rhs for mask,rhs in xor_equations):
            witnesses+=1
    assert (witnesses>0)==result
    return witnesses


@dataclass
class FactRecord:
    statement: str
    context: str
    provenance: str
    certificate: dict
    score_definition: str
    info_value: float
    score_discovery_tests: int
    acquisition_cost: int
    verification_cost: int
    application_cost: int
    note: str = ""


def contextual_fact_interpreter(b:int, target_mask:int, observed_world:int, facts:list, old_known:list):
    """Small exact finite model. Acquisition is charged and observations use an
    externally supplied raw world only as a TEST control, not as solver advice.
    """
    def possibilities(given):
        accepted=[];examined=0
        for source in range(1<<b):
            examined+=1
            if all(parity(source&mask)==rhs for mask,rhs in given): accepted.append(source)
        return set(parity(src&target_mask) for src in accepted),examined
    assert all(parity(observed_world&mask)==rhs for mask,rhs in facts)
    base,c0=possibilities(old_known)
    extended,c1=possibilities(old_known+facts)
    assert base and extended
    v=math.log2(len(base))-math.log2(len(extended))
    return FactRecord(
      statement=" AND ".join(f"(mask=0x{mask:x},rhs={rhs})|_v" for mask,rhs in facts),
      context=f"target_parity_mask=0x{target_mask:x}, known={old_known}",
      provenance="finite-observed-world-with-verification; NOT an algorithmic SAT witness",
      certificate={"source_bits_test_only": observed_world,"constraints_satisfied":True},
      score_definition="log2 number of remaining target outcomes; decrease upon applying observed facts",
      info_value=v,
      score_discovery_tests=c0+c1,
      acquisition_cost=len(facts),
      verification_cost=len(facts),
      application_cost=len(facts),
      note="The true world is hidden from the solver; this record is only a finite scoring control."
    )


def entropy(p):
    return -(p*math.log2(p)+(1-p)*math.log2(1-p)) if 0<p<1 else 0.0


def run():
    begun=time.perf_counter()
    randomgen=random.Random(SEED)
    exact_points=[]
    exhaustive=0
    sampled=0
    paired=[]
    # All b<=6 source/query combinations are exhaustively tested, larger fixed-
    # length cases are exhaustively tested over query masks for selected sources.
    for m in [1,2,3,4,5]:
        b=layout(m);L=b-2*m
        V=sum(math.comb(b,j) for j in range(3))
        assert 2**(2*m)<=V<2**(2*m+1)
        lower=b-int(math.log2(V))
        # Avoid floating point exactness for large integers in verification.
        lower=b-(V.bit_length()-1)
        assert L==lower
        q1_L=b-((b+1).bit_length()-1)
        point={"m":m,"b":b,"fixed_L_Q0":b,"fixed_L_Q1":q1_L,
               "fixed_L_Q2":L,"ball_volume":V,"ball_floor_log2":V.bit_length()-1,
               "summary_bits_saved_vs_literals":2*m}
        exact_points.append(point)
        if m<=2:
            sources=range(1<<b)
            masks=range(1<<b)
        elif m==3:
            sources=[0,(1<<b)-1,randomgen.getrandbits(b),randomgen.getrandbits(b)]
            masks=range(1<<b)
        else:
            sources=[0,(1<<b)-1]+[randomgen.getrandbits(b) for _ in range(16)]
            masks=None
        for source in sources:
            meter=Meter()
            sigma=encode_two_probe(source,m,meter)
            if masks is None:
                maskset=[0,(1<<b)-1]+[randomgen.getrandbits(b) for _ in range(128)]
            else: maskset=masks
            for w in maskset:
                got,addresses=decode_two_probe(source,w,m,sigma,meter)
                want=parity(w&source)
                assert got==want,(m,source,w,got,want)
                assert len(addresses)<=2
                if m<=2: exhaustive+=1
                else: sampled+=1
        if m<=4:
            source=randomgen.getrandbits(b)
            tracemalloc.start();tic=time.perf_counter()
            a=Meter();sketch=encode_two_probe(source,m,a)
            for w in range(min(1024,1<<b)):
                guess,_=decode_two_probe(source,w,m,sketch,a)
                assert guess==parity(w&source)
            secs=time.perf_counter()-tic
            peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
            paired.append({"b":b,"queries":min(1024,1<<b),"elapsed_seconds":secs,
                           "same_run_python_traced_peak_bytes":peak,"meter":asdict(a)})
    assert exhaustive==16+4096
    # Independent general lower bound: for every b<=9 and Q<=3 the declared
    # dimension of degree-Q source characters equals the Hamming ball volume.
    degree_checks=0
    for b in range(1,10):
        for q in range(0,min(b,3)+1):
            monomials=[w for w in range(1<<b) if w.bit_count()<=q]
            assert len(monomials)==sum(math.comb(b,j) for j in range(q+1))
            degree_checks+=1
    # SAT embedding A_a AND parity mask eq bit: exact full X-enumeration.
    sat_embedded=0
    for b in range(1,6):
        for source in range(1<<b):
            unary=[((i+1) if (source>>i)&1 else -(i+1),) for i in range(b)]
            for w in range(1<<b):
                for t in (0,1):
                    assert projection_facts(b,unary,[(w,t)],parity(w&source)==t)==int(parity(w&source)==t)
                    sat_embedded+=1
    # SAT/UNSAT controls across different syntactic classes.
    cases={
      "2sat_sat":projection_facts(2,[(1,2),(-1,2)],[],True),
      "2sat_unsat":projection_facts(1,[(1,),(-1,)],[],False),
      "xor_sat":projection_facts(3,[],[(0b111,0)],True),
      "xor_unsat":projection_facts(3,[],[(0b111,0),(0b111,1)],False),
      "mixed_sat":projection_facts(2,[(1,2)],[(0b11,1)],True),
      "mixed_unsat":projection_facts(2,[(1,),(2,)],[(0b11,1)],False),
      "strict22_sat":projection_facts(3,parity3_clauses(0),[],True),
      "strict22_unsat":projection_facts(15,W1,[],False),
    }
    strict_controls=[strict22(parity3_clauses(0)),strict22(W1)]
    assert cases['strict22_sat']==4 and cases['strict22_unsat']==0
    # Nonadditive and zero/positive contextual values. Observed world x=1,y=0;
    # target x XOR y, neither fact alone fixes it, together does.
    b=2;t=0b11;world=0b01
    share_x=contextual_fact_interpreter(b,t,world,[(0b01,1)],[])
    share_y=contextual_fact_interpreter(b,t,world,[(0b10,0)],[])
    both=contextual_fact_interpreter(b,t,world,[(0b01,1),(0b10,0)],[])
    dup=contextual_fact_interpreter(b,t,world,[(0b01,1)],[(0b01,1)])
    assert (share_x.info_value,share_y.info_value,both.info_value,dup.info_value)==(0.0,0.0,1.0,0.0)
    negative_realized=entropy(0.1)-entropy(0.5)
    expected=entropy(.1)-(.1*entropy(.5)+.9*entropy(1/18))
    assert negative_realized<0<expected
    results={
      "run_id":RUN_ID,"status":"COMPUTATIONAL exact finite controls; restricted proof in .tex",
      "parameters":{"seed":SEED,"source_bits_model":"raw source retained read-only; future arbitrary parity masks"},
      "symbolic_checks":{"m_values":[1,2,3,4,5],"points":exact_points,
                         "degree_volume_cases":degree_checks},
      "decoder_checks":{"exhaustive_source_mask_pairs":exhaustive,
                        "partial_source_mask_pairs":sampled,
                        "sampled_larger_sources_not_exhaustive":True},
      "sat_controls":{"source_query_answer_exhaustive":sat_embedded,
                      "satisfying_assignment_counts":cases,"strict22_metadata":strict_controls},
      "information_value":{"x_share":asdict(share_x),"y_share":asdict(share_y),
                           "both_shares":asdict(both),"duplicate":asdict(dup),
                           "realized_entropy_value_negative":negative_realized,
                           "expected_entropy_value_positive":expected},
      "paired_observational_resource_traces":paired,
      "elapsed_total_seconds":time.perf_counter()-begun,
      "provenance":{"reference":"prior report NONLINEAR_ONE_PROBE236",
                    "no_external_solver_or_answer_oracle":True,
                    "independent_source_value_ground_truth_checks_are_test_only":True}
    }
    print(json.dumps(results,sort_keys=True,indent=2))

if __name__=="__main__":
    run()
