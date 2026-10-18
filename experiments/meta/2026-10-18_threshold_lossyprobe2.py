#!/usr/bin/env python3
"""Reproducible integer and Boolean identity tests for THRES-LOSSYPROBE2.
No SAT solver is used. These are exact counting controls, not time lower bounds.
"""
import json

def cl2(x):
    assert x >= 1
    return (x - 1).bit_length()

def circuit_count_log_upper(n, s):
    # At most (s+1)(n+s)[3(n+s)^2]^s ordered fan-in-two circuits.
    return cl2(s+1) + cl2(n+s) + s*(cl2(3)+2*cl2(n+s))

def run():
    rows = []
    for n in (12,16,24,32,40,48,64,80):
        for p, d in ((1,2),(3,4)):
            assert n*p % d == 0
            s = 1 << (p*n//d)
            N = 1 << n
            B = circuit_count_log_upper(n, s)
            k = ((d-p)*n)//(2*d)
            m = n-k
            t = 2*B+2
            rows.append({
                "n":n,
                "beta":f"{p}/{d}",
                "size_parameter":str(s),
                "circuit_count_log_upper_B":str(B),
                "deterministic_zero_input_probe_floor":str(max(0,N-B)),
                "randomized_probe_floor":str(N//(3*t) if t<=N else 0),
                "guard_k":k,
                "guard_hard_core_existence_certified":(1<<m)>B,
            })
    counts={"distinct_blocks":0,"pairwise_half_distance_checks":0,"recovery_bit_checks":0}
    for n in (2,3,4,5,6):
        N=1<<n
        # An arbitrary deterministic base truth table; the identities hold for any base.
        f=[((x*x+7*x+13*n)%17)&1 for x in range(N)]
        blocks=[[f[x]^((i&x).bit_count()&1) for x in range(N)] for i in range(N)]
        for i in range(N):
            for x in range(N):
                assert (blocks[i][x]^((i&x).bit_count()&1)) == f[x]
                counts["recovery_bit_checks"]+=1
            for j in range(i+1,N):
                assert sum(a^b for a,b in zip(blocks[i],blocks[j]))==N//2
                counts["pairwise_half_distance_checks"]+=1
        counts["distinct_blocks"]+=N
    result={
        "id":"THRES_LOSSYPROBE2",
        "kind":"exact integer counts and finite structural identity checks",
        "cases":len(rows),
        "rows":rows,
        "block_audit":counts,
        "discrepancies":0,
        "not_a_runtime_lower_bound":True,
    }
    assert result["cases"]==16
    assert counts=={
        "distinct_blocks":124,
        "pairwise_half_distance_checks":2666,
        "recovery_bit_checks":5456,
    }
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    run()
