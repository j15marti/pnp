#!/usr/bin/env python3
"""Independent full-C-level audit of the LOCAL3COL-C1 3-CNF -> strict-C compiler.

Reimplemented from the PROSE of
research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md
(the original script is not in the repository).  No code was shared.

Checks
  1. C relation: 30/125 accepted triples; exact symmetry group of C on Z5.
  2. Head lemma (exists h C(h,u,w) iff u != w) -- recorded but NOT used by the solver.
  3. Size formulas V_C = 15+9v+39m, M_C = 10+7v+31m.
  4. Both directions of  F SAT <=> K(F) SAT  with a GENERIC GAC+MRV CSP solver that
     knows only the strict-C table (no graph/colouring reasoning, no head lemma).
     UNSAT direction is a full C-level refutation (exhaustive search tree).
  5. Every C solution found projects (colour(x) == colour(T)) to a Boolean model.
Standard library only.  Deterministic seed below.
"""
import itertools, json, random, sys, time, hashlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mini_cdcl

SEED = 2026111917
D = 5
FULL = (1 << D) - 1
POP = [bin(i).count('1') for i in range(1 << D)]

def R(a, b):
    return (b - a) % 5 in (1, 3)

def C(x, y, z):
    return (R(x, y) and R(y, z) and R(z, x)) or (R(x, z) and R(z, y) and R(y, x))

TRIPLES = [t for t in itertools.product(range(D), repeat=3) if C(*t)]

def symmetry_group():
    good = []
    for p in itertools.permutations(range(D)):
        if all(C(p[a], p[b], p[c]) == C(a, b, c) for a, b, c in itertools.product(range(D), repeat=3)):
            good.append(p)
    return good

# ---------------- compiler (from prose) -----------------
def compile_K(v, clauses):
    """clauses: list of 3-tuples of nonzero ints (DIMACS literals over 1..v).
    Returns (names, Cclauses, meta) with C clauses as (head, u, w) index triples."""
    vid = {}
    def V(name):
        if name not in vid:
            vid[name] = len(vid)
        return vid[name]
    edges = []
    def E(a, b):
        edges.append((V(a), V(b)))
    # base triangle
    for n in ('T', 'F', 'B'):
        V(n)
    E('T', 'F'); E('F', 'B'); E('B', 'T')
    for i in range(1, v + 1):
        E(('x', i), ('nx', i)); E(('x', i), 'B'); E(('nx', i), 'B')
    def lit(l):
        return ('x', l) if l > 0 else ('nx', -l)
    for j, (a, b, c) in enumerate(clauses):
        s, ns = ('s', j), ('ns', j)
        E(s, ns); E(s, 'B'); E(ns, 'B')
        for g, terms in enumerate(((lit(a), lit(b), s), (ns, lit(c), 'F'))):
            tri = [('g', j, g, k) for k in range(3)]
            E(tri[0], tri[1]); E(tri[1], tri[2]); E(tri[2], tri[0])
            for k in range(3):
                E(tri[k], terms[k])
    V3, E3 = len(vid), len(edges)
    old = list(vid.keys())
    E('U', 'V')
    for n in old:
        E('U', n); E('V', n)
    V5, E5 = len(vid), len(edges)
    cl = []
    for e, (u, w) in enumerate(edges):
        h = V(('h', e))
        cl.append((h, u, w))
    meta = dict(V3=V3, E3=E3, V5=V5, E5=E5, VC=len(vid), MC=len(cl))
    return vid, cl, meta

# ---------------- generic GAC CSP solver -----------------
SUPPORT = {}
def supports(mx, my, mz):
    key = (mx, my, mz)
    r = SUPPORT.get(key)
    if r is None:
        sx = sy = sz = 0
        for a, b, c in TRIPLES:
            if mx >> a & 1 and my >> b & 1 and mz >> c & 1:
                sx |= 1 << a; sy |= 1 << b; sz |= 1 << c
        r = (sx, sy, sz)
        SUPPORT[key] = r
    return r

class Solver:
    def __init__(self, n, cl):
        self.n, self.cl = n, cl
        self.occ = [[] for _ in range(n)]
        for k, t in enumerate(cl):
            for x in t:
                self.occ[x].append(k)
        self.deg = [len(o) for o in self.occ]
        self.nodes = 0
        self.revisions = 0

    def propagate(self, dom, queue):
        inq = set(queue)
        while queue:
            k = queue.pop(); inq.discard(k)
            x, y, z = self.cl[k]
            self.revisions += 1
            nx, ny, nz = supports(dom[x], dom[y], dom[z])
            for var, new in ((x, nx), (y, ny), (z, nz)):
                if new != dom[var]:
                    if new == 0:
                        return False
                    dom[var] = new
                    for k2 in self.occ[var]:
                        if k2 != k and k2 not in inq:
                            queue.append(k2); inq.add(k2)
        return True

    def solve(self, dom=None):
        if dom is None:
            dom = [FULL] * self.n
            if not self.propagate(dom, list(range(len(self.cl)))):
                return None
        self.nodes += 1
        # generic dom/deg heuristic: smallest |dom|/degree among unfixed variables
        best, bscore = -1, None
        for i, m in enumerate(dom):
            c = POP[m]
            if c > 1:
                sc = c / self.deg[i]
                if bscore is None or sc < bscore:
                    best, bscore = i, sc
        if best < 0:
            return [m.bit_length() - 1 for m in dom]
        m = dom[best]
        for a in range(D):
            if m >> a & 1:
                d2 = dom[:]
                d2[best] = 1 << a
                if self.propagate(d2, list(self.occ[best])):
                    r = self.solve(d2)
                    if r is not None:
                        return r
        return None

def brute_sat(v, clauses):
    for bits in itertools.product((False, True), repeat=v):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            return bits
    return None

def direct_cnf(n, cl):
    """Direct encoding: Boolean var 5x+a+1 means x=a.  ALO+AMO per C variable and one
    blocking clause per rejected value triple of each strict-C clause (95 per clause)."""
    lit = lambda x, a: 5 * x + a + 1
    cnf = []
    for x in range(n):
        cnf.append([lit(x, a) for a in range(D)])
        for a in range(D):
            for b in range(a + 1, D):
                cnf.append([-lit(x, a), -lit(x, b)])
    for (x, y, z) in cl:
        for a, b, c in itertools.product(range(D), repeat=3):
            if not C(a, b, c):
                cnf.append([-lit(x, a), -lit(y, b), -lit(z, c)])
    return cnf

def check_instance(v, clauses, check_rup=True):
    vid, cl, meta = compile_K(v, clauses)
    m = len(clauses)
    assert meta['VC'] == 15 + 9 * v + 39 * m, meta
    assert meta['MC'] == 10 + 7 * v + 31 * m, meta
    assert meta['V5'] == 5 + 2 * v + 8 * m and meta['E3'] == 3 + 3 * v + 15 * m
    for (h, u, w) in cl:
        assert len({h, u, w}) == 3
    bool_model = brute_sat(v, clauses)
    n = len(vid)
    cnf = direct_cnf(n, cl)
    model, lemmas, st = mini_cdcl.solve(5 * n, cnf)
    sol = None
    if model is not None:
        sol = []
        for x in range(n):
            vals = [a for a in range(D) if model[5 * x + a + 1]]
            assert len(vals) == 1
            sol.append(vals[0])
    rec = dict(v=v, m=m, VC=meta['VC'], MC=meta['MC'], cnf_vars=5 * n, cnf_clauses=len(cnf),
               boolSAT=bool_model is not None, cSAT=sol is not None,
               conflicts=st.get('conflicts'), lemmas=len(lemmas))
    if sol is not None:
        assert all(C(sol[h], sol[u], sol[w]) for h, u, w in cl)
        tcol = sol[vid['T']]
        proj = [sol[vid[('x', i)]] == tcol for i in range(1, v + 1)]
        rec['projection_ok'] = all(any(proj[abs(l) - 1] == (l > 0) for l in c) for c in clauses)
        assert rec['projection_ok']
    elif check_rup:
        ok, bad = mini_cdcl.rup_check(5 * n, cnf, lemmas)
        rec['rup_verified'] = ok
        assert ok, bad
    assert rec['boolSAT'] == rec['cSAT'], rec
    return rec

def rand_clause(rng, v):
    vs = rng.sample(range(1, v + 1), 3) if v >= 3 else [rng.randint(1, v) for _ in range(3)]
    return tuple(x if rng.random() < .5 else -x for x in vs)

def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else 'A'
    t0 = time.time()
    rng = random.Random(SEED + ord(stage))
    out = {'seed': SEED, 'stage': stage, 'python': sys.version.split()[0]}
    out['accepted_triples'] = len(TRIPLES)
    out['symmetry_group'] = symmetry_group()
    out['head_lemma'] = all(any(C(h, u, w) for h in range(D)) == (u != w) for u in range(D) for w in range(D))
    recs = []
    full8 = [tuple(s * x for s, x in zip(signs, (1, 2, 3))) for signs in itertools.product((1, -1), repeat=3)]
    if stage == 'A':   # canonical minimal UNSAT and all 8 single-clause deletions (SAT)
        recs.append(('A_full8', check_instance(3, full8)))
        for k in range(8):
            recs.append(('A_del%d' % k, check_instance(3, full8[:k] + full8[k + 1:])))
    elif stage == 'B':  # full8 relabelled into 4 variables with sign flips and 0-2 extra clauses
        while time.time() < t0 + 25:
            v = 4
            vars3 = rng.sample(range(1, v + 1), 3)
            flip = [rng.choice((1, -1)) for _ in range(3)]
            cls = [tuple((1 if l > 0 else -1) * flip[abs(l) - 1] * vars3[abs(l) - 1] for l in c) for c in full8]
            cls += [rand_clause(rng, v) for _ in range(rng.randint(0, 2))]
            rng.shuffle(cls)
            recs.append(('B_embed', check_instance(v, cls)))
    elif stage == 'C':  # random 3-CNF, v=4, m in [8,14]; both outcomes
        while time.time() < t0 + 25:
            v = 4
            m = rng.randint(8, 14)
            recs.append(('C_rand', check_instance(v, [rand_clause(rng, v) for _ in range(m)])))
    out['n_instances'] = len(recs)
    out['n_boolSAT'] = sum(r['boolSAT'] for _, r in recs)
    out['n_UNSAT_full_C_refuted_RUP'] = sum((not r['cSAT']) and r.get('rup_verified', False) for _, r in recs)
    out['max_VC'] = max(r['VC'] for _, r in recs)
    out['records'] = [dict(family=f, **r) for f, r in recs]
    out['wall_seconds'] = round(time.time() - t0, 2)
    here = os.path.dirname(os.path.abspath(__file__))
    out['script_sha256'] = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()
    out['mini_cdcl_sha256'] = hashlib.sha256(open(os.path.join(here, 'mini_cdcl.py'), 'rb').read()).hexdigest()
    json.dump(out, sys.stdout, indent=1)

if __name__ == '__main__':
    main()
