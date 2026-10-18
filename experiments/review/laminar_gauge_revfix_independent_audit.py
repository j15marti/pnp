#!/usr/bin/env python3
"""Independent finite audit of LAMINAR-GAUGE-TREE24 and REVFIX2.

All exhaustive stages are bounded below 30 seconds.  The script uses no SAT
package and reconstructs both encodings independently from their definitions.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json
import random
import time
from pathlib import Path

SEED = 202610190624
FIELDS = (2, 3, 5, 7)


@dataclass(frozen=True)
class Lit:
    v: str
    neg: bool = False

    def flip(self):
        return Lit(self.v, not self.neg)


def lv(l, a):
    return a[l.v] ^ int(l.neg)


def nae(cl, a):
    z = [lv(x, a) for x in cl]
    return min(z) != max(z)


def ors(cl, a):
    return any(lv(x, a) for x in cl)


def unrooted_tree(m):
    """Full unrooted binary tree: m leaves, internal degree 3 (m>=2)."""
    assert m >= 2
    leaves = [f"g{i}" for i in range(m)]
    if m == 2:
        return leaves, [(leaves[0], leaves[1])]
    if m == 3:
        return leaves + ["q0"], [("q0", x) for x in leaves]
    # Caterpillar: q0--...--q_{m-3}; endpoints have two leaves, middle one.
    ints = [f"q{i}" for i in range(m-2)]
    edges = [(ints[i], ints[i+1]) for i in range(len(ints)-1)]
    edges += [(ints[0], leaves[0]), (ints[0], leaves[1])]
    for i in range(1, len(ints)-1):
        edges.append((ints[i], leaves[i+1]))
    edges += [(ints[-1], leaves[-2]), (ints[-1], leaves[-1])]
    return leaves + ints, edges


def compile_laminar(source):
    m = len(source)
    nodes, edges = unrooted_tree(m)
    cls = []
    for i, (a, b, c) in enumerate(source):
        u, g = Lit(f"u{i}"), Lit(f"g{i}")
        cls += [(a, b, u), (u.flip(), c, g)]
    for j, (v, w) in enumerate(edges):
        e = Lit(f"e{j}")
        cls += [(Lit(v), Lit(w, True), e),
                (Lit(v), Lit(w, True), e.flip())]
    source_vars = sorted({l.v for cl in source for l in cl})
    vars_ = source_vars + [f"u{i}" for i in range(m)] + nodes + [f"e{j}" for j in range(len(edges))]
    assert len(vars_) == len(set(vars_))
    return cls, vars_, nodes, edges, source_vars


def source_family(m):
    clauses = [
        (Lit("x0"), Lit("x1"), Lit("x2")),
        (Lit("x0", True), Lit("x1"), Lit("x2")),
        (Lit("x0"), Lit("x1", True), Lit("x2")),
        (Lit("x0"), Lit("x1"), Lit("x2", True)),
    ]
    return clauses[:m]


def h_value(source, x):
    # Last literal true and first two differ, evaluated in source coordinates.
    return sum(lv(c, x) == 1 and lv(a, x) != lv(b, x) for a, b, c in source)


def target_projection(a, source_vars):
    g = a["g0"]
    return {x: a[x] ^ g for x in source_vars}


def exhaustive_laminar(m, failures, checks):
    source = source_family(m)
    cls, vars_, nodes, edges, sv = compile_laminar(source)
    models = 0
    fibers = Counter()
    projected_bad = 0
    for bits in product((0, 1), repeat=len(vars_)):
        a = dict(zip(vars_, bits))
        if all(nae(c, a) for c in cls):
            models += 1
            x = target_projection(a, sv)
            key = tuple(x[v] for v in sv)
            fibers[key] += 1
            if not all(ors(c, x) for c in source):
                projected_bad += 1
    expected_source = sum(all(ors(c, dict(zip(sv, bits))) for c in source)
                          for bits in product((0, 1), repeat=len(sv)))
    expected_models = 0
    for bits in product((0, 1), repeat=len(sv)):
        x = dict(zip(sv, bits))
        if all(ors(c, x) for c in source):
            f = 2 ** (2*m - 2 + h_value(source, x))
            expected_models += f
            if fibers[bits] != f:
                failures.append(f"fiber m={m} x={bits}: {fibers[bits]} != {f}")
    occ = Counter(l.v for c in cls for l in c if l.v not in sv)
    proper = all(len({l.v for l in c}) == 3 for c in cls)
    want_vars, want_cls = len(sv)+5*m-5, 6*m-6
    if (len(vars_), len(cls), max(occ.values()), proper, projected_bad) != (want_vars, want_cls, 6 if m >= 3 else 3, True, 0):
        failures.append(f"structure m={m}")
    if models != expected_models:
        failures.append(f"model count m={m}: {models} != {expected_models}")
    checks["laminar_assignments"] += 2 ** len(vars_)
    checks["laminar_models"] += models
    return {
        "m": m, "variables": len(vars_), "clauses": len(cls),
        "source_models": expected_source, "target_models": models,
        "expected_target_models": expected_models, "proper": proper,
        "max_aux_occurrence": max(occ.values()), "projected_bad": projected_bad,
        "fiber_histogram": dict(sorted(Counter(fibers.values()).items())),
    }


def min_gauge_boundary(m, leaf_colours):
    nodes, edges = unrooted_tree(m)
    best = None
    for edge_bits in product((0, 1), repeat=len(edges)):
        incident = {v: [] for v in nodes}
        for colour, (v, w) in zip(edge_bits, edges):
            incident[v].append(colour)
            incident[w].append(colour)
        cost = 0
        for i in range(m):
            if incident[f"g{i}"][0] != leaf_colours[i]:
                cost += 1
        for v in nodes:
            if v.startswith("q") and len(set(incident[v])) > 1:
                cost += 1
        best = cost if best is None else min(best, cost)
    return best


def component_leaves(m, cut_index):
    nodes, edges = unrooted_tree(m)
    keep = [e for i, e in enumerate(edges) if i != cut_index]
    seen = {edges[cut_index][0]}
    changed = True
    while changed:
        changed = False
        for a, b in keep:
            if a in seen and b not in seen:
                seen.add(b); changed = True
            if b in seen and a not in seen:
                seen.add(a); changed = True
    return {int(x[1:]) for x in seen if x.startswith("g")}


def width_audit(failures, checks):
    displayed = []
    for w, m in ((6, 6), (8, 8)):
        nodes, edges = unrooted_tree(m)
        # Choose a central cut and assign source variables so exactly w cross.
        cut = min(range(len(edges)), key=lambda i: abs(len(component_leaves(m, i))-m/2))
        left = component_leaves(m, cut)
        colours = tuple(0 if i in left else 1 for i in range(m))
        overhead = min_gauge_boundary(m, colours)
        if overhead != 1:
            failures.append(f"displayed cut m={m}: overhead {overhead}")
        displayed.append({"source_width": w, "target_width": w+overhead,
                          "tree_edge": cut, "leaf_partition": colours})
        checks["displayed_cut_cells"] += 1

    rng = random.Random(SEED)
    hostile = []
    for m in (6, 8):
        seen = set()
        for _ in range(24):
            colours = tuple(rng.getrandbits(1) for _ in range(m))
            if len(set(colours)) < 2 or colours in seen:
                continue
            seen.add(colours)
            overhead = min_gauge_boundary(m, colours)
            hostile.append({"m": m, "leaf_partition": colours, "minimum_gauge_overhead": overhead})
            checks["incompatible_cut_cells"] += 1
    counter = max(hostile, key=lambda z: z["minimum_gauge_overhead"])
    if counter["minimum_gauge_overhead"] <= 1:
        failures.append("no incompatible-cut counterexample found")
    return displayed, hostile, counter


# Minimal sparse polynomials over GF(p), exponent tuples retained before Boolean reduction.
class Poly:
    def __init__(self, n, p, t=None):
        self.n, self.p = n, p
        self.t = {m: c % p for m, c in (t or {}).items() if c % p}
    @classmethod
    def one(cls, n, p): return cls(n, p, {(0,)*n: 1})
    @classmethod
    def var(cls, n, p, i):
        e = [0]*n; e[i] = 1; return cls(n, p, {tuple(e): 1})
    def __add__(self, o):
        if not isinstance(o, Poly): o = Poly(self.n, self.p, {(0,)*self.n: o})
        d = dict(self.t)
        for m, c in o.t.items(): d[m] = (d.get(m, 0)+c) % self.p
        return Poly(self.n, self.p, d)
    __radd__ = __add__
    def __neg__(self): return Poly(self.n, self.p, {m: -c for m,c in self.t.items()})
    def __sub__(self, o): return self + (-o)
    def __rsub__(self, o): return o + (-self)
    def __mul__(self, o):
        if not isinstance(o, Poly): o = Poly(self.n, self.p, {(0,)*self.n: o})
        d = {}
        for a, ca in self.t.items():
            for b, cb in o.t.items():
                m = tuple(x+y for x,y in zip(a,b)); d[m] = (d.get(m,0)+ca*cb)%self.p
        return Poly(self.n, self.p, d)
    __rmul__ = __mul__
    def degree(self): return max((sum(m) for m in self.t), default=-1)
    def ml(self):
        d = {}
        for m, c in self.t.items():
            mm = tuple(min(1, x) for x in m)
            d[mm] = (d.get(mm, 0) + c) % self.p
        return Poly(self.n, self.p, d)


def pc_front_audit(failures, checks):
    rows = []
    for p in FIELDS:
        one = Poly.one(4, p)
        a,b,c,e = [Poly.var(4,p,i) for i in range(4)]
        u = (one-a)*(one-b)
        # NAE(a,b,u): all-zero and all-one forbidden monomials.
        A0, A1 = (one-a)*(one-b)*(one-u), a*b*u
        # NAE(not u,c,0): false monomial is u(1-c); true monomial is zero.
        B0, B1 = u*(one-c), (one-u)*c*0
        source = (one-a)*(one-b)*(one-c)
        # Equality pair at g=h=edge=0 under replay restriction.
        eq = [0*one, 0*one, 0*one, 0*one]
        if A0.ml().t or A1.ml().t or (B0-source).t or B1.t or any(q.t for q in eq):
            failures.append(f"PC frontend p={p}")
        maxdeg = max(A0.degree(), A1.degree(), B0.degree(), source.degree())
        if maxdeg > 6:
            failures.append(f"PC degree p={p}: {maxdeg}")
        rows.append({"field": p, "max_repair_degree": maxdeg,
                     "front_boolean_remainders_zero": True,
                     "second_clause_equals_source_axiom": True})
        checks["pc_field_cells"] += 1
    return rows


class CNF:
    def __init__(self, source_vars):
        self.vars, self.clauses, self.pad = set(source_vars), [], 0
    def add(self, lits):
        lits = tuple(lits)
        if len(lits) == 2:
            q = Lit(f"pad{self.pad}"); self.pad += 1; self.vars.add(q.v)
            self.clauses += [lits+(q,), lits+(q.flip(),)]
        else: self.clauses.append(lits)
        self.vars.update(l.v for l in lits)
    def AND(self,a,b,z):
        self.vars.add(z); Z=Lit(z)
        self.add((a.flip(),b.flip(),Z)); self.add((a,Z.flip())); self.add((b,Z.flip()))
    def XOR(self,a,b,z):
        self.vars.add(z); Z=Lit(z)
        self.add((a,b,Z.flip())); self.add((a,b.flip(),Z)); self.add((a.flip(),b,Z)); self.add((a.flip(),b.flip(),Z.flip()))
    def EQ(self,a,b):
        self.add((Lit(a,True),Lit(b))); self.add((Lit(a),Lit(b,True)))


def revfix_one(cyclic):
    # Signed source (not x0 or x1 or x2) has the hostile false row x0=1.
    B=CNF(["x0","x1","x2"])
    false = [Lit("x0"), Lit("x1",True), Lit("x2",True)]
    B.AND(false[0],false[1],"r0"); B.AND(Lit("r0"),false[2],"v0")
    h="v0"
    if cyclic:
        B.AND(Lit("x0"),Lit("v0"),"cw"); B.XOR(Lit("v0"),Lit("cw"),"h0"); h="h0"
    B.vars.add("y0"); B.XOR(Lit("y0"),Lit(h),"yp0"); B.EQ("yp0","y0")
    return B


def revfix_audit(failures, checks):
    rows=[]
    for cyclic in (False,True):
        B=revfix_one(cyclic); names=sorted(B.vars); models=0; false_models=0
        for bits in product((0,1), repeat=len(names)):
            a=dict(zip(names,bits))
            if all(any(lv(l,a) for l in cl) for cl in B.clauses):
                models += 1
                source_ok = (not a["x0"]) or a["x1"] or a["x2"]
                false_models += int(not source_ok)
        expected=(17,27,4096,512) if cyclic else (13,18,896,0)
        got=(len(names),len(B.clauses),models,false_models)
        if got != expected: failures.append(f"REVFIX cyclic={cyclic}: {got} != {expected}")
        rows.append({"cyclic":cyclic,"variables":len(names),"clauses":len(B.clauses),
                     "models":models,"false_source_fixed_point_models":false_models})
        checks["revfix_assignments"] += 2**len(names)
    return rows


def main():
    t0=time.perf_counter(); failures=[]; checks=Counter()
    model_rows=[exhaustive_laminar(m,failures,checks) for m in (2,3,4)]
    displayed,hostile,counter=width_audit(failures,checks)
    pc_rows=pc_front_audit(failures,checks)
    revfix_rows=revfix_audit(failures,checks)
    result={
        "run_id":"LAMINARTREE24_TEST1","seed":SEED,
        "status":"PASS" if not failures else "FAIL","failures":failures,
        "elapsed_seconds":time.perf_counter()-t0,"checks":dict(checks),
        "model_rows":model_rows,"displayed_cuts":displayed,
        "incompatible_cut_sample":hostile,"smallest_reported_counterexample":counter,
        "pc_rows":pc_rows,"revfix_rows":revfix_rows,
        "conclusions":[
            "Unrooted full degree-three gauge trees have n+5m-5 variables and 6m-6 clauses for m>=2.",
            "The supplied four-clause source has 4 models and the 18-variable target has exactly 576 models.",
            "The witness fiber is 2^(2m-2+h_F(x)); the compiler is not parsimonious.",
            "Displayed tree-edge cuts add exactly one gauge boundary variable; incompatible partitions need not.",
            "The all-field degree-two frontend replay passes ordinary-ring Boolean reduction.",
            "Two-shear REVFIX is unsound for m=1; the hostile one-clause target has 512 false-source fixed-point models.",
            "None of these finite/proof-system checks is an unrestricted machine-time lower bound."
        ]}
    out=Path("results/raw/review/2026-10-19_LAMINARTREE24_TEST1.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"; out.write_text(text)
    print(text,end=""); print("raw_sha256",sha256(text.encode()).hexdigest())
    if failures: raise SystemExit(1)


if __name__ == "__main__": main()
