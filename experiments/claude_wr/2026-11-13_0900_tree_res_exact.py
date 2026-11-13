"""Exact minimum tree-like resolution refutation size (leaf count) via the
decision-tree characterisation: L(rho)=1 if rho falsifies a clause, else
min_x L(rho|x=0)+L(rho|x=1).  Min tree-like refutation has 2L-1 clauses.
Each invocation is one instance (keeps every run < ~30 s)."""
import sys, json, itertools, random, time
from functools import lru_cache

def min_leaves(n, clauses):
    # clause -> (mask of vars, bits that falsify)
    cl = []
    for c in clauses:
        m = f = 0
        for lit in c:
            v = abs(lit) - 1; m |= 1 << v
            if lit < 0: f |= 1 << v          # literal ~x false when x=1
        cl.append((m, f))
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def L(am, av):
        for m, f in cl:
            if m & am == m and av & m == f: return 1
        best = 1 << 60
        for v in range(n):
            b = 1 << v
            if am & b: continue
            s = L(am | b, av)
            if s >= best: continue
            s += L(am | b, av | b)
            if s < best: best = s
        return best
    r = L(0, 0); return r, L.cache_info().currsize

def php(m):  # m+1 pigeons, m holes; var p(i,j)
    var = lambda i, j: i * m + j + 1
    C = [[var(i, j) for j in range(m)] for i in range(m + 1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m + 1), 2):
            C.append([-var(a, j), -var(b, j)])
    return (m + 1) * m, C

def tseitin(edges, charge):
    n = len(edges); C = []
    for v in set(x for e in edges for x in e):
        inc = [k + 1 for k, e in enumerate(edges) if v in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge.get(v, 0):   # forbid assignments with wrong parity
                C.append([(-x if s else x) for x, s in zip(inc, signs)])
    return n, C

def rand3(n, m, seed):
    R = random.Random(seed)
    return n, [[R.choice([1, -1]) * v for v in R.sample(range(1, n + 1), 3)] for _ in range(m)]

def is_unsat(n, C):
    for a in range(1 << n):
        if all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in C): return False
    return True

if __name__ == "__main__":
    kind = sys.argv[1]; t = time.time()
    if kind == "php": n, C = php(int(sys.argv[2])); name = f"PHP^{int(sys.argv[2])+1}_{sys.argv[2]}"
    elif kind == "tseitinK4":
        n, C = tseitin([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)], {0: 1}); name = "Tseitin(K4,odd)"
    elif kind == "tseitinK33":
        n, C = tseitin([(a, b) for a in range(3) for b in range(3, 6)], {0: 1}); name = "Tseitin(K33,odd)"
    elif kind == "tseitinPetersen":
        E=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
        n, C = tseitin(E, {0: 1}); name = "Tseitin(Petersen,odd)"
    elif kind == "rand3max":
        nv, ratio, seeds = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
        best = None; cnt = 0
        for s in range(seeds):
            n, C = rand3(nv, int(ratio * nv), s)
            if not is_unsat(n, C): continue
            cnt += 1; L, _ = min_leaves(n, C)
            if best is None or L > best[0]: best = (L, s)
        print(json.dumps({"instance": f"rand3 n={nv} m={int(ratio*nv)}", "unsat_samples": cnt,
                          "max_min_leaves": best[0] if best else None, "argmax_seed": best[1] if best else None,
                          "secs": round(time.time() - t, 2)})); sys.exit()
    assert is_unsat(n, C) if n <= 16 else True
    L, st = min_leaves(n, C)
    print(json.dumps({"instance": name, "vars": n, "clauses": len(C), "min_leaves": L,
                      "min_tree_res_size": 2 * L - 1, "states": st, "secs": round(time.time() - t, 2)}))
