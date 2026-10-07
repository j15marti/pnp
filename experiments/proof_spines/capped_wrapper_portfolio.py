#!/usr/bin/env python3
"""Executable capped-restart double-wrapper portfolio and beacon controls.
Linux research prototype, Python standard library. No asymptotic bound claimed.
Usage: python capped_wrapper_portfolio.py test SOURCE.py OUTPUT.json
       python capped_wrapper_portfolio.py beacon OUTPUT.json
Each test batch has a 25-second alarm; child attempts have a 2-second timeout.
"""
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import random
import resource
import signal
import subprocess
import sys
import time

def load_source(path):
    spec = importlib.util.spec_from_file_location('wrapper', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class FuelExceeded(Exception):
    pass

def worker(source, mode, fuel, cap_mib):
    # Enforced address-space ceiling includes Python, imports and input storage.
    cap = int(cap_mib)*1024*1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    count = 0
    started = time.perf_counter()
    status, answer, metrics = 'error', None, None
    def trace(frame, event, arg):
        nonlocal count
        if event == 'line':
            count += 1
            if count > int(fuel): raise FuelExceeded()
        return trace
    try:
        w = load_source(source)
        f = json.loads(sys.stdin.read())
        def prohibited(*args): raise AssertionError('Reference SAT called in production')
        w.reference = prohibited
        sys.settrace(trace)
        if mode == 'memory_hostile':
            # Semantically inert if it succeeds; intentional over-cap allocation.
            unused = bytearray(cap*2)
            answer, metrics = w.outer(f, 'flat')
        else:
            answer, metrics = w.outer(f, mode)
        status = 'answer'
    except FuelExceeded:
        status = 'fuel_cap'
    except MemoryError:
        status = 'memory_cap'
    except Exception as exc:
        status = 'error:' + type(exc).__name__
    finally:
        sys.settrace(None)
    print(json.dumps(dict(status=status, answer=answer, line_events=count,
        solve_seconds=time.perf_counter()-started,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        address_cap_mib=int(cap_mib), mode=mode, metrics=metrics)))

def attempt(source, f, mode, fuel, cap=64):
    started = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, __file__, 'worker', str(source), mode,
                            str(fuel), str(cap)], input=json.dumps(f),
                           text=True, capture_output=True, timeout=2)
        if p.returncode: r = dict(status='process_failure', returncode=p.returncode)
        else: r = json.loads(p.stdout)
    except subprocess.TimeoutExpired:
        r = dict(status='wall_timeout')
    r.update(total_seconds=time.perf_counter()-started, fuel=fuel, mode=mode)
    return r

def reference(f):
    vs = sorted({abs(x) for c in f for x in c})
    return any(all(any(a[abs(x)] == (x>0) for x in c) for c in f)
               for values in itertools.product((False,True), repeat=len(vs))
               for a in [dict(zip(vs,values))])

def portfolio(source, f):
    attempts=[]
    for fuel in (64,256,1024,4096,16384,65536):
        for mode in ('memory_hostile','flat','components','separator_fast'):
            r=attempt(source,f,mode,fuel);attempts.append(r)
            if r['status']=='answer':
                return dict(answer=r['answer'],winner=mode,attempts=attempts,
                            total_seconds=sum(a['total_seconds'] for a in attempts),
                            total_recorded_line_events=sum(a.get('line_events',0) for a in attempts))
    return dict(answer=None,winner=None,attempts=attempts)

def run_test(source):
    w=load_source(source);rng=random.Random(20261007)
    cases=[('empty',()),('contradiction',((1,),(-1,))),
           ('independent',((1,2,3),(4,5,6))),('PHP_4_3',w.php(4,3)),
           ('xor_sat',w.xor_triangle(False)),('xor_unsat',w.xor_triangle(True))]
    for seed in range(4):
        f=tuple(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,9),3)) for _ in range(32))
        cases.append(('random8_'+str(seed),f))
    rows=[]
    for name,f in cases:
        expected=reference(f)
        direct=[]
        for mode in ('flat','components','separator_fast'):
            r=attempt(source,f,mode,4000000)
            assert r['status']=='answer' and r['answer']==expected and r['line_events']>0,(name,r)
            direct.append(r)
        r=portfolio(source,f)
        assert r['answer']==expected,(name,r)
        assert all(a.get('answer') is None for a in r['attempts'] if a['status']!='answer')
        rows.append(dict(name=name,expected=expected,direct=direct,portfolio=r))
    return dict(status='COMPUTATIONAL',cases=len(rows),correctness_checks=4*len(rows),
        errors=0,rows=rows,source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        limitations=['Fixed 64 MiB OS address-space ceiling is not an asymptotic sublinear-space proof.',
          'Python line-event fuel omits C builtin costs; wall time includes imports, startup and discarded attempts.',
          'Only one solver child process is live; parent, OS and output logs are additional memory.',
          'Finite fuel schedule may return unknown; cap failures never mean UNSAT.',
          'No arbitrary-SAT favorable-member theorem established.'])

def beacon():
    # Exhaustive independent 4-bit block model, not a claim about a physical beacon.
    rows=[]
    for r1,r2 in itertools.product(range(16),repeat=2):
        committed=('source-A',1)  # Fixed before either challenge.
        transcript=(committed,r1,r1^3,r2,(r1^3)^r2)
        # Passive wait-and-copy can reproduce a revealed transcript.
        copied=(committed,r1,r1^3,r2,(r1^3)^r2)
        assert copied==transcript
        wrong=((committed[0],0),)+transcript[1:]
        assert wrong!=transcript
        # If token identity is existentially free, a different token has an extension.
        other=r1^1
        assert other!=r1 and (other^3)^r2 in range(16)
        rows.append([r1,r2])
    # Search-G coordinate audit: four-bit record, two retained bits, future index.
    signatures={x:tuple((x>>j)&1 for j in range(4)) for x in range(16)}
    collisions=0
    for x,y in itertools.combinations(range(16),2):
        if (x&3)==(y&3):
            assert signatures[x]!=signatures[y]
            collisions+=1
    rereads=0
    for x in range(16):
        for j in range(4):
            assert ((x>>j)&1)==signatures[x][j]
            rereads+=1
    return dict(status='COMPUTATIONAL',exhaustive_two_block_histories=len(rows),
        pre_revelation_fixed_guess_successes=1,possible_first_tokens=16,
        passive_post_revelation_reproductions=len(rows),
        fixed_identity_wrong_commitments_rejected=len(rows),
        existential_alternative_token_extensions=len(rows),
        distinct_coordinate_response_signatures=len(set(signatures.values())),
        two_bit_retention_collisions=collisions,one_probe_reread_successes=rereads,
        finding='Freshness and exact identity can be enforced in a protocol; neither test forces SAT computation or a SAT cost lower bound.',
        limitations=['Protocol countermodels only, not a implementation of every historical bitstream design.',
                     'No cryptographic hash binding or factoring hardness assumed.',
                     'Environmental waiting time is not a standard deterministic SAT computation bound.'])

def deadline(*args): raise TimeoutError('25-second batch budget; split cases')

if __name__=='__main__':
    if sys.argv[1]=='worker': worker(*sys.argv[2:])
    else:
        signal.signal(signal.SIGALRM,deadline);signal.alarm(25)
        start=time.perf_counter()
        data=run_test(Path(sys.argv[2]).resolve()) if sys.argv[1]=='test' else beacon()
        data['seconds']=time.perf_counter()-start
        data['runner_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        Path(sys.argv[-1]).write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({k:v for k,v in data.items() if k!='rows'},indent=2))
