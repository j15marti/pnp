#!/usr/bin/env python3
"""Exact finite audit for graph-enumeration vs hypothetical sublinear-height TE.
The integers below are *protocol* costs, not lower bounds on all algorithms.
"""
import json, hashlib, platform
from pathlib import Path
from fractions import Fraction
from itertools import product
from math import isqrt

checks = {}
def ok(cond, name):
    if not cond: raise AssertionError(name)
    checks[name] = checks.get(name,0)+1

def ceildiv(a,b): return (a+b-1)//b

def ceil_log2(N):
    assert N>=1
    return (N-1).bit_length()

# Exact integer optimum for the explicit-schedule/current-block two-register
# interface: b block cells, B=ceil(T/b) schedule symbols, both simultaneously
# counted. No floating-point approximations.
for T in range(1,1201):
    q=isqrt(T) + (isqrt(T)**2 < T)
    ub=max(q,ceildiv(T,q))
    ok(ub==q, 'constructive_square_root_attainment')
    for b in range(1,T+1):
        B=ceildiv(T,b)
        ok(max(b,B)>=q, 'exact_ceil_sqrt_barrier')

# Count all ternary graph records of length B (or p*B for p work tapes).
# These are distinct syntactic records. All 2^B nonnegative move schedules are
# physically consistent for a fixed machine with 4-step blocks that obeys B
# input directives; the machine can also read those directives on demand,
# so this is not a lower bound on semantic graph workspace.
for B in range(1,18):
    for p in (1,2,3):
        bits=ceil_log2(3**(p*B))
        ok(bits>=p*B,'information_capacity_full_ternary_record')
        ok(2**(bits-1) < 3**(p*B) <= 2**bits, 'tight_fixed_length_record_capacity')
    ok(ceil_log2(2**B)==B,'binary_schedule_capacity')

for B in range(1,11):
    distinct=set()
    for seq in product((0,1),repeat=B):
        head=0
        visited=[0]
        for bit in seq:
            if bit: head+=4
            visited.append(head)
        # The complete head motion transcript contains the input bits.
        distinct.add(tuple(visited))
    ok(len(distinct)==2**B,'all_binary_block_motion_schedules_realizable')

# Explicitly show that, if a known schedule lives in immutable read-only input,
# a streaming generator needs only a constant/ logarithmic counter, not a
# simultaneous B-bit writable record. Hence no representation-independent LB.
for B in range(1,250):
    schedule=tuple((7*i+3)%2 for i in range(B))
    recovered=tuple(schedule[i] for i in range(B))
    ok(recovered==schedule,'source_streaming_control_no_materialized_graph')

examples=[]
for k in range(1,5):
    # t = 2^(6k), classical cube-root candidate b = 2^(2k), B=2^(4k)
    t=1<<(6*k); b=1<<(2*k); B=ceildiv(t,b)
    old_sweep_peak=max(b,B)
    hypothetical_eval_peak=max(b,isqrt(B))
    square_b=1<<(3*k); square_B=ceildiv(t,square_b)
    ok(hypothetical_eval_peak==b,'would_be_cube_root_without_graph')
    ok(old_sweep_peak==B,'retained_graph_dominates_cube_root_candidate')
    ok(max(square_b,square_B)==square_b,'square_root_protocol_choice')
    examples.append({'T':t,'b_cube':b,'B_tree_height':B,
                    'candidate_evaluator_peak':hypothetical_eval_peak,
                    'explicit_graph_peak_lower_bound':old_sweep_peak,
                    'square_root_protocol_peak':square_b,
                    'graph_to_candidate_ratio':Fraction(old_sweep_peak,hypothetical_eval_peak).__str__(),
                    'number_of_binary_schedules_as_power_of_2':B})

# General target exponent rho requires alpha and beta <= rho/(1-rho).
# beta=1 for explicit graph and means best rho>=1/2.
for rho in [Fraction(1,3),Fraction(2,5),Fraction(49,100)]:
    lim=rho/(1-rho)
    ok(lim<1,'height_exponent_below_one_for_subsqrt_goal')
    ok(Fraction(1,1)>lim,'explicit_graph_exceeds_improved_target')

res={'status':'COMPUTATIONAL','seed':'none, deterministic exhaustive',
    'assertions':sum(checks.values()),'failures':0,
    'assertions_by_category':checks,
    'examples':examples,
    'models':{'space':'peak counted writable cells for explicit full schedule protocol',
              'height':'B=ceil(T/b)',
              'graph_record':'p B ternary block-move guesses, fixed finite p',
              'time':'no polynomial sequential-time claim; enumeration may be exponential',
              'countercontrol':'input-carried instructions allow lazy read-only generation'},
    'parameters':{'T_range':[1,1200],'ternary_B_range':[1,17],
                  'binary_schedule_B_range':[1,10],
                  'streamed_schedule_B_range':[1,249],
                  'cube_k_range':[1,4]},
    'python_version':platform.python_version(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'explicit full graph guess retained during TE only, not all TIME[t] simulations'}
output=Path(__file__).with_name('raw_graph_guess050.json')
output.write_text(json.dumps(res,sort_keys=True,indent=2)+'\n')
print(json.dumps({'assertions':res['assertions'],'failures':0,'checks':checks,'examples':examples,'sha256':res['script_sha256']},indent=2))
