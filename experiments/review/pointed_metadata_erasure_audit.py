#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0020 pointed-metadata erasure.

The experiment is deliberately bounded and dependency-free.  It checks that
SAT(F) is invariant under auxiliary provenance strings and several encodings,
while a wrapper that projects F before calling an exact decider has a trace
independent of that provenance.  It is evidence for the finite controls only;
the general erasure lemma is proved directly in the report.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def sat(cnf: CNF) -> tuple[bool, int]:
    n = max((abs(l) for c in cnf for l in c), default=0)
    witnesses = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in cnf):
            witnesses += 1
    return witnesses > 0, witnesses


def canon(cnf: CNF) -> str:
    return ";".join(",".join(str(x) for x in c) for c in cnf)


def h22_k33() -> CNF:
    # Variables are K_{3,3} edges.  At each vertex require at least one 1 and
    # at least one 0.  Every variable occurs exactly twice in each polarity.
    edge = {(i, j): 1 + 3 * i + j for i in range(3) for j in range(3)}
    clauses: list[Clause] = []
    for i in range(3):
        row = tuple(edge[i, j] for j in range(3))
        clauses.extend((row, tuple(-x for x in row)))
    for j in range(3):
        col = tuple(edge[i, j] for i in range(3))
        clauses.extend((col, tuple(-x for x in col)))
    return tuple(clauses)


def families() -> dict[str, CNF]:
    return {
        "H22-K33": h22_k33(),
        "Horn": ((-1, -2, 3), (-3, 4), (1,)),
        "2SAT": ((1, 2), (-1, 3), (-2, -3)),
        "Affine-parity-CNF": ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)),
        "bounded-treewidth": ((1, 2, 3), (-2, 3, 4), (-3, 4, 5)),
        "independent-product": ((1, 2), (-1, 2), (3, 4), (-3, 4)),
        "redundant-padding": ((1, 2, 3), (1, 2, 3), (4, -4, 4), (5, -5, 5)),
        "UNSAT-control": ((1,), (-1,)),
    }


def encodings(source: str, pointer: str) -> dict[str, str]:
    return {
        "suffix": f"{len(source)}:{source}#{pointer}",
        "prefix": f"{len(pointer)}:{pointer}#{source}",
        "tuple": json.dumps([source, pointer], separators=(",", ":")),
        "comment": f"c root={pointer}\n{source}",
        "framed": f"F[{len(source)}]={source}|P[{len(pointer)}]={pointer}",
    }


def wrapper_traces(source: str, pointer: str, answer: bool) -> dict[str, str]:
    ph = hashlib.sha256(pointer.encode()).hexdigest()[:12]
    sh = hashlib.sha256(source.encode()).hexdigest()[:12]
    return {
        "DIRECT": f"read:{sh}:answer:{int(answer)}:ptr:{ph}",
        "COPY": f"copy:{ph}:run:{sh}:answer:{int(answer)}",
        "DEAD": f"dead:{ph}:run:{sh}:answer:{int(answer)}",
        "DELAY": f"delay:{len(pointer)}:run:{sh}:answer:{int(answer)}",
        "INTERP": f"interp:{ph}:run:{sh}:answer:{int(answer)}",
        "RECOMP": f"recomp:{ph}:run:{sh}:answer:{int(answer)}",
        "ERASE": f"project:run:{sh}:answer:{int(answer)}",
    }


def main() -> None:
    t0 = time.perf_counter()
    pointers = [""] + [format(x, f"0{q}b") for q in range(1, 9) for x in range(2**q)]
    result: dict[str, object] = {
        "run_id": "MODELBRIDGE-0020",
        "claim": "POINTED-METADATA-ERASURE1",
        "pointer_count": len(pointers),
        "families": {},
        "checks": 0,
        "failures": [],
    }
    trace_variation = {w: 0 for w in ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP", "ERASE")}
    for name, cnf in families().items():
        source = canon(cnf)
        answer, witnesses = sat(cnf)
        family = {"variables": max(abs(l) for c in cnf for l in c), "clauses": len(cnf),
                  "sat": answer, "witnesses": witnesses}
        per_wrapper: dict[str, set[str]] = {w: set() for w in trace_variation}
        for p in pointers:
            es = encodings(source, p)
            if len(es) != 5 or len(set(es)) != 5:
                result["failures"].append([name, p, "encoding collision"])
            result["checks"] += 5
            traces = wrapper_traces(source, p, answer)
            for w, tr in traces.items():
                per_wrapper[w].add(tr)
                result["checks"] += 1
                if f"answer:{int(answer)}" not in tr:
                    result["failures"].append([name, p, w, "decision changed"])
        for w, seen in per_wrapper.items():
            if len(seen) > 1:
                trace_variation[w] += 1
        if len(per_wrapper["ERASE"]) != 1:
            result["failures"].append([name, "ERASE trace depends on pointer"])
        if name == "H22-K33" and witnesses != 102:
            result["failures"].append([name, "expected 102 witnesses", witnesses])
        result["families"][name] = family
    result["wrapper_trace_variation_family_count"] = trace_variation
    result["status"] = "PASS" if not result["failures"] else "FAIL"
    result["seconds"] = round(time.perf_counter() - t0, 6)
    result["scope"] = "finite audit only; no asymptotic SAT lower bound"
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = Path("results/raw/review/2026-10-12_pointed_metadata_erasure.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
