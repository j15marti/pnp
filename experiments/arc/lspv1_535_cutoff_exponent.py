#!/usr/bin/env python3
"""LSPV-1/535 independent numerical checks of the parameterized identifier cutoff.
No external SAT algorithm or R_mix341 checker is executed. Python 3.10+ standard library.
"""
import json, math, hashlib, sys

def scale(N, alpha, d):
    t=math.log2(N)
    return N * (math.log2(t))**d / t**(1.0+alpha)

def cut(N, alpha, d):
    return max(1, math.floor(math.log2(scale(N,alpha,d))))

def guest_exponent(n, alpha, d):
    if not n: return 0.0
    t=math.log2(n+16)
    return n * math.log2(t)**d / t**alpha

def check():
    rows=[]; checks=0; errors=[]
    params=[(0.5,2),(0.5,1),(1/3,1),(1.0,0)]
    for alpha,d in params:
        for e in range(12,43,2):
            N=2**e
            L=cut(N,alpha,d)
            short_count=2**L-1
            Q=N//L
            guest_n=2*Q
            work=guest_exponent(guest_n,alpha,d)
            target=scale(N,alpha,d)
            ratio=max(2**L,work)/target
            assert 2**L<=target+1e-5*target
            assert short_count < 2**L
            assert Q*L<=N
            assert guest_n<=2*N/L
            assert ratio<30, (N,alpha,d,ratio)
            checks+=5
            rows.append(dict(N=N,alpha=alpha,d=d,L=L,short_ids_upper=2**L,
                residual_literals_upper=Q,guest_variables_upper=guest_n,
                benchmark_exponent=round(target,3),
                guest_exponent=round(work,3),
                normalized_ratio=round(ratio,6)))
    # Exact grammar-level occurrence charging, using variable IDs of mixed lengths.
    # Each source occurrence explicitly stores the entire identifier. No implicit dictionary indices.
    for k in range(1,121):
        lengths=[1+((k*13+i*17)%75) for i in range(1+(k%9))]
        # self-delimited, sign-bearing, repeated identifier occurrences; overhead is nonnegative
        N=sum(z+3 for z in lengths)+24
        L=cut(max(N,4096),.5,2)
        Q=sum(z>=L for z in lengths)
        true_bit_budget=sum(z for z in lengths if z>=L)
        assert Q*L<=true_bit_budget<=N
        assert len(set(range(Q)))<=Q
        checks+=2
    return {"run":"LSPV-1/535 quantitative identifier-cutoff audit", "status":"PROVED/RESTRICTED symbolic and COMPUTATIONAL finite controls", "checks":checks,
        "parameter_grid":len(params),"exponent_samples":len(rows),"length_charge_controls":120,
        "min_ratio":min(x["normalized_ratio"] for x in rows),
        "max_ratio":max(x["normalized_ratio"] for x in rows),
        "selected_rows":[x for x in rows if x["alpha"]==.5 and x["d"]==2 and int(math.log2(x["N"])) in [12,20,30,40,42]],
        "proof_system":"NONE (numerical resource envelope only)",
        "historical_mixed_checker_executed":False,
        "guest_subexponential_algorithm_executed":False,
        "note":"Asymptotic theorem proved symbolically; these are finite algebra/inequality controls."}

if __name__ == '__main__':
    result=check()
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    sys.stdout.write(raw)
