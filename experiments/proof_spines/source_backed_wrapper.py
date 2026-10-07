#!/usr/bin/env python3
"""No retained residual CNFs: iterative prefix search over a read-only source.
Usage: python source_backed_wrapper.py OUTPUT.json
Standard library; 25-second total batch limit. Finite tests, no separation claim.
"""
import itertools as it
import json
import random
import signal
import sys
import time
import tracemalloc
import hashlib
from pathlib import Path

def scan(source, depth, values, metrics):
    """Evaluate a prefix restriction by scanning source, retaining no clause copy."""
    unresolved = False
    for clause in source:
        satisfied = False
        pending = False
        for literal in clause:
            metrics['literal_reads'] += 1
            v = abs(literal)
            if v > depth:
                pending = True
            elif bool((values >> (v-1)) & 1) == (literal > 0):
                satisfied = True
                break
        if not satisfied:
            if not pending: return False
            unresolved = True
    return None if unresolved else True

def source_solve(source, n):
    """Depth-first prefix traversal, one assignment integer and depth counter.
    No recursion stack, parent copies, residual clauses, or answer cache.
    Input has variable labels in 1..n. False branch is always visited first.
    """
    depth = values = 0
    m = dict(literal_reads=0,nodes=0,max_depth=0,retained_residual_formulas=0)
    while True:
        m['nodes'] += 1
        m['max_depth'] = max(m['max_depth'],depth)
        status = scan(source,depth,values,m)
        if status is True: return True,m
        if status is None:
            assert depth < n
            depth += 1
            continue
        # Ascend through exhausted true branches, then try the next false sibling.
        while depth and ((values >> (depth-1)) & 1):
            values &= ~(1 << (depth-1))
            depth -= 1
        if depth == 0: return False,m
        values |= 1 << (depth-1)

def materialized_solve(source,n):
    """Same prefix order, explicitly stored residual CNFs on recursive frames."""
    m=dict(literal_reads=0,nodes=0,max_depth=0,max_live_literal_slots=0)
    def walk(f,d,live):
        m['nodes']+=1;m['max_depth']=max(m['max_depth'],d)
        live+=sum(map(len,f));m['max_live_literal_slots']=max(m['max_live_literal_slots'],live)
        if not f:return True
        if () in f:return False
        assert d<n
        for value in (False,True):
            out=[]
            for c in f:
                residual=[];sat=False
                for lit in c:
                    m['literal_reads']+=1
                    if abs(lit)==d+1:
                        if (lit>0)==value:sat=True;break
                    else:residual.append(lit)
                if not sat:out.append(tuple(residual))
            child=tuple(out)
            del out
            if walk(child,d+1,live):return True
        return False
    return walk(source,0,0),m

def propagated_source_solve(source,n):
    """Streaming unit propagation plus trail undo; no full assignment snapshots."""
    mask=values=0;trail=[];decisions=[]
    m=dict(literal_reads=0,nodes=0,propagations=0,max_trail=0,max_decisions=0,
           retained_residual_formulas=0)
    def assign(v,value):
        nonlocal mask,values
        mask|=1<<(v-1)
        if value:values|=1<<(v-1)
        else:values&=~(1<<(v-1))
        trail.append(v);m['max_trail']=max(m['max_trail'],len(trail))
    while True:
        m['nodes']+=1;unit=None;first=None;conflict=False
        for clause in source:
            satisfied=False;count=0;last=None
            for literal in clause:
                m['literal_reads']+=1;v=abs(literal)
                if (mask>>(v-1))&1:
                    if bool((values>>(v-1))&1)==(literal>0):satisfied=True;break
                else:count+=1;last=literal
            if satisfied:continue
            if count==0:conflict=True;break
            if first is None:first=abs(last)
            if count==1 and unit is None:unit=last
        if not conflict:
            if first is None:return True,m
            if unit is not None:
                assign(abs(unit),unit>0);m['propagations']+=1;continue
            decisions.append((first,len(trail),False))
            m['max_decisions']=max(m['max_decisions'],len(decisions))
            assign(first,False);continue
        while decisions:
            v,mark,tried_true=decisions.pop()
            while len(trail)>mark:
                old=trail.pop();mask&=~(1<<(old-1));values&=~(1<<(old-1))
            if not tried_true:
                decisions.append((v,mark,True));assign(v,True);break
        else:return False,m

def brute(source,n):
    return any(all(any(bool((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in source)
               for a in range(1<<n))

def measure(fn,f,n):
    tracemalloc.start();start=time.perf_counter()
    answer,m=fn(f,n)
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return dict(answer=answer,seconds=time.perf_counter()-start,
                incremental_python_peak_bytes=peak,**m)

def cases():
    clauses=[tuple((i+1)*s for i,s in enumerate(signs)) for signs in it.product((-1,1),repeat=3)]
    for subset in range(256):
        yield 'exhaustive3',subset,3,tuple(c for i,c in enumerate(clauses) if (subset>>i)&1)
    rng=random.Random(20261007)
    for n in (6,8,10):
        for seed in range(4):
            yield 'random',seed,n,tuple(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(4*n))
    for n in (12,24,48):
        yield 'positive_units',0,n,tuple((v,) for v in range(1,n+1))
        yield 'negative_units',0,n,tuple((-v,) for v in range(1,n+1))
        yield 'independent3',0,n,tuple(tuple(range(v,v+3)) for v in range(1,n+1,3))
    # Easy UNSAT, but prefix order postpones its two contradictory clauses.
    # Tautologies ensure all earlier variable names actually occur.
    for n in (8,10,12):
        yield 'late_contradiction',0,n,tuple((v,-v) for v in range(1,n))+((n,),(-n,))

def delayed_audit():
    # Exact Search-G test: record is an eight-bit deterministic source function.
    # Fresh three-bit challenge chooses a coordinate after a two-bit commitment.
    records={x:((x*73+19)%256) for x in range(256)}
    conflicts=checks=0
    groups={}
    for x,y in records.items():groups.setdefault(y&3,[]).append((x,y))
    for group in groups.values():
        for (_,y),(_,z) in it.combinations(group,2):
            assert y!=z and any(((y>>j)&1)!=((z>>j)&1) for j in range(8))
            conflicts+=1
    for x,y in records.items():
        for challenge in range(8):
            # No retained y: reread x and regenerate the same deterministic record.
            regenerated=(x*73+19)%256
            assert ((regenerated>>challenge)&1)==((y>>challenge)&1)
            checks+=1
    return dict(records=256,challenges_per_record=8,retained_bits=2,
                distinguishable_pairs_with_same_commitment=conflicts,
                post_revelation_recomputation_checks=checks,errors=0,
                scope='Toy deterministic-record countermodel, not an arbitrary SAT lower bound.')

def deadline(*args):raise TimeoutError('Split batch: 25-second limit reached')

if __name__=='__main__':
    signal.signal(signal.SIGALRM,deadline);signal.alarm(25)
    started=time.perf_counter();rows=[]
    for family,seed,n,f in cases():
        a=measure(source_solve,f,n);b=measure(materialized_solve,f,n)
        c=measure(propagated_source_solve,f,n)
        expected=brute(f,n) if n<=12 else True
        assert a['answer']==b['answer']==c['answer']==expected,(family,seed)
        assert a['nodes']==b['nodes'],(family,seed,'Traversal mismatch')
        rows.append(dict(family=family,seed=seed,n=n,source_literals=sum(map(len,f)),
                         regenerated=a,materialized=b,propagated=c))
    out=dict(status='COMPUTATIONAL',cases=len(rows),answer_comparison_checks=3*len(rows),
             matched_prefix_traversal_checks=len(rows),
             errors=0,seconds=time.perf_counter()-started,rows=rows,delayed_audit=delayed_audit(),
             runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             limitations=['Read-only source input allocated before tracemalloc; parser/input conversion not included.',
              'Assignment counter needs O(n) bits, not generally N^o(1).',
              'Source rescans charged as literal reads; Python timing is not a target-machine theorem.',
              'Matched prefix pair omits unit propagation; third backend uses streaming units and trail undo.',
              'Propagation backend retains O(n) trail/decision records of O(log n) bits each.',
              'Full worst-case search can remain exponential.'])
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
