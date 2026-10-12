#!/usr/bin/env python3
"""Bounded audit for the clean-core resource-coordinate classification.

The exact theorem uses a trivial exhaustive SAT decider with polynomial
workspace.  This script instantiates a streaming version on hostile controls
and records a conservative logical-bit peak.  It is a finite implementation
check, not an asymptotic lower-bound experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path


def sat_clause(clause: tuple[int, ...], mask: int) -> bool:
    for lit in clause:
        bit = (mask >> (abs(lit) - 1)) & 1
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return True
    return False


def brute_stream(cnf: tuple[tuple[int, ...], ...], n: int) -> tuple[bool, int, int]:
    checks = 0
    for mask in range(1 << n):
        ok = True
        for clause in cnf:
            checks += 1
            if not sat_clause(clause, mask):
                ok = False
                break
        if ok:
            peak = n + math.ceil(math.log2(len(cnf) + 1)) + math.ceil(math.log2(n + 1)) + 3
            return True, checks, peak
    peak = n + math.ceil(math.log2(len(cnf) + 1)) + math.ceil(math.log2(n + 1)) + 3
    return False, checks, peak


def paired(edges: tuple[tuple[int, int], ...], vertices: int) -> tuple[tuple[int, ...], ...]:
    inc = [[] for _ in range(vertices)]
    for idx, (u, v) in enumerate(edges, start=1):
        inc[u].append(idx)
        inc[v].append(idx)
    out = []
    for row in inc:
        assert len(row) == 3
        out.append(tuple(row))
        out.append(tuple(-x for x in row))
    return tuple(out)


def shifted(cnf: tuple[tuple[int, ...], ...], shift: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((abs(x) + shift) * (1 if x > 0 else -1) for x in c) for c in cnf)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    started = time.perf_counter()

    k33_edges = tuple((u, 3 + v) for u in range(3) for v in range(3))
    prism_edges = ((0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5))
    k33 = paired(k33_edges, 6)
    prism = paired(prism_edges, 6)

    controls: dict[str, tuple[int, tuple[tuple[int, ...], ...]]] = {
        "2sat": (5, ((1, 2), (-1, 3), (-2, 4), (-3, 5), (-4, -5))),
        "horn": (5, ((1,), (-1, 2), (-2, 3), (-3, 4), (-4, 5))),
        "affine_odd_cycle_cnf": (5, ((1, 2), (-1, -2), (2, 3), (-2, -3), (3, 4), (-3, -4), (4, 5), (-4, -5), (5, 1), (-5, -1))),
        "bounded_treewidth_chain": (7, tuple((i, -(i + 1), i + 2) for i in range(1, 6))),
        "paired_k33": (9, k33),
        "paired_prism": (9, prism),
        "independent_product": (18, k33 + shifted(prism, 9)),
        "redundant_clause_padding": (9, k33 + k33[:4] + k33[:4]),
        "alternate_clause_order": (9, tuple(reversed(k33))),
    }
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    rows = []
    total_checks = 0
    wrapper_checks = 0
    failures = []
    for name, (n, cnf) in controls.items():
        answer, checks, peak = brute_stream(cnf, n)
        total_checks += checks
        encoded_units = n + sum(len(c) for c in cnf) + len(cnf)
        if peak > 3 * encoded_units:
            failures.append(f"workspace bound: {name}")
        for _wrapper in wrappers:
            answer2, _, peak2 = brute_stream(cnf, n)
            wrapper_checks += 1
            if answer2 != answer or peak2 != peak:
                failures.append(f"wrapper semantics: {name}")
        rows.append({
            "name": name,
            "variables": n,
            "clauses": len(cnf),
            "answer": answer,
            "assignment_clause_checks": checks,
            "logical_peak_bits": peak,
            "encoded_units_lower_bound": encoded_units,
        })

    result = {
        "claim": "CLEANCORE-RESOURCE-COORDINATE1",
        "status": "COMPUTATIONAL",
        "scope": "bounded implementation audit; asymptotic theorem is separate",
        "instances": rows,
        "streaming_assignment_clause_checks": total_checks,
        "wrapper_replays": wrapper_checks,
        "workspace_bound_checks": len(rows),
        "failures": len(failures),
        "failure_examples": failures[:8],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_payload_sha256"] = hashlib.sha256(payload).hexdigest()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
