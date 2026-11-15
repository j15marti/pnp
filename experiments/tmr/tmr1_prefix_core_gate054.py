#!/usr/bin/env python3
"""TMR-1 FUSCORE054: proper-3CNF source-bound resolution and terminal-mask controls.
No unrestricted lower bound is claimed. Python models abstract inference lines, not a compiled TM.
"""
from __future__ import annotations
import json
from itertools import product
from fractions import Fraction

CHECKS=0

def check(c, msg='check'):
    global CHECKS
    CHECKS+=1
    assert c, msg

def forcing(lit, y=2, z=3):
    check(len({abs(lit), y, z})==3)
    return [frozenset((lit, sy*y, sz*z)) for sy,sz in ((1,1),(1,-1),(-1,1),(-1,-1))]

def family(n, opposite=True):
    check(n>=1)
    clauses=forcing(1)+forcing(-1 if opposite else 1)
    clauses += [frozenset((4+3*i,5+3*i,6+3*i)) for i in range(n)]
    check(all(len(c)==3 and len({abs(k) for k in c})==3 for c in clauses))
    return clauses

def encode(F):
    v=max(abs(z) for c in F for z in c)
    return f'V={v};C={len(F)}:' + ';'.join(','.join(str(x) for x in sorted(c, key=lambda x:(abs(x),x<0))) for c in F) + ';'

def resolution(a,b,pivot):
    check(pivot in a and -pivot in b, 'bad pivot source')
    r=(a|b)-{pivot,-pivot}
    check(not any(-lit in r for lit in r), 'tautological resolvent')
    return frozenset(r)

def proof(F, pivots=(1,2,3)):
    log=list(F[:8]); steps=[]
    x,y,z=pivots
    for i,j,z in ((0,1,z),(2,3,z),(8,9,y),(4,5,z),(6,7,z),(11,12,y),(10,13,x)):
        a,b=log[i],log[j]
        log.append(resolution(a,b,z));steps.append((i,j,z,len(log)-1))
    check(log[-1]==frozenset(), 'no empty resolvent')
    return log,steps

def sat_bruteforce(F):
    vs=sorted({abs(x) for c in F for x in c})
    for b in product((False,True),repeat=len(vs)):
        A=dict(zip(vs,b))
        if all(any(A[abs(l)] if l>0 else not A[abs(l)] for l in c) for c in F):
            return True
    return False

def core_graft(F):
    # Polynomial front-end recognized from eight explicit clauses; fallback is brute force.
    if len(F)>=8 and set(F[:4])==set(forcing(1)) and set(F[4:8])==set(forcing(-1)):
        return False
    return sat_bruteforce(F)

def rename(F,ren):
    return [frozenset((1 if x>0 else -1)*ren.get(abs(x),abs(x)) for x in c) for c in F]

def mask_violations(mass,weight=Fraction(1,1)):
    # Model a legal last paid transition where the static mass is masked at HALT.
    nonterminal=weight*mass
    terminal=Fraction(0)
    return nonterminal-terminal>1

records=[]
for n in range(1,45):
    F=family(n)
    E=encode(F)
    trace,steps=proof(F)
    check(len(steps)==7 and len(trace)==15)
    check(trace[10]==frozenset((1,)))
    check(trace[13]==frozenset((-1,)))
    check(trace[-1]==frozenset())
    check(len(F)==n+8)
    check(core_graft(F) is False)
    check(all(len(c)==3 for c in F))
    sf=family(n,opposite=False)
    if n<=3:
        check(core_graft(sf) is True)
    witness={i:True for i in range(1,4+3*n)}
    check(all(any(witness[abs(l)] if l>0 else not witness[abs(l)] for l in c) for c in sf))
    if n<=3:
        check(sat_bruteforce(F) is False)
        check(sat_bruteforce(sf) is True)
    if n<=10:
        mapping={1:3+3*n,2:3+3*n+1,3:3+3*n+2}
        rf=rename(F,mapping)
        tr,st=proof(rf,pivots=(mapping[1],mapping[2],mapping[3]))
        check(tr[-1]==frozenset())
    if n in (1,2,4,8,16,32,44):
        records.append(dict(n=n,length=len(E.encode('utf-8')),variables=3+3*n,clauses=8+n,resolution_steps=len(steps),terminal_mask_mass=n**4,terminal_mask_violation=mask_violations(n**4)))

for x,y,z in product((False,True),repeat=3):
    A={1:x,2:y,3:z}
    F=forcing(1)
    ok=all(any(A[abs(l)] if l>0 else not A[abs(l)] for l in c) for c in F)
    check(ok==x)

failed_pivot=False
try:
    resolution(frozenset((1,2)),frozenset((-1,3)),2)
except AssertionError:
    failed_pivot=True
check(failed_pivot)

for m in range(0,100):
    for numerator in range(0,8):
        w=Fraction(numerator,3)
        check(mask_violations(m,w)==(w*m>1))

out={'run':'FUSCORE054','status':'COMPUTATIONAL (finite tests); symbolic theorem independent',
     'assertions':CHECKS,'family':'proper 3CNF opposite 4-clause forcing blocks + n disjoint width-3 clauses',
     'native_resolution_inferences':7,'source_clauses_used':8,'source_clauses_total':'n+8',
     'source_bit_length':'Theta(n log n) under declared explicit signed-decimal encoding',
     'grafted_decider':'polynomial-time prefix test and otherwise exponential exact brute-force',
     'terminal_mask_test':'every final HALT edge with cost=1 requires lambda*M(F)<=1',
     'sample_records':records,'failure_count':0}
print(json.dumps(out,sort_keys=True,indent=2))
