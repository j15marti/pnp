#!/usr/bin/env python3
"""RACE-SAT77 exact finite controls. Python 3 standard library; no randomness."""
import json
from itertools import product

def force(lit, a, b):
    """Four proper-3CNF clauses equivalent to unit literal lit."""
    return [(lit, a, b), (lit, a, -b), (lit, -a, b), (lit, -a, -b)]

def val(lit, bits):
    x = bool((bits >> (abs(lit)-1)) & 1)
    return x if lit>0 else not x

def sat_assignment(clauses, bits):
    return all(any(val(lit, bits) for lit in c) for c in clauses)

def alltrue(clauses, n):
    return sat_assignment(clauses, (1<<n)-1)

def exact_sat(clauses, n):
    for bits in range(1<<n):
        if sat_assignment(clauses,bits):
            return True,bits
    return False,None

def branch(formula, orig_n, assignment):
    out=list(formula)
    for i,(var,truth) in enumerate(assignment):
        a=orig_n+2*i+1
        b=a+1
        out.extend(force(var if truth else -var,a,b))
    return out,orig_n+2*len(assignment)

def base(q):
    cnf=[]
    for i in range(1,q+1):
        cnf.extend(force(i,q+2*i-1,q+2*i))
    return cnf,3*q

def test():
    counters={'force_truth_rows':0,'canonical_sources':0,
              'race_trajectories':0,'sat_branch_verifications':0,
              'unsat_branch_verifications':0,'control_formulas':0}
    details=[]
    for lit_true,a,b in product([False,True],repeat=3):
        clauses=force(1,2,3)
        bits=int(lit_true)+2*int(a)+4*int(b)
        assert sat_assignment(clauses,bits)==lit_true
        counters['force_truth_rows']+=1
    for q in range(1,4):
        F,n=base(q)
        assert len(F)==4*q
        assert all(len(set(abs(t) for t in c))==3 for c in F)
        assert alltrue(F,n)
        label,w=exact_sat(F,n)
        assert label and w is not None
        counters['canonical_sources']+=1
        pref=[]; wrong_costs=[]; race_ceiling=[]
        for i in range(1,q+1):
            false_G,nf=branch(F,n,pref+[(i,False)])
            true_G,nt=branch(F,n,pref+[(i,True)])
            false_sat,_=exact_sat(false_G,nf)
            true_sat,_=exact_sat(true_G,nt)
            assert not false_sat and true_sat
            assert alltrue(true_G,nt) and not alltrue(false_G,nf)
            counters['unsat_branch_verifications']+=1
            counters['sat_branch_verifications']+=1
            false_candidates=1<<nf
            fast_true_cost=len(true_G)*3+nt
            race_cost=2*fast_true_cost
            wrong_costs.append(false_candidates)
            race_ceiling.append(race_cost)
            pref.append((i,True))
            counters['race_trajectories']+=1
        assert sat_assignment(F,(1<<n)-1)
        details.append({'q':q,'base_variables':n,'base_clauses':len(F),
                        'wrong_false_branch_assignment_trials':wrong_costs,
                        'race_at_most_literal_scan_units':race_ceiling,
                        'total_wrong_branch_trials':sum(wrong_costs),
                        'total_race_scan_upper':sum(race_ceiling)})
    G1,n1=base(1)
    controls=[('source_witness_sat',G1,n1,True),
              ('source_witness_unsat',G1+force(-1,n1+1,n1+2),n1+2,False)]
    def pad(a,b,z):return [(a,b,z),(a,b,-z)]
    controls.extend([('padded_2sat_sat',pad(1,2,3),3,True),
                     ('padded_2sat_unsat',force(1,2,3)+force(-1,4,5),5,False),
                     ('xor_2sat_sat',pad(1,2,3)+pad(-1,-2,4),4,True),
                     ('horn_sat',pad(-1,2,3)+force(1,4,5),5,True),
                     ('independent_components',G1+[tuple((t+3 if t>0 else t-3) for t in c) for c in G1],6,True)])
    for name,f,num,expected in controls:
        result,_=exact_sat(f,num)
        assert result==expected,(name,result,expected)
        counters['control_formulas']+=1
    return {'run_id':'RACE-SAT77','status':'COMPUTATIONAL, finite controls only',
            'claim':'SAT-only fair racing avoids slow UNSAT child calls; all proper-3CNF',
            'counts':counters,'details':details,'controls':[x[0] for x in controls],
            'discrepancies':0}

if __name__=='__main__':
    output=test()
    print(json.dumps(output,indent=2,sort_keys=True))
