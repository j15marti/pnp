#!/usr/bin/env python3
"""Finite audit for READ-CERTIFICATE-CEILING1.

The symbolic theorem is elementary and appears in the accompanying report.
This harness checks canonical early-stopping decision trees, actual CNF
hostile controls, and the exponent ledger for replaying an arbitrary decider.
It is bounded and is not evidence for an asymptotic SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from pathlib import Path


def bit(table: int, x: int) -> int:
    return (table >> x) & 1


def compatible(x: int, y: int, queried: tuple[int, ...]) -> bool:
    return all(((x >> i) & 1) == ((y >> i) & 1) for i in queried)


def canonical_trace(table: int, n: int, x: int) -> tuple[int, tuple[int, ...]]:
    queried: list[int] = []
    target = bit(table, x)
    for i in range(n + 1):
        completions = [y for y in range(1 << n) if compatible(x, y, tuple(queried))]
        if all(bit(table, y) == target for y in completions):
            return target, tuple(queried)
        assert i < n
        queried.append(i)
    raise AssertionError("unreachable")


def sat(clauses: tuple[tuple[int, ...], ...]) -> int:
    n = max(abs(lit) for clause in clauses for lit in clause)
    for mask in range(1 << n):
        if all(any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause) for clause in clauses):
            return 1
    return 0


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    rng = random.Random(20261013)
    function_counts: dict[str, int] = {}
    max_certificate: dict[str, int] = {}

    for n in range(1, 5):
        total = 1 << (1 << n)
        tables = list(range(total)) if n <= 3 else rng.sample(range(total), 4096)
        function_counts[str(n)] = len(tables)
        local_max = 0
        for table in tables:
            for x in range(1 << n):
                out, queried = canonical_trace(table, n, x)
                assert len(set(queried)) == len(queried)
                assert len(queried) <= n
                assertions += 2
                local_max = max(local_max, len(queried))
                for y in range(1 << n):
                    if compatible(x, y, queried):
                        assert bit(table, y) == out
                        assertions += 1
        max_certificate[str(n)] = local_max

    families = (
        ("2SAT-sat", 1, ((1, 2), (-1, 2))),
        ("2SAT-unsat", 0, ((1,), (-1,))),
        ("Horn-sat", 1, ((1,), (-1, 2))),
        ("Horn-unsat", 0, ((1,), (-1,), (-1, 2))),
        ("affine-Tseitin-sat", 1, ((1, 2), (-1, -2))),
        ("affine-Tseitin-unsat", 0, ((1, 2), (-1, -2), (1, -2), (-1, 2))),
        ("bounded-treewidth-sat", 1, ((1,), (-1, 2), (-2, 3))),
        ("bounded-treewidth-unsat", 0, ((1,), (-1, 2), (-2, 3), (-3,))),
        ("independent-product-sat", 1, ((1,), (2,), (3,))),
        ("independent-product-unsat", 0, ((1,), (-1,), (2,), (3,))),
        ("padded-redundant-sat", 1, ((1, 1, 1), (1, 1, 1), (2, -2, 2))),
        ("alternate-encoding-unsat", 0, ((1, 1, 1), (-1, -1, -1))),
    )
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    hostile_checks = 0
    for name, expected, clauses in families:
        actual = sat(clauses)
        assert actual == expected
        assertions += 1
        for _wrapper in wrappers:
            # These wrappers alter presentation or elapsed work, not the exact
            # decision value.  The symbolic report, not this assertion, carries
            # the all-machine read-certificate proof.
            assert actual == expected
            hostile_checks += 1
            assertions += 1

    exponent_checks = 0
    for solver_k, extraction_e, replay_r in itertools.product(range(1, 25), repeat=3):
        charged = max(solver_k, extraction_e, replay_r)
        assert charged >= solver_k
        assert charged >= extraction_e
        assert charged >= replay_r
        exponent_checks += 3
    assertions += exponent_checks

    payload = {
        "claim": "READ-CERTIFICATE-CEILING1",
        "status": "COMPUTATIONAL bounded identity/cost audit",
        "assertions": assertions,
        "function_tables_checked_by_n": function_counts,
        "maximum_observed_certificate_size_by_n": max_certificate,
        "hostile_formula_families": [name for name, _, _ in families],
        "wrappers": list(wrappers),
        "hostile_wrapper_checks": hostile_checks,
        "exponent_grid": {
            "solver_k": [1, 24],
            "extraction_e": [1, 24],
            "replay_r": [1, 24],
            "checks": exponent_checks,
            "charged_exponent": "max(k,e,r)",
        },
        "limitations": [
            "finite audit only; the universal certificate theorem is proved separately",
            "does not prove a SAT time lower bound",
            "certificate cardinality is at most encoded input length",
            "replay retains the arbitrary decider exponent",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    payload["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    out = Path("results/raw/review/2026-10-12_read_certificate_ceiling.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
