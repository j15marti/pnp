"""Exact minimum tree-like resolution refutation size (number of nodes in the
decision tree = 2*leaves-1) versus a fixed DPLL heuristic, for tiny UNSAT CNFs.
Illustrates W_R(F) = min_pi cost_R(pi) with the best strategy chosen for free.
Usage: python3 tree_res_minsize.py FAMILY PARAM OUTJSON   (each call < 30 s)
FAMILY in {php, rand3}. Deterministic seeds."""
import sys, json, random, itertools, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j) = i*m+j+1
    v = lambda i, j: i*m + j + 1
    cl = [tuple(v(i, j) for j in range(m)) for i in range(m+1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m+1), 2):
            cl.append((-v(a, j), -v(b, j)))
    return (m+1)*m, cl

def sat(n, cl):
    for bits in range(1 << n):
        if all(any((l > 0) == bool(bits >> (abs(l)-1) & 1) for l in c) for c in cl):
            return True
    return False

def rand3(n, seed, ratio=6.0):
    rng = random.Random(seed)
    while True:
        cl = [tuple(rng.choice([1, -1])*x for x in rng.sample(range(1, n+1), 3))
              for _ in range(int(ratio*n))]
        if not sat(n, cl):
            return n, cl
        seed += 1000; rng = random.Random(seed)

def restrict(cl, lit):
    out = []
    for c in cl:
        if lit in c: continue
        out.append(tuple(l for l in c if l != -lit))
    return tuple(sorted(set(out)))

def min_tree(n, cl):
    @lru_cache(maxsize=None)
    def best(F):
        if () in F: return 1
        vs = sorted({abs(l) for c in F for l in c})
        return 1 + min(best(restrict(F, x)) + best(restrict(F, -x)) for x in vs)
    r = best(tuple(sorted(set(cl)))); return r, best.cache_info().currsize

def dpll_fixed(n, cl):  # branch on smallest-index variable, no unit propagation
    def go(F):
        if () in F: return 1
        x = min(abs(l) for c in F for l in c)
        return 1 + go(restrict(F, x)) + go(restrict(F, -x))
    return go(tuple(sorted(set(cl))))

if __name__ == "__main__":
    fam, p, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    t = time.time(); rows = []
    insts = [php(p)] if fam == "php" else [rand3(p, s) for s in range(3)]
    for k, (n, cl) in enumerate(insts):
        opt, states = min_tree(n, cl)
        rows.append(dict(family=fam, param=p, inst=k, n=n, m=len(cl),
                         min_tree_nodes=opt, fixed_order_dpll_nodes=dpll_fixed(n, cl),
                         memo_states=states))
    json.dump(dict(rows=rows, seconds=round(time.time()-t, 2)), open(out, "w"), indent=1)
    print(json.dumps(rows))
