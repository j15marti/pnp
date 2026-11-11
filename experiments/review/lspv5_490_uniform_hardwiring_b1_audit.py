#!/usr/bin/env python3
"""LSPV-5/490 uniform-hardwiring B1 falsifier: finite control.

Checks, on small instances only (COMPUTATIONAL, not asymptotic evidence):
  1. A_hw (recognise the n-th PHP^{n+1}_n CNF syntactically, else brute force)
     is a total correct SAT/UNSAT decider on an exhaustive/random battery.
  2. Charged step count of A_hw on PHP_n versus the exact minimum tree-like
     Resolution size (= minimum falsified-clause decision-tree size, Lovasz et al.).
Runtime target: < 30 s (n <= 3 for exact tree-like DP).
"""
import itertools, json, random, sys, time
from functools import lru_cache

def php(n):
    """PHP^{n+1}_n: pigeons 0..n, holes 0..n-1; var p(i,j)=i*n+j+1."""
    v = lambda i, j: i * n + j + 1
    cls = [tuple(v(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for a in range(n + 1):
            for b in range(a + 1, n + 1):
                cls.append((-v(a, j), -v(b, j)))
    return tuple(tuple(sorted(c, key=abs)) for c in cls)

def encode(cnf):
    return ";".join(",".join(map(str, c)) for c in cnf)

class Counter:
    def __init__(self): self.steps = 0

def brute(cnf, ctr):
    vs = sorted({abs(l) for c in cnf for l in c})
    for bits in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, bits)); ok = True
        for c in cnf:
            ctr.steps += len(c)
            if not any(a[abs(l)] == (l > 0) for l in c):
                ok = False; break
        if ok: return "SAT"
    return "UNSAT"

def A_hw(cnf, ctr):
    """Total correct decider: hardwired recognition of PHP family, else brute force."""
    s = encode(cnf); ctr.steps += len(s)
    n = 1
    while True:
        t = encode(php(n)); ctr.steps += len(t)  # charged generation + compare
        if len(t) > len(s): break
        if t == s: return "UNSAT"
        n += 1
    return brute(cnf, ctr)

def min_tree_res(cnf):
    """Exact min tree-like Resolution size (#nodes) = min decision tree size
    for the falsified-clause search problem (leaves = clauses falsified)."""
    vs = sorted({abs(l) for c in cnf for l in c}); idx = {x: i for i, x in enumerate(vs)}
    cl = [[(idx[abs(l)], l > 0) for l in c] for c in cnf]
    m = len(vs)
    @lru_cache(maxsize=None)
    def size(st):  # st: tuple of 0/1/2 (2=unset)
        for c in cl:
            if all(st[i] != 2 and (st[i] == 1) != pos for i, pos in c):
                return 1
        best = None
        for i in range(m):
            if st[i] != 2: continue
            a = size(st[:i] + (0,) + st[i+1:])
            if best is not None and a >= best: continue
            b = size(st[:i] + (1,) + st[i+1:])
            t = a + b + 1
            if best is None or t < best: best = t
        return best
    return size(tuple([2] * m))

def main():
    t0 = time.time(); rows = []; checks = 0
    for n in (1, 2, 3):
        F = php(n); c = Counter(); ans = A_hw(F, c)
        assert ans == "UNSAT"; checks += 1
        assert brute(F, Counter()) == "UNSAT"; checks += 1
        rows.append({"n": n, "vars": n * (n + 1), "clauses": len(F),
                     "encoded_chars": len(encode(F)), "A_hw_steps": c.steps,
                     "min_tree_res_nodes": min_tree_res(F)})
    rnd = random.Random(490)
    for _ in range(3000):
        nv = rnd.randint(1, 6); k = rnd.randint(1, 14)
        F = tuple(tuple(sorted({rnd.choice((-1, 1)) * rnd.randint(1, nv) for _ in range(rnd.randint(1, 3))}, key=abs)) for _ in range(k))
        assert A_hw(F, Counter()) == brute(F, Counter()); checks += 1
    # hostile near-miss: drop one hole clause from PHP_2 -> still must be decided correctly
    F = php(2)[:-1]
    assert A_hw(F, Counter()) == brute(F, Counter()); checks += 1
    out = {"run": "LSPV5-490", "rows": rows, "assertions": checks,
           "seconds": round(time.time() - t0, 2),
           "note": "finite control only; asymptotic tree-like/DAG Resolution PHP lower bounds are KNOWN THEOREMS (Haken 1985, Buss-Pitassi 1998), not proved here"}
    json.dump(out, sys.stdout, indent=1); print()

if __name__ == "__main__":
    main()
