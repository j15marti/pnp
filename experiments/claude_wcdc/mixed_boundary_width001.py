#!/usr/bin/env python3
"""WCDC-001: finite checks of the mixed (clause / local factor / GF(2) row) boundary-support
lemma and of the failure of a size-width relation in the definition-free R_mix fragment.
Deterministic, stdlib only, designed to finish in < 30 s.  Output: JSON to argv[1]."""
import itertools, json, random, sys, time
t0 = time.time()
random.seed(20261114)
checks = 0; fails = 0
def lit_true(l, a): v = abs(l) - 1; return ((a >> v) & 1) == (1 if l > 0 else 0)
def clause_sat(c, a): return any(lit_true(l, a) for l in c)
def models(S, n): return [a for a in range(1 << n) if all(clause_sat(c, a) for c in S)]
def popc(x): return bin(x).count("1")
def implied_equations(M, n):
    """all nontrivial affine equations <mask,x> = b (mask != 0) true on every model in M"""
    out = []
    for mask in range(1, 1 << n):
        for b in (0, 1):
            if all((popc(mask & a) & 1) == b for a in M): out.append((mask, b))
    return out
def implied_clauses(M, n, maxw=3):
    out = []
    for w in range(1, maxw + 1):
        for vs in itertools.combinations(range(n), w):
            for signs in itertools.product((1, -1), repeat=w):
                c = tuple(s * (v + 1) for v, s in zip(vs, signs))
                if all(clause_sat(c, a) for a in M): out.append(c)
    return out
def boundary(S):
    cnt = {}
    for c in S:
        for l in c: cnt[abs(l) - 1] = cnt.get(abs(l) - 1, 0) + 1
    return {v for v, k in cnt.items() if k == 1}
def lemma_check(F, n, maxS):
    """For every inclusion-minimal S (|S|<=maxS) implying object E, check boundary(S) subset supp(E)."""
    global checks, fails
    cache = {}
    def imp(S):
        if S not in cache:
            M = models([F[i] for i in S], n)
            cache[S] = (frozenset(implied_equations(M, n)), frozenset(implied_clauses(M, n)))
        return cache[S]
    local = 0
    for k in range(1, maxS + 1):
        for S in itertools.combinations(range(len(F)), k):
            eqs, cls = imp(S)
            subs = [imp(tuple(x for x in S if x != d)) if k > 1 else (frozenset(), frozenset()) for d in S]
            B = boundary([F[i] for i in S])
            for (mask, b) in eqs:
                if any((mask, b) in s[0] for s in subs): continue  # S not minimal for E
                if k == 1 and False: pass
                supp = {v for v in range(n) if (mask >> v) & 1}
                checks += 1; local += 1
                if not B <= supp: fails += 1
            for c in cls:
                if any(c in s[1] for s in subs): continue
                supp = {abs(l) - 1 for l in c}
                checks += 1; local += 1
                if not B <= supp: fails += 1
    return local
def tseitin(edges, h, charge):
    """strict 3-CNF Tseitin for cubic graph: per vertex, 4 clauses forbidding wrong-parity patterns"""
    inc = {v: [] for v in range(h)}
    for i, (u, v) in enumerate(edges): inc[u].append(i); inc[v].append(i)
    F = []
    for v in range(h):
        es = inc[v]; assert len(es) == 3
        for z in itertools.product((0, 1), repeat=3):
            if (sum(z) & 1) != charge[v]:
                F.append(tuple((e + 1) if z[j] == 0 else -(e + 1) for j, e in enumerate(es)))
    return F
def random_3cnf(n, m):
    F = set()
    while len(F) < m:
        vs = random.sample(range(n), 3)
        F.add(tuple(sorted(((v + 1) * random.choice((1, -1)) for v in vs), key=abs)))
    return sorted(F)
lemma_runs = []
K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for name, F, n, maxS in [
    ("tseitin_K4_odd", tseitin(K4, 4, [1, 0, 0, 0]), 6, 4),
    ("tseitin_K4_even", tseitin(K4, 4, [0, 0, 0, 0]), 6, 4),
    ("rand3cnf_n7_m14_a", random_3cnf(7, 14), 7, 3),
    ("rand3cnf_n7_m14_b", random_3cnf(7, 14), 7, 3),
    ("rand3cnf_n6_m16", random_3cnf(6, 16), 6, 4)]:
    nM = len(models(F, n))
    lemma_runs.append({"name": name, "n": n, "m": len(F), "models": nM, "maxS": maxS,
                       "minimal_implications_checked": lemma_check(F, n, maxS)})
# --- size/support failure: cubic Tseitin.  Any refutation in the definition-free fragment contains an
# object whose minimal implying source set S has |S| in (mu*/3, 2mu*/3]; its support >= |boundary(S)|.
# For Tseitin a minimal source set implying a row/clause is a union of whole vertex blocks up to
# local slack; we report the standard edge-cut quantity  min_{h/3<|U|<=2h/3} |delta(U)|  (exact, brute force)
def cubic_random(h):
    while True:
        pts = [v for v in range(h) for _ in range(3)]; random.shuffle(pts)
        E = set(); ok = True
        for i in range(0, len(pts), 2):
            u, v = pts[i], pts[i + 1]
            if u == v or (min(u, v), max(u, v)) in E: ok = False; break
            E.add((min(u, v), max(u, v)))
        if ok: return sorted(E)
def mincut_mid(edges, h):
    best = None
    for U in range(1, 1 << h):
        k = popc(U)
        if not (h / 3 < k <= 2 * h / 3): continue
        cut = sum(1 for (u, v) in edges if ((U >> u) & 1) != ((U >> v) & 1))
        best = cut if best is None else min(best, cut)
    return best
def canonical_maxsupport(edges, h):
    # canonical 4h-1 proof: sum rows of vertices 0..j; support of prefix row = |delta({0..j})|
    mx = 0
    for j in range(h):
        U = (1 << (j + 1)) - 1
        mx = max(mx, sum(1 for (u, v) in edges if ((U >> u) & 1) != ((U >> v) & 1)))
    return mx
PET = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
graphs = [("K4", K4, 4), ("Petersen", PET, 10)] + [("random_cubic_h%d" % h, cubic_random(h), h) for h in (8, 10, 12, 14, 16)]
def connected(E, h, skip=None):
    adj = {v: [] for v in range(h)}
    for i, (u, v) in enumerate(E):
        if i != skip: adj[u].append(v); adj[v].append(u)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == h
size_width = []
for name, E, h in graphs:
    conn = connected(E, h); bridgeless = conn and all(connected(E, h, i) for i in range(len(E)))
    size_width.append({"graph": name, "h": h, "edges": len(E), "connected": conn, "bridgeless": bridgeless,
                       "W_Rmix341": (4 * h - 1) if bridgeless else None,
                       "W_status": "PROVED/EXACT (LSPV-2/341)" if bridgeless else "not claimed",
                       "mid_edge_cut_lower_bound_on_some_row_support": mincut_mid(E, h),
                       "canonical_proof_max_row_support": canonical_maxsupport(E, h)})
    checks += 1
    if size_width[-1]["canonical_proof_max_row_support"] < size_width[-1]["mid_edge_cut_lower_bound_on_some_row_support"]:
        # canonical proof is a valid refutation, so lemma predicts max support >= lower bound
        fails += 1
out = {"id": "CLAUDE-WCDC-001", "checks": checks, "failures": fails, "lemma_runs": lemma_runs,
       "tseitin_size_vs_support": size_width, "seconds": round(time.time() - t0, 2),
       "note": "finite COMPUTATIONAL evidence only; host time is not native machine cost"}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: out[k] for k in ("checks", "failures", "seconds")}), file=sys.stderr)
for r in lemma_runs: print(r, file=sys.stderr)
for r in size_width: print(r, file=sys.stderr)
