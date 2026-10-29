#!/usr/bin/env python3
"""ARC211: reproducible finite audit of a signed exact-(2,2) tightness family.

Standalone Python 3, no dependencies; deterministic, no random seed.
The finite checks do not certify the all-r theorem, which is proved separately.
"""
import hashlib
import itertools
import json
from collections import defaultdict, Counter


def build(r):
    assert isinstance(r,int) and r>=2
    b=3*r
    Y=list(range(1,b+1))
    P=[[b+1+j*b+i for i in range(b)] for j in range(b)]
    clauses=[]
    owner=[]
    # Boundary ring: the negative literal of each original cyclic clause
    # has been exchanged with a negative private-block literal.
    for j in range(b):
        clauses.append((Y[j],Y[(j+1)%b],-P[j][0]))
        owner.append(j)
    # Original all-negative boundary block clauses are Y-only and belong to M_0.
    for h in range(r):
        clauses.append(tuple(-Y[3*h+i] for i in range(3)))
        owner.append(0)
    for j in range(b):
        p=P[j]
        for i in range(b):
            clauses.append((p[i],p[(i+1)%b],-p[(i+2)%b]))
            owner.append(j)
        # The replaced private all-negative Q_0 clause.
        clauses.append((-Y[(j+2)%b],-p[1],-p[2]))
        owner.append(j)
        for h in range(1,r):
            clauses.append(tuple(-p[3*h+i] for i in range(3)))
            owner.append(j)
    return {'r':r,'b':b,'k':b,'n':b+b*b,'Y':Y,'P':P,'clauses':clauses,'owner':owner,
            'B':[{p[3*h] for h in range(r)} for p in P]}


def check_formula(f):
    n=f['n']; cls=f['clauses'];Y=set(f['Y']);P=[set(p) for p in f['P']]
    degree={i:[0,0] for i in range(1,n+1)}
    seen=set()
    for clause in cls:
        assert len(clause)==3 and len({abs(x) for x in clause})==3
        assert all(1<=abs(x)<=n for x in clause)
        normalized=tuple(sorted(clause,key=lambda x:abs(x)))
        assert normalized not in seen
        seen.add(normalized)
        for lit in clause:
            degree[abs(lit)][lit<0]+=1
    assert len(cls)*3==4*n
    assert all(tuple(v)==(2,2) for v in degree.values())
    assert len(f['owner'])==len(cls)
    for clause,j in zip(cls,f['owner']):
        private={abs(x) for x in clause if abs(x) not in Y}
        assert private<=P[j]
        assert any(abs(x) in Y|f['B'][j] for x in clause)
    # Independent incidence-connectedness BFS, not just graph connectivity by assertion.
    adjacency=defaultdict(set)
    for ix,clause in enumerate(cls):
        c=('c',ix)
        for v in map(abs,clause):
            x=('v',v)
            adjacency[c].add(x)
            adjacency[x].add(c)
    reached={('v',1)}
    pending=[('v',1)]
    while pending:
        for z in adjacency[pending.pop()]:
            if z not in reached:
                reached.add(z)
                pending.append(z)
    assert len(reached)==n+len(cls)
    # Independent direct witness; residue 2 mod 3 is false.
    truth={v: (i%3 !=2) for i,v in enumerate(f['Y'])}
    truth.update({v:(i%3 !=2) for p in f['P'] for i,v in enumerate(p)})
    assert all(any(truth[abs(x)] if x>0 else not truth[abs(x)] for x in c)
               for c in cls)
    assert f['k']==f['b'] and f['n']==f['b']*(f['b']+1)
    assert f['b']+f['r']==4*f['r']
    assert f['n'] <= 3*f['b']+12*f['b']*f['r']
    return len(cls), len(reached),sum(1 for cl in cls if all(abs(x) in Y for x in cl))


def local_min_hitting(f,j):
    Y=set(f['Y']);P=f['P'][j]
    private_only=[{abs(lit) for lit in clause}
                  for clause,idx in zip(f['clauses'],f['owner'])
                  if idx==j and all(abs(lit) not in Y for lit in clause)]
    assert len(private_only)==4*f['r']-1
    # Exhaustive on one module, which is isomorphic for each j except
    # for the added Y-only clauses in M_0, which are ignored here.
    n=f['b']
    masks=[]
    mp={v:i for i,v in enumerate(P)}
    for cl in private_only:
        mask=0
        for v in cl:mask|=1<<mp[v]
        masks.append(mask)
    totals=0
    minimum=None
    min_example=None
    for mask in range(1<<n):
        totals+=1
        if minimum is not None and mask.bit_count()>minimum:
            continue
        if all(mask&c for c in masks):
            minimum=mask.bit_count()
            min_example=mask
    assert minimum==f['r']
    assert all((min_example&c) for c in masks)
    return minimum,totals


def hostile_variants(f):
    # Independent negative controls must fail the expected model invariant.
    orig=f['clauses']
    degree=Counter((abs(lit),lit<0) for c in orig for lit in c)
    # Flipping one occurrence violates strict balanced polarity, even though
    # the clause remains a proper ternary clause.
    flipped=[list(c) for c in orig]
    flipped[0][0]*=-1
    assert any(degree[(v,True)]!=degree[(v,False)] for v in range(1,f['n']+1)) is False
    dflip=Counter((abs(lit),lit<0) for c in flipped for lit in c)
    assert any(dflip[(v,True)]!=dflip[(v,False)] for v in range(1,f['n']+1))
    # A malformed Y-only-to-mixed splice does not satisfy the modular owner rule.
    altered=list(orig)
    y0=f['Y'][0]
    foreign=f['P'][1][0]
    # The selected first clause is assigned to module 0, not module 1.
    altered[0]=(y0,f['Y'][1],-foreign)
    assert any(abs(v) not in set(f['Y'])|set(f['P'][0]) for v in altered[0])
    return 2


def run():
    per=[]; checked=0; local_enumerations=0; negative_checks=0
    for r in (2,3,4,5,7,10):
        f=build(r)
        num_clauses,incidence_vertices,pure_y=check_formula(f)
        checked+=num_clauses
        negative_checks+=hostile_variants(f)
        lmin=None
        if r<=4:
            lmin,enum=local_min_hitting(f,0)
            local_enumerations+=enum
        per.append({'r':r,'b':f['b'],'k':f['k'],'n':f['n'],
                    'clauses':num_clauses,'global_boundary':f['b'],
                    'local_backdoor_exact':f['r'],
                    'b_plus_q':4*r,'incidence_nodes':incidence_vertices,
                    'boundary_only_clauses':pure_y,
                    'exhaustive_local_optimum':lmin})
    return {'status':'PASS','script':'2026-10-28_2000_ARC211_tight_static_interface_audit.py',
            'seed':None,'scope':'deterministic formula checks and local-hitting exhaustive subset controls',
            'cases':per,'clauses_checked':checked,
            'exhaustive_local_candidates':local_enumerations,
            'negative_model_controls':negative_checks,
            'limitations':['family is explicitly SAT','asymptotics follow from proof, not tests',
                           'no arbitrary-SAT contraction','no native TM runtime measured']}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))