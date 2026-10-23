#!/usr/bin/env python3
"""ADAPTIVE-SPLIT74 stdlib-only exhaustive verification, including the
Role-4 implication chain, first-true Horn selector, and easy controls.
Run: python 2026-10-24_0526_ADAPTIVE_SPLIT74_quickcheck.py
Writes 2026-10-24_0526_ADAPTIVE_SPLIT74_raw.json beside this script.
This finite audit is not a P-vs-NP lower bound.
"""
import hashlib
import itertools
import json
from pathlib import Path

MAX_Q = 8
CHECKS = 0

def check(ok, tag):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(tag)

def clause(*literals):
    return tuple(literals)

def chain(q, b):
    u,v=q+1,q+2
    cs=[clause((0,True),(u,True)),clause((0,True),(u,False)),
        clause((q,False),(v,True)),clause((q,False),(v,False))]
    for i,bit in enumerate(b,1):
        cs.append(clause((i-1,False),(i,bool(bit))))
    return cs

def sat_assignment(cs,mask,n):
    return all(any(bool((mask>>(n-1-i))&1)==pos for i,pos in c)
               for c in cs)

def brute_attempts(cs,n):
    for i in range(1<<n):
        if sat_assignment(cs,i,n):
            return True,i+1
    return False,1<<n

def first_true_gadget(l1,l2,l3,s1,s2,s3):
    return ((s1 or s2 or s3) and
            (not s1 or l1) and (not s2 or l2) and (not s3 or l3) and
            (not s2 or not l1) and (not s3 or not l1) and
            (not s3 or not l2))

def main():
    rows=[]
    totals={'orientations':0,'sat':0,'unsat':0,'brute_candidates':0,
            'left_slow':0,'right_slow':0,'priority_local_truth_rows':0,
            'controls':0}
    for q in range(1,MAX_Q+1):
        sat_count=unsat_count=0
        minimum_slow=1<<(q+3)
        maximum_slow=0
        n,m=q+3,q+4
        w=(64*(n+m+1)-1).bit_length()
        N=(4*m+2)*w
        for b in itertools.product((0,1),repeat=q):
            cs=chain(q,b)
            check(len(cs)==q+4,('clauses',q,b))
            check(all(len(c)==2 and c[0][0]!=c[1][0] for c in cs),
                  ('proper',q,b))
            yes,attempts=brute_attempts(cs,n)
            direct=any(x==0 for x in b)
            check(yes==direct,('label',q,b))
            left_fast=(b[0]==0)
            right_fast=(b[0]==1)
            check(left_fast!=right_fast,('partition',q,b))
            left_yes=True if left_fast else yes
            right_yes=direct if right_fast else yes
            check(left_yes==yes and right_yes==yes,('soundness',q,b))
            check(attempts>=(1<<(q+2)),('lex_bad_early',q,b,attempts))
            minimum_slow=min(minimum_slow,attempts)
            maximum_slow=max(maximum_slow,attempts)
            sat_count+=yes
            unsat_count+=not yes
            totals['orientations']+=1
            totals['brute_candidates']+=attempts
            totals['left_slow']+=right_fast
            totals['right_slow']+=left_fast
        check(sat_count==(1<<q)-1 and unsat_count==1,
              ('counts',q,sat_count,unsat_count))
        rows.append({'q':q,'n':n,'m':m,'N_bits':N,'w_bits':w,
                     'orientations':1<<q,'SAT':sat_count,'UNSAT':unsat_count,
                     'minimum_slow_bruteforce_trials':minimum_slow,
                     'claimed_lower_bound_trials':1<<(q+2),
                     'maximum_slow_bruteforce_trials':maximum_slow,
                     'fast_word_scan_upper':(4*m+2)+q})
        totals['sat']+=sat_count
        totals['unsat']+=unsat_count
    for l in itertools.product((False,True),repeat=3):
        exts=[s for s in itertools.product((False,True),repeat=3)
              if first_true_gadget(*(l+s))]
        check(len(exts)==int(any(l)),('first_true',l,exts))
        if exts:
            check(exts[0]==tuple(i==l.index(True) for i in range(3)),
                  ('unique',l,exts))
        totals['priority_local_truth_rows']+=1
    fixtures=[
        ('KROM_SAT',2,[clause((0,True),(1,True))],True),
        ('KROM_UNSAT',1,[clause((0,True)),clause((0,False))],False),
        ('HORN_SAT',3,[clause((0,False),(1,False),(2,True)),
                       clause((0,True))],True),
        ('HORN_UNSAT',1,[clause((0,True)),clause((0,False))],False),
        ('XOR3_SAT',3,[clause((0,True),(1,True),(2,True)),
                       clause((0,True),(1,False),(2,False)),
                       clause((0,False),(1,True),(2,False)),
                       clause((0,False),(1,False),(2,True))],True),
        ('XOR3_UNSAT',3,[clause((0,True),(1,True),(2,True)),
                         clause((0,True),(1,False),(2,False)),
                         clause((0,False),(1,True),(2,False)),
                         clause((0,False),(1,False),(2,True)),
                         clause((0,False),(1,False),(2,False)),
                         clause((0,False),(1,True),(2,True)),
                         clause((0,True),(1,False),(2,True)),
                         clause((0,True),(1,True),(2,False))],False),
        ('COMPONENTS_UNSAT',2,[clause((0,True)),
                              clause((1,True)),clause((1,False))],False),
        ('READABLE_WITNESS',3,[clause((0,True),(1,True),(2,True))],True)
    ]
    for name,n,cs,want in fixtures:
        yes,_=brute_attempts(cs,n)
        check(yes==want,('control',name,yes,want))
        totals['controls']+=1
    raw={'run':'ADAPTIVE_SPLIT74',
         'model':'canonical 2-CNF indexed fields; exhaustive lex assignment trials',
         'max_q':MAX_Q,'summary':totals,'per_q':rows,
         'assertions':CHECKS,'failures':0,
         'limitations':'finite controls only; asymptotic statements require separate proof'}
    body=json.dumps(raw,sort_keys=True,indent=2)+'\n'
    out=Path(__file__).with_name('2026-10-24_0526_ADAPTIVE_SPLIT74_raw.json')
    out.write_text(body)
    print(json.dumps({'sha256':hashlib.sha256(body.encode()).hexdigest(),
                      'summary':totals,'assertions':CHECKS},sort_keys=True))
    print(json.dumps(rows,sort_keys=True))

if __name__=='__main__':
    main()
