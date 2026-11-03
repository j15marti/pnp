#!/usr/bin/env python3
"""Positive completeness control: admit and replay a nine-node mixed proof."""

from __future__ import annotations

import json
import resource
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from experiments.arc.lspv5_304.peitl_exact_eight_referee304 import (
    Encoder,
    INPUT,
    parse_dimacs,
    validate_relaxed_proof,
)


OUT = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_NINE_NODE_POSITIVE_REFEREE304.json")


def main():
    started = time.perf_counter()
    n, clauses = parse_dimacs(INPUT.read_text())
    encoder = Encoder(clauses, n=n, nodes=9)
    cnf = encoder.build()
    with Solver(name="glucose4", bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        stats = solver.accum_stats()
    proof = encoder.decode(model) if model else None
    valid = bool(proof) and validate_relaxed_proof(clauses, proof, n)
    assert sat and valid and len(proof) == 9 and proof[-1]["truth_table"] == 0
    result = {
        "claim_id": "PEITL-NINE-NODE-POSITIVE-REFEREE304",
        "status": "PASS",
        "sat": sat,
        "replay_valid": valid,
        "nodes": len(proof),
        "encoding_variables": cnf.nv,
        "encoding_clauses": len(cnf.clauses),
        "solver": "glucose4",
        "solver_stats": stats,
        "proof": proof,
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "Positive completeness control for the encoding implementation; not a lower bound.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
