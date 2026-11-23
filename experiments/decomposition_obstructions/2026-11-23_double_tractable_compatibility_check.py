#!/usr/bin/env python3
"""Exact 3SAT -> (2CNF) AND (GF2) red-team, standard Python only.
Every 3SAT instance maps to two separately satisfiable components.
Run: python3 obstruction_compact_checker_20261123.py
"""
import itertools as it
import json
import random

def lit_true(lit, bits):
    b=bits[abs(lit)-1]
    return b==int(lit>0)

def cnf_true(cnf,bits):
    return all(any(lit_true(l,bits) for l in c) for c in cnf)

def encode(cnf,n):
    binary=[];parity=[]
    for i,c in enumerate(cnf):
        assert len(c)==3
        ys=[n+3*i+j+1 for j in range(3)]
        binary.extend([(-ys[a],-ys[b]) for a,b in it.combinations(range(3),2)])
        binary.extend([(-ys[j],c[j]) for j in range(3)])
        parity.append((ys,1))
    return n+3*len(cnf),binary,parity

def parity_true(rows,bits):
    return all(sum(bits[v-1] for v in ys)%2==rhs for ys,rhs in rows)

def original_count(cnf,n):
    return sum(cnf_true(cnf,x) for x in it.product((0,1),repeat=n))

def joint_count_by_originals(cnf,n):
    result=0
    for x in it.product((0,1),repeat=n):
        ways=1
        for c in cnf:
            ways*=sum(lit_true(l,x) for l in c)
        result+=ways
    return result

def joint_bruteforce(cnf,n):
    N,B,P=encode(cnf,n)
    assert N<=15
    return sum(cnf_true(B,z) and parity_true(P,z)
               for z in it.product((0,1),repeat=N))

def subsystem_controls(cnf,n):
    N,B,P=encode(cnf,n)
    zero=(0,)*N
    affine=list(zero)
    for i in range(len(cnf)):
        affine[n+3*i]=1
    assert cnf_true(B,zero)
    assert parity_true(P,affine)
    assert len(B)==6*len(cnf) and len(P)==len(cnf)
    return N

def random_cnf(n,m,rng,planted=None):
    F=[]
    while len(F)<m:
        names=rng.sample(range(1,n+1),3)
        c=tuple(v if rng.getrandbits(1) else -v for v in names)
        if planted is not None and not any(lit_true(l,planted) for l in c):
            continue
        F.append(c)
    return F

def main():
    signs=[tuple(v if b else -v for v,b in zip((1,2,3),p))
           for p in it.product((0,1),repeat=3)]
    all_subformulas=0;full_joint=0
    for mask in range(256):
        F=[signs[j] for j in range(8) if mask>>j&1]
        subsystem_controls(F,3)
        assert (original_count(F,3)>0)==(joint_count_by_originals(F,3)>0)
        # Every 3CNF is a conjunction of two individually SAT tractable CNFs.
        horn=[c for c in F if sum(l>0 for l in c)<=1]
        dual=[c for c in F if sum(l>0 for l in c)>=2]
        assert cnf_true(horn,(0,0,0)) and cnf_true(dual,(1,1,1))
        if len(F)<=3:
            assert joint_bruteforce(F,3)==joint_count_by_originals(F,3)
            full_joint+=1
        all_subformulas+=1
    core=[]
    for omitted in [None]+list(range(8)):
        F=signs if omitted is None else signs[:omitted]+signs[omitted+1:]
        models=original_count(F,3)
        extensions=joint_count_by_originals(F,3)
        assert (models,extensions)==((0,0) if omitted is None else (1,24))
        core.append({'omitted':omitted,'m':len(F),'source_models':models,
                     'mixed_models':extensions,'selector_interface':3*len(F),
                     'affine_rank':len(F)})
    rng=random.Random(20261123)
    random_controls=[]
    for n in (3,4,5,6,7,8):
        for m in (3,6,9,12):
            for plant in (False,True):
                x=tuple(rng.getrandbits(1) for _ in range(n)) if plant else None
                F=random_cnf(n,m,rng,x)
                subsystem_controls(F,n)
                a=original_count(F,n)
                b=joint_count_by_originals(F,n)
                assert (a>0)==(b>0)
                if plant:assert a>0
                random_controls.append({'n':n,'m':m,'sat':a>0,'source_models':a,'mixed_models':b})
    near_threshold=[]
    for n in (8,10,12,14):
        for case in range(4):
            m=round(4.3*n)
            F=random_cnf(n,m,rng)
            subsystem_controls(F,n)
            a=original_count(F,n)
            b=joint_count_by_originals(F,n)
            assert (a>0)==(b>0)
            near_threshold.append({'n':n,'m':m,'case':case,'sat':a>0,
                                   'source_models':a,'mixed_models':b})
    residual_controls=[]
    for n in range(1,13):
        # F_n = conjunction (x_i OR y_i); assigning x yields 2^n residuals.
        residuals={tuple(i for i,b in enumerate(x) if b==0)
                   for x in it.product((0,1),repeat=n)}
        assert len(residuals)==2**n
        residual_controls.append({'n':n,'residuals':len(residuals)})
    clique_controls=[]
    for n in (3,5,8,12,20):
        # 2CNF equalities between all pairs; primal graph is K_n.
        clauses=[c for i,j in it.combinations(range(1,n+1),2)
                 for c in ((-i,j),(i,-j))]
        assert cnf_true(clauses,(0,)*n) and cnf_true(clauses,(1,)*n)
        clique_controls.append({'n':n,'treewidth':n-1,'clauses':len(clauses)})
    output={'status':'PASS','subformulas_checked':all_subformulas,
            'independent_full_joint_cases':full_joint,
            'random_controls':len(random_controls),
            'near_threshold_both_labels':{'sat':sum(x['sat'] for x in near_threshold),
                                          'unsat':sum(not x['sat'] for x in near_threshold)},
            'minimal_unsat_core_and_neighbors':core,
            'near_threshold_examples':near_threshold,
            'residual_controls':residual_controls,'clique_controls':clique_controls,
            'scope':'finite checks; complexity implication proved separately by gadget reduction'}
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
