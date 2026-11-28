#!/usr/bin/env python3
"""Lazy (counterexample-guided) exact decision of AG(2t)-n.

Same instance as ag2t_threshold.py (NAE over all 2t-subsets of F_2^k with
XOR 0), but blocks are added lazily: solve the current clause set; for the
model, test each colour class X for a zero-sum subset of exactly 2t
distinct points by an exact subset-sum DP over (size, xor); if one exists,
add that block's two NAE clauses and repeat.  Termination: either the
lazily built clause set (a SUBSET of the true clauses) is UNSAT -- so the
full instance is UNSAT, and the added blocks form an explicit UNSAT core --
or a model passes the exact DP check in both classes -- a genuine YES
witness, re-verified from scratch.  Pin x_0 = 0 (complement symmetry).
"""
import sys, json, time
from pysat.solvers import Solver

def zero_sum_subset(X, s, n):
    """Return a list of s distinct elements of X with XOR 0, or None (exact)."""
    # reach[c] = dict xor -> (prev_xor, element) parent pointers, layered by index
    m = len(X)
    if s > m:
        return None
    # layers: R[i][c] = set of xors reachable using exactly c elements from X[:i]
    R = [[set() for _ in range(s + 1)] for _ in range(m + 1)]
    R[0][0].add(0)
    for i, x in enumerate(X):
        for c in range(s + 1):
            R[i + 1][c] |= R[i][c]
            if c > 0:
                R[i + 1][c] |= {v ^ x for v in R[i][c - 1]}
    if 0 not in R[m][s]:
        return None
    out, c, v = [], s, 0
    for i in range(m, 0, -1):
        x = X[i - 1]
        if v in R[i - 1][c]:
            continue
        out.append(x); v ^= x; c -= 1
    assert c == 0 and v == 0 and len(set(out)) == s
    return out

def decide(k, t, maxit=200000):
    n = 1 << k; s = 2 * t
    t0 = time.time()
    blocks = []
    with Solver(name='cadical153') as S:
        S.add_clause([-1])
        it = 0
        while True:
            it += 1
            if not S.solve():
                return dict(t=t, arity=s, k=k, n=n, status='UNSAT', core_blocks=len(blocks),
                            iterations=it, seconds=round(time.time() - t0, 2), blocks=blocks)
            mv = {abs(v): v > 0 for v in S.get_model()}
            col = [1 if mv.get(p + 1, False) else 0 for p in range(n)]
            found = None
            for c in (0, 1):
                X = [p for p in range(n) if col[p] == c]
                B = zero_sum_subset(X, s, n)
                if B is not None:
                    found = sorted(B); break
            if found is None:
                ones = [p for p in range(n) if col[p]]
                # independent re-verification by brute recomputation of DP on both classes
                assert zero_sum_subset(ones, s, n) is None
                assert zero_sum_subset([p for p in range(n) if not col[p]], s, n) is None
                return dict(t=t, arity=s, k=k, n=n, status='SAT', iterations=it,
                            lazily_added_blocks=len(blocks), class_sizes=[n - len(ones), len(ones)],
                            class1_points=ones, seconds=round(time.time() - t0, 2))
            x = 0
            for p in found: x ^= p
            assert x == 0 and len(set(found)) == s
            blocks.append(found)
            S.add_clause([p + 1 for p in found]); S.add_clause([-(p + 1) for p in found])
            if it > maxit:
                return dict(t=t, k=k, n=n, status='UNKNOWN_CAP', iterations=it)

if __name__ == '__main__':
    out = []
    for a in sys.argv[1:]:
        t, k = map(int, a.split(','))
        r = decide(k, t)
        short = {kk: v for kk, v in r.items() if kk not in ('blocks', 'class1_points')}
        print(json.dumps(short), flush=True)
        out.append(r)
    json.dump(out, open('ag2t_cegar_out_%s.json' % '_'.join(a.replace(',', 'k') for a in sys.argv[1:]), 'w'))
