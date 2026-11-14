"""Exact minimum tree-like resolution refutation size (= minimum DPLL/decision-tree
leaves+internal nodes, Beame-Pitassi equivalence) for tiny UNSAT families, plus a
hostile control: F2 Gaussian-elimination row-operation count for Tseitin.
Each family is bounded so the whole script runs in well under 30 s."""
import itertools, json, sys, time
from functools import lru_cache
sys.setrecursionlimit(10000)

def simplify(clauses, var, val):
    lit = var if val else -var
    out = []
    for c in clauses:
        if lit in c: continue
        out.append(tuple(l for l in c if l != -lit))
    return tuple(sorted(set(out)))

def min_tree(clauses):
    @lru_cache(maxsize=None)
    def S(F):
        if () in F: return 1           # leaf: some clause falsified
        vs = sorted({abs(l) for c in F for l in c})
        best = None
        for v in vs:
            s = 1 + S(simplify(F, v, 0)) + S(simplify(F, v, 1))
            if best is None or s < best: best = s
        return best
    r = S(tuple(sorted(set(tuple(sorted(c)) for c in clauses))))
    return r, S.cache_info().currsize

def php(n):  # n+1 pigeons, n holes
    var = lambda p, h: p * n + h + 1
    cl = [tuple(var(p, h) for h in range(n)) for p in range(n + 1)]
    for h in range(n):
        for p, q in itertools.combinations(range(n + 1), 2):
            cl.append((-var(p, h), -var(q, h)))
    return cl

def tseitin_cycle_chords(nv):  # 3-regular circulant (Moebius ladder), odd charge
    edges = [(i, (i + 1) % nv) for i in range(nv)] + [(i, i + nv // 2) for i in range(nv // 2)]
    inc = {v: [] for v in range(nv)}
    for e, (a, b) in enumerate(edges):
        inc[a].append(e + 1); inc[b].append(e + 1)
    cl = []
    for v in range(nv):
        charge = 1 if v == 0 else 0
        es = inc[v]
        for signs in itertools.product([0, 1], repeat=len(es)):
            if sum(signs) % 2 != charge:  # forbid assignments with wrong parity
                cl.append(tuple(e if s == 0 else -e for e, s in zip(es, signs)))
    return cl, edges, inc

def gauss_ops(nv, edges, inc):
    rows = []
    for v in range(nv):
        m = 0
        for e in inc[v]: m |= 1 << e
        rows.append((m, 1 if v == 0 else 0))
    ops = 0; piv = {}
    for m, b in rows:
        while m:
            hb = m.bit_length() - 1
            if hb in piv:
                pm, pb = piv[hb]; m ^= pm; b ^= pb; ops += 1
            else:
                piv[hb] = (m, b); break
        if m == 0 and b == 1:
            return ops, True
    return ops, False

res = {"php": [], "tseitin": []}
t0 = time.time()
for n in range(1, 4):
    s, states = min_tree(php(n))
    res["php"].append({"holes": n, "vars": n * (n + 1), "min_tree_size": s, "memo_states": states})
for nv in (4, 6, 8):
    cl, edges, inc = tseitin_cycle_chords(nv)
    s, states = min_tree(cl)
    ops, refuted = gauss_ops(nv, edges, inc)
    res["tseitin"].append({"vertices": nv, "vars": len(edges), "clauses": len(cl), "min_tree_size": s,
                           "memo_states": states, "gauss_row_ops": ops, "gauss_refutes": refuted})
res["seconds"] = round(time.time() - t0, 2)
print(json.dumps(res, indent=1))
json.dump(res, open("wr_tree_exact_results.json", "w"), indent=1)
