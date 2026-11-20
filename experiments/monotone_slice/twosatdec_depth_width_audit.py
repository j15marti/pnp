"""DEPTHWIDTH1: minimal free-exact-2-SAT decision depth on UNSAT random 3-CNF.

Certificate (TWOSATDEC protocol): a variable set S certifies F iff every assignment
to S, followed by unit propagation, yields an empty clause or an unsatisfiable
width<=2 skeleton (surviving width-3 clauses are ignored).  We compute the least |S|.
Exact-layer sampling: t = round(density*q) distinct proper 3-clauses, uniform.
Usage: python3 twosatdec_depth_width_audit.py SEED DENSITY Q1,Q2,.. SAMPLES RMAX
"""
import itertools, random, sys, time, json

def clauses_list(q):
    out = []
    for tr in itertools.combinations(range(q), 3):
        for s in range(8):
            out.append(tuple((v + 1) * (1 if (s >> i) & 1 else -1) for i, v in enumerate(tr)))
    return out

def up(cls, assign):
    assign = dict(assign)
    while True:
        changed = False
        live = []
        for c in cls:
            sat = False; rest = []
            for l in c:
                v = abs(l); val = assign.get(v)
                if val is None: rest.append(l)
                elif val == (l > 0): sat = True; break
            if sat: continue
            if not rest: return None, None
            if len(rest) == 1:
                assign[abs(rest[0])] = rest[0] > 0; changed = True
            live.append(tuple(rest))
        if not changed: return live, assign
        cls = live

def twosat_unsat(cls2):
    # implication graph SCC (Kosaraju) over literals
    g = {}; rg = {}
    lits = set()
    for c in cls2:
        a, b = c
        for x, y in ((-a, b), (-b, a)):
            g.setdefault(x, []).append(y); rg.setdefault(y, []).append(x)
            lits.update((x, y, -x, -y))
    seen = set(); order = []
    for s in lits:
        if s in seen: continue
        stack = [(s, iter(g.get(s, [])))]; seen.add(s)
        while stack:
            v, it = stack[-1]
            nxt = next(it, None)
            if nxt is None: order.append(v); stack.pop()
            elif nxt not in seen: seen.add(nxt); stack.append((nxt, iter(g.get(nxt, []))))
    comp = {}
    for s in reversed(order):
        if s in comp: continue
        comp[s] = s; st = [s]
        while st:
            v = st.pop()
            for w in rg.get(v, []):
                if w not in comp: comp[w] = s; st.append(w)
    return any(comp.get(l) == comp.get(-l) for l in lits if l > 0)

def leaf_refuted(cls, assign):
    live, _ = up(cls, assign)
    if live is None: return True
    return twosat_unsat([c for c in live if len(c) == 2])

def certifies(cls, S):
    for bits in itertools.product((False, True), repeat=len(S)):
        if not leaf_refuted(cls, dict(zip(S, bits))): return False
    return True

def sat(cls, q):
    def rec(cls, assign):
        live, a = up(cls, assign)
        if live is None: return False
        if not live: return True
        v = abs(live[0][0])
        return rec(live, {**a, v: True}) or rec(live, {**a, v: False})
    return rec(cls, {})

def min_depth(cls, q, rmax, deadline):
    for r in range(rmax + 1):
        for S in itertools.combinations(range(1, q + 1), r):
            if time.time() > deadline: return None, r
            if certifies(cls, S): return r, r
    return None, rmax + 1

def main():
    seed, dens = int(sys.argv[1]), float(sys.argv[2])
    qs = [int(x) for x in sys.argv[3].split(',')]; N = int(sys.argv[4]); rmax = int(sys.argv[5])
    rng = random.Random(seed); res = []
    for q in qs:
        L = clauses_list(q); t = round(dens * q)
        for i in range(N):
            F = rng.sample(L, t)
            if sat(F, q): res.append({'q': q, 't': t, 'i': i, 'sat': True}); continue
            t0 = time.time(); r, lb = min_depth(F, q, rmax, t0 + 4.0)
            res.append({'q': q, 't': t, 'i': i, 'sat': False, 'min_r': r, 'lower_bound_r': lb,
                        'secs': round(time.time() - t0, 2)})
    print(json.dumps({'seed': seed, 'density': dens, 'rmax': rmax, 'results': res}))

if __name__ == '__main__':
    main()
