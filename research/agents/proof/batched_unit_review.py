#!/usr/bin/env python3
"""Independent BATCHED-UNIT-REPLAY1 oracle and chain-order audit (<25 s)."""
import hashlib, itertools, json, random, signal, time
from pathlib import Path
from batched_unit_replay import BatchedUnitReplaySolver

def truth(cnf,n):
    return any(all(any(bool(a & (1<<(abs(x)-1))) == (x>0) for x in c) for c in cnf) for a in range(1<<n))

def run():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('25 second limit')))
    signal.alarm(25)
    start=time.monotonic()
    counts={'chain_permutations':0,'small_formulas':0,'random_signed_formulas':0,'collision_rejections':0,'direct_conflicts':0}
    means=[]
    for n in range(2,8):
        sums=0; k=0
        for order in itertools.permutations(range(n-1)):
            cnf=tuple((-(i+1),i+2) for i in order)
            s=BatchedUnitReplaySolver(cnf,n,frontier_cap=0,cache_budget_bits=0)
            state,bad=s.propagate_sweeps((None,1,1),0)
            positions={e:p for p,e in enumerate(order)}
            predicted=1+sum(positions[i+1]<positions[i] for i in range(n-2))
            assert not bad and state[1]==state[2]==(1<<n)-1
            assert s.metrics['unit_sweep_passes']==predicted+1
            assert s.metrics['unit_sweep_assignments']==n-1
            assert s.metrics['unit_sweep_clause_accesses']==(predicted+1)*(n-1)
            sums+=predicted;k+=1;counts['chain_permutations']+=1
        assert 2*sums==n*k
        means.append({'n':n,'permutations':k,'mean_productive_passes':sums/k,'expected':n/2})
    # All proper clauses on three variables, including empty; at most two clauses.
    clauses=[tuple((i+1)*v for i,v in enumerate(pattern) if v) for pattern in itertools.product((-1,0,1),repeat=3)]
    formulas=[()]+[(c,) for c in clauses]+list(itertools.combinations(clauses,2))
    for cnf in formulas:
        expected=truth(cnf,3)
        for cap,budget in ((0,0),(0,128),(2,128)):
            s=BatchedUnitReplaySolver(cnf,3,frontier_cap=cap,cache_budget_bits=budget,digest_bytes=0)
            result,metrics=s.solve()
            assert result==expected,(cnf,cap)
            assert s.cache_bits<=budget
            counts['collision_rejections']+=metrics['cache_hash_collisions_rejected']
        counts['small_formulas']+=1
    rng=random.Random(80437)
    for _ in range(350):
        n=rng.randrange(3,8)
        cnf=tuple(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),rng.randrange(1,min(n,4)+1))) for _ in range(rng.randrange(1,22)))
        expected=truth(cnf,n)
        s=BatchedUnitReplaySolver(cnf,n,frontier_cap=0,cache_budget_bits=512,digest_bytes=0)
        result,metrics=s.solve()
        assert result==expected
        assert s.cache_bits<=512
        counts['collision_rejections']+=metrics['cache_hash_collisions_rejected']
        counts['random_signed_formulas']+=1
    for cnf in (((1,),(-1,)),((),),((-1,2),(-2,))):
        s=BatchedUnitReplaySolver(cnf,2,frontier_cap=0,cache_budget_bits=0)
        _,bad=s.propagate_sweeps((None,1,1),0)
        assert bad
        counts['direct_conflicts']+=1
    # Scope isolation: ignored contradictory clauses must not leak into state.
    s=BatchedUnitReplaySolver(((1,),(-1,),(2,)),2,frontier_cap=0,cache_budget_bits=512,digest_bytes=0)
    isolated,bad=s.propagate_sweeps(((0,2),0,0),0)
    assert not bad and isolated[1]==isolated[2]==3
    _,bad=s.propagate_sweeps(((0,1),0,0),0)
    assert bad
    # False is a valid cache value, distinct from missing (None).
    s=BatchedUnitReplaySolver(((1,),(-1,)),1,frontier_cap=0,cache_budget_bits=512,digest_bytes=0)
    assert s.solve()[0] is False
    root=(None,0,0)
    s.cache_insert(root,False,s.descriptor_bits(root))
    hits=s.metrics['cache_hits']
    assert s.solve()[0] is False and s.metrics['cache_hits']>hits
    counts['scope_and_false_cache_checks']=3
    assert counts['collision_rejections']>0
    signal.alarm(0)
    return {'status':'PASS','elapsed_seconds':round(time.monotonic()-start,4),'counts':counts,'chain_means':means,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),Path(__file__).with_name('batched_unit_replay.py'),Path(__file__).with_name('unit_tail_replay.py'))},'scope':'Independent Boolean correctness and logical counter checks; not total Python memory or asymptotic all-input proof.'}

if __name__=='__main__':
    result=run()
    path=Path(__file__).with_name('batched_unit_review_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
