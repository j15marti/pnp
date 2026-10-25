#!/usr/bin/env python3
"""ARC-STAGE-EXCHANGE168: exact rational stage-order proof checks and real
ordinary-CNF SAT/UNSAT descendants.  Python 3 standard library only.

Usage: python 2026-10-25_0454_ARC_STAGE_EXCHANGE168_repro.py OUTPUT.json
The counters are logical source/serialized-bit accounting proxies, NOT a
physical FLMV random-access Turing machine trace or a complexity proof.
"""
from __future__ import annotations
import itertools
import hashlib
import json
import random
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

SEED = 202610250454
rng = random.Random(SEED)
checks = Counter()

def audit(pred, key):
    checks[key] += 1
    if not pred:
        raise AssertionError(key)


def stage(a, lam, r=0, g=0, eta=0, name=''):
    return {'name':name,'a':Q(a),'lam':Q(lam),'r':Q(r),'g':Q(g),'eta':Q(eta)}


def guest_exponent(order, t):
    exponent = Q(0)
    scale = Q(1)
    for st in order:
        exponent += scale*st['a']
        scale *= st['lam']
    return exponent + scale*Q(t)


def envelope(order, t, s, kappa=0):
    """Fully eager depth-first upper certificate, conditional on EXACT semantics."""
    scale, calls, costs = Q(1), Q(0), []
    space = Q(kappa)
    for st in order:
        previous_scale, previous_calls = scale, calls
        calls += scale*st['a']
        scale *= st['lam']
        costs.extend([previous_calls+previous_scale*st['r'],
                      calls+scale+previous_scale*st['g']])
        space = max(space,scale,previous_scale*st['eta'])
    costs.append(calls+scale*Q(t))
    space = max(space,scale*Q(s))
    return max(costs), space, {'calls':calls,'leaf_scale':scale,'costs':costs}


def sort_rule(st):
    return st['a']/(1-st['lam'])

# Exhaustive rational tests of adjacent interchange and global sorting.
rat = [Q(0),Q(1,10),Q(1,4),Q(1,2),Q(3,5),Q(4,5)]
lam = [Q(1,4),Q(1,2),Q(2,3),Q(4,5)]
for k in [2,3,4,5]:
    for trial in range(150):
        ops = [stage(rng.choice(rat),rng.choice(lam),name=str(i)) for i in range(k)]
        sorted_order = sorted(ops,key=sort_rule)
        sorted_guest = guest_exponent(sorted_order,Q(2))
        all_guest = [guest_exponent(p,Q(2)) for p in itertools.permutations(ops)]
        audit(sorted_guest==min(all_guest),'sorted_global_minimum')
        for i in range(k-1):
            p = list(ops)
            before = guest_exponent(p,Q(3))
            left,right=p[i],p[i+1]
            prefix=Q(1)
            for x in p[:i]:prefix*=x['lam']
            delta = prefix*(left['a']*(1-right['lam'])-right['a']*(1-left['lam']))
            p[i],p[i+1] = p[i+1],p[i]
            audit(before-guest_exponent(p,Q(3))==delta,'adjacent_swap_identity')

X=stage(Q(3,5),Q(1,2),r=1,name='X')
Y=stage(Q(1,10),Q(4,5),r=2,name='Y')
xy=envelope([X,Y],2,1)
yx=envelope([Y,X],2,1)
audit(sort_rule(Y)<sort_rule(X),'guest_sorted_Y_first')
audit(yx[2]['calls']<xy[2]['calls'],'guest_fanout_Y_first_better')
audit(xy[0]<yx[0] and xy[1]<yx[1],'full_joint_certificate_X_first_better')

# DIMACS encoding/decoding is a real ordinary-CNF child input, not a pointer.
def encode(cnf):
    declared = max((abs(v) for clause in cnf for v in clause), default=0)
    rows = [f'p cnf {declared} {len(cnf)}']
    rows.extend(' '.join(map(str,c))+' 0' for c in cnf)
    return ('\n'.join(rows)+'\n').encode('ascii')

def decode(data):
    rows=data.decode('ascii').splitlines()
    if not rows or len(rows[0].split())!=4:
        raise ValueError('missing header')
    header=rows[0].split()
    if header[:2]!=['p','cnf']:
        raise ValueError('bad header')
    n,m=map(int,header[2:]); result=[]
    for ln in rows[1:]:
        lits=list(map(int,ln.split()))
        if not lits or lits[-1]!=0 or any(v==0 for v in lits[:-1]):
            raise ValueError('bad record')
        clause=tuple(lits[:-1])
        if any(abs(v)>n for v in clause):
            raise ValueError('invalid variable')
        result.append(clause)
    if len(result)!=m:
        raise ValueError('mismatch')
    return tuple(result)

def restrict(cnf, var, value, meter):
    """Unit Shannon restriction without semantic SAT oracle."""
    out=[]
    for clause in cnf:
        reduced=[]; hit=False
        for l in clause:
            meter['literal_tests']+=1
            if abs(l)==var:
                meter['pin_tests']+=1
                if (l>0)==bool(value):hit=True
            else:
                reduced.append(l)
                meter['retained_literal_writes']+=1
        if not hit:out.append(tuple(reduced))
        else:meter['satisfied_clause_deletions']+=1
    return tuple(out)

def brute_sat(cnf):
    vs=sorted({abs(v) for c in cnf for v in c})
    for bits in itertools.product((False,True),repeat=len(vs)):
        assignment=dict(zip(vs,bits))
        if all(any((l>0)==assignment[abs(l)] for l in c) for c in cnf):
            return True
    return False

def guard_formula(repetitions, good_quadrant):
    clauses=[]
    # Each quadrant has independent payload names: one residual literal pair.
    for xb,yb in itertools.product((False,True),repeat=2):
        lx = -1 if xb else 1  # false when guard x=xb
        ly = -2 if yb else 2  # false when guard y=yb
        for j in range(repetitions):
            z=3+((int(xb)*2+int(yb))*repetitions+j)
            clauses.append((lx,ly,z))
            if (xb,yb)!=good_quadrant:
                clauses.append((lx,ly,-z))
    return tuple(clauses)

controls=[('empty',()),('unit_yes',((1,),)),
          ('unit_no',((1,),(-1,))),
          ('krom',((1,2),(-1,3),(-2,-3))),
          ('horn',((-1,-2,3),(-3,4))),
          ('dual_horn',((1,2,-3),(3,-4))),
          ('affine_xor_unsat',((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3),
                               (-1,-2,-3),(-1,2,3),(1,-2,3),(1,2,-3))),
          ('disconnected',((1,2),(3,4))),
          ('padding',((1,2),(5,-5))),
          ('shared_join_false',((1,),(-1,)))]
for copies in (1,2):
    for good in (None,(False,False),(False,True),(True,False),(True,True)):
        controls.append((f'guard_{copies}_{good}',guard_formula(copies,good)))

counts=Counter(); rows=[]
for label,clauses in controls:
    original=encode(clauses)
    audit(decode(original)==clauses,'root_encode_roundtrip')
    expected=brute_sat(clauses)
    leaf_vectors=[]
    for order in [(1,2),(2,1)]:
        meter=Counter(); row={'order':list(order),'levels':[],'leaf_labels':[]}
        # A real full first layer and a real second layer, no free recursive oracle.
        first=[]
        for b in (False,True):
            child=restrict(decode(original),order[0],b,meter)
            child_data=encode(child)
            audit(decode(child_data)==child,'first_ordinary_roundtrip')
            meter['parent_source_bytes_read']+=len(original)
            meter['ordinary_child_bytes_written']+=len(child_data)
            first.append((child_data,b))
            row['levels'].append({'depth':1,'source_pin':order[0],
                                  'bit':int(b),'child_bytes':len(child_data)})
            counts['first_children']+=1
        leaves=[]
        for child_data,b in first:
            for c in (False,True):
                grand=restrict(decode(child_data),order[1],c,meter)
                grand_data=encode(grand)
                audit(decode(grand_data)==grand,'second_ordinary_roundtrip')
                meter['child_source_bytes_read']+=len(child_data)
                meter['ordinary_grandchild_bytes_written']+=len(grand_data)
                label_bit=brute_sat(decode(grand_data))
                leaves.append((b,c,label_bit,grand_data))
                row['leaf_labels'].append({'first':int(b),'second':int(c),
                                           'SAT':label_bit,'bytes':len(grand_data)})
                counts['second_children']+=1
                counts['actual_leaf_decisions']+=1
        joined=any(z[2] for z in leaves)
        audit(joined==expected,'two_level_shannon_equivalence')
        audit(len(first)==2 and len(leaves)==4,'two_real_levels')
        leaf_vector={(dict(zip(order,(b,c)))[1],dict(zip(order,(b,c)))[2]):int(sat)
                     for b,c,sat,_ in leaves}
        leaf_vectors.append(leaf_vector)
        counts['source_bytes_read']+=meter['parent_source_bytes_read']+meter['child_source_bytes_read']
        counts['ordinary_bytes_written']+=meter['ordinary_child_bytes_written']+meter['ordinary_grandchild_bytes_written']
        counts['literal_tests']+=meter['literal_tests']
        counts['unchanged_literal_writes']+=meter['retained_literal_writes']
        counts['root_label_SAT' if expected else 'root_label_UNSAT']+=1
        row['meters']=dict(meter)
        if label.startswith('guard_'):
            # Finite factor shrink DOES NOT constitute lambda<1 asymptotically.
            audit(all(z['child_bytes']<len(original) for z in row['levels']),
                  'guard_first_child_strict_byte_shrink')
        if len(rows)<12:rows.append({'name':label,'root_SAT':expected,'root_bytes':len(original),
                                    'first_and_second':row})
    audit(leaf_vectors[0]==leaf_vectors[1],'interchange_leaf_assignment_invariance')

# Hostile case: independently satisfiable children may have UNSAT conjunction.
a=((1,),);b=((-1,),)
audit(brute_sat(a) and brute_sat(b) and not brute_sat(a+b),'shared_variable_join_counterexample')

# Failure mode: constant-size branching leaves Theta(N) full encoded formulas.
for r in (1,2,3,4,6):
    orig=encode(guard_formula(r,None)); met=Counter()
    child=encode(restrict(decode(orig),1,0,met))
    grand=encode(restrict(decode(child),2,0,met))
    audit(0<len(grand)<len(child)<len(orig),'linear_guard_length_chain')
    counts['length_examples']+=1

report={'run':'ARC-STAGE-EXCHANGE168','timestamp_local':'2026-10-25 04:54 PDT',
        'method':'Exact Fraction permutation identities; exhaustive truth evaluation of bounded ordinary CNF roots and fully serialized two genuine Shannon levels',
        'seed':SEED,'status':'COMPUTATIONAL finite controls; conditional algebraic theorem has independent proof',
        'rational_assertions':checks['sorted_global_minimum']+checks['adjacent_swap_identity'],
        'assertions':sum(checks.values()),'failures':0,
        'assertions_by_type':dict(checks),'controls':len(controls),
        'counts':dict(counts),'illustrative_xy':{'t':'2','s':'1',
            'X_then_Y':{'time':str(xy[0]),'space':str(xy[1]),'guest_fanout':str(xy[2]['calls']),
                        'guest_term':str(guest_exponent([X,Y],2))},
            'Y_then_X':{'time':str(yx[0]),'space':str(yx[1]),'guest_fanout':str(yx[2]['calls']),
                        'guest_term':str(guest_exponent([Y,X],2))}},
        'sample_cases':rows,
        'guards':['No asymptotic upper bound follows from finite length ratios.',
                  'The stage-order theorem assumes two transformations commute semantically and retain descendant eligibility; no all-input such pair is constructed.',
                  'The bit counters are instrumented Python logical proxies, not FLMV work/index machine costs.',
                  'The root read-only source is not counted as writable state; all ordinary children are real serialized bytes.',
                  'Flips, bit-time and transistor counts are not inferred from write counts.',
                  'SAT and UNSAT are independently evaluated for two fully serialized recursion levels.']}
report['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
output=Path(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/2026-10-25_0454_ARC_STAGE_EXCHANGE168_results.json')
output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:report[k] for k in ['run','controls','assertions','failures','rational_assertions','counts','illustrative_xy','code_sha256']},indent=2))
