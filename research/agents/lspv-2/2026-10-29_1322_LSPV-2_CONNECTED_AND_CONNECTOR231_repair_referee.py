#!/usr/bin/env python3
"""Independent replay of original 16-seed/flip=n repair test on connected J products.
This code copies the deterministic repair policy from supplied Polynomial_Coverage_Proof_Study,
with no changes to its RNG, scoring, tie order, or budget. Produces JSON line for each k.
"""
import importlib.util,json,random,time,sys
from collections import Counter
from pathlib import Path
base=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('connector',base/'2026-10-29_1322_LSPV-2_CONNECTED_AND_CONNECTOR231_repro.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
M=[tuple((-l if i in (1,15) and abs(l)==9 else l) for l in c) for i,c in enumerate(C.W1)]
assert C.validate(M)==(15,20)
table,witness,profile=C.local_profile()
models=list(C.simple_models(M))
assert models
m0=models[0];model0={v:int(bool(m0&(1<<(v-1)))) for v in range(1,16)}

def repair(source, flips=32, seed=0):
    rng=random.Random(seed)
    vs=sorted({abs(l) for c in source for l in c})
    a={v:rng.randrange(2) for v in vs}
    evaluations=0
    def false_clauses(a):
        nonlocal evaluations
        evaluations+=1
        return [i for i,c in enumerate(source) if not any(a[abs(l)]==int(l>0) for l in c)]
    for step in range(flips+1):
        bad=false_clauses(a)
        if not bad:return {'status':'SAT','flips':step,'evaluations':evaluations}
        if step==flips or any(not source[i] for i in bad):break
        c=source[rng.choice(bad)];candidates=[]
        for v in sorted({abs(l) for l in c}):
            a[v]^=1;score=len(false_clauses(a));a[v]^=1;candidates.append((score,v))
        best=min(s for s,v in candidates)
        options=[v for s,v in candidates if s==best]
        v=rng.choice([v for s,v in candidates] if rng.random()<0.2 else options)
        a[v]^=1
    return {'status':'GAP','flips':step,'evaluations':evaluations}

def run_k(k,permuted=False,seed_start=0,seed_end=16):
    cs=list(M);model=dict(model0)
    for i in range(1,k):cs,model,_=C.join(cs,M,model,model0,mode=i%3,witness=witness)
    assert model is not None and C.validate(cs) and C.connected_components_count(cs)==1
    if permuted:
        cs,mp=C.renamed(cs,seed=20261029+k)
        model={mp[v]:b for v,b in model.items()}
        assert all(any(model[abs(l)]==int(l>0) for l in c) for c in cs)
    n=max(abs(l) for c in cs for l in c)
    outputs=[repair(cs,n,seed) for seed in range(seed_start,seed_end)]
    return {'k':k,'n':n,'m':len(cs),'source_mutation':'W1-x9-flip-clauses-1-and-15',
        'permuted':permuted,'SAT_witness_valid':True,
        'seed_start':seed_start,'seed_end':seed_end,
        'successful_seeds':[i+seed_start for i,x in enumerate(outputs) if x['status']=='SAT'],
        'full_assignment_evaluations':sum(x['evaluations'] for x in outputs),
        'repair_flips':sum(x['flips'] for x in outputs),
        'per_seed':outputs}

if __name__=='__main__':
    k=int(sys.argv[1]);p=bool(int(sys.argv[2])) if len(sys.argv)>2 else False
    start=int(sys.argv[3]) if len(sys.argv)>3 else 0
    end=int(sys.argv[4]) if len(sys.argv)>4 else 16
    print(json.dumps(run_k(k,p,start,end),sort_keys=True))