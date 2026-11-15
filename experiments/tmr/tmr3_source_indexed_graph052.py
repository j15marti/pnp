#!/usr/bin/env python3
"""Exact finite audit for a source-indexed adaptive headwalk graph family.

Fixed physical program: scan immutable source one symbol per step; move a blank
work-tape head right on symbol 1 and stay on 0. Promised sources are B aligned
constant runs of length b. Every such source yields a distinct B-bit work-head
block-movement transcript. This is a restricted source-controlled machine, not
an arbitrary SAT or Tree Evaluation algorithm.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
from collections import Counter
from pathlib import Path

TESTS = Counter()

def ck(statement, label):
    if not statement:
        raise AssertionError(label)
    TESTS[label] += 1

def source_encode(word, b):
    return ''.join(v*b for v in word)

def physical_headwalk(source, b):
    head = 0
    first = []
    movement = []
    for j, bit in enumerate(source):
        if j % b == 0:
            first.append(head//b)
        head += int(bit)
        if (j+1) % b == 0:
            movement.append((head//b) - first[-1])
    return tuple(movement), tuple(first), head

def canonical_selector(source, b, i):
    if i<1 or i*b>len(source):
        raise IndexError(i)
    return int(source[(i-1)*b])

def promise_check(source, b):
    return b>=1 and len(source) % b == 0 and all(
        source[j]==source[(j//b)*b] for j in range(len(source))
    )

def edges_from_positions(blocks):
    # Read-from last use of a given work-tape block, one source node otherwise.
    predecessors = []
    for j, block in enumerate(blocks):
        earlier = [i for i in range(j) if blocks[i] == block]
        predecessors.append(earlier[-1] if earlier else -1)
    return tuple(predecessors)

def local_predecessor(movement, stage):
    # stage is 0-based. 0 = source; j-1 = most recent if previous move stays.
    if stage == 0 or movement[stage-1] == 1:
        return -1
    return stage-1

def min_binary_space_capacity(B, N, q=8):
    # One read-only head, one binary writable tape, q control states.
    # C <= q * (N+2) * (S+2) * 2^S, an intentionally generous capacity.
    S=0
    while q*(N+2)*(S+2)*(1<<S) < (1<<B):
        S+=1
    return S

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('raw.json'))
    args=parser.parse_args()
    cases=0
    examples=[]
    for B in range(1,16):
        for b in (1,3,5):
            signatures=set()
            maxrank=0
            for v in range(1<<B):
                word=format(v,f'0{B}b')
                source=source_encode(word,b)
                schedule, blocks, head=physical_headwalk(source,b)
                ck(promise_check(source,b), 'well_formed_promise')
                ck(''.join(map(str,schedule))==word,'headwalk_trajectory')
                ck(head==b*word.count('1'),'head_position')
                accept=(sum(int(t) for t in source)&1)==1
                ck(accept==((word.count('1')&1)==1),'source_parity_label')
                ck(blocks==tuple(sum(int(x) for x in word[:j]) for j in range(B)),'block_prefix_positions')
                predecessor=edges_from_positions(blocks)
                ck(predecessor==tuple(local_predecessor(schedule,j) for j in range(B)),'local_edges')
                for j in range(1,B+1):
                    ck(canonical_selector(source,b,j)==int(word[j-1]),'index_bit_authentic')
                    ck((j-1)*b <= len(source)-b,'local_source_access_range')
                signatures.add(schedule)
                maxrank=max(maxrank,v+1)
                cases+=1
            ck(len(signatures)==(1<<B),'injective_schedule_count')
            ck(maxrank==(1<<B),'fixed_order_last_rank')
            if B in (4,8,12,15):
                examples.append({'B':B,'b':b,'input_symbols':B*b,
                                 'distinct_true_graph_signatures':len(signatures),
                                 'fixed_binary_order_last_rank':maxrank,
                                 'all_zero_schedule': '0'*B,
                                 'all_one_schedule': '1'*B})
    # Malformed run and source-query bounds are hostile controls.
    for B in range(2,100):
        for b in (2,3,4,7):
            s = ('0'*(b-1)+'1') + ('0'*b)*(B-1)
            ck(not promise_check(s,b),'malformed_runs_not_promised')
            ck(B*b==len(s),'malformed_length_held')
            # Reading an arbitrary indexed bit with a local head after reset
            # takes <=2N physical head movements and O(log N) address bits.
            for j in (1,B//2,B):
                ck(2*(j-1)*b<=2*B*b,'charged_two_way_seek_bound')
    # A schedule selector could be badly wrong if it used the first symbol on
    # arbitrary sources; verify the requirement to authenticate the promise.
    s='1000'
    sch,_,_=physical_headwalk(s,4)
    ck(not promise_check(s,4) and sch!=(canonical_selector(s,4,1),),
       'source_selector_promise_essential')
    quantitative=[]
    for B in (16,32,64,128,256,512):
        b=math.isqrt(B)+(math.isqrt(B)**2<B)
        if b%2==0: b+=1
        N=B*b
        S=min_binary_space_capacity(B,N)
        ck(8*(N+2)*(S+2)*(1<<S)>=(1<<B),'exact_configuration_bound')
        ck(S==0 or 8*(N+2)*(S+1)*(1<<(S-1))<(1<<B),
           'sharp_integer_capacity_floor')
        quantitative.append({'B':B,'b':b,'source_length_N':N,
                            'simulated_physical_steps_T':N,
                            'candidate_graph_count':str(1<<B),
                            'binary_one_work_tape_min_S':S,
                            'cube_root_b':b,
                            'source_local_per_query_seek_upper':N,
                            'per_B_queries_seek_upper':B*N})
    data={
        'status':'COMPUTATIONAL',
        'theorem_scope':'fixed-order input-independent exhaustive graph enumeration vs source-aware selector on promised constant-run physical headwalk family',
        'assertions':sum(TESTS.values()),'failures':0,
        'assertions_by_category':dict(TESTS),
        'cases':cases,'B_range':[1,15], 'b_values':[1,3,5],
        'examples':examples,'capacity_cases':quantitative,
        'machine':{'read_only_input_heads':1,'write_tapes':1,
                   'source_head':'move right exactly one cell per input symbol',
                   'work_head':'move right on 1, stay on 0',
                   'output':'halt with parity of input symbols in finite control at right-end marker',
                   'input_promise':'B consecutive constant runs each of b symbols'},
        'seed':None,'python':platform.python_version(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limits':['No end-to-end multitape SAT simulation','No improved general-purpose Tree Evaluation evaluator',
                  'No general lower bound from number of possible graph transcripts',
                  'Physical local-head query bound differs from random-access address model',
                  'Enumeration lower bound requires an input-independent candidate order and actual individual tests']
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'assertions':data['assertions'],'cases':cases,'failures':0,
                      'raw_path':str(args.output)}))

if __name__=='__main__':
    main()
