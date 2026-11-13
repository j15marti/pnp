#!/usr/bin/env python3
"""Independent exhaustive local control for LSPV-1/610.

A reference semantics implementation, NOT the historical /341 verifier.
The theorem is proved symbolically in the accompanying report.
"""
from __future__ import annotations
import itertools, json, sys
from pathlib import Path

E=3
U=tuple(range(E))
SUBSETS=[tuple(i for i in U if (mask>>i)&1) for mask in range(1<<E)]

def value(table,support,bits):
    pos=sum(bits[e]<<i for i,e in enumerate(support))
    return (table>>pos)&1

def make_and(a,sa,b,sb,support):
    out=0
    for m in range(1<<len(support)):
        bits=[0]*E
        for j,e in enumerate(support): bits[e]=(m>>j)&1
        if value(a,sa,bits) and value(b,sb,bits):out|=1<<m
    return out

def assert_local(a,sa,b,sb,order):
    q=make_and(a,sa,b,sb,order)
    for bits in itertools.product((0,1),repeat=E):
        assert value(q,order,bits)==(value(a,sa,bits)&value(b,sb,bits))
    return q

def affine_table(mask,rhs,support):
    out=0
    for m in range(1<<len(support)):
        bits=[0]*E
        for j,e in enumerate(support):bits[e]=(m>>j)&1
        parity=0
        for e in U:parity^=bits[e]*((mask>>e)&1)
        if parity==rhs:out|=1<<m
    return out

def main():
    checks=0; pairs=0; ordered=0; rows=0
    for sa in SUBSETS:
        for sb in SUBSETS:
            union=tuple(sorted(set(sa)|set(sb)))
            for order in itertools.permutations(union):
                aliases={}
                for mask in range(1<<E):
                    if any(((mask>>e)&1) and e not in union for e in U):continue
                    for rhs in (0,1):
                        aliases.setdefault(affine_table(mask,rhs,order),[]).append((mask,rhs))
                for a in range(1<<(1<<len(sa))):
                    for b in range(1<<(1<<len(sb))):
                        q=assert_local(a,sa,b,sb,order)
                        ordered+=1;checks+=(1<<E)
                        for mask,rhs in aliases.get(q,[]):
                            rows+=1
                            for bits in itertools.product((0,1),repeat=E):
                                assert value(q,order,bits)==(int(sum(bits[e]*((mask>>e)&1) for e in U)%2==rhs))
                                checks+=1
            pairs+=1
    masks=[-2**30,-8,-1,0,1,2,7,8,15,2**30,2**100+5]
    for a in masks:
        for b in masks:
            low=lambda x:x&((1<<E)-1)
            assert low(a^b)==(low(a)^low(b));checks+=1
            for e in U:
                assert ((a>>e)&1)==((low(a)>>e)&1);checks+=1
    original=[0,1,10];raw='102'
    assert len(raw)==len(original)
    assert len(set(raw))==len(original)
    assert all(str(x) in raw for x in original)
    actual=[int(c) for c in raw]
    assert actual!=original
    assert 10 not in actual
    result={
      'id':'LSPV-1/610','date_pst':'2026-11-12 22:00',
      'status':'PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL exhaustive 3-variable local semantics',
      'scope':'archived /341 accepted proof if source literals are signed safe integers and all AND3 support values are JavaScript arrays; not full R_mix341',
      'parent_scope_pairs':pairs,'ordered_truth_table_pairs':ordered,
      'truth_table_and_affine_checks':checks,'matching_affine_aliases':rows,
      'signed_and_highbit_masks_tested':len(masks),
      'string_shadow':{'source_union':original,'malformed_support':raw,'actual_enumerated_coords':actual,'substring_membership_passes':True},
      'open':['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],
      'limitations':'Reference local semantics only; does not execute checker, prove completeness/cheap-proof normalizer, or constrain an unknown historical rule.'
    }
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(output)
    print(output,end='')

if __name__=='__main__':main()
