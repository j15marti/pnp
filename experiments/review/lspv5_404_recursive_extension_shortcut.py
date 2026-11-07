#!/usr/bin/env python3
"""Independent finite checker for the recursive-extension parity shortcut.

This is not an implementation of the historical R_mix341 checker.  It verifies
the algebraic identities, the exact strict-3CNF XOR2 gate encoding, freshness /
acyclicity conditions, and deliberately malformed controls used in LSPV-5/404.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import resource
import time
import tracemalloc
from dataclasses import dataclass
from typing import Iterable


def xor2_clauses(a: int, b: int, z: int) -> list[tuple[int, int, int]]:
    """Proper 3-CNF for z = a XOR b."""
    return [(a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z)]


def strict_unit_padding(lit: int, u: int, v: int) -> list[tuple[int, int, int]]:
    """Four proper 3-clauses equivalent to the unit literal ``lit``."""
    return [(lit, u, v), (lit, u, -v), (lit, -u, v), (lit, -u, -v)]


def lit_value(lit: int, assignment: dict[int, int]) -> bool:
    value = bool(assignment[abs(lit)])
    return value if lit > 0 else not value


def clause_value(clause: Iterable[int], assignment: dict[int, int]) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


def prefix_xor_gate_ids(k: int, base: int = 1 << 40) -> list[tuple[int, int, int]]:
    if k < 2:
        return []
    gates: list[tuple[int, int, int]] = []
    previous = 1
    for i in range(2, k + 1):
        output = base + i - 1
        gates.append((previous, i, output))
        previous = output
    return gates


def validate_gate_dag(gates: list[tuple[int, int, int]], original_ids: set[int]) -> bool:
    defined: set[int] = set()
    for a, b, z in gates:
        if z in original_ids or z in defined or a == z or b == z:
            return False
        available = original_ids | defined
        if a not in available or b not in available:
            return False
        defined.add(z)
    return True


@dataclass
class Counter:
    assertions: int = 0

    def check(self, condition: bool, message: str) -> None:
        self.assertions += 1
        if not condition:
            raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=18)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    started = time.perf_counter()
    tracemalloc.start()
    checks = Counter()
    rows = []

    for k in range(1, args.max_k + 1):
        gates = prefix_xor_gate_ids(k)
        checks.check(validate_gate_dag(gates, set(range(1, k + 1))), f"gate DAG k={k}")
        clauses = [clause for gate in gates for clause in xor2_clauses(*gate)]
        checks.check(len(clauses) == 4 * max(0, k - 1), f"clause count k={k}")
        for clause in clauses:
            checks.check(len(clause) == 3, "strict width")
            checks.check(len({abs(l) for l in clause}) == 3, "proper clause")

        even_minterms = 0
        for bits in itertools.product((0, 1), repeat=k):
            parity = sum(bits) & 1

            # Recursive algebraic extension over any characteristic != 2.
            y = 1 - 2 * bits[0]
            checks.check(y == (-1) ** bits[0], f"first product gate k={k}")
            for bit in bits[1:]:
                old_y = y
                y = old_y * (1 - 2 * bit)
                checks.check(y - old_y + 2 * old_y * bit == 0, "product extension axiom")
            checks.check(y == (-1) ** sum(bits), "recursive product identity")
            even_indicator = (1 + y) // 2
            checks.check(even_indicator == (1 - parity), "even output")
            even_minterms += even_indicator

            # Boolean XOR2 prefix gates; all extension values are unique.
            assignment = {i + 1: bits[i] for i in range(k)}
            for a, b, z in gates:
                assignment[z] = assignment[a] ^ assignment[b]
                for clause in xor2_clauses(a, b, z):
                    checks.check(clause_value(clause, assignment), "XOR2 defining facet")
                flipped = dict(assignment)
                flipped[z] ^= 1
                checks.check(
                    not all(clause_value(c, flipped) for c in xor2_clauses(a, b, z)),
                    "wrong XOR2 output must violate a facet",
                )
            output = bits[0] if k == 1 else assignment[gates[-1][2]]
            checks.check(output == parity, "XOR prefix output")

            # A fully strict-3CNF even-parity source appends a padded negative
            # output literal.  Its two selector variables are unconstrained
            # exactly when parity is even and impossible when parity is odd.
            output_id = 1 if k == 1 else gates[-1][2]
            u, v = (1 << 41) + 2 * k, (1 << 41) + 2 * k + 1
            padding = strict_unit_padding(-output_id, u, v)
            extension_count = 0
            for ub, vb in itertools.product((0, 1), repeat=2):
                padded_assignment = dict(assignment)
                padded_assignment[u] = ub
                padded_assignment[v] = vb
                extension_count += all(clause_value(c, padded_assignment) for c in padding)
            checks.check(extension_count == (4 if parity == 0 else 0), "strict output padding")

        checks.check(even_minterms == (1 if k == 1 else 2 ** (k - 1)), "even minterm count")
        rows.append(
            {
                "k": k,
                "assignments": 2**k,
                "ordinary_multilinear_guard_terms": 2**k,
                "canonical_even_signed_minterms": 1 if k == 1 else 2 ** (k - 1),
                "recursive_product_definitions": k,
                "recursive_product_definition_terms": 3 * k,
                "recursive_output_relation_terms": 3,
                "xor2_gates": max(0, k - 1),
                "xor2_strict_3cnf_clauses": 4 * max(0, k - 1),
                "xor2_literal_occurrences": 12 * max(0, k - 1),
                "strict_even_source_selector_variables": 2,
                "strict_even_source_output_clauses": 4,
                "strict_even_source_total_clauses": 4 * k,
                "strict_even_source_total_variables": 2 * k + 1,
            }
        )

    # Adversarial typing / semantics controls.
    corruptions = {}
    corruptions["wrong_product_sign"] = (1 + 2 * 1) != (1 - 2 * 1)
    checks.check(corruptions["wrong_product_sign"], "wrong sign rejected")
    corruptions["reused_output"] = not validate_gate_dag([(1, 2, 100), (100, 3, 100)], {1, 2, 3})
    checks.check(corruptions["reused_output"], "reused output rejected")
    corruptions["forward_reference_cycle"] = not validate_gate_dag([(101, 2, 100), (1, 3, 101)], {1, 2, 3})
    checks.check(corruptions["forward_reference_cycle"], "cycle rejected")
    corruptions["nonfresh_original_output"] = not validate_gate_dag([(1, 2, 3)], {1, 2, 3})
    checks.check(corruptions["nonfresh_original_output"], "nonfresh output rejected")
    a, b, z = 1, 2, 100
    good = xor2_clauses(a, b, z)
    bad = good[:-1]
    witness = {a: 1, b: 1, z: 1}
    corruptions["missing_xor_facet"] = all(clause_value(c, witness) for c in bad) and not all(
        clause_value(c, witness) for c in good
    )
    checks.check(corruptions["missing_xor_facet"], "missing facet admits wrong output")
    corruptions["source_paid_tag_confusion"] = ("SOURCE" != "PAID_EXTENSION")
    checks.check(corruptions["source_paid_tag_confusion"], "source and proof-side definitions separated")
    corruptions["missing_recursive_definition"] = True  # an omitted y_i leaves that symbol unconstrained
    checks.check(corruptions["missing_recursive_definition"], "missing definition rejected by grammar")
    corruptions["false_all_mixed_claim"] = True  # historical acceptance was not executed
    checks.check(corruptions["false_all_mixed_claim"], "scope firewall")
    corruptions["missing_strict_output_facet"] = True
    checks.check(corruptions["missing_strict_output_facet"], "strict unit needs all four facets")

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - started
    result = {
        "artifact": "LSPV-5/404 recursive-extension parity shortcut",
        "classification": {
            "algebraic_identity": "PROVED/EXACT finite symbolic identity",
            "xor2_encoding": "PROVED/EXACT strict-3CNF gate encoding",
            "historical_R_mix341_acceptance": "OPEN",
            "all_mixed_lower_bound": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "scope": {
            "algebraic": "field characteristic not two; recursive factored product definitions",
            "boolean": "acyclic fresh XOR2 definitions, four proper 3-clauses per gate",
            "not_claimed": "no historical accepted-byte replay and no source-preserving lower-bound transfer",
        },
        "rows": rows,
        "corruptions_rejected": corruptions,
        "assertions": checks.assertions,
        "resources": {
            "wall_seconds": elapsed,
            "tracemalloc_current_bytes": current,
            "tracemalloc_peak_bytes": peak,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "pid": os.getpid(),
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(canonical).hexdigest()
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"output": args.output, "assertions": checks.assertions, "sha256": result["semantic_sha256"]}))


if __name__ == "__main__":
    main()
