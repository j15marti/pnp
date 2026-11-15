"""TMR-5/051 independent red-team replay of CLAUDE WBAR-0001 (branch ccr-1695bd63-ps9gxt, 8a43e284).
Independent code (not imported from WBAR). Deterministic; no seed.
Stage T: exact minimum tree-like resolution size (with weakening) by recursion on residual
         clause sets: T(G)=1 if empty clause in G else min_x 1+T(G|x=0)+T(G|x=1).
         Memoized on the residual clause SET (not on the restriction), an independent method.
Stage D: explicit shared-DAG (general) resolution refutations by Davis-Putnam variable
         elimination over all/greedy orders; every resolvent is re-verified as a sound
         resolution step from two earlier lines; count of distinct lines = DAG size.
Stage G: Gaussian elimination over F2 with explicit linear-combination certificate.
Usage: python3 -I tmr5_wbar_dag_audit051.py OUT.json [graphs...]"""
import sys, json, time, itertools
from functools import lru_cache

GRAPHS = {
  "K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
  "prism": [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
  "K33": [(a,b) for a in range(3) for b in range(3,6)],
  "cube": [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)],
  "petersen": [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)],
}

def tseitin(E, odd=0):
    V = sorted({v for e in E for v in e}); cl = []
    for v in V:
        inc = [i for i,e in enumerate(E) if v in e]
        ch = 1 if v == odd else 0
        for bits in itertools.product((0,1), repeat=len(inc)):
            if sum(bits) % 2 != ch:  # clause forbidding this local assignment; literal +i / -i (1-based)
                cl.append(frozenset((-(i+1) if b else (i+1)) for i,b in zip(inc,bits)))
    return V, cl

def restrict(G, lit):
    out = set()
    for c in G:
        if lit in c: continue
        out.add(c - {-lit})
    return frozenset(out)

def tree_size(F):
    @lru_cache(maxsize=None)
    def T(G):
        if frozenset() in G: return 1
        vs = sorted({abs(l) for c in G for l in c})
        best = None
        for x in vs:
            a = T(restrict(G, x))
            if best is not None and 1 + a + 1 >= best: continue
            s = 1 + a + T(restrict(G, -x))
            if best is None or s < best: best = s
        return best
    r = T(frozenset(F)); return r, T.cache_info().currsize

def dp_refute(F, order):
    """Davis-Putnam elimination; returns list of lines (clause, premises) forming a DAG refutation."""
    lines = []; idx = {}
    def add(c, prem):
        if c in idx: return idx[c]
        idx[c] = len(lines); lines.append((c, prem)); return idx[c]
    for c in F: add(c, None)
    active = set(F)
    for x in order:
        P = [c for c in active if x in c]; N = [c for c in active if -x in c]
        active -= set(P) | set(N)
        for p in P:
            for n in N:
                r = (p - {x}) | (n - {-x})
                if any(-l in r for l in r): continue  # tautology, skip
                if any(a <= r for a in active): continue  # subsumed by an active clause
                add(r, (idx[p], idx[n], x)); active.add(r)
                if not r: return lines
        # remove subsumed
        act = sorted(active, key=len); keep = []
        for c in act:
            if not any(k <= c for k in keep): keep.append(c)
        active = set(keep)
    return lines

def verify(F, lines):
    Fs = set(F)
    for c, prem in lines:
        if prem is None:
            assert c in Fs
        else:
            i, j, x = prem
            p, n = lines[i][0], lines[j][0]
            assert i < len(lines) and j < len(lines) and x in p and -x in n
            assert c == (p - {x}) | (n - {-x})
    assert lines[-1][0] == frozenset()
    # count only lines used by the empty clause (pruned DAG size)
    used = set(); st = [len(lines)-1]
    while st:
        k = st.pop()
        if k in used: continue
        used.add(k); pr = lines[k][1]
        if pr: st += [pr[0], pr[1]]
    return len(used), sum(1 for k in used if lines[k][1] is None)

def gauss(V, E, odd=0):
    rows = [[sum(1<<i for i,e in enumerate(E) if v in e), 1 if v==odd else 0, 1<<k] for k,v in enumerate(V)]
    ops = 0; piv = 0
    for col in range(len(E)):
        p = next((i for i in range(piv,len(rows)) if rows[i][0]>>col & 1), None)
        if p is None: continue
        rows[piv], rows[p] = rows[p], rows[piv]
        for i in range(len(rows)):
            if i != piv and rows[i][0]>>col & 1:
                for t in range(3): rows[i][t] ^= rows[piv][t]
                ops += 1
        piv += 1
    bad = [r for r in rows if r[0]==0 and r[1]==1]
    # certificate check: the recorded vertex combination sums to 0 = 1
    comb = bad[0][2]; s = 0; ch = 0
    for k,v in enumerate(V):
        if comb>>k & 1:
            s ^= sum(1<<i for i,e in enumerate(E) if v in e); ch ^= (1 if v==odd else 0)
    assert s == 0 and ch == 1
    return ops, bin(comb).count("1")

if __name__ == "__main__":
    out_path = sys.argv[1]; names = sys.argv[2:] or ["K4","prism","K33","cube"]
    out = {"revision": "tmr5-wbar-dag-audit051.v1", "seed": None, "graphs": {}}
    for g in names:
        E = GRAPHS[g]; V, F = tseitin(E); t0 = time.time(); rec = {"vertices": len(V), "vars": len(E), "clauses": len(F)}
        if len(E) <= 12:
            rec["min_tree_res_size"], rec["tree_memo_states"] = tree_size(F)
        n = len(E); orders = list(itertools.permutations(range(1,n+1))) if n <= 6 else None
        best = None; tried = 0
        cand = orders if orders else [tuple(range(1,n+1))]
        if not orders:  # deterministic greedy min-degree-product orders from every start
            for s in range(1, n+1):
                o = [s]; rem = set(range(1,n+1)) - {s}; Fc = list(F)
                while rem:
                    o.append(min(rem, key=lambda x: (sum(1 for c in F if x in c)*sum(1 for c in F if -x in c), x))); rem.discard(o[-1])
                cand.append(tuple(o))
            # also edge orders along vertex BFS
        for o in cand:
            L = dp_refute(F, o); tried += 1
            if L[-1][0] != frozenset(): continue
            size, ax = verify(F, L)
            if best is None or size < best[0]: best = (size, ax, list(o))
        rec.update(dp_dag_size=best[0], dp_dag_axioms=best[1], dp_best_order=best[2], dp_orders_tried=tried,
                   dp_exhaustive=bool(orders))
        rec["gauss_row_ops"], rec["gauss_cert_vertices"] = gauss(V, E)
        rec["seconds"] = round(time.time()-t0, 2); out["graphs"][g] = rec; print(g, rec, flush=True)
    json.dump(out, open(out_path, "w"), indent=1)
