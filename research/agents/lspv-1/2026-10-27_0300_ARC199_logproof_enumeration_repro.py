#!/usr/bin/env python3
"""ARC199: exact finite controls for a length-capped UNSAT verifier and enumeration.
No random seed. Standard library. Promise controls do not prove a full-SAT lower bound.
"""
import json
from fractions import Fraction
from math import ceil, log2
from pathlib import Path

W1 = [
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
A=((6,0),(11,0))
B=((9,2),(17,2))
checks=0

def ck(x, explanation=''):
    global checks
    checks += 1
    if not x: raise AssertionError(explanation)

def module(a,b):
    clauses=[list(row) for row in W1]
    if a == 0:
        for row,col in A:clauses[row][col]*=-1
    if b == 0:
        for row,col in B:clauses[row][col]*=-1
    return tuple(tuple(c) for c in clauses)

def proper_22(clauses):
    ck(len(clauses)==20)
    ck(len(set(clauses))==20)
    pos={i:0 for i in range(1,16)}
    neg={i:0 for i in range(1,16)}
    for c in clauses:
        ck(len(c)==3 and len({abs(x) for x in c})==3)
        for x in c:
            (pos if x>0 else neg)[abs(x)]+=1
    ck(all(pos[i]==neg[i]==2 for i in range(1,16)))

def eval_clause(c,mask):
    return any(bool(mask & (1<<(abs(lit)-1))) == (lit>0) for lit in c)

def count_models(clauses):
    return sum(all(eval_clause(c,x) for c in clauses) for x in range(1<<15))

counts={}
for a in (0,1):
    for b in (0,1):
        c=module(a,b)
        proper_22(c)
        n=count_models(c)
        counts[f'{a}{b}']=n
        ck((n>0)==(not(a and b)))
ck(counts=={'00':772,'01':272,'10':272,'11':0},str(counts))

# Candidate is a 0-based module index ON THE CANONICAL PROMISE.
# For globally sound ordinary-CNF verification also authenticate all 20 source clauses.
def local_certificate(a,b,index):
    return 0<=index<len(a) and a[index]==b[index]==1

cases=0
sat_cases=0
unsat_cases=0
accepted_valid=0
for m in range(1,5):
    ell=(m-1).bit_length()
    ck(2**ell>=m)
    for ai in range(1<<m):
        for bi in range(1<<m):
            a=tuple((ai>>i)&1 for i in range(m))
            b=tuple((bi>>i)&1 for i in range(m))
            unsat=any(a[i]&b[i] for i in range(m))
            proof_set=[i for i in range(1<<ell) if local_certificate(a,b,i)]
            ck(bool(proof_set)==unsat)
            ck(all(0<=i<m and a[i]==b[i]==1 for i in proof_set))
            if not unsat:
                ck(not proof_set)
                sat_cases+=1
            else:
                ck(len(proof_set)==sum(a[i]&b[i] for i in range(m)))
                unsat_cases+=1
            cases+=1
ck(cases==sum(4**m for m in range(1,5)))

# Hostile controls: bit flips and invalid/out-of-range indices.
for m in range(1,5):
    a=(1,)+(0,)*(m-1)
    b=(1,)+(0,)*(m-1)
    ck(local_certificate(a,b,0))
    for pos in range(m):
        aa=list(a);aa[pos]=1-aa[pos]
        bb=list(b);bb[pos]=1-bb[pos]
        ck(local_certificate(tuple(aa),b,0)==(pos!=0))
        ck(local_certificate(a,tuple(bb),0)==(pos!=0))
    ck(not local_certificate(a,b,m))
    ck(not local_certificate(a,b,-1))

c0=Fraction(241,200)
s0=Fraction(11642479,23232400)
beta=lambda c: Fraction(1,2)*( (c+2)/c**2 -c )
ck(beta(c0)==s0)
numrows=[]
for r,a,s in [
    (Fraction(1),Fraction(1,5),Fraction(2,5)),
    (Fraction(1),Fraction(21,100),Fraction(2,5)),
    (Fraction(1),Fraction(41,200),Fraction(2,5)),
    (Fraction(11,10),Fraction(1,10),Fraction(2,5)),
    (Fraction(1),Fraction(1,5),Fraction(3,5))]:
    t=max(Fraction(1),r+a)
    forbidden=(t<c0 and s<s0)
    ck(forbidden==((r+a<c0) and (s<s0)) if r>=1 else forbidden)
    numrows.append({'r':str(r),'a':str(a),'s':str(s),'time':str(t),
                    'strict_FLVM_box':forbidden})
ck(numrows[0]['strict_FLVM_box'])
ck(not numrows[1]['strict_FLVM_box'])
ck(not numrows[2]['strict_FLVM_box'])
ck(numrows[3]['strict_FLVM_box'])
ck(not numrows[4]['strict_FLVM_box'])
mkrows=[]
for r,a,s in [
    (Fraction(1),Fraction(1),Fraction(0)),
    (Fraction(1),Fraction(3,5),Fraction(1,5)),
    (Fraction(3,2),Fraction(1,4),Fraction(1,4))]:
    t=a+max(1,r)
    mkrows.append({'r':str(r),'a':str(a),'s':str(s),'t':str(t),
                   'sequential_tape_forbidden': t+s<2})
ck(not mkrows[0]['sequential_tape_forbidden'])
ck(mkrows[1]['sequential_tape_forbidden'])
ck(not mkrows[2]['sequential_tape_forbidden'])
raw={'run_id':'ARC199_LOGPROOF_ENUMERATION_FRONTIER','seed':None,
     'verification_scope':'finite controls for a promise-only verifier, exact fraction arithmetic',
     'gadget_model_counts':counts,'canonical_disj_cases':cases,
     'sat_cases':sat_cases,'unsat_cases':unsat_cases,
     'coefficient_FLVM':str(c0),'space_FLVM':str(s0),
     'numeric_FLMV_frontier':numrows,'native_tape_frontier':mkrows,
     'assertion_groups':checks,'failures':0,
     'limits':['General all-ordinary-UNSAT proof coverage not tested or established.',
               'Finite gadget experiments do not prove an asymptotic SAT lower bound.',
               'Sequential-input and indexed-RAM boundaries apply only in their separate declared models.']}
p=Path(__file__).with_name('2026-10-27_0300_ARC199_logproof_enumeration_raw.json')
p.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
print(json.dumps(raw,indent=2,sort_keys=True))
