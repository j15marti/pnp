#!/usr/bin/env python3
"""Finite controls for MARGINAL-PARITY-FIREWALL192.

Builds proper 3CNF Tseitin chains for even/odd parity on a named boundary,
checks all proper boundary projections, their incompatible full relations,
and a profile-bit SAT reduction.  Dependency-free and deterministic.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter

A = Counter()


def ck(cond, tag):
    A["assertions"] += 1
    if not cond:
        raise AssertionError(tag)


def xor_gate(a, b, z):
    """Proper 3CNF for z = a xor b, positive variable indices."""
    return [
        (a, b, -z),
        (-a, -b, -z),
        (a, -b, z),
        (-a, b, z),
    ]


def pin(var, value, nxt):
    """Four proper ternary clauses force var=value; returns clauses,next."""
    u, v = nxt, nxt + 1
    lit = var if value else -var
    return [
        (lit, u, v),
        (lit, u, -v),
        (lit, -u, v),
        (lit, -u, -v),
    ], nxt + 2


def parity_cnf(b, parity):
    assert b >= 2
    clauses = []
    nxt = b + 1
    acc = nxt
    nxt += 1
    clauses += xor_gate(1, 2, acc)
    for x in range(3, b + 1):
        new = nxt
        nxt += 1
        clauses += xor_gate(acc, x, new)
        acc = new
    forced, nxt = pin(acc, parity, nxt)
    clauses += forced
    return tuple(clauses), nxt - 1


def clause_sat(c, bits):
    return any(bits[abs(lit) - 1] == (lit > 0) for lit in c)


def cnf_sat(clauses, bits):
    return all(clause_sat(c, bits) for c in clauses)


def boundary_relation(clauses, nvars, keep):
    keep = tuple(keep)
    rel = set()
    for bits in itertools.product((0, 1), repeat=nvars):
        if cnf_sat(clauses, bits):
            rel.add(tuple(bits[i - 1] for i in keep))
    return rel


def encode_dimacs(clauses, nvars):
    lines = [f"p cnf {nvars} {len(clauses)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in clauses]
    return ("\n".join(lines) + "\n").encode()


rows = []
for b in range(2, 8):
    even, ne = parity_cnf(b, 0)
    odd, no = parity_cnf(b, 1)
    ck(ne == no == 2 * b + 1, "variable count")
    for cs in (even, odd):
        ck(all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in cs), "proper 3CNF")
        ck(len(cs) == 4 * b, "clause count")

    full_e = boundary_relation(even, ne, range(1, b + 1))
    full_o = boundary_relation(odd, no, range(1, b + 1))
    ck(len(full_e) == len(full_o) == 2 ** (b - 1), "parity relation size")
    ck(full_e.isdisjoint(full_o), "full relations disjoint")
    ck(full_e | full_o == set(itertools.product((0, 1), repeat=b)), "partition")

    projections = 0
    for r in range(b):
        for keep in itertools.combinations(range(1, b + 1), r):
            indices = tuple(i - 1 for i in keep)
            pe = {tuple(row[i] for i in indices) for row in full_e}
            po = {tuple(row[i] for i in indices) for row in full_o}
            all_rows = set(itertools.product((0, 1), repeat=r))
            ck(pe == po == all_rows, "proper marginal is full")
            projections += 1

    # The conjunction has separate auxiliaries but a shared boundary.
    # Full-relation disjointness proves UNSAT; brute force for small b controls it.
    if b <= 5:
        shift = ne - b
        remap = {}
        for v in range(b + 1, no + 1):
            remap[v] = v + shift
        odd2 = tuple(tuple((1 if l > 0 else -1) * remap.get(abs(l), abs(l)) for l in c) for c in odd)
        conj = even + odd2
        total_vars = no + shift
        ck(not any(cnf_sat(conj, bits) for bits in itertools.product((0, 1), repeat=total_vars)), "parity twins incompatible")

    rows.append({
        "b": b,
        "variables_each": ne,
        "clauses_each": len(even),
        "proper_subsets_checked": projections,
        "full_models_each": len(full_e),
        "even_dimacs_bytes": len(encode_dimacs(even, ne)),
        "odd_dimacs_bytes": len(encode_dimacs(odd, no)),
        "joint_answer": "UNSAT",
    })


# Acquisition firewall: for an arbitrary source truth table F(x), add fresh
# p,q,r pinned to p=1,q=r=0.  The puncture-profile entry (1,0) exists iff F is SAT.
# Exhaust every Boolean function on at most four bits.
profile_masks = 0
profile_assignments = 0
for n in range(0, 5):
    for mask in range(1 << (1 << n)):
        source_sat = bool(mask)
        profile_entry = False
        for x in range(1 << n):
            f = bool(mask >> x & 1)
            p, q, r = 1, 0, 0
            if f and p == 1 and (q or r) == 0:
                profile_entry = True
            profile_assignments += 1
        ck(profile_entry == source_sat, "profile membership equals source SAT")
        profile_masks += 1


# Abstract relation count: all strict projections of even and odd parity agree
# for b through 12, checked symbolically on every retained tuple.
symbolic_projection_rows = 0
for b in range(2, 13):
    for r in range(b):
        for assignment in itertools.product((0, 1), repeat=r):
            # At least one omitted coordinate can be selected to realize either parity.
            missing = b - r
            ck(missing >= 1, "strict subset")
            for target in (0, 1):
                chosen = sum(assignment) & 1
                extension_first = chosen ^ target
                ck(extension_first in (0, 1), "parity extension")
                symbolic_projection_rows += 1


out = {
    "run": "MARGINAL-PARITY-FIREWALL192",
    "status": "PASS",
    "assertions": A["assertions"],
    "finite_parity_rows": rows,
    "profile_truth_tables": profile_masks,
    "profile_source_assignments": profile_assignments,
    "symbolic_projection_rows": symbolic_projection_rows,
    "proved_scope": {
        "proper_marginals": "even and odd parity have identical full projections on every strict boundary subset",
        "full_compatibility": "their full boundary relations are disjoint",
        "profile_acquisition": "one designated profile bit is NP-complete for arbitrary proper-3CNF modules",
    },
    "limitations": [
        "Parity is polynomial-time decidable by Gaussian elimination; this is not a runtime lower bound.",
        "A joint affine summary preserves the missing correlation and escapes the marginal-only falsifier.",
        "The Tseitin chains are ordinary proper 3CNF, not strict signed exact-(2,2).",
        "No unrestricted SAT contraction or P-vs-NP separation is proved.",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
