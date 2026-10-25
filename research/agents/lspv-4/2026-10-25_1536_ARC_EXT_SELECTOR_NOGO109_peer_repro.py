#!/usr/bin/env python3
"""ARC-EXT-SELECTOR-NOGO109 portable independent finite reproducer.

Restricted result: exact rational FLMV-box accounting and two-level
disconnected ordinary 3CNF SAT/UNSAT controls. No unrestricted lower bound
is inferred from finite checks. Python memory is not FLMV peak tape space.
"""
import json, math
from fractions import Fraction as Q
from itertools import product

c = Q(241, 200)
d = Q(11642479, 23232400)
assert ((c+2)/c**2-c)/2 == d
R, a, lam = Q(11,10), Q(3,5), Q(1,2)

def envelope(b, rho):
    t = max(R, a/(1-lam), b/(1-rho))
    s = max(Q(1,2), rho)
    return t, s, t < c and s < d

def clause_blocks(p, unsat_indices):
    # Each block has three fresh names, seven or eight proper width-3 clauses.
    blocks = []
    for i in range(p):
        ids = (3*i+1, 3*i+2, 3*i+3)
        rows = list(product((0,1),repeat=3))
        if i not in unsat_indices:
            rows.pop()
        blocks.append([tuple(-v if z else v for v,z in zip(ids,row))
                       for row in rows])
    return blocks

def sat_small(formula):
    vs = sorted({abs(x) for clause in formula for x in clause})
    for bits in product((0,1),repeat=len(vs)):
        assignment=dict(zip(vs,bits))
        if all(any(assignment[abs(x)] == (x>0) for x in cl)
               for cl in formula):
            return True
    return False

def checks():
    grid, included = 0, 0
    for bi in range(580,631):
        for ri in range(490,521):
            b, rho = Q(bi,1000),Q(ri,1000)
            t,s,ok = envelope(b,rho)
            assert ok == (b<c*(1-rho) and rho<d)
            assert ok == (t<c and s<d)
            grid += 1
            included += ok
    assert grid==1581 and included==341
    recurrences=0
    for K in range(2,21):
        for bi,ri in [(600,500),(610,500),(600,501),(590,490)]:
            b,rho=Q(bi,1000),Q(ri,1000)
            one=max(R,a+lam*K,b+rho*K)
            two=max(R,a+lam*one,b+rho*one)
            expanded=[R,a+lam*R,b+rho*R,
                      a+lam*a+lam*lam*K,
                      a+lam*b+lam*rho*K,
                      b+rho*a+rho*lam*K,
                      b+rho*b+rho*rho*K]
            assert two == max(expanded)
            recurrences+=1
    assert recurrences==76
    cases=[]
    for p in (16,64,256):
        q=math.isqrt(p)
        assert q*q==p
        for unsat in (set(),{0},{p//2,p-1}):
            blocks=clause_blocks(p,unsat)
            truth = all(sat_small(z) for z in blocks)
            # Exactly two successive actual SAT-preserving AND levels:
            groupbits=[all(sat_small(z) for z in blocks[i*q:(i+1)*q])
                       for i in range(q)]
            assert truth==all(groupbits)==(not unsat)
            cases.append({'p':p,'unsat_blocks':sorted(unsat),
                          'SAT':truth,'level1_calls':q,
                          'level2_calls':p,'total_calls':q+p,
                          'source_clauses':sum(map(len,blocks))})
    assert len(cases)==9
    return {'run':'ARC_EXT_SELECTOR_NOGO109','grid_points':grid,
            'grid_in_strict_box':included,'recurrence_checks':recurrences,
            'two_level_cases':cases,'failures':0,
            'classification':'FINITE COMPUTATIONAL checks of scoped exact theorem'}

if __name__=='__main__':
    result=checks()
    print(json.dumps(result,indent=2))
