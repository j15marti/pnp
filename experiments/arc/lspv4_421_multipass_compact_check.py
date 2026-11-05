#!/usr/bin/env python3
"""LSPV-4/421 compact independently runnable finite set-intersection check.
The full gated 3-CNF producer and independent JS referee are archived separately.
This checks p-pass logic and the deterministic DISJ fooling set, not FLMV physics.
"""
from itertools import product

def passes(S,T,M,p):
    width=(M+p-1)//p
    sat=False
    for j in range(p):
        lo=j*width
        hi=min(M,(j+1)*width)
        mask=(1<<(hi-lo))-1 if hi>lo else 0
        chunk=(S>>lo)&mask
        sat|=bool(chunk & ((T>>lo)&mask))
    return sat

def audit(M):
    full=(1<<M)-1
    valid=0
    fooling=0
    for S in range(1<<M):
        assert S&(full^S)==0
        for T in range(S):
            assert (S&(full^T)) or (T&(full^S))
            fooling+=1
        for T in range(1<<M):
            for p in sorted({1,2,3,4,M}):
                assert passes(S,T,M,p)==bool(S&T)
                valid+=1
    return {"M":M,"pair_pass_checks":valid,"fooling_pair_checks":fooling}

if __name__=="__main__":
    rows=[audit(4),audit(8)]
    print(rows)
    assert sum(x["pair_pass_checks"] for x in rows)==328704
    assert sum(x["fooling_pair_checks"] for x in rows)==32760
    print("PASS: restricted deterministic p-pass set-intersection lemma controls")
