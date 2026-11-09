#!/usr/bin/env python3
"""Exact GF(2) affine rank of one-hot modular boundary fibers; not an Rmix checker."""
import itertools
import json
import hashlib
from pathlib import Path

def rank_basis(vectors):
    pivots={}
    for x in vectors:
        while x:
            i=x.bit_length()-1
            if i not in pivots:
                pivots[i]=x
                break
            x ^= pivots[i]
    return pivots

def encode(x,q):
    a=0
    for i,v in enumerate(x):
        a |= 1 << (i*q+v)
    return a

def case(q,b,c,signs):
    sat=[]
    for x in itertools.product(range(q),repeat=b):
        if sum(signs[i]*x[i] for i in range(b))%q==c:
            sat.append(x)
    assert len(sat)==q**(b-1)
    rows=[encode(x,q) for x in sat]
    basis=rank_basis([r^rows[0] for r in rows[1:]])
    dim=len(basis)
    expect=q-1 if b==2 else b*(q-1)-(1 if q%2==0 else 0)
    assert dim==expect,(q,b,c,dim,expect)
    wrong=0
    inside=0
    for x in itertools.product(range(q),repeat=b):
        if sum(signs[i]*x[i] for i in range(b))%q!=c:
            wrong+=1
            delta=encode(x,q)^rows[0]
            for i in sorted(basis,reverse=True):
                if delta & (1<<i):
                    delta ^= basis[i]
            inside += int(delta==0)
    assert wrong==(q-1)*q**(b-1)
    if q%2 and b>=3:
        assert inside==wrong
    if b==2 and q==3: assert inside==0
    if q==2 and b>=3: assert inside==0
    return dict(q=q,b=b,c=c,signs=signs,models=len(sat),
        dimension=dim,expected=expect,free_dimension=b*(q-1),
        wrong=wrong,wrong_in_affine_hull=inside)

def main():
    cases=[]
    for b in range(2,8):
        for c in (0,1,2):
            cases.append(case(3,b,c,tuple((-1)**i for i in range(b))))
    for q,b in ((2,3),(2,5),(4,3),(4,4),(5,3),(5,4),(6,3)):
        for c in (0,1):
            cases.append(case(q,b,c,tuple((-1)**i for i in range(b))))
    assert len(cases)==32
    assert any(x['q']==3 and x['b']==4 and x['c']==1
               and x['wrong']==54 and x['wrong_in_affine_hull']==54 for x in cases)
    data=dict(status='FINITE EXACT GF2 RANK CONTROLS ONLY',
        cases=cases,
        summary=dict(case_count=len(cases),
            total_fiber_points=sum(x['models'] for x in cases),
            total_wrong_examined=sum(x['wrong'] for x in cases)))
    out=Path(__file__).with_name('lspv1_530_affine_boundary_raw.json')
    out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(data['summary'],sort_keys=True))
    print('sha256',hashlib.sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':
    main()
