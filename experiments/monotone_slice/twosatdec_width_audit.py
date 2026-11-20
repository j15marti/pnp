"""TWOSATDEC-WIDTH1 audit: free exact 2-SAT depth-r certificates vs density.

Reconstructs the TWOSATDEC exact-layer protocol (generator described in
research/explorations/monotone-slice/*TWOSATDEC*.md; original code was never
committed) and measures the minimum certifying depth r on UNSAT draws.

Usage: python3 twosatdec_width_audit.py replay
       python3 twosatdec_width_audit.py density DELTA Q N RMAX SEED
"""
import itertools, random, sys, time, json

def clause_list(q):
    out = []
    for tri in itertools.combinations(range(q), 3):
        for s in range(8):
            out.append(tuple((v + 1) if (s >> b) & 1 else -(v + 1) for b, v in enumerate(tri)))
    return out

def sample(q, t, n, seed):
    L = clause_list(q); rng = random.Random(seed)
    return [rng.sample(L, t) for _ in range(n)]

def unit_prop(clauses, assign):
    """assign: dict var->bool. Returns (conflict, reduced clause list)."""
    a = dict(assign)
    cls = clauses
    while True:
        new, unit, changed = [], None, False
        for c in cls:
            keep = []; sat = False
            for l in c:
                v = abs(l)
                if v in a:
                    if a[v] == (l > 0): sat = True; break
                else: keep.append(l)
            if sat: continue
            if not keep: return True, None
            if len(keep) == 1 and unit is None: unit = keep[0]
            new.append(tuple(keep))
        if unit is None: return False, new
        a[abs(unit)] = unit > 0; cls = new

def two_sat_unsat(cls):
    """True iff the width<=2 skeleton is unsatisfiable (implication graph SCC)."""
    two = [c for c in cls if len(c) <= 2]
    lits = set()
    adj = {}
    for c in two:
        x, y = (c[0], c[0]) if len(c) == 1 else c
        adj.setdefault(-x, []).append(y); adj.setdefault(-y, []).append(x)
        lits.update([x, -x, y, -y])
    idx, low, st, on, comp, cnt = {}, {}, [], set(), {}, [0]
    sys.setrecursionlimit(10000)
    def dfs(u):
        idx[u] = low[u] = cnt[0]; cnt[0] += 1; st.append(u); on.add(u)
        for w in adj.get(u, []):
            if w not in idx: dfs(w); low[u] = min(low[u], low[w])
            elif w in on: low[u] = min(low[u], idx[w])
        if low[u] == idx[u]:
            while True:
                w = st.pop(); on.discard(w); comp[w] = u
                if w == u: break
    for u in lits:
        if u not in idx: dfs(u)
    return any(comp[l] == comp[-l] for l in lits if l > 0)

def branch_closed(F, assign):
    conf, red = unit_prop(F, assign)
    return conf or two_sat_unsat(red)

def certifies(F, S):
    for bits in itertools.product((False, True), repeat=len(S)):
        if not branch_closed(F, dict(zip(S, bits))): return False
    return True

def dpll(cls, a=None):
    conf, red = unit_prop(cls, a or {})
    if conf: return False
    if not red: return True
    v = abs(red[0][0])
    return dpll(red, {v: True}) or dpll(red, {v: False})

def min_depth(F, q, rmax, deadline):
    for r in range(rmax + 1):
        for S in itertools.combinations(range(1, q + 1), r):
            if time.time() > deadline: return None, 'timeout'
            if certifies(F, S): return r, list(S)
    return None, '>rmax'

if __name__ == '__main__':
    if sys.argv[1] == 'replay':
        q = 26; t = int(3.5 * q)
        fs = sample(q, t, 16, 20261005)
        res = [dpll(F) for F in fs]
        print(json.dumps({'q': q, 't': t, 'SAT': sum(res), 'UNSAT_idx': [i for i, s in enumerate(res) if not s]}))
    else:
        delta, q, n, rmax, seed = float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        t = int(delta * q); t0 = time.time()
        fs = sample(q, t, n, seed); rows = []
        for i, F in enumerate(fs):
            if dpll(F): rows.append({'i': i, 'sat': True}); continue
            r, S = min_depth(F, q, rmax, t0 + 25)
            rows.append({'i': i, 'sat': False, 'min_r': r, 'witness': S})
        print(json.dumps({'delta': delta, 'q': q, 't': t, 'N': n, 'rmax': rmax, 'seed': seed,
                          'elapsed': round(time.time() - t0, 2), 'rows': rows}))
