#!/usr/bin/env python3
"""ARCHIVE-ARC-SEMANTIC82 exact finite regression controls; not a P vs NP proof."""
import json
from fractions import Fraction
from pathlib import Path

def parity(v): return v.bit_count() & 1

def beta(c): return ((c+2)/(c*c)-c)/2

def finite_depth(K):
    t=s=Fraction(K); c=Fraction(241,200)
    for i in range(100):
        if t<c and s<=Fraction(1,2): return i
        t=max(Fraction(11,10), Fraction(3,5)+t/2)
        s=max(Fraction(1,2), s/2)
    raise AssertionError("no finite entry")

def main():
    c=Fraction(241,200); b=beta(c)
    assert b==Fraction(11642479,23232400)>Fraction(1,2)
    sat=unsat=projection_checks=flips=0
    for k in range(2,9):
        cosets=[[x for x in range(1<<k) if parity(x)==z] for z in (0,1)]
        assert len(cosets[0])==len(cosets[1])==(1<<(k-1))
        for mask in range((1<<k)-1):
            js=[j for j in range(k) if mask>>j&1]
            all_s=set(range(1<<len(js)))
            for z in (0,1):
                proj={sum(((x>>j)&1)<<i for i,j in enumerate(js))
                      for x in cosets[z]}
                assert proj==all_s,(k,mask,z)
                projection_checks+=1
        for e in range(1<<k):
            p=parity(e)
            answer=bool(set(cosets[0])&set(cosets[p]))
            assert answer==(p==0)
            sat+=int(answer); unsat+=int(not answer)
            for i in range(k):
                assert parity(e^(1<<i))==1-p
                flips+=1
    starts=[2,3,7,31,127,1024]
    depths={str(K):finite_depth(K) for K in starts}
    assert [depths[str(K)] for K in starts]==[8,9,11,13,15,18]
    out={
        "run_id":"ARCHIVE-ARC-SEMANTIC82",
        "status":"COMPUTATIONAL; mathematical statements have separate proofs",
        "source_k_range":[2,8],
        "matched_sat":sat,"matched_unsat":unsat,
        "proper_projection_checks":projection_checks,
        "single_bit_flip_checks":flips,
        "endpoint_c":str(c),"endpoint_beta":str(b),
        "finite_recurrence_depths":depths,
        "unrestricted_P_vs_NP":"OPEN"
    }
    Path(__file__).with_name("2026-10-24_LSPV3_ARC_SEMANTIC82_raw.json").write_text(
        json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":main()
