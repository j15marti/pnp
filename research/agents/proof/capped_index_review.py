#!/usr/bin/env python3
"""Independent finite audit of capped occurrence propagation; not an asymptotic solver proof."""
import itertools, json, random, signal, time, inspect, hashlib
from pathlib import Path
from capped_index_replay import CappedIndexReplaySolver
from batched_unit_replay import BatchedUnitReplaySolver

def closure(source,scope,mask,values,n):
    assignment={v:bool(values&(1<<(v-1))) for v in range(1,n+1) if mask&(1<<(v-1))}
    while True:
        forced=[]
        for cid in scope:
            clause=source[cid]
            if any(abs(x) in assignment and assignment[abs(x)]==(x>0) for x in clause): continue
            free=[x for x in clause if abs(x) not in assignment]
            if not free: return None
            if len(free)==1: forced.append(free[0])
        if not forced: return assignment
        for x in forced:
            if abs(x) in assignment and assignment[abs(x)]!=(x>0): return None
            assignment[abs(x)]=x>0

def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(25); t=time.monotonic(); rng=random.Random(90812)
    counts={'empty_clause_checks':0,'closure_checks':0,'fallback_release_checks':0,'read_counter_checks':0,'order_checks':0}
    original=BatchedUnitReplaySolver.propagate_sweeps
    def observed_fallback(self,state,anc):
        f=inspect.currentframe().f_back
        assert not f.f_locals['occurrence'] and not f.f_locals['pending'] and not f.f_locals['queued']
        counts['fallback_release_checks']+=1
        return original(self,state,anc)
    BatchedUnitReplaySolver.propagate_sweeps=observed_fallback
    class WatchedClause(tuple):
        def __iter__(self):
            for value in super().__iter__():
                observed[0]+=1
                yield value
    for budget in (0,1,100000):
        obj=CappedIndexReplaySolver(((),),0,index_budget_bits=budget)
        _,bad=obj.propagate_sweeps((None,0,0),0)
        assert bad and obj.metrics['source_literal_reads']==0
        counts['empty_clause_checks']+=1
    for case in range(400):
        n=rng.randint(1,7)
        src=tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(0,n))) for _ in range(rng.randint(0,16)))
        scope=tuple(i for i in range(len(src)) if rng.randrange(2))
        mask=rng.randrange(1<<n); values=rng.randrange(1<<n)&mask
        expected=closure(src,scope,mask,values,n)
        full=CappedIndexReplaySolver(src,n,index_budget_bits=100000)
        full.propagate_sweeps((scope,mask,values),17)
        threshold=full.metrics['index_peak_bits']
        for budget in sorted(set((0,max(0,threshold-1),threshold,threshold+1))):
            obj=CappedIndexReplaySolver(src,n,index_budget_bits=budget)
            observed=[0]; obj.source=tuple(WatchedClause(c) for c in src)
            state,bad=obj.propagate_sweeps((scope,mask,values),17)
            assert bad==(expected is None)
            if not bad:
                actual={v:bool(state[2]&(1<<(v-1))) for v in range(1,n+1) if state[1]&(1<<(v-1))}
                assert actual==expected
            met=obj.metrics
            assert met['index_peak_bits']<=budget
            assert met['source_literal_reads']==observed[0]
            assert met['source_literal_reads']==met['index_acquisition_literal_reads']+met['index_event_literal_reads']+met['unit_sweep_literal_reads']
            if met['index_successes']:
                assert met['index_event_literal_reads']<=sum(len(src[i])*(1+len(src[i])) for i in scope)
                assert met['index_occurrence_visits']<=sum(len(src[i]) for i in scope)
                assert met['index_event_clause_accesses']<=len(scope)+sum(len(src[i]) for i in scope)
                assert met['index_acquisition_literal_reads']+met['index_event_literal_reads']<=sum(len(src[i])*(len(src[i])+2) for i in scope)
                assert met['index_fallbacks']==0
            else:
                assert met['index_failed_acquisition_literal_reads']==met['index_acquisition_literal_reads']
            counts['closure_checks']+=1; counts['read_counter_checks']+=1
    for n in range(2,7):
        chain=((1,),)+tuple((-i,i+1) for i in range(1,n))
        for source in itertools.permutations(chain):
            obj=CappedIndexReplaySolver(source,n,index_budget_bits=100000)
            state,bad=obj.propagate_sweeps((None,0,0),0)
            assert not bad and state[1]==state[2]==(1<<n)-1
            assert obj.metrics['index_event_literal_reads']<=1+4*(n-1)
            counts['order_checks']+=1
    BatchedUnitReplaySolver.propagate_sweeps=original
    signal.alarm(0)
    result=dict(status='PASS',**counts,elapsed_seconds=time.monotonic()-t,candidate_sha256=hashlib.sha256(Path(__file__).with_name('capped_index_replay.py').read_bytes()).hexdigest(),limitations=['Proper clauses, unique valid scope IDs, valid preassignments.','Logical index and queue payload cap, not Python allocation cap.','Source reads and occurrence visits measured, not full machine runtime.','Inherited random-access locator and ancestor/cache payload remain separately charged.'])
    Path(__file__).with_name('capped_index_review_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
