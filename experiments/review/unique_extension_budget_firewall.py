#!/usr/bin/env python3
"""Bounded audit for PROMISEGATE1.

Checks the exact logarithmic program-budget padding inequality and the
smallest orbit example showing that source-orientation decoding can fail
while witness finding remains trivial.  Finite checks support, but do not
prove, the symbolic theorem in the matching MAIN report.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path


def budget(n: int, b0: int) -> int:
    return b0 + ((n + 2).bit_length() - 1)


def shear(x: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = x
    return (a, b, c ^ (a & b))


def permute_assignment(a: tuple[int, ...], p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(a)
    for old, new in enumerate(p):
        out[new] = a[old]
    return tuple(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-n", type=int, default=4096)
    args = ap.parse_args()
    start = time.perf_counter()
    assertions = 0
    failures: list[str] = []

    # Exact padding rule: N'+2 >= 2^c (N+2) buys c program bits.
    padding_cases = 0
    for b0 in range(0, 9):
        for c in range(0, 13):
            for n in range(args.max_n + 1):
                npad = (1 << c) * (n + 2) - 2
                assertions += 1
                padding_cases += 1
                if budget(npad, b0) < budget(n, b0) + c:
                    failures.append(f"padding:{b0}:{c}:{n}")

    # Polynomial-depth composition accounting: sum of D layer costs N^c.
    hierarchy_cases = 0
    for n in range(1, 257):
        for degree in range(0, 6):
            for depth in (1, max(1, n // 3), n):
                charged = depth * (n**degree)
                bound = n ** (degree + 1)
                assertions += 1
                hierarchy_cases += 1
                if charged > bound:
                    failures.append(f"hierarchy:{n}:{degree}:{depth}")

    # Promise-recognition firewall.  For every Boolean function C on at most
    # four inputs (represented by its truth table), both general validity
    # checks below hold exactly when C is identically zero:
    #   (i) c_C(u)=(C(u),0) has even parity for every u;
    #  (ii) P=id and J_C(x,t)=(x,t xor C(x)) are mutual inverses.
    # This is the finite shadow of the symbolic Circuit-UNSAT reductions.
    recognition_cases = 0
    for arity in range(0, 5):
        rows = 1 << arity
        for mask in range(1 << rows):
            all_zero = mask == 0
            even_charge_valid = all(((mask >> x) & 1) == 0 for x in range(rows))
            inverse_pair_valid = True
            for x in range(rows):
                cx = (mask >> x) & 1
                for t in (0, 1):
                    # P is identity, so J_C(P(x,t))=(x,t xor C(x)).
                    if (t ^ cx) != t:
                        inverse_pair_valid = False
            assertions += 2
            recognition_cases += 1
            if even_charge_valid != all_zero:
                failures.append(f"even-contract:{arity}:{mask}")
            if inverse_pair_valid != all_zero:
                failures.append(f"inverse-contract:{arity}:{mask}")

    # Graph of the quadratic involution S.  All-zero is a target-only witness
    # under every variable permutation, although the two 3-variable blocks
    # are exchanged by an automorphism and hence have no covariant orientation.
    models = []
    for x in itertools.product((0, 1), repeat=3):
        models.append(x + shear(x))
        assertions += 1
        if shear(shear(x)) != x:
            failures.append(f"involution:{x}")

    swap = (3, 4, 5, 0, 1, 2)
    model_set = set(models)
    assertions += 2
    if {permute_assignment(m, swap) for m in models} != model_set:
        failures.append("swap-not-automorphism")
    if {swap[i] for i in range(3)} == set(range(3)):
        failures.append("source-block-invariant")

    zero = (0, 0, 0, 0, 0, 0)
    permutation_cases = 0
    for p in itertools.permutations(range(6)):
        assertions += 2
        permutation_cases += 1
        if permute_assignment(zero, p) != zero:
            failures.append(f"zero-renaming:{p}")
        if zero not in {permute_assignment(m, p) for m in models}:
            failures.append(f"zero-not-model:{p}")

    elapsed = time.perf_counter() - start
    here = Path(__file__)
    code_sha = hashlib.sha256(here.read_bytes()).hexdigest()
    result = {
        "run_id": "PROMISEGATE1",
        "status": "PASS" if not failures else "FAIL",
        "assertions": assertions,
        "failures": failures,
        "parameters": {"max_n": args.max_n, "b0": [0, 8], "wrapper_bits": [0, 12]},
        "counts": {
            "padding_cases": padding_cases,
            "hierarchy_cases": hierarchy_cases,
            "recognition_truth_tables": recognition_cases,
            "orbit_models": len(models),
            "variable_permutations": permutation_cases,
        },
        "claims_checked": {
            "padding_budget": "floor(log2(N'+2)) >= floor(log2(N+2))+c",
            "hierarchy_bound": "D*N^k <= N^(k+1) for D<=N",
            "promise_recognition": "even-charge and claimed-inverse validity iff C is identically zero",
            "orientation": "block swap is an automorphism and moves the source block",
            "witness": "all-zero remains a model under all 6! variable permutations",
        },
        "limitations": [
            "finite arithmetic and orbit checks do not prove an asymptotic lower bound",
            "the symbolic search-equivalence theorem is proved separately in the report",
            "no claim is made for untagged encodings lacking a decoder",
        ],
        "elapsed_seconds": elapsed,
        "code_sha256": code_sha,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
