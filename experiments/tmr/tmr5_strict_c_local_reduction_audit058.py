#!/usr/bin/env python3
"""TMR-5/058 independent audit of the proof lead's LOCAL3COL-C1 reduction.

Fixed-width indexed 3-CNF F  ->  H3 (3-COLOR)  ->  H5 (5-COLOR)  ->  strict-C K(F).

Written independently from the lead's report text only (the lead's script is not in
the repository).  Checks:
  A. exhaustive local gadget tables (C 30/125, head projection, NAE triangle, OR split);
  B. a fixed-width bit encoding with an authenticating parser and malformed-input tests;
  C. a LOCAL clause oracle K_clause(i) that reads only header + at most one source clause
     (bit reads counted), compared with an independent materialized builder;
  D. exact counts V_C = 15+9v+39m and M_C = 10+7v+31m;
  E. SAT sources: Boolean witness -> full strict-C coloring checked on every C clause;
  F. UNSAT sources refuted DIRECTLY at the strict-C level by a generic GAC/backtracking CSP
     solver that knows only the 30-tuple table (no projection argument, no graph view);
  G. the unused-variable size counterexample (|K(F)| not bounded by |F|^{1+o(1)}).
Deterministic seed 20261119.  Standard Python only.
"""
import itertools, json, random, sys, time, hashlib

SEED = 20261119
MAGIC = [1, 0, 1, 1, 0, 0, 1, 1]  # 8-bit tag

# ---------------- A. local gadget tables ----------------
def R(a, b):
    return (b - a) % 5 in (1, 3)

def C(x, y, z):
    return (R(x, y) and R(y, z) and R(z, x)) or (R(x, z) and R(z, y) and R(y, x))

C_TABLE = [t for t in itertools.product(range(5), repeat=3) if C(*t)]

def gadget_tables():
    out = {}
    out["C_accepting"] = len(C_TABLE)
    head_ok = all((any(C(h, u, w) for h in range(5))) == (u != w)
                  for u in range(5) for w in range(5))
    out["head_projection_25_pairs_ok"] = head_ok
    # symmetry group of C on Z5 among affine maps x -> a x + k
    sym = [(a, k) for a in range(1, 5) for k in range(5)
           if all(C(*t) == C(*[(a * x + k) % 5 for x in t])
                  for t in itertools.product(range(5), repeat=3))]
    out["affine_symmetries"] = len(sym)
    # NAE triangle: terminals colored in {T,F} = {0,1} (B=2); triangle t_i != terminal_i
    nae_ok = True
    for a in itertools.product((0, 1), repeat=3):
        col = any(len({t0, t1, t2}) == 3 and t0 != a[0] and t1 != a[1] and t2 != a[2]
                  for t0, t1, t2 in itertools.product(range(3), repeat=3))
        nae_ok &= (col == (len(set(a)) > 1))
    out["nae_triangle_8_rows_ok"] = nae_ok
    # OR split: (a|b|c) <-> exists s NAE(a,b,s) & NAE(not s, c, False)
    nae = lambda *t: len(set(t)) > 1
    or_ok = all((a or b or c) == any(nae(a, b, s) and nae(not s, c, False) for s in (False, True))
                for a, b, c in itertools.product((False, True), repeat=3))
    out["or_split_8_rows_ok"] = or_ok
    return out

# ---------------- B. fixed-width encoding and parser ----------------
def width_for(v):
    return max(1, v.bit_length())

def encode(v, clauses, w=None):
    """header: MAGIC | 6-bit w | w-bit v | w-bit m | 3m literals of (1 sign bit + w index bits)."""
    w = w or width_for(max(v, len(clauses)))
    bits = list(MAGIC) + [(w >> (5 - j)) & 1 for j in range(6)]
    num = lambda x: [(x >> (w - 1 - j)) & 1 for j in range(w)]
    bits += num(v) + num(len(clauses))
    for cl in clauses:
        for lit in cl:
            bits += [1 if lit < 0 else 0] + num(abs(lit))
    return bits

class Src:
    """Read-only random-access source; counts bit reads."""
    def __init__(self, bits):
        self.b = bits; self.reads = 0
    def get(self, i):
        self.reads += 1
        return self.b[i]
    def num(self, off, w):
        x = 0
        for j in range(w):
            x = 2 * x + self.get(off + j)
        return x

def parse_header(src):
    n = len(src.b)
    if n < 14 or [src.get(i) for i in range(8)] != MAGIC:
        raise ValueError("bad magic/short")
    w = src.num(8, 6)
    if w < 1 or n < 14 + 2 * w:
        raise ValueError("bad width")
    v = src.num(14, w); m = src.num(14 + w, w)
    if v < 1 or m < 1:
        raise ValueError("v,m must be >=1")
    if n != 14 + 2 * w + 3 * m * (w + 1):
        raise ValueError("length mismatch")
    return w, v, m

def literal(src, hdr, j):
    w, v, m = hdr
    off = 14 + 2 * w + j * (w + 1)
    s = src.get(off); idx = src.num(off + 1, w)
    if not (1 <= idx <= v):
        raise ValueError("literal index out of range")
    return -idx if s else idx

def authenticate(bits):
    """Full authentication: header + every literal in range.  O(log) registers."""
    src = Src(bits)
    hdr = parse_header(src)
    for j in range(3 * hdr[2]):
        literal(src, hdr, j)
    return hdr, src.reads

# ---------------- C. vertex naming and the LOCAL clause oracle ----------------
# H3 vertex ids: 0=T 1=F 2=B ; var x (1..v): 3+2(x-1) is x, +1 is not-x ;
# clause k (0..m-1): base 3+2v+8k: s, not-s, p0,p1,p2 (NAE(a,b,s)), q0,q1,q2 (NAE(not s,c,F))
# H5 adds U = V3, V = V3+1.  C variables: H5 vertices 0..V5-1, then head of edge e is V5+e.
def lit_vertex(v, lit):
    x = abs(lit)
    return 3 + 2 * (x - 1) + (1 if lit < 0 else 0)

def edge_local(src, hdr, e):
    """e-th edge of H5 computed from header and at most ONE source clause."""
    w, v, m = hdr
    V3 = 3 + 2 * v + 8 * m
    if e < 3:
        return [(0, 1), (1, 2), (0, 2)][e]
    e -= 3
    if e < 3 * v:
        x, r = divmod(e, 3); a = 3 + 2 * x
        return [(a, a + 1), (a, 2), (a + 1, 2)][r]
    e -= 3 * v
    if e < 15 * m:
        k, r = divmod(e, 15)
        b = 3 + 2 * v + 8 * k
        s, ns, p, q = b, b + 1, b + 2, b + 5
        fixed = [(s, ns), (s, 2), (ns, 2), (p, p + 1), (p + 1, p + 2), (p, p + 2),
                 (q, q + 1), (q + 1, q + 2), (q, q + 2)]
        if r < 9:
            return fixed[r]
        r -= 9
        # terminals: p0-a p1-b p2-s q0-ns q1-c q2-F
        if r == 2: return (p + 2, s)
        if r == 3: return (q, ns)
        if r == 5: return (q + 2, 1)
        j = {0: 0, 1: 1, 4: 2}[r]
        return ((p + r) if r < 2 else (q + 1), lit_vertex(v, literal(src, hdr, 3 * k + j)))
    e -= 15 * m
    if e == 0:
        return (V3, V3 + 1)
    e -= 1
    if e < 2 * V3:
        apex, u = divmod(e, V3)
        return (V3 + apex, u)
    raise IndexError("edge index out of range")

def c_clause_local(src, hdr, i):
    w, v, m = hdr
    V5 = 5 + 2 * v + 8 * m
    u, x = edge_local(src, hdr, i)
    return (V5 + i, u, x)

def counts(v, m):
    return 15 + 9 * v + 39 * m, 10 + 7 * v + 31 * m

# ---------------- independent materialized builder (graph-first, by name) ----------------
def build_named(v, clauses):
    E = set()
    add = lambda a, b: E.add(frozenset((a, b)))
    add("T", "F"); add("F", "B"); add("T", "B")
    L = lambda l: ("x", abs(l), l < 0)
    for x in range(1, v + 1):
        add(("x", x, False), ("x", x, True)); add(("x", x, False), "B"); add(("x", x, True), "B")
    for k, (a, b, c) in enumerate(clauses):
        s, ns = ("s", k, 0), ("s", k, 1)
        add(s, ns); add(s, "B"); add(ns, "B")
        for g, terms in (("p", (L(a), L(b), s)), ("q", (ns, L(c), "F"))):
            t = [(g, k, j) for j in range(3)]
            add(t[0], t[1]); add(t[1], t[2]); add(t[0], t[2])
            for j in range(3):
                add(t[j], terms[j])
    V3names = ["T", "F", "B"] + [("x", x, n) for x in range(1, v + 1) for n in (False, True)] + \
              [nm for k in range(len(clauses)) for nm in
               [("s", k, 0), ("s", k, 1)] + [(g, k, j) for g in "pq" for j in range(3)]]
    for u in V3names:
        add("U", u); add("V", u)
    add("U", "V")
    return V3names + ["U", "V"], E

def name_of(v, m, idx):
    V3 = 3 + 2 * v + 8 * m
    if idx < 3: return ["T", "F", "B"][idx]
    if idx < 3 + 2 * v:
        x, n = divmod(idx - 3, 2); return ("x", x + 1, bool(n))
    if idx < V3:
        k, r = divmod(idx - 3 - 2 * v, 8)
        return ("s", k, r) if r < 2 else (("p", k, r - 2) if r < 5 else ("q", k, r - 5))
    return ["U", "V"][idx - V3]

# ---------------- E. witness extension ----------------
def extend_witness(v, clauses, assign):
    """Boolean assignment -> H3 3-coloring (T=0,F=1,B=2) -> 5-coloring -> C assignment."""
    col = {"T": 0, "F": 1, "B": 2, "U": 3, "V": 4}
    val = lambda l: assign[abs(l)] ^ (l < 0)
    for x in range(1, v + 1):
        col[("x", x, False)] = 0 if assign[x] else 1
        col[("x", x, True)] = 1 if assign[x] else 0
    for k, (a, b, c) in enumerate(clauses):
        A, Bv, Cv = val(a), val(b), val(c)
        for sv in (False, True):
            if len({A, Bv, sv}) > 1 and len({not sv, Cv, False}) > 1:
                s = sv; break
        else:
            return None
        col[("s", k, 0)] = 0 if s else 1; col[("s", k, 1)] = 1 if s else 0
        for g, terms in (("p", (col[lit_name(a)], col[lit_name(b)], col[("s", k, 0)])),
                         ("q", (col[("s", k, 1)], col[lit_name(c)], 1))):
            for perm in itertools.permutations(range(3)):
                if all(perm[j] != terms[j] for j in range(3)):
                    for j in range(3): col[(g, k, j)] = perm[j]
                    break
            else:
                return None
    return col

def lit_name(l):
    return ("x", abs(l), l < 0)

def c_assignment(v, m, col, hdr, src):
    V5 = 5 + 2 * v + 8 * m
    Vc, Mc = counts(v, m)
    a = [None] * Vc
    for idx in range(V5):
        a[idx] = col[name_of(v, m, idx)]
    for i in range(Mc):
        h, u, x = c_clause_local(src, hdr, i)
        a[h] = next(hh for hh in range(5) if C(hh, a[u], a[x]))
    return a

# ---------------- F. generic strict-C CSP solver (table only) ----------------
def csp_solve(nvars, cons, budget):
    """GAC (support over the 30 accepting tuples) + dom/deg branching; one translation fix."""
    occ = [[] for _ in range(nvars)]
    for ci, c in enumerate(cons):
        for p in c: occ[p].append(ci)
    nodes = [0]
    def revise(doms, queue):
        while queue:
            ci = queue.pop()
            x, y, z = cons[ci]
            sup = [set(), set(), set()]
            for t in C_TABLE:
                if t[0] in doms[x] and t[1] in doms[y] and t[2] in doms[z]:
                    sup[0].add(t[0]); sup[1].add(t[1]); sup[2].add(t[2])
            for p, s in zip((x, y, z), sup):
                if s != doms[p]:
                    if not s: return False
                    doms[p] = s
                    queue.extend(occ[p])
        return True
    def rec(doms):
        nodes[0] += 1
        if nodes[0] > budget: raise TimeoutError
        free = [i for i in range(nvars) if len(doms[i]) > 1]
        if not free: return doms
        p = min(free, key=lambda i: (len(doms[i]), -len(occ[i])))
        for val in sorted(doms[p]):
            d2 = [set(d) for d in doms]; d2[p] = {val}
            if revise(d2, list(occ[p])):
                r = rec(d2)
                if r: return r
        return None
    doms = [set(range(5)) for _ in range(nvars)]
    # translation symmetry x -> x+k preserves C: fixing one variable is sound
    doms[cons[0][1]] = {0}
    if not revise(doms, list(range(len(cons)))):
        return None, nodes[0]
    return rec(doms), nodes[0]

def brute_sat(v, clauses):
    for bits in itertools.product((False, True), repeat=v):
        a = {x + 1: bits[x] for x in range(v)}
        if all(any(a[abs(l)] ^ (l < 0) for l in cl) for cl in clauses):
            return a
    return None

# ---------------- main ----------------
def main():
    t0 = time.time()
    rng = random.Random(SEED)
    out = {"revision": "TMR5_STRICT_C_LOCAL_REDUCTION_AUDIT058_v1", "seed": SEED,
           "python": sys.version.split()[0]}
    out["A_gadgets"] = gadget_tables()

    # B/C/D/E random sources
    stats = dict(instances=0, sat=0, unsat=0, edges_compared=0, c_clauses_checked=0,
                 max_reads_per_clause=0, max_header_reads=0, count_formula_ok=True,
                 local_eq_materialized=True, witness_ok=True)
    unsat_sources = []
    for it in range(300):
        v = rng.randint(1, 5); m = rng.randint(1, 8)
        clauses = [tuple(rng.choice((1, -1)) * rng.randint(1, v) for _ in range(3)) for _ in range(m)]
        bits = encode(v, clauses)
        hdr, _ = authenticate(bits)
        Vc, Mc = counts(v, m)
        names, Eset = build_named(v, clauses)
        stats["count_formula_ok"] &= (len(names) + len(Eset) == Vc and len(Eset) == Mc)
        # local oracle, fresh source per clause to count reads in isolation
        local_edges = set()
        for i in range(Mc):
            s = Src(bits); h = parse_header(s); hr = s.reads
            hh, u, x = c_clause_local(s, h, i)
            stats["max_header_reads"] = max(stats["max_header_reads"], hr)
            stats["max_reads_per_clause"] = max(stats["max_reads_per_clause"], s.reads - hr)
            assert u != x and hh == 5 + 2 * v + 8 * m + i
            local_edges.add(frozenset((name_of(v, m, u), name_of(v, m, x))))
        stats["local_eq_materialized"] &= (local_edges == Eset and len(local_edges) == Mc)
        stats["edges_compared"] += Mc
        stats["instances"] += 1
        a = brute_sat(v, clauses)
        if a:
            stats["sat"] += 1
            col = extend_witness(v, clauses, a)
            ok = col is not None and all(col[p] != col[q] for p, q in map(tuple, Eset))
            src = Src(bits)
            ca = c_assignment(v, m, col, hdr, src)
            for i in range(Mc):
                hh, u, x = c_clause_local(src, hdr, i)
                ok &= C(ca[hh], ca[u], ca[x]); stats["c_clauses_checked"] += 1
            # projection back: Boolean value of x is color(x)==color(T)
            proj = {x: ca[3 + 2 * (x - 1)] == ca[0] for x in range(1, v + 1)}
            ok &= all(any(proj[abs(l)] ^ (l < 0) for l in cl) for cl in clauses)
            stats["witness_ok"] &= ok
        else:
            stats["unsat"] += 1
            unsat_sources.append((v, clauses))
    out["BCDE_random"] = stats

    # B. malformed inputs
    good = encode(2, [(1, -2, 2)])
    mal = {
        "bad_magic": [0] + good[1:],
        "truncated": good[:-1],
        "trailing_bit": good + [0],
        "index_zero": encode(2, [(1, 0, 2)]),
        "index_gt_v": encode(2, [(3, 1, 1)], w=2),
        "m_zero": encode(1, []),
        "v_zero": encode(0, [(1, 1, 1)], w=1),
        "v_exceeds_width_field_mislabeled_length": encode(3, [(1, 2, 3)], w=2)[:-1],
        "width_zero": list(MAGIC) + [0] * 6,
    }
    rej = {}
    for k, b in mal.items():
        try:
            authenticate(b); rej[k] = "ACCEPTED"
        except ValueError as ex:
            rej[k] = "rejected: " + str(ex)
    out["B_malformed"] = rej

    # F. UNSAT controls refuted directly at strict-C level
    controls = {
        "two_var_repeated_literal_4clauses": (2, [(1, 1, 2), (1, 1, -2), (-1, -1, 2), (-1, -1, -2)]),
        "three_var_all8": (3, [tuple(s * (j + 1) for s, j in zip(sg, range(3)))
                               for sg in itertools.product((1, -1), repeat=3)]),
        "one_var_x_and_notx": (1, [(1, 1, 1), (-1, -1, -1)]),
    }
    small_random_unsat = sorted(unsat_sources, key=lambda t: counts(t[0], len(t[1]))[0])[:2]
    for j, (v, cl) in enumerate(small_random_unsat):
        controls[f"random_unsat_{j}"] = (v, cl)
    sat_controls = {"sat_three_var_7of8": (3, controls["three_var_all8"][1][:7])}
    fres = {}
    for name, (v, cl) in list(controls.items()) + list(sat_controls.items()):
        assert (brute_sat(v, cl) is None) == (name not in sat_controls)
        bits = encode(v, cl); src = Src(bits); hdr = parse_header(src)
        Vc, Mc = counts(v, len(cl))
        cons = [c_clause_local(src, hdr, i) for i in range(Mc)]
        ts = time.time()
        try:
            sol, nodes = csp_solve(Vc, cons, budget=40000)
            verdict = "SAT" if sol else "UNSAT"
            if sol:
                a = [next(iter(d)) for d in sol]
                assert all(C(a[x], a[y], a[z]) for x, y, z in cons)
                verdict += "(verified)"
        except TimeoutError:
            verdict, nodes = "UNKNOWN(budget)", 40000
        fres[name] = dict(v=v, m=len(cl), V_C=Vc, M_C=Mc, csp_verdict=verdict,
                          search_nodes=nodes, seconds=round(time.time() - ts, 3),
                          boolean_truth="SAT" if name in sat_controls else "UNSAT")
    out["F_direct_C_level"] = fres

    # G. unused-variable size counterexample
    g = []
    for k in (8, 16, 24, 32):
        v = 2 ** k - 1; cl = [(1, 2, 3)]
        n_src = len(encode(v, cl))
        Vc, Mc = counts(v, 1)
        g.append(dict(k=k, v=v, m=1, source_bits=n_src, V_C=Vc, M_C=Mc,
                      C_bits_lower_bound=Mc * 3 * k))
    out["G_unused_variable_blowup"] = g
    out["seconds_total"] = round(time.time() - t0, 2)
    return out

if __name__ == "__main__":
    res = main()
    blob = json.dumps(res, indent=1, sort_keys=True, default=str)
    print(blob)
    print("SHA256_OF_JSON", hashlib.sha256(blob.encode()).hexdigest(), file=sys.stderr)
