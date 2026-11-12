#!/usr/bin/env python3
"""Exact small-instance derivation-cost audit for the worst-case derivation target
W_R(N) = max_{F in UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi).

Usage: python3 2026-11-12_wcd_exact.py <family> <out.json> [tseitin graph list]
Each family is a separate invocation (chunking rule: each run < ~30 s).

Measures (all EXACT for the given instance):
  tree_size : minimum number of leaves of a tree-like resolution refutation
              (= min size of a decision tree solving the false-clause search
              problem; regular tree-like resolution is optimal for tree-like).
  width     : minimum resolution refutation width (width-bounded saturation).
  gauss_ops : for Tseitin instances, number of F2 row additions in the
              linear-algebra refutation (sum of all vertex parity equations).
"""
import sys, json, itertools, random, time
from functools import lru_cache

def lit(v, s):  # clause as (pos_mask, neg_mask)
    return (1 << v, 0) if s else (0, 1 << v)

def clause(lits):
    p = n = 0
    for v, s in lits:
        if s: p |= 1 << v
        else: n |= 1 << v
    return (p, n)

def php(m):  # m+1 pigeons, m holes; var x_{i,j}
    var = lambda i, j: i * m + j
    C = [clause([(var(i, j), 1) for j in range(m)]) for i in range(m + 1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m + 1), 2):
            C.append(clause([(var(a, j), 0), (var(b, j), 0)]))
    return (m + 1) * m, C

def tseitin(edges, nv):
    charge = [0] * nv; charge[0] = 1
    inc = [[k for k, e in enumerate(edges) if v in e] for v in range(nv)]
    C = []
    for v in range(nv):
        for bits in itertools.product([0, 1], repeat=len(inc[v])):
            if sum(bits) % 2 != charge[v]:  # forbid this assignment
                C.append(clause([(e, 1 - b) for e, b in zip(inc[v], bits)]))
    return len(edges), C, inc, charge

def random_unsat(n, m, seed):
    rng = random.Random(seed)
    while True:
        C = []
        for _ in range(m):
            vs = rng.sample(range(n), 3)
            C.append(clause([(v, rng.randint(0, 1)) for v in vs]))
        if not any(sat(C, a) for a in range(1 << n)):
            return C
        seed += 1000; rng = random.Random(seed)

def sat(C, a):
    return all((p & a) or (nm & ~a) for p, nm in C)

def min_tree_size(n, C):
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def f(setm, val):
        # falsified clause present? -> leaf
        for p, nm in C:
            if ((p | nm) & ~setm) == 0 and (p & val) == 0 and (nm & val) == nm:
                return 1
        best = None
        free = full & ~setm
        v = 0
        while free:
            if free & 1:
                b = 1 << v
                s = f(setm | b, val) + f(setm | b, val | b)
                if best is None or s < best: best = s
            free >>= 1; v += 1
        return best
    return f(0, 0)

def min_width(n, C):
    start = set(C)
    for w in range(max(bin(p | q).count('1') for p, q in C), n + 1):
        S = {c for c in start}
        frontier = list(S)
        while frontier:
            new = []
            Sl = list(S)
            for c1 in frontier:
                for c2 in Sl:
                    clash = (c1[0] & c2[1]) | (c1[1] & c2[0])
                    if clash and (clash & (clash - 1)) == 0:
                        r = ((c1[0] | c2[0]) & ~clash, (c1[1] | c2[1]) & ~clash)
                        if r[0] & r[1]: continue
                        if bin(r[0] | r[1]).count('1') > w: continue
                        if r == (0, 0): return w
                        if r not in S:
                            S.add(r); new.append(r)
            frontier = new
    return None

def main():
    fam, out = sys.argv[1], sys.argv[2]
    rows = []
    t0 = time.time()
    if fam == 'php':
        for m in (2, 3):
            n, C = php(m)
            rows.append(dict(name=f'PHP^{m+1}_{m}', n=n, m=len(C),
                             tree_size=min_tree_size(n, C), width=min_width(n, C)))
    elif fam == 'tseitin':
        graphs = {
            'K4': ([(a, b) for a, b in itertools.combinations(range(4), 2)], 4),
            'K33': ([(a, b) for a in range(3) for b in range(3, 6)], 6),
            'Q3': ([(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)], 8),
            'C8': ([(i, (i + 1) % 8) for i in range(8)], 8),
        }
        sel = sys.argv[3].split(',') if len(sys.argv) > 3 else list(graphs)
        for name in sel:
            E, nv = graphs[name]
            n, C, inc, ch = tseitin(E, nv)
            ta = time.time(); ts = min_tree_size(n, C); tb = time.time()
            wd = min_width(n, C) if n <= 9 else 'not computed (chunk budget)'
            rows.append(dict(name=f'Tseitin({name})', n=n, m=len(C),
                             tree_size=ts, width=wd, gauss_ops=nv - 1,
                             tree_seconds=round(tb - ta, 2)))
    elif fam == 'random':
        for n, seed in ((8, 1), (10, 2), (12, 3)):
            C = random_unsat(n, 6 * n, seed)
            rows.append(dict(name=f'rand3CNF(n={n},m={6*n},seed={seed})', n=n, m=len(C),
                             tree_size=min_tree_size(n, C), width=min_width(n, C)))
    json.dump(dict(family=fam, seconds=round(time.time() - t0, 2), rows=rows),
              open(out, 'w'), indent=1)
    print(json.dumps(rows, indent=1))

if __name__ == '__main__':
    main()
