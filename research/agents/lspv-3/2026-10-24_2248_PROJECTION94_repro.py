#!/usr/bin/env python3
"""Finite exact checks for source-name-preserving existential interface joins.
The polynomial-size witness-lift circuit theorem is conditional on P=NP;
these finite exhaustive controls are not evidence of the hypothesis.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SEED=20261024
rng=random.Random(SEED)
checks=0
counts={'SAT':0,'UNSAT':0,'random':0,'controls':0,'grouped':0,'identity_rejection':0,'witness_lifts':0}
logical={'source_clauses_checked':0,'candidate_assignments':0,'projection_queries':0}

def check(pred,label):
    global checks
    checks+=1
    if not pred: raise AssertionError(label)

def clause_true(clause,assignment):
    logical['source_clauses_checked']+=1
    return any((assignment[abs(v)] if v>0 else not assignment[abs(v)]) for v in clause)

def formula_true(clauses,assignment):
    return all(clause_true(c,assignment) for c in clauses)

def solver(clauses,variable_ids,fixed):
    """Exhaustive finite oracle for testing, not a polynomial-time solver."""
    rest=tuple(x for x in sorted(variable_ids) if x not in fixed)
    for bits in itertools.product((0,1),repeat=len(rest)):
        logical['candidate_assignments']+=1
        a=dict(fixed);a.update(zip(rest,bits))
        if formula_true(clauses,a): return a
    return None

def unit3(x,value,a,b):
    l=x if value else -x
    return [(l,ka*a,kb*b) for ka,kb in itertools.product((1,-1),repeat=2)]

def xor3(x,y,z,rhs):
    return [tuple(v if bit==0 else -v for v,bit in zip((x,y,z),bits))
            for bits in itertools.product((0,1),repeat=3) if (sum(bits)%2)!=rhs]

def padded2(x,y,p):
    return [(x,y,p),(x,y,-p)]

def sample_case(caseid,kind='random'):
    m=3
    common=(1,2)
    ys=[(3,4),(5,6),(7,8)]
    clauses=[];mods=[]
    for i in range(m):
        allowed=common+ys[i]
        cs=[]
        if kind=='random':
            for _ in range(rng.randint(2,7)):
                tri=rng.sample(list(allowed),3)
                cs.append(tuple(v*(1 if rng.getrandbits(1) else -1) for v in tri))
        elif kind=='affine':
            cs=xor3(common[0],ys[i][0],ys[i][1],(caseid+i)%2)
        elif kind=='horn':
            cs=[(-common[0],-ys[i][0],ys[i][1]),(-common[1],ys[i][0],ys[i][1])]
        elif kind=='2sat':
            cs=padded2(common[0],-common[1],ys[i][0])
        elif kind=='units':
            cs=unit3(common[0],(caseid+i)%2,*ys[i])
        elif kind=='easy':
            cs=[(common[0],ys[i][0],ys[i][1])]
        for c in cs: check(len({abs(v) for v in c})==3,'proper clause')
        clauses+=cs;mods.append((cs,set(common+ys[i]),set(ys[i])))
    return clauses,mods,set(common),set(range(1,9))

def validate(mods,boundary):
    seen=set()
    for clauses,varset,priv in mods:
        if not priv<=varset or not priv.isdisjoint(boundary) or not priv.isdisjoint(seen):
            return False
        seen |= priv
        for clause in clauses:
            if any(abs(lit) not in varset for lit in clause): return False
    return True

def audit_case(caseid,kind):
    clauses,mods,B,V=sample_case(caseid,kind)
    check(validate(mods,B),'valid private-disjoint decomposition')
    direct=solver(clauses,V,{})
    root=None
    for bb in itertools.product((0,1),repeat=len(B)):
        named=dict(zip(sorted(B),bb));lifts=[]
        for cs,vars_i,_ in mods:
            logical['projection_queries']+=1
            lifted=solver(cs,vars_i,named)
            if lifted is None: break
            lifts.append(lifted)
        else:
            global_witness=dict(named)
            for lift in lifts: global_witness.update(lift)
            check(formula_true(clauses,global_witness),'global witness validates')
            counts['witness_lifts']+=1
            root=global_witness
            break
    check((direct is not None)==(root is not None),'source-named exact join')
    check((direct is None) == (root is None),'SAT/UNSAT label')
    if root is None:counts['UNSAT']+=1
    else:counts['SAT']+=1
    group01=mods[0][0]+mods[1][0]
    groupV=mods[0][1]|mods[1][1]
    groot=None
    for bb in itertools.product((0,1),repeat=len(B)):
        named=dict(zip(sorted(B),bb))
        a=solver(group01,groupV,named)
        b=solver(mods[2][0],mods[2][1],named)
        if a is not None and b is not None:
            groot=dict(a);groot.update(b)
            break
    check((groot is not None)==(direct is not None),'two-level grouped identity')
    if groot is not None:check(formula_true(clauses,groot),'two-level witness')
    counts['grouped']+=1
    if kind=='random':counts['random']+=1
    else:counts['controls']+=1

def structural_countercontrols():
    F1=unit3(1,1,2,3)
    F2=unit3(1,0,4,5)
    check(solver(F1,{1,2,3},{}) is not None,'first locally SAT')
    check(solver(F2,{1,4,5},{}) is not None,'second locally SAT')
    check(solver(F1+F2,{1,2,3,4,5},{}) is None,'global UNSAT requires name coherence')
    F2_independent=[tuple(6 if x==1 else (-6 if x==-1 else x) for x in c) for c in F2]
    check(solver(F1+F2_independent,{1,2,3,4,5,6},{}) is not None,'anonymous local copies falsely SAT')
    counts['identity_rejection']+=1
    bad=[(unit3(1,1,2,3),{1,2,3},{2,3}),
         (unit3(1,0,3,4),{1,3,4},{3,4})]
    check(not validate(bad,{1}),'untracked private-variable overlap rejected')
    counts['identity_rejection']+=1
    for values in itertools.product((0,1),repeat=4):
        x,a,b,c=values
        guarded=((not x) or a or False) or (b or c)
        enc=any(((not x) or a or u) and ((not u) or b or c) for u in (0,1))
        check(bool(guarded)==bool(enc),'guarded elimination')

def main():
    structural_countercontrols()
    for i in range(256): audit_case(i,'random')
    for k in ('affine','horn','2sat','units','easy'):
        for i in range(20): audit_case(i,k)
    data={'tag':'PROJECTION_LIFT_JOIN94','classification':'COMPUTATIONAL finite tests only',
          'seed':SEED,'checks':checks,'cases':counts,'logical_operation_counts':logical,
          'P_vs_NP':'OPEN','notes':['brute-force finite oracle is NOT a P=NP witness',
          'logical clause count is NOT a measured FLMV bit-TM instruction count',
          'conditional P=NP uniform circuit/witness-lift theorem proved separately']}
    output=ROOT/'PROJECTION94_raw.json'
    output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
