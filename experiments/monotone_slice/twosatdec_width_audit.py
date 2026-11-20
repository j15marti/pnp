#!/usr/bin/env python3
"""TWOSATDEC-WIDTH1 audit (COMPUTATIONAL companion to a KNOWN-THEOREM argument).

Two finite checks on the exact-layer protocol used by TWOSATDEC6..96:
  (A) UNSAT frequency at the protocol density t = floor(3.5 q) as q grows.
  (B) Minimal free-2-SAT certifying depth r*(F) for UNSAT formulas at
      density 6 (above every known 3-SAT threshold upper bound), q small.

Generator, certificate and seed conventions follow TWOSATDEC21:
uniform sample of t distinct proper 3-clauses (Python random.Random.sample
on the lexicographic list), depth-r set S certifies iff every assignment of S,
after unit propagation, yields an empty clause or an unsatisfiable
width<=2 skeleton (surviving width-3 clauses are not charged).
Pure Python, no external solver. Usage: python3 twosatdec_width_audit.py A|B
"""
import itertools, random, sys, time, json

def clause_list(q):
    out = []
    for tri in itertools.combinations(range(q), 3):
        for s in range(8):
            out.append(tuple((v, (s >> i) & 1) for i, v in enumerate(tri)))  # (var, pol) pol1=positive
    return out

def lit(v, p):
    return v + 1 if p else -(v + 1)

def sample(q, t, rng, cache={}):
    if q not in cache:
        cache[q] = clause_list(q)
    return [tuple(lit(v, p) for v, p in c) for c in rng.sample(cache[q], t)]

def unit_prop(clauses, assign):
    """assign: dict var->bool (1-based var). Returns (conflict, residual clauses)."""
    assign = dict(assign)
    cl = clauses
    while True:
        new, units, changed = [], [], False
        for c in cl:
            keep, sat = [], False
            for l in c:
                v = abs(l)
                if v in assign:
                    if assign[v] == (l > 0):
                        sat = True; break
                else:
                    keep.append(l)
            if sat:
                continue
            if not keep:
                return True, None
            if len(keep) == 1:
                units.append(keep[0])
            new.append(tuple(keep))
        if not units:
            return False, new
        for u in units:
            v = abs(u)
            if v in assign and assign[v] != (u > 0):
                return True, None
            assign[v] = u > 0
        cl = new

def twosat_unsat(clauses):
    """True iff the width<=2 part (all width<=2 here, units already gone) is UNSAT."""
    two = [c for c in clauses if len(c) <= 2]
    if not two:
        return False
    adj = {}
    for c in two:
        a, b = (c[0], c[0]) if len(c) == 1 else c
        adj.setdefault(-a, []).append(b); adj.setdefault(-b, []).append(a)
    # Kosaraju SCC
    nodes = set(adj) | {x for vs in adj.values() for x in vs}
    nodes |= {-x for x in nodes}
    order, seen = [], set()
    for s in nodes:
        if s in seen: continue
        stack = [(s, iter(adj.get(s, ())))]; seen.add(s)
        while stack:
            n, it = stack[-1]
            for m in it:
                if m not in seen:
                    seen.add(m); stack.append((m, iter(adj.get(m, ())))); break
            else:
                stack.pop(); order.append(n)
    radj = {}
    for a, vs in adj.items():
        for b in vs: radj.setdefault(b, []).append(a)
    comp = {}
    for s in reversed(order):
        if s in comp: continue
        comp[s] = s; stack = [s]
        while stack:
            n = stack.pop()
            for m in radj.get(n, ()):
                if m not in comp: comp[m] = s; stack.append(m)
    return any(comp[x] == comp.get(-x) for x in nodes if x > 0)

def branch_refuted(clauses, assign):
    conf, res = unit_prop(clauses, assign)
    return conf or twosat_unsat(res)

def certifies(clauses, S):
    for bits in itertools.product((False, True), repeat=len(S)):
        if not branch_refuted(clauses, dict(zip(S, bits))):
            return False
    return True

def min_depth(clauses, q, rmax, deadline):
    for r in range(rmax + 1):
        for S in itertools.combinations(range(1, q + 1), r):
            if time.time() > deadline: return None
            if certifies(clauses, S): return r
    return ">%d" % rmax

def dpll(clauses, assign=None):
    conf, res = unit_prop(clauses, assign or {})
    if conf: return False
    if not res: return True
    cnt = {}
    for c in res:
        for l in c: cnt[abs(l)] = cnt.get(abs(l), 0) + 1
    v = max(cnt, key=cnt.get)
    base = dict(assign or {})
    # re-derive assignment from residual: residual omits assigned vars, so branch on residual
    for val in (True, False):
        if dpll(res, {v: val}): return True
    return False

def stage_A():
    rng_seed = 20261005; N = 200; out = []
    for q in (20, 30, 40, 60, 80, 100):
        rng = random.Random(rng_seed); t = int(3.5 * q)
        uns = sum(1 for _ in range(N) if not dpll(sample(q, t, rng)))
        out.append({"q": q, "t": t, "N": N, "unsat": uns})
        print(out[-1], flush=True)
    return out

def stage_B():
    rng_seed = 20261005; N = 12; out = []
    for q in ((8, 10, 12, 14, 16, 18) if len(sys.argv) < 3 else tuple(int(x) for x in sys.argv[2].split(","))):
        rng = random.Random(rng_seed); t = 6 * q
        ds = []; t0 = time.time()
        for _ in range(N):
            F = sample(q, t, rng)
            if dpll(F): ds.append("SAT"); continue
            ds.append(min_depth(F, q, 6, t0 + 25))
        rec = {"q": q, "t": t, "N": N, "rstar": ds, "secs": round(time.time() - t0, 2)}
        out.append(rec); print(rec, flush=True)
    return out

if __name__ == "__main__":
    st = sys.argv[1]
    res = stage_A() if st == "A" else stage_B()
    print("JSON", json.dumps({"stage": st, "seed": 20261005, "results": res}))
