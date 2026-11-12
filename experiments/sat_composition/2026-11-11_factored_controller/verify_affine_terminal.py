#!/usr/bin/env python3
"""Exact full-rank affine terminal controls with zero expansion/search budgets."""
import hashlib
import json
from pathlib import Path
import time

from factored_solver import solve_decomposed


def main():
    started = time.perf_counter()
    n = 1024
    target = sum(1 << i for i in range(n) if i % 3 == 0)
    all_bits = (1 << n) - 1
    # The suffix-one matrix is triangular with diagonal one, hence full rank.
    # Many rows have hundreds of coefficients, so this is not just unary input.
    equations = []
    for i in range(n):
        row = all_bits ^ ((1 << i) - 1)
        equations.append((row, (row & target).bit_count() % 2))
    units = [((i + 1) if (target >> i) & 1 else -(i + 1),)
             for i in (0, n // 2, n - 1)]
    decomposition = {"bags": [list(range(n))], "edges": []}
    cases = []
    for mode in ("2cnf", "horn"):
        for strategy in ("polynomial", "seeds"):
            for contradiction in (False, True):
                clauses = units + ([(-units[0][0],)] if contradiction else [])
                result = solve_decomposed(n, clauses, equations, decomposition, mode, strategy,
                                          term_cap=0, seed_cap=0)
                assert result["status"] == ("UNSAT" if contradiction else "SAT")
                assert result["counters"]["max_local_affine_rank"] == n
                assert result["counters"]["backend_calls"] == 1
                assert result["counters"]["affine_terminal_calls"] == 1
                assert result["counters"]["frozen_backend_calls"] == 0
                backend = result["bag_results"][0]["states"][0]["backend"]
                assert backend["terminal"] == "unit_affine"
                if not contradiction:
                    assert result["witness"] == target
                    assert all((row & result["witness"]).bit_count() % 2 == rhs for row, rhs in equations)
                    assert all(bool((result["witness"] >> (abs(c[0]) - 1)) & 1) == (c[0] > 0) for c in clauses)
                cases.append({"mode": mode, "strategy": strategy, "contradiction": contradiction,
                              "result": result})
    output = {"status": "COMPUTATIONAL", "checks": len(cases), "failures": 0,
              "n": n, "matrix_rank": n, "target_witness": target,
              "matrix_recipe": "row_i has ones in columns i..n-1; target_i=1 iff i mod3=0",
              "unit_clauses": units, "equations": equations, "decomposition": decomposition,
              "term_cap": 0, "seed_cap": 0, "cases": cases,
              "elapsed_seconds": time.perf_counter() - started,
              "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("factored_solver.py", "verify_affine_terminal.py")},
              "limitation": "Finite implementation checks; arbitrary-rank polynomial guarantee follows from Gaussian elimination."}
    Path(__file__).with_name("affine_terminal_validation.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items()
                      if k not in ("target_witness", "unit_clauses", "equations", "decomposition", "cases")}, indent=2))


if __name__ == "__main__":
    main()
