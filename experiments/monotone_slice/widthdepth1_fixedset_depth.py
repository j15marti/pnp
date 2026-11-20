"""WIDTHDEPTH1: minimal fixed-set decision depth r for the TWOSATDEC certifier
(every assignment of r chosen variables, then unit propagation, then the
width-<=2 skeleton must be 2-UNSAT; surviving width-3 clauses are ignored),
on random proper 3-CNF above the proven UNSAT threshold (density 5.0).
COMPUTATIONAL illustration only. Usage: python -I widthdepth1_fixedset_depth.py
"""
import itertools, random, sys, time, json

def gen(q, t, rng):
    trip = list(itertools.combinations(range(q), 3))
    cl = []
    for idx in rng.sample(range(8 * len(trip)), t):
        a, s = trip[idx // 8], idx % 8
        cl.append(tuple((v + 1) if (s >> i) & 1 else -(v + 1) for i, v in enumerate(a)))
    return cl

def up(cls, asg):
    asg = dict(asg)
    while True:
        changed = False; rest = []
        for c in cls:
            lits = []; sat = False
            for l in c:
                v = abs(l)
                if v in asg:
                    if asg[v] == (l > 0): sat = True; break
                else: lits.append(l)
            if sat: continue
            if not lits: return None, None
            if len(lits) == 1:
                asg[abs(lits[0])] = lits[0] > 0; changed = True
            else: rest.append(tuple(lits))
        if not changed: return asg, rest
        cls = rest

def twosat_unsat(c2, q):
    # implication graph SCC (Kosaraju), literal node 2v / 2v+1
    n = 2 * (q + 1); g = [[] for _ in range(n)]; rg = [[] for _ in range(n)]
    node = lambda l: 2 * abs(l) + (0 if l > 0 else 1)
    for a, b in c2:
        for x, y in ((-a, b), (-b, a)):
            g[node(x)].append(node(y)); rg[node(y)].append(node(x))
    seen = [False] * n; order = []
    for s in range(n):
        if seen[s]: continue
        st = [(s, 0)]; seen[s] = True
        while st:
            u, i = st.pop()
            if i < len(g[u]):
                st.append((u, i + 1)); w = g[u][i]
                if not seen[w]: seen[w] = True; st.append((w, 0))
            else: order.append(u)
    comp = [-1] * n; c = 0
    for s in reversed(order):
        if comp[s] != -1: continue
        st = [s]; comp[s] = c
        while st:
            u = st.pop()
            for w in rg[u]:
                if comp[w] == -1: comp[w] = c; st.append(w)
        c += 1
    return any(comp[2 * v] == comp[2 * v + 1] for v in range(1, q + 1))

def leaf_ok(cls, q, asg):
    a, rest = up(cls, asg)
    if a is None: return True
    return twosat_unsat([c for c in rest if len(c) == 2], q)

def sat(cls, q):
    def dp(asg):
        a, rest = up(cls_holder[0], asg)
        if a is None: return False
        if not rest: return True
        v = abs(rest[0][0])
        return dp({**a, v: True}) or dp({**a, v: False})
    cls_holder = [cls]; return dp({})

def min_r(cls, q, rmax, deadline):
    for r in range(0, rmax + 1):
        for S in itertools.combinations(range(1, q + 1), r):
            if time.time() > deadline: return None, r
            if all(leaf_ok(cls, q, dict(zip(S, bits)))
                   for bits in itertools.product((False, True), repeat=r)):
                return r, r
    return None, rmax + 1

QS = tuple(int(x) for x in sys.argv[1:]) or (10, 14, 18, 22, 26)

def main():
    seed = 20261120; dens = 5.0; N = 6; out = {"seed": seed, "density": dens, "rows": []}
    rng = random.Random(seed)
    for q in QS:
        t = int(dens * q); rs = []
        for k in range(N):
            cls = gen(q, t, rng)
            if sat(cls, q): rs.append("SAT"); continue
            r, lb = min_r(cls, q, 6, time.time() + 3.0)
            rs.append(r if r is not None else ">=%d(timeout)" % lb)
        out["rows"].append({"q": q, "t": t, "min_r": rs}); print(q, t, rs, flush=True)
    print(json.dumps(out))

if __name__ == "__main__":
    main()
