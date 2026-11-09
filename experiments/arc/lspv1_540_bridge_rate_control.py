#!/usr/bin/env python3
"""Finite arithmetic checks for the logical bridge-rate theorem, not a SAT proof."""
import json, math, sys

checks=[]
for r in (2,3,4):
    q=(1+r)/2
    assert 1<q<r
    for log_n in (16.,32.,64.,128.,256.,512.,1024.):
        log_w=log_n**q
        assert log_w/log_n>1
        assert log_w<=log_n**r
        checks.append(dict(r=r,q=q,logN=log_n,logW_per_logN=log_w/log_n,logW_per_logN_to_r=log_w/(log_n**r)))
for h in (64,256,1024,4096):
    nbits=h*math.ceil(math.log2(h+2))
    x=math.sqrt(nbits/math.log(nbits))
    ratio=math.sqrt(h)/x
    assert 0.75<ratio<1.25
    checks.append(dict(h=h,encoded_bits=nbits,root_h=math.sqrt(h),root_N_over_logN=x,ratio=ratio))
print(json.dumps({"proof_status":"COMPUTATIONAL numeric controls only; symbolic proof in report", "checks":len(checks), "parameters":{"r":[2,3,4],"logN":[16,32,64,128,256,512,1024],"h":[64,256,1024,4096]},"values":checks},indent=2))
