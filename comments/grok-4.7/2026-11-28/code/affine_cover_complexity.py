#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 ~07:00 KST: affine guard-cover complexity and Res(+) transfer checks.
Exhaustive / seeded checks only (COMPUTATIONAL). Deterministic seed 20261128.
Points of F_2^n are ints; an affine guard is a list of (mask, bit) equations  popcount(mask & x)%2 == bit.
"""
import itertools, json, random, sys
SEED = 20261128
rng = random.Random(SEED)
par = lambda v: bin(v).count('1') & 1

def members(g, n):
    return frozenset(x for x in range(1 << n) if all(par(m & x) == b for m, b in g))

def rank(vecs):
    basis = []  # GF(2) elimination
    for v in vecs:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis)

def affine_solve(eqs, n):
    """return True iff linear system over GF(2) consistent (Gaussian elimination)."""
    rows = [(m, b) for m, b in eqs]
    piv = {}
    for m, b in rows:
        for p, (pm, pb) in piv.items():
            if m >> p & 1:
                m ^= pm; b ^= pb
        if m == 0:
            if b: return False
            continue
        p = m.bit_length() - 1
        for q in list(piv):
            qm, qb = piv[q]
            if qm >> p & 1:
                piv[q] = (qm ^ m, qb ^ b)
        piv[p] = (m, b)
    return True

out = {"seed": SEED}

# ---------- 1. Brouwer-type joint rank bound for irredundant covers (spot-check of T2 1cab6e6 / T1 ab7288c) ----------
def all_affine_subspaces(n):
    seen = {}
    masks = range(1, 1 << n)
    for c in range(0, n + 1):
        for ms in itertools.combinations(masks, c):
            if rank(list(ms)) != c: continue
            for bits in itertools.product((0, 1), repeat=c):
                g = list(zip(ms, bits))
                S = members(g, n)
                if S and S not in seen:
                    seen[S] = g
    return seen

def joint_rank(subsets_eqs):
    return rank([m for g in subsets_eqs for m, _ in g])

def canonical_eqs(S, n):
    # normals of aff(S): masks u with u.x constant on S
    S = list(S); x0 = S[0]
    normals = [u for u in range(1, 1 << n) if all(par(u & (x ^ x0)) == 0 for x in S)]
    return normals

def brouwer_check(n, kmax, exhaustive_k, samples):
    subs = all_affine_subspaces(n)
    items = [S for S in subs if len(S) < (1 << n)]  # proper subspaces
    normals = {S: canonical_eqs(S, n) for S in items}
    full = frozenset(range(1 << n))
    stats = {}; worst = None
    def irredundant(cov):
        for i in range(len(cov)):
            rest = frozenset().union(*[cov[j] for j in range(len(cov)) if j != i])
            if rest == full: return False
        return True
    def check(cov):
        nonlocal worst
        r = rank([u for S in cov for u in normals[S]])
        k = len(cov)
        st = stats.setdefault(k, {"covers": 0, "max_joint_rank": 0, "max_indiv_codim": 0, "kraft_min": None})
        st["covers"] += 1
        st["max_joint_rank"] = max(st["max_joint_rank"], r)
        st["max_indiv_codim"] = max(st["max_indiv_codim"], max(rank(normals[S]) for S in cov))
        kr = sum(len(S) for S in cov) / (1 << n)
        st["kraft_min"] = kr if st["kraft_min"] is None else min(st["kraft_min"], kr)
        if r > k - 1: worst = (k, r, [sorted(S) for S in cov])
    # exhaustive for small k
    for k in range(2, exhaustive_k + 1):
        for cov in itertools.combinations(items, k):
            if frozenset().union(*cov) == full and irredundant(cov):
                check(cov)
    # random greedy irredundant covers for larger k
    for _ in range(samples):
        k_target = rng.randint(exhaustive_k + 1, kmax)
        cov = []; covered = frozenset()
        while covered != full and len(cov) < 3 * k_target:
            cand = rng.choice(items)
            if not cand <= covered:
                cov.append(cand); covered |= cand
        if covered != full: continue
        # prune to irredundant
        changed = True
        while changed:
            changed = False
            for i in range(len(cov)):
                rest = [cov[j] for j in range(len(cov)) if j != i]
                if frozenset().union(*rest) == full:
                    cov = rest; changed = True; break
        check(tuple(cov))
    return {"n": n, "num_proper_affine_subspaces": len(items), "by_k": stats, "counterexample": worst}

out["brouwer_rank_check"] = [brouwer_check(3, 7, 4, 20000), brouwer_check(4, 9, 3, 20000)]

# ---------- 2. Coverage complexity: codim-1 guards in poly time; NAE codim-2 reduction ----------
def covered_bruteforce(guards, n):
    return all(any(all(par(m & x) == b for m, b in g) for g in guards) for x in range(1 << n))

def covered_codim1(guards, n):
    # x uncovered iff for each hyperplane guard (m,b): m.x = 1-b  -> a linear system
    eqs = []
    for g in guards:
        if not affine_solve(g, n): continue          # empty guard covers nothing
        assert rank([m for m, _ in g]) <= 1
        if rank([m for m, _ in g]) == 0: return True  # whole-space guard
        m, b = g[0]
        eqs.append((m, 1 - b))
    return not affine_solve(eqs, n)

agree = 0; ncov = 0
for t in range(3000):
    n = rng.randint(1, 8); k = rng.randint(1, 3 * n)
    guards = [[(rng.randrange(1, 1 << n), rng.randint(0, 1))] for _ in range(k)]
    a = covered_bruteforce(guards, n); b = covered_codim1(guards, n)
    agree += (a == b); ncov += a
out["codim1_poly_check"] = {"trials": 3000, "agree": agree, "covered_instances": ncov}

def nae_guards(triples, n):
    # guard {x_a = x_b = x_c} = {x_a+x_b=0, x_b+x_c=0}: codim 2, linear (contains 0 and all-ones)
    return [[((1 << a) | (1 << b), 0), ((1 << b) | (1 << c), 0)] for a, b, c in triples]

def nae_sat(triples, n):
    return any(all(not ((x >> a & 1) == (x >> b & 1) == (x >> c & 1)) for a, b, c in triples) for x in range(1 << n))

agree = 0; unsat = 0
for t in range(3000):
    n = rng.randint(3, 10); m = rng.randint(1, 4 * n)
    triples = [tuple(rng.sample(range(n), 3)) for _ in range(m)]
    cov = covered_bruteforce(nae_guards(triples, n), n)
    agree += (cov == (not nae_sat(triples, n))); unsat += cov
out["nae_reduction_check"] = {"trials": 3000, "cover_iff_NAE_unsat": agree, "covered(=NAE-UNSAT)": unsat}

# Kraft-type necessary condition sum 2^-codim >= 1 on random covers
viol = 0; tested = 0
for t in range(3000):
    n = rng.randint(2, 7); k = rng.randint(1, 12)
    guards = []
    for _ in range(k):
        c = rng.randint(0, min(3, n))
        guards.append([(rng.randrange(1, 1 << n), rng.randint(0, 1)) for _ in range(c)])
    if covered_bruteforce(guards, n):
        tested += 1
        s = sum(len(members(g, n)) for g in guards) / (1 << n)
        viol += s < 1
out["kraft_check"] = {"covers_tested": tested, "violations": viol}

# ---------- 3. Batching non-compositionality: complement of 5 codim-2 guards needs many affine pieces ----------
def min_disjoint_pieces_upper(guards, n):
    # disjointification count via A\G = disjoint union of codim pieces (upper bound prod codim)
    pieces = [[]]
    for g in guards:
        new = []
        for p in pieces:
            # p \ g : split on equations of g sequentially
            prefix = []
            for (m, b) in g:
                cand = p + prefix + [(m, 1 - b)]
                if affine_solve(cand, n): new.append(cand)
                prefix.append((m, b))
                if not affine_solve(p + prefix, n): break
        pieces = new
    return len(pieces)

# disjoint coordinate guards {x_{2i}=0, x_{2i+1}=0}, i<5, n=10: complement = product of 3-point sets
n = 10
g5 = [[(1 << (2 * i), 0), (1 << (2 * i + 1), 0)] for i in range(5)]
U = [x for x in range(1 << n) if not any(all(par(m & x) == b for m, b in g) for g in g5)]
out["batching_example"] = {"n": n, "uncovered_points": len(U), "equals_3^5": len(U) == 3 ** 5,
                           "disjointification_pieces": min_disjoint_pieces_upper(g5, n),
                           "note": "U is a product of five 3-point sets {01,10,11}; any affine flat inside U has <=2^5 points (projection to each pair is a flat inside a 3-point set, size<=2), so U needs >= ceil(243/32)=8 flats and its affine hull is all of F_2^10."}
aff_hull_rank = rank([x ^ U[0] for x in U])
out["batching_example"]["affine_hull_dim_of_U"] = aff_hull_rank

# ---------- 4. Spot-check of T1 certificate 18cef33 (EB-JOINT-24) inclusion-exclusion arithmetic ----------
cert_counts = {1: 33554432, 2: 33554432, 4: 33554432, 8: 33554432, 16: 67108864, 17: 16777216, 18: 16777216, 20: 16777216, 24: 16777216}
cover = sum(((-1) ** (bin(S).count('1') + 1)) * c for S, c in cert_counts.items())
out["t1_cert_18cef33"] = {"carrier": 2 ** 27, "inclusion_exclusion": cover, "covered": cover == 2 ** 27,
    "observation": "guards 0-3 pin (rel. port 545, rel. port 617) to all four values: a depth-2 decision split, i.e. joint normal rank 2; guard 4 is redundant"}
# replicate with symbolic affine guards on a 27-dim carrier (coords 0,1 for the two pins, 2 for port 249)
n = 27
g = [[(1, a), (2, b)] for b in (0, 1) for a in (0, 1)] + [[(4, 0)]]
def isect_count(gs, n):
    eqs = [e for gg in gs for e in gg]
    return 0 if not affine_solve(eqs, n) else 2 ** (n - rank([m for m, _ in eqs]))
ie = sum(((-1) ** (len(S) + 1)) * isect_count([g[i] for i in S], n) for k in range(1, 6) for S in itertools.combinations(range(5), k))
out["t1_cert_18cef33"]["symbolic_replay_count"] = ie
out["t1_cert_18cef33"]["joint_normal_rank_irredundant_subcover"] = rank([m for gg in g[:4] for m, _ in gg])

json.dump(out, sys.stdout, indent=1, default=str)
print()
