"""Exact audit of rank claims in the Google Doc 'P vs. NP Proof Attempts'
(Attempt IB and the Section 4 'Reciprocal Barrier' synthesis).

Claim audited (doc, Sec. 4): "the multilinear evaluation matrix of an
unsatisfiable or #P-hard constraint system across variable bipartitions
exhibits full rank 2^Omega(n)" and (Sec. 2.2) exact bond dimension along
any contraction order >= 2^Omega(tw).

All ranks are exact over GF(P), P = 2^31-1 (NOT over Q; GF(P) rank <= Q rank
for integer matrices; for 0/1 matrices of this size they agree w.h.p. but this
is not asserted). Deterministic seeds. Run: python3 -I doc_rank_claim_audit.py OUT.json
"""
import itertools, json, random, sys, time
import numpy as np

P = 2147483647
N = 16
HALF = N // 2

def rank_mod_p(M):
    A = (np.array(M, dtype=np.int64) % P).copy()
    r = 0
    rows, cols = A.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] != 0:
                piv = i; break
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), P - 2, P)
        A[r] = (A[r] * inv) % P
        nz = np.nonzero(A[:, c])[0]
        for i in nz:
            if i != r:
                A[i] = (A[i] - A[i, c] * A[r]) % P
        r += 1
        if r == rows:
            break
    return r

ASSIGN = np.array(list(itertools.product([0, 1], repeat=N)), dtype=np.int8)  # row index = x as big-endian int

def falsified(clauses):
    """bool array [2^N, m]: clause j falsified by x."""
    out = np.zeros((len(ASSIGN), len(clauses)), dtype=bool)
    for j, cl in enumerate(clauses):
        f = np.ones(len(ASSIGN), dtype=bool)
        for lit in cl:
            v = abs(lit) - 1
            f &= (ASSIGN[:, v] == (0 if lit > 0 else 1))
        out[:, j] = f
    return out

def cut_matrix(vec):
    # left = first HALF variables (high bits), right = last HALF
    return np.asarray(vec).reshape(2 ** HALF, 2 ** HALF)

def rand3cnf(rng, m):
    cls = []
    for _ in range(m):
        vs = rng.sample(range(1, N + 1), 3)
        cls.append([v if rng.random() < 0.5 else -v for v in vs])
    return cls

def inv_mod(vals):
    return np.array([pow(int(v) % P, P - 2, P) for v in vals], dtype=np.int64)

def main(out):
    t0 = time.time()
    res = {"P": P, "N": N, "cut": [HALF, HALF], "experiments": {}}
    # A: random 3-CNF near threshold
    m = round(4.26 * N)
    A = []
    unsat_example = None
    for seed in range(12):
        rng = random.Random(seed)
        cls = rand3cnf(rng, m)
        F = falsified(cls)
        sat = ~F.any(axis=1)
        r = rank_mod_p(cut_matrix(sat.astype(np.int64)))
        A.append({"seed": seed, "m": m, "num_solutions": int(sat.sum()), "cut_rank_solution_indicator": r})
        if sat.sum() == 0 and unsat_example is None:
            unsat_example = (seed, cls, F)
    res["experiments"]["A_random3cnf_solution_indicator"] = A
    # B: unique-solution family (planted a*, all 3-clauses satisfied by a*, plus units forcing)
    rng = random.Random(1001)
    astar = [rng.randint(0, 1) for _ in range(N)]
    cls = []
    while len(cls) < m:
        c = rand3cnf(rng, 1)[0]
        if any((l > 0) == bool(astar[abs(l) - 1]) for l in c):
            cls.append(c)
    cls += [[(i + 1) if astar[i] else -(i + 1)] for i in range(N)]
    sat = ~falsified(cls).any(axis=1)
    res["experiments"]["B_unique_solution"] = {"num_solutions": int(sat.sum()),
        "cut_rank": rank_mod_p(cut_matrix(sat.astype(np.int64)))}
    # C: easy-family controls with FULL cut rank
    eq2 = []
    for i in range(HALF):
        a, b = i + 1, i + 1 + HALF
        eq2 += [[a, -b], [-a, b]]
    sat = ~falsified(eq2).any(axis=1)
    res["experiments"]["C_2SAT_equality_matching"] = {"class": "2-SAT/affine (in P)",
        "num_solutions": int(sat.sum()), "cut_rank": rank_mod_p(cut_matrix(sat.astype(np.int64))),
        "max_possible": 2 ** HALF}
    # C2: count tensor (all-ones = no constraints, trivial) rank 1 -> rank is not monotone in hardness
    # D: linear-IPS functional 1/f on an UNSAT random 3-CNF, two aggregation weightings
    if unsat_example is not None:
        seed, cls, F = unsat_example
        cnt = F.sum(axis=1).astype(np.int64)  # >=1 everywhere
        w = np.array([pow(2, j, P) for j in range(len(cls))], dtype=np.int64)
        fw = (F.astype(np.int64) * w).sum(axis=1) % P  # nonzero mod P? check
        D = {"seed": seed, "min_falsified": int(cnt.min())}
        D["rank_inv_count"] = rank_mod_p(cut_matrix(inv_mod(cnt)))
        if (fw != 0).all():
            D["rank_inv_binary_weighted"] = rank_mod_p(cut_matrix(inv_mod(fw)))
        # canonical first-falsified-clause certificate: g_j = [j first falsified]
        first = F.argmax(axis=1)
        ranks = []
        for j in range(len(cls)):
            ind = (first == j).astype(np.int64)
            if ind.any():
                ranks.append(rank_mod_p(cut_matrix(ind)))
        D["first_falsified_certificate"] = {"clauses_used": len(ranks), "sum_cut_ranks": sum(ranks), "max_cut_rank": max(ranks)}
        # greedy single-clause certificate using a better clause order (sort by #vars on one side): rank still order-dependent
        res["experiments"]["D_linear_IPS_functional"] = D
    res["seconds"] = round(time.time() - t0, 2)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
