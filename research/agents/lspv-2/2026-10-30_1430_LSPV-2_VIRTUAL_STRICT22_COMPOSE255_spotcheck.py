#!/usr/bin/env python3
"""Compact, independent source-indexed sanity checker for COMPOSE255.
Python >= 3.10, no external dependencies.
The full composed bit emitter and eager oracle are distributed separately in
the VIRTUAL-STRICT22-COMPOSE255 reproducibility ZIP and are not replicated here.
This checker is NOT the full virtual compiler or a SAT decider.
"""
import itertools
import json

Q = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
     (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
     (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
     (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]

def evaluate_clause(c, assignment):
    return any(bool(assignment[abs(l)-1]) == (l > 0) for l in c)

def validate_fixed_port():
    count=0
    for mask in range(1<<15):
        assignment=tuple((mask>>i)&1 for i in range(15))
        if all(evaluate_clause(c,assignment) for c in Q):
            assert (assignment[0],assignment[6],assignment[12]) == (0,0,0)
            count+=1
    assert count==244
    return count

def degree_prefix_record(r,f,w,L,P):
    assert 0<=r<P and 0<=f<=w
    return 15*w*r+5*min(r,L)+8*max(0,r-L)+15*min(f,w)

def verify_record_degrees(m,n):
    L=3*m
    P=1<<(L-1).bit_length()
    w=(n+1).bit_length()
    d=[15 if f<w else (5 if r<L else 8)
       for r in range(P) for f in range(w+1)]
    p=0
    for r in range(P):
        for f in range(w+1):
            assert degree_prefix_record(r,f,w,L,P)==p
            p+=d[r*(w+1)+f]
    assert p==15*P*w+5*L+8*(P-L)
    return {'source_clauses':m,'original_variables':n,
            'sort_records':P,'key_width':w,'record_degree_sum':p}

def verify_Q_resolution_targets():
    # The complete proof DAG is shipped as q_port_resolution_DAG.json.
    # This independent exhaustive semantic audit does not itself replay the DAG.
    return {'Q_models':validate_fixed_port(),'forced_port_literals':[-1,-7,-13]}

def main():
    results=[verify_record_degrees(m,n) for m,n in ((1,3),(2,3),(8,3),(20,15))]
    models=verify_Q_resolution_targets()
    sizes={}
    for label,M in [('SAT1',797),('SAT2',2962),
                    ('UNSAT8',28048),('W1_or_S15',122234)]:
        sizes[label]={'E_clauses':M,'T_vars':72*M,'T_clauses':96*M}
    assert sizes['SAT1']['T_clauses']==76512
    assert sizes['UNSAT8']['T_clauses']==2692608
    assert sizes['W1_or_S15']['T_clauses']==11734464
    print(json.dumps({'run':'VIRTUAL-STRICT22-COMPOSE255-SPOTCHECK',
          'status':'COMPUTATIONAL',
          'record_prefix_controls':results,
          'Q_semantics':models,
          'physical_size_controls':sizes,
          'limitations':'Does not implement entire local bit accessor; see full ZIP'},
          indent=2))

if __name__=='__main__':
    main()
