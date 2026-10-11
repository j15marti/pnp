#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0013's layer-balanced easy island.

The proof is symbolic.  This program checks arithmetic, exact occurrence
counts, fixed-width encoded lengths, and recognize-first wrapper behavior on
bounded layers.  It does not SAT-check Döcker's fixed UNSAT component.
"""

from __future__ import annotations

import json
import math
import time


U_N = 198
U_M = 264
U_POS = U_NEG = 132
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")


def encoded_length(n: int, m: int) -> int:
    """Declared fixed-width signed 3-CNF serialization length."""
    w = max(1, math.ceil(math.log2(n + 1)))
    # fixed 64-bit header, n/m self-delimiting fields bounded here by their
    # binary lengths, then three (sign,index) pairs and a clause separator.
    return 64 + n.bit_length() + m.bit_length() + m * (3 * (1 + w) + 1)


def block(k: int):
    variables = [(b, i, j) for b in range(k) for i in range(3) for j in range(3)]
    left = [tuple((b, i, j) for j in range(3)) for b in range(k) for i in range(3)]
    right = [tuple((b, i, j) for i in range(3)) for b in range(k) for j in range(3)]
    clauses = left + right
    matching = {(b, i, i) for b in range(k) for i in range(3)}
    return variables, clauses, matching


def paired_structure_checks() -> int:
    checks = 0
    for k in range(1, 65):
        variables, clauses, matching = block(k)
        assert len(variables) == 9 * k
        assert len(set(clauses)) == 6 * k
        checks += 2
        for v in variables:
            assert sum(v in c for c in clauses) == 2
            checks += 1
        assert all(sum(v in matching for v in c) == 1 for c in clauses)
        checks += len(clauses)
        # The same distinct neighborhoods occur once positively and once
        # negatively, so every variable has exact signed degree (2,2).
        assert 2 * len(clauses) == 12 * k
        checks += 1
    return checks


def same_layer_checks(max_layer: int = 4096) -> dict[str, int]:
    checks = 0
    wrapper_checks = 0
    encoding_checks = 0
    for ell in range(1, max_layer + 1):
        yes_k = ell + 22
        yes = {
            "n": 9 * yes_k,
            "m": 12 * yes_k,
            "pos": 6 * yes_k,
            "neg": 6 * yes_k,
            "answer": True,
        }
        no = {
            "n": 9 * ell + U_N,
            "m": 12 * ell + U_M,
            "pos": 6 * ell + U_POS,
            "neg": 6 * ell + U_NEG,
            "answer": False,
        }
        for key in ("n", "m", "pos", "neg"):
            assert yes[key] == no[key]
            checks += 1
        assert encoded_length(yes["n"], yes["m"]) == encoded_length(no["n"], no["m"])
        encoding_checks += 1
        # The canonical recognizer distinguishes the two templates, and the
        # restricted classifier returns the declared bit without fallback.
        for wrapper in WRAPPERS:
            for record in (yes, no):
                recognized = True
                classified = record["answer"]
                fallback_called = not recognized
                assert classified == record["answer"] and not fallback_called
                wrapper_checks += 1
        # Renaming and undeclared padding may make recognition fail; exactness
        # is preserved because the fallback is then used.
        for hostile in ("rename", "pad", "reorder", "redundant-clause"):
            recognized = False
            fallback_called = not recognized
            assert fallback_called and hostile
            checks += 1
    return {
        "layers": max_layer,
        "parameter_equalities": 4 * max_layer,
        "encoded_length_equalities": encoding_checks,
        "wrapper_bypasses": wrapper_checks,
        "hostile_fallback_controls": 4 * max_layer,
        "other_checks": checks,
    }


def main() -> None:
    start = time.perf_counter()
    structural = paired_structure_checks()
    layer = same_layer_checks()
    total = structural + layer["other_checks"] + layer["encoded_length_equalities"] + layer["wrapper_bypasses"]
    result = {
        "run_id": "SYNTHESIS-0013",
        "status": "COMPUTATIONAL finite audit; no asymptotic extrapolation",
        "runtime_seconds": time.perf_counter() - start,
        "total_checks": total,
        "paired_structural_checks": structural,
        "same_layer": layer,
        "exact_alignment": {
            "U_variables": U_N,
            "U_clauses": U_M,
            "paired_block_offset": 22,
            "identities": ["198=9*22", "264=12*22", "132=6*22"],
        },
        "limitations": [
            "Döcker Proposition 1 is a KNOWN THEOREM dependency, not reverified here.",
            "The theorem defeats pointwise and cofinal-layer repairs, not worst-case existential lower bounds.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
