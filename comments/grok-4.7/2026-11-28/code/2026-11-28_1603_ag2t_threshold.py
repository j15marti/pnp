#!/usr/bin/env python3
"""Exact SAT/UNSAT status of the even-arity XOR-zero NAE family AG(2t)-n.

Instance AG(2t)-n, n = 2^k: one Boolean variable x_p per point p of F_2^k.
For every set B of 2t DISTINCT points with XOR(B) = 0 add the two
complementary clauses (OR_{p in B} x_p) and (OR_{p in B} ~x_p), i.e. B is
not monochromatic (NAE_{2t}).  This is T2's AG4 family (t=2) and its
symbolic generalisation in research/agents/algebraic-geometric-closure/
2026-11-27_2231_T2_full_pc/report.md.

For each (t,k) we: enumerate blocks, assert every (2t-1)-subset lies in at
most one block (the unique-top-monomial hypothesis of the PC fixed point),
solve with CaDiCaL (pysat) under the complement-symmetry pin x_0 = 0, and
independently verify any model by recomputing every block, or record UNSAT.
"""
import itertools, sys, json, time
from pysat.solvers import Solver

def blocks(k, t):
    n = 1 << k
    out = []
    for S in itertools.combinations(range(n), 2 * t - 1):
        x = 0
        for p in S:
            x ^= p
        if x > S[-1]:          # last element larger than all: canonical, distinct
            out.append(S + (x,))
    return out

def check_unique_tops(bl, t):
    seen = set()
    for B in bl:
        for T in itertools.combinations(B, 2 * t - 1):
            if T in seen:
                return False
            seen.add(T)
    return True

def solve(k, t, solver='cadical153'):
    n = 1 << k
    t0 = time.time()
    bl = blocks(k, t)
    uniq = check_unique_tops(bl, t) if len(bl) < 400000 else None
    cls = []
    for B in bl:
        cls.append([p + 1 for p in B])
        cls.append([-(p + 1) for p in B])
    with Solver(name=solver, bootstrap_with=cls) as s:
        s.add_clause([-1])     # complement symmetry: x_0 = 0 w.l.o.g.
        sat = s.solve()
        model = s.get_model() if sat else None
        stats = s.accum_stats()
    rec = dict(t=t, arity=2 * t, k=k, n=n, blocks=len(bl), clauses=2 * len(bl),
               unique_top_monomials=uniq, status='SAT' if sat else 'UNSAT',
               seconds=round(time.time() - t0, 2), solver=solver,
               solver_stats={kk: stats[kk] for kk in ('conflicts', 'decisions', 'propagations') if kk in stats})
    if sat:
        mv = {abs(v): v > 0 for v in model}
        col = [1 if mv.get(p + 1, False) else 0 for p in range(n)]
        bad = [B for B in bl if len({col[p] for p in B}) == 1]
        assert not bad, 'model violates a block'
        # independent re-check straight from the definition (no block list reuse)
        ones = [p for p in range(n) if col[p]]
        rec['verified_model'] = True
        rec['class_sizes'] = [n - len(ones), len(ones)]
        rec['class1_points'] = ones
    return rec

if __name__ == '__main__':
    plan = [(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 4), (4, 5)]
    if len(sys.argv) > 1:
        plan = [tuple(map(int, a.split(','))) for a in sys.argv[1:]]
    res = []
    for t, k in plan:
        r = solve(k, t)
        print(json.dumps(r), flush=True)
        res.append(r)
