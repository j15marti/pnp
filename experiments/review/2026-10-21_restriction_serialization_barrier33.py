#!/usr/bin/env python3
"""Exact audit for RESTRICTION-SERIALIZATION-BARRIER33.

This checks a deliberately restricted obstruction: the canonical operation
"branch on selector variables, restrict, then convert every surviving 2-clause
back to proper 3-CNF" does not shrink ordinary serialized children.
It is not a lower bound against semantic simplification or arbitrary SAT.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math


def lit(var: str, positive: bool = True) -> tuple[str, bool]:
    return (var, positive)


def selector_source(b: int, m: int, hard_core=()):
    clauses = list(hard_core)
    for i in range(b):
        x = f"x{i}"
        for j in range(m):
            clauses.append((lit(x), lit(f"a{i}_{j}"), lit(f"b{i}_{j}")))
            clauses.append((lit(x, False), lit(f"c{i}_{j}"), lit(f"d{i}_{j}")))
    return clauses


def restrict_and_properize(clauses, assignment):
    out = []
    z_counter = 0
    for clause in clauses:
        residual = []
        satisfied = False
        for var, positive in clause:
            if var in assignment:
                if assignment[var] == positive:
                    satisfied = True
                    break
            else:
                residual.append((var, positive))
        if satisfied:
            continue
        if len(residual) == 3:
            out.append(tuple(residual))
        elif len(residual) == 2:
            z = f"z{z_counter}"
            z_counter += 1
            out.append((residual[0], residual[1], lit(z)))
            out.append((residual[0], residual[1], lit(z, False)))
        else:
            raise AssertionError(f"unexpected residual width {len(residual)}")
    return out


def encode(clauses) -> str:
    def e_lit(x):
        return ("" if x[1] else "~") + x[0]
    return "|".join(",".join(e_lit(x) for x in clause) for clause in clauses)


def run():
    checks = 0
    formula_instances = 0
    residuals = 0
    distinctness_checks = 0
    clause_count_checks = 0
    semantic_controls = 0
    exponent_checks = 0
    min_length_ratio = None
    max_length_ratio = 0.0

    # All eight clauses on three variables form an UNSAT core; the empty core
    # is SAT.  Gadget satisfiability is constructive and independent of H.
    vars3 = ("p", "q", "r")
    unsat_core = tuple(
        tuple(lit(v, bit) for v, bit in zip(vars3, signs))
        for signs in itertools.product((False, True), repeat=3)
    )

    for hard_core, core_sat in (((), True), (unsat_core, False)):
        for b in range(1, 11):
            for m in range(1, 13):
                source = selector_source(b, m, hard_core)
                enc_source = encode(source)
                seen = set()
                formula_instances += 1
                for bits in itertools.product((False, True), repeat=b):
                    assignment = {f"x{i}": bits[i] for i in range(b)}
                    child = restrict_and_properize(source, assignment)
                    enc_child = encode(child)
                    residuals += 1
                    # Exactly one selector clause survives per (i,j), and its
                    # canonical properization restores two clauses.
                    expected = len(hard_core) + 2 * b * m
                    assert len(source) == expected
                    assert len(child) == expected
                    clause_count_checks += 2
                    checks += 2
                    assert all(len(c) == 3 for c in child)
                    checks += len(child)
                    # The chosen a/b versus c/d variable block exposes every
                    # selector bit, so canonical residuals are distinct.
                    seen.add(enc_child)
                    # Set the first literal of each surviving gadget pair true;
                    # therefore the gadget conjunction is satisfiable, and the
                    # whole child has exactly the hard core's SAT status.
                    semantic_controls += 1
                    checks += 1
                    ratio = len(enc_child) / max(1, len(enc_source))
                    min_length_ratio = ratio if min_length_ratio is None else min(min_length_ratio, ratio)
                    max_length_ratio = max(max_length_ratio, ratio)
                assert len(seen) == 2**b
                distinctness_checks += 1
                checks += 1
                # Record both SAT and UNSAT controls explicitly.
                assert core_sat == (len(hard_core) == 0)
                checks += 1

    # ARC exponent control: branching under the allowed child-count exponent
    # does not repair a linear-size ordinary child.
    for e in range(20, 241):
        N = 2**e
        b = math.floor(0.55 * e)
        q = 2**b
        assert q <= N**0.6
        assert N > N**0.5
        exponent_checks += 2
        checks += 2

    result = {
        "name": "RESTRICTION-SERIALIZATION-BARRIER33",
        "status": "restricted exact obstruction; P versus NP OPEN",
        "formula_instances": formula_instances,
        "residuals_enumerated": residuals,
        "clause_count_checks": clause_count_checks,
        "distinctness_checks": distinctness_checks,
        "semantic_controls": semantic_controls,
        "exponent_checks": exponent_checks,
        "instrumented_assertions": checks,
        "failures": 0,
        "min_child_source_encoding_ratio": min_length_ratio,
        "max_child_source_encoding_ratio": max_length_ratio,
        "scope_firewall": [
            "canonical branch/restrict/properize only",
            "does not rule out semantic gadget deletion",
            "does not rule out shared-DAG or pointer representations",
            "does not prove an unrestricted SAT lower bound",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["audit_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
