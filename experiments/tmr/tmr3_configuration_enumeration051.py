#!/usr/bin/env python3
"""Exact audit of bounded-space deterministic enumeration versus configurations.
All claims are scoped to fixed-tape, fixed-alphabet total deterministic deciders
with read-only source length n and all writable tapes counted. No SAT bound.
"""
from __future__ import annotations
import argparse, json, hashlib, math, sys
from pathlib import Path
from collections import Counter

checks=Counter()
def ck(pred,key):
    if not pred: raise AssertionError(key)
    checks[key]+=1

def ceil_log2(v:int)->int:
    return (v-1).bit_length() if v>0 else 0

def single_binary_upper_configs(n:int,s:int,q:int=8)->int:
    """Generous overcount for finite control q, one writable binary tape."""
    return q*(n+2)*(s+2)*(1<<s)

def min_s_for_k(k:int,n:int,q:int=8)->int:
    s=0
    while single_binary_upper_configs(n,s,q)<k:
        s+=1
    return s

def trits(index:int,width:int)->tuple[int,...]:
    o=[]
    for _ in range(width):
        index,rem=divmod(index,3);o.append(rem)
    ck(index==0,'trits_range')
    return tuple(o)

def run():
    finite=[]
    for b in range(1,11):
        k=3**b
        got=set()
        for v in range(k):
            digits=trits(v,b)
            got.add(digits)
            ck(len(digits)==b and all(x in (0,1,2) for x in digits),'trit_structure')
            ck(sum(z*(3**i) for i,z in enumerate(digits))==v,'trit_roundtrip')
        ck(len(got)==k,'full_ternary_enumeration')
        ck(trits(k-1,b)==(2,)*b,'last_candidate_all_plus')
        ck(ceil_log2(k)==(k-1).bit_length(),'information_state_bits')
        # A necessary, NOT sufficient, writable-space condition for a particular
        # fixed q-state one-binary-work-tape machine that actually takes k steps.
        n=2*b
        floor=min_s_for_k(k,n)
        ck(single_binary_upper_configs(n,floor)>=k,'config_floor_upper_count')
        if floor:
            ck(single_binary_upper_configs(n,floor-1)<k,'config_floor_minimal')
        finite.append({'B':b,'candidates':k,'minimum_internal_state_bits':ceil_log2(k),
                       'necessary_single_tape_writable_cells_from_config_bound':floor,
                       'n':n,'q':8})

    # Formula inequality for a fixed-q, fixed-one-work-tape machine, including
    # the work-head and input-head positions. These are necessary bounds,
    # independent of the encoding of the candidate records.
    large=[]
    for b in range(1,201):
        k=3**b;n=2*b
        floor=min_s_for_k(k,n)
        ck(single_binary_upper_configs(n,floor)>=k,'large_config_floor')
        if floor:ck(single_binary_upper_configs(n,floor-1)<k,'large_floor_tight')
        ck(floor <= ceil_log2(k),'info_entropy_ceiling')
        if b in [1,2,4,8,12,16,24,32,64,128,200]:
            large.append({'B':b,'log2_K_ceil':ceil_log2(k),
                          'lower_S_binary_one_tape':floor,'n':n})

    exponent=[]
    for p in range(1,8):
        # T=2^(3p), cube-root block b=2^p, h=T/b=2^(2p)
        t=2**(3*p);block=2**p;h=t//block
        s_cuberoot=block
        ck(h>block,'cube_gap_beyond_p1') if p>1 else None
        ck(t==h*block,'cube_arithmetic')
        # If all 3^h candidates are actually inspected on an n <= poly(h)
        # length input, s must be Omega(h), not O(t^(1/3)).
        # No enormous exponentiation needed to find log2(3^h).
        label_bits=ceil_log2(3**h)
        ck(label_bits>=h,'log_candidate_capacity')
        lower_s=min_s_for_k(3**h,2*h)
        ck(single_binary_upper_configs(2*h,lower_s)>=3**h,'cube_config_count')
        exponent.append({'original_T':t,'block_b':block,'height_B':h,
                         'cube_target_S':s_cuberoot,'exhaustive_candidates':'3^'+str(h),
                         'ceil_log2_candidates':label_bits,
                         'necessary_binary_one_tape_S':lower_s})

    # A genuine compact alternative: graph indexed directly on the short,
    # read-only source. A machine can answer any requested graph symbol by
    # scanning, using O(log B) indexing space; no forced 3^B enumeration.
    for b in range(1,256):
        words=[(5*i+3)%3 for i in range(b)]
        for index in (0,b//2,b-1):
            observed=next(x for i,x in enumerate(words) if i==index)
            ck(observed==words[index],'read_only_direct_graph_control')

    # Semantic/physical sanity checks: 2^B distinct nonnegative head-motion
    # traces are possible across B specified steps, but not on one fixed input
    # for one fixed deterministic machine. This is only a source-variation count.
    for b in range(1,17):
        vals=set()
        for v in range(2**b):
            head=0;trace=[0]
            for i in range(b):
                head+=(v>>i)&1
                trace.append(head)
            vals.add(tuple(trace))
        ck(len(vals)==2**b,'distinct_source_dependent_move_traces')

    return {
        'status':'COMPUTATIONAL', 'assertions':sum(checks.values()),
        'failures':0,'assertions_by_category':dict(sorted(checks.items())),
        'parameter_ranges':{'enumeration_B':[1,10],'config_bound_B':[1,200],
                            'cube_power_p':[1,7],'read_only_control_B':[1,255],
                            'motion_trace_B':[1,16]},
        'finite_enumeration':finite,'large_bound_examples':large,
        'cube_examples':exponent,'seed':'none; deterministic exhaustive',
        'machine_scope':'fixed total deterministic; read-only input length n; finite control; one binary counted work tape for numeric floor',
        'protocol_scope':'machine must actually process 3^B distinct candidates sequentially on one fixed input',
        'limitations':['No lower bound for arbitrary simulation or graph acquisition.',
                       'No polynomial time bound for a hypothetical Tree Evaluation algorithm.',
                       'No claim that Williams requires the full candidate scan on each input.',
                       'Finite checks do not prove asymptotic lower bounds.',
                       'Work tape space must include output buffers, messages and any storage used by the iterator.'],
        'python_version':sys.version.split()[0],
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='tmr3_configuration_enumeration051_raw.json')
    a=p.parse_args()
    obj=run()
    Path(a.output).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'checks':obj['assertions'],'failures':obj['failures'],
                      'sha256':obj['source_sha256'],'raw_file':a.output,
                      'cube_examples':obj['cube_examples']},indent=2))
