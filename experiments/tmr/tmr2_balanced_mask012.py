#!/usr/bin/env python3
"""Exact source/sign query-certificate audit for TMR-2/012, not a physical TM.
Permutations of eight masks are the precisely UNSAT eight-clause blocks.
All 24 source sign-bit positions are free; headers/IDs/fillers fixed.
"""
import itertools, json, sys, time
from math import comb

BAL=(0,0,3,3,5,5,6,6)
OLD=(1,2,3,4,5,6,7,7)
FULL=tuple(range(8))

def matchable(t, positions):
    domains=[list(range(8)) for _ in range(8)]
    for p in positions:
        i,b=divmod(p,3)
        domains[i]=[m for m in domains[i] if (m>>b)&1==(t[i]>>b)&1]
    owner=[-1]*8
    def augment(row, seen):
        for mask in domains[row]:
            if mask in seen: continue
            seen.add(mask)
            if owner[mask]<0 or augment(owner[mask],seen):
                owner[mask]=row
                return True
        return False
    return all(augment(i,set()) for i in range(8))

def audit(t,max_query=6):
    out={}
    for k in range(max_query+1):
        n=cert=0
        for coords in itertools.combinations(range(24),k):
            n+=1
            if not matchable(t,coords): cert+=1
        out[str(k)]={'subsets':n,'SAT_certificates':cert}
    return out

def labels(t):
    return any(a not in t for a in range(8))

def radius(t):
    for k in range(1,6):
        cnt=0
        for positions in itertools.combinations(range(24),k):
            arr=list(t)
            for p in positions:
                row,b=divmod(p,3)
                arr[row]^=1<<b
            if not labels(arr):cnt+=1
        if cnt:return {'distance':k,'UNSAT_neighbors_at_distance':cnt}
    raise AssertionError('No short UNSAT neighbor')

def check_control(t):
    assert labels(t) is True
    assert all(sum((x>>b)&1 for x in t)==4 for b in range(3))
    assert len(set(t))<8


def main():
    st=time.time()
    check_control(BAL)
    assert labels(OLD)
    out={'tag':'TMR2-BALANCED-MASK-012','status':'COMPUTATIONAL', 'python':sys.version.split()[0],
      'old':{'tuple':OLD,'certs':audit(OLD,5)},
      'balanced':{'tuple':BAL,'certs':audit(BAL,6)},
      'balanced_hamming':radius(BAL),
      'structured_product_examples':[],'failures':0}
    assert all(out['balanced']['certs'][str(k)]['SAT_certificates']==0 for k in range(6))
    assert out['balanced']['certs']['6']['SAT_certificates']>=4
    assert all(out['old']['certs'][str(k)]['SAT_certificates']==0 for k in range(5))
    assert out['old']['certs']['5']['SAT_certificates']>0
    assert out['balanced_hamming']['distance']==4
    for r in [1,2,3,8,64]:
        masks=[BAL]*r
        assert all(labels(m) for m in masks)
        for g in range(min(r,3)):
            swapped=list(masks)
            swapped[g]=FULL
            assert any(not labels(m) for m in swapped)
        out['structured_product_examples'].append({'r':r,'SAT_cert_bits':6*r,'UNSAT_cert_bits':24,'free_sign_bits':24*r})
    out['wall_s']=round(time.time()-st,3)
    return out

if __name__=='__main__':print(json.dumps(main(),indent=2))
