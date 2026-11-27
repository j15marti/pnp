"""Standalone copy of executed independent original-row transfer (unused grid26 import omitted).
No closure assumptions, no dependencies beyond Python standard library.
"""
from collections import defaultdict
from functools import lru_cache
import json

def count(s,cap=200000):
    full=(1<<s)-1
    checks=0
    peak=1
    @lru_cache(None)
    def row(a,b):
        nonlocal checks
        if a==full:
            return {b:1}
        bit=(~a&full)&-(~a&full)
        D=defaultdict(int)
        for u,v in [(bit|(bit<<1),bit),(bit,bit|(bit>>1))]:
            checks+=1
            if checks>cap:
                raise TimeoutError
            if (u&~full) or (v&~full) or v.bit_count()+u.bit_count()!=3 or (a&u) or (b&v):
                continue
            for c,k in row(a|u,b|v).items():
                D[c]+=k
        return dict(D)
    S={0:1}
    layers=[]
    try:
        for i in range(s-1):
            R=defaultdict(int)
            for a,k in S.items():
                for b,j in row(a,0).items():
                    checks+=1
                    if checks>cap:
                        raise TimeoutError
                    R[b]+=k*j
            S=dict(R)
            peak=max(peak,len(S))
            layers.append(len(S))
        return dict(status='NO' if S.get(full,0)==0 else 'YES_CONTROL_EXCLUDED',count=str(S.get(full,0)),checks=checks,peak=peak,layers=layers,cache=row.cache_info().currsize)
    except TimeoutError:
        return dict(status='UNKNOWN',checks=checks-1,peak=peak,layers=layers,cache=row.cache_info().currsize)

if __name__=='__main__':
    for s in [3,9,15,21]:
        z=count(s)
        z['s']=s
        print(json.dumps(z))
