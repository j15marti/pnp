#!/usr/bin/env python3
"""CLOCKEXCEPT10 finite controls; standard library only; under 30 seconds.

Checks exact binary-matrix section collision counts, rare-seed KL cost,
and adaptive nonlinear source-transcript sparse completions. These are
finite controls, NOT P versus NP or unrestricted runtime lower bounds.
"""
import itertools
import json
import math
import random
from pathlib import Path

SEED = 202610181944
rng = random.Random(SEED)

def digest(rows, f):
    return tuple(((row & f).bit_count() & 1) for row in rows)

def matrix_case(N, b, t, f):
    section = [sum(1 << i for i in v) for v in itertools.combinations(range(N), t)]
    total = 2 ** (N*b)
    misses = 0
    for x in range(total):
        rows = tuple((x >> (k*N)) & ((1 << N)-1) for k in range(b))
        y = digest(rows, f)
        if all(digest(rows, g) != y for g in section):
            misses += 1
    assert 0 < misses < total
    assert misses * math.comb(N,t) <= total * 2**b
    p = misses / total
    # The KL of Q conditioned on E against Q is exactly log2(1/p).
    divergence = math.log2(total/misses)
    assert divergence >= math.log2(math.comb(N,t)/(2**b))-1e-12
    two_thirds_trials = math.ceil(math.log(1/3)/math.log(1-p))
    assert two_thirds_trials*p >= 2/3 -1e-12
    return {"N":N,"b":b,"t":t,"f":f,"exceptional":misses,
            "seeds":total,"KL_bits":divergence,"trials_2_3":two_thirds_trials}

def transducer(f, N, b, seed):
    values = []
    seen = set()
    for j in range(b):
        i=(3*seed+7*j+1)%N
        a=(f>>i)&1; seen.add(i)
        i=(seed+11*j+5*a+2)%N
        c=(f>>i)&1; seen.add(i)
        i=(7*seed+13*j+3*a+5*c+4)%N
        d=(f>>i)&1; seen.add(i)
        values.append(a^(c&d)^(j&1))
    return tuple(values),seen

def nonlinear_controls():
    N=32; b=5; trials=1000
    max_queries=0; zero_weights=0; minority_exceptions=0
    original_weights=0; majority_one=0; fewer=0
    for _ in range(trials):
        f=rng.getrandbits(N)
        seed=rng.randrange(50)
        y,seen=transducer(f,N,b,seed)
        g0=sum(((f>>i)&1)<<i for i in seen)
        y0,seen0=transducer(g0,N,b,seed)
        assert (y0,seen0)==(y,seen)
        ones=sum((f>>i)&1 for i in seen)
        zeros=len(seen)-ones
        background=int(ones>zeros)
        g1=((1<<N)-1) if background else 0
        for i in seen:
            if ((g1>>i)&1)!=((f>>i)&1):
                g1 ^= 1<<i
        y1,seen1=transducer(g1,N,b,seed)
        assert (y1,seen1)==(y,seen)
        assert min(ones,zeros)<=len(seen)//2
        zero_weights += g0.bit_count()
        original_weights += f.bit_count()
        minority_exceptions += min(ones,zeros)
        majority_one += background
        max_queries=max(max_queries,len(seen))
        fewer += len(seen)<3*b
    # Source-dependent selector recomputation may differ from holding
    # the seed fixed. A charged whole-selector transcript repairs this.
    f=3; g=1
    assert (f.bit_count()%2)!=(g.bit_count()%2)
    return {"trials":trials,"N":N,"b":b,"max_distinct_queries":max_queries,
            "mean_zero_weight":zero_weights/trials,
            "mean_original_weight":original_weights/trials,
            "mean_minority_exceptions":minority_exceptions/trials,
            "majority_one_trials":majority_one,
            "strictly_fewer_than_15_queries":fewer,
            "source_selector_replay_counterexample":[f,g]}

def main():
    matrix=[matrix_case(*x) for x in [(6,2,2,7),(8,1,3,0),(8,2,3,0)]]
    result={"report":"CLOCKEXCEPT10","random_seed":SEED,
            "matrix_cases":matrix,"nonlinear":nonlinear_controls(),
            "status":"COMPUTATIONAL finite checks; P versus NP OPEN"}
    out=Path("results/raw/meta_lift/2026-10-18_CLOCK_EXCEPTIONAL_SEED10.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,sort_keys=True,indent=2))
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
