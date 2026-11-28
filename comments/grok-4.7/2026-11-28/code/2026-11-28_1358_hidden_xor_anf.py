#!/usr/bin/env python3
"""Grok 4.7, 2026-11-28 ~14:00 KST.  Hidden-XOR (Tseitin o gadget) families vs.
width-2 RUP, grouped affine-hull GE, and grouped exact-ANF F2 span.
Pure Python 3 + networkx + python-sat (only for an independent UNSAT check).
Deterministic seeds.  Output: JSON on stdout + human summary on stderr."""
import itertools, json, random, sys, time
import networkx as nx

# ---------------- F2 multilinear polynomials: set of monomials (int bitmasks over global vars)
def padd(a, b):
    return a ^ b  # sets of monomials as python sets -> use symmetric difference
def clause_anf(clause):
    """falsity indicator of clause (DIMACS ints, var ids 1..)."""
    neg = 0; pos = []
    for l in clause:
        if l > 0: pos.append(1 << l)
        else: neg |= 1 << (-l)
    out = set()
    for r in range(len(pos) + 1):
        for sub in itertools.combinations(pos, r):
            m = neg
            for x in sub: m |= x
            out ^= {m}
    return out
def anf_from_truth(local, f):
    """local: list of var ids; f: function word(tuple)->0/1. Moebius transform."""
    k = len(local); T = [f(tuple((w >> i) & 1 for i in range(k))) for w in range(1 << k)]
    for i in range(k):
        for w in range(1 << k):
            if w >> i & 1: T[w] ^= T[w ^ (1 << i)]
    out = set()
    for w in range(1 << k):
        if T[w]:
            m = 0
            for i in range(k):
                if w >> i & 1: m |= 1 << local[i]
            out.add(m)
    return out
def f2_rank(vecs):
    basis = {}  # pivot -> vec
    r = 0
    for v in vecs:
        while v:
            p = v.bit_length() - 1
            if p in basis: v ^= basis[p]
            else: basis[p] = v; r += 1; break
    return r, basis
def in_span(basis, v):
    while v:
        p = v.bit_length() - 1
        if p not in basis: return False
        v ^= basis[p]
    return True

# ---------------- gadgets
GADGETS = {
    'ID1':  (1, lambda u: u[0]),
    'AND2': (2, lambda u: u[0] & u[1]),
    'MAJ3': (3, lambda u: 1 if u[0] + u[1] + u[2] >= 2 else 0),
    'IND3': (3, lambda u: u[1 + u[0]] if True else 0),  # 1-bit index into 2 data bits
}

def tseitin_gadget(G, charge, gname, encoding='canonical'):
    b, g = GADGETS[gname]
    edges = sorted(tuple(sorted(e)) for e in G.edges())
    var = {}; nv = 0
    for e in edges:
        var[e] = list(range(nv + 1, nv + b + 1)); nv += b
    groups = {}  # vertex -> list of clauses
    for v in sorted(G.nodes()):
        inc = [e for e in edges if v in e]
        local = [x for e in inc for x in var[e]]
        k = len(local)
        def viol(word, inc=inc, v=v):
            s = charge[v]
            for j, e in enumerate(inc): s ^= g(word[j * b:(j + 1) * b])
            return s  # 1 iff constraint violated
        bad = [w for w in itertools.product((0, 1), repeat=k) if viol(w)]
        badset = set(bad)
        def cl(w, skip=None):
            return [(-local[i] if w[i] else local[i]) for i in range(k) if i != skip]
        if encoding == 'canonical':
            cls = [cl(w) for w in bad]
        elif encoding == 'merged':
            cls = set()
            for w in bad:
                merged = False
                for i in range(k):
                    w2 = list(w); w2[i] ^= 1
                    if tuple(w2) in badset:
                        cls.add(tuple(sorted(cl(w, skip=i), key=abs))); merged = True
                if not merged: cls.add(tuple(sorted(cl(w), key=abs)))
            cls = [list(c) for c in sorted(cls)]
        groups[v] = (local, cls, viol)
    return nv, edges, var, groups

# ---------------- unit propagation / width-2 RUP
def up(clauses, assign):
    """assign: dict var->bool. returns (conflict, assign). naive repeated scan."""
    a = dict(assign); changed = True
    while changed:
        changed = False
        for c in clauses:
            unassigned = []; sat = False
            for l in c:
                v = abs(l)
                if v in a:
                    if a[v] == (l > 0): sat = True; break
                else: unassigned.append(l)
            if sat: continue
            if not unassigned: return True, a
            if len(unassigned) == 1:
                l = unassigned[0]; a[abs(l)] = l > 0; changed = True
    return False, a
def width2_rup_admissions(clauses, nv):
    """count width<=2 clauses that are RUP w.r.t. the ORIGINAL clause set (root fixed point test)."""
    conf, _ = up(clauses, {})
    if conf: return 'root-conflict'
    adm = 0
    lits = [l for v in range(1, nv + 1) for l in (v, -v)]
    for l in lits:
        if up(clauses, {abs(l): not (l > 0)})[0]: adm += 1
    for l1, l2 in itertools.combinations(lits, 2):
        if abs(l1) == abs(l2): continue
        if up(clauses, {abs(l1): not (l1 > 0), abs(l2): not (l2 > 0)})[0]: adm += 1
    return adm

def affine_hull_dim(local, cls):
    k = len(local); idx = {x: i for i, x in enumerate(local)}
    sat = []
    for w in range(1 << k):
        ok = True
        for c in cls:
            if all(((w >> idx[abs(l)]) & 1) != (l > 0) for l in c): ok = False; break
        if ok: sat.append(w)
    if not sat: return -1, 0
    r, _ = f2_rank([s ^ sat[0] for s in sat[1:]])
    return r, len(sat)

def sat_check(clauses, tlimit=60):
    try:
        from pysat.solvers import Cadical153 as S
    except Exception:
        from pysat.solvers import Glucose4 as S
    s = S(bootstrap_with=clauses)
    t = time.time(); r = s.solve(); dt = time.time() - t
    st = s.accum_stats(); s.delete()
    return {'sat': r, 'seconds': round(dt, 3), 'conflicts': st.get('conflicts')}

def analyse(name, G, gname, encoding, do_rup, seed=0):
    rnd = random.Random(seed)
    charge = {v: 0 for v in G.nodes()}; charge[min(G.nodes())] = 1
    nv, edges, var, groups = tseitin_gadget(G, charge, gname, encoding)
    allcl = [c for v in groups for c in groups[v][1]]
    res = {'name': name, 'gadget': gname, 'encoding': encoding, 'V': G.number_of_nodes(),
           'E': G.number_of_edges(), 'vars': nv, 'clauses': len(allcl),
           'max_width': max(len(c) for c in allcl), 'min_width': min(len(c) for c in allcl)}
    # (1) general Theorem-1 certificate: sum_v [1+prod_C(1+p_C)] computed from the CLAUSES' truth table
    tot = set()
    for v, (local, cls, _) in groups.items():
        idx = {x: i for i, x in enumerate(local)}
        def falsified(word, cls=cls, idx=idx):
            for c in cls:
                if all(word[idx[abs(l)]] != (1 if l > 0 else 0) for l in c): return 1
            return 0
        tot ^= anf_from_truth(local, falsified)
    res['thm1_sum_is_const_1'] = (tot == {0})
    # (2) constant-coefficient certificate sum_C p_C
    s = set()
    for c in allcl: s ^= clause_anf(c)
    res['sum_all_clause_indicators_is_1'] = (s == {0})
    res['sum_all_clause_indicators_num_monomials'] = len(s)
    # (3) grouped affine hull per vertex group
    dims = [affine_hull_dim(groups[v][0], groups[v][1]) for v in groups]
    res['affine_hull_full_in_all_groups'] = all(d == len(groups[v][0]) for d, v in zip([x[0] for x in dims], groups))
    res['affine_equations_extracted'] = sum(len(groups[v][0]) - d for (d, _), v in zip(dims, groups))
    # (4) random-assignment sanity: number of violated vertex constraints is odd
    odd_ok = True
    for _ in range(2000):
        a = [rnd.randint(0, 1) for _ in range(nv + 1)]
        cnt = 0
        for v, (local, cls, viol) in groups.items():
            cnt += viol(tuple(a[x] for x in local))
        if cnt % 2 == 0: odd_ok = False; break
    res['random_2000_assignments_violate_odd_count'] = odd_ok
    # (5) width-2 RUP saturation (root fixed point)
    if do_rup:
        t = time.time(); res['width2_rup_admissions'] = width2_rup_admissions(allcl, nv)
        res['width2_rup_seconds'] = round(time.time() - t, 2)
    # (6) independent UNSAT check
    res['solver'] = sat_check(allcl)
    return res, allcl

def random3cnf_control(n=40, m=184, seed0=20261128):
    seed = seed0
    while True:
        rnd = random.Random(seed)
        cls = []
        for _ in range(m):
            vs = rnd.sample(range(1, n + 1), 3)
            cls.append([v if rnd.random() < 0.5 else -v for v in vs])
        if sat_check(cls)['sat'] is False: break
        seed += 1
    # equal-scope grouping + group ANF
    grp = {}
    for c in cls: grp.setdefault(tuple(sorted(abs(l) for l in c)), []).append(c)
    allmons = {}
    def vec(poly):
        v = 0
        for mo in poly:
            if mo not in allmons: allmons[mo] = len(allmons)
            v |= 1 << allmons[mo]
        return v
    gvecs = []
    for sc, cl in grp.items():
        p = set()
        for c in cl: p ^= clause_anf(c)   # distinct clauses on a scope have disjoint falsity words
        gvecs.append(vec(p))
    cvecs = [vec(clause_anf(c)) for c in cls]
    one = vec({0})
    rg, bg = f2_rank(gvecs); rc, bc = f2_rank(cvecs)
    # affine hull extraction per group
    aff = 0
    for sc, cl in grp.items():
        d, _ = affine_hull_dim(list(sc), cl); aff += 3 - d
    return {'n': n, 'm': m, 'seed': seed, 'distinct_scopes': len(grp),
            'max_clauses_per_scope': max(len(v) for v in grp.values()),
            'group_anf_rank': rg, 'clause_anf_rank': rc,
            'const1_in_group_span': in_span(bg, one), 'const1_in_clause_span': in_span(bc, one),
            'affine_equations_extracted': aff, 'width2_rup_admissions': width2_rup_admissions(cls, n),
            'solver': sat_check(cls)}

def coupled_prism_rank(n=4):
    """T3-09 spot check: two prisms C_n x K2 sharing one edge variable, canonical parity CNF."""
    P = nx.circular_ladder_graph(n)
    E = sorted(tuple(sorted(e)) for e in P.edges())
    var = {}; nv = 0
    for blk in (0, 1):
        for e in E:
            if blk == 1 and e == E[0]: var[(1, e)] = var[(0, e)]; continue
            nv += 1; var[(blk, e)] = nv
    cls = []
    for blk in (0, 1):
        for v in P.nodes():
            inc = [var[(blk, e)] for e in E if v in e]
            c = 1 if v == 0 else 0
            for w in itertools.product((0, 1), repeat=3):
                if (sum(w) % 2) != c: cls.append([(-x if w[i] else x) for i, x in enumerate(inc)])
    mons = {}
    vecs = []
    for c in cls:
        v = 0
        for mo in clause_anf(c):
            if mo not in mons: mons[mo] = len(mons)
            v |= 1 << mons[mo]
        vecs.append(v)
    r, b = f2_rank(vecs)
    one = 1 << mons[0] if 0 in mons else None
    return {'n': n, 'vars': nv, 'clauses': len(cls), 'rank_P': r, 'expected_m_minus_1': len(cls) - 1,
            'const1_in_span': (one is not None and in_span(b, one)),
            'width2_rup_admissions': width2_rup_admissions(cls, nv)}

def mobius_parity_rup(k=8):
    """T2 spot check: Mobius ladder (cycle C_k + opposite chords), parity CNF, odd charge."""
    G = nx.cycle_graph(k)
    for i in range(k // 2): G.add_edge(i, i + k // 2)
    charge = {v: 0 for v in G}; charge[0] = 1
    nv, edges, var, groups = tseitin_gadget(G, charge, 'ID1', 'canonical')
    allcl = [c for v in groups for c in groups[v][1]]
    return {'k': k, 'vars': nv, 'clauses': len(allcl), 'width2_rup_admissions': width2_rup_admissions(allcl, nv)}

if __name__ == '__main__' and len(sys.argv) == 1:
    out = {'tseitin_gadget': [], 'controls': {}}
    cases = [
        ('prism4', nx.circular_ladder_graph(4), 'AND2', 'canonical', True),
        ('prism4', nx.circular_ladder_graph(4), 'AND2', 'merged', True),
        ('prism8', nx.circular_ladder_graph(8), 'AND2', 'canonical', False),
        ('prism16', nx.circular_ladder_graph(16), 'AND2', 'canonical', False),
        ('rcubic10', nx.random_regular_graph(3, 10, seed=1), 'AND2', 'canonical', True),
        ('rcubic20', nx.random_regular_graph(3, 20, seed=2), 'AND2', 'canonical', False),
        ('rcubic20', nx.random_regular_graph(3, 20, seed=2), 'AND2', 'merged', False),
        ('rcubic30', nx.random_regular_graph(3, 30, seed=3), 'AND2', 'canonical', False),
        ('rcubic10', nx.random_regular_graph(3, 10, seed=1), 'MAJ3', 'canonical', False),
        ('rcubic10', nx.random_regular_graph(3, 10, seed=1), 'IND3', 'canonical', False),
        ('rcubic10', nx.random_regular_graph(3, 10, seed=1), 'ID1', 'canonical', True),
    ]
    for name, G, gn, enc, rup in cases:
        r, _ = analyse(name, G, gn, enc, rup)
        out['tseitin_gadget'].append(r); print(json.dumps(r), file=sys.stderr)
    out['controls']['random3cnf'] = random3cnf_control(); print(out['controls']['random3cnf'], file=sys.stderr)
    out['controls']['T3_09_coupled_prism_n4'] = coupled_prism_rank(4); print(out['controls']['T3_09_coupled_prism_n4'], file=sys.stderr)
    out['controls']['T2_mobius8_parity'] = mobius_parity_rup(8); print(out['controls']['T2_mobius8_parity'], file=sys.stderr)
    print(json.dumps(out, indent=1))

def merged_const_span(G, gname='AND2'):
    """Is 1 in the constant-coefficient F2 span of individual clause indicators (no products)?"""
    charge = {v: 0 for v in G.nodes()}; charge[min(G.nodes())] = 1
    nv, edges, var, groups = tseitin_gadget(G, charge, gname, 'merged')
    allcl = [c for v in groups for c in groups[v][1]]
    mons = {}
    def vec(p):
        v = 0
        for mo in p:
            if mo not in mons: mons[mo] = len(mons)
            v |= 1 << mons[mo]
        return v
    vecs = [vec(clause_anf(c)) for c in allcl]
    one = vec({0})
    r, b = f2_rank(vecs)
    return {'V': G.number_of_nodes(), 'clauses': len(allcl), 'rank': r, 'const1_in_constcoef_span': in_span(b, one)}

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'merged':
    res = [merged_const_span(nx.circular_ladder_graph(4)), merged_const_span(nx.random_regular_graph(3, 10, seed=1)),
           merged_const_span(nx.random_regular_graph(3, 20, seed=2))]
    print(json.dumps(res, indent=1))
