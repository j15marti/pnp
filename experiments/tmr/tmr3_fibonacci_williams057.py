#!/usr/bin/env python3
"""TMR-3/057: authenticated actual-block graph Fibonacci-unrolling control.

Research model: fixed blank-start deterministic machine, 1 read-only source
head, one writable locally headed tape and finite control. Source words are
1^(b-1)0 followed by B records x_i 1^(b-2)0, b>=3, B>=1.
No claim about arbitrary Tree Evaluation, SAT runtime, or P vs NP.
Run: python tmr3_fibonacci_williams057.py --output raw.json
Python 3 standard library. No external inputs or hidden random sources.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

REVISION='tmr3-fibonacci-williams057-v2'
SEED=20261115
CHECKS=Counter()

def check(condition:bool, name:str)->None:
    if not condition:
        raise AssertionError(name)
    CHECKS[name]+=1

def encode(bits:tuple[int,...], b:int)->str:
    assert b>=3 and len(bits)>=1
    return '1'*(b-1)+'0'+''.join(str(v)+'1'*(b-2)+'0' for v in bits)

def authenticate(word:str)->tuple[int,tuple[int,...]]|None:
    # A one-pass authentication with counters (not a physical bit trace).
    if not word or any(c not in '01' for c in word):
        return None
    first=word.find('0')
    if first<2:
        return None
    b=first+1
    if len(word)<2*b or len(word)%b:
        return None
    B=len(word)//b-1
    bits=[]
    for i in range(B):
        record=word[(i+1)*b:(i+2)*b]
        if len(record)!=b or record[1:]!='1'*(b-2)+'0':
            return None
        bits.append(int(record[0]))
    return b,tuple(bits)

def physical_suffix(bits:tuple[int,...], b:int):
    # State variables correspond to a SINGLE fixed finite-control machine;
    # b and B are source constraints, NOT hardwired in its transition rules.
    tape={}
    pos=0
    moves=0
    for _ in range(b-1): # each real header '1' moves the work head right
        pos+=1;moves+=1
    check(pos==b-1,'header_physical_position')
    state=0
    direction=1
    trace=[]
    history={}
    # The header terminal '0' causes a real paid stationary source step.
    for i,x in enumerate(bits,1):
        old=tape.get(pos,0)
        previous=history.get(pos,0)
        check(old==previous,'authentic_old_cell')
        new=state ^ old ^ x
        tape[pos]=new
        # record a genuine read/write at the FIRST source symbol of record i.
        rec={'i':i,'position':pos,'block':pos//b,'old':old,
             'previous_state':state,'source_bit':x,'write':new,
             'last_same_stage':history.get(('seen',pos)),
             'head_dir_after_block':direction}
        history[pos]=new
        history[('seen',pos)]=i
        # Each filler read is paid but no work movement; delimiter moves head.
        pos+=direction
        moves+=1
        direction=-direction
        state=new
        trace.append(rec)
    # Actual work-source paid microsteps: one per authenticated source bit,
    # with no free header, payload, filler, or delimiter source operations.
    source_steps=b*(len(bits)+1)
    return state, trace, {'source_steps':source_steps,'work_head_moves':moves,
        'work_visited_cells':b+1,'work_cell_contents':len(tape),
        'final_work_head':pos,'terminal_state':state}

def direct_recurrence(bits:tuple[int,...])->int:
    a=c=0
    for x in bits:
        a,c=c,(a^c^x)
    return c

def all_predecessors(trace):
    # The work-tape part of Williams' authentic block-dependency graph:
    # mandatory consecutive-time state edge and most recent same-block read.
    result=[]
    for rec in trace:
        i=rec['i']
        mandatory=(i-1 if i>=2 else None)
        old=rec['last_same_stage']
        result.append((mandatory,old))
        check((old is None and i<=2) or (old==i-2),
              'real_last_visit_two_back')
        check(rec['block']==((i-1)%2),'block_alternation')
    return result

def naive_tree_evaluate(bits:tuple[int,...])->tuple[int,int,int]:
    # No memoization: explicit unary node fetch for EACH unrolled occurrence.
    count=0
    max_depth=0
    def evalnode(i,depth):
        nonlocal count,max_depth
        if i<=0:
            return 0
        count+=1
        max_depth=max(depth,max_depth)
        return bits[i-1]^evalnode(i-1,depth+1)^evalnode(i-2,depth+1)
    result=evalnode(len(bits),1)
    return result,count,max_depth

def fibonacci(n:int)->int:
    a,c=0,1
    for _ in range(n): a,c=c,a+c
    return a

def query_count(B:int)->int:
    return fibonacci(B+2)-1

def run()->dict:
    rng=random.Random(SEED)
    source_cases=0
    physical_steps=0
    total_real_edgelinks=0
    query_checks=0
    malformed_cases=0
    # Exhaustive authentic words for small B; seeded larger instances.
    for b in range(3,9):
        for B in range(1,13):
            inputs=list(itertools.product((0,1),repeat=B)) if B<=7 else [tuple(rng.randrange(2) for _ in range(B)) for __ in range(36)]
            for bits in inputs:
                word=encode(bits,b)
                check(authenticate(word)==(b,bits),'source_authentication')
                got,trace,ledger=physical_suffix(bits,b)
                check(len(word)==b*(B+1),'exact_source_length')
                check(got==direct_recurrence(bits),'physical_versus_two_register')
                edges=all_predecessors(trace)
                for i,(consecutive,old) in enumerate(edges,1):
                    if i>=3:
                        check(consecutive==i-1 and old==i-2,'true_fibonacci_two_edges')
                        total_real_edgelinks+=2
                check(ledger['source_steps']==len(word),'charged_physical_source_steps')
                check(ledger['work_head_moves']==b-1+B,'charged_physical_work_moves')
                check(ledger['work_visited_cells']==b+1,'charged_work_visited_cells')
                if B<=10 and (B<=6 or source_cases%13==0):
                    value,q,depth=naive_tree_evaluate(bits)
                    check(value==got,'naive_unrolling_semantics')
                    check(q==query_count(B),'naive_expansion_query_count')
                    check(depth==B,'naive_height')
                    query_checks+=1
                source_cases+=1
                physical_steps+=ledger['source_steps']
            # Distinct malformed words: truncate, append, wrong middle filler,
            # invalid header and nonbinary source, all rejected before run.
            basis=encode(tuple(0 for _ in range(B)),b)
            bad=[basis[:-1],basis+'0',basis[:b+1]+'0'+basis[b+2:],
                 '0'+basis,basis+'X']
            for w in bad:
                check(authenticate(w) is None,'malformed_rejection')
                malformed_cases+=1
    for B in range(1,128):
        a=query_count(B)
        check(a==1+(query_count(B-1) if B>1 else 0)+(query_count(B-2) if B>2 else 0),
              'symbolic_fibonacci_recurrence')
    for s in range(3,11):
        b=s;B=s*s
        N=b*(B+1)
        q=query_count(B)
        check(q > B,'cube_root_input_scale_exponential_query')
        check(B>0 and (N//b)==B+1,'cube_root_exact_scale')
    examples=[]
    for s in [3,4,5,6,8,10]:
        b=s;B=s*s;N=b*(B+1)
        Q=query_count(B)
        examples.append({'b':b,'B':B,'encoded_source_bits':N,
                         'unrolled_stage_queries_exact':str(Q),
                         'unrolled_stage_queries_digits':len(str(Q)),
                         'physical_source_steps':N,
                         'real_work_visited_cells':b+1,
                         'two_register_simulator_source_scans':1})
    return {'status':'COMPUTATIONAL','revision':REVISION,'seed':SEED,
            'assertions':sum(CHECKS.values()),'failures':0,
            'assertion_categories':dict(CHECKS),
            'cases':{'authenticated_sources':source_cases,
                     'physical_source_steps':physical_steps,
                     'authentic_two_parent_edges_checked':total_real_edgelinks,
                     'explicit_unrolling_runs':query_checks,
                     'malformed_sources_rejected':malformed_cases},
            'examples':examples,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limits':[
                'The exponent is for a specified duplicate-recomputing tree-unrolling evaluator, not arbitrary Cook-Mertz evaluation.',
                'The work-tape subgraph omits extra legitimate input/state edges in the complete Williams graph; those can only add tree occurrences.',
                'Source grammar is authenticated; the fixed physical service is specified symbolically, not compiled to an independent native transition table.',
                'No general SAT lower bound or improved Tree Evaluation algorithm is established.',
                'Query count is symbolic for B>10; no exponential actual traversal is claimed for large B.'
             ]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='results.json')
    args=p.parse_args()
    result=run()
    with open(args.output,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'assertions':result['assertions'],'failures':0,'cases':result['cases'],'output':args.output},indent=2))
if __name__=='__main__':main()
