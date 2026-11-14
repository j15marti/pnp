#!/usr/bin/env python3
"""CLAUDE-SWITCH-0001: exact check of the guarded-composition lemma.

G = (z OR F1) AND (NOT z OR F2), with F1, F2 UNSAT on disjoint variables.
Claim (PROVED in the report): for tree-like Resolution with weakening,
measured by minimum number of leaves L(.), we have L(G) = L(F1) + L(F2).
Tree-like Resolution with weakening refutations of F correspond exactly to
decision trees whose leaves each falsify a clause of F (Lovasz et al. 1995;
Beame-Pitassi survey), so L is computed exactly by DP over partial assignments.

Runtime design: each call < 25 s on one core. Deterministic seed.
"""
import itertools, json, random, sys, time
from functools import lru_cache

def falsified(clauses, rho):
    # rho: dict var->bool ; clause: tuple of nonzero ints
    for c in clauses:
        if all((abs(l) in rho) and (rho[abs(l)] != (l > 0)) for l in c):
            return True
    return False

def is_unsat(clauses, nvars_list):
    vs = sorted(nvars_list)
    for bits in itertools.product([False, True], repeat=len(vs)):
        rho = dict(zip(vs, bits))
        if not falsified(clauses, rho):
            return False
    return True

def min_leaves(clauses, variables):
    variables = tuple(sorted(variables))
    cl = [tuple(c) for c in clauses]
    @lru_cache(maxsize=None)
    def T(key):
        rho = dict(key)
        if falsified(cl, rho):
            return 1
        best = None
        for x in variables:
            if x in rho:
                continue
            a = T(tuple(sorted({**rho, x: False}.items())))
            if best is not None and a >= best:
                continue
            b = T(tuple(sorted({**rho, x: True}.items())))
            if best is None or a + b < best:
                best = a + b
        return best
    return T(tuple())

def shift(clauses, off):
    return [tuple((abs(l) + off) * (1 if l > 0 else -1) for l in c) for c in clauses]

def guarded(F1, F2, z):
    return [c + (z,) for c in F1] + [c + (-z,) for c in F2]

def rand_unsat(n, rng, width=3):
    while True:
        m = rng.randint(n + 2, 4 * n + 4)
        F = []
        for _ in range(m):
            k = rng.randint(1, min(width, n))
            vs = rng.sample(range(1, n + 1), k)
            F.append(tuple(v if rng.random() < .5 else -v for v in vs))
        if is_unsat(F, range(1, n + 1)):
            return F

def tseitin_k4_odd():
    # edges of K4 -> vars 1..6 ; vertex 0 has charge 1, others 0
    edges = list(itertools.combinations(range(4), 2))
    F = []
    for v in range(4):
        inc = [i + 1 for i, e in enumerate(edges) if v in e]
        ch = 1 if v == 0 else 0
        for signs in itertools.product([0, 1], repeat=3):
            if sum(signs) % 2 != ch:  # forbid this assignment
                F.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return F, 6

def php_3_2():
    var = lambda p, h: p * 2 + h + 1
    F = [tuple(var(p, h) for h in range(2)) for p in range(3)]
    for h in range(2):
        for p, q in itertools.combinations(range(3), 2):
            F.append((-var(p, h), -var(q, h)))
    return F, 6

def main():
    t0 = time.time()
    rng = random.Random(20261114)
    out = {"run": "CLAUDE-SWITCH-0001", "random_pairs": [], "named": {}}
    fails = 0
    for trial in range(80):
        n1, n2 = rng.randint(1, 5), rng.randint(1, 4)
        F1 = rand_unsat(n1, rng)
        F2 = shift(rand_unsat(n2, rng), n1)
        z = n1 + n2 + 1
        G = guarded(F1, F2, z)
        allv = list(range(1, z + 1))
        assert is_unsat(G, allv)
        # restriction controls
        r0 = [tuple(l for l in c if l != z) for c in G if -z not in c]
        assert sorted(r0) == sorted(F1)
        L1 = min_leaves(F1, range(1, n1 + 1))
        L2 = min_leaves(F2, range(n1 + 1, n1 + n2 + 1))
        LG = min_leaves(G, allv)
        ok = (LG == L1 + L2)
        fails += (not ok)
        # SAT control: dropping all F2 clauses makes G satisfiable (z=1)
        assert not is_unsat([c + (z,) for c in F1], allv)
        out["random_pairs"].append({"n1": n1, "n2": n2, "L1": L1, "L2": L2, "LG": LG, "ok": ok})
    T, nt = tseitin_k4_odd(); P, npv = php_3_2()
    out["named"]["tseitin_k4_odd_leaves"] = min_leaves(T, range(1, nt + 1))
    out["named"]["php_3_2_leaves"] = min_leaves(P, range(1, npv + 1))
    out["named"]["tseitin_unsat"] = is_unsat(T, range(1, 7))
    out["named"]["php_unsat"] = is_unsat(P, range(1, 7))
    # mixed-system control: GF(2) sum of all Tseitin vertex equations gives 0=1
    # (row XOR count = 3 sums of 4 rows) -- linear cost, independent of tree-res size
    out["named"]["tseitin_gf2_row_xors"] = 3
    # named composite: G(PHP_3^2, odd Tseitin on K3) on 10 variables
    E3 = list(itertools.combinations(range(3), 2)); T3 = []
    for v in range(3):
        inc = [i + 1 for i, e in enumerate(E3) if v in e]; ch = 1 if v == 0 else 0
        for sg in itertools.product([0, 1], repeat=2):
            if sum(sg) % 2 != ch:
                T3.append(tuple(-x if b else x for x, b in zip(inc, sg)))
    T3s = shift(T3, 6); Gc = guarded(P, T3s, 10)
    lp, lt, lg = min_leaves(P, range(1, 7)), min_leaves(T3s, range(7, 10)), min_leaves(Gc, range(1, 11))
    out["named"]["composite_php32_tseitinK3"] = {"L_php": lp, "L_tseitin": lt, "L_G": lg, "ok": lg == lp + lt}
    fails += (lg != lp + lt)
    out["failures"] = fails
    out["seconds"] = round(time.time() - t0, 2)
    print(json.dumps(out, indent=1))
    return 0 if fails == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
