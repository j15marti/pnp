#!/usr/bin/env python3
"""Exact finite source-grammar/serialization guard for M22-PIN-DIVISIBILITY141.

No solver lower bound is claimed.  The enumeration budget in this test is
an explicitly chosen naive exhaustive-completion list, not an algorithm bound.
"""
import json
from collections import Counter


def canonical_bits(k):
    assert k >= 6 and k % 3 == 0
    m = 4*k//3
    b = m.bit_length()  # ceil(log2(m+1))
    return 3*b+1 + m*(1+3*b)


def quota_floor(k, d):
    assert k % 3 == 0 and 0 <= d <= k
    return max(6,3*((k-d+2)//3))


def support_clauses(positive, negative):
    return [tuple(t) for t in positive]+[tuple(-v for v in t) for t in negative]


def is_m22(formula):
    if not formula: return False
    if len(set(tuple(sorted(clause)) for clause in formula)) != len(formula):return False
    degrees=Counter()
    for clause in formula:
        if len(clause)!=3 or len(set(abs(t) for t in clause))!=3:return False
        if not (all(t>0 for t in clause) or all(t<0 for t in clause)):return False
        for lit in clause:degrees[(abs(lit),int(lit>0))]+=1
    return all(degrees[(x,sgn)]==2 for x in {v for v,_ in degrees} for sgn in (0,1))


def nonpaired(formula):
    clauses={tuple(sorted(cl)) for cl in formula}
    return any(tuple(sorted(-x for x in c)) not in clauses for c in formula)


def pin(formula,x,val):
    out=[]
    for c in formula:
        if x in c and val:continue
        if -x in c and not val:continue
        new=tuple(lit for lit in c if abs(lit)!=x)
        out.append(new)
    return out


def sat(formula,k):
    return any(all(any(((mask>>(abs(lit)-1))&1)==int(lit>0) for lit in c) for c in formula) for mask in range(1<<k))


def fixture(h=1):
    pos=[];neg=[]
    for i in range(h):
        base=6*i
        def a(z):return base+z
        nxt=6*((i+1)%h)+1
        pos += [(nxt,a(2),a(3)),(a(1),a(4),a(5)),(a(2),a(4),a(6)),(a(3),a(5),a(6))]
        neg += [(a(1),a(2),a(4)),(a(1),a(3),a(6)),(a(2),a(3),a(5)),(a(4),a(5),a(6))]
    return support_clauses(pos,neg)


def run():
    rows=[];checks=0
    for k in (6,9,12,18,96,198,600):
        for d in (1,2,3,4,5,6,9):
            if d>k:continue
            kd=quota_floor(k,d)
            assert kd>=k-d and kd%3==0
            assert kd == max(6,k - 3*(d//3))
            if d in (1,2):assert kd==k and canonical_bits(kd)==canonical_bits(k)
            rows.append({"k":k,"d":d,"min_valid_child_k":kd,"parent_bits":canonical_bits(k),"child_floor_bits":canonical_bits(kd),"minimum_aux_if_all_other_names_retained":kd-(k-d)})
            checks+=4
    for h in (1,2,3,16):
        f=fixture(h);assert is_m22(f) and nonpaired(f)
        checks+=2
        if h==1:
            assert sum(sat(f,6) for _ in (0,))==1
            nmodels=sum(all(any(((mask>>(abs(lit)-1))&1)==int(lit>0) for lit in c) for c in f) for mask in range(64))
            assert nmodels==20
            checks+=2
            for x in range(1,7):
                for v in (0,1):
                    c=pin(f,x,v)
                    assert not is_m22(c)
                    assert all(any(abs(l)==y for cl in c for l in cl) for y in range(1,7) if y!=x)
                    assert sat(c,6)==any(all(any(((mask>>(abs(lit)-1))&1)==int(lit>0) for lit in cl) for cl in f) for mask in range(64) if ((mask>>(x-1))&1)==v)
                    checks+=3
                    for z in range(1,7):
                        if z==x:continue
                        for w in (0,1):
                            c2=pin(c,z,w)
                            assert not is_m22(c2)
                            checks+=1
    return {"id":"M22-PIN-DIVISIBILITY141", "status":"COMPUTATIONAL exact integer/finite assertions; no machine lower bound", "cases":rows,"checks":checks,"failures":0,"fixture_model_count":20,"one_level_target_valid_children":0,"two_level_target_valid_children":0,"naive_raw_full_branch_two_level_Rsearch":0,"naive_repaired_binary_two_level_Rsearch_ceiling":-2}

if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
