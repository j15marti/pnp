#!/usr/bin/env python3
"""Finite audit for MUTABLE-TRACE-COPY-LEAKAGE1.

The symbolic theorem is in the accompanying LSPV-1 report.  This audit checks
that excluding the read-only input from a trace does not prevent a linear-time
wrapper from copying the source into mutable state.  It also checks that a
scrubbed terminal projection collapses to the answer bit.  No finite count is
used as an asymptotic SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


Formula = tuple[int, tuple[tuple[int, ...], ...]]


FAMILIES: dict[str, Formula] = {
    "signed-monotone-3sat-2-2-control": (
        6,
        (
            (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
            (-1, -2, -4), (-1, -3, -5), (-2, -3, -6), (-4, -5, -6),
        ),
    ),
    "2sat-sat": (4, ((1, 2), (-1, 3), (-2, 4), (-3, 4))),
    "2sat-unsat": (2, ((1, 2), (1, -2), (-1, 2), (-1, -2))),
    "horn": (5, ((1,), (-1, 2), (-2, 3), (-3, 4), (-4, 5))),
    "affine-tseitin-cnf": (4, ((1, 2), (-1, -2), (3, 4), (-3, -4))),
    "bounded-treewidth": (6, ((1, 2, 3), (-2, 3, 4), (-3, 4, 5), (-4, 5, 6))),
    "independent-product": (6, ((1, 2), (-1, 2), (3, 4), (-3, 4), (5, 6), (-5, 6))),
    "padded": (6, ((1, 2, 3), (-1, -2, -3), (4, -4), (5, -5), (6, -6))),
    "redundant-clauses": (5, ((1, 2, 3), (1, 2, 3), (-1, 4, 5), (-1, 4, 5))),
}

ENCODINGS = ("canonical", "reversed", "renamed-metadata", "padded-metadata", "circuit-envelope")
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")


def canonical_object(formula: Formula) -> dict[str, object]:
    n, clauses = formula
    return {"n": n, "clauses": [list(c) for c in clauses]}


def encode(formula: Formula, kind: str) -> bytes:
    obj = canonical_object(formula)
    if kind == "reversed":
        obj["clauses"] = list(reversed(obj["clauses"]))
    elif kind == "renamed-metadata":
        obj["renaming"] = list(range(obj["n"], 0, -1))
    elif kind == "padded-metadata":
        obj["padding"] = "0" * 37
    elif kind == "circuit-envelope":
        obj = {"format": "cnf-as-circuit-input", "payload": obj}
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def decode(data: bytes) -> Formula:
    obj = json.loads(data.decode())
    if obj.get("format") == "cnf-as-circuit-input":
        obj = obj["payload"]
    n = int(obj["n"])
    clauses = tuple(tuple(int(x) for x in c) for c in obj["clauses"])
    return n, tuple(sorted(clauses))


def solve(formula: Formula, partial: tuple[int, ...] | None = None) -> tuple[bool, int, int]:
    n, clauses = formula
    values0 = [-1] * n if partial is None else list(partial)
    free = [i for i, value in enumerate(values0) if value == -1]
    assignments = clause_tests = 0
    for bits in itertools.product((0, 1), repeat=len(free)):
        values = list(values0)
        for idx, bit in zip(free, bits):
            values[idx] = bit
        assignments += 1
        good = True
        for clause in clauses:
            clause_tests += 1
            if not any((lit > 0 and values[abs(lit) - 1] == 1) or
                       (lit < 0 and values[abs(lit) - 1] == 0)
                       for lit in clause):
                good = False
                break
        if good:
            return True, assignments, clause_tests
    return False, assignments, clause_tests


def mutable_trace(encoded: bytes, wrapper: str, answer: bool) -> list[dict[str, object]]:
    """A trace projection containing mutable state only, never raw-input fields."""
    copied = encoded.hex()
    digest = hashlib.sha256(encoded).hexdigest()[:16]
    states: list[dict[str, object]] = [
        {"phase": "copy-end", "work_copy": copied, "copied_bytes": len(encoded)},
        {"phase": "simulate", "wrapper": wrapper, "tag": digest},
    ]
    if wrapper == "DEAD":
        states.append({"phase": "dead-code", "work": "unreachable"})
    elif wrapper == "COPY":
        states.append({"phase": "duplicate", "work_copy_2": copied})
    elif wrapper == "DELAY":
        states.extend({"phase": "delay", "tick": i} for i in range(5))
    elif wrapper == "INTERP":
        states.append({"phase": "interpreter", "bytecode_tag": digest[::-1]})
    elif wrapper == "RECOMP":
        states.append({"phase": "recompute", "work_copy": copied})
    states.append({"phase": "scrubbed-halt", "answer": int(answer)})
    return states


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    traces = 0
    total_preprocess_reads = 0
    total_copy_writes = 0
    total_extraction_reads = 0
    total_reconstruction_writes = 0
    total_assignments = 0
    total_clause_tests = 0
    copy_images: set[bytes] = set()
    answer_images: dict[int, set[str]] = {0: set(), 1: set()}
    digest_images: set[str] = set()
    prefix_images: set[bytes] = set()
    semantic_by_answer: dict[int, set[bool]] = {0: set(), 1: set()}
    wrapper_suffixes: set[str] = set()

    for _, formula in FAMILIES.items():
        canonical = (formula[0], tuple(sorted(formula[1])))
        answer, assignments, clause_tests = solve(canonical)
        total_assignments += assignments
        total_clause_tests += clause_tests
        partial = (0,) + (-1,) * (formula[0] - 1)
        point, point_assignments, point_clause_tests = solve(canonical, partial)
        total_assignments += point_assignments
        total_clause_tests += point_clause_tests
        semantic_by_answer[int(answer)].add(point)

        for encoding in ENCODINGS:
            encoded = encode(formula, encoding)
            assert decode(encoded) == canonical
            assertions += 1
            total_preprocess_reads += len(encoded)
            for wrapper in WRAPPERS:
                tr = mutable_trace(encoded, wrapper, answer)
                traces += 1
                assert all("read_only_input" not in state and "input" not in state for state in tr)
                assertions += 1

                recovered = bytes.fromhex(str(tr[0]["work_copy"]))
                assert recovered == encoded
                assert decode(recovered) == canonical
                assertions += 2
                total_copy_writes += len(encoded)
                total_extraction_reads += len(encoded)
                total_reconstruction_writes += len(encoded)

                copy_images.add(recovered)
                digest_images.add(hashlib.sha256(encoded).hexdigest()[:16])
                prefix_images.add(encoded[:16])
                answer_images[int(answer)].add(json.dumps(tr[-1], sort_keys=True))
                wrapper_suffixes.add(json.dumps(tr[1:-1], sort_keys=True))

                assert tr[-1] == {"phase": "scrubbed-halt", "answer": int(answer)}
                assertions += 1

    # Terminal states are constant on each answer fiber, while compatibility
    # at x1=0 varies within the satisfiable fiber in this finite suite.
    assert all(len(v) <= 1 for v in answer_images.values())
    assertions += 2
    assert len(semantic_by_answer[1]) == 2
    assertions += 1
    assert len(wrapper_suffixes) >= len(WRAPPERS)
    assertions += 1

    # Exhaustive binary-string control: mutable copying has 2^N images at
    # length N with exactly N reads and N writes; j-prefix copying has 2^j.
    binary_controls = 0
    for n in range(1, 13):
        strings = [bytes(bits) for bits in itertools.product((0, 1), repeat=n)]
        full = {s for s in strings}
        j = min(n, 5)
        prefixes = {s[:j] for s in strings}
        assert len(full) == 2 ** n
        assert len(prefixes) == 2 ** j
        assertions += 2
        binary_controls += len(strings)

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "DERIVEDLEAK1",
        "claim": "MUTABLE-TRACE-COPY-LEAKAGE1",
        "status": "COMPUTATIONAL",
        "scope_warning": (
            "Finite source-copy and scrubbed-terminal audit only; image size is not "
            "a SAT time lower bound and no asymptotic conclusion is extrapolated."
        ),
        "dimensions": {
            "families": len(FAMILIES),
            "encodings": len(ENCODINGS),
            "wrappers": len(WRAPPERS),
            "traces": traces,
            "binary_strings_exhausted": binary_controls,
        },
        "image_counts": {
            "full_mutable_copy": len(copy_images),
            "prefix_16": len(prefix_images),
            "sha256_prefix_16_hex": len(digest_images),
            "scrubbed_terminal_answer_0": len(answer_images[0]),
            "scrubbed_terminal_answer_1": len(answer_images[1]),
        },
        "charged_operations": {
            "preprocess_input_byte_reads": total_preprocess_reads,
            "mutable_copy_byte_writes": total_copy_writes,
            "copy_extraction_byte_reads": total_extraction_reads,
            "copy_reconstruction_byte_writes": total_reconstruction_writes,
            "bruteforce_assignments": total_assignments,
            "bruteforce_clause_tests": total_clause_tests,
        },
        "counts": {"assertions": assertions, "failures": 0},
        "runtime_seconds": round(elapsed, 6),
        "chunking": "Single deterministic invocation below 30 seconds.",
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
    }
    path = Path("results/raw/review/2026-10-12_input_erased_mutable_trace_copy.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
