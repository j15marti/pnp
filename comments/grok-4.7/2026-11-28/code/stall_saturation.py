#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 08:5x KST.
Counterexample search for the conjectured step
  'a strict local-search stall yields a NOVEL paid bounded-width (<=w) resolution consequence'
(T4-05 'next target', T3-06 sec.3 caveat, T1-05 'universal acquisition' arrow).

For an UNSAT 3-CNF F we compute the width-w resolution saturation S_w(F):
the closure of F under resolution steps whose resolvent has width <= w,
discarding resolvents subsumed by a clause already present. If the empty
clause is not in S_w(F), then S_w(F) is UNSAT, closed, and EVERY assignment
minimising the number of violated clauses of S_w(F) is a strict stall; at such a
stall every critical pair (C violated, D with unique true literal -p) yields a
resolvent that is either subsumed (not novel) or has width > w.
We verify that last statement explicitly by enumeration (not just by appeal
to closure), and report the minimum width of a novel critical resolvent.
Also: unit propagation and failed-literal probing on S_w(F), and the affine
(GF(2)) relaxation of the per-clause tables, which is trivial for clauses of
width >= 2 (allowed set of a k-clause, k>=2, has full affine hull).
Deterministic: seeds fixed. Pure Python + PySAT (minisat22) for UNSAT check
and an independent brute-force check for n<=22.
"""
import itertools, json, random, sys
from pysat.solvers import Minisat22

def rand3cnf(n, m, seed):
    rnd = random.Random(seed)
    F = set()
    while len(F) < m:
        vs = rnd.sample(range(1, n+1), 3)
        F.add(frozenset(v if rnd.random() < .5 else -v for v in vs))
    return [tuple(sorted(c, key=abs)) for c in F]

def unsat_minisat(F):
    with Minisat22(bootstrap_with=[list(c) for c in F]) as s:
        return not s.solve()

def brute_unsat(F, n):
    # independent check: bitmask evaluation over all 2^n assignments
    masks = []
    for c in F:
        pos = sum(1 << (l-1) for l in c if l > 0); neg = sum(1 << (-l-1) for l in c if l < 0)
        masks.append((pos, neg))
    full = (1 << n) - 1
    for a in range(1 << n):
        na = full ^ a
        if all((a & p) or (na & q) for p, q in masks):
            return False
    return True

def subsumed(R, S):
    R = tuple(sorted(R, key=abs))
    for k in range(0, len(R)+1):
        for sub in itertools.combinations(R, k):
            if frozenset(sub) in S:
                return True
    return False

def saturate(F, w, cap=400000):
    S = set(frozenset(c) for c in F)
    occ = {}
    for c in S:
        for l in c: occ.setdefault(l, set()).add(c)
    queue = list(S); steps = 0
    while queue:
        C = queue.pop()
        if C not in S: continue
        for l in C:
            for D in list(occ.get(-l, ())):
                steps += 1
                R = (C - {l}) | (D - {-l})
                if len(R) > w: continue
                if any(-x in R for x in R): continue
                R = frozenset(R)
                if subsumed(R, S): continue
                S.add(R); queue.append(R)
                for x in R: occ.setdefault(x, set()).add(R)
                if len(R) == 0: return S, steps, True
                if len(S) > cap: raise RuntimeError('cap')
    return S, steps, False

def violated(S, a):  # a: dict var->bool
    return [c for c in S if not any((l > 0) == a[abs(l)] for l in c)]

def min_violation_assignment(S, n):
    # exact minimum by brute force over 2^n (n<=22) using bitmasks
    masks = []
    for c in S:
        pos = sum(1 << (l-1) for l in c if l > 0); neg = sum(1 << (-l-1) for l in c if l < 0)
        masks.append((pos, neg))
    full = (1 << n) - 1; best = None; arg = None
    for x in range(1 << n):
        nx = full ^ x
        v = 0
        for p, q in masks:
            if not ((x & p) or (nx & q)):
                v += 1
                if best is not None and v >= best: break
        if best is None or v < best:
            best, arg = v, x
    return best, {i: bool(arg >> (i-1) & 1) for i in range(1, n+1)}

def is_strict_stall(S, a, n):
    base = len(violated(S, a))
    for v in range(1, n+1):
        a[v] = not a[v]; nb = len(violated(S, a)); a[v] = not a[v]
        if nb < base: return False
    return True

def critical_pairs(S, a, w):
    true = lambda l: (l > 0) == a[abs(l)]
    V = [c for c in S if not any(true(l) for l in c)]
    crit = {}
    for D in S:
        t = [l for l in D if true(l)]
        if len(t) == 1: crit.setdefault(t[0], []).append(D)
    out = {'pairs': 0, 'novel_le_w': 0, 'dup_or_subsumed': 0, 'novel_gt_w': 0, 'min_novel_width': None}
    for C in V:
        for p in C:
            for D in crit.get(-p, []):
                out['pairs'] += 1
                R = frozenset((C - {p}) | (D - {-p}))
                assert not any(-x in R for x in R)
                assert not any(true(x) for x in R)  # resolvent false at a
                if subsumed(R, S): out['dup_or_subsumed'] += 1
                elif len(R) <= w: out['novel_le_w'] += 1
                else:
                    out['novel_gt_w'] += 1
                    if out['min_novel_width'] is None or len(R) < out['min_novel_width']:
                        out['min_novel_width'] = len(R)
    return out

def unit_prop(S, assign=None):
    a = dict(assign or {})
    changed = True
    while changed:
        changed = False
        for c in S:
            un = [l for l in c if abs(l) not in a]
            if any((l > 0) == a[abs(l)] for l in c if abs(l) in a): continue
            if not un: return None
            if len(un) == 1:
                a[abs(un[0])] = un[0] > 0; changed = True
    return a

def failed_literals(S, n):
    if unit_prop(S) is None: return 'UP_REFUTES'
    fl = []
    for v in range(1, n+1):
        for b in (True, False):
            if unit_prop(S, {v: b}) is None: fl.append(v if b else -v)
    both = [v for v in range(1, n+1) if v in fl and -v in fl]
    return {'failed': len(fl), 'both_polarities_failed': both}

def run(n, ratio, seeds, w):
    res = []
    for seed in seeds:
        F = rand3cnf(n, int(ratio*n), seed)
        if not unsat_minisat(F): continue
        rec = {'n': n, 'm': len(F), 'seed': seed, 'w': w}
        rec['brute_unsat'] = brute_unsat(F, n) if n <= 22 else None
        S, steps, empty = saturate(F, w)
        rec.update(sat_size=len(S), sat_steps=steps, empty_derived=empty,
                   width_hist={k: sum(1 for c in S if len(c) == k) for k in range(w+1)})
        if not empty:
            # independent closure re-check: no width<=w resolvent of S is unsubsumed
            closed = True
            Sl = list(S)
            for i, C in enumerate(Sl):
                for D in Sl[i+1:]:
                    piv = [l for l in C if -l in D]
                    if len(piv) != 1: continue
                    R = frozenset((C - {piv[0]}) | (D - {-piv[0]}))
                    if len(R) <= w and not subsumed(R, S): closed = False; break
                if not closed: break
            rec['independent_closure_check'] = closed
            best, a = min_violation_assignment(S, n)
            rec['min_violated'] = best
            rec['global_min_is_strict_stall'] = is_strict_stall(S, a, n)
            rec['critical'] = critical_pairs(S, a, w)
            rec['failed_literal'] = failed_literals(S, n)
            rec['stall_assignment'] = ''.join('1' if a[i] else '0' for i in range(1, n+1))
        res.append(rec)
    return res

if __name__ == '__main__':
    out = {}
    for (n, ratio, w) in [(14, 8.0, 3), (14, 8.0, 4), (18, 7.0, 4), (20, 6.0, 4), (22, 5.5, 4)]:
        out[f'n{n}_r{ratio}_w{w}'] = run(n, ratio, range(1, 13), w)
        print(n, ratio, w, [(r['seed'], r['empty_derived'], r.get('sat_size')) for r in out[f'n{n}_r{ratio}_w{w}']], flush=True)
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 'stall_saturation_random.out.json', 'w'), indent=1, default=str)
