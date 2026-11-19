#!/usr/bin/env python3
"""Strict-C local transfer audit (generic hourly routine, 2026-11-19).

Pipeline audited: clause-addressable width-W CNF  -> fixed-width 3-CNF (FW3)
-> strict-C CSP instance K(F) with random-access clause generation.

Strict-C: R(a,b) iff (b-a) mod 5 in {1,3};
C(x,y,z) = R(x,y)R(y,z)R(z,x) or R(x,z)R(z,y)R(y,x).

Every generated object is produced by an index -> record function that reads
O(1) source records; a separately written materialising builder is compared
record-for-record.  SAT/UNSAT of every C instance is decided by an
independent GAC backtracking CSP solver over the 5 colours (never via the
Boolean source), and compared with brute force on the source CNF.
Standard library only.  Deterministic seed below.
"""
import itertools, json, random, sys, time, hashlib

SEED = 2026111917
N_RANDOM = int(sys.argv[1]) if len(sys.argv) > 1 else 60
def R(a, b): return (b - a) % 5 in (1, 3)
def C(x, y, z): return (R(x, y) and R(y, z) and R(z, x)) or (R(x, z) and R(z, y) and R(y, x))
C_TABLE = frozenset(t for t in itertools.product(range(5), repeat=3) if C(*t))

# ---------------- wide CNF -> FW3 (random access) ----------------
# A wide source is (v, m, W, clause_oracle) where clause_oracle(j) returns a
# list of exactly W nonzero DIMACS literals over 1..v (shorter clauses are
# padded by repeating their last literal, which preserves the clause).
def fw3_header(v, m, W):
    if W < 3: raise ValueError("W>=3 required")
    return v + m * (W - 3), m * (W - 2)

def fw3_clause(t, v, m, W, oracle):
    """t-th clause of FW3(F). One oracle call. Chain y_{j,0..W-4}."""
    j, k = divmod(t, W - 2)
    if not (0 <= j < m): raise IndexError(t)
    lits = oracle(j)
    if W == 3: return tuple(lits)
    y = lambda q: v + j * (W - 3) + q + 1          # fresh var ids
    if k == 0: return (lits[0], lits[1], y(0))
    if k == W - 3: return (-y(W - 4), lits[W - 2], lits[W - 1])
    return (-y(k - 1), lits[k + 1], y(k))

# ---------------- FW3 -> strict-C K(F) (random access) ----------------
def layout(v, m):
    V3 = 3 + 2 * v + 8 * m; E3 = 3 + 3 * v + 15 * m
    V5 = V3 + 2; E5 = E3 + 1 + 2 * V3
    return V3, E3, V5, E5, V5 + E5        # last = number of C variables

def lit_vertex(l):                          # DIMACS literal -> H3 vertex
    x = abs(l) - 1
    return 3 + 2 * x + (0 if l > 0 else 1)

def h3_edge(e, v, m, clause3):
    """e-th edge of H3; reads at most one source 3-clause."""
    T, F, B = 0, 1, 2
    if e < 3: return [(T, F), (F, B), (B, T)][e]
    e -= 3
    if e < 3 * v:
        x, r = divmod(e, 3); p, n = 3 + 2 * x, 4 + 2 * x
        return [(p, n), (p, B), (n, B)][r]
    e -= 3 * v
    j, r = divmod(e, 15)
    if j >= m: raise IndexError
    base = 3 + 2 * v + 8 * j
    s, ns, t0, t1, t2, u0, u1, u2 = range(base, base + 8)
    if r < 3: return [(s, ns), (s, B), (ns, B)][r]
    if r < 6: return [(t0, t1), (t1, t2), (t2, t0)][r - 3]
    if r < 9: return [(u0, u1), (u1, u2), (u2, u0)][r - 6]
    a, b, c = clause3(j)                    # the single source read
    if r == 9: return (t0, lit_vertex(a))
    if r == 10: return (t1, lit_vertex(b))
    if r == 11: return (t2, s)
    if r == 12: return (u0, ns)
    if r == 13: return (u1, lit_vertex(c))
    return (u2, F)

def c_clause(i, v, m, clause3):
    """i-th strict-C clause of K(F) as (head, u, w)."""
    V3, E3, V5, E5, NC = layout(v, m)
    if not (0 <= i < E5): raise IndexError(i)
    U, W_ = V3, V3 + 1
    if i < E3: u, w = h3_edge(i, v, m, clause3)
    elif i == E3: u, w = U, W_
    else:
        o, r = divmod(i - E3 - 1, 2); u, w = (U if r == 0 else W_), o
    return (V5 + i, u, w)

# ---------------- fixed-width bit encodings ----------------
def bw(x): return max(1, x.bit_length())

def fw3_bit(p, v3, m3, clause_fn):
    """bit p of encoded FW3: header v3,m3 in 32-bit fields (scope n<2^32);
    each clause = 3 fields of width w=bw(2*v3+1) holding 2|l|-[l<0]... we use
    (2*(|l|-1) + (l<0))."""
    w = bw(2 * v3); hdr = 64
    if p < hdr: return ((v3 if p < 32 else m3) >> (p % 32)) & 1
    q, b = divmod(p - hdr, w); j, f = divmod(q, 3)
    l = clause_fn(j)[f]
    code = 2 * (abs(l) - 1) + (1 if l < 0 else 0)
    return (code >> b) & 1

def c_bit(p, NC, MC, cclause):
    w = bw(NC - 1); hdr = 64
    if p < hdr: return ((NC if p < 32 else MC) >> (p % 32)) & 1
    q, b = divmod(p - hdr, w); i, f = divmod(q, 3)
    return (cclause(i)[f] >> b) & 1

# ---------------- independent materialising builder ----------------
def direct_build(v, cls):
    """Builds H3 by named-object dictionaries (different code path)."""
    m = len(cls); names = {}; order = []
    def V(nm):
        if nm not in names: names[nm] = len(order); order.append(nm)
        return names[nm]
    for nm in ("T", "F", "B"): V(nm)
    for x in range(1, v + 1): V(("x", x, 1)); V(("x", x, 0))
    for j in range(m):
        for nm in ("s", "ns", "t0", "t1", "t2", "u0", "u1", "u2"): V((nm, j))
    E = [("T", "F"), ("F", "B"), ("B", "T")]
    for x in range(1, v + 1):
        E += [(("x", x, 1), ("x", x, 0)), (("x", x, 1), "B"), (("x", x, 0), "B")]
    L = lambda l: ("x", abs(l), 1 if l > 0 else 0)
    for j, (a, b, c) in enumerate(cls):
        g = lambda nm: (nm, j)
        E += [(g("s"), g("ns")), (g("s"), "B"), (g("ns"), "B"),
              (g("t0"), g("t1")), (g("t1"), g("t2")), (g("t2"), g("t0")),
              (g("u0"), g("u1")), (g("u1"), g("u2")), (g("u2"), g("u0")),
              (g("t0"), L(a)), (g("t1"), L(b)), (g("t2"), g("s")),
              (g("u0"), g("ns")), (g("u1"), L(c)), (g("u2"), "F")]
    E = [(names[a], names[b]) for a, b in E]
    V3 = len(order); U, W_ = V3, V3 + 1
    E5 = E + [(U, W_)] + [(ap, o) for o in range(V3) for ap in (U, W_)]
    V5 = V3 + 2
    return V5 + len(E5), [(V5 + i, u, w) for i, (u, w) in enumerate(E5)]

# ---------------- independent strict-C CSP solver (GAC + DFS) ----------------
class Budget(Exception): pass
def solve_c(nvars, clauses, node_cap=60_000, sym=None):
    """Generic 5-colour CSP: domains are 5-bit masks, GAC on every ternary
    C constraint, DFS on smallest domain.  Uses only C_TABLE."""
    occ = [[] for _ in range(nvars)]
    for ci, cl in enumerate(clauses):
        if len(set(cl)) != 3: raise ValueError("C clause needs 3 distinct names")
        for x in cl: occ[x].append(ci)
    TB = [(1 << a, 1 << b, 1 << c) for a, b, c in C_TABLE]
    nodes = [0]
    def gac(dom, queue):
        inq = set(queue)
        while queue:
            ci = queue.pop(); inq.discard(ci); a, b, c = clauses[ci]
            da, db, dc = dom[a], dom[b], dom[c]; sa = sb = sc = 0
            for ta, tb, tc in TB:
                if ta & da and tb & db and tc & dc: sa |= ta; sb |= tb; sc |= tc
            for x, s, d in ((a, sa, da), (b, sb, db), (c, sc, dc)):
                if s != d:
                    if not s: return False
                    dom[x] = s
                    for k in occ[x]:
                        if k != ci and k not in inq: queue.append(k); inq.add(k)
        return True
    # Branch only on names with >=2 occurrences.  Every clause must contain
    # at most one single-occurrence name (asserted); once all branch names are
    # singletons and GAC holds, each such name has a supported value.
    branch = [x for x in range(nvars) if len(occ[x]) >= 2]
    for cl in clauses:
        assert sum(1 for x in cl if len(occ[x]) < 2) <= 1
    def dfs(dom):
        nodes[0] += 1
        if nodes[0] > node_cap: raise Budget
        best = None; key = None
        for x in branch:
            d = dom[x]
            if d & (d - 1):
                k = (bin(d).count("1"), -len(occ[x]))
                if key is None or k < key: key = k; best = x
        if best is None:
            return [d & -d for d in dom]       # lowest supported value
        x = best
        for col in range(5):
            if dom[x] >> col & 1:
                d2 = dom[:]; d2[x] = 1 << col
                if gac(d2, list(occ[x])):
                    r = dfs(d2)
                    if r: return r
        return None
    dom = [31] * nvars
    if sym is not None:                      # D5-orbit representative
        p, q = sym; dom[p] = 1; dom[q] = (1 << 1) | (1 << 2)
    if not gac(dom, list(range(len(clauses)))): return None, nodes[0]
    r = dfs(dom)
    return (None if r is None else [d.bit_length() - 1 for d in r]), nodes[0]

def brute_sat(v, cls):
    for bits in itertools.product((False, True), repeat=v):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in cls): return bits
    return None

def extend_witness(v, cls, bits):
    """Boolean witness -> full strict-C colouring of K(F) (explicit)."""
    m = len(cls); V3, E3, V5, E5, NC = layout(v, m)
    T, F_, B = 0, 1, 2; col = [None] * NC
    col[0], col[1], col[2] = T, F_, B
    val = lambda l: bits[abs(l) - 1] == (l > 0)
    for x in range(v):
        col[3 + 2 * x] = T if bits[x] else F_; col[4 + 2 * x] = F_ if bits[x] else T
    def tri(terms, base):
        for perm in itertools.permutations((0, 1, 2)):
            if all(perm[k] != terms[k] for k in range(3)):
                for k in range(3): col[base + k] = perm[k]
                return True
        return False
    for j, (a, b, c) in enumerate(cls):
        base = 3 + 2 * v + 8 * j
        s = not (val(a) or val(b))             # s true iff needed
        if val(a) and val(b): s = False
        col[base] = T if s else F_; col[base + 1] = F_ if s else T
        ca, cb, cc = (T if val(l) else F_ for l in (a, b, c))
        ok1 = tri((ca, cb, col[base]), base + 2)
        ok2 = tri((col[base + 1], cc, F_), base + 5)
        if not (ok1 and ok2): return None
    col[V3], col[V3 + 1] = 3, 4
    clauses = [c_clause(i, v, m, lambda q: cls[q]) for i in range(E5)]
    for h, u, w in clauses:
        hs = [hc for hc in range(5) if C(hc, col[u], col[w])]
        if not hs: return None
        col[h] = hs[0]
    return col

def project(v, col):
    T, F_ = col[0], col[1]
    out = []
    for x in range(v):
        c = col[3 + 2 * x]
        if c not in (T, F_): return None
        out.append(c == T)
    return tuple(out)

def check_assign(clauses, col): return all(C(col[a], col[b], col[c]) for a, b, c in clauses)

# ---------------- main audit ----------------
def main():
    t0 = time.time(); rng = random.Random(SEED); res = {"seed": SEED}
    res["C_true_triples"] = len(C_TABLE)
    res["head_projection_ok"] = all(any(C(h, a, b) for h in range(5)) == (a != b)
                                    for a in range(5) for b in range(5))
    # D5 invariance (sanity only)
    res["d5_invariant"] = all(C(*[(s * x + r) % 5 for x in t]) == C(*t)
                              for t in itertools.product(range(5), repeat=3)
                              for r in range(5) for s in (1, 4))
    stats = dict(cases=0, sat=0, unsat=0, record_match=0, bit_match=0,
                 witness_ok=0, projection_ok=0, solver_agree=0, budget=0,
                 max_C_vars=0, max_C_clauses=0, oracle_calls_max_per_record=0,
                 fw3_equisat=0, nodes_total=0)
    cases = []
    # hand-built UNSAT controls (3-CNF, repeats allowed)
    cases.append((1, 3, [[1, 1, 1], [-1, -1, -1]]))
    cases.append((2, 3, [[1, 2, 2], [1, -2, -2], [-1, 2, 2], [-1, -2, -2]]))
    cases.append((2, 4, [[1, 2, 2, 2], [1, -2, -2, -2], [-1, 2, 2, 2], [-1, -2, -2, -2]]))
    cases.append((1, 4, [[1, 1, 1, 1], [-1, -1, -1, -1]]))
    cases.append((1, 5, [[1, 1, 1, 1, 1], [-1, -1, -1, -1, -1]]))
    cases.append((3, 3, [[s1 * 1, s2 * 2, s3 * 3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]))
    cases.append((2, 3, [[1, 2, 2], [-1, 2, 2], [-2, -2, -2]]))
    for _ in range(N_RANDOM):
        v = rng.randint(1, 3); W = rng.choice([3, 3, 4, 5]); m = rng.randint(1, 4 if W == 3 else 2)
        cls = [[rng.choice([-1, 1]) * rng.randint(1, v) for _ in range(W)] for _ in range(m)]
        cases.append((v, W, cls))
    for v, W, wide in cases:
        m = len(wide); calls = [0]
        def oracle(j, wide=wide):
            calls[0] += 1; return wide[j]
        v3, m3 = fw3_header(v, m, W)
        fw3 = [fw3_clause(t, v, m, W, lambda j: wide[j]) for t in range(m3)]
        src_sat = brute_sat(v, wide) is not None
        if (brute_sat(v3, fw3) is not None) == src_sat: stats["fw3_equisat"] += 1
        V3, E3, V5, E5, NC = layout(v3, m3)
        # random-access records, counting oracle calls per record
        recs = []
        for i in range(E5):
            calls[0] = 0
            recs.append(c_clause(i, v3, m3, lambda j: fw3_clause(j, v, m, W, oracle)))
            stats["oracle_calls_max_per_record"] = max(stats["oracle_calls_max_per_record"], calls[0])
        nd, drecs = direct_build(v3, fw3)
        assert nd == NC == 15 + 9 * v3 + 39 * m3 and E5 == 10 + 7 * v3 + 31 * m3
        if drecs == recs: stats["record_match"] += 1
        # encoded-bit check on a sample of positions
        Lbits = 64 + 3 * bw(NC - 1) * E5
        ok = True
        for p in rng.sample(range(Lbits), min(200, Lbits)):
            if c_bit(p, NC, E5, lambda i: recs[i]) != c_bit(p, NC, E5, lambda i: drecs[i]): ok = False
        stats["bit_match"] += ok
        stats["max_C_vars"] = max(stats["max_C_vars"], NC); stats["max_C_clauses"] = max(stats["max_C_clauses"], E5)
        try:
            sol, nodes = solve_c(NC, recs, sym=(0, 1))
        except Budget:
            stats["budget"] += 1; stats.setdefault("budget_cases", []).append([v, W, wide, "src_sat" if src_sat else "src_unsat"]); continue
        stats["nodes_total"] += nodes
        c_sat = sol is not None
        stats["cases"] += 1; stats["sat" if src_sat else "unsat"] += 1
        if c_sat == src_sat: stats["solver_agree"] += 1
        if c_sat:
            assert check_assign(recs, sol)
            pr = project(v3, sol)
            if pr is not None and all(any(pr[abs(l) - 1] == (l > 0) for l in c) for c in fw3)\
               and all(any(pr[abs(l) - 1] == (l > 0) for l in c) for c in wide):
                stats["projection_ok"] += 1
        if src_sat:
            bits = brute_sat(v3, fw3); col = extend_witness(v3, fw3, bits)
            if col is not None and check_assign(recs, col): stats["witness_ok"] += 1
    res.update(stats); res["seconds"] = round(time.time() - t0, 2)
    res["script_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    print(json.dumps(res, indent=1))
    return res

if __name__ == "__main__":
    main()
