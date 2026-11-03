#!/usr/bin/env python3
"""Rmix341 seven-node exclusion for authentic rsmu_5_7_1.cnf.

The exhaustive lower certificate reuses the independently specified relaxed
tree/unicycle search of REFEREE301.  Search work is external certification and
is not charged to the freely selected minimum derivation cost.
"""

from __future__ import annotations

import hashlib
import json
import platform
import resource
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from experiments.arc.lspv5_300.peitl_mixed_floor_referee300 import (
    malformed_controls,
    model_count,
    parity_cnf_k4,
    parse_dimacs,
    sign_flip_counts,
)
from experiments.arc.lspv5_301.peitl_exact_six_referee301 import (
    canonical_clause,
    reject_corruptions,
    relaxed_unicycle_search,
    resolve,
)


INPUT = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
OUT = Path("results/raw/arc/2026-11-02_1948_LSPV5_PEITL_SEVEN_NODE_EXCLUSION_REFEREE302_raw.json")


def resolution_witness(clauses):
    """Replay the Peitl--Szeider 16-line / nine-derived-node proof."""
    lines = [canonical_clause(c) for c in clauses]
    steps = [
        (3, 5, -4, (1, 2, 3, 5)),
        (4, 7, -5, (1, 2, 3)),
        (0, 6, 2, (-1, -3, -4, -5)),
        (0, 8, -1, (2, 3)),
        (4, 9, 1, (-3, -4, -5)),
        (1, 10, -2, (3,)),
        (3, 11, 5, (-3, -4)),
        (2, 13, 4, (-3,)),
        (12, 14, 3, ()),
    ]
    certificate = []
    for left, right, pivot, expected in steps:
        got = resolve(lines[left], lines[right], pivot)
        expected = canonical_clause(expected)
        if got != expected:
            raise AssertionError((left, right, pivot, got, expected))
        lines.append(got)
        certificate.append({
            "left_line": left + 1,
            "right_line": right + 1,
            "pivot": pivot,
            "clause": got,
        })
    if lines[-1] != ():
        raise AssertionError("witness does not end in contradiction")
    return certificate


def main():
    started = time.perf_counter()
    raw = INPUT.read_bytes()
    n, clauses = parse_dimacs(raw.decode())
    models = model_count(clauses, n)
    deletions = [model_count(clauses[:i] + clauses[i + 1 :], n) for i in range(len(clauses))]
    flips = sign_flip_counts(clauses, n)
    search = relaxed_unicycle_search(clauses, n)
    proof = resolution_witness(clauses)
    corrupted = reject_corruptions(clauses, proof)
    malformed = malformed_controls()
    odd_n, odd = parity_cnf_k4((1, 0, 0, 0))
    even_n, even = parity_cnf_k4((0, 0, 0, 0))
    parity = {"odd_models": model_count(odd, odd_n), "even_models": model_count(even, even_n)}
    assertions = {
        "authentic_sha256": hashlib.sha256(raw).hexdigest()
        == "6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6",
        "source_unsat": models == 0,
        "clause_minimal": all(x > 0 for x in deletions),
        "all_occurrence_sign_flips_sat": all(x > 0 for x in flips),
        "floor_tree_excluded": not search["full_tree_contains_false"],
        "unicycle_excluded": not search["contradiction_found"],
        "nine_node_resolution_upper": len(proof) == 9 and proof[-1]["clause"] == (),
        "all_corruptions_rejected": all(corrupted),
        "all_malformed_rejected": all(malformed.values()),
        "parity_both_labels": parity == {"odd_models": 0, "even_models": 8},
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    result = {
        "claim_id": "PEITL-SEVEN-NODE-EXCLUSION-REFEREE302",
        "status": {
            "source_excess_topology": "PROVED/EXACT",
            "seven_node_relaxed_exclusion": "COMPUTATIONAL exhaustive finite",
            "nine_node_upper": "PROVED by syntactic Resolution replay",
            "mixed_interval": "PROVED 8 <= W_Rmix341 <= 9",
            "B1_B2_B3": "OPEN",
        },
        "input": {
            "path": str(INPUT),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "variables": n,
            "clauses": len(clauses),
            "signed_clauses": clauses,
            "models": models,
            "deletion_model_counts": deletions,
            "sign_flip_model_counts": flips,
        },
        "fixed_calculus": "Rmix341 source-independent zero-premise VARDEF; unit binary RES/AND3/XOR; exact paid unary CONVERT",
        "topology_identity": "q-(mu-1)=beta+u+2*d0 for r=mu=7; q=7 gives (beta,u,d0)=(0,1,0) or (1,0,0)",
        "unary_class": "excluded because free exact representation aliases strengthen and subsume the single paid conversion, reducing to the exhausted six-binary-node tree relaxation",
        "unicycle_search": search,
        "resolution_upper_certificate": proof,
        "mixed_cost_interval": [8, 9],
        "malformed_controls": malformed,
        "corrupted_proof_rejections": corrupted,
        "parity_controls": parity,
        "assertions": assertions,
        "optimizer_cost_note": "free best proof selection is granted; enumeration work is external certification, not part of W_R",
        "resource_ledger": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": platform.python_version(),
            "all_phase_note": "materializes 32-bit truth tables, tree banks, extension cache, controls and JSON; no machine lower-bound or sublinear-space claim",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "mixed_cost_interval": [8, 9],
        "assertions": assertions,
        "search": search,
        "resources": result["resource_ledger"],
    }, indent=2))


if __name__ == "__main__":
    main()
