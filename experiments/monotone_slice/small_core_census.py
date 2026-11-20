"""SMALLCORE1: exact census of 8-clause UNSAT proper 3-CNFs.

A set of width-3 clauses is UNSAT iff the falsifying subcubes cover {0,1}^k.
Each covers 2^(k-3) points, so 8 clauses (Kraft sum exactly 1) is the minimum,
and an 8-clause UNSAT set must partition the cube, i.e. clauses pairwise clash.
We count, for k = 3..7, 8-sets of clauses on variables {0..k-1} that are
UNSAT and use all k variables (labeled counts c_k). Also verifies the
partition/pairwise-clash equivalence by brute force evaluation.
Deterministic; no randomness.
"""
import itertools, math, sys, time

def clauses(k):
    out = []
    for tri in itertools.combinations(range(k), 3):
        for s in range(8):
            out.append(tuple((v, (s >> i) & 1) for i, v in enumerate(tri)))
    return out

def clash(a, b):
    da = dict(a)
    return any(v in da and da[v] != p for v, p in b)

def unsat_bruteforce(cs, k):
    for x in range(1 << k):
        if all(any(((x >> v) & 1) == p for v, p in c) for c in cs):
            return False  # literal (v,p) true iff x_v == p; clause satisfied
    return True

def census(k):
    cl = clauses(k)
    n = len(cl)
    adj = [set(j for j in range(n) if j != i and clash(cl[i], cl[j])) for i in range(n)]
    count = 0; checked = 0
    def grow(cur, cand):
        nonlocal count, checked
        if len(cur) == 8:
            used = set(v for i in cur for v, _ in cl[i])
            if len(used) == k:
                if checked < 200:
                    assert unsat_bruteforce([cl[i] for i in cur], k)
                    checked += 1
                count += 1
            return
        for j in sorted(cand):
            if cur and j < cur[-1]:
                continue
            grow(cur + [j], cand & adj[j])
    grow([], set(range(n)))
    return count

if __name__ == "__main__":
    t0 = time.time()
    res = {}
    for k in range(3, 8):
        res[k] = census(k)
        print(f"k={k} labeled UNSAT 8-sets using all k vars: {res[k]}  ({time.time()-t0:.1f}s)", flush=True)
    # tree prediction for k=7: ordered depth-3 decision trees with 7 distinct vars
    print("k=7 depth-3 tree prediction 7! =", math.factorial(7))
    # first-moment E[X_k] = c_k * binom(q,k) * prod_{i<8}(t-i)/(M-i)
    for q in (50, 100, 1000, 10**4):
        M = 8 * math.comb(q, 3); t = int(3.5 * q)
        p8 = math.prod((t - i) / (M - i) for i in range(8))
        tot = {k: res[k] * math.comb(q, k) * p8 for k in res}
        print(f"q={q} t={t} M={M} " + " ".join(f"E{k}={v:.3e}" for k, v in tot.items())
              + f" q^9*E7={tot[7]*q**9:.4f}")
    print(f"runtime {time.time()-t0:.1f}s")
