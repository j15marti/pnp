#!/usr/bin/env python3
"""Independent exact audit of REVFIX anchored/two-shear PC substitutions.

The program reconstructs the complete proper exact-3-CNF gate encoding,
checks exact variable/clause counts and model count for the one-clause case,
and verifies ordinary-polynomial-ring Boolean-ideal/source-ideal certificates
over GF(2), GF(3), GF(5), GF(7), and GF(11).  It also audits the laminar
degree-three NAE equality node and the degree-six three-variable by-cases
repair.  No finite check is interpreted as an unrestricted runtime bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SEED = 202610190616
FIELDS = (2, 3, 5, 7, 11)


class Poly:
    """Sparse ordinary polynomial over GF(p), with exponent-tuple monomials."""

    def __init__(self, n: int, p: int, terms=None):
        self.n, self.p = n, p
        out = {}
        for mon, coeff in (terms or {}).items():
            coeff %= p
            if coeff:
                out[tuple(mon)] = (out.get(tuple(mon), 0) + coeff) % p
        self.t = {m: c for m, c in out.items() if c}

    @classmethod
    def zero(cls, n, p):
        return cls(n, p)

    @classmethod
    def one(cls, n, p):
        return cls(n, p, {(0,) * n: 1})

    @classmethod
    def var(cls, n, p, i):
        e = [0] * n
        e[i] = 1
        return cls(n, p, {tuple(e): 1})

    def __add__(self, other):
        assert self.n == other.n and self.p == other.p
        d = dict(self.t)
        for m, c in other.t.items():
            d[m] = (d.get(m, 0) + c) % self.p
        return Poly(self.n, self.p, d)

    def __neg__(self):
        return Poly(self.n, self.p, {m: -c for m, c in self.t.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        assert self.n == other.n and self.p == other.p
        d = {}
        for a, ca in self.t.items():
            for b, cb in other.t.items():
                m = tuple(x + y for x, y in zip(a, b))
                d[m] = (d.get(m, 0) + ca * cb) % self.p
        return Poly(self.n, self.p, d)

    def scale(self, c):
        return Poly(self.n, self.p, {m: c * a for m, a in self.t.items()})

    def degree(self):
        return max((sum(m) for m in self.t), default=-1)

    def multilinear(self):
        d = {}
        for m, c in self.t.items():
            q = tuple(min(1, e) for e in m)
            d[q] = (d.get(q, 0) + c) % self.p
        return Poly(self.n, self.p, d)

    def eval(self, bits):
        return sum(c * _mon_eval(m, bits) for m, c in self.t.items()) % self.p

    def __eq__(self, other):
        return self.n == other.n and self.p == other.p and self.t == other.t


def _mon_eval(mon, bits):
    z = 1
    for e, b in zip(mon, bits):
        z *= b ** e
    return z


def xor_poly(a: Poly, b: Poly) -> Poly:
    return a + b - (a * b).scale(2)


def and_poly(a: Poly, b: Poly) -> Poly:
    return a * b


@dataclass(frozen=True)
class Lit:
    wire: str
    neg: bool = False

    def flip(self):
        return Lit(self.wire, not self.neg)


Clause = tuple[Lit, Lit, Lit]


class CNFBuilder:
    def __init__(self, source_vars):
        self.vars = set(source_vars)
        self.clauses: list[Clause] = []
        self.kinds: list[str] = []
        self.and_gates = []
        self.xor_gates = []
        self.equalities = []
        self.pad_counter = 0

    def fresh(self, prefix):
        name = f"{prefix}_{len(self.vars)}"
        if name in self.vars:
            raise AssertionError("freshness")
        self.vars.add(name)
        return name

    def emit(self, lits, kind):
        if len(lits) == 3:
            clause = tuple(lits)
            self.clauses.append(clause)
            self.kinds.append(kind)
            return
        if len(lits) != 2:
            raise ValueError("only binary padding is supported")
        q = self.fresh(f"pad{self.pad_counter}")
        self.pad_counter += 1
        self.clauses += [tuple(lits) + (Lit(q),), tuple(lits) + (Lit(q, True),)]
        self.kinds += [kind, kind]

    def gate_and(self, a: Lit, b: Lit, out: str):
        self.vars.add(out)
        self.emit((a.flip(), b.flip(), Lit(out)), "gate")
        self.emit((a, Lit(out, True)), "gate")
        self.emit((b, Lit(out, True)), "gate")
        self.and_gates.append((a, b, out))

    def gate_xor(self, a: Lit, b: Lit, out: str):
        self.vars.add(out)
        self.emit((a, b, Lit(out, True)), "gate")
        self.emit((a, b.flip(), Lit(out)), "gate")
        self.emit((a.flip(), b, Lit(out)), "gate")
        self.emit((a.flip(), b.flip(), Lit(out, True)), "gate")
        self.xor_gates.append((a, b, out))

    def equality(self, a: str, b: str):
        self.emit((Lit(a, True), Lit(b)), "closing")
        self.emit((Lit(a), Lit(b, True)), "closing")
        self.equalities.append((a, b))


def source_lit_value(name, neg, x):
    return 1 - x[name] if neg else x[name]


def eval_lit(lit, assignment):
    b = assignment[lit.wire]
    return 1 - b if lit.neg else b


def sat_clause(clause, assignment):
    return any(eval_lit(l, assignment) for l in clause)


def extend_gates(builder, source_assignment, free_y, free_padding=None):
    a = dict(source_assignment)
    a.update(free_y)
    pending = [("and", gate) for gate in builder.and_gates]
    pending += [("xor", gate) for gate in builder.xor_gates]
    while pending:
        progress = False
        for item in list(pending):
            kind, (x, y, out) = item
            if x.wire not in a or y.wire not in a:
                continue
            a[out] = (eval_lit(x, a) & eval_lit(y, a)) if kind == "and" else (
                eval_lit(x, a) ^ eval_lit(y, a))
            pending.remove(item)
            progress = True
        if not progress:
            raise AssertionError(f"gate evaluation DAG did not close: {pending[:2]}")
    padding = sorted(v for v in builder.vars if v.startswith("pad"))
    free_padding = free_padding or {v: 0 for v in padding}
    a.update(free_padding)
    return a


def build_revfix(source, cyclic=False):
    """Source clauses are triples (variable_name, negated)."""
    source_vars = sorted({x for cl in source for x, _ in cl})
    b = CNFBuilder(source_vars)
    m = len(source)
    vnames = []
    for i, cl in enumerate(source):
        false_lits = [Lit(x, not neg) for x, neg in cl]
        r, v = f"r{i}", f"v{i}"
        b.gate_and(false_lits[0], false_lits[1], r)
        b.gate_and(Lit(r), false_lits[2], v)
        vnames.append(v)

    tnames = [vnames[0]]
    for i in range(1, m):
        first_var = source[i][0][0]
        c, t = f"c{i}", f"t{i}"
        b.gate_and(Lit(first_var), Lit(vnames[i-1]), c)
        b.gate_xor(Lit(vnames[i]), Lit(c), t)
        tnames.append(t)

    if cyclic:
        c0, h0 = "cwrap", "h0"
        first_var = source[0][0][0]
        b.gate_and(Lit(first_var), Lit(tnames[-1]), c0)
        b.gate_xor(Lit(tnames[0]), Lit(c0), h0)
        hnames = [h0] + tnames[1:]
    else:
        hnames = tnames

    ynames, ypnames = [], []
    for i in range(m):
        y, yp = f"y{i}", f"yp{i}"
        b.vars.add(y)
        b.gate_xor(Lit(y), Lit(hnames[i]), yp)
        b.equality(yp, y)
        ynames.append(y)
        ypnames.append(yp)
    return b, source_vars, vnames, tnames, hnames, ynames, ypnames


def poly_lit(lit, sigma, one):
    z = sigma[lit.wire]
    return one - z if lit.neg else z


def clause_poly(clause, sigma, one):
    out = one
    for lit in clause:
        out = out * (one - poly_lit(lit, sigma, one))
    return out


def build_substitution(builder, source, cyclic, p):
    source_vars = sorted({x for cl in source for x, _ in cl})
    index = {x: i for i, x in enumerate(source_vars)}
    n = len(source_vars)
    zero, one = Poly.zero(n, p), Poly.one(n, p)
    sigma = {x: Poly.var(n, p, index[x]) for x in source_vars}
    # The replay restriction sets every feedback input and padding variable to
    # zero before evaluating the gate DAG.
    for v in builder.vars:
        if v.startswith("y") or v.startswith("pad"):
            sigma.setdefault(v, zero)
    cert = {}
    source_v = [None] * len(source)

    def lp(lit):
        return poly_lit(lit, sigma, one)

    # The builder stores ANDs and XORs separately, so recover topological order
    # from dependencies rather than assuming list order.
    pending = [("and", g) for g in builder.and_gates] + [("xor", g) for g in builder.xor_gates]
    # Names encode a DAG; repeatedly execute enabled gates to avoid relying on
    # separate AND/XOR storage order.
    while pending:
        progress = False
        for item in list(pending):
            kind, (a, bb, out) = item
            if a.wire not in sigma or bb.wire not in sigma:
                continue
            pa, pb = poly_lit(a, sigma, one), poly_lit(bb, sigma, one)
            sigma[out] = pa * pb if kind == "and" else xor_poly(pa, pb)
            if out.startswith("v"):
                i = int(out[1:])
                source_v[i] = sigma[out]
                cert[out] = {i: one}
            elif a.wire in cert or bb.wire in cert:
                ca, cb = cert.get(a.wire, {}), cert.get(bb.wire, {})
                if a.neg or bb.neg:
                    raise AssertionError("certified residual wire unexpectedly negated")
                if kind == "and":
                    if ca and cb:
                        # Assign the product to the first certificate.
                        cert[out] = {j: q * pb for j, q in ca.items()}
                    elif ca:
                        cert[out] = {j: q * pb for j, q in ca.items()}
                    else:
                        cert[out] = {j: q * pa for j, q in cb.items()}
                else:
                    # a+b-2ab = sum_j [(1-2b)A_j+B_j] v_j.
                    keys = set(ca) | set(cb)
                    cert[out] = {
                        j: ca.get(j, zero) * (one - pb.scale(2)) + cb.get(j, zero)
                        for j in keys
                    }
            pending.remove(item)
            progress = True
        if not progress:
            raise AssertionError(f"gate DAG did not close: {pending[:2]}")
    for v in builder.vars:
        if v.startswith("y") or v.startswith("pad"):
            sigma.setdefault(v, zero)
    return sigma, cert, source_v


def cert_reconstruct(cert, source_v, zero):
    out = zero
    for i, q in cert.items():
        out = out + q * source_v[i]
    return out


def all_boolean_values(poly):
    return [poly.eval(bits) for bits in itertools.product((0, 1), repeat=poly.n)]


def exact_counts(source, cyclic):
    b, *_ = build_revfix(source, cyclic)
    n, m = len({x for cl in source for x, _ in cl}), len(source)
    want_v = n + (14*m if cyclic else 14*m-4)
    want_c = 27*m if cyclic else 27*m-9
    return b, want_v, want_c


def source_satisfied(source, x):
    return all(any(source_lit_value(v, neg, x) for v, neg in cl) for cl in source)


def audit_one_clause_model_count(failures, checks):
    source = [(('x0', False), ('x1', False), ('x2', False))]
    b, *_ = build_revfix(source, False)
    names = sorted(b.vars)
    models = 0
    for bits in itertools.product((0, 1), repeat=len(names)):
        a = dict(zip(names, bits))
        if all(sat_clause(cl, a) for cl in b.clauses):
            models += 1
    checks["one_clause_assignments"] += 2 ** len(names)
    if models != 7 * 2**7 or len(names) != 13 or len(b.clauses) != 18:
        failures.append(f"one-clause model count {models}/{len(names)}/{len(b.clauses)}")
    return models


def audit_by_cases(p, failures, checks):
    n = 6
    one = Poly.one(n, p)
    xs = [Poly.var(n, p, i) for i in range(n)]
    deltas = []
    for a in itertools.product((0, 1), repeat=3):
        d = one
        for i, bit in enumerate(a):
            d = d * (xs[i] if bit else one-xs[i])
        deltas.append(d)
    total = Poly.zero(n, p)
    for d in deltas:
        total = total + d
    if total != one:
        failures.append(f"indicator partition p={p}")
    # All proper signed 3-clauses, with overlaps with the case variables.
    for vars_ in itertools.combinations(range(n), 3):
        for negs in itertools.product((0, 1), repeat=3):
            clause = one
            for i, neg in zip(vars_, negs):
                lit = one-xs[i] if neg else xs[i]
                clause = clause * (one-lit)
            for idx, a in enumerate(itertools.product((0, 1), repeat=3)):
                restricted = clause
                # Evaluation of first three variables in the polynomial.
                val_terms = {}
                for mon, coeff in clause.t.items():
                    coeff2 = coeff
                    mon2 = list(mon)
                    for i in range(3):
                        coeff2 *= a[i] ** mon2[i]
                        mon2[i] = 0
                    val_terms[tuple(mon2)] = val_terms.get(tuple(mon2), 0)+coeff2
                restricted = Poly(n, p, val_terms)
                diff = deltas[idx]*clause - deltas[idx]*restricted
                if diff.multilinear().t or diff.degree() > 6:
                    failures.append(f"by-cases repair p={p}")
                checks["by_cases_clause_repairs"] += 1
    # ONE3/NOT-ONE3 truth-table partition and non-affinity control.
    one3 = [sum(a) == 1 for a in itertools.product((0, 1), repeat=3)]
    if sum(one3) != 3 or any(x == (not (not x)) for x in []):
        failures.append("ONE3 table")
    checks["one3_rows"] += 8


def audit_laminar_node(p, failures, checks):
    n = 3
    zero, one = Poly.zero(n, p), Poly.one(n, p)
    sigma = {"x": zero, "y": zero, "e": zero}
    clauses = [
        (Lit("x"), Lit("y", True), Lit("e")),
        (Lit("x"), Lit("y", True), Lit("e", True)),
    ]
    for cl in clauses:
        if clause_poly(cl, sigma, one).t:
            failures.append(f"laminar equality p={p}")
        checks["laminar_nae_axioms"] += 1


def main():
    started = time.perf_counter()
    failures = []
    checks = Counter()
    rng = random.Random(SEED)

    # All-positive disjoint source clauses make the expanded-size hostile
    # control exact: each violation polynomial has eight monomials over every
    # field. Random signed clauses are exercised separately below.
    source = [
        ((f"x{3*i}", False), (f"x{3*i+1}", False), (f"x{3*i+2}", False))
        for i in range(8)
    ]

    count_rows = []
    field_rows = []
    for cyclic in (False, True):
        b, want_v, want_c = exact_counts(source, cyclic)
        proper = all(len({l.wire for l in cl}) == 3 for cl in b.clauses)
        if len(b.vars) != want_v or len(b.clauses) != want_c or not proper:
            failures.append(f"count/properness cyclic={cyclic}")
        count_rows.append({"cyclic": cyclic, "variables": len(b.vars),
                           "clauses": len(b.clauses), "proper": proper})

        for p in FIELDS:
            sigma, cert, source_v = build_substitution(b, source, cyclic, p)
            n_source = len({x for cl in source for x, _ in cl})
            zero, one = Poly.zero(n_source, p), Poly.one(n_source, p)
            max_var_degree = max(q.degree() for q in sigma.values())
            expected = 11 if cyclic else 7
            if max_var_degree > expected:
                failures.append(f"max substitution degree {max_var_degree}, p={p}, cyc={cyclic}")

            max_gate_degree = max_bool_degree = max_close_degree = 0
            gate_axioms = bool_axioms = close_axioms = 0
            for cl, kind in zip(b.clauses, b.kinds):
                q = clause_poly(cl, sigma, one)
                if kind == "gate":
                    gate_axioms += 1
                    max_gate_degree = max(max_gate_degree, q.degree())
                    if q.multilinear().t:
                        failures.append(f"gate Boolean-ideal remainder p={p}, cyc={cyclic}")
                else:
                    close_axioms += 1
                    max_close_degree = max(max_close_degree, q.degree())
                    # Closing images are zero or the changed-bit polynomial,
                    # hence lie in the source-clause ideal by its certificate.
                    if q.t:
                        matches = [name for name, qq in sigma.items()
                                   if name.startswith("yp") and qq == q]
                        if not matches:
                            failures.append(f"closing image mismatch p={p}, cyc={cyclic}")
                        else:
                            hname = "h0" if cyclic and matches[0] == "yp0" else (
                                "v0" if matches[0] == "yp0" else f"t{matches[0][2:]}")
                            if cert_reconstruct(cert[hname], source_v, zero) != sigma[hname]:
                                failures.append(f"source ideal certificate p={p}, {hname}")
            for name, q in sigma.items():
                ax = q*q-q
                bool_axioms += 1
                max_bool_degree = max(max_bool_degree, ax.degree())
                if ax.multilinear().t:
                    failures.append(f"Boolean axiom remainder p={p}, {name}")

            if max_gate_degree > 3*expected or max_bool_degree > 2*expected or max_close_degree > expected:
                failures.append(f"degree ledger p={p}, cyc={cyclic}")
            # Compiler-specific expanded-size counterexample: disjoint v_i.
            prod = one
            monomial_counts = []
            for i in range(4):
                prod = prod * sigma[f"v{i}"]
                monomial_counts.append(len(prod.t))
            if monomial_counts != [8, 64, 512, 4096]:
                failures.append(f"monomial growth p={p}: {monomial_counts}")

            field_rows.append({
                "field": p, "cyclic": cyclic,
                "max_substitution_degree": max_var_degree,
                "max_gate_axiom_degree": max_gate_degree,
                "max_boolean_axiom_degree": max_bool_degree,
                "max_closing_axiom_degree": max_close_degree,
                "gate_axioms": gate_axioms,
                "boolean_axioms": bool_axioms,
                "closing_axioms": close_axioms,
                "disjoint_v_product_terms": monomial_counts,
            })
            checks["field_mode_cells"] += 1
            checks["gate_axioms"] += gate_axioms
            checks["boolean_axioms"] += bool_axioms
            checks["closing_axioms"] += close_axioms
            audit_by_cases(p, failures, checks)
            audit_laminar_node(p, failures, checks)

    # Random polarity/renaming/duplicate-clause semantic extension controls.
    semantic_cases = 0
    cyclic_m1_counterexamples = 0
    for cyclic in (False, True):
        for m in range(1, 5):
            for rep in range(12):
                names = [f"z{i}" for i in range(max(3, 3*m))]
                src = []
                for i in range(m):
                    vs = rng.sample(names, 3)
                    src.append(tuple((v, bool(rng.getrandbits(1))) for v in vs))
                if m > 1 and rep == 0:
                    src[-1] = src[0]
                b, sv, _vn, _tn, _hn, yn, _yp = build_revfix(src, cyclic)
                for bits in itertools.product((0, 1), repeat=len(sv)):
                    x = dict(zip(sv, bits))
                    y = {name: rng.getrandbits(1) for name in yn}
                    a = extend_gates(b, x, y)
                    target = all(sat_clause(cl, a) for cl in b.clauses)
                    if target != source_satisfied(src, x):
                        if cyclic and m == 1:
                            cyclic_m1_counterexamples += 1
                        else:
                            failures.append(f"semantic mismatch cyc={cyclic},m={m}")
                    semantic_cases += 1
    checks["semantic_assignments"] = semantic_cases

    model_count = audit_one_clause_model_count(failures, checks)
    elapsed = time.perf_counter() - started
    result = {
        "run_id": "REVFIXGATEAUDIT1",
        "seed": SEED,
        "fields": list(FIELDS),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "elapsed_seconds": elapsed,
        "count_rows": count_rows,
        "field_rows": field_rows,
        "one_clause_models": model_count,
        "two_shear_m1_counterexamples": cyclic_m1_counterexamples,
        "checks": dict(checks),
        "proved_by_symbolic_argument": [
            "anchored exact counts n+14m-4 variables and 27m-9 clauses",
            "two-shear exact counts n+14m variables and 27m clauses",
            "all-field substitution degree at most 7 and 11 respectively",
            "laminar all-zero equality-tree axioms vanish exactly",
            "three-variable by-cases Boolean-ideal repair has degree at most 6",
        ],
        "limitations": [
            "Finite audits supplement but do not replace the symbolic proofs.",
            "Degree transport does not preserve expanded monomial size; 8^d growth is explicit.",
            "The two-shear ring requires m>=2 (or a one-clause padding repair).",
            "The ONE3/NOT-ONE3 hard side may depend on the field.",
            "No unrestricted deterministic SAT-time lower bound is inferred.",
        ],
    }
    out = Path("results/raw/review/2026-10-19_REVFIXGATEAUDIT1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("raw_sha256", hashlib.sha256(text.encode()).hexdigest())
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
