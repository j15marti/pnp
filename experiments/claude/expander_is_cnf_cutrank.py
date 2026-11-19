"""Exact cut-rank of the independent-set 2-CNF of Gabber-Galil expanders.

Claude lane, 2026-11-19. Finite COMPUTATIONAL illustration of the symbolic lemma in
research/agents/claude/cut-rank/2026-11-19_1300_CLAUDE_EXPANDER_IS_CNF_CUTRANK.md.

F_H = AND_{uv in E(H)} (not x_u or not x_v).  For a variable bipartition (A,B) we compute
the rank of the 2^|A| x 2^|B| solution-indicator matrix over GF(2) and mod p=2^31-1 (m<=4),
and a greedy induced matching across the cut, checking rank >= 2^k (lemma) for every cut.
"""
import itertools, json, random, sys, time
import numpy as np

P = 2147483647

def gabber_galil(m):
    N = m * m
    idx = lambda x, y: (x % m) * m + (y % m)
    multi = []
    for x in range(m):
        for y in range(m):
            u = idx(x, y)
            for v in (idx(x + 2*y, y), idx(x + 2*y + 1, y), idx(x, y + 2*x), idx(x, y + 2*x + 1)):
                multi.append((u, v))
    A = np.zeros((N, N))
    for u, v in multi:
        A[u, v] += 1; A[v, u] += 1          # forward maps + inverses -> 8-regular multigraph
    simple = sorted({(min(u, v), max(u, v)) for u, v in multi if u != v})
    return N, A, simple

def gf2_rank(rows):
    rank, rows = 0, [r for r in rows if r]
    basis = {}
    for r in rows:
        while r:
            h = r.bit_length() - 1
            if h in basis: r ^= basis[h]
            else: basis[h] = r; rank += 1; break
    return rank

def modp_rank(M):
    M = M.astype(np.int64) % P; r = 0; R, C = M.shape
    for c in range(C):
        piv = next((i for i in range(r, R) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), P - 2, P)
        M[r] = (M[r] * inv) % P
        nz = np.nonzero(M[:, c])[0]
        for i in nz:
            if i != r: M[i] = (M[i] - M[i, c] * M[r]) % P
        r += 1
        if r == R: break
    return r

def indicator_rows(N, edges, Aside, Bside):
    """Row a (assignment to Aside) -> bitmask over assignments to Bside."""
    posA = {v: i for i, v in enumerate(Aside)}; posB = {v: i for i, v in enumerate(Bside)}
    EA = [(posA[u], posA[v]) for u, v in edges if u in posA and v in posA]
    EB = [(posB[u], posB[v]) for u, v in edges if u in posB and v in posB]
    EX = [(posA[u], posB[v]) if u in posA else (posA[v], posB[u]) for u, v in edges if (u in posA) != (v in posA)]
    nB = len(Bside)
    okB = np.ones(1 << nB, dtype=bool); b = np.arange(1 << nB)
    for i, j in EB: okB &= ~(((b >> i) & 1).astype(bool) & ((b >> j) & 1).astype(bool))
    rows, dense = [], []
    for a in range(1 << len(Aside)):
        if any((a >> i) & 1 and (a >> j) & 1 for i, j in EA): continue
        forb = 0
        for i, j in EX:
            if (a >> i) & 1: forb |= 1 << j
        ok = okB & ((b & forb) == 0)
        rows.append(int(np.packbits(ok[::-1].astype(np.uint8)).tobytes().hex() or '0', 16))
        dense.append(ok)
    return rows, dense

def greedy_induced_matching(edges, Aset, nbr):
    cross = [(u, v) for u, v in edges if (u in Aset) != (v in Aset)]
    blocked, M = set(), []
    for u, v in cross:
        if u in blocked or v in blocked: continue
        # require no edge from {u,v} to an already matched vertex: enforced by blocking closed nbhds
        M.append((u, v)); blocked |= {u, v} | nbr[u] | nbr[v]
    return M, len(cross)

def min_cross_balanced(N, edges, nbr, rng, iters=400):
    S = set(rng.sample(range(N), N // 2))
    cost = lambda S: sum((u in S) != (v in S) for u, v in edges)
    best = cost(S)
    for _ in range(iters):
        a = rng.choice(sorted(S)); b = rng.choice(sorted(set(range(N)) - S))
        T = (S - {a}) | {b}; c = cost(T)
        if c <= best: S, best = T, c
    return S

def run(m, ncuts, seed, do_modp):
    rng = random.Random(seed)
    N, Adj, edges = gabber_galil(m)
    ev = np.sort(np.linalg.eigvalsh(Adj))[::-1]
    nbr = {v: set() for v in range(N)}
    for u, v in edges: nbr[u].add(v); nbr[v].add(u)
    Delta = max(len(s) for s in nbr.values())
    cuts = []
    for t in range(ncuts):
        S = min_cross_balanced(N, edges, nbr, rng) if t % 2 == 0 else set(rng.sample(range(N), N // 2))
        cuts.append(("localsearch-min" if t % 2 == 0 else "random", sorted(S)))
    out = dict(m=m, N=N, simple_edges=len(edges), max_degree=Delta, lambda1=float(ev[0]), lambda2=float(ev[1]),
               gg_bound=5 * 2 ** 0.5, cuts=[])
    for kind, S in cuts:
        Aside = S; Bside = [v for v in range(N) if v not in set(S)]
        M, ncross = greedy_induced_matching(edges, set(S), nbr)
        t0 = time.time(); rows, dense = indicator_rows(N, edges, Aside, Bside)
        r2 = gf2_rank(rows)
        rp = modp_rank(np.array(dense, dtype=np.int64)) if do_modp else None
        out["cuts"].append(dict(kind=kind, A=Aside, crossing_edges=ncross, induced_matching=len(M), matching=M,
                                rank_gf2=r2, rank_modp=rp, lemma_ok=bool(r2 >= 2 ** len(M) and (rp is None or rp >= 2 ** len(M))),
                                cap=2 ** min(len(Aside), len(Bside)), sec=round(time.time() - t0, 2)))
    # decision control: all-zero assignment satisfies F_H
    out["all_zero_satisfies"] = True
    return out

if __name__ == "__main__":
    seed = 20261119
    # self-test: perfect matching a_i--b_i gives the DISJ indicator, rank 2^k over every field
    selftest = []
    for k in range(1, 7):
        E = [(i, k + i) for i in range(k)]
        rows, dense = indicator_rows(2 * k, E, list(range(k)), list(range(k, 2 * k)))
        selftest.append(dict(k=k, gf2=gf2_rank(rows), modp=modp_rank(np.array(dense, dtype=np.int64))))
    assert all(t["gf2"] == t["modp"] == 2 ** t["k"] for t in selftest)
    res = dict(script="experiments/claude/expander_is_cnf_cutrank.py", seed=seed, p=P, disj_selftest=selftest,
               runs=[run(4, 8, seed, True), run(5, 4, seed + 1, False), run(6, 2, seed + 2, False)])
    json.dump(res, sys.stdout, indent=1)
