"""Worst-case derivation cost probe (COMPUTATIONAL, illustrative).
Fixed reduction system R_DP: Davis-Putnam variable elimination on a clause
hypergraph (signed incidences), with tautology + subsumption removal.
cost(order) = total clauses produced; we minimise over elimination orders
via subset DP (free optimal sequence, search NOT charged).  Caveat: with
subsumption the reached clause set may depend on order; the subset DP keeps
the argmin-path state, so the value is an UPPER bound on min over orders.
Control: GF(2) Gaussian elimination on the same Tseitin system (row ops).
Each instance runs well under 30 s; instances are independent chunks."""
import itertools, json, sys, time

def tseitin(edges, nv):
    var = {e: i for i, e in enumerate(edges)}
    clauses = []
    for v in range(nv):
        inc = [var[e] for e in edges if v in e]
        charge = 1 if v == 0 else 0          # total charge odd -> UNSAT
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge:      # forbid assignments with wrong parity
                clauses.append(frozenset((x + 1) * (1 if s == 0 else -1) for x, s in zip(inc, signs)))
    return len(edges), clauses

def reduce_set(cls):
    cls = sorted(set(cls), key=len)
    out = []
    for c in cls:
        if not any(d <= c for d in out):
            out.append(c)
    return frozenset(out)

def elim(cls, x):
    pos = [c for c in cls if x in c]; neg = [c for c in cls if -x in c]
    rest = [c for c in cls if x not in c and -x not in c]
    new = []
    for p in pos:
        for q in neg:
            r = (p - {x}) | (q - {-x})
            if not any(-l in r for l in r):
                new.append(r)
    return reduce_set(rest + new), len(new)

def min_dp_cost(n, clauses, cap=200000):
    full = (1 << n) - 1
    best = {0: (0, reduce_set(clauses))}
    for mask in range(1, full + 1):
        cand = None
        for x in range(n):
            if mask >> x & 1:
                pm = mask ^ (1 << x)
                if pm not in best: continue
                c0, st = best[pm]
                st2, produced = elim(st, x + 1)
                tot = c0 + produced
                if tot > cap: continue
                if cand is None or tot < cand[0]:
                    cand = (tot, st2)
        if cand: best[mask] = cand
    if full not in best: return None
    tot, st = best[full]
    assert frozenset() in st or frozenset([frozenset()]) == st, "should derive empty clause"
    return tot

def gf2_ops(edges, nv):
    rows = []
    for v in range(nv):
        r = 0
        for i, e in enumerate(edges):
            if v in e: r |= 1 << i
        rows.append((r, 1 if v == 0 else 0))
    ops = 0; piv = 0; n = len(edges)
    for col in range(n):
        k = next((i for i in range(piv, len(rows)) if rows[i][0] >> col & 1), None)
        if k is None: continue
        rows[piv], rows[k] = rows[k], rows[piv]
        for i in range(len(rows)):
            if i != piv and rows[i][0] >> col & 1:
                rows[i] = (rows[i][0] ^ rows[piv][0], rows[i][1] ^ rows[piv][1]); ops += 1
        piv += 1
    assert any(r == 0 and b == 1 for r, b in rows)
    return ops

def graphs():
    G = {}
    for k in (4, 6, 8, 10): G[f"cycle{k}"] = ([(i, (i + 1) % k) for i in range(k)], k)
    G["K4"] = (list(itertools.combinations(range(4), 2)), 4)
    G["K33"] = ([(a, b) for a in range(3) for b in range(3, 6)], 6)
    G["prism3"] = ([(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)], 6)
    G["cube3"] = ([(a, a ^ (1 << i)) for a in range(8) for i in range(3) if a < a ^ (1 << i)], 8)
    G["wagner8"] = ([(i, (i + 1) % 8) for i in range(8)] + [(i, i + 4) for i in range(4)], 8)
    out = [(i, (i + 1) % 5) for i in range(5)]; inn = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    G["petersen"] = (out + inn + [(i, i + 5) for i in range(5)], 10)
    return G

if __name__ == "__main__":
    name = sys.argv[1]
    edges, nv = graphs()[name]
    n, cls = tseitin(edges, nv)
    t = time.time(); c = min_dp_cost(n, cls); dt = time.time() - t
    print(json.dumps({"graph": name, "vars": n, "clauses": len(cls), "min_dp_cost_ub": c,
                      "gf2_row_ops": gf2_ops(edges, nv), "seconds": round(dt, 2)}))
