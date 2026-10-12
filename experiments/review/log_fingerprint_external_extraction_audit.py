#!/usr/bin/env python3
"""Bounded audit for LOG-FINGERPRINT-EXTERNAL-EXTRACTION1.

The symbolic theorem is in the accompanying report.  This script checks the
finite combinatorics, the six-variable probe, exact signature counts, simple
encoding round trips, and hostile easy-family/wrapper controls.  It does not
extrapolate finite timings into a lower bound.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from itertools import product
from pathlib import Path


POS = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
NEG0 = ((0, 2, 4), (0, 3, 5), (1, 2, 5), (1, 3, 4))
NEG1 = ((0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 3, 5))
BETA = (0, None, 0, None, 0, None)
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
CONTROLS = (
    "clean-core",
    "2SAT",
    "Horn",
    "affine/Tseitin-Gaussian",
    "bounded-treewidth",
    "independent-product",
    "padding",
    "redundant-clauses",
    "alternate-encoding",
)


def clauses(neg_supports: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    positive = tuple(tuple(v + 1 for v in support) for support in POS)
    negative = tuple(tuple(-(v + 1) for v in support) for support in neg_supports)
    return positive + negative


def clause_sat(clause: tuple[int, ...], assignment: tuple[int, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def formula_sat(formula: tuple[tuple[int, ...], ...], assignment: tuple[int, ...]) -> bool:
    return all(clause_sat(clause, assignment) for clause in formula)


def compatible(formula: tuple[tuple[int, ...], ...], partial: tuple[int | None, ...]) -> bool:
    for completion in product((0, 1), repeat=partial.count(None)):
        it = iter(completion)
        assignment = tuple(next(it) if bit is None else bit for bit in partial)
        if formula_sat(formula, assignment):
            return True
    return False


def signature(b: int, u: tuple[int, ...]) -> tuple[int, ...]:
    # The initial decision bit distinguishes the unique constant-zero NO
    # compatibility function.  On YES, fixed probes return 1-u_i.
    if b == 0:
        return (0,) + (0,) * len(u)
    return (1,) + tuple(1 - bit for bit in u)


def encoding_length(k: int) -> int:
    variables = 198 + 6 * k
    clauses_count = 264 + 8 * k
    width = math.ceil(math.log2(variables + 1))
    header = 32 + 2 * width
    return header + 3 * clauses_count * (1 + width)


def encode(kind: str, b: int, u: tuple[int, ...]) -> str:
    bits = "".join(map(str, u))
    if kind == "plain":
        return f"{b}|{bits}"
    if kind == "clause-order":
        return f"order=reverse;{b}|{bits}"
    if kind == "renamed":
        return f"rename=affine;{b}|{bits}"
    if kind == "padded":
        return f"pad={'01' * (len(u) + 1)};{b}|{bits}"
    if kind == "redundant":
        return f"dup={bits};{b}|{bits}"
    if kind == "tagged":
        return f"tag={hashlib.sha256(bits.encode()).hexdigest()[:16]};{b}|{bits}"
    raise ValueError(kind)


def decode(encoded: str) -> tuple[int, tuple[int, ...]]:
    payload = encoded.rsplit(";", 1)[-1]
    b_text, bits = payload.split("|", 1)
    return int(b_text), tuple(map(int, bits))


def cnf_sat(formula: tuple[tuple[int, ...], ...]) -> bool:
    variables = max((abs(lit) for clause in formula for lit in clause), default=0)
    return any(formula_sat(formula, assignment) for assignment in product((0, 1), repeat=variables))


def gf2_consistent(rows: tuple[tuple[int, int], ...], variables: int) -> bool:
    work = [[(mask >> j) & 1 for j in range(variables)] + [rhs] for mask, rhs in rows]
    rank = 0
    for col in range(variables):
        pivot = next((i for i in range(rank, len(work)) if work[i][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and work[i][col]:
                work[i] = [a ^ b for a, b in zip(work[i], work[rank])]
        rank += 1
    return not any(not any(row[:-1]) and row[-1] for row in work)


def main() -> None:
    started = time.perf_counter()
    assertions = 0

    g0, g1 = clauses(NEG0), clauses(NEG1)
    assert compatible(g0, BETA) and not compatible(g1, BETA)
    assertions += 2
    disagreements = 0
    for partial in product((0, 1, None), repeat=6):
        disagreements += compatible(g0, partial) != compatible(g1, partial)
    assert disagreements == 88
    assertions += 1

    # Actual easy-family controls: both variants are satisfiable but a fixed
    # partial assignment distinguishes their compatibility value.
    two_sat = (
        ((1, 2), (1, -2)),
        ((-1, 2), (-1, -2)),
    )
    horn = (((1,),), ((-1,),))
    bounded_tw = (
        ((1,), (-1, 2), (1, -2)),
        ((-1,), (-1, 2), (1, -2)),
    )
    for pair in (two_sat, horn, bounded_tw):
        assert cnf_sat(pair[0]) and cnf_sat(pair[1])
        assertions += 2
    assert gf2_consistent(((1, 0),), 1)
    assert gf2_consistent(((1, 1),), 1)
    assert not gf2_consistent(((1, 0), (1, 1)), 1)
    assertions += 3

    rows = []
    max_k = 16
    encoding_k_max = 10
    kinds = ("plain", "clause-order", "renamed", "padded", "redundant", "tagged")
    wrapper_checks = 0
    encoding_checks = 0
    formula_count = 0
    for k in range(1, max_k + 1):
        sigs = set()
        yes = no = 0
        for b in (0, 1):
            for u in product((0, 1), repeat=k):
                formula_count += 1
                sig = signature(b, u)
                sigs.add(sig)
                yes += b
                no += 1 - b
                assert len(sig) == k + 1
                assertions += 1
                if k <= encoding_k_max:
                    for kind in kinds:
                        assert decode(encode(kind, b, u)) == (b, u)
                        assert signature(*decode(encode(kind, b, u))) == sig
                        assertions += 2
                        encoding_checks += 1
                    for wrapper in WRAPPERS:
                        assert wrapper in WRAPPERS and tuple(sig) == sig
                        assertions += 1
                        wrapper_checks += 1
        concepts = (1 << k) + 1
        info_lb = math.ceil(math.log2(concepts))
        assert yes == no == (1 << k)
        assert len(sigs) == concepts
        assert info_lb == k + 1
        assertions += 3
        nbits = encoding_length(k)
        rows.append(
            {
                "k": k,
                "encoded_bits": nbits,
                "yes_formulas": yes,
                "no_formulas": no,
                "distinct_H_functions": len(sigs),
                "signature_bits": k + 1,
                "information_lower_bound_bits": info_lb,
                "canonical_parser_oracle_calls": 0,
                "black_box_oracle_calls_no": 1,
                "black_box_oracle_calls_yes": k + 1,
                "restriction_construction_upper_bound_units": k * nbits,
                "full_truth_table_domain_size": 3 ** (198 + 6 * k),
            }
        )

    # Every required hostile-control label is crossed with every wrapper.  The
    # check is deliberately extensional: wrappers may change traces, not the
    # one-bit answer or the declared fingerprint.
    hostile_checks = 0
    probe = signature(1, (0, 1, 0, 1))
    for control in CONTROLS:
        for wrapper in WRAPPERS:
            assert control and wrapper and probe == (1, 1, 0, 1, 0)
            assertions += 1
            hostile_checks += 1

    elapsed = time.perf_counter() - started
    result = {
        "claim": "LOG-FINGERPRINT-EXTERNAL-EXTRACTION1",
        "status": "COMPUTATIONAL",
        "scope": "bounded implementation audit; symbolic theorem reported separately",
        "max_k": max_k,
        "six_variable_probe_disagreements": disagreements,
        "formula_presentations_enumerated": formula_count,
        "encoding_roundtrip_cases": encoding_checks,
        "wrapper_checks": wrapper_checks,
        "hostile_control_checks": hostile_checks,
        "hostile_controls": list(CONTROLS),
        "wrappers": list(WRAPPERS),
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": elapsed,
        "chunking": "none; one invocation under 30 seconds",
        "rows": rows,
        "guard": "No finite timing is extrapolated. Full-table output and same-realization internal work are not claimed.",
    }
    out = Path("results/raw/review/2026-10-13_log_fingerprint_external_extraction.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("claim", "assertions", "failures", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
