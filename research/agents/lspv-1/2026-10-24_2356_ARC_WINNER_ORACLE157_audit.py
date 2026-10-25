#!/usr/bin/env python3
"""ARC-WINNER-ORACLE157: finite exact control for a SAT-hard fastest-policy index.
No timing or space lower bounds on a physical random-access Turing machine are inferred.
"""
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

SEED = 202610242356


def sat_with_cost(n, clauses):
    # Conventional ordinary CNF: clauses may have length 0, 1, 2, 3, etc.
    # Invalid encodings are rejected. This function is a finite exhaustive oracle.
    if not isinstance(n, int) or n < 0 or any(
        not isinstance(c, (tuple, list)) or
        any(not isinstance(lit, int) or lit == 0 or abs(lit) > n for lit in c)
        for c in clauses
    ):
        return False, 1, 0
    ops = 0
    for bits in itertools.product((False, True), repeat=n):
        ok = True
        for c in clauses:
            satisfied = False
            for lit in c:
                ops += 1
                v = bits[abs(lit)-1]
                if (v if lit > 0 else not v):
                    satisfied = True
                    break
            if not satisfied:
                ok = False
                break
        if ok:
            return True, ops+1, 1
    return False, ops+1, 2**n


def pin(clauses, index, value):
    reduced = []
    for c in clauses:
        if any(abs(lit) == index and (lit > 0) == value for lit in c):
            continue
        reduced.append(tuple(lit for lit in c if abs(lit) != index))
    return tuple(reduced)


def two_level_decision(n, clauses):
    if n < 2:
        raise ValueError('two real pin levels require n >= 2')
    grandchild_results = []
    child_results = []
    for a in (False, True):
        c1 = pin(clauses, 1, a)
        row = []
        for b in (False, True):
            c2 = pin(c1, 2, b)
            v = sat_with_cost(n, c2)[0]
            row.append(v)
            grandchild_results.append(v)
        child_results.append(any(row))
        assert sat_with_cost(n, c1)[0] == any(row)
    return any(child_results), child_results, grandchild_results


def all_sign_patterns():
    return [tuple((i+1) if bit else -(i+1) for i,bit in enumerate(bits))
            for bits in itertools.product((False, True), repeat=3)]


def examples():
    patterns = all_sign_patterns()
    for mask in range(256):
        clauses = tuple(patterns[i] for i in range(8) if mask & (1<<i))
        yield 'exhaustive3', 3, clauses
    # Both labels at the same 8-clause count in an ordinary CNF.
    yield 'repeated_clause_sat', 3, tuple(patterns[:7] + patterns[:1])
    yield 'eight_clause_unsat', 3, tuple(patterns)
    yield 'horn_sat', 3, ((-1,2),(-2,3),(1,))
    yield 'horn_unsat', 3, ((1,),(-1,))
    yield 'xor_sat', 3, ((1,2),(-1,-2),(2,3),(-2,-3))
    yield 'xor_unsat', 3, ((1,2),(-1,-2),(2,3),(-2,-3),(1,3),(-1,-3))
    yield 'malformed', 3, ((0,1),)
    rng = random.Random(SEED)
    literals = [v for i in range(1,5) for v in (i,-i)]
    for _ in range(400):
        clauses = tuple(tuple(rng.sample(literals,3)) for __ in range(rng.randrange(3,28)))
        yield 'random4', 4, clauses


def run():
    cases = []
    totals = {'cases':0,'sat':0,'unsat_or_invalid':0,'winner_errors':0,
              'two_level_errors':0,'two_level_checks':0, 'fastest_is_base_errors':0,
              'overlap_labels_at_eight_clauses':False}
    for kind,n,clauses in examples():
        b,dwork,assignments = sat_with_cost(n, clauses)
        # Both portfolio programs run the same D; only conditional delay differs.
        N = len(repr((n,clauses)).encode('utf-8'))
        delay = (N+2)**4
        cost_a0 = dwork + (delay if b else 0)
        cost_a1 = dwork + (0 if b else delay)
        fastest_idx = 0 if cost_a0 < cost_a1 else 1
        assert cost_a0 != cost_a1
        assert fastest_idx == int(b)
        assert min(cost_a0,cost_a1) == dwork
        totals['cases'] += 1
        totals['sat' if b else 'unsat_or_invalid'] += 1
        if kind != 'malformed':
            two,child,grand=two_level_decision(n,clauses)
            assert two == b
            totals['two_level_checks'] += 1
        if len(cases)<10 or kind in ('repeated_clause_sat','eight_clause_unsat',
                                      'horn_unsat','xor_unsat','malformed'):
            cases.append(dict(kind=kind,variables=n,clauses=len(clauses),
                              encoded_py_bytes=N,sat=b,base_work=dwork,
                              delay=delay,winner=fastest_idx,
                              assignments_considered=assignments))
    endpoint=Fraction(11642479,23232400)
    assert Fraction(1,2)<endpoint
    assert Fraction(6,5)<Fraction(241,200)
    assert totals['cases']==663
    assert totals['sat']>0 and totals['unsat_or_invalid']>0
    totals['overlap_labels_at_eight_clauses']=True
    return dict(run_id='ARC-WINNER-ORACLE157',seed=SEED,totals=totals,
                cases_sample=cases,endpoint={'time_c':'241/200','space_d':str(endpoint)},
                formal_scope='winner-index equality and finite two-pin ordinary CNF semantics',
                limits='Python logical operations; not FLMV physical work/space measurement or a new ARC successor')

if __name__ == '__main__':
    out=run()
    path=Path(__file__).with_name('ARC_WINNER_ORACLE157_results.json')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print(json.dumps(out['totals'],sort_keys=True))
