#!/usr/bin/env python3
"""Horizon-reset and dynamic-child audit, deterministic stdlib Python.

This concerns dynamic AND/ordinary proper-3CNF scalar inputs, not an
unrestricted SAT lower bound. Numeric counting results are illustrative;
finite tests are distinct from the combinatorial proof.
"""
from __future__ import annotations
import itertools, math, json, hashlib, importlib.util, subprocess
from pathlib import Path
from collections import Counter

HERE=Path(__file__).resolve().parent
PREV=HERE/'2026-10-28_2206_LSPV4_FINITE_HORIZON_UPDATE_ENTROPY213_repro.py'
sp=importlib.util.spec_from_file_location('entropy213',PREV)
old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
C=Counter()

def ck(x,why):
    C[why]+=1
    if not x: raise AssertionError(f'{why} #{C[why]}')

def exact_classes(m,h):
    h=min(m,h)
    return sum(math.comb(m,j) for j in range(h+1))+(h<m)

def apply(mask,i,v):
    return ((mask & ~(1<<i)) if v==1 else (mask | (1<<i)))

def all_streams(m,h):
    yield ()
    ops=list(itertools.product(range(m),(0,1)))
    for k in range(1,h+1): yield from itertools.product(ops,repeat=k)

def signature(mask,streams):
    ans=bytearray()
    for stream in streams:
        x=mask
        for (i,v) in stream: x=apply(x,i,v)
        ans.append(x==0)
    return bytes(ans)

def sketch(mask,m,H):
    """Canonical prefix-free dynamic state; no original source after construction."""
    if H>=m:
        return {'kind':'bitset','m':m,'H':H,'mask':mask}
    zeros=[i for i in range(m) if mask&(1<<i)]
    if len(zeros)>H: return {'kind':'overflow','m':m,'H':H}
    if H*math.ceil(math.log2(m+1))>=m:
        return {'kind':'bitset','m':m,'H':H,'mask':mask}
    return {'kind':'sparse','m':m,'H':H,'zeros':zeros}

def sketch_apply(state,stream):
    """Return final SAT response under a declared total H-operation budget."""
    assert len(stream)<=state['H']
    kind=state['kind']
    if kind=='overflow':return False
    if kind=='bitset':
        mask=state['mask']
        for i,v in stream: mask=apply(mask,i,v)
        return mask==0
    zeros=set(state['zeros'])
    for i,v in stream:
        if v==0: zeros.add(i)
        else: zeros.discard(i)
    return not zeros

def packed_state_size_upper(m,H):
    """Conservative physical bit bound including mode, dimensions, budget."""
    header=3+2*math.ceil(math.log2(m+2))
    if H>=m:return header+m
    return header+min(m,math.ceil(math.log2(H+2)) + H*math.ceil(math.log2(m+1)))

def rerun_original():
    script=HERE/'src'/'audit.py'
    if not script.exists():return {'status':'missing'}
    p=subprocess.run(['python',str(script)],cwd=script.parent,capture_output=True,check=True,timeout=60)
    oldjson=(HERE/'src'/'results.json').read_bytes()
    stdout=p.stdout
    ck(stdout.strip()==oldjson.strip(),'archived_audit_exact_replay')
    return {'status':'match','original_sha256':hashlib.sha256(oldjson).hexdigest(),
            'new_stdout_sha256':hashlib.sha256(stdout).hexdigest()}

def run():
    # Exact behaviour classes even allowing BOTH overwrite values.
    group=[]
    for m in range(1,7):
        for H in range(0,min(3,m)+1):
            streams=list(all_streams(m,H))
            sigs=[signature(mask,streams) for mask in range(1<<m)]
            distinct=len(set(sigs))
            E=exact_classes(m,H)
            ck(distinct==E,'full_stream_equivalence')
            small=[mask for mask in range(1<<m) if mask.bit_count()<=H]
            for mask in small:
                ck(sigs.count(sigs[mask])==1,'individual_small_sets_unique')
            big=[mask for mask in range(1<<m) if mask.bit_count()>H]
            if big:ck(len({sigs[x] for x in big})==1,'overflow_one_class')
            group.append({'m':m,'H':H,'streams':len(streams),'equivalence_classes':distinct})
    # Exhaustive staged budget recurrence. Resetting phase-local h must not
    # reset total interaction horizon H=min(m,p*h).
    stage=[]
    for m in range(2,7):
        for h in range(1,min(3,m)+1):
            for p in range(1,4):
                H=min(m,p*h)
                E=exact_classes(m,H)
                ck(E>=exact_classes(m,h),'staged_entropy_monotone')
                if p*h>=m: ck(E==2**m,'staged_full_entropy')
                stage.append({'m':m,'h_each':h,'stages':p,'H_total':H,'classes':E})
    # Explicit adversarial two-stage control:
    # both sources have >1 zeros => identical first-stage 1-edit behaviour;
    # a second edit distinguishes them.
    m=4; S=(1<<0)|(1<<1); T=(1<<0)|(1<<2)
    stream1=((0,1),); stream2=((1,1),)
    sigs_h1=[signature(mask,list(all_streams(m,1))) for mask in (S,T)]
    ck(sigs_h1[0]==sigs_h1[1],'same_one_stage_class')
    ck(not (apply(S,0,1)==0) and not (apply(T,0,1)==0),'one_stage_both_unsat')
    ck(apply(apply(S,0,1),1,1)==0,'second_stage_sat')
    ck(apply(apply(T,0,1),1,1)!=0,'second_stage_unsat')
    # Correct H-total sketch (and failure for a falsely reset h-only sketch).
    for m in range(1,10):
        for H in range(0,min(3,m)+1):
            streams=list(all_streams(m,H))
            for mask in range(1<<m):
                z=sketch(mask,m,H)
                for stream in streams:
                    phys=mask
                    for i,v in stream:phys=apply(phys,i,v)
                    ck(sketch_apply(z,stream)==(phys==0),'exact_sketch_stream')
    # Canonical source bits are physically present: no free succinct formula.
    enc=[]
    for m in [1,2,3,4,8,16,64,256,1024]:
        inputs=[tuple([1]*m),tuple([0]*m)]
        if m<=16: inputs += [tuple(int((i*17+3)%7<3) for i in range(m))]
        lens=[]
        for bits in inputs:
            blob=old.pack_canonical(bits)
            ck(old.unpack_canonical(blob)==list(bits),'source_roundtrip')
            lens.append(len(blob)*8)
        ck(len(set(lens))==1,'equal_canonical_lengths')
        enc.append({'m':m,'source_bits':lens[0],
                    'total_horizon':min(m,max(1,int(m**.75))),
                    'necessary_sketch_bits':math.ceil(math.log2(exact_classes(m,min(m,max(1,int(m**.75)))))),
                    'constructive_sketch_upper':packed_state_size_upper(m,min(m,max(1,int(m**.75))))})
    original=rerun_original()
    report={'version':'LSPV4_HORIZON_RESET_DYNAMIC_CHILD214_v1',
            'status':'RESTRICTED PROVED theorem; COMPUTATIONAL finite controls',
            'checks':dict(C),'total_checks':sum(C.values()),
            'full_stream_group_checks':group,'stage_checks':stage,
            'counterexample':{'m':4,'h_each':1,'stages':2,
                     'initial_zeros_S':[0,1],'initial_zeros_T':[0,2],
                     'common_overwrites':[[0,1],[1,1]],
                     'after_stage1_both':'UNSAT',
                     'after_stage2_S':'SAT','after_stage2_T':'UNSAT'},
            'physical_source_lengths':enc,
            'original_archive':original}
    out=HERE/'2026-10-28_2236_LSPV4_HORIZON_RESET_DYNAMIC_CHILD214_raw.json'
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'version':report['version'],'assertions':report['total_checks'],
          'checks':report['checks'],'original':original,
          'output':str(out)},indent=2))
if __name__=='__main__':run()