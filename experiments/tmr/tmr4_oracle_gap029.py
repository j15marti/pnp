#!/usr/bin/env python3
"""TMR-4/029: black-box evaluation-locality and SAT masking controls.
No circuit-size oracle. All tests are finite, symbolic and reproducible.
"""
import json
import random
from collections import Counter


def zero_gate_tables(n):
    N=1<<n
    out={0, (1<<N)-1}
    for i in range(n):
        mask=sum((((x>>i)&1)<<x) for x in range(N))
        out.add(mask)
    return out


def sat_mask_truth_table(fmask,v):
    # Variables: x_0..x_(v-1), u=x_v, w=x_(v+1).
    # g_F(x,u,w)=F(x) AND u AND w.
    n=v+2
    N=1<<n
    return sum(((((fmask>>(x&((1<<v)-1)))&1) & ((x>>v)&1) & ((x>>(v+1))&1))<<x) for x in range(N))


def random_adaptive_output(fmask, M, seed, j, q):
    # Deterministic for fixed seed,j and oracle f, allowed nonlinear,
    # state-dependent queries; zero-oracle output is always zero.
    rng_seed=seed*10007+j*101
    responses=[]
    seen=set()
    for step in range(q):
        # Query depends on the entire transcript, but zero path is fixed.
        state=rng_seed + step*1000003
        for t,b in enumerate(responses):
            state += (t+1)*7919*b
        a=random.Random(state).randrange(M)
        seen.add(a)
        responses.append((fmask>>a)&1)
    return int(any(responses)),len(seen)


def check():
    counts=Counter(); results=[]
    # Direct reduction F -> truth table of h_F: UNSAT -> MCSP_0 YES,
    # SAT -> MCSP_0 NO, output N=2^(v+2), exponential in v.
    for v in range(0,5):
        M=1<<v
        cases=(1<<M)
        for fmask in range(cases):
            g=sat_mask_truth_table(fmask,v)
            z=zero_gate_tables(v+2)
            assert (g in z)==(fmask==0), (v,fmask,g)
            assert g.bit_count()==fmask.bit_count(),(v,fmask)
            counts['direct_mask_instances']+=1
        # Padding dummy variables multiplies numerator and denominator.
        if v <=3:
            for a in range(M):
                f=1<<a
                g=sat_mask_truth_table(f,v)
                assert g.bit_count()==1
                for t in range(4):
                    G=sum(((g>>x)&1) << (x + r*(1<<(v+2))) for r in range(1<<t) for x in range(1<<(v+2)))
                    assert G.bit_count()*(1<<(v+2))==((1<<(v+2+t)))
                    counts['dummy_padding_checks']+=1
    # Non-adaptive balanced cyclic q-evaluation OR generator gives sharpness.
    for v in range(1,7):
        M=1<<v
        N=2*M
        for q in range(0,M+1):
            weights=[]
            for a in range(M):
                y=sum((int(any(((a == ((j+t)%M)) for t in range(q))))<<j) for j in range(N))
                weights.append(y.bit_count())
            assert set(weights)=={N*q//M},(v,q,weights)
            counts['cyclic_singleton_checks']+=M
        results.append({'v':v,'M':M,'N':N,'sharp_q1_weight':N//M,'sharp_q_half_weight':N//2})
    # Adaptive queries, zero-transcript double counting under arbitrary
    # source-independent output programs. A unary spike oracle f_a differs
    # at only a, so changes only outputs whose zero path queried a.
    for v in range(1,6):
        M=1<<v; N=3*M
        for q in range(0,min(M,7)+1):
            for seed in range(5):
                zero=[random_adaptive_output(0,M,seed,j,q)[0] for j in range(N)]
                assert not any(zero)
                weights=[]
                for a in range(M):
                    w=sum(random_adaptive_output(1<<a,M,seed,j,q)[0]!=zero[j] for j in range(N))
                    weights.append(w)
                assert sum(weights)<=N*q,(v,q,seed,weights)
                assert min(weights)*M<=N*q,(v,q,seed,weights)
                counts['adaptive_adversary_suites']+=1
                counts['adaptive_spike_outputs']+=M*N
    return {'claim':'TMR4-ORACLEGAP29 finite evidence','status':'COMPUTATIONAL','counts':dict(counts),'cyclic_samples':results,'assertion_failures':0,
        'scope':'source-independent adaptive evaluation-oracle output programs; no general SAT algorithm lower bound'}

if __name__=='__main__':
    print(json.dumps(check(),indent=2,sort_keys=True))
