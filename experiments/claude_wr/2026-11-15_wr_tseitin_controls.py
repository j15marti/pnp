"""W_R(N) control experiment (Claude worst-case-derivation log, run WR-0001).

For small 3-regular Tseitin formulas (3-CNF, odd charge => UNSAT) compute exactly:
  * minimum tree-like Resolution refutation size (decision-tree DP over restrictions),
  * minimum Resolution refutation width (width-bounded saturation),
  * Gaussian-elimination XOR-row operation count (an algorithm outside Resolution).
Each instance runs in a few seconds; the whole script is < 30 s (AGENTS.md runtime rule).
"""
import itertools, json, sys, time
from functools import lru_cache

GRAPHS = {
 "K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
 "K33": [(a,b) for a in range(3) for b in range(3,6)],
 "prism": [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
 "Q3": [(a,a^b) for a in range(8) for b in (1,2,4) if a < a^b],
 "Mobius8": [(i,(i+1)%8) for i in range(8)]+[(i,i+4) for i in range(4)],
}

def tseitin(edges):
    nv = max(max(e) for e in edges)+1
    charge = [1 if v == 0 else 0 for v in range(nv)]          # total charge odd
    clauses = []
    for v in range(nv):
        inc = [i for i,e in enumerate(edges) if v in e]
        for bits in itertools.product((0,1), repeat=len(inc)):
            if sum(bits) % 2 != charge[v]:                     # forbid wrong parity
                # clause falsified exactly by this assignment; literal = (var, sign)
                clauses.append(frozenset((x, 1-b) for x,b in zip(inc,bits)))
    return len(edges), clauses, charge, nv

def treelike_size(n, clauses):
    cl = [tuple(c) for c in clauses]
    @lru_cache(maxsize=None)
    def S(rho):  # rho: tuple of -1/0/1 per var
        for c in cl:   # falsified clause => leaf
            if all(rho[x] == 1-s for x,s in c):
                return 1
        best = None
        for x in range(n):
            if rho[x] != -1: continue
            r0 = rho[:x]+(0,)+rho[x+1:]; r1 = rho[:x]+(1,)+rho[x+1:]
            v = S(r0)+S(r1)+1
            if best is None or v < best: best = v
        return best
    val = S(tuple([-1]*n)); info = S.cache_info().currsize
    S.cache_clear(); return val, info

def resolve(a, b):
    piv = [x for x,s in a if (x,1-s) in b]
    if len(piv) != 1: return None
    x = piv[0]
    r = (a - {(x,0),(x,1)}) | (b - {(x,0),(x,1)})
    vs = [y for y,_ in r]
    return frozenset(r) if len(vs) == len(set(vs)) else None

def min_width(clauses, wmax=7):
    """Exact minimum refutation width: smallest w such that width-<=w saturation derives the empty clause.
    Literal-indexed saturation (each pair resolved once)."""
    for w in range(max(len(c) for c in clauses), wmax+1):
        known = set(clauses); bylit = {}
        for c in known:
            for l in c: bylit.setdefault(l, []).append(c)
        frontier = list(known)
        while frontier:
            new = []
            for a in frontier:
                for (x, s) in a:
                    for b in bylit.get((x, 1-s), ()):
                        r = resolve(a, b)
                        if r is not None and len(r) <= w and r not in known:
                            if len(r) == 0: return w
                            known.add(r); new.append(r)
                            for l in r: bylit.setdefault(l, []).append(r)
            frontier = new
    return None

def gauss_ops(edges, charge, nv):
    m = len(edges); rows = []
    for v in range(nv):
        mask = 0
        for i,e in enumerate(edges):
            if v in e: mask |= 1 << i
        rows.append((mask, charge[v]))
    ops = 0; piv_rows = []
    for col in range(m):
        idx = next((i for i,(r,_) in enumerate(rows) if r >> col & 1), None)
        if idx is None: continue
        p = rows.pop(idx)
        rows = [((r ^ p[0], c ^ p[1]) if r >> col & 1 else (r, c)) for r,c in rows]
        ops += sum(1 for _ in rows)
        piv_rows.append(p)
    contradiction = any(r == 0 and c == 1 for r,c in rows)
    return ops, contradiction

# Chunking: one graph per invocation (argv[2]); results merged into argv[1].
import os
out = json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
NOWIDTH = '--no-width' in sys.argv
for name in [a for a in sys.argv[2:] if not a.startswith('--')]:
    E = GRAPHS[name]
    t = time.time()
    n, C, ch, nv = tseitin(E)
    tl, states = treelike_size(n, C)
    w = None if NOWIDTH else min_width(C)
    g, contra = gauss_ops(E, ch, nv)
    out[name] = dict(vars=n, clauses=len(C), treelike_min_size=tl, dp_states=states,
                     min_res_width=w, gauss_rowops=g, gauss_detects_unsat=contra,
                     seconds=round(time.time()-t, 2))
    print(name, out[name], flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1)
