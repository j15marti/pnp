#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0028.

This checks an exact finite collision: an input-oblivious operation/address
schedule plus the final SAT bit cannot determine a nonconstant residual
compatibility bit, even when both formulas are satisfiable.  It is a bounded
regression only; the report contains the symbolic normalization theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def sat_formula(formula: Formula, assignment: tuple[int, ...]) -> bool:
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in formula)


def satisfiable(formula: Formula, nvars: int, partial: dict[int, int] | None = None) -> bool:
    partial = partial or {}
    for bits in itertools.product((0, 1), repeat=nvars):
        if all(bits[i - 1] == value for i, value in partial.items()) and sat_formula(formula, bits):
            return True
    return False


def fixed_schedule(nvars: int, nclauses: int, width: int, wrapper: str, encoded_len: int) -> tuple[str, ...]:
    """A toy straight-line exhaustive-evaluation schedule; no data values."""
    ops: list[str] = [f"LEN[{encoded_len}]", "INIT_ACC"]
    wrapper_ops = {
        "DIRECT": (),
        "COPY": tuple(f"COPY_ADDR[{i}]" for i in range(encoded_len)),
        "DEAD": tuple(f"DEAD[{i}]" for i in range(3)),
        "DELAY": tuple(f"DELAY[{i}]" for i in range(5)),
        "INTERP": ("INTERP_ENTER", "INTERP_EXIT"),
        "RECOMP": ("RECOMP_ENTER", "RECOMP_EXIT"),
    }[wrapper]
    ops.extend(wrapper_ops)
    for a in range(1 << nvars):
        ops.append(f"ASSIGN[{a}]")
        for c in range(nclauses):
            ops.append(f"CLAUSE[{c}]")
            for j in range(width):
                ops.extend((f"READ_LIT[{c},{j}]", "EVAL_LIT", "OR"))
            ops.append("AND")
        ops.append("OR_ACC")
    ops.append("OUTPUT")
    return tuple(ops)


def encode(formula: Formula, nvars: int, variant: str) -> bytes:
    clauses = list(formula)
    if variant == "reversed":
        clauses = [tuple(reversed(c)) for c in reversed(clauses)]
    body = ";".join(",".join(("+" if x > 0 else "-") + str(abs(x)) for x in c) for c in clauses)
    if variant == "indexed":
        text = f"n={nvars}|m={len(clauses)}|{body}"
    elif variant == "signed":
        text = f"{nvars:02d}:{len(clauses):02d}:{body}"
    elif variant == "reversed":
        text = f"rev:{nvars}:{len(clauses)}:{body}"
    elif variant == "padded":
        text = f"pad:{nvars}:{len(clauses)}:{body}:" + "0" * 17
    elif variant == "wrapper":
        text = f"interp({nvars},{len(clauses)},{body})"
    else:
        raise ValueError(variant)
    return text.encode("ascii")


def regular_hypergraphs(n: int) -> list[tuple[tuple[int, int, int], ...]]:
    triples = list(itertools.combinations(range(1, n + 1), 3))
    out = []
    for hs in itertools.combinations(triples, 4):
        deg = [0] * (n + 1)
        for h in hs:
            for v in h:
                deg[v] += 1
        if all(deg[v] == 2 for v in range(1, n + 1)):
            out.append(hs)
    return out


def clean_core_pair() -> tuple[Formula, Formula, dict[int, int]]:
    """Find a duplicate-free signed monotone (2,2) pair on six variables."""
    hs = regular_hypergraphs(6)
    records: list[tuple[Formula, tuple[bool, ...]]] = []
    partials = [{i + 1: bits[i] for i in range(3)} for bits in itertools.product((0, 1), repeat=3)]
    for pos in hs:
        for neg in hs:
            formula: Formula = tuple(tuple(h) for h in pos) + tuple(tuple(-v for v in h) for h in neg)
            if satisfiable(formula, 6):
                records.append((formula, tuple(satisfiable(formula, 6, p) for p in partials)))
    for i, (f0, sig0) in enumerate(records):
        for f1, sig1 in records[i + 1:]:
            for j, (a, b) in enumerate(zip(sig0, sig1)):
                if a != b:
                    return f0, f1, partials[j]
    raise AssertionError("no clean-core collision pair found")


def normalize_width(formula: Formula, width: int = 3) -> Formula:
    return tuple(c + (c[-1],) * (width - len(c)) for c in formula)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=202610121600)
    args = ap.parse_args()

    t0 = time.perf_counter_ns()
    cc0, cc1, cc_partial = clean_core_pair()
    families: dict[str, tuple[Formula, Formula, int, dict[int, int]]] = {
        "3sat": (((1, 2, 3),), ((-1, -2, -3),), 3, {1: 0, 2: 0, 3: 0}),
        "2sat": (((1, 2),), ((-1, -2),), 2, {1: 0, 2: 0}),
        "horn": (((1,),), ((-1,),), 1, {1: 0}),
        "bounded_treewidth": (((1, 2), (-2, 3)), ((-1, -2), (-2, 3)), 3, {1: 0, 2: 0, 3: 1}),
        "affine_tseitin": (((1, 2), (-1, -2)), ((1, -2), (-1, 2)), 2, {1: 0, 2: 0}),
        "independent_product": (((1, 2), (3, 4)), ((-1, -2), (3, 4)), 4, {1: 0, 2: 0, 3: 1}),
        "padding_redundancy": (((1, 2, 3), (1, 2, 3), (4, -4)), ((-1, -2, -3), (-1, -2, -3), (4, -4)), 4, {1: 0, 2: 0, 3: 0}),
        "signed_monotone_22_core": (cc0, cc1, 6, cc_partial),
    }
    preprocess_ns = time.perf_counter_ns() - t0

    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    encodings = ("indexed", "signed", "reversed", "padded", "wrapper")
    checks = 0
    cases = 0
    eval_ns = 0
    extract_ns = 0
    reconstruct_ns = 0
    schedule_lengths: list[int] = []

    for family, (raw0, raw1, nvars, partial) in families.items():
        f0, f1 = normalize_width(raw0), normalize_width(raw1)
        e0_sat = satisfiable(f0, nvars)
        e1_sat = satisfiable(f1, nvars)
        h0 = satisfiable(f0, nvars, partial)
        h1 = satisfiable(f1, nvars, partial)
        assert e0_sat and e1_sat and h0 != h1, family
        for enc in encodings:
            a = encode(f0, nvars, enc)
            b = encode(f1, nvars, enc)
            width = max(len(a), len(b))
            a = a.ljust(width, b"#")
            b = b.ljust(width, b"#")
            for wrapper in wrappers:
                t = time.perf_counter_ns()
                out0, out1 = satisfiable(f0, nvars), satisfiable(f1, nvars)
                eval_ns += time.perf_counter_ns() - t
                t = time.perf_counter_ns()
                s0 = fixed_schedule(nvars, len(f0), 3, wrapper, len(a))
                s1 = fixed_schedule(nvars, len(f1), 3, wrapper, len(b))
                view0, view1 = (s0, out0), (s1, out1)
                extract_ns += time.perf_counter_ns() - t
                t = time.perf_counter_ns()
                reconstruction_collision = view0 == view1 and h0 != h1
                reconstruct_ns += time.perf_counter_ns() - t
                assert a != b
                assert out0 == out1 == True
                assert s0 == s1
                assert view0 == view1
                assert reconstruction_collision
                checks += 5
                cases += 1
                schedule_lengths.append(len(s0))

    result = {
        "run_id": "MODELBRIDGE-0028",
        "seed": args.seed,
        "status": "COMPUTATIONAL",
        "symbolic_claim": "schedule_plus_decision_does_not_determine_compatibility",
        "families": list(families),
        "encodings": list(encodings),
        "wrappers": list(wrappers),
        "cases": cases,
        "checks": checks,
        "failures": 0,
        "clean_core_partial": cc_partial,
        "clean_core_pair_sha256": [
            hashlib.sha256(repr(cc0).encode()).hexdigest(),
            hashlib.sha256(repr(cc1).encode()).hexdigest(),
        ],
        "schedule_length_min": min(schedule_lengths),
        "schedule_length_max": max(schedule_lengths),
        "measured_ns": {
            "preprocessing": preprocess_ns,
            "decision_evaluation": eval_ns,
            "schedule_extraction": extract_ns,
            "collision_reconstruction_check": reconstruct_ns,
        },
        "scope_warning": "Finite regression only; no asymptotic inference.",
    }
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
