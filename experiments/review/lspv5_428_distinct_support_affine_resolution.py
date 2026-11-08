#!/usr/bin/env python3
"""LSPV-5/428: distinct-support 3-CNF affine-extraction audit.

This is a finite, exact control.  It checks a 12-clause proper 3-CNF in
which every unsigned source support is distinct, verifies two explicit
five-step ordinary-Resolution derivations, and exhaustively computes the
projection to the two exported variables.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


Clause = tuple[int, ...]


SOURCES: dict[str, Clause] = {
    "C1": (1, -3, 4),
    "C2": (1, -4, 5),
    "C3": (1, -5, -3),
    "C4": (2, 3, 6),
    "C5": (2, -6, 7),
    "C6": (2, -7, 3),
    "D1": (-1, -8, 9),
    "D2": (-1, -9, 10),
    "D3": (-1, -10, -8),
    "D4": (-2, 8, 11),
    "D5": (-2, -11, 12),
    "D6": (-2, -12, 8),
}

TRACE = [
    ("R1", "C1", "C2", 4, (1, -3, 5)),
    ("R2", "R1", "C3", 5, (1, -3)),
    ("R3", "C4", "C5", 6, (2, 3, 7)),
    ("R4", "R3", "C6", 7, (2, 3)),
    ("R5", "R4", "R2", 3, (1, 2)),
    ("S1", "D1", "D2", 9, (-1, -8, 10)),
    ("S2", "S1", "D3", 10, (-1, -8)),
    ("S3", "D4", "D5", 11, (-2, 8, 12)),
    ("S4", "S3", "D6", 12, (-2, 8)),
    ("S5", "S4", "S2", 8, (-1, -2)),
]


def canon(clause: Clause) -> Clause:
    return tuple(sorted(set(clause), key=lambda z: (abs(z), z < 0)))


def is_tautology(clause: Clause) -> bool:
    s = set(clause)
    return any(-lit in s for lit in s)


def resolve(left: Clause, right: Clause, pivot: int) -> Clause:
    """Strict oriented Resolution: +pivot left, -pivot right."""
    if pivot not in left or -pivot not in right:
        raise ValueError("oriented pivot absent")
    out = tuple(lit for lit in left if lit != pivot) + tuple(
        lit for lit in right if lit != -pivot
    )
    if is_tautology(out):
        raise ValueError("tautological resolvent")
    return canon(out)


def satisfies(clause: Clause, bits: tuple[bool, ...]) -> bool:
    return any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)


def model(bits: tuple[bool, ...], names: list[str] | None = None) -> dict[str, int]:
    labels = names or [str(i) for i in range(1, len(bits) + 1)]
    return {name: int(value) for name, value in zip(labels, bits)}


def satisfiable(clauses: list[Clause], nvars: int) -> bool:
    return any(all(satisfies(c, bits) for c in clauses)
               for bits in itertools.product((False, True), repeat=nvars))


def exhaustive_simple_support_2cnf_floor() -> dict[str, int | bool]:
    """Check the finite boundary relevant to the two six-clause cores.

    Every formula considered has proper binary clauses and at most one signed
    clause on each unsigned variable pair.  A minimally UNSAT formula with at
    most five clauses has at most four variables (the standard deficiency
    lower bound supplies the symbolic reduction); this enumerates that entire
    reduced range.
    """
    formulas = 0
    unsat = 0
    for nvars in range(2, 5):
        supports = list(itertools.combinations(range(1, nvars + 1), 2))
        for m in range(1, min(5, len(supports)) + 1):
            for selected in itertools.combinations(supports, m):
                for signs in itertools.product((1, -1), repeat=2 * m):
                    clauses = []
                    for idx, (u, v) in enumerate(selected):
                        clauses.append((signs[2 * idx] * u, signs[2 * idx + 1] * v))
                    formulas += 1
                    if not satisfiable(clauses, nvars):
                        unsat += 1
    return {
        "formulas_checked": formulas,
        "unsat_found": unsat,
        "no_unsat_with_at_most_five_clauses": unsat == 0,
    }


def main() -> None:
    started = time.perf_counter()
    proper = all(len(c) == 3 and len({abs(x) for x in c}) == 3 and not is_tautology(c)
                 for c in SOURCES.values())
    supports = [tuple(sorted(abs(x) for x in c)) for c in SOURCES.values()]
    distinct_supports = len(supports) == len(set(supports))

    derived: dict[str, Clause] = dict(SOURCES)
    trace_rows = []
    for name, left, right, pivot, expected in TRACE:
        actual = resolve(derived[left], derived[right], pivot)
        assert actual == canon(expected), (name, actual, canon(expected))
        derived[name] = actual
        trace_rows.append({
            "name": name,
            "left": left,
            "right": right,
            "pivot": pivot,
            "clause": list(actual),
        })

    names = ["x", "y", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    projection_counts = {(x, y): 0 for x in (0, 1) for y in (0, 1)}
    total_models = 0
    for bits in itertools.product((False, True), repeat=12):
        if all(satisfies(c, bits) for c in SOURCES.values()):
            total_models += 1
            projection_counts[(int(bits[0]), int(bits[1]))] += 1
    assert set(k for k, v in projection_counts.items() if v) == {(0, 1), (1, 0)}

    deletion_witnesses: dict[str, dict[str, int]] = {}
    for omitted in SOURCES:
        kept = [c for name, c in SOURCES.items() if name != omitted]
        witness = None
        for bits in itertools.product((False, True), repeat=12):
            if bits[0] == bits[1] and all(satisfies(c, bits) for c in kept):
                witness = model(bits, names)
                break
        assert witness is not None, omitted
        deletion_witnesses[omitted] = witness

    corrupt_controls = {}
    for label, left, right, pivot in [
        ("wrong_pivot", SOURCES["C1"], SOURCES["C2"], 5),
        ("reversed_orientation", SOURCES["C2"], SOURCES["C1"], 4),
        ("missing_negative_pivot", SOURCES["C1"], SOURCES["C4"], 4),
    ]:
        try:
            resolve(left, right, pivot)
            corrupt_controls[label] = "ACCEPTED_UNEXPECTEDLY"
        except ValueError as exc:
            corrupt_controls[label] = f"REJECTED: {exc}"
    assert all(v.startswith("REJECTED") for v in corrupt_controls.values())

    two_cnf_floor = exhaustive_simple_support_2cnf_floor()
    assert two_cnf_floor["no_unsat_with_at_most_five_clauses"]
    first_core = [tuple(lit for lit in SOURCES[name] if abs(lit) not in (1, 2))
                  for name in ("C1", "C2", "C3", "C4", "C5", "C6")]
    second_core = [tuple(lit for lit in SOURCES[name] if abs(lit) not in (1, 2))
                   for name in ("D1", "D2", "D3", "D4", "D5", "D6")]
    assert not satisfiable(first_core, 7)
    # Remap variables 8..12 to 1..5 before the compact satisfiability check.
    remap = {8: 1, 9: 2, 10: 3, 11: 4, 12: 5}
    second_core_small = [tuple((1 if lit > 0 else -1) * remap[abs(lit)] for lit in c)
                         for c in second_core]
    assert not satisfiable(second_core_small, 5)

    dimacs_lines = ["c LSPV-5/428 distinct-support affine control", "p cnf 12 12"]
    dimacs_lines.extend(" ".join(map(str, c)) + " 0" for c in SOURCES.values())
    dimacs = "\n".join(dimacs_lines) + "\n"

    result = {
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "source_clauses": {k: list(v) for k, v in SOURCES.items()},
        "proper_3cnf": proper,
        "unsigned_supports_pairwise_distinct": distinct_supports,
        "resolution_trace": trace_rows,
        "derived_facets": {"x_or_y": list(derived["R5"]), "not_x_or_not_y": list(derived["S5"])},
        "logical_resolution_nodes": len(TRACE),
        "projection_model_counts": {f"x={x},y={y}": n for (x, y), n in projection_counts.items()},
        "projection_exactly_xor_one": True,
        "total_models": total_models,
        "every_source_clause_essential_for_xor_implication": True,
        "deletion_witnesses": deletion_witnesses,
        "corrupt_controls": corrupt_controls,
        "simple_support_2cnf_five_clause_floor": two_cnf_floor,
        "six_clause_core_is_unsat": True,
        "dimacs_utf8_bytes": len(dimacs.encode("utf-8")),
        "dimacs_sha256": hashlib.sha256(dimacs.encode("utf-8")).hexdigest(),
        "scope": "ordinary Resolution derivation only; no claim that historical LOCAL-CONVERT accepts the pair as GF(2)",
        "runtime_seconds_before_serialization": round(time.perf_counter() - started, 6),
        "max_rss_kib_before_serialization": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }

    out_dir = Path("experiments/review/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "lspv5_428_distinct_support_affine.cnf").write_text(dimacs, encoding="utf-8")
    (out_dir / "lspv5_428_distinct_support_affine_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
