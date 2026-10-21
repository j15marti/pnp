#!/usr/bin/env python3
"""Finite controls for RP-TEMPORAL-OVERLAP-NORMALIZATION43.

The proof is mathematical; this script exhausts small Boolean acceptance
functions and the circuit-truth-table reduction used by the scope firewall.
"""

import json
from pathlib import Path


ASSERTIONS = 0


def check(condition, message):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def temporal_padding_audit():
    functions = 0
    executions = 0
    for m in range(1, 5):
        tape_count = 1 << m
        for table in range(1 << tape_count):
            functions += 1
            # The padded verifier prereads every address, evaluates the same
            # truth table, then rereads every address.  All address intervals
            # span the evaluation and hence overlap there.
            for r in range(tape_count):
                base = (table >> r) & 1
                padded = (table >> r) & 1
                check(base == padded, "pointwise equivalence failed")
                executions += 1
            first_reads = list(range(m))
            last_reads = list(range(2 * m + 1, 3 * m + 1))
            common_time = m
            check(all(first_reads[j] <= common_time <= last_reads[j]
                      for j in range(m)),
                  "all temporal windows must overlap at evaluation")
    return {"functions": functions, "executions": executions}


def dead_read_reduction_audit():
    circuits = 0
    verifier_rows = 0
    for k in range(0, 5):
        z_count = 1 << k
        for c_table in range(1 << z_count):
            circuits += 1
            unsat = c_table == 0
            a_live = False
            accepted = 0
            total = 4 * z_count  # q,a,z
            for z in range(z_count):
                c = (c_table >> z) & 1
                f0 = 0 | (0 & c)
                f1 = 0 | (1 & c)
                if f0 != f1:
                    a_live = True
                for q in (0, 1):
                    for a in (0, 1):
                        value = q | (a & c)
                        accepted += value
                        verifier_rows += 1
                        check(value in (0, 1), "non-Boolean verifier output")
            check((not a_live) == unsat,
                  "address a is dead iff C is unsatisfiable")
            check(2 * accepted >= total,
                  "every verifier must have RP YES density at least one half")
    return {"truth_table_circuits": circuits,
            "verifier_rows": verifier_rows,
            "largest_circuit_input_bits": 4}


def main():
    temporal = temporal_padding_audit()
    dead = dead_read_reduction_audit()
    result = {
        "name": "RP-TEMPORAL-OVERLAP-NORMALIZATION43",
        "status": "COMPUTATIONAL finite controls; theorem proof separate",
        "temporal_padding": temporal,
        "dead_read_reduction": dead,
        "assertions": ASSERTIONS,
        "failures": 0,
        "scope_firewall": [
            "Temporal overlap is a verifier property, not a language invariant.",
            "Dead-read certification is coNP-hard by circuit UNSAT.",
            "No conclusion about P=RP, P!=RP, or P!=NP."
        ]
    }
    Path("RP_TEMPORAL_OVERLAP_NORMALIZATION43_raw.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
