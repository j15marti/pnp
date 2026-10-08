#!/usr/bin/env python3
"""Bounded source-occurrence unit replay; logical packed payload, not Python RSS.

Acquisition indexes only clause IDs, never residual CNFs. A budget reserves the
entire possible queue and its membership bits before indexing. Failed acquisition
is charged and discarded before the inherited sweep fallback. Full index is
rebuilt on every propagation invocation. Random access source locator costs are
inherited; event clause probes are not a sequential-source implementation.
"""
import itertools
import json
import random
import signal
import time
from collections import deque
from pathlib import Path
from batched_unit_replay import BatchedUnitReplaySolver, _base

class CappedIndexReplaySolver(BatchedUnitReplaySolver):
    def __init__(self, *args, index_budget_bits=0, **kwargs):
        super().__init__(*args, **kwargs)
        if index_budget_bits < 0: raise ValueError('negative index budget')
        self.index_budget_bits = index_budget_bits
        for key in ('attempts','successes','fallbacks','acquisition_literal_reads',
                    'acquisition_clause_accesses','event_literal_reads','event_clause_accesses',
                    'occurrence_visits','queue_pushes','assignments','peak_bits',
                    'failed_acquisition_literal_reads'):
            self.metrics['index_'+key]=0

    def propagate_sweeps(self, state, ancestor_live_bits):
        self.metrics['index_attempts'] += 1
        scope, mask, values = state
        cw, vw = self.clause_index_width, self.variable_width
        pw = max(1,(2*self.n*self.m+1).bit_length())
        # Packed queue entries and one source-ID membership bit per clause.
        reserve = self.m*(cw+1)
        header = vw+1+3*pw
        entry = cw+pw
        scratch = 8*max(1,self.n)+12*(cw+vw+pw)+16
        live = ancestor_live_bits+self.descriptor_bits(state)
        self.update_live(live,scratch)
        occurrence={}; pending=deque(); queued=set(); used=reserve
        initial_reads=self.metrics['index_acquisition_literal_reads']
        def charge():
            self.metrics['index_peak_bits']=max(self.metrics['index_peak_bits'],used)
            self.update_live(live,scratch+used)
        def fallback():
            occurrence.clear(); pending.clear(); queued.clear()
            self.metrics['index_fallbacks'] += 1
            self.metrics['index_failed_acquisition_literal_reads'] += self.metrics['index_acquisition_literal_reads']-initial_reads
            # Current frame's masks/scalars survive while calling parent sweeps.
            return super(CappedIndexReplaySolver,self).propagate_sweeps(state,ancestor_live_bits+scratch)
        if reserve>self.index_budget_bits: return fallback()
        charge()
        self.metrics['source_passes'] += 1
        self.metrics['sequential_replay_clause_steps'] += self.m
        for cid in self.scope_ids(scope):
            self.metrics['source_clause_accesses'] += 1
            self.metrics['index_acquisition_clause_accesses'] += 1
            for lit in self.source[cid]:
                self.metrics['source_literal_reads'] += 1
                self.metrics['index_acquisition_literal_reads'] += 1
                extra=entry+(header if lit not in occurrence else 0)
                if used+extra>self.index_budget_bits: return fallback()
                occurrence.setdefault(lit,[]).append(cid); used+=extra; charge()
            pending.append(cid); queued.add(cid)
            self.metrics['index_queue_pushes'] += 1
        self.metrics['index_successes'] += 1
        while pending:
            cid=pending.popleft(); queued.remove(cid)
            self.metrics['source_clause_accesses'] += 1
            self.metrics['index_event_clause_accesses'] += 1
            remaining=0; last=0; satisfied=False
            for lit in self.source[cid]:
                self.metrics['source_literal_reads'] += 1
                self.metrics['index_event_literal_reads'] += 1
                bit=1<<(abs(lit)-1)
                if mask&bit:
                    if bool(values&bit)==(lit>0): satisfied=True; break
                else: remaining=min(2,remaining+1); last=lit
            if satisfied: continue
            if remaining==0: return (scope,mask,values),True
            if remaining==1:
                bit=1<<(abs(last)-1)
                mask|=bit
                values=values|bit if last>0 else values&~bit
                self.metrics['unit_propagations'] += 1
                self.metrics['unit_tail_steps'] += 1
                self.metrics['index_assignments'] += 1
                for target in occurrence.get(-last,()):
                    self.metrics['index_occurrence_visits'] += 1
                    if target not in queued:
                        queued.add(target); pending.append(target)
                        self.metrics['index_queue_pushes'] += 1
        return (scope,mask,values),False

def run_tests():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('25 sec')))
    signal.alarm(25); start=time.monotonic(); rng=random.Random(20261008)
    count=0; collisions=0; rows=[]
    def check(source,n,budget,cache=0,record=None):
        nonlocal count,collisions
        old=BatchedUnitReplaySolver(source,n,frontier_cap=0,cache_budget_bits=cache,digest_bytes=0)
        new=CappedIndexReplaySolver(source,n,frontier_cap=0,cache_budget_bits=cache,digest_bytes=0,index_budget_bits=budget)
        a,am=old.solve(); b,bm=new.solve()
        expected=_base.truth(source,n) if n<=7 else a
        assert a==b==expected
        assert bm['index_peak_bits']<=budget
        assert new.cache_bits<=cache
        assert bm['retained_formula_dag_nodes']==bm['retained_residual_formulas']==bm['sat_oracle_calls']==0
        count+=1; collisions+=bm['cache_hash_collisions_rejected']
        if record: rows.append(dict(label=record,n=n,budget=budget,old=am,new=bm))
    clauses=[tuple(v*s for v,s in zip(vs,ss)) for w in range(1,4) for vs in itertools.combinations(range(1,4),w) for ss in itertools.product((-1,1),repeat=w)]
    for k in range(4):
        for source in itertools.combinations(clauses,k): check(source,3,100000)
    exhaustive=count
    for i in range(180):
        n=rng.randint(1,7)
        source=tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(1,min(3,n)))) for _ in range(rng.randint(0,20)))
        for budget in (0,64,512,100000): check(source,n,budget,256)
    for n in (16,32,64,128,256):
        chain=((1,),)+tuple((-i,i+1) for i in range(1,n)); shuffled=list(chain);rng.shuffle(shuffled)
        for name,source in (('forward',chain),('reverse',tuple(reversed(chain))),('shuffle',tuple(shuffled))):
            for budget in (0,n*20,1000000): check(source,n,budget,record=name)
        check(chain+((-n,),),n,1000000,record='conflict')
    for budget in (0,70,100000):
        scoped=CappedIndexReplaySolver(((1,),(-1,),(-1,2),(-2,3)),3,index_budget_bits=budget,frontier_cap=0,cache_budget_bits=0)
        st,bad=scoped.propagate_sweeps(((0,2,3),0,0),0)
        assert not bad and st[1]==st[2]==7
        assert scoped.metrics['index_peak_bits']<=budget
    partial_checks=0
    for _ in range(500):
        n=rng.randint(1,7)
        source=tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(1,n))) for _ in range(rng.randint(1,18)))
        scope=tuple(i for i in range(len(source)) if rng.randrange(2))
        mask=rng.randrange(1<<n); values=rng.randrange(1<<n)&mask
        state=(scope,mask,values)
        baseline=BatchedUnitReplaySolver(source,n,frontier_cap=0,cache_budget_bits=0)
        st0,bad0=baseline.propagate_sweeps(state,0)
        for budget in (0,100,100000):
            obj=CappedIndexReplaySolver(source,n,index_budget_bits=budget,frontier_cap=0,cache_budget_bits=0)
            st,bad=obj.propagate_sweeps(state,0)
            assert bad==bad0 and (bad or st==st0)
            assert obj.metrics['index_peak_bits']<=budget
            partial_checks+=1
    permutation_checks=0
    chain=((1,),)+tuple((-i,i+1) for i in range(1,6))
    for source in itertools.permutations(chain):
        obj=CappedIndexReplaySolver(source,6,index_budget_bits=100000,frontier_cap=0,cache_budget_bits=0)
        st,bad=obj.propagate_sweeps((None,0,0),0)
        assert not bad and st[1]==st[2]==63
        # At most the initial probe plus one false-literal-triggered probe per binary clause.
        assert obj.metrics['index_event_literal_reads']<=21
        permutation_checks+=1
    signal.alarm(0)
    return dict(partial_scope_checks=partial_checks,chain_order_checks=permutation_checks,status='PASS',comparisons=count,exhaustive=exhaustive,scope_checks=3,collision_candidates_rejected=collisions,elapsed_seconds=time.monotonic()-start,rows=rows,note='Packed logical index/queue budget; masks, ancestor descriptors, cache and inherited source locator additionally charged. Python heap overhead not measured. No favorable universal resource bound.')

if __name__=='__main__':
    result=run_tests();Path(__file__).with_name('capped_index_replay_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
