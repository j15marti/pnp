#!/usr/bin/env python3
"""Independent NAND2 circuit census and last-additive FK structural-toy audit.
Toy masks are not the original CHMY indexed PRG. Proof works for every public-seed distribution.
"""
import argparse, json, math, random
from pathlib import Path

def circuit_sets(n, max_gates):
    N=1<<n; mask=(1<<N)-1
    inputs=[sum(((a>>j)&1)<<a for a in range(N)) for j in range(n)]
    terminals=inputs+[0,mask]
    by_s=[set(terminals)]
    states=[tuple(terminals)]
    populations=[1]
    for size in range(1,max_gates+1):
        next_states=[]
        discovered=set(by_s[-1])
        for wires in states:
            for i in range(len(wires)):
                for j in range(i,len(wires)):
                    out=(~(wires[i]&wires[j]))&mask
                    next_states.append(wires+(out,))
                    discovered.update(wires)
                    discovered.add(out)
        states=list(set(next_states))
        by_s.append(discovered)
        populations.append(len(states))
    return by_s,populations

def toy_fk_offset(N,r,rng):
    # Independent UNIFORM full-vector masks are a structural toy, not CHMY parameters.
    g=rng.getrandbits(N)
    for _ in range(1,r-1):
        d=rng.getrandbits(N)
        t=rng.getrandbits(N)
        g=d^(t&g)
    return rng.getrandbits(N)&g

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=202610200050)
    ap.add_argument("--n",type=int,default=3)
    ap.add_argument("--source-size",type=int,default=3)
    ap.add_argument("--target-size",type=int,default=1)
    ap.add_argument("--samples",type=int,default=512)
    ap.add_argument("--output",default="results.json")
    a=ap.parse_args()
    N=1<<a.n
    sets,populations=circuit_sets(a.n,max(a.source_size,a.target_size))
    sources=sorted(sets[a.source_size])
    targets=set(sets[a.target_size])
    assert targets.issubset(set(sources))
    shifts=[]
    for b in range(1<<N):
        hits=sum((f^b) in targets for f in sources)
        assert hits<=len(targets)
        shifts.append(hits)
    rng=random.Random(a.seed)
    toy=[toy_fk_offset(N,math.ceil(math.log2(N)),rng) for _ in range(a.samples)]
    per_seed=[]
    for b in toy:
        hits=sum((f^b) in targets for f in sources)
        assert hits<=len(targets)
        per_seed.append(hits)
    per_source=[sum((f^b) in targets for b in toy) for f in sources]
    worst=min(range(len(sources)),key=lambda i:per_source[i])
    assert per_source[worst]/a.samples<=len(targets)/len(sources)
    for f in sources:
        assert sum((f^b) in targets for b in range(1<<N))==len(targets)
    no=next((f for f in range(1<<N) if f not in sources),None)
    if no is not None:
        assert sum((no^b) in targets for b in range(1<<N))==len(targets)
    result={
        "run_id":"CHMY_LAST_ADDITIVE_YES_CARDINALITY1",
        "seed":a.seed,
        "status":"COMPUTATIONAL, with separate symbolic theorem",
        "N":N,"n":a.n,
        "source_gate_size":a.source_size,
        "target_gate_size":a.target_size,
        "model":"NAND2; free input wires and 0/1; gate budget; arbitrary output pointer",
        "toy_FK":"Independent uniform D/T vectors, NOT full CHMY indexed PRG",
        "class_cardinalities":[len(v) for v in sets],
        "state_histories":populations,
        "source_class_cardinality":len(sources),
        "target_class_cardinality":len(targets),
        "upper_bound_source_yes_success":len(targets)/len(sources),
        "all_shifts_checked":len(shifts),
        "max_hits_per_shift":max(shifts),
        "mean_hits_per_shift":sum(shifts)/len(shifts),
        "toy_samples":len(toy),
        "toy_mean_yes_success":sum(per_seed)/(len(toy)*len(sources)),
        "worst_source_bitstring":format(sources[worst],f"0{N}b"),
        "worst_source_toy_success":per_source[worst]/len(toy),
        "uniform_shifts_yes_success":len(targets)/(1<<N),
        "NO_control_present":no is not None,
        "uniform_shifts_NO_false_accept":len(targets)/(1<<N) if no is not None else None,
        "assertion_failures":0,
        "limitations":"Toy masks; no claim about CHMY one-tape time or full PRG security"
    }
    Path(a.output).write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
