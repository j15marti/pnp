#!/usr/bin/env python3
"""Finite audit for SERIAL-TRACE-FACTORIZATION1.

The symbolic theorem is in the accompanying LSPV-2 report.  This audit checks
that a mutable trace can reveal an encoded source one byte at a time while no
trace state contains the whole source and the variable auxiliary payload is
only one byte plus a logarithmic index.  It also charges trace extraction and
source reconstruction.  The finite checks are not extrapolated to a SAT lower
bound.
"""

from __future__ import annotations

import itertools
import json
import math
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
    "affine-tseitin-parity": (4, ((1, 2), (-1, -2), (3, 4), (-3, -4))),
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
            if not any(
                (lit > 0 and values[abs(lit) - 1] == 1)
                or (lit < 0 and values[abs(lit) - 1] == 0)
                for lit in clause
            ):
                good = False
                break
        if good:
            return True, assignments, clause_tests
    return False, assignments, clause_tests


def serial_mutable_trace(encoded: bytes, wrapper: str, answer: bool) -> list[dict[str, object]]:
    """Emit source bytes sequentially; no state contains the complete source."""
    states: list[dict[str, object]] = []
    for index, value in enumerate(encoded):
        states.append({"phase": "emit", "index": index, "byte": value})
        if wrapper == "COPY":
            states.append({"phase": "emit-copy", "index": index, "byte": value})
        elif wrapper == "INTERP":
            states.append({"phase": "interpret", "index": index, "opcode": value ^ 0x5A})
        elif wrapper == "DELAY":
            states.append({"phase": "delay", "index": index, "tick": 0})
    states.append({"phase": "end", "length": len(encoded)})
    if wrapper == "DEAD":
        states.append({"phase": "dead-code", "reachable": 0})
    elif wrapper == "RECOMP":
        for index, value in enumerate(encoded):
            states.append({"phase": "re-emit", "index": index, "byte": value})
    states.append({"phase": "scrubbed-halt", "answer": int(answer)})
    return states


def recover(trace: list[dict[str, object]]) -> bytes:
    emits = [state for state in trace if state.get("phase") == "emit"]
    assert [int(state["index"]) for state in emits] == list(range(len(emits)))
    return bytes(int(state["byte"]) for state in emits)


def main() -> None:
    started = time.perf_counter()
    assertions = traces = 0
    total_input_reads = total_emit_writes = 0
    total_trace_reads = total_reconstruction_writes = 0
    total_assignments = total_clause_tests = 0
    peak_variable_payload_bits = 0
    semantic_by_answer: dict[int, set[bool]] = {0: set(), 1: set()}
    recovered_images: set[bytes] = set()
    terminal_images: dict[int, set[str]] = {0: set(), 1: set()}

    for formula in FAMILIES.values():
        canonical = (formula[0], tuple(sorted(formula[1])))
        answer, assignments, clause_tests = solve(canonical)
        total_assignments += assignments
        total_clause_tests += clause_tests
        partial = (0,) + (-1,) * (formula[0] - 1)
        point, assignments, clause_tests = solve(canonical, partial)
        total_assignments += assignments
        total_clause_tests += clause_tests
        semantic_by_answer[int(answer)].add(point)

        for encoding in ENCODINGS:
            encoded = encode(formula, encoding)
            assert decode(encoded) == canonical
            assertions += 1
            for wrapper in WRAPPERS:
                trace = serial_mutable_trace(encoded, wrapper, answer)
                traces += 1
                recovered = recover(trace)
                assert recovered == encoded
                assert decode(recovered) == canonical
                assertions += 2

                emits = [state for state in trace if state.get("phase") == "emit"]
                assert len(emits) == len(encoded)
                assert all(set(state) == {"phase", "index", "byte"} for state in emits)
                assert all("source" not in state and "input" not in state for state in trace)
                assertions += 3

                index_bits = max(1, math.ceil(math.log2(len(encoded) + 1)))
                peak_variable_payload_bits = max(peak_variable_payload_bits, index_bits + 8)
                assert index_bits + 8 < 8 * len(encoded)
                assertions += 1

                assert trace[-1] == {"phase": "scrubbed-halt", "answer": int(answer)}
                assertions += 1
                recovered_images.add(recovered)
                terminal_images[int(answer)].add(json.dumps(trace[-1], sort_keys=True))

                total_input_reads += len(encoded)
                total_emit_writes += len(encoded)
                total_trace_reads += len(emits)
                total_reconstruction_writes += len(recovered)

    assert all(len(images) <= 1 for images in terminal_images.values())
    assert len(semantic_by_answer[1]) == 2
    assertions += 3

    binary_strings = 0
    for n in range(2, 12):
        traces_at_n: set[tuple[tuple[int, int], ...]] = set()
        for bits in itertools.product((0, 1), repeat=n):
            source = bytes(bits)
            trace = serial_mutable_trace(source, "DIRECT", True)
            assert recover(trace) == source
            traces_at_n.add(tuple((int(s["index"]), int(s["byte"])) for s in trace if s.get("phase") == "emit"))
            assertions += 1
            binary_strings += 1
        assert len(traces_at_n) == 2 ** n
        assertions += 1

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "SERIALTRACE1",
        "claim": "SERIAL-TRACE-FACTORIZATION1",
        "status": "COMPUTATIONAL",
        "scope_warning": (
            "Finite serial-trace identity audit only. The symbolic wrapper theorem supplies "
            "the general statement; trace factorization is not a SAT time or space lower bound."
        ),
        "dimensions": {
            "families": len(FAMILIES),
            "encodings": len(ENCODINGS),
            "wrappers": len(WRAPPERS),
            "traces": traces,
            "binary_strings_exhausted": binary_strings,
        },
        "charged_operations": {
            "input_byte_reads": total_input_reads,
            "serial_emit_writes": total_emit_writes,
            "extractor_trace_state_reads": total_trace_reads,
            "source_reconstruction_writes": total_reconstruction_writes,
            "bruteforce_assignments": total_assignments,
            "bruteforce_clause_tests": total_clause_tests,
        },
        "resource_observations": {
            "peak_serial_variable_payload_bits": peak_variable_payload_bits,
            "whole_source_held_in_one_serial_state": False,
            "distinct_recovered_sources": len(recovered_images),
            "terminal_answer_0_images": len(terminal_images[0]),
            "terminal_answer_1_images": len(terminal_images[1]),
        },
        "counts": {"assertions": assertions, "failures": 0},
        "runtime_seconds": round(elapsed, 6),
        "chunking": "Single deterministic invocation below 30 seconds.",
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
    }
    path = Path("results/raw/review/2026-10-13_serial_trace_semantic_factorization.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
