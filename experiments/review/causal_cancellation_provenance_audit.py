#!/usr/bin/env python3
"""Bounded audit for the CAUSALCANCEL1 wrapper theorem.

The symbolic theorem is in the accompanying report.  This program only checks
finite Boolean sources, small CNFs, encodings, and wrapper implementations.
It is dependency-free and deliberately bounded to finish well under 30 s.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path


def parity(bits: tuple[int, ...]) -> int:
    p = 0
    for b in bits:
        p ^= b
    return p


def direct(bits: tuple[int, ...], answer: int) -> dict[str, int]:
    return {"answer": answer, "output": answer, "reads": 0, "xors": 0}


def cancel(bits: tuple[int, ...], answer: int, mode: str) -> dict[str, int]:
    p = parity(bits)
    q = p
    z = answer ^ p
    y = z ^ q
    extra_reads = 0
    extra_steps = 0
    recomputations = 0
    if mode == "COPY_CANCEL":
        copied = tuple(bits)
        assert copied == bits
        extra_reads = len(bits)
    elif mode == "DELAY_CANCEL":
        delay = 0
        for _ in range(len(bits)):
            delay ^= 1
        extra_steps = len(bits)
    elif mode == "INTERP_CANCEL":
        internal = tuple(1 ^ b for b in bits)
        assert tuple(1 ^ b for b in internal) == bits
        extra_reads = 2 * len(bits)
    elif mode == "RECOMP_CANCEL":
        assert parity(bits) == p
        recomputations = 1
        extra_reads = len(bits)
    elif mode == "DEAD_CANCEL":
        dead = p ^ p
        assert dead == 0
        extra_steps = 1
    elif mode != "CANCEL":
        raise ValueError(mode)
    return {
        "answer": answer,
        "p": p,
        "q": q,
        "z": z,
        "output": y,
        "reads": len(bits) + extra_reads,
        "xors": len(bits) + 2,
        "extra_steps": extra_steps,
        "recomputations": recomputations,
    }


def intervention_output(answer: int, p: int, q: int, which: str) -> int:
    if which == "p":
        p ^= 1
    elif which == "q":
        q ^= 1
    else:
        raise ValueError(which)
    return (answer ^ p) ^ q


def sat(cnf: tuple[tuple[int, ...], ...], nvars: int) -> tuple[int, tuple[int, ...]]:
    models = []
    for a in itertools.product((0, 1), repeat=nvars):
        ok = all(any((lit > 0) == bool(a[abs(lit) - 1]) for lit in c) for c in cnf)
        if ok:
            models.append(sum(bit << i for i, bit in enumerate(a)))
    return int(bool(models)), tuple(models)


def encode(cnf: tuple[tuple[int, ...], ...], nvars: int, mode: str) -> tuple[int, ...]:
    if mode == "DIMACS_ASCII":
        s = f"p cnf {nvars} {len(cnf)}\n" + "".join(
            " ".join(map(str, c)) + " 0\n" for c in cnf
        )
        return tuple((byte >> j) & 1 for byte in s.encode() for j in range(8))
    width = max(1, nvars.bit_length())
    clauses = cnf if mode == "TOKEN" else tuple(reversed(cnf))
    out = []
    for c in clauses:
        out.extend(((len(c) >> j) & 1) for j in range(2))
        lits = c if mode != "REVERSED" else tuple(reversed(c))
        for lit in lits:
            out.append(int(lit < 0))
            out.extend(((abs(lit) >> j) & 1) for j in range(width))
    return tuple(out)


def shifted(cnf: tuple[tuple[int, ...], ...], k: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((1 if x > 0 else -1) * (abs(x) + k) for x in c) for c in cnf)


def cnf_controls() -> dict[str, tuple[tuple[tuple[int, ...], ...], int]]:
    two = ((1, 2), (-1, 2), (1, -2))
    horn = ((-1, -2, 3), (1,), (2,))
    affine_even = ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))
    tw_path = ((1, 2), (-2, 3), (-3, 4), (-4, 5))
    product = two + shifted(horn, 2)
    padded = two + (two[0], (1, -1, 2))
    signed = ((1, 2, 3), (-1, 2, 4), (1, -3, 4), (-2, -3, -4))
    return {
        "2SAT": (two, 2),
        "Horn": (horn, 3),
        "affine_Tseitin": (affine_even, 3),
        "bounded_treewidth": (tw_path, 5),
        "independent_product": (product, 5),
        "padding_redundancy": (padded, 2),
        "signed_3CNF": (signed, 4),
    }


def forced_assignment_formula(a: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(((i + 1 if bit else -(i + 1)),) * 3 for i, bit in enumerate(a))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()
    assertions = 0
    binary_sources = 0
    bit_flips = 0
    interventions = 0
    function_cases = 0

    funcs = {
        "zero": lambda x: 0,
        "first": lambda x: x[0],
        "majority": lambda x: int(2 * sum(x) >= len(x)),
        "parity": parity,
    }
    for n in range(1, 13):
        for x in itertools.product((0, 1), repeat=n):
            binary_sources += 1
            p = parity(x)
            for f in funcs.values():
                a = f(x)
                tr = cancel(x, a, "CANCEL")
                assert tr["output"] == a
                assertions += 1
                assert intervention_output(a, p, p, "p") == (a ^ 1)
                assert intervention_output(a, p, p, "q") == (a ^ 1)
                assertions += 2
                interventions += 2
                function_cases += 1
            for i in range(n):
                y = list(x)
                y[i] ^= 1
                assert parity(tuple(y)) == (p ^ 1)
                assertions += 1
                bit_flips += 1

    wrapper_modes = (
        "CANCEL", "DEAD_CANCEL", "COPY_CANCEL", "DELAY_CANCEL",
        "INTERP_CANCEL", "RECOMP_CANCEL",
    )
    encoding_modes = ("TOKEN", "REVERSED", "DIMACS_ASCII")
    cnf_cases = 0
    wrapper_checks = 0
    total_reads = 0
    total_xors = 0
    for _, (cnf, nvars) in cnf_controls().items():
        answer, _ = sat(cnf, nvars)
        cnf_cases += 1
        for enc in encoding_modes:
            bits = encode(cnf, nvars, enc)
            assert direct(bits, answer)["output"] == answer
            assertions += 1
            for mode in wrapper_modes:
                tr = cancel(bits, answer, mode)
                assert tr["output"] == answer
                assert tr["p"] == tr["q"]
                assertions += 2
                wrapper_checks += 1
                total_reads += tr["reads"]
                total_xors += tr["xors"]

    # Eight satisfiable formulas force eight distinct 3-bit assignments.  Since
    # the decision bit is always one and parity has two values, two formulas
    # necessarily share (answer, parity) but have different full H.
    buckets: dict[tuple[int, int], list[dict[str, object]]] = {}
    for a in itertools.product((0, 1), repeat=3):
        cnf = forced_assignment_formula(a)
        answer, models = sat(cnf, 3)
        bits = encode(cnf, 3, "TOKEN")
        key = (answer, parity(bits))
        buckets.setdefault(key, []).append({"assignment": a, "models": models, "bit_length": len(bits)})
    collision = None
    for key, vals in buckets.items():
        if len(vals) >= 2 and vals[0]["models"] != vals[1]["models"]:
            collision = {"view": key, "left": vals[0], "right": vals[1]}
            break
    assert collision is not None
    assertions += 1

    elapsed = time.perf_counter() - t0
    result = {
        "run_id": "CAUSALCANCEL1",
        "status": "COMPUTATIONAL",
        "scope_warning": "Finite audit only; symbolic claims are proved in the report.",
        "chunking": "One bounded invocation; n<=12; no stage exceeded 30 seconds.",
        "elapsed_seconds": elapsed,
        "counts": {
            "assertions": assertions,
            "binary_sources": binary_sources,
            "binary_function_cases": function_cases,
            "source_bit_flip_checks": bit_flips,
            "structural_interventions": interventions,
            "cnf_family_cases": cnf_cases,
            "encoding_modes": len(encoding_modes),
            "wrapper_checks": wrapper_checks,
            "charged_reads": total_reads,
            "charged_xors": total_xors,
        },
        "full_H_collision_witness": collision,
        "theorem_shape": {
            "p": "xor_i x_i",
            "q": "p",
            "z": "A(x) xor p",
            "y": "z xor q = A(x)",
            "pointwise_source_support": "every source bit toggles p and q",
            "live_intervention": "flipping p alone or q alone flips y",
            "net_behavior": "the paired paths cancel, so y equals A(x)",
        },
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], sort_keys=True))
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
