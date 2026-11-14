"""Certificate-closure controls (deterministic, single stage, < 30 s).
(1) 2-SAT: polynomial SCC-style decider; its rejection certificate (implication
    paths x=>~x=>x) is converted into an explicit Resolution refutation, every
    step checked; size recorded.
(2) Tseitin (odd charge) on small 3-regular graphs: Gaussian-elimination
    rejection (row operations counted) vs exact minimum tree-like Resolution
    leaves (falsified-clause decision-tree DP)."""
import json, sys, random, itertools, hashlib, time
from functools import lru_cache
from collections import deque

# ---------- 2-SAT ----------
def lit_neg(l): return -l
def implication_path(adj, s, t):
    prev = {s: None}; q = deque([s])
    while q:
        u = q.popleft()
        if u == t: break
        for v, ci in adj.get(u, []):
            if v not in prev: prev[v] = (u, ci); q.append(v)
    if t not in prev: return None
    path = []; v = t
    while prev[v] is not None:
        u, ci = prev[v]; path.append(ci); v = u
    return path[::-1]

def resolve(c1, c2, var):
    assert var in c1 and -var in c2
    return frozenset((c1 - {var}) | (c2 - {-var}))

def chain_clause(clauses, path, s):
    # path of clause indices forming s -> ... ; returns derived clause (~s v end) and steps
    cur = frozenset(clauses[path[0]]); steps = 0
    lit = [l for l in clauses[path[0]] if l != -s]
    end = lit[0] if lit else -s
    for ci in path[1:]:
        c = frozenset(clauses[ci])
        # cur contains end; c contains -end
        nxt = [l for l in c if l != -end]
        cur = resolve(cur, c, end); steps += 1
        end = nxt[0] if nxt else -end
    return cur, steps

def two_sat_case(n, m, rng):
    while True:
        cl = []
        for _ in range(m):
            a, b = rng.sample(range(1, n + 1), 2)
            cl.append((a * rng.choice((1, -1)), b * rng.choice((1, -1))))
        adj = {}
        for i, (a, b) in enumerate(cl):
            adj.setdefault(-a, []).append((b, i)); adj.setdefault(-b, []).append((a, i))
        for x in range(1, n + 1):
            p1 = implication_path(adj, x, -x); p2 = implication_path(adj, -x, x)
            if p1 and p2:
                c1, s1 = chain_clause(cl, p1, x)   # expect {~x}
                c2, s2 = chain_clause(cl, p2, -x)  # expect {x}
                assert c1 == frozenset({-x}) and c2 == frozenset({x}), (c1, c2)
                empty = resolve(c2, c1, x); assert empty == frozenset()
                return {"n": n, "m": m, "res_steps": s1 + s2 + 1,
                        "bound_2m_plus_1": 2 * m + 1}

# ---------- Tseitin ----------
GRAPHS = {
 "K4": [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
 "K33": [(a,b) for a in range(3) for b in range(3,6)],
 "prism": [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)],
 "Q3": [(a,a^b) for a in range(8) for b in (1,2,4) if a < a^b],
}
def tseitin(edges):
    nv = max(max(e) for e in edges) + 1
    inc = {v: [i for i, e in enumerate(edges) if v in e] for v in range(nv)}
    charge = {v: (1 if v == 0 else 0) for v in range(nv)}  # total odd -> UNSAT
    cls = []
    for v, es in inc.items():
        for bits in itertools.product((0, 1), repeat=len(es)):
            if sum(bits) % 2 != charge[v]:  # forbid this assignment
                cls.append([(e, 1 - b) for e, b in zip(es, bits)])
    return len(edges), cls, inc, charge

def gauss_ops(nvars, inc, charge):
    rows = [(sum(1 << e for e in es), charge[v]) for v, es in inc.items()]
    ops = 0; piv = []
    for r in rows:
        a, c = r
        for pa, pc, bit in piv:
            if a >> bit & 1: a ^= pa; c ^= pc; ops += 1
        if a: piv.append((a, c, a.bit_length() - 1))
        elif c: return ops, True
    return ops, False

def min_leaves(nv, cls):
    @lru_cache(maxsize=None)
    def L(st):
        if any(all(st[v] != 2 and st[v] != s for v, s in c) for c in cls): return 1
        best = None
        for v in range(nv):
            if st[v] == 2:
                a = L(st[:v] + (0,) + st[v+1:])
                if best is not None and a >= best: continue
                b = L(st[:v] + (1,) + st[v+1:])
                if best is None or a + b < best: best = a + b
        return best
    return L((2,) * nv)

out = {"two_sat": [], "tseitin": []}
rng = random.Random(20261114)
for n in (8, 16, 32, 64, 128):
    out["two_sat"].append(two_sat_case(n, 2 * n, rng))
for name, ed in GRAPHS.items():
    t = time.time()
    nv, cls, inc, ch = tseitin(ed)
    ops, unsat = gauss_ops(nv, inc, ch); assert unsat
    out["tseitin"].append({"graph": name, "vars": nv, "clauses": len(cls),
        "gauss_row_ops": ops, "min_treelike_leaves": min_leaves(nv, cls),
        "seconds": round(time.time() - t, 2)})
out["seed"] = 20261114
out["code_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
json.dump(out, sys.stdout, indent=1)
