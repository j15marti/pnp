#!/usr/bin/env python3
"""WORSTCASE-DERIV-0001: exact minimum tree-like Resolution size (free optimal
sequence) versus algebraic shortcuts on hostile families.

Signed hypergraph: clause = hyperedge whose vertices carry sign +/-.
Minimal reduced state: a minimal unsatisfiable core (deletion-based MUS).
Minimal work (tree-like R): exact minimum decision-tree leaf count over all
branching orders, memoized on the residual signed hypergraph; tree-like
refutation clause count = 2*leaves - 1 (regular optimal trees suffice).
Each invocation runs one family chunk (CLI arg) to obey the 30 s rule.
"""
import itertools, json, sys, time
from functools import lru_cache

def simplify(cls, lit):
    out = []
    for c in cls:
        if lit in c: continue
        d = c - {-lit}
        out.append(d)
    return out

def is_sat(cls):
    cls = [frozenset(c) for c in cls]
    if any(len(c) == 0 for c in cls): return False
    if not cls: return True
    v = abs(next(iter(min(cls, key=len))))
    return is_sat(simplify(cls, v)) or is_sat(simplify(cls, -v))

def mus(cls):
    core = list(cls)
    i = 0
    while i < len(core):
        trial = core[:i] + core[i+1:]
        if not is_sat(trial): core = trial
        else: i += 1
    return core

def min_tree_leaves(cls):
    @lru_cache(maxsize=None)
    def f(state):
        if any(len(c) == 0 for c in state): return 1
        vs = sorted({abs(l) for c in state for l in c})
        best = None
        for v in vs:
            a = f(canon(simplify(state, v)))
            if best is not None and a >= best: continue
            b = f(canon(simplify(state, -v)))
            if best is None or a + b < best: best = a + b
        return best
    def canon(s):
        return frozenset(frozenset(c) for c in s)
    r = f(canon(cls))
    return r, f.cache_info().currsize

def php(n):  # n+1 pigeons, n holes; var p(i,j)
    var = lambda i, j: i * n + j + 1
    cls = [frozenset(var(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for i, k in itertools.combinations(range(n + 1), 2):
            cls.append(frozenset({-var(i, j), -var(k, j)}))
    return cls

def tseitin(edges, charge):
    idx = {e: t + 1 for t, e in enumerate(edges)}
    nv = 1 + max(max(e) for e in edges)
    cls = []
    for v in range(nv):
        inc = [idx[e] for e in edges if v in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[v]:  # forbid assignments with wrong parity
                cls.append(frozenset(x if s == 0 else -x for x, s in zip(inc, signs)))
    return cls, len(edges), nv

def prism(k):  # circular ladder CL_k, cubic, 3k edges
    E = [(i, (i + 1) % k) for i in range(k)] + [(k + i, k + (i + 1) % k) for i in range(k)] + [(i, k + i) for i in range(k)]
    return [tuple(sorted(e)) for e in E], 2 * k

def gauss_ops(cls_edges, nv, charge, ne):
    """Fully charged F2 elimination op count on the parity system (bit-ops)."""
    rows = []
    for v in range(nv):
        r = 0
        for t, e in enumerate(cls_edges):
            if v in e: r |= 1 << t
        rows.append([r, charge[v]])
    ops = 0; piv = 0
    for col in range(ne):
        p = next((i for i in range(piv, len(rows)) if rows[i][0] >> col & 1), None)
        if p is None: continue
        rows[piv], rows[p] = rows[p], rows[piv]
        for i in range(len(rows)):
            if i != piv and rows[i][0] >> col & 1:
                rows[i][0] ^= rows[piv][0]; rows[i][1] ^= rows[piv][1]; ops += ne + 1
        piv += 1
    contradiction = any(r[0] == 0 and r[1] == 1 for r in rows)
    return ops, contradiction

def run(chunk):
    out = []
    t0 = time.time()
    if chunk == "php":
        for n in (1, 2, 3):
            F = php(n); core = mus(F); L, memo = min_tree_leaves(core)
            out.append(dict(family="PHP", n=n, vars=n*(n+1), clauses=len(F), mus=len(core),
                            min_leaves=L, min_treeres_clauses=2*L-1, memo=memo,
                            note="CP refutation is polynomial (Cook-Coullard-Turan 1987); not executed here"))
    elif chunk.startswith("tseitin"):
        ks = {"tseitin_a": (2, 3, 4), "tseitin_b": (5,)}[chunk]
        for k in ks:
            E, nv = prism(k); ch = [1] + [0] * (nv - 1)
            F, ne, _ = tseitin(E, ch)
            core = mus(F); L, memo = min_tree_leaves(core)
            ops, contra = gauss_ops(E, nv, ch, ne)
            out.append(dict(family="Tseitin-prism", k=k, vars=ne, clauses=len(F), mus=len(core),
                            min_leaves=L, min_treeres_clauses=2*L-1, memo=memo,
                            gauss_bitops=ops, gauss_contradiction=contra))
    return dict(chunk=chunk, results=out, seconds=round(time.time() - t0, 2))

if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1]), indent=1))
