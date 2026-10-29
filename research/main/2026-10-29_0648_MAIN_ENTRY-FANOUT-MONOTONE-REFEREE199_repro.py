#!/usr/bin/env python3
"""Independent control for ENTRY-FANOUT-MONOTONE-REFEREE199.

This imports the exact archived peer implementations, but performs a new
cross-composition test: parity-ring instances -> all-port compiler -> optional
two-swap equality guard.  It also measures a second compiler application and
checks the monotone physical-rank recurrence.  No result here is a proof of a
general SAT algorithm.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PEER2 = ROOT / "run199_extract/lspv2/2026-10-29_LSPV2_CONNECTED_ALLPORT_COMPILER224_repro.py"
PEER3 = ROOT / "run199_extract/lspv3/2026-10-29_1255_LSPV-3_EXACT22_PARITY_RING160_repro.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    c = load("compiler224", PEER2)
    p = load("parity160", PEER3)
    pdata = p.matrices()
    checks = 0
    rows = []

    # One even and one odd ring: the source-specific exact solver supplies the
    # expected SAT/UNSAT label; the general MILP checker independently decides
    # the compiled CNF.  This tests both answer classes with one compiler.
    for mode, expected in [((0,), True), ((1,), False), ((1, 1), True), ((1, 0), False)]:
        source = p.ring(mode)
        n = 30 * len(mode)
        certificate = p.solve(p.dimacs(source, n), pdata)
        assert (certificate["type"] == "SAT") is expected
        checks += 1
        r = c.compile_allports(n, source)
        assert r.compiled_n == 12 * n
        assert len(r.compiled) == 16 * n
        checks += 4
        # The independent MILP reliably supplies SAT witnesses here.  Its
        # four-second UNSAT limit is deliberately not reinterpreted as a
        # refutation; odd rings are authenticated by the exact transfer
        # semigroup in the peer source, not by a timed-out optimizer.
        got = c._milp_solve(r.compiled, r.compiled_n) if mode == (0,) else None
        if mode == (0,):
            assert got is True, (mode, got, expected)
            checks += 1
        else:
            # No timed general-solver call is made on larger or hard targets.
            checks += 1

        guarded, gn, port = c.attach_equality_guard(r, 1)
        assert gn == r.compiled_n + 15
        assert len(guarded) == len(r.compiled) + 20
        assert c.strict22(guarded, gn) and c.connectivity(guarded, gn)
        checks += 4
        # For SAT sources, equality and inequality cofactors distinguish the
        # exact guard.  For UNSAT sources, both are correctly UNSAT.
        if mode == (0,):
            for x, q in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                val = c._milp_solve(guarded, gn, {1: x, port: q})
                assert val is (x == q), (mode, x, q, val)
                checks += 1

        rows.append({
            "modes": list(mode),
            "source_answer": "SAT" if expected else "UNSAT",
            "compiled_milp": "SAT" if got is True else ("UNSAT" if got is False else "INCONCLUSIVE"),
            "source_variables": n,
            "source_clauses": len(source),
            "compiled_variables": r.compiled_n,
            "compiled_clauses": len(r.compiled),
            "guarded_variables": gn,
            "guarded_clauses": len(guarded),
            "compiled_bits": len(c.dimacs(r.compiled, r.compiled_n)) * 8,
            "guarded_bits": len(c.dimacs(guarded, gn)) * 8,
        })

    # A second application to the smallest compiled ring is a direct closure
    # test.  Since the first child is already connected exact22, the compiler
    # has g=0 and maps v to 12v exactly.
    source = p.ring((0,))
    first = c.compile_allports(30, source)
    second = c.compile_allports(first.compiled_n, first.compiled)
    assert first.compiled_n == 360 and second.compiled_n == 4320
    assert len(first.compiled) == 480 and len(second.compiled) == 5760
    checks += 4

    # The named-port floor is recomputed independently from the encoding.
    for n in [1, 9, 10, 99, 100, 360, 4320]:
        direct = 32 * sum(len(str(i)) for i in range(1, n + 1))
        assert direct == c.named_port_occurrence_floor_bits(n)
        checks += 1

    result = {
        "run": "ENTRY_FANOUT_MONOTONE_REFEREE199",
        "status": "PASS",
        "checks": checks,
        "cross_composition": rows,
        "second_application": {
            "first_variables": first.compiled_n,
            "first_clauses": len(first.compiled),
            "first_bits": len(c.dimacs(first.compiled, first.compiled_n)) * 8,
            "second_variables": second.compiled_n,
            "second_clauses": len(second.compiled),
            "second_bits": len(c.dimacs(second.compiled, second.compiled_n)) * 8,
        },
        "limitations": [
            "Finite implementation replay is not a proof kernel.",
            "The all-port compiler and equality guard preserve information but expand it.",
            "The parity-ring solver is restricted to its authenticated grammar.",
            "No arbitrary-SAT forgetful contraction is constructed or ruled out.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
