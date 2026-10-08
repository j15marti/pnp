#!/usr/bin/env python3
"""Run an orbit prefilter inside the byte-verified historical double wrapper.
No historical file is modified. Every global substitution is restored.
This tests actual integration, independently of the controlled clause-first variant.
The old size/literal counters are retained and explicitly not called machine bounds.
"""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib.util
import json
import signal
import sys
import time
import tracemalloc
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import orbit_first_wrapper as orb

BASE=ROOT/'vendor/double_wrapper.py'
body=BASE.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
assert blob=='04cf06305b5beff2a36f631e4a38b5e09553c1ee', 'historical source drift'
spec=importlib.util.spec_from_file_location('verified_double_wrapper',BASE)
old=importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
ORIGINAL_SIMPLIFY=old.simplify
ORIGINAL_INNER=old.inner
ROWS=[]

def install(mode, extra, plan_stats):
    def adapted(f,m):
        f=ORIGINAL_SIMPLIFY(f,m)
        if mode=='pure':
            return orb.simplify(orb.canon(f),extra)
        if mode=='orbit_stream':
            return orb.stream_fix(orb.canon(f),extra)
        return f
    def counted(*args,**kwargs):
        plan=ORIGINAL_INNER(*args,**kwargs)
        for key in ('intern_calls','cache_reuses','stored_formula_bits','leaf_count','gates'):
            plan_stats[key]+=plan['metrics'][key]
        assert all(old.size(node['formula'])<=plan['metrics']['target_bits']
                   for node in plan['nodes'] if node['type']=='LEAF')
        plan_stats['verified_leaf_cutoff_plans']+=1
        return plan
    old.simplify=adapted; old.inner=counted

def run(f,mode,memory=False,do_inner_check=False,expected=None):
    extra=Counter(); ps=Counter()
    old.reference.cache_clear(); old.prime_list.cache_clear()
    if memory: gc.collect()
    install(mode,extra,ps)
    if memory: tracemalloc.start()
    begin=time.monotonic()
    try:
        answer,metrics=old.outer(f,'components')
        elapsed=time.monotonic()-begin
        peak=tracemalloc.get_traced_memory()[1] if memory else None
        if expected is not None: assert answer==expected
        result={'answer':answer,'seconds':elapsed,'outer_metrics':metrics,
                'plan_metrics':dict(ps),'prefilter_metrics':dict(extra)}
        if memory: result['incremental_python_peak_bytes']=peak
        if do_inner_check:
            plan=old.inner(f,'components')
            assert old.evaluate(plan,old.reference)==expected
            result['inner_answer_check']=True
        return result
    finally:
        if memory and tracemalloc.is_tracing(): tracemalloc.stop()
        old.simplify=ORIGINAL_SIMPLIFY; old.inner=ORIGINAL_INNER

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--suite',choices=('controls','php'),required=True)
    p.add_argument('--holes',type=int,default=5)
    p.add_argument('--memory',action='store_true')
    p.add_argument('--start',type=int,default=0)
    p.add_argument('--stop',type=int,default=100000)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    out={'run_id':'ARC-0005-ORBIT','base_git_blob':blob,
         'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'prefilter_sha256':hashlib.sha256(Path(orb.__file__).read_bytes()).hexdigest(),
         'suite':args.suite,'case_range':[args.start,args.stop],'status':'RUNNING','cases':ROWS,
         'comparison':'Byte-verified original outer/inner in components mode; original vs pure-only vs orbit-stream prefilter',
         'memory_scope':'Tracemalloc incremental Python allocations; source preallocated, caches cleared and GC collected before each mode; not RSS or an asymptotic work-space theorem.'}
    try:
        if args.suite=='controls':
            cases=list(old.cases())[args.start:args.stop]
        else:
            cases=[(f'PHP_{p}_{args.holes}',0,old.php(p,args.holes)) for p in (args.holes,args.holes+1)]
        for name,seed,f in cases:
            orb.guard()
            expected=old.reference(old.normalize(f)) if args.suite=='controls' else int(name.split('_')[1])<=args.holes
            row={'family':name,'seed':seed,'expected':bool(expected),'input_proxy_bits':old.size(old.normalize(f)),
                 'input_dimacs_bits':orb.bits(orb.normalize(orb.canon(f)))}
            ROWS.append(row) # Partial record survives a budget exit.
            for mode in ('original','pure','orbit_stream'):
                row[mode]=run(f,mode,args.memory,args.suite=='controls',expected)
        out['status']='PASS'
        out['completed_cases']=len(ROWS)
        out['answer_checks']=len(ROWS)*3*(2 if args.suite=='controls' else 1)
    except orb.BudgetExceeded as e:
        out['status']='BLOCKED_BUDGET'; out['error']=str(e)
    except Exception as e:
        out['status']='FAIL'; out['error']=repr(e)
        raise
    finally:
        out['elapsed_seconds']=time.monotonic()-orb.START
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
    if args.suite=='php':
        for row in ROWS: print(json.dumps(row,sort_keys=True))
    return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
