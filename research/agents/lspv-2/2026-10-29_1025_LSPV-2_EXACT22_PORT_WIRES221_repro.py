#!/usr/bin/env python3
"""LSPV-2 EXACT22-PORT-WIRES221: stdlib, deterministic exhaustive controls.

No external SAT solver or hidden source table. The 20-clause source W1 was
published in the project's signed-puncture-profile218 reproducer. This file
includes every clause and tests all 2^15 assignments. The two 30-variable
joined formulas are independently checked using a fresh DPLL implementation.

Run: python3 exact22_port_wires221.py > raw221.json
"""
from __future__ import annotations
import collections, hashlib, itertools, json

SEED = 'none, deterministic exhaustive'
W1 = (
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))


def clause_key(c):
    return tuple(sorted(c, key=lambda x:(abs(x),x<0)))


def canon(clauses):
    return tuple(sorted(map(clause_key,clauses)))


def base():
    data=[list(c) for c in W1]
    # Mode (0,1) in the prior source: exactly two controlled sign flips.
    for i in (6,11): data[i][0]=-data[i][0]
    C=canon(data)
    assert len(C)==20 and C[2]==(-4,-9,-11) and C[3]==(-4,-8,-11)
    assert C[15]==(4,8,-10) and C[16]==(4,9,-10)
    return C


def is_proper_connected_exact22(C,n):
    if len(C)*3!=4*n or len(set(map(clause_key,C)))!=len(C):return False
    cnt=collections.Counter(l for c in C for l in c)
    if any(cnt[v]!=2 or cnt[-v]!=2 for v in range(1,n+1)):return False
    adj=[set() for _ in range(n+1)]
    for c in C:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(abs(x)>n for x in c):return False
        for x in c:
            adj[abs(x)].update(abs(y) for y in c)
    visited={1};stack=[1]
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in visited:visited.add(v);stack.append(v)
    return len(visited)==n


def lit_true(z,mask):
    return bool(mask>>(abs(z)-1)&1)==(z>0)


def cnf_true(C,mask):
    return all(any(lit_true(z,mask) for z in c) for c in C)


def source_profile(C,slots):
    """All assignments to a 15-variable module punctured at given clauses.

    Return each distinct (port bit, tuple of other-foot values), with exact
    multiplicities and an explicit witness bitmask.
    """
    slots=tuple(sorted(slots))
    counts=collections.Counter();examples={}
    for mask in range(1<<15):
        if not all(any(lit_true(z,mask) for z in C[i])
                   for i in range(20) if i not in slots): continue
        p=(mask>>3)&1
        feet=tuple(int(any(lit_true(z,mask) for z in C[i] if abs(z)!=4))
                   for i in slots)
        sig=(p,)+feet
        counts[sig]+=1
        examples.setdefault(sig,mask)
    return {'slots':slots,'counts':counts,'examples':examples}


def offset(c,amount):
    return tuple((1 if z>0 else -1)*(abs(z)+amount) for z in c)


def make_pair(kind):
    assert kind in ('eq','xor')
    C=base()
    blocks=[[list(offset(cl,15*j)) for cl in C] for j in range(2)]
    if kind=='eq':
        # Swap ONE negative x4 occurrence (both source clauses C[2]).
        assert blocks[0][2][0]==-4 and blocks[1][2][0]==-19
        blocks[0][2][0]=-19
        blocks[1][2][0]=-4
    else:
        # Balance BOTH cross-polarity substitutions: (-4,+19), (+4,-19).
        # Every variable retains two positive and two negative incidences.
        assert blocks[0][2][0]==-4 and blocks[0][15][0]==4
        assert blocks[1][2][0]==-19 and blocks[1][15][0]==19
        blocks[0][2][0]=19
        blocks[1][15][0]=-4
        blocks[0][15][0]=-19
        blocks[1][2][0]=4
    out=canon(cl for block in blocks for cl in block)
    assert is_proper_connected_exact22(out,30)
    return out


def make_eq_path(k):
    assert k>=2
    C=base()
    blocks=[[list(offset(cl,15*j)) for cl in C] for j in range(k)]
    for j in range(k-1):
        # Each vertex has exactly two available negative occurrences of its
        # signal variable. Left edge uses slot 2, right edge uses slot 3.
        assert blocks[j][3][0]==-(15*j+4)
        assert blocks[j+1][2][0]==-(15*(j+1)+4)
        blocks[j][3][0]=-(15*(j+1)+4)
        blocks[j+1][2][0]=-(15*j+4)
    out=canon(cl for block in blocks for cl in block)
    assert is_proper_connected_exact22(out,15*k)
    return out


def dimacs(C,n):
    return (f'p cnf {n} {len(C)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode('ascii')


def equality_child():
    # Ordinary proper ternary CNF equivalent pointwise to (a <=> b),
    # independent of auxiliary u,v. Pins/source are NOT carried forward.
    return canon([(-1,2,3),(-1,2,-3),(1,-2,4),(1,-2,-4)])


def sat_dpll(C,pins):
    """Independent deterministic unit-propagating DPLL, returns witness/calls.

    This uses the *actual joint 30-variable 3CNF*, not the puncture formula.
    Only small k=2 and k=3 controls are tested.
    """
    calls=[0]
    vars_=set(abs(z) for c in C for z in c)
    def solve(C,assignment):
        calls[0]+=1
        while True:
            residual=[];units=[]
            for clause in C:
                if any((assignment.get(abs(z)) is not None and
                        assignment[abs(z)]==(z>0)) for z in clause):continue
                alive=[z for z in clause if abs(z) not in assignment]
                if not alive:return None
                residual.append(alive)
                if len(alive)==1:units.append(alive[0])
            if not residual:return dict(assignment)
            if not units:break
            for u in units:
                x=abs(u);bit=(u>0)
                if x in assignment and assignment[x]!=bit:return None
                assignment[x]=bit
        freq=collections.Counter(abs(z) for cl in residual for z in cl)
        x=max(freq, key=lambda y:(freq[y],-y))
        for bit in (False,True):
            new=dict(assignment);new[x]=bit
            ans=solve(C,new)
            if ans is not None:return ans
        return None
    r=solve(C,dict(pins))
    if r is not None:
        for v in vars_:r.setdefault(v,False)
        assert all(any(r[abs(z)]==(z>0) for z in c) for c in C)
    return r,calls[0]


def exact_pair_projection(C,kind):
    # Exact independent cofactor checks with full 30-var source.
    obs={};total_calls=0
    for a,b in itertools.product((0,1),repeat=2):
        sol,ncalls=sat_dpll(C,{4:bool(a),19:bool(b)})
        expected=(a==b) if kind=='eq' else (a!=b)
        assert (sol is not None)==expected,(kind,a,b,ncalls)
        obs[f'{a}{b}']={'sat':sol is not None,'dpll_calls':ncalls,
                         'witness_integer':sum((1<<(v-1)) for v in range(1,31) if sol and sol.get(v,False)) if sol else None}
        total_calls+=ncalls
    return obs,total_calls


def negative_controls(C):
    altered=list(C)
    v=list(altered[0]);v[0]=-v[0];altered[0]=tuple(v)
    assert not is_proper_connected_exact22(altered,15)
    wrong_pair=list(make_pair('eq'))
    z=list(wrong_pair[0]);z[0]=-z[0];wrong_pair[0]=tuple(z)
    assert not is_proper_connected_exact22(wrong_pair,30)
    return {'single_sign_flip_rejected':True,'source_degree_damage_rejected':True}


def main():
    C=base()
    assert is_proper_connected_exact22(C,15)
    full={};full_counts=collections.Counter();first={}
    for mask in range(1<<15):
        if cnf_true(C,mask):
            triple=((mask>>3)&1,(mask>>7)&1,(mask>>8)&1)
            full_counts[triple]+=1
            first.setdefault(triple,mask)
    assert dict(full_counts)=={(0,1,1):153,(1,0,0):119}
    assert sum(full_counts.values())==272
    for slots in ((2,),(3,),(15,),(16,),(2,3),(2,15),(3,16)):
        x=source_profile(C,slots)
        # Puncture implications relevant to each admissible splice.
        if set(slots).issubset({2,3}):
            assert all(not (signature[0]==0 and any(signature[1:]))
                       for signature in x['counts'])
        full[','.join(map(str,slots))]={
            'states':{','.join(map(str,k)):v for k,v in sorted(x['counts'].items())},
            'witnesses':{','.join(map(str,k)):v for k,v in sorted(x['examples'].items())},
            'puncture_models':sum(x['counts'].values())}
    # Two joint formulas, exact 2-port truth table from independent DPLL.
    pair_result={}
    for kind in ('eq','xor'):
        joint=make_pair(kind)
        obs,steps=exact_pair_projection(joint,kind)
        pair_result[kind]={
            'variables':30,'clauses':40,'physical_bits':8*len(dimacs(joint,30)),
            'cofactor_tests':obs,'dpll_calls':steps,
            'source_sha256':hashlib.sha256(dimacs(joint,30)).hexdigest()}
    # Pure-negative equality path: all ports equal by exact local signatures,
    # and both common-bit assignments extend via original full witnesses.
    paths=[]
    for k in (2,3,4,5,8,16,32,64,128):
        path=make_eq_path(k)
        if k<=3:
            for a,b in itertools.product((0,1),repeat=2):
                sol,_=sat_dpll(path,{4:bool(a),15*(k-1)+4:bool(b)})
                assert (sol is not None)==(a==b)
        paths.append({'k':k,'n':15*k,'m':20*k,
                      'physical_bits':8*len(dimacs(path,15*k))})
    child=equality_child()
    assert len(child)==4
    eq_child_bits=8*len(dimacs(child,4))
    # exact ordinary 3CNF pointwise evaluation across a,b,aux.
    for a,b,c,d in itertools.product((0,1),repeat=4):
        aa={1:bool(a),2:bool(b),3:bool(c),4:bool(d)}
        got=all(any(aa[abs(z)]==(z>0) for z in clause) for clause in child)
        assert got==(a==b)
    for t in paths:
        t['ordinary_eq_child_bits']=eq_child_bits
        t['power_short_3_4']=eq_child_bits <= t['physical_bits']**.75
    # Exact source audit source-preserving, replicated separately by runner.
    out={'status':'PASS','run':'LSPV-2 EXACT22-PORT-WIRES221',
         'source':'W1 15-variable 20-clause signed (2,2) exact gadget; mode (0,1)',
         'seed':SEED,'source_exact_15var_models':272,
         'three_port_counts':{''.join(map(str,k)):v for k,v in sorted(full_counts.items())},
         'three_port_first_witness':{''.join(map(str,k)):v for k,v in sorted(first.items())},
         'puncture_profiles':full,'joint_pair_results':pair_result,
         'equality_paths':paths,'ordinary_equality_child':{
             'clauses':[list(x) for x in child], 'bits':eq_child_bits},
         'negative_controls':negative_controls(C),
         'source_sha256':hashlib.sha256(dimacs(C,15)).hexdigest(),
         'limitations':[
             'The source equality/inequality gadget is a fixed 15-variable finite control; no general SAT hardness follows.',
             'Two-copy connected formulas are strict signed exact-(2,2), but their four-clause ordinary equality projection is not strict exact-(2,2).',
             'Equality paths use negative slots 2,3 only; arbitrary branching and mixed-sign repeated splice closure is not proved.',
             'No port-preserving regularizer for arbitrary 3CNF, unrestricted SAT shrinker, or separation is supplied.',
             'DPLL finite cross-checks are not a kernel-verified proof; mathematical lifting relies on exact finite puncture tables.']}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()