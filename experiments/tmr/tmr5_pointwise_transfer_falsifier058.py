#!/usr/bin/env python3
"""TMR-5/058: pointwise algorithm-to-derivation transfer falsifier (finite illustration).

Revision tmr5-pointwise-transfer058.v1, deterministic, no randomness.
For explicit P-uniform UNSAT families (PHP_n^{n+1}, odd-charge Tseitin on
small 3-regular graphs) compute EXACT minimum decision-tree leaf count
L(F) (= minimum DPLL tree; minimum tree-like resolution refutation size
lies in [L, 2L-1]) by memoized recursion over restricted clause sets, and
count the elementary comparisons of a CORRECT total decider A that
recognises the canonical encoding (falling back to brute force otherwise).
Finite results are COMPUTATIONAL; asymptotics are KNOWN THEOREMS (Haken 1985,
Urquhart 1987, Ben-Sasson--Wigderson 2001).
"""
import itertools, json, sys, time, hashlib
from functools import lru_cache

def php(n):  # n+1 pigeons, n holes; var p(i,j)
    v = lambda i, j: i * n + j + 1
    cl = [tuple(v(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for a, b in itertools.combinations(range(n + 1), 2):
            cl.append((-v(a, j), -v(b, j)))
    return (n + 1) * n, cl

def tseitin(edges, charge):
    nv = len(edges); cl = []
    verts = sorted({u for e in edges for u in e})
    for x in verts:
        inc = [k + 1 for k, e in enumerate(edges) if x in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[x]:  # forbid assignments with wrong parity
                cl.append(tuple(-l if s else l for l, s in zip(inc, signs)))
    return nv, cl

def min_leaves(cls):
    sys.setrecursionlimit(10000)
    memo = {}
    def simp(cs, lit):
        out = []
        for c in cs:
            if lit in c: continue
            out.append(tuple(l for l in c if l != -lit))
        return frozenset(out)
    def L(cs):
        if () in cs: return 1
        if cs in memo: return memo[cs]
        vars_ = {abs(l) for c in cs for l in c}
        best = None
        for x in sorted(vars_):
            a = simp(cs, x); b = simp(cs, -x)
            # quick lower bound 1 each
            if best is not None and best <= 2: break
            la = L(a)
            if best is not None and la + 1 >= best: continue
            t = la + L(b)
            if best is None or t < best: best = t
        if best is None: raise ValueError("satisfiable branch reached")
        memo[cs] = best
        return best
    return L(frozenset(tuple(sorted(c)) for c in cls)), len(memo)

def decider_cost(n, cls):
    """Correct total decider A: if input == canonical PHP_k for k with matching
    size, answer UNSAT; else brute force. Return elementary literal comparisons
    used on the canonical instance (input-length linear)."""
    _, ref = php(n)
    comps = 0
    if len(ref) != len(cls): return None
    for c, d in zip(cls, ref):
        comps += 1 + len(c)
        if c != d: return None
    return comps

def brute_unsat(nv, cls):
    for a in range(1 << nv):
        if all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in cls):
            return False
    return True

rows = []; t0 = time.time()
for n in range(1, 4):  # PHP_4^5 (20 vars) exceeds the 30 s stage budget; not executed
    nv, cls = php(n)
    if nv <= 20: assert brute_unsat(nv, cls)
    t = time.time(); L, states = min_leaves(cls)
    size = sum(len(c) for c in cls)
    rows.append(dict(family="PHP", n=n, vars=nv, clauses=len(cls), literals=size,
                     min_dt_leaves=L, treeres_lower=L, treeres_upper=2 * L - 1,
                     memo_states=states, decider_comparisons=decider_cost(n, cls),
                     secs=round(time.time() - t, 3)))
graphs = {"K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
          "K33": [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
          "prism": [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
          "cube": [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)]}
for name, E in graphs.items():
    verts = sorted({u for e in E for u in e})
    ch = {x: (1 if x == 0 else 0) for x in verts}
    nv, cls = tseitin(E, ch); assert brute_unsat(nv, cls)
    t = time.time(); L, states = min_leaves(cls)
    rows.append(dict(family="Tseitin-odd", graph=name, vars=nv, clauses=len(cls),
                     literals=sum(len(c) for c in cls), min_dt_leaves=L,
                     treeres_lower=L, treeres_upper=2 * L - 1, memo_states=states,
                     gaussian_elim_rowops_upper=len(verts) ** 2,
                     secs=round(time.time() - t, 3)))
out = dict(revision="tmr5-pointwise-transfer058.v1", seed=None, python=sys.version.split()[0],
           rows=rows, total_secs=round(time.time() - t0, 2))
src = open(__file__, "rb").read()
out["source_sha256"] = hashlib.sha256(src).hexdigest()
print(json.dumps(out, indent=1))
