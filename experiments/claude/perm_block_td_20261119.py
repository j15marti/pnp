"""Independent finite check of the coefficient-transcendence-degree core of
openai/ten-proofs Permanent.lean (rev 94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6).

Marked variables: a matching of 2*ell entries (rows r_i, cols c_i distinct).
For each subset S of marked positions, coefficient P_S of prod_{i in S} y_i in
per_n is per of the matrix with rows/cols of S deleted and the remaining
marked entries set to 0.  Rank (mod p) of the Jacobian of {P_S} w.r.t. the
unmarked variables at a random integer point is a SOUND lower bound on the
transcendence degree over C (rank mod p <= rank over Q <= generic rank).
Also reports the trivial ceiling min(2^(2 ell), n^2 - 2 ell).
"""
import itertools, json, random, sys, hashlib, time
import numpy as np

P = 1000003

def minor_perms(A):
    """All d per(A)/d a_kl mod P via Ryser, vectorized over column subsets."""
    n = A.shape[0]
    T = np.array([[(t >> j) & 1 for j in range(n)] for t in range(1, 1 << n)], dtype=np.int64)
    sign = np.where((T.sum(1) % 2) == (n % 2), 1, -1).astype(np.int64)  # (-1)^{n-|T|}
    R = (T @ A.T) % P            # R[t,i] = sum_{j in T} a_ij
    G = np.zeros((n, n), dtype=np.int64)
    # prefix/suffix products excluding row k
    pre = np.ones((R.shape[0], n + 1), dtype=np.int64)
    suf = np.ones((R.shape[0], n + 1), dtype=np.int64)
    for i in range(n):
        pre[:, i + 1] = pre[:, i] * R[:, i] % P
    for i in range(n - 1, -1, -1):
        suf[:, i] = suf[:, i + 1] * R[:, i] % P
    for k in range(n):
        ex = pre[:, k] * suf[:, k + 1] % P * sign % P
        G[k, :] = (ex[:, None] * T).sum(0) % P   # T[t,l]=1 iff l in T
    return G

def rank_mod_p(M):
    M = M.copy() % P; r = 0; rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), P - 2, P)
        M[r] = M[r] * inv % P
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % P
        r += 1
        if r == rows: break
    return r

def run(ell, m, seed):
    n = 2 * ell + m
    rng = random.Random(seed)
    marked = [(i, (i + 1) % n) for i in range(2 * ell)]   # a matching: distinct rows, distinct cols
    mset = set(marked)
    other = [(i, j) for i in range(n) for j in range(n) if (i, j) not in mset]
    col = {v: k for k, v in enumerate(other)}
    A = np.array([[rng.randrange(1, P) for _ in range(n)] for _ in range(n)], dtype=np.int64)
    J = []
    for bits in range(1 << (2 * ell)):
        S = [marked[i] for i in range(2 * ell) if bits >> i & 1]
        dr = {r for r, _ in S}; dc = {c for _, c in S}
        rk = [i for i in range(n) if i not in dr]; ck = [j for j in range(n) if j not in dc]
        B = A[np.ix_(rk, ck)].copy()
        for (r, c) in marked:
            if (r, c) not in S and r in rk and c in ck:
                B[rk.index(r), ck.index(c)] = 0
        G = minor_perms(B)
        row = np.zeros(len(other), dtype=np.int64)
        for a, r in enumerate(rk):
            for b, c in enumerate(ck):
                if (r, c) in col:
                    row[col[(r, c)]] = G[a, b]
        J.append(row)
    J = np.array(J)
    rk_ = rank_mod_p(J)
    return dict(ell=ell, m=m, n=n, seed=seed, coeffs=1 << (2 * ell), unmarked_vars=len(other),
                claimed_lower_m2=m * m, jacobian_rank_mod_p=rk_,
                ceiling=min(1 << (2 * ell), len(other)), hypotheses_m_le_2pow_ell_and_2ell_lt_m=(m <= 2 ** ell and 2 * ell < m))

if __name__ == "__main__":
    t0 = time.time(); out = []
    for ell, m in [(2, 3), (2, 4), (3, 7), (3, 8)]:
        for seed in (2026111901, 2026111902):
            out.append(run(ell, m, seed)); print(out[-1], flush=True)
    res = dict(source="openai/ten-proofs@94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6 Permanent.lean",
               prime=P, script_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
               results=out, seconds=round(time.time() - t0, 2))
    json.dump(res, open(sys.argv[1], 'w'), indent=1)
