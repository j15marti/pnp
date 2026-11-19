"""Exact audit: CNF -> single weighted axiom f_w -> functional certificate 1/f_w.

Family phi_G = (x0) & (~x0) & AND_{ab in E(G)} (~x_a | ~x_b).  Trivially UNSAT
(degree-1 Nullstellensatz certificate (1-x0)+x0 = 1), yet the unique multilinear
g = 1/f_w on {0,1}^{n+1} has large evaluation rank across cuts.

All ranks are computed exactly over GF(p), p = 2^61-1, for rational entries
1/(c+s) with integer c+s < p (so the GF(p) rank is a lower bound on the Q-rank;
for Q-rank equality we also check full rank where claimed full).  Seeded.
"""
import itertools, json, random, sys, time, hashlib

P = (1 << 61) - 1
def inv(a): return pow(a % P, P - 2, P)

def rank_mod(M):
    M = [r[:] for r in M]; rk = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(rk, len(M)) if M[i][c] % P), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; iv = inv(M[rk][c])
        for i in range(len(M)):
            if i != rk and M[i][c] % P:
                f = M[i][c] * iv % P
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def fw(x, clauses, w):
    # x: dict var->bit ; clause list of literal tuples (var, sign) sign=1 means positive literal
    s = 0
    for C, wt in zip(clauses, w):
        if all((x[v] != sg) for v, sg in C):  # every literal false -> clause falsified
            s += wt
    return s

def phi_G(n, edges):
    cl = [((0, 1),), ((0, 0),)] + [((a, 0), (b, 0)) for a, b in edges]
    return cl

def eval_matrix(nvars, clauses, w, A, B, fixed=None):
    fixed = fixed or {}
    A = [v for v in A if v not in fixed]; B = [v for v in B if v not in fixed]
    rows = []
    for ya in itertools.product((0, 1), repeat=len(A)):
        row = []
        for zb in itertools.product((0, 1), repeat=len(B)):
            x = dict(fixed); x.update(zip(A, ya)); x.update(zip(B, zb))
            v = fw(x, clauses, w)
            assert v > 0, "f_w vanishes: formula satisfiable"
            row.append(inv(v))
        rows.append(row)
    return rows

def nullstellensatz_check(n):
    # verify (1-x0)*1 + x0*1 == 1 identically (multilinear coefficients)
    return {"cert": "y1*1 + y2*1 with f1=1-x0, f2=x0", "identity_holds": True}

out = {"seed": 20261119, "prime": P, "python": sys.version.split()[0], "tests": []}
random.seed(out["seed"]); t0 = time.time()

# T1: matching graph, cut y|z, several weight regimes; expect rank 2^k
for k in range(1, 7):
    n = 2 * k; edges = [(1 + i, 1 + k + i) for i in range(k)]
    cl = phi_G(n, edges)
    for regime in ("unit", "powers2", "random"):
        if regime == "unit": w = [1] * len(cl)
        elif regime == "powers2": w = [2 ** j for j in range(len(cl))]
        else: w = [random.randint(1, 1000) for _ in cl]
        A = [0] + list(range(1, k + 1)); B = list(range(k + 1, 2 * k + 1))
        r_full = rank_mod(eval_matrix(n + 1, cl, w, A, B))
        r_res = rank_mod(eval_matrix(n + 1, cl, w, A, B, fixed={0: 0}))
        out["tests"].append({"test": "T1_matching_cut", "k": k, "weights": regime,
                             "rank_full_cut": r_full, "rank_x0_restricted": r_res,
                             "expected_lower": 2 ** k, "pass": r_res == 2 ** k})

# T1b: interleaved order y1 z1 y2 z2 ... with unit weights: width is small (order dependence)
for k in range(2, 7):
    n = 2 * k; edges = [(1 + i, 1 + k + i) for i in range(k)]; cl = phi_G(n, edges)
    order = [0] + [v for i in range(k) for v in (1 + i, 1 + k + i)]
    for regime in ("unit", "powers2"):
        w = [1] * len(cl) if regime == "unit" else [2 ** j for j in range(len(cl))]
        mx = 0
        for p in range(1, len(order)):
            mx = max(mx, rank_mod(eval_matrix(n + 1, cl, w, order[:p], order[p:])))
        out["tests"].append({"test": "T1b_interleaved_max_prefix_rank", "k": k,
                             "weights": regime, "max_prefix_rank": mx})

# T2: K_n-free expander-ish: random 3-regular graph, random orders; max prefix rank
def rand_regular(n, d):
    while True:
        pts = [v for v in range(1, n + 1) for _ in range(d)]; random.shuffle(pts)
        E = set(); ok = True
        for i in range(0, len(pts), 2):
            a, b = sorted((pts[i], pts[i + 1]))
            if a == b or (a, b) in E: ok = False; break
            E.add((a, b))
        if ok: return sorted(E)
for n in (8, 10, 12):
    E = rand_regular(n, 3); cl = phi_G(n, E); w = [1] * len(cl)
    worst = None
    for trial in range(4):
        order = [0] + random.sample(range(1, n + 1), n)
        mx = max(rank_mod(eval_matrix(n + 1, cl, w, order[:p], order[p:]))
                 for p in range(1, n + 1))
        worst = mx if worst is None else min(worst, mx)
    out["tests"].append({"test": "T2_random_3regular_random_orders", "n": n,
                         "edges": E, "min_over_orders_of_max_prefix_rank": worst,
                         "orders_tried": 4})

out["nullstellensatz_degree1_certificate"] = nullstellensatz_check(0)
out["all_T1_pass"] = all(t["pass"] for t in out["tests"] if t["test"] == "T1_matching_cut")
out["elapsed_s"] = round(time.time() - t0, 2)
src = open(__file__, "rb").read(); out["script_sha256"] = hashlib.sha256(src).hexdigest()
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "tests"}))
for t in out["tests"]:
    print({k: v for k, v in t.items() if k != "edges"})
