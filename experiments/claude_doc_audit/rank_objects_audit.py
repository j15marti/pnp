"""Audit of two rank claims in the user's Google doc 'P vs. NP Proof Attempts'.
(1) Solution-indicator matricization rank of random 3-CNF across balanced variable splits
    (the 'volume-law MPS' object of Attempt IB): rank_Q <= #solutions, = 0 when UNSAT.
(2) Evaluation matrix of g = 1/f for f = 1 + sum 2^(i-1) x_i (IPS_LIN' functional object,
    Attempt IIB): exact rank over Q for every balanced split (Cauchy matrix => full rank).
Exact arithmetic only: (1) mod-p rank (lower bound on rank_Q) plus #solutions (upper bound);
(2) Fraction Gaussian elimination. Seed fixed. Prints JSON."""
import itertools, json, random, sys, time
from fractions import Fraction

P = 2**31 - 1

def rank_mod_p(rows):
    rows = [r[:] for r in rows if any(r)]
    rk, col, ncol = 0, 0, (len(rows[0]) if rows else 0)
    while rows and col < ncol:
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] % P), None)
        if piv is None:
            col += 1; continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][col], P - 2, P)
        rows[rk] = [(v * inv) % P for v in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][col] % P:
                c = rows[i][col]
                rows[i] = [(a - c * b) % P for a, b in zip(rows[i], rows[rk])]
        rk += 1; col += 1
    return rk

def rank_Q(M):
    M = [r[:] for r in M]; rk = 0; n = len(M[0])
    for col in range(n):
        piv = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                c = M[i][col] / M[rk][col]
                M[i] = [a - c * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk

def random_3cnf(n, m, rng):
    cls = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        cls.append([(v, rng.random() < 0.5) for v in vs])  # (var, positive?)
    return cls

def sat_table(n, cls):
    # truth table over all 2^n assignments, bit i of index = x_i
    N = 1 << n; tab = [1] * N
    for x in range(N):
        for c in cls:
            if not any(((x >> v) & 1) == pos for v, pos in c):
                tab[x] = 0; break
    return tab

def indicator_rank(n, tab, A):
    B = [i for i in range(n) if i not in A]
    rows = []
    for a in range(1 << len(A)):
        xa = sum(((a >> j) & 1) << A[j] for j in range(len(A)))
        rows.append([tab[xa | sum(((b >> j) & 1) << B[j] for j in range(len(B)))]
                     for b in range(1 << len(B))])
    return rank_mod_p(rows)

def main():
    t0 = time.time(); seed = 20261120; rng = random.Random(seed); out = {"seed": seed}
    n = 14; res = []
    for alpha in (3.0, 4.26, 5.5):
        m = round(alpha * n)
        for trial in range(4):
            cls = random_3cnf(n, m, rng); tab = sat_table(n, cls); s = sum(tab)
            splits = [list(range(n // 2))] + [sorted(rng.sample(range(n), n // 2)) for _ in range(2)]
            rks = [indicator_rank(n, tab, A) for A in splits]
            assert all(r <= s for r in rks)
            if s == 0: assert all(r == 0 for r in rks)
            res.append({"alpha": alpha, "m": m, "trial": trial, "solutions": s,
                        "rank_modp_lower_bounds": rks, "full_rank_would_be": 1 << (n // 2)})
    out["indicator"] = {"n": n, "rows": res}
    ipr = []
    for k in (3, 4, 5):
        nn = 2 * k; w = [1 << i for i in range(nn)]
        for trial in range(3):
            A = list(range(k)) if trial == 0 else sorted(rng.sample(range(nn), k))
            B = [i for i in range(nn) if i not in A]
            M = [[Fraction(1, 1 + sum(w[A[j]] for j in range(k) if (a >> j) & 1)
                              + sum(w[B[j]] for j in range(k) if (b >> j) & 1))
                  for b in range(1 << k)] for a in range(1 << k)]
            r = rank_Q(M); assert r == 1 << k
            ipr.append({"n": nn, "split_A": A, "rank_Q": r, "full": 1 << k})
    out["inverse_subset_sum"] = ipr
    out["runtime_s"] = round(time.time() - t0, 2)
    json.dump(out, sys.stdout, indent=1)

if __name__ == "__main__":
    main()
