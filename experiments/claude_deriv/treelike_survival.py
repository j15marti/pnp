"""Exact minimum tree-like Resolution(+weakening) refutation size via the
decision-tree characterization, versus GF(2) elimination cost, on small
canonical UNSAT families. One instance per invocation (<30 s each).
Usage: python treelike_survival.py <instance-name>   (or 'list')
Free choice of the optimal branching sequence is granted (exact min over all
query orders); search cost is NOT charged -- this is the user's W_R regime."""
import sys, json, itertools, random, time
from functools import lru_cache

def php(n):  # n+1 pigeons, n holes; var p(i,j)
    v = lambda i, j: i * n + j + 1
    C = [tuple(v(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for a, b in itertools.combinations(range(n + 1), 2):
            C.append((-v(a, j), -v(b, j)))
    return C, n * (n + 1)

def tseitin(edges, charge):
    nv = len(edges); C = []
    verts = sorted({x for e in edges for x in e})
    for u in verts:
        inc = [k + 1 for k, e in enumerate(edges) if u in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[u]:  # forbid assignments with wrong parity
                C.append(tuple(-x if s else x for x, s in zip(inc, signs)))
    return C, nv, verts

def gf2_cost(edges, charge):
    """Row operations of Gaussian elimination on the vertex equations."""
    verts = sorted({x for e in edges for x in e})
    rows = [[(1 if u in e else 0) for e in edges] + [charge[u]] for u in verts]
    ops = 0; r = 0; m = len(edges)
    for c in range(m):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]; ops += 1
        r += 1
    inconsistent = any(all(x == 0 for x in row[:-1]) and row[-1] for row in rows)
    return ops, inconsistent

def restrict(clauses, lit):
    out = []
    for c in clauses:
        if lit in c: continue
        out.append(tuple(x for x in c if x != -lit))
    return frozenset(out)

def min_tree(F):
    @lru_cache(maxsize=None)
    def S(G):
        if () in G: return 1
        vs = {abs(x) for c in G for x in c}
        if not vs: raise ValueError("satisfiable branch")
        best = None
        for x in vs:
            a = S(restrict(G, x)); 
            if best is not None and a >= best: continue
            b = S(restrict(G, -x)); t = 1 + a + b
            if best is None or t < best: best = t
        return best
    val = S(frozenset(F)); return val, S.cache_info().currsize

def brute_unsat(C, nv):
    for a in itertools.product([False, True], repeat=nv):
        if all(any((x > 0) == a[abs(x) - 1] for x in c) for c in C): return False
    return True

K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
K33 = [(a, b) for a in range(3) for b in range(3, 6)]
Q3 = [(a, a ^ (1 << k)) for a in range(8) for k in range(3) if a < a ^ (1 << k)]
PRISM = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]

def rand3(n, m, seed):
    rng = random.Random(seed)
    while True:
        C = [tuple(rng.choice([1,-1]) * v for v in rng.sample(range(1, n+1), 3)) for _ in range(m)]
        if brute_unsat(C, n): return C
        seed += 1000; rng = random.Random(seed)

INST = {}
for n in (1, 2, 3): INST[f"PHP{n+1}_{n}"] = ("php", n)
for name, E in (("TseitinK4", K4), ("TseitinK33", K33), ("TseitinPrism", PRISM), ("TseitinQ3", Q3)):
    INST[name] = ("tseitin", E)
for s in range(3): INST[f"Rand3_n10_m60_s{s}"] = ("rand", (10, 60, s))

def run(name):
    kind, p = INST[name]; t0 = time.time(); rec = {"instance": name}
    if kind == "php": C, nv = php(p)
    elif kind == "rand": C = rand3(*p); nv = p[0]
    else:
        verts = sorted({x for e in p for x in e})
        ch = {u: (1 if u == verts[0] else 0) for u in verts}  # odd total charge
        C, nv, _ = tseitin(p, ch); ops, inc = gf2_cost(p, ch)
        rec.update(gf2_row_ops=ops, gf2_detects_unsat=inc, vertices=len(verts))
    assert brute_unsat(C, nv), "control failure: instance satisfiable"
    rec.update(vars=nv, clauses=len(C), dimacs_bits=sum(len(c) for c in C))
    rec["min_treelike_res_size"], rec["memo_states"] = min_tree(C)
    # hostile control: delete one clause -> must become SAT (for PHP/Tseitin minimal UNSAT)
    rec["deletion_control_sat"] = not brute_unsat(C[1:], nv)
    rec["seconds"] = round(time.time() - t0, 2); return rec

if __name__ == "__main__":
    if sys.argv[1] == "list": print("\n".join(INST)); sys.exit()
    print(json.dumps(run(sys.argv[1])))
