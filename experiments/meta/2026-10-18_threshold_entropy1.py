#!/usr/bin/env python3
"""Exact integer checks for the THRES-ENTROPY1 counting theorem."""
import json
def cl2(x):
    return (x-1).bit_length()
rows=[]
for n in (16,24,32,40,48,64):
    s=1 << (3*n//4)
    t=s//(2*n)
    L=t*(n-cl2(t))
    assert n+n*t<=s
    for expansion in (1,2):
        m=n*expansion
        r=1 << (n//2)
        U=cl2(r+1)+cl2(m+r)+r*(cl2(3)+2*cl2(m+r))
        rows.append(dict(n=n,m=m,source_lower=L,target_upper=U,forbidden=L>U))
assert len(rows)==12
assert sum(z["forbidden"] for z in rows)==8
print(json.dumps(rows,indent=2))
