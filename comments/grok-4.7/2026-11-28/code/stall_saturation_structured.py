#!/usr/bin/env python3
"""Structured UNSAT 3-CNF families for the width-w saturated-stall counterexample.
Tseitin (odd charge) on small cubic graphs, and a 3-CNF encoding of the
ordering principle GT_n (reduced tournament version). Reuses stall_saturation.py.
"""
import itertools, json, random, sys
from stall_saturation import (saturate, subsumed, unsat_minisat, brute_unsat, is_strict_stall,
                              critical_pairs, failed_literals, violated, min_violation_assignment)

def tseitin(edges, nv, odd_vertex=0):
    var = {e: i+1 for i, e in enumerate(edges)}
    F = []
    for v in range(nv):
        inc = [var[e] for e in edges if v in e]
        charge = 1 if v == odd_vertex else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            # forbid assignments with parity != charge: clause falsified exactly by that assignment
            if sum(signs) % 2 != charge:
                F.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return F, len(edges)

def gt3(n):
    # x(i,j) for i<j true means i before j. tournament totality is built in.
    idx = {}
    for i, j in itertools.combinations(range(n), 2): idx[(i, j)] = len(idx)+1
    def before(i, j):  # literal 'i before j'
        return idx[(i, j)] if i < j else -idx[(j, i)]
    F = []
    for i, j, k in itertools.permutations(range(n), 3):
        F.append((-before(i, j), -before(j, k), before(i, k)))
    nxt = len(idx)
    # every element j has a predecessor: OR_{i!=j} before(i,j), split into 3-clauses with extension vars
    for j in range(n):
        lits = [before(i, j) for i in range(n) if i != j]
        while len(lits) > 3:
            nxt += 1
            F.append((lits[0], lits[1], nxt)); lits = [-nxt] + lits[2:]
        F.append(tuple(lits))
    F = list({tuple(sorted(set(c), key=abs)) for c in F})
    return F, nxt

def greedy_stall(S, n, seed):
    rnd = random.Random(seed)
    a = {i: rnd.random() < .5 for i in range(1, n+1)}
    while True:
        base = len(violated(S, a)); best = None
        for v in range(1, n+1):
            a[v] = not a[v]; nb = len(violated(S, a)); a[v] = not a[v]
            if nb < base and (best is None or nb < best[0]): best = (nb, v)
        if best is None: return a, base
        a[best[1]] = not a[best[1]]

def full_closure_check(S, w):
    Sl = list(S)
    for i, C in enumerate(Sl):
        for D in Sl[i+1:]:
            piv = [l for l in C if -l in D]
            if len(piv) != 1: continue
            R = frozenset((C - {piv[0]}) | (D - {-piv[0]}))
            if len(R) <= w and not subsumed(R, S): return False
    return True

def study(name, F, n, ws, starts=8):
    out = []
    unsat = unsat_minisat(F)
    for w in ws:
        rec = {'family': name, 'n_vars': n, 'm': len(F), 'max_clause_width': max(map(len, F)), 'w': w,
               'minisat_unsat': unsat, 'brute_unsat': brute_unsat(F, n) if n <= 22 else None}
        S, steps, empty = saturate(F, w)
        rec.update(sat_size=len(S), sat_steps=steps, empty_derived=empty,
                   width_hist={k: sum(1 for c in S if len(c) == k) for k in range(w+1)})
        if not empty:
            rec['independent_closure_check'] = full_closure_check(S, w)
            rec['failed_literal'] = failed_literals(S, n)
            stalls = []
            if n <= 22:
                best, a = min_violation_assignment(S, n)
                stalls.append({'start': 'global_min', 'violated': best, 'strict_stall': is_strict_stall(S, a, n),
                               'critical': critical_pairs(S, a, w)})
            for sd in range(starts):
                a, b = greedy_stall(S, n, 1000+sd)
                stalls.append({'start': f'greedy_seed{1000+sd}', 'violated': b, 'strict_stall': is_strict_stall(S, a, n),
                               'critical': critical_pairs(S, a, w)})
            rec['stalls'] = stalls
        out.append(rec)
        print(name, 'w', w, 'empty', empty, 'size', len(S), flush=True)
    return out

if __name__ == '__main__':
    K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    K33 = [(a, b) for a in range(3) for b in range(3, 6)]
    Q3 = [(a, b) for a in range(8) for b in range(8) if a < b and bin(a ^ b).count('1') == 1]
    P = [(i, (i+1) % 5) for i in range(5)] + [(i, i+5) for i in range(5)] + [(5+i, 5+(i+2) % 5) for i in range(5)]
    P = [tuple(sorted(e)) for e in P]
    results = []
    for name, E, nv in [('Tseitin-K4', K4, 4), ('Tseitin-K33', K33, 6), ('Tseitin-Q3', Q3, 8), ('Tseitin-Petersen', P, 10)]:
        F, n = tseitin(E, nv)
        results += study(name, F, n, [3, 4, 5])
    for k in (4, 5, 6):
        F, n = gt3(k)
        results += study(f'GT3-{k}', F, n, [3, 4, 5])
    json.dump(results, open(sys.argv[1] if len(sys.argv) > 1 else 'stall_saturation_structured.out.json', 'w'), indent=1, default=str)
