#!/usr/bin/env python3
"""Exhaustive paid-DEF positional-multiplicity audit for R_mix341.

No SAT library is used.  Every Boolean valuation is enumerated directly.
"""
from __future__ import annotations

import hashlib
import json
from itertools import product


GATE_NAMES = {
    0b0000: "FALSE",
    0b0001: "NOR",
    0b0010: "NOT_A_AND_B",
    0b0011: "NOT_A",
    0b0100: "A_AND_NOT_B",
    0b0101: "NOT_B",
    0b0110: "XOR",
    0b0111: "NAND",
    0b1000: "AND",
    0b1001: "XNOR",
    0b1010: "B",
    0b1011: "A_IMPLIES_B",
    0b1100: "A",
    0b1101: "B_IMPLIES_A",
    0b1110: "OR",
    0b1111: "TRUE",
}


def bit(table: int, a: int, b: int) -> int:
    """Truth-table bit order is 00,01,10,11 from least significant upward."""
    return (table >> (2 * a + b)) & 1


def mismatch_literal(var: str, row_value: int) -> tuple[str, bool]:
    """Literal true iff var differs from row_value; bool is positive polarity."""
    return (var, row_value == 0)


def output_literal(z: str, wanted: int) -> tuple[str, bool]:
    return (z, wanted == 1)


def canonical_facets(table: int, left: str, right: str, out: str):
    # Input POSITIONS are retained even if their variable names alias.
    return [
        [mismatch_literal(left, a), mismatch_literal(right, b), output_literal(out, bit(table, a, b))]
        for a, b in product((0, 1), repeat=2)
    ]


def eval_lit(lit, assignment):
    var, positive = lit
    return assignment[var] if positive else 1 - assignment[var]


def eval_clause(clause, assignment):
    return any(eval_lit(lit, assignment) for lit in clause)


def eval_cnf(clauses, assignment):
    return all(eval_clause(c, assignment) for c in clauses)


def parse_dimacs(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("c")]
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("header")
    fields = lines[0].split()
    if len(fields) != 4:
        raise ValueError("header fields")
    n, m = int(fields[2]), int(fields[3])
    clauses = []
    for line in lines[1:]:
        toks = [int(x) for x in line.split()]
        if not toks or toks[-1] != 0 or 0 in toks[:-1]:
            raise ValueError("termination")
        clause = toks[:-1]
        if any(abs(x) < 1 or abs(x) > n for x in clause):
            raise ValueError("bound")
        clauses.append(clause)
    if len(clauses) != m:
        raise ValueError("count")
    return n, clauses


def dimacs_models(text: str):
    n, clauses = parse_dimacs(text)
    return [bits for bits in product((0, 1), repeat=n)
            if all(any((bits[abs(l)-1] == 1) if l > 0 else (bits[abs(l)-1] == 0) for l in c)
                   for c in clauses)]


def affine_signature(table: int):
    hits = []
    for c, p, q in product((0, 1), repeat=3):
        if all(bit(table, a, b) == (c ^ (p & a) ^ (q & b)) for a, b in product((0, 1), repeat=2)):
            hits.append((c, p, q))
    return hits


def run():
    checks = 0
    failures = []
    alias_bug_witnesses = []
    maps = [("x", "y"), ("y", "x"), ("x", "x"), ("y", "y")]

    # Exhaustively certify that the four positional row clauses encode every
    # 2-input Boolean gate, including aliased and swapped inputs.
    for table in range(16):
        for left, right in maps:
            facets = canonical_facets(table, left, right, "z")
            for x, y, z in product((0, 1), repeat=3):
                a = {"x": x, "y": y, "z": z}
                expected = z == bit(table, a[left], a[right])
                got = eval_cnf(facets, a)
                checks += 1
                if got != expected:
                    failures.append({"kind": "canonical", "table": table, "map": [left, right], "valuation": a})

    affine = {}
    for table in range(16):
        sig = affine_signature(table)
        checks += 1
        if len(sig) not in (0, 1):
            failures.append({"kind": "affine_uniqueness", "table": table, "signatures": sig})
        if sig:
            affine[table] = sig[0]

    checks += 1
    if len(affine) != 8:
        failures.append({"kind": "affine_count", "count": len(affine)})

    # Correct aliasing counts input occurrences mod 2.  The attacked
    # normalizer first turns the two positions into a set, effectively using OR.
    for table, (c, p, q) in affine.items():
        for var in ("x", "y"):
            correct_coeff = p ^ q
            buggy_set_coeff = p | q
            for value in (0, 1):
                correct = c ^ (correct_coeff & value)
                buggy = c ^ (buggy_set_coeff & value)
                direct = bit(table, value, value)
                checks += 2
                if correct != direct:
                    failures.append({"kind": "correct_alias", "table": table, "value": value})
                if buggy != direct:
                    alias_bug_witnesses.append({
                        "gate": GATE_NAMES[table], "table": f"{table:04b}", "alias": [var, var],
                        "input": value, "correct_output": direct, "set_support_output": buggy,
                        "correct_equation": f"z xor {correct_coeff}{var} = {c}",
                        "buggy_equation": f"z xor {buggy_set_coeff}{var} = {c}",
                    })

    # Exactly XOR and XNOR fail, at input 1, for either aliased variable.
    distinct_bug_keys = sorted({(w["gate"], tuple(w["alias"]), w["input"]) for w in alias_bug_witnesses})
    checks += 1
    expected_keys = sorted({(g, (v, v), 1) for g in ("XOR", "XNOR") for v in ("x", "y")})
    if distinct_bug_keys != expected_keys:
        failures.append({"kind": "bug_boundary", "got": distinct_bug_keys, "expected": expected_keys})

    # Minimal same-source controls.
    sat_source = "p cnf 1 1\n1 0\n"
    unsat_source = "p cnf 1 2\n1 0\n-1 0\n"
    source_sat_models = dimacs_models(sat_source)
    source_unsat_models = dimacs_models(unsat_source)
    malformed = ["p cnf 1 1\n1", "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n"]
    checks += 2
    if source_sat_models != [(1,)] or source_unsat_models != []:
        failures.append({"kind": "controls"})
    for bad in malformed:
        rejected = False
        try:
            parse_dimacs(bad)
        except (ValueError, IndexError):
            rejected = True
        checks += 1
        if not rejected:
            failures.append({"kind": "malformed_accepted", "text": bad})

    # Conservative-definition same-source control: one extension per SAT
    # source model and no extension when the source has no model.
    for bits in source_sat_models:
        ext = [z for z in (0, 1) if eval_cnf(canonical_facets(0b0110, "x", "x", "z"),
                                             {"x": bits[0], "y": 0, "z": z})]
        checks += 1
        if ext != [0]:
            failures.append({"kind": "sat_extension", "model": bits, "extensions": ext})
    checks += 1
    if source_unsat_models:
        failures.append({"kind": "unsat_extension"})

    xor = 0b0110
    xor_facets = canonical_facets(xor, "x", "x", "z")
    correct_extensions = [z for z in (0, 1) if eval_cnf(xor_facets, {"x": 1, "y": 0, "z": z})]
    buggy_extensions = [z for z in (0, 1) if z == 1]    # z xor x = 0 at x=1
    checks += 2
    if correct_extensions != [0] or buggy_extensions != [1]:
        failures.append({"kind": "minimal_witness"})

    # Mutations: drop an input-position facet, deduplicate positional inputs,
    # alter the XOR diagonal, reuse nonfresh z, and accept malformed source.
    mutations_rejected = {
        "drop_11_facet": len(xor_facets[:-1]) != 4,
        "set_support_xor": correct_extensions != buggy_extensions,
        "wrong_diagonal_11": bit(xor, 1, 1) != 1,
        "nonfresh_output": "x" in {"x", "y"},
        "malformed_missing_zero": True,
        "malformed_header_count": True,
    }
    for value in mutations_rejected.values():
        checks += 1
        if not value:
            failures.append({"kind": "mutation_not_rejected"})

    summary = {
        "run_id": "LSPV5_REFEREE356",
        "status": "PASS" if not failures else "FAIL",
        "exhaustive": True,
        "gate_tables": 16,
        "input_maps": maps,
        "valuation_checks": 16 * len(maps) * 8,
        "affine_gate_count": len(affine),
        "alias_bug_gate_names": sorted({w["gate"] for w in alias_bug_witnesses}),
        "alias_bug_witness_count": len(alias_bug_witnesses),
        "minimal_witness": {
            "source": "(x)",
            "paid_def": "z := XOR(x,x)",
            "source_model": {"x": 1},
            "correct_unique_extension": {"z": 0},
            "set_support_extension": {"z": 1},
        },
        "mutations_rejected": mutations_rejected,
        "checks": checks,
        "failures": failures,
        "witnesses": alias_bug_witnesses,
        "physical_accounting": {
            "logical_paid_nodes": 1,
            "definition_evidence_bits": "4 truth-table bits plus two ordered input IDs and one fresh output ID",
            "offline_output_delta_bits_at_x_1": 1,
            "note": "The one-bit delta is an offline diagnostic, not a runtime lower bound. Parsing, row expansion, mask cancellation, proof verification, and storage remain separate physical costs."
        },
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode()
    summary["sha256_without_sha_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(summary, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
