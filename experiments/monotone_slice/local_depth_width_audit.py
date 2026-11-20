"""LOCALDEPTH-WIDTH1 audit: minimal free-2-SAT decision depth on the exact 3-CNF layer.

Protocol (TWOSATDEC family): lexicographic proper 3-clause list over q variables,
triples increasing, sign pattern s in 0..7 with bit j for the j-th variable of the
triple, bit=1 positive literal. Instances: random.Random(seed).sample(list, t),
drawn sequentially from one RNG.  A variable set S certifies if every assignment of S,
after unit propagation, yields an empty clause or an unsatisfiable width<=2 skeleton.
Usage: python3 local_depth_width_audit.py q density N rmax seed
"""
import itertools, random, sys, time

def clause_list(q):
    L = []
    for tri in itertools.combinations(range(q), 3):
        for s in range(8):
            L.append(tuple((v + 1) if (s >> j) & 1 else -(v + 1) for j, v in enumerate(tri)))
    return L

def up(clauses, assign):
    """Unit propagation. Returns (conflict, assign, reduced clauses)."""
    a = dict(assign)
    while True:
        changed = False; red = []
        for c in clauses:
            lits = []; sat = False
            for l in c:
                v = a.get(abs(l))
                if v is None: lits.append(l)
                elif v == (l > 0): sat = True; break
            if sat: continue
            if not lits: return True, a, None
            if len(lits) == 1:
                a[abs(lits[0])] = lits[0] > 0; changed = True
            red.append(lits)
        if not changed: return False, a, red

def twosat_unsat(cls):
    """cls: list of width-1/2 clauses. True iff unsatisfiable (implication-graph SCC)."""
    g = {}
    def add(u, w): g.setdefault(u, []).append(w); g.setdefault(w, [])
    for c in cls:
        if len(c) == 1: add(-c[0], c[0])
        else: add(-c[0], c[1]); add(-c[1], c[0])
    idx = {}; low = {}; st = []; on = set(); comp = {}; cnt = [0]
    sys.setrecursionlimit(10000)
    def sc(v):
        idx[v] = low[v] = cnt[0]; cnt[0] += 1; st.append(v); on.add(v)
        for w in g[v]:
            if w not in idx: sc(w); low[v] = min(low[v], low[w])
            elif w in on: low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            while True:
                w = st.pop(); on.discard(w); comp[w] = v
                if w == v: break
    for v in list(g):
        if v not in idx: sc(v)
    return any(v in comp and -v in comp and comp[v] == comp[-v] for v in g)

def branch_refuted(F, rho):
    conf, a, red = up(F, rho)
    if conf: return True
    return twosat_unsat([c for c in red if len(c) <= 2])

def certifies(F, S):
    for bits in itertools.product((False, True), repeat=len(S)):
        if not branch_refuted(F, dict(zip(S, bits))): return False
    return True

def sat(F, q):
    def dp(a):
        conf, a2, red = up(F, a)
        if conf: return False
        if not red: return True
        v = abs(red[0][0])
        return dp({**a2, v: True}) or dp({**a2, v: False})
    return dp({})

def min_depth(F, q, rmax, budget):
    t0 = time.time()
    for r in range(rmax + 1):
        n_cert = 0; first = None
        for S in itertools.combinations(range(1, q + 1), r):
            if certifies(F, S):
                n_cert += 1; first = first or S
                break
            if time.time() - t0 > budget: return None, r, None
        if n_cert: return r, r, first
    return None, rmax + 1, None

if __name__ == "__main__":
    q, dens, N, rmax, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    t = int(dens * q); L = clause_list(q); rng = random.Random(seed); T0 = time.time()
    print(f"q={q} density={dens} t={t} M={len(L)} N={N} rmax={rmax} seed={seed}")
    for i in range(N):
        F = rng.sample(L, t)
        if sat(F, q): print(f"idx {i}: SAT"); continue
        r, lo, S = min_depth(F, q, rmax, 25.0 / N)
        if r is None: print(f"idx {i}: UNSAT min_depth >= {lo} (search {'budget' if lo<=rmax else 'rmax'} exhausted)")
        else: print(f"idx {i}: UNSAT min_depth = {r} first certifying set {S}")
    print(f"elapsed {time.time()-T0:.2f}s")
