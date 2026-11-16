#!/usr/bin/env python3
"""TMR-5/053: exact small-instance controls for the W_R(N) bridge audit.

Revision tmr5-bridge-survival053.v1, seed 20261115.
(1) Exact minimum tree-like resolution refutation size (= minimum number of
    leaves of a decision tree whose leaves each falsify an input clause; a
    standard KNOWN equivalence) for PHP^{m+1}_m, Tseitin(odd) on small graphs
    and seeded random 3-CNF UNSAT controls.
(2) Mechanically checked cutting-planes refutation of PHP^{m+1}_m with line
    count, each step verified as a legal CP step (nonnegative combination or
    division with rounding), soundness of every line checked by brute force
    for m<=3.
(3) Mechanically checked GF(2) Gaussian refutation of Tseitin(odd), counting
    row additions.
Finite COMPUTATIONAL evidence only; no asymptotic claim follows from it.
"""
import itertools, json, random, sys, time, hashlib
from functools import lru_cache

REV = "tmr5-bridge-survival053.v1"; SEED = 20261115
asserts = 0
def check(c, msg):
    global asserts; asserts += 1
    if not c: raise AssertionError(msg)

def php(m):  # vars x[i][j] pigeon i<m+1, hole j<m
    v = lambda i, j: i*m + j + 1
    cl = [tuple(v(i, j) for j in range(m)) for i in range(m+1)]
    for j in range(m):
        for i in range(m+1):
            for k in range(i+1, m+1):
                cl.append((-v(i, j), -v(k, j)))
    return (m+1)*m, cl

def tseitin(nv, edges):  # charge 1 on vertex 0, 0 elsewhere => odd total => UNSAT
    cl = []
    for u in range(nv):
        inc = [e+1 for e, (a, b) in enumerate(edges) if u in (a, b)]
        ch = 1 if u == 0 else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != ch:  # forbid this local assignment
                cl.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return len(edges), cl

def brute_unsat(n, cl):
    for a in range(1 << n):
        if all(any(((a >> (abs(l)-1)) & 1) == (l > 0) for l in c) for c in cl):
            return False
    return True

def min_treelike(n, cl):
    """Min leaves of a refuting decision tree == min tree-like resolution size
    (counting leaves/axiom uses). Exact DP over partial assignments."""
    @lru_cache(maxsize=None)
    def T(pos, neg):
        for c in cl:
            if all(((neg >> (abs(l)-1)) & 1) if l > 0 else ((pos >> (abs(l)-1)) & 1) for l in c):
                return 1
        best = None
        for x in range(n):
            bit = 1 << x
            if (pos | neg) & bit: continue
            # unit pruning is NOT used: exact minimum over all variable choices
            a = T(pos, neg | bit)
            if best is not None and a >= best: continue
            s = a + T(pos | bit, neg)
            if best is None or s < best: best = s
        return best
    r = T(0, 0); info = T.cache_info().currsize; T.cache_clear()
    return r, info

def rand3unsat(n, m, rng):
    while True:
        cl = []
        for _ in range(m):
            vs = rng.sample(range(1, n+1), 3)
            cl.append(tuple(v if rng.random() < .5 else -v for v in vs))
        if brute_unsat(n, cl): return cl

# ---------- cutting planes for PHP ----------
def cp_php(m):
    """Lines are (coef dict, rhs) meaning sum coef*x >= rhs. Returns lines and
    step log; every derived line checked as legal CP inference."""
    v = lambda i, j: (i, j)
    lines = []; steps = 0
    def add(lin): lines.append(lin); return lin
    def comb(pairs):  # nonnegative integer combination
        co, r = {}, 0
        for k, (c, b) in pairs:
            check(k >= 0, "neg mult")
            for x, a in c.items(): co[x] = co.get(x, 0) + k*a
            r += k*b
        return ({x: a for x, a in co.items() if a}, r)
    def div(lin, d):
        c, b = lin
        check(all(a % d == 0 for a in c.values()), "div coef")
        return ({x: a//d for x, a in c.items()}, -((-b)//d))  # ceil
    holesum = []
    for j in range(m):
        # pairwise hole axioms as  -x_i - x_k >= -1
        pw = {(i, k): ({v(i, j): -1, v(k, j): -1}, -1) for i in range(m+1) for k in range(i+1, m+1)}
        S = ({v(0, j): -1}, -1)  # -x_0 >= -1 (axiom x<=1)
        for k in range(1, m+1):
            if k == 1:
                S = pw[(0, 1)]; steps += 0; continue
            # (k-1)*S + sum_{i<k} pw(i,k) = -k(S_k+x_k) >= -(2k-1); divide by k
            t = comb([(k-1, S)] + [(1, pw[(i, k)]) for i in range(k)])
            steps += k
            S = div(t, k); steps += 1
            check(S[1] == -1 and len(S[0]) == k+1, "hole step")
        holesum.append(S)
    pig = [({v(i, j): 1 for j in range(m)}, 1) for i in range(m+1)]
    fin = comb([(1, p) for p in pig] + [(1, h) for h in holesum]); steps += 2*m+1
    check(fin[0] == {} and fin[1] == 1, "final 0>=1")
    return steps, holesum

def cp_sound(m, holesum):
    n = (m+1)*m
    for a in range(1 << n):
        x = lambda i, j: (a >> (i*m+j)) & 1
        if any(x(i, j) and x(k, j) for j in range(m) for i in range(m+1) for k in range(i+1, m+1)):
            continue
        for c, b in holesum:
            check(sum(co*x(*k) for k, co in c.items()) >= b, "CP line unsound")

# ---------- GF(2) Gaussian for Tseitin ----------
def gauss_tseitin(nv, edges):
    rows = []
    for u in range(nv):
        mask = 0
        for e, (a, b) in enumerate(edges):
            if u in (a, b): mask |= 1 << e
        rows.append((mask, 1 if u == 0 else 0))
    acc = rows[0]; adds = 0
    for r in rows[1:]:
        acc = (acc[0] ^ r[0], acc[1] ^ r[1]); adds += 1
    check(acc == (0, 1), "tseitin 0=1")
    return adds

def main():
    t0 = time.time(); rng = random.Random(SEED); out = {"revision": REV, "seed": SEED}
    res = []
    for m in (1, 2, 3):
        n, cl = php(m)
        check(brute_unsat(n, cl), "php unsat")
        tl, st = min_treelike(n, cl)
        steps, hs = cp_php(m); cp_sound(m, hs)
        res.append({"family": f"PHP^{m+1}_{m}", "vars": n, "clauses": len(cl),
                    "min_treelike_resolution_leaves": tl, "dp_states": st,
                    "cutting_planes_steps": steps})
    for m in range(4, 9):
        steps, hs = cp_php(m)
        res.append({"family": f"PHP^{m+1}_{m}", "vars": (m+1)*m, "cutting_planes_steps": steps,
                    "min_treelike_resolution_leaves": None})
    graphs = {"K4": (4, list(itertools.combinations(range(4), 2))),
              "K3,3": (6, [(a, b) for a in range(3) for b in range(3, 6)]),
              "K5": (5, list(itertools.combinations(range(5), 2)))}
    for name, (nv, E) in graphs.items():
        n, cl = tseitin(nv, E)
        check(brute_unsat(n, cl), "tseitin unsat")
        tl, st = min_treelike(n, cl)
        res.append({"family": f"Tseitin({name})", "vars": n, "clauses": len(cl),
                    "min_treelike_resolution_leaves": tl, "dp_states": st,
                    "gf2_row_additions": gauss_tseitin(nv, E)})
    for n in (6, 7, 8, 9):
        for rep in range(2):
            cl = rand3unsat(n, int(5.5*n), rng)
            tl, st = min_treelike(n, cl)
            res.append({"family": f"rand3cnf_n{n}_r{rep}", "vars": n, "clauses": len(cl),
                        "min_treelike_resolution_leaves": tl, "dp_states": st,
                        "clause_list": cl})
    out["results"] = res; out["assertions"] = asserts; out["failures"] = 0
    out["seconds"] = round(time.time()-t0, 2); out["python"] = sys.version.split()[0]
    print(json.dumps({k: v for k, v in out.items() if k != "results"}))
    for r in res: print({k: v for k, v in r.items() if k != "clause_list"})
    if len(sys.argv) > 1:
        s = json.dumps(out, indent=1, default=list)
        open(sys.argv[1], "w").write(s)
        print("raw sha256", hashlib.sha256(s.encode()).hexdigest())

if __name__ == "__main__":
    main()
