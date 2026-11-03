#!/usr/bin/env python3
"""Independent SAT-engine replay of all 105 REFEREE304 degree cases."""

from __future__ import annotations

import json
import resource
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from experiments.arc.lspv5_304.peitl_exact_eight_referee304 import Encoder, INPUT, parse_dimacs


OUT = Path("results/raw/arc/2026-11-02_2148_LSPV5_PEITL_EXACT_EIGHT_REFEREE304_maple.json")


def main():
    started = time.perf_counter()
    n, clauses = parse_dimacs(INPUT.read_text())
    encoder = Encoder(clauses, n=n, nodes=8)
    cnf = encoder.build()
    cases = []
    with Solver(name="maplechrono", bootstrap_with=cnf.clauses) as solver:
        for i, pattern in enumerate(encoder.degree_patterns):
            t0 = time.perf_counter()
            sat = solver.solve(assumptions=[pattern["selector"]])
            cases.append({
                "case_index": i,
                "kind": pattern["kind"],
                "exceptional_lines": pattern["exceptional_lines"],
                "sat": sat,
                "seconds": time.perf_counter() - t0,
            })
            assert not sat, cases[-1]
            if (i + 1) % 20 == 0:
                print(f"maplechrono: {i + 1}/{len(encoder.degree_patterns)} UNSAT", flush=True)
        stats = solver.accum_stats()
    result = {
        "claim_id": "PEITL-EXACT-EIGHT-REFEREE304-MAPLE",
        "status": "PASS",
        "solver": "maplechrono",
        "all_unsat": all(not x["sat"] for x in cases),
        "case_count": len(cases),
        "cases": cases,
        "encoding_variables": cnf.nv,
        "encoding_clauses": len(cnf.clauses),
        "solver_stats": stats,
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scope": "Independent solver engine over the same generated encoding; not an independent encoding implementation.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("claim_id", "status", "solver", "all_unsat", "case_count", "encoding_variables", "encoding_clauses", "solver_stats", "elapsed_seconds", "peak_rss_kib", "scope")}, indent=2))


if __name__ == "__main__":
    main()
