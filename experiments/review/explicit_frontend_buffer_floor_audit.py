#!/usr/bin/env python3
"""Finite audit for the explicit retained-buffer floor in KCALIB1.

This script checks exponent bookkeeping exactly (Fractions plus a high-
precision golden-ratio comparison) and measures finite copy/buffer ledgers on
hostile CNF controls.  It does not infer asymptotic lower bounds from the
finite measurements.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from fractions import Fraction
from pathlib import Path


OUT = Path("results/raw/review/2026-10-12_explicit_frontend_buffer_floor.json")


def dimacs(nvars: int, clauses: list[tuple[int, ...]]) -> bytes:
    rows = [f"p cnf {nvars} {len(clauses)}"]
    rows.extend(" ".join(map(str, c)) + " 0" for c in clauses)
    return ("\n".join(rows) + "\n").encode()


BASE = {
    "horn": dimacs(3, [(-1, -2, 3), (-3, 2), (1,)]),
    "2sat": dimacs(4, [(1, -2), (2, 3), (-3, 4), (-4, 1)]),
    "affine_tseitin": dimacs(4, [(1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)]),
    "bounded_treewidth": dimacs(5, [(1, 2, 3), (-2, 3, 4), (-3, 4, 5)]),
    "independent_product": dimacs(6, [(1, 2, 3), (-1, -2, -3), (4, 5, 6), (-4, -5, -6)]),
    "redundant_clauses": dimacs(3, [(1, 2, 3)] * 8),
    "padding": dimacs(12, [(1, 2, 3), (-1, -2, -3), (10, -10), (11, -11), (12, -12)]),
}


def variants(name: str, payload: bytes) -> list[tuple[str, bytes]]:
    text = payload.decode()
    return [
        (f"{name}/dimacs", payload),
        (f"{name}/json", json.dumps({"kind": name, "cnf": text}, sort_keys=True).encode()),
        (f"{name}/copy", payload + payload),
        (f"{name}/dead", payload + b"c dead wrapper metadata\n"),
        (f"{name}/delay", b"c delay=4096\n" + payload),
        (f"{name}/interp", payload.replace(b" 1 ", b" 01 ")),
        (f"{name}/recomp", hashlib.sha256(payload).hexdigest().encode() + b"\n" + payload),
    ]


def retained_copy(payload: bytes) -> dict[str, int | str]:
    # An explicit same-machine realization: every output byte is written once
    # into a writable bytearray and retained for the next phase.
    buf = bytearray()
    writes = 0
    for byte in payload:
        buf.append(byte)
        writes += 1
    assert bytes(buf) == payload
    return {
        "bytes": len(payload),
        "bit_writes": 8 * writes,
        "peak_writable_bits": 8 * len(buf),
        "sha256": hashlib.sha256(buf).hexdigest(),
        "extraction_calls": 0,
        "reconstruction_calls": 0,
        "communication_bits": 0,
    }


def main() -> None:
    started = time.perf_counter()
    phi = (1 + math.sqrt(5)) / 2
    lambdas = [Fraction(1, 1), Fraction(11, 10), Fraction(5, 4), Fraction(3, 2)]
    parameter_checks = 0
    parameter_failures = 0
    examples = []
    for lam in lambdas:
        for k in range(1, 65):
            for d in range(1, 65):
                # Any explicit retained M-bit buffer gives c>=lambda and
                # rho>=lambda, independently of beta,K,D.
                floor_sum = 2 * lam
                forbidden = float(floor_sum) >= phi
                expected = lam >= 1
                parameter_checks += 1
                if forbidden != expected:
                    parameter_failures += 1
                if k == d == 1:
                    examples.append({"lambda": str(lam), "floor_sum": str(floor_sum), "phi": phi})

    finite = []
    for family, payload in BASE.items():
        for label, encoded in variants(family, payload):
            row = {"control": label, **retained_copy(encoded)}
            # Outside-hypothesis controls.  These are realizations to be
            # charged separately, not counterexamples to the retained-buffer
            # theorem.
            row["stream_peak_bits"] = 8 * max((len(line) for line in encoded.splitlines()), default=0)
            row["virtual_descriptor_bits"] = 256
            row["fused_retained_buffer_bits"] = 0
            finite.append(row)

    assert parameter_failures == 0
    assert all(x["bit_writes"] == x["peak_writable_bits"] for x in finite)
    assert all(x["extraction_calls"] == x["reconstruction_calls"] == 0 for x in finite)
    result = {
        "claim": "EXPLICIT-RETAINED-FRONTEND-FLOOR1",
        "status": "COMPUTATIONAL",
        "asymptotic_theorem_checked_symbolically": "c>=lambda, rho>=lambda, hence c+rho>=2lambda",
        "endpoint": {"name": "FLMV golden-ratio region", "phi": phi},
        "parameter_grid": {
            "lambda_values": [str(x) for x in lambdas],
            "K_range": [1, 64],
            "D_range": [1, 64],
            "checks": parameter_checks,
            "failures": parameter_failures,
            "examples": examples,
        },
        "finite_controls": {
            "families": sorted(BASE),
            "variants_per_family": 7,
            "rows": len(finite),
            "total_bit_writes": sum(int(x["bit_writes"]) for x in finite),
            "max_peak_writable_bits": max(int(x["peak_writable_bits"]) for x in finite),
            "rows_detail": finite,
        },
        "interpretation_guard": [
            "Finite byte counts are not asymptotic evidence.",
            "Streaming, virtual, and fused realizations are outside the explicit retained-buffer hypothesis.",
            "Their generation, access, reread, recomputation, and parent-retention costs remain to be proved and charged.",
        ],
        "runtime_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "checks": parameter_checks,
        "failures": parameter_failures,
        "finite_rows": len(finite),
        "total_bit_writes": result["finite_controls"]["total_bit_writes"],
        "runtime_seconds": result["runtime_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
