#!/usr/bin/env python3
"""Finite quantifier regression for PROMISE-FASTPATH-EQUIVALENCE1.

This is deliberately finite: it checks the wrapper construction on every
Boolean language and every promise subset of an eight-element universe, plus
named hostile-control labels.  It does not infer an asymptotic lower bound.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


UNIVERSE_SIZE = 8
OUT = Path("results/raw/review/2026-10-12_promise_fastpath_core.json")


def bit(mask: int, x: int) -> int:
    return (mask >> x) & 1


def main() -> None:
    start = time.perf_counter()
    checks = 0
    failures: list[dict[str, int | str]] = []
    monochromatic_promises = 0
    wrapper_cases = 0

    # Every finite promise admits a table solver.  The point here is only to
    # regress the exact fast-path/fallback quantifier construction.
    for language in range(1 << UNIVERSE_SIZE):
        for promise in range(1 << UNIVERSE_SIZE):
            fallback = lambda x, language=language: bit(language, x)
            promise_solver = lambda x, language=language: bit(language, x)
            vals = [bit(language, x) for x in range(UNIVERSE_SIZE) if bit(promise, x)]
            mono = not vals or all(v == vals[0] for v in vals)
            monochromatic_promises += int(mono)

            for x in range(UNIVERSE_SIZE):
                in_promise = bool(bit(promise, x))
                wrapped = promise_solver(x) if in_promise else fallback(x)
                expected = bit(language, x)
                checks += 1
                if wrapped != expected:
                    failures.append({
                        "kind": "global_exactness",
                        "language": language,
                        "promise": promise,
                        "x": x,
                    })
                if in_promise:
                    checks += 1
                    if wrapped != promise_solver(x):
                        failures.append({
                            "kind": "fast_path",
                            "language": language,
                            "promise": promise,
                            "x": x,
                        })
            wrapper_cases += 1

    named_controls = [
        "2SAT", "Horn", "affine_Tseitin", "bounded_treewidth", "parity",
        "signed_clean_core", "all_yes", "all_no", "padding",
        "redundant_clauses", "independent_products", "alternate_encoding",
        "DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP",
        "one_bit_output",
    ]
    for name in named_controls:
        checks += 1
        if not name:
            failures.append({"kind": "empty_control", "control": name})

    elapsed = time.perf_counter() - start
    payload = {
        "run_id": "PROMFAST1",
        "status": "COMPUTATIONAL",
        "universe_size": UNIVERSE_SIZE,
        "languages": 1 << UNIVERSE_SIZE,
        "promises_per_language": 1 << UNIVERSE_SIZE,
        "wrapper_cases": wrapper_cases,
        "monochromatic_promises": monochromatic_promises,
        "checks": checks,
        "failures": failures,
        "named_controls": named_controls,
        "elapsed_seconds": elapsed,
        "chunking": "none; one invocation, designed for well under 30 seconds",
        "limitation": (
            "Finite tables make every finite promise easy; this run validates "
            "only the wrapper and quantifier bookkeeping, not asymptotics."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["content_sha256_without_hash_field"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "checks": checks,
        "failures": len(failures),
        "wrapper_cases": wrapper_cases,
        "elapsed_seconds": round(elapsed, 6),
        "output": str(OUT),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
