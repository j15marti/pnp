#!/usr/bin/env python3
"""Finite audit for INPUT-TRACE-SOURCE-LEAKAGE1.

The audit checks a narrow identity: when a full execution trace includes the
initial configuration, a program-specific extractor can recover the encoded
source independently of all later wrapper-specific states.  It then computes
pointwise compatibility by a separately charged decision procedure.  This is
not evidence of an asymptotic SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


Formula = tuple[int, tuple[tuple[int, ...], ...]]


FAMILIES: dict[str, Formula] = {
    "3sat-clean-core-control": (5, ((1, 2, 3), (-1, -2, -3), (1, -4, 5), (-2, 4, -5))),
    "2sat": (5, ((1, 2), (-1, 3), (-2, 4), (-3, 5))),
    "horn": (5, ((-1, -2, 3), (-3, 4), (-4, 5), (-5,))),
    "affine-tseitin-cnf": (4, ((1, 2), (-1, -2), (3, 4), (-3, -4))),
    "bounded-treewidth": (6, ((1, 2, 3), (-2, 3, 4), (-3, 4, 5), (-4, 5, 6))),
    "independent-product": (6, ((1, 2), (-1, 2), (3, 4), (-3, 4), (5, 6), (-5, 6))),
    "padded": (6, ((1, 2, 3), (-1, -2, -3), (4, -4), (5, -5), (6, -6))),
    "redundant-clauses": (5, ((1, 2, 3), (1, 2, 3), (-1, 4, 5), (-1, 4, 5))),
    "parity": (5, ((1, 2), (-1, -2), (2, 3), (-2, -3), (4, 5), (-4, -5))),
}

ENCODINGS = ("canonical", "reversed", "renamed", "padded-metadata", "circuit-envelope")
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")


def canonical_object(formula: Formula) -> dict[str, object]:
    n, clauses = formula
    return {"n": n, "clauses": [list(c) for c in clauses]}


def encode(formula: Formula, kind: str) -> bytes:
    obj = canonical_object(formula)
    if kind == "reversed":
        obj["clauses"] = list(reversed(obj["clauses"]))
    elif kind == "renamed":
        obj["renaming"] = list(range(obj["n"], 0, -1))
    elif kind == "padded-metadata":
        obj["padding"] = "0" * 31
    elif kind == "circuit-envelope":
        obj = {"format": "cnf-as-circuit-input", "payload": obj}
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def decode(data: bytes) -> Formula:
    obj = json.loads(data.decode())
    if obj.get("format") == "cnf-as-circuit-input":
        obj = obj["payload"]
    n = int(obj["n"])
    clauses = tuple(tuple(int(x) for x in c) for c in obj["clauses"])
    # Clause order and metadata do not affect the represented source formula.
    return n, tuple(sorted(clauses))


def sat_under(formula: Formula, partial: tuple[int, ...]) -> bool:
    n, clauses = formula
    free = [i for i, value in enumerate(partial) if value == -1]
    for bits in itertools.product((0, 1), repeat=len(free)):
        values = list(partial)
        for idx, bit in zip(free, bits):
            values[idx] = bit
        good = True
        for clause in clauses:
            if not any((lit > 0 and values[abs(lit) - 1] == 1) or
                       (lit < 0 and values[abs(lit) - 1] == 0)
                       for lit in clause):
                good = False
                break
        if good:
            return True
    return False


def trace(encoded: bytes, wrapper: str) -> list[dict[str, object]]:
    digest = hashlib.sha256(encoded).hexdigest()[:16]
    initial = {"time": 0, "read_only_input": encoded.hex(), "control": "start"}
    later = [
        {"time": 1, "control": wrapper, "tag": digest},
        {"time": 2, "control": f"{wrapper}-internal", "tag": digest[::-1]},
        {"time": 3, "control": "halt", "answer": digest[-1] in "02468ace"},
    ]
    if wrapper == "DELAY":
        later[1:1] = [{"time": 1, "control": "dummy", "tag": i} for i in range(7)]
    if wrapper == "COPY":
        later[0]["copy"] = encoded.hex()
    if wrapper == "DEAD":
        later[0]["dead"] = "unreachable-branch"
    return [initial, *later]


def extract_source(full_trace: list[dict[str, object]]) -> Formula:
    return decode(bytes.fromhex(str(full_trace[0]["read_only_input"])))


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    point_queries = 0
    traces = 0
    explicit_table_entries = 0

    for name, formula in FAMILIES.items():
        canonical = (formula[0], tuple(sorted(formula[1])))
        for encoding in ENCODINGS:
            encoded = encode(formula, encoding)
            wrapper_tags: set[str] = set()
            for wrapper in WRAPPERS:
                tr = trace(encoded, wrapper)
                traces += 1
                recovered = extract_source(tr)
                assert recovered == canonical
                assertions += 1
                wrapper_tags.add(json.dumps(tr[1:], sort_keys=True))

                n = formula[0]
                for partial in itertools.product((-1, 0, 1), repeat=n):
                    direct = sat_under(canonical, partial)
                    external = sat_under(recovered, partial)
                    assert direct == external
                    assertions += 1
                    point_queries += 1
                explicit_table_entries += 3 ** n

            # Later traces differ across wrappers although source extraction
            # from the initial state is identical.
            assert len(wrapper_tags) == len(WRAPPERS)
            assertions += 1

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "MODELBRIDGE-0027",
        "claim": "INPUT-TRACE-SOURCE-LEAKAGE1",
        "status": "COMPUTATIONAL",
        "scope_warning": (
            "Finite audit of source recovery and pointwise compatibility only; "
            "no runtime lower bound or SAME_REALIZATION exposure theorem follows."
        ),
        "dimensions": {
            "families": len(FAMILIES),
            "encodings": len(ENCODINGS),
            "wrappers": len(WRAPPERS),
            "traces": traces,
        },
        "counts": {
            "assertions": assertions,
            "failures": 0,
            "point_queries": point_queries,
            "explicit_table_entries_across_traces": explicit_table_entries,
        },
        "runtime_seconds": round(elapsed, 6),
        "chunking": "Single exhaustive finite invocation below 30 seconds.",
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
    }
    path = Path("results/raw/review/2026-10-12_full_trace_source_leakage.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
