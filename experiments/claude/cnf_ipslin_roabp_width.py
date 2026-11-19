"""roABP width (variable order x_pi(1..n), then y_1..y_m) of the multilinear IPS_LIN'
certificate P(x,y)=sum_j g_j(x) y_j with g_j=[C_j is the first falsified clause] for
random UNSAT 3-CNF. Width at x-cut k = rank over Q of M_k[a,(b,j)] = [J(a,b)=j]
(multilinear evaluation rank = coefficient rank). Rank computed as rank of the smaller
Gram matrix (rank(M M^T)=rank(M) over R): exact integer Gram, rank mod p (lower bound)
and float rank (cross-check). Widths at y-cuts are <= m+1 and reported separately.
Usage: python3 -I cnf_ipslin_roabp_width.py OUT.json
"""
import json, sys, time, itertools
import numpy as np
P = 2147483647

def rank_mod_p(A):
    A = (A % P).astype(np.int64).copy(); r = 0; rows, cols = A.shape
    for c in range(cols):
        piv = np.nonzero(A[r:, c])[0]
        if piv.size == 0: continue
        i = r + piv[0]; A[[r, i]] = A[[i, r]]
        inv = pow(int(A[r, c]), P - 2, P); A[r] = (A[r] * inv) % P
        f = A[:, c].copy(); f[r] = 0; nz = np.nonzero(f)[0]
        if nz.size: A[nz] = (A[nz] - (f[nz, None] * A[r][None, :]) % P) % P
        r += 1
        if r == rows: break
    return r

def random_cnf(n, m, rng):
    cl = []
    for _ in range(m):
        v = rng.choice(n, 3, replace=False); s = rng.integers(0, 2, 3)
        cl.append([(int(a), int(b)) for a, b in zip(v, s)])  # literal true iff x_v == b
    return cl

def first_falsified(n, cl, order):
    # points indexed by integer whose bit (n-1-t) is x_{order[t]}  (prefix = high bits)
    N = 1 << n; idx = np.arange(N, dtype=np.int64)
    bits = {order[t]: (idx >> (n - 1 - t)) & 1 for t in range(n)}
    J = np.full(N, -1, dtype=np.int64)
    for j, c in enumerate(cl):
        fals = np.ones(N, dtype=bool)
        for v, s in c: fals &= (bits[v] != s)
        J[(J < 0) & fals] = j
    return J

def cut_rank(J, n, k, m):
    R = J.reshape(1 << k, 1 << (n - k))
    U = np.unique(R, axis=0)            # distinct subfunctions
    D = U.shape[0]
    cols = np.unique(U.T, axis=0)       # distinct column patterns b -> (J(a,b))_a
    if D <= cols.shape[0] * 1:          # Gram over rows: G[a,a'] = #{b: J(a,b)=J(a',b)}
        G = np.zeros((D, D), dtype=np.int64)
        for b in range(U.shape[1]):
            col = U[:, b]; G += (col[:, None] == col[None, :])
    else:                               # Gram over (b,j) column side via M^T M, use distinct b-patterns w/ multiplicity
        # rank(M)=rank of block matrix with columns (b,j); duplicate b-patterns don't change rank
        H = []
        for col in cols:
            for j in np.unique(col): H.append((col == j).astype(np.int64))
        H = np.array(H)                 # rows = (b,j) pairs, cols = a
        G = H @ H.T
    rp = rank_mod_p(G); rf = int(np.linalg.matrix_rank(G.astype(float)))
    return D, rp, rf

def primal_order(n, cl):
    # reverse Cuthill-McKee-like BFS order on primal graph (heuristic small cutwidth)
    adj = {v: set() for v in range(n)}
    for c in cl:
        for (u, _), (w, _) in itertools.combinations(c, 2): adj[u].add(w); adj[w].add(u)
    start = min(range(n), key=lambda v: len(adj[v])); seen = [start]; q = [start]
    while q:
        u = q.pop(0)
        for w in sorted(adj[u] - set(seen), key=lambda v: len(adj[v])): seen.append(w); q.append(w)
    seen += [v for v in range(n) if v not in seen]
    return seen[::-1]

def run():
    out = {"meta": {"python": sys.version.split()[0], "numpy": np.__version__, "p": P,
                    "ratio": 6.0, "seeds": list(range(3))}, "rows": []}
    t0 = time.time()
    for n in [8, 10, 12, 14, 16, 18]:
        m = int(round(6.0 * n))
        for seed in range(3):
            rng = np.random.default_rng(10_000 * n + seed); cl = random_cnf(n, m, rng)
            for oname in ["natural", "bfs"]:
                order = list(range(n)) if oname == "natural" else primal_order(n, cl)
                pos = {v: t for t, v in enumerate(order)}
                for cname in ["given", "sorted_by_last_var"]:
                    cc = cl if cname == "given" else sorted(cl, key=lambda c: max(pos[v] for v, _ in c))
                    J = first_falsified(n, cc, order)
                    if (J < 0).any():
                        out["rows"].append({"n": n, "seed": seed, "sat": True}); break
                    ws = []
                    for k in range(1, n):
                        D, rp, rf = cut_rank(J, n, k, m); ws.append([k, D, rp, rf])
                    W = max(w[2] for w in ws)
                    cutw = max(sum(1 for c in cc if min(pos[v] for v, _ in c) < k <= max(pos[v] for v, _ in c)) for k in range(1, n))
                    out["rows"].append({"n": n, "m": m, "seed": seed, "order": oname, "clause_order": cname,
                                        "width_x_cuts_modp": W, "width_bound_y_cuts": m + 1,
                                        "two_pow_half_n": 2 ** (n // 2), "clause_cutwidth": cutw,
                                        "per_cut[k,distinct,rank_p,rank_float]": ws,
                                        "distinct_used_clauses": int(len(np.unique(J)))})
                    print(n, seed, oname, cname, "W=", W, "2^(n/2)=", 2 ** (n // 2), "D_max=", max(w[1] for w in ws), "cw=", cutw, f"{time.time()-t0:.1f}s", flush=True)
    out["meta"]["seconds"] = round(time.time() - t0, 2)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
if __name__ == "__main__":
    run()
