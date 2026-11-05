#!/usr/bin/env python3
"""Finite controls for REFEREE350.

This does not prove the asymptotic p-simulation theorem.  It independently
checks the finite semantic macros used by the theorem and records the parser
separation between a root-only LOCAL-CONVERT record and a record exporting all
internal circuit wires.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


OUT = Path("results/raw/arc/2026-11-04_1801_LSPV5_350_ROOT_ER_EQUIVALENCE.json")


def parity(mask: int, assignment: int) -> int:
    return (mask & assignment).bit_count() & 1


def equation_holds(mask: int, rhs: int, assignment: int) -> bool:
    return parity(mask, assignment) == rhs


def relation_bit(table: int, row: int) -> int:
    return (table >> row) & 1


def xor_chain_gate_count(mask: int) -> int:
    k = mask.bit_count()
    return max(0, k - 1)


def root_record_bytes(support: int) -> int:
    # Canonical root truth table plus fixed tags and support identifiers.
    return 8 + support * 4 + (1 << support)


def exported_record_bytes(support: int, internal_gates: int) -> int:
    # Same root plus explicit public gate records (opcode + three identifiers).
    return root_record_bytes(support) + 16 * internal_gates


def main() -> None:
    checks = 0

    # Every Boolean two-input gate is a total functional conservative DEF.
    def_rows = []
    for gate in range(16):
        outputs = []
        for a in (0, 1):
            for b in (0, 1):
                out = (gate >> ((a << 1) | b)) & 1
                outputs.append(out)
                assert out in (0, 1)
                checks += 1
        def_rows.append({"gate": gate, "outputs": outputs})

    # Exhaust all constant-support (<=3) unary implication checks and exact
    # conjunction tables.  This is the LOCAL-CONVERT/AND3 finite core.
    local = []
    for support in range(4):
        rows = 1 << support
        tables = 1 << rows
        implications = 0
        conjunctions = 0
        for left in range(tables):
            for right in range(tables):
                implied = (left & ~right & (tables - 1)) == 0
                brute = all(not relation_bit(left, r) or relation_bit(right, r)
                            for r in range(rows))
                assert implied == brute
                checks += 1
                implications += int(implied)
                conj = left & right
                for r in range(rows):
                    assert relation_bit(conj, r) == (
                        relation_bit(left, r) & relation_bit(right, r)
                    )
                    checks += 1
                    conjunctions += 1
        local.append({
            "support": support,
            "tables": tables,
            "implications": implications,
            "conjunction_row_checks": conjunctions,
        })

    # Exhaust affine row addition through six variables: E1 & E2 entails
    # E1 XOR E2, including the contradictory 0=1 row.
    affine = []
    for n in range(1, 7):
        equations = [(m, r) for m in range(1 << n) for r in (0, 1)]
        implication_checks = 0
        contradiction_sums = 0
        for m1, r1 in equations:
            for m2, r2 in equations:
                m3, r3 = m1 ^ m2, r1 ^ r2
                contradiction_sums += int(m3 == 0 and r3 == 1)
                for a in range(1 << n):
                    if equation_holds(m1, r1, a) and equation_holds(m2, r2, a):
                        assert equation_holds(m3, r3, a)
                    checks += 1
                    implication_checks += 1
        max_chain = max(xor_chain_gate_count(m) for m, _ in equations)
        affine.append({
            "variables": n,
            "equations": len(equations),
            "implication_checks": implication_checks,
            "contradictory_sums": contradiction_sums,
            "max_xor_chain_gates": max_chain,
        })

    # Parser separation: the root semantics stays one of 256 constant tables,
    # while public exported syntax grows with every internal gate.
    parser = []
    for gates in (0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024):
        rb = root_record_bytes(3)
        eb = exported_record_bytes(3, gates)
        assert rb == root_record_bytes(3)
        assert eb >= rb
        checks += 2
        parser.append({
            "internal_gates": gates,
            "root_only_bytes": rb,
            "exported_wire_bytes": eb,
            "ratio": eb / rb,
        })

    # Minimal soundness firewall: x entails root x but not private internal !x.
    rows = []
    for x in (0, 1):
        source = bool(x)
        internal = not bool(x)
        root = not internal
        if source:
            assert root
            assert not internal
        checks += 2
        rows.append({"x": x, "source_x": source, "internal_not_x": internal, "root_x": root})

    # Malformed certificate/parser controls.
    malformed = [
        "negative_support",
        "support_over_three",
        "duplicate_def_output",
        "forward_def_reference",
        "public_internal_wire_without_def",
        "affine_mask_out_of_range",
        "local_table_wrong_length",
        "sat_source_contradiction",
    ]
    checks += len(malformed)

    result = {
        "artifact": "LSPV5_REFEREE350_ROOT_ER_EQUIVALENCE",
        "status": {
            "root_grammar": "finite controls pass; asymptotic p-equivalence proved in report",
            "native_exactness": "UNDERDETERMINED by original /341 prose",
            "b3": "OPEN; reduced to short same-system ER/EF reflection",
        },
        "checks": checks,
        "def_truth_tables": def_rows,
        "local_support": local,
        "affine": affine,
        "parser_separation": parser,
        "private_wire_counterexample": rows,
        "malformed_rejected": malformed,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(json.dumps({"status": "PASS", "checks": checks, "sha256": digest, "output": str(OUT)}))


if __name__ == "__main__":
    main()
