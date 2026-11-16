#!/usr/bin/env python3
"""TMR-3/055: canonical, source-authenticated circuit evaluator with public work-head sweeps.

Program is self-contained, Python 3.10+, no packages. One invocation designed <30s.
The exhaustive/seeded tests validate finite construction identities, not P-completeness
or any new uniform time-space simulation theorem.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

SEED=20261115
REVISION='tmr3-canonical-cvp055-v1'
COUNTS=Counter()

def verify(q:bool,label:str):
    if not q: raise AssertionError(label)
    COUNTS[label]+=1

def enc(gates):
    n=len(gates)
    assert n>=1
    parts=['1'*n+'0']
    for j,(op,a,b) in enumerate(gates):
        assert op in (0,1,2,3)
        if op in (0,1):
            assert a is None and b is None
        else:
            assert a is not None and b is not None and 0<=a<j and 0<=b<j
        parts.append(f'{op:02b}')
        parts.append(''.join('1' if a==i else '0' for i in range(n)))
        parts.append(''.join('1' if b==i else '0' for i in range(n)))
    result=''.join(parts)
    assert len(result)==2*n*n+3*n+1
    return result

def dec(src:str):
    if not src or any(c not in '01' for c in src): raise ValueError('nonbinary')
    n=0
    while n<len(src) and src[n]=='1': n+=1
    if n<1 or n>=len(src) or src[n]!='0': raise ValueError('header')
    if len(src)!=2*n*n+3*n+1: raise ValueError('length')
    p=n+1; out=[]
    for j in range(n):
        op=int(src[p:p+2],2); p+=2
        sa=src[p:p+n]; p+=n
        sb=src[p:p+n]; p+=n
        if op in (0,1):
            if '1' in sa+sb: raise ValueError('constant masks')
            out.append((op,None,None));continue
        a=[i for i,c in enumerate(sa) if c=='1']
        b=[i for i,c in enumerate(sb) if c=='1']
        if len(a)!=1 or len(b)!=1 or a[0]>=j or b[0]>=j:
            raise ValueError('invalid gate references')
        out.append((op,a[0],b[0]))
    verify(p==len(src),'full_input_parse')
    return out

def expected(gates):
    vals=[]
    for op,a,b in gates:
        if op<2: value=op
        elif op==2: value=vals[a]&vals[b]
        else: value=vals[a]|vals[b]
        vals.append(value)
    return vals

def sweep(n:int):
    """Value-tape head visit sequence, independent of every gate value and mask.

    Stage j begins at the previous write location j-1 (or 0 for first stage).
    First reset to zero, then scan 0..n-1, then seek j for one write.
    """
    cur=0; trace=[]; stages=[]
    for j in range(n):
        positions=[]
        while cur>0:
            cur-=1; positions.append(cur)
        positions.append(cur)
        while cur<n-1:
            cur+=1;positions.append(cur)
        while cur!=j:
            cur+=1 if cur<j else -1;positions.append(cur)
        trace.extend(positions)
        stages.append(positions)
    return stages,trace

def _authenticate_header(src: str) -> int:
    if not src or any(c not in '01' for c in src): raise ValueError('nonbinary')
    n=0
    while n<len(src) and src[n]=='1':n+=1
    if n<1 or n>=len(src) or src[n]!='0': raise ValueError('header')
    if len(src)!=2*n*n+3*n+1: raise ValueError('length')
    return n

def _record(src:str,n:int,j:int):
    """On-demand view of ONE source record, not an in-memory gate table."""
    p=n+1+j*(2+2*n)
    op=int(src[p:p+2],2)
    sa=src[p+2:p+2+n]
    sb=src[p+2+n:p+2+2*n]
    if op<2:
        if '1' in sa+sb:raise ValueError('bad constant masks')
    else:
        apos=[i for i,c in enumerate(sa) if c=='1']
        bpos=[i for i,c in enumerate(sb) if c=='1']
        if len(apos)!=1 or len(bpos)!=1 or apos[0]>=j or bpos[0]>=j:
            raise ValueError('invalid gate references')
    return op,sa,sb

def interp(src):
    n=_authenticate_header(src)
    # A valid-source prepass checks every record, retaining only a row/counter.
    for j in range(n):_record(src,n,j)
    vals=[0]*n; out=[]; workreads=0;workwrites=0;headmoves=0;cur=0
    stages=[]
    for j in range(n):
        # The authenticated gate record is recovered from immutable source afresh.
        op,sa,sb=_record(src,n,j)
        trace=[]
        while cur>0:
            cur-=1;trace.append(cur);headmoves+=1
        v1=v2=0
        trace.append(0)
        for i in range(n):
            value=vals[i]
            workreads+=1
            if sa[i]=='1': v1=value
            if sb[i]=='1': v2=value
            if i<n-1:
                cur+=1;trace.append(cur);headmoves+=1
        while cur!=j:
            cur+=1 if cur<j else -1;trace.append(cur);headmoves+=1
        if op<2:value=op
        elif op==2:value=v1&v2
        else:value=v1|v2
        vals[j]=value;workwrites+=1;out.append(value)
        stages.append(trace)
    return {'output':out[-1],'values':out,'stages':stages,
            'data_reads':workreads,'data_writes':workwrites,'head_moves':headmoves,
            'data_space_cells':n,
            'source_bytes':len(src),
            'source_head_move_upper':2*n*len(src)+2*len(src)}

def generic_eval(g):
    vals=[]
    for rec in g:
        k=rec[0]
        if k=='c':v=rec[1]
        elif k=='not':v=1-vals[rec[1]]
        elif k=='and':v=vals[rec[1]] & vals[rec[2]]
        elif k=='or':v=vals[rec[1]] | vals[rec[2]]
        else:raise ValueError(k)
        vals.append(v)
    return vals[-1]

def dualrail(g):
    out=[];rails=[]
    def const(v):out.append((v,None,None));return len(out)-1
    def binary(op,a,b):out.append((op,a,b));return len(out)-1
    for rec in g:
        op=rec[0]
        if op=='c':
            t=const(rec[1]);f=const(1-rec[1])
        elif op=='not':
            a=rails[rec[1]]
            t=binary(2,a[1],a[1]);f=binary(2,a[0],a[0])
        elif op in ('and','or'):
            a=rails[rec[1]];b=rails[rec[2]]
            t=binary(2 if op=='and' else 3,a[0],b[0]);f=binary(3 if op=='and' else 2,a[1],b[1])
        rails.append((t,f))
    binary(2,rails[-1][0],rails[-1][0])
    return out

def run():
    rng=random.Random(SEED)
    source_cases=0;general_cases=0
    for n in range(1,13):
        stage_template,_=sweep(n)
        for trial in range(96):
            gates=[]
            for j in range(n):
                op=rng.randrange(4) if j else rng.randrange(2)
                if op<2:gates.append((op,None,None))
                else:gates.append((op,rng.randrange(j),rng.randrange(j)))
            src=enc(gates);a=interp(src);want=expected(gates)
            verify(a['values']==want,'authentic_gate_values')
            verify(a['output']==want[-1],'actual_output')
            verify(a['stages']==stage_template,'data_head_schedule_independent')
            verify(a['data_reads']==n*n,'data_reads_paid')
            verify(a['data_writes']==n,'data_writes_paid')
            verify(a['head_moves']==2*n*n-3*n+1,'data_head_move_formula')
            verify(a['data_space_cells']==n,'same_run_data_storage')
            verify(a['source_bytes']==2*n*n+3*n+1,'complete_input_bit_length')
            source_cases+=1
        # source lengths equal; graph schedule identical for oppositely answered values
        zero=enc([(0,None,None)]*n)
        one=enc([(1,None,None)]*n)
        z=interp(zero);o=interp(one)
        verify(z['stages']==o['stages'] and z['output']==0 and o['output']==1,'same_graph_opposite_labels')

    for n in range(1,15):
        for trial in range(80):
            g=[]
            for j in range(n):
                op=rng.choice(['c','c','not','and','or']) if j else 'c'
                if op=='c':g.append(('c',rng.randrange(2)))
                elif op=='not':g.append((op,rng.randrange(j)))
                else:g.append((op,rng.randrange(j),rng.randrange(j)))
            v=generic_eval(g)
            mono=dualrail(g)
            s=enc(mono)
            result=interp(s)
            verify(result['output']==v,'general_circuit_dualrail_logspace_reduction')
            verify(result['values']==expected(mono),'dualrail_internal_values')
            verify(result['data_reads']==len(mono)**2,'reduced_head_scan_cost')
            general_cases+=1
    src=enc([(0,None,None),(1,None,None),(2,0,1)])
    # forged mask with two 1s on a binary gate
    bad=list(src)
    n=3;idx=n+1+2*(2+2*n)+2
    bad[idx]='1';bad[idx+1]='1'
    negatives=["", "0", "111", "2", src+"0",src[:-1], ''.join(bad), '00'+src]
    for badword in negatives:
        try:interp(badword)
        except ValueError:COUNTS['malformed_rejected']+=1
        else:raise AssertionError('malformed accepted')
    output={
        'revision':REVISION, 'status':'COMPUTATIONAL', 'seed':SEED,
        'source_program_instances':source_cases,
        'general_circuit_reduction_instances':general_cases,
        'malformed_rejections':len(negatives),
        'assertions':sum(COUNTS.values()),'by_category':dict(COUNTS),
        'failures':0,
        'theorem_not_computationally_proved':'P-completeness uses the classical logspace CVP theorem and symbolic reduction, not finite tests',
        'same_model_ledger':{'input_bits':'N=2n^2+3n+1','value_tape_reads':'n^2','value_tape_writes':'n','value_head_moves':'2n^2-3n+1','source_seek_upper':'2nN+2N','sequential_work_time':'O(n^3 log(n+2)) conservative','writable_space':'O(n+log n) bits, including n stored values'},
        'limitations':['Macro data-head trajectory independence only, not the full tape-head vector',
                       'No reduction from general CVP implemented in native finite TM microcode',
                       'P-hardness corollary is conditional on the standard logspace reduction theorem',
                       'Does not prove L is different from P or a generic space lower bound',
                       'Not an improved evaluator for arbitrary-height nonassociative Tree Evaluation']
    }
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('raw.json'));args=p.parse_args()
    result=run()
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'
')
    print(json.dumps({k:result[k] for k in ('assertions','failures','source_program_instances','general_circuit_reduction_instances','malformed_rejections')},indent=2))
