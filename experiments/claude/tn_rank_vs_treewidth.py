"""Falsifier for a graph-only claim: 'exact tensor-network bond dimension for 3-SAT
is lower-bounded by 2^Omega(tw(G))' (Google Doc 'Dual Proof Attempts', Attempt IB).

For each instance: exact primal-graph treewidth (O(2^n n) subset DP), and the rank of the
solution indicator f matricized across balanced variable cuts, over GF(2) and mod a 61-bit
prime (rank_p <= rank_Q; a Fraction-exact rank is computed for one cut as confirmation).
Pure Python, deterministic seeds. Usage: python3 -I tn_rank_vs_treewidth.py OUT.json
"""
import itertools, json, random, sys, time
from fractions import Fraction

P = (1 << 61) - 1

def exact_treewidth(n, adj):
    # Bodlaender et al. DP: TW(S) = min_{v in S} max(TW(S-v), |Q(S-v, v)|)
    full = (1 << n) - 1
    def qsize(S, v):
        seen = 1 << v; stack = [v]; out = 0
        while stack:
            u = stack.pop()
            for w in adj[u]:
                b = 1 << w
                if seen & b: continue
                seen |= b
                if S & b: stack.append(w)
                else: out += 1
        return out
    TW = {0: -1}
    for size in range(1, n + 1):
        for comb in itertools.combinations(range(n), size):
            S = 0
            for c in comb: S |= 1 << c
            best = n
            for v in comb:
                R = S & ~(1 << v)
                t = max(TW[R], qsize(R, v))
                if t < best: best = t
            TW[S] = best
        # free memory of size-2 layers
        if size >= 2:
            for comb in itertools.combinations(range(n), size - 2):
                S = 0
                for c in comb: S |= 1 << c
                TW.pop(S, None)
    return TW[full]

def sat_table(n, clauses):
    tab = []
    for a in range(1 << n):
        ok = True
        for cl in clauses:
            if not any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in cl):
                ok = False; break
        tab.append(1 if ok else 0)
    return tab

def matrix(n, tab, A):
    B = [i for i in range(n) if i not in A]
    M = [[0] * (1 << len(B)) for _ in range(1 << len(A))]
    for a in range(1 << n):
        if tab[a]:
            r = sum(((a >> v) & 1) << k for k, v in enumerate(A))
            c = sum(((a >> v) & 1) << k for k, v in enumerate(B))
            M[r][c] = 1
    return M

def rank_mod(M, p):
    M = [row[:] for row in M]; r = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p) if p > 2 else 1
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        r += 1
    return r

def rank_Q(M):
    M = [[Fraction(x) for x in row] for row in M]; r = 0
    for c in range(len(M[0])):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r

def primal_adj(n, clauses):
    adj = [set() for _ in range(n)]
    for cl in clauses:
        vs = [abs(l) - 1 for l in cl]
        for u in vs:
            for w in vs:
                if u != w: adj[u].add(w)
    return adj

def random_3cnf(n, m, rng):
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        out.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return out

def main(path):
    t0 = time.time(); n = 14
    rng = random.Random(20261119)
    base = random_3cnf(n, 42, rng)          # ratio 3.0 core, used for all variants
    forced = [tuple(abs(l) for l in cl) for cl in base] + [(v,) for v in range(1, n + 1)]
    xor3 = []                               # parity x_a+x_b+x_c=1 as 4 clauses each
    for cl in base[:10]:
        a, b, c = (abs(l) for l in cl)
        # forbid each even-parity assignment of (a,b,c) with one clause
        for bits in itertools.product([0, 1], repeat=3):
            if sum(bits) % 2 == 0:
                xor3.append(tuple((v if bit == 0 else -v) for v, bit in zip((a, b, c), bits)))
    instances = {
        "random3cnf_ratio3_seed20261119": base,
        "monotone_core_plus_all_units_FORCED_POINT": forced,
        "xor3_parity_first10_triples": xor3,
        "random3cnf_ratio4.6_seed20261119": base + random_3cnf(n, 22, rng),
    }
    cut_rng = random.Random(7)
    cuts = [list(range(7))] + [sorted(cut_rng.sample(range(n), 7)) for _ in range(5)]
    rows = []
    for name, cls in instances.items():
        adj = primal_adj(n, cls)
        tw = exact_treewidth(n, adj)
        tab = sat_table(n, cls)
        res = {"name": name, "n": n, "clauses": len(cls), "models": sum(tab),
               "exact_primal_treewidth": tw, "cuts": []}
        for i, A in enumerate(cuts):
            M = matrix(n, tab, A)
            e = {"A": A, "rank_GF2": rank_mod(M, 2), "rank_mod_2^61-1": rank_mod(M, P),
                 "cut_cap": 2 ** 7}
            if i == 0: e["rank_Q_exact"] = rank_Q(M)
            res["cuts"].append(e)
        rows.append(res)
        print(name, "tw", tw, "models", sum(tab),
              [(c["rank_GF2"], c["rank_mod_2^61-1"]) for c in res["cuts"]], flush=True)
    out = {"script": "experiments/claude/tn_rank_vs_treewidth.py", "seed": 20261119,
           "cut_seed": 7, "instances": {k: v for k, v in instances.items()},
           "results": rows, "elapsed_s": round(time.time() - t0, 2)}
    json.dump(out, open(path, "w"), indent=1)
    print("elapsed", out["elapsed_s"])

if __name__ == "__main__":
    main(sys.argv[1])
