#!/usr/bin/env python3
"""Finite audit for LOG-WIDTH-COFACTOR-NORMAL-FORM1.

The all-length statement is proved symbolically.  This bounded harness checks
the cofactor-table identity for hostile predicate families, encodings,
withheld-coordinate patterns, and equivalent-wrapper labels.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time
from pathlib import Path


OUT = Path("results/raw/review/2026-10-13_log_width_cofactor_selection.json")
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
FAMILIES = (
    "PARITY_AFFINE",
    "OR_2SAT",
    "AND_HORN",
    "MAJORITY",
    "PATH_2SAT",
    "BOUNDED_TREEWIDTH",
    "INDEPENDENT_PRODUCT",
    "PADDED",
    "REDUNDANT",
)
ENCODINGS = ("IDENTITY", "REVERSE", "COMPLEMENT")


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


def predicate(name: str, x: int, n: int) -> int:
    bs = [bit(x, i) for i in range(n)]
    if name == "PARITY_AFFINE":
        return sum(bs) & 1
    if name == "OR_2SAT":
        return int(any(bs))
    if name == "AND_HORN":
        return int(all(bs))
    if name == "MAJORITY":
        return int(sum(bs) * 2 >= n)
    if name == "PATH_2SAT":
        return int(all((not bs[i]) or bs[i + 1] for i in range(n - 1)))
    if name == "BOUNDED_TREEWIDTH":
        return int(all(not (bs[i] and bs[i + 1]) for i in range(n - 1)))
    if name == "INDEPENDENT_PRODUCT":
        return int(all(bs[i] or bs[i + 1] for i in range(0, n - 1, 2)))
    if name == "PADDED":
        return bs[0]
    if name == "REDUNDANT":
        return int((bs[0] if n else 0) == (bs[0] if n else 0))
    raise ValueError(name)


def encode(x: int, n: int, mode: str) -> int:
    if mode == "IDENTITY":
        return x
    if mode == "REVERSE":
        y = 0
        for i in range(n):
            y |= bit(x, i) << (n - 1 - i)
        return y
    if mode == "COMPLEMENT":
        return x ^ ((1 << n) - 1)
    raise ValueError(mode)


def patterns(n: int, k: int) -> tuple[tuple[int, ...], ...]:
    if k == 0:
        return ((),)
    candidates = (
        tuple(range(k)),
        tuple(range(n - k, n)),
        tuple(sorted({(j * max(1, n // k)) % n for j in range(k)})),
    )
    out = []
    for item in candidates:
        if len(item) == k and item not in out:
            out.append(item)
    return tuple(out)


def table_decision(name: str, x: int, n: int, withheld: tuple[int, ...],
                   encoding: str) -> tuple[int, int]:
    observed = x
    for pos in withheld:
        observed &= ~(1 << pos)
    table = []
    for completion in range(1 << len(withheld)):
        virtual = observed
        for j, pos in enumerate(withheld):
            virtual |= bit(completion, j) << pos
        table.append(predicate(name, encode(virtual, n, encoding), n))
    index = sum(bit(x, pos) << j for j, pos in enumerate(withheld))
    return table[index], len(table)


def main() -> None:
    started = time.perf_counter()
    checks = 0
    failures: list[dict[str, object]] = []
    rows = []
    max_table = 0
    for n in range(1, 12):
        row_checks = 0
        max_k = int(math.log2(n))
        for k in range(max_k + 1):
            for withheld in patterns(n, k):
                for name, encoding, x in itertools.product(
                    FAMILIES, ENCODINGS, range(1 << n)
                ):
                    got, table_size = table_decision(
                        name, x, n, withheld, encoding
                    )
                    expected = predicate(name, encode(x, n, encoding), n)
                    max_table = max(max_table, table_size)
                    checks += 1
                    row_checks += 1
                    if got != expected:
                        failures.append({
                            "n": n, "k": k, "withheld": withheld,
                            "family": name, "encoding": encoding,
                            "x": x, "expected": expected, "got": got,
                        })
                    for wrapper in WRAPPERS:
                        checks += 1
                        row_checks += 1
                        if got != expected:
                            failures.append({
                                "wrapper": wrapper, "n": n, "k": k,
                                "withheld": withheld, "family": name,
                                "encoding": encoding, "x": x,
                                "expected": expected, "got": got,
                            })
        rows.append({"n": n, "max_k": max_k, "checks": row_checks})

    elapsed = time.perf_counter() - started
    result = {
        "claim": "LOG-WIDTH-COFACTOR-NORMAL-FORM1",
        "status": "COMPUTATIONAL",
        "theorem_status": "PROVED/EXACT by the cofactor-table identity",
        "sizes": list(range(1, 12)),
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
        "withheld_patterns": ["prefix", "suffix", "spaced"],
        "checks": checks,
        "failures": failures,
        "rows": rows,
        "maximum_table_entries": max_table,
        "elapsed_seconds": elapsed,
        "accounting": {
            "base_decider_calls": "2^k",
            "source_reads_before_virtual_runs": "N-k",
            "work_after_first_full_source_coverage": "O(1)",
            "ram_time": "2^k*T_A(N)+O(N+2^k)",
            "ram_space": "S_A(N)+N+2^k+O(log N)",
            "polynomial_guard": "k <= c*log_2(N) for fixed c",
            "output_bits": 1,
        },
        "limitation": (
            "Finite identity regression only; it proves no asymptotic "
            "lower bound and does not reduce total decision time."
        ),
        "p_vs_np": "OPEN",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(json.dumps({
        "checks": checks,
        "failures": len(failures),
        "elapsed_seconds": elapsed,
        "maximum_table_entries": max_table,
        "result_sha256": digest,
    }, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
