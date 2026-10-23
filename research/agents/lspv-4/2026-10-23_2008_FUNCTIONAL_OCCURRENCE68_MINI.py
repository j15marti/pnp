#!/usr/bin/env python3
"""Standalone degree-three functional Horn lift and exact small-case checks."""
from collections import Counter
from itertools import product
import json


def lift(n, formula):
    next_id = n
    ports = {}
    clauses = []
    cycles = []
    def fresh():
        nonlocal next_id
        next_id += 1
        return next_id
    def port(lit):
        v = fresh()
        ports.setdefault(abs(lit), []).append(v)
        return v if lit > 0 else -v
    for a,b,c in formula:
        assert len({abs(a),abs(b),abs(c)}) == 3
        assert all(1 <= abs(v) <= n for v in (a,b,c))
        a1,a2,a3 = [port(a) for _ in range(3)]
        b1,b2 = [port(b) for _ in range(2)]
        c1 = port(c)
        s1,s2,t0,t1,t2,t3 = [fresh() for _ in range(6)]
        clauses += [(s1,s2,t0),(-s1,a1),(-s2,b1),(-t1,c1),
                    (-s2,-a2),(-t2,-a3),(-t3,-b2)]
        cycles.append((t0,t1,t2,t3))
    cycles += [(x,*ports[x]) for x in range(1,n+1) if x in ports]
    for cycle in cycles:
        clauses += [(-x,cycle[(i+1)%len(cycle)]) for i,x in enumerate(cycle)]
    return next_id, tuple(clauses)


def count_models(formula, n, fixed=None):
    def visit(clauses, assignment):
        while True:
            left = []
            for clause in clauses:
                if any(abs(v) in assignment and assignment[abs(v)] == (v>0)
                       for v in clause):
                    continue
                c = tuple(v for v in clause if abs(v) not in assignment)
                if not c:
                    return 0
                left.append(c)
            clauses = tuple(left)
            unit = next((c[0] for c in clauses if len(c)==1), None)
            if unit is None:
                break
            assignment[abs(unit)] = int(unit>0)
        if not clauses:
            return 2**(n-len(assignment))
        v = min(abs(v) for c in clauses for v in c)
        return sum(visit(clauses,{**assignment,v:b}) for b in (0,1))
    return visit(tuple(formula),dict(fixed or {}))


def run():
    checks = 0
    all_rows = tuple(tuple(-(i+1) if row>>i&1 else i+1 for i in range(3))
                     for row in range(8))
    rows = []
    for name,source in [('single_clause',((1,2,3),)),
                        ('UNSAT',all_rows),('unique_SAT',all_rows[1:])]:
        n,target = lift(3,source)
        deg = Counter(abs(v) for c in target for v in c)
        assert max(deg.values()) <= 3
        assert all(sum(v>0 for v in c)<=1 for c in target if len(c)==2)
        assert n == 3+12*len(source)
        assert len(target) == 17*len(source)+3
        checks += 4
        for a in product((0,1),repeat=3):
            expected = int(all(any(a[abs(v)-1]==(v>0) for v in c) for c in source))
            assert count_models(target,n,dict(enumerate(a,1))) == expected
            checks += 1
        sc=count_models(source,3);tc=count_models(target,n)
        assert sc==tc
        checks += 1
        rows.append({'name':name,'variables':n,'clauses':len(target),
                     'max_occurrence':max(deg.values()),'source_models':sc,'target_models':tc})
    return {'checks':checks,'failures':0,'cases':rows}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
