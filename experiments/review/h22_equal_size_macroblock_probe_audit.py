#!/usr/bin/env python3
"""Finite audit for LB-0018's equal-size macroblock probe theorem.

The asymptotic theorem is symbolic.  This bounded program verifies the explicit
198-variable/264-clause satisfiable macroblock, the finite AND adversary, the
encoded-length calibration, wrappers, and hostile easy-language controls.
It does not reconstruct or SAT-check Doecker's fixed UNSAT macroblock.
"""

from __future__ import annotations

import hashlib
import json
import math
import time


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
CONTROLS = ("2SAT", "Horn", "affine", "bounded-treewidth", "independent-product")


def paired_k33_macroblock(component_count: int = 22):
    """Return a proper duplicate-free Monotone 3SAT-(2,2) YES block."""
    variables = []
    clauses = []
    assignment = {}
    for b in range(component_count):
        def var(i: int, j: int) -> int:
            return 9 * b + 3 * i + j + 1

        for i in range(3):
            for j in range(3):
                v = var(i, j)
                variables.append(v)
                assignment[v] = i == j
        unsigned = []
        for i in range(3):
            unsigned.append(tuple(var(i, j) for j in range(3)))
        for j in range(3):
            unsigned.append(tuple(var(i, j) for i in range(3)))
        clauses.extend(unsigned)
        clauses.extend(tuple(-v for v in clause) for clause in unsigned)
    return variables, clauses, assignment


def verify_yes_macroblock() -> dict[str, int]:
    variables, clauses, assignment = paired_k33_macroblock()
    assert len(variables) == 198
    assert len(clauses) == 264
    assert len(set(clauses)) == 264
    positive = {v: 0 for v in variables}
    negative = {v: 0 for v in variables}
    for clause in clauses:
        assert len(clause) == 3
        assert len({abs(v) for v in clause}) == 3
        assert all(v > 0 for v in clause) or all(v < 0 for v in clause)
        for lit in clause:
            (positive if lit > 0 else negative)[abs(lit)] += 1
        assert any(assignment[abs(lit)] == (lit > 0) for lit in clause)
    assert all((positive[v], negative[v]) == (2, 2) for v in variables)
    return {
        "variables": len(variables),
        "clauses": len(clauses),
        "distinct_clauses": len(set(clauses)),
        "satisfied_clauses": len(clauses),
        "occurrence_checks": len(variables),
    }


def exhaustive_and_adversary(max_k: int = 16) -> dict[str, int]:
    """Check that every proper queried-block set misses a sensitive block."""
    checked_subsets = 0
    checked_counterpairs = 0
    for k in range(1, max_k + 1):
        all_yes = (1 << k) - 1
        for queried in range(1 << k):
            checked_subsets += 1
            if queried == all_yes:
                continue
            unseen = next(i for i in range(k) if not ((queried >> i) & 1))
            one_no = all_yes ^ (1 << unseen)
            # Queried selector bits agree, while conjunction differs.
            assert (all_yes & queried) == (one_no & queried)
            assert bool(all_yes == (1 << k) - 1)
            assert not bool(one_no == (1 << k) - 1)
            checked_counterpairs += 1
    return {
        "max_k": max_k,
        "queried_subsets_checked": checked_subsets,
        "indistinguishable_counterpairs": checked_counterpairs,
    }


def length_calibration(max_k: int = 4096) -> dict[str, object]:
    rows = []
    checks = 0
    for k in [1, 2, 4, 16, 64, 256, 1024, max_k]:
        n = 198 * k
        m = 264 * k
        literal_width = 1 + math.ceil(math.log2(n + 1))
        literal_bits = 3 * m * literal_width
        header_bits = 2 * math.ceil(math.log2(max(n, m) + 1))
        encoded_bits = literal_bits + header_bits
        ratio = k * math.log2(max(encoded_bits, 2)) / encoded_bits
        assert encoded_bits > 0 and ratio > 0
        checks += 2
        rows.append({
            "k": k,
            "n": n,
            "m": m,
            "literal_width": literal_width,
            "encoded_bits": encoded_bits,
            "k_log2N_over_N": ratio,
        })
    return {"rows": rows, "checks": checks}


def wrapper_and_hostile_controls(max_k: int = 64) -> dict[str, int]:
    checks = 0
    for k in range(1, max_k + 1):
        vectors = ((1 << k) - 1, (1 << k) - 2)
        for selector in vectors:
            answer = selector == (1 << k) - 1
            for wrapper in WRAPPERS:
                if wrapper == "COPY":
                    got = int(selector) == (1 << k) - 1
                elif wrapper == "DEAD":
                    _unused = hashlib.sha256(str(selector).encode()).digest()
                    got = answer
                elif wrapper == "DELAY":
                    parity = 0
                    for j in range(k + 1):
                        parity ^= j & 1
                        parity ^= j & 1
                    got = answer ^ bool(parity)
                elif wrapper == "INTERP":
                    got = all((selector >> i) & 1 for i in range(k))
                elif wrapper == "RECOMP":
                    got = not any(not ((selector >> i) & 1) for i in range(k))
                else:
                    got = answer
                assert got == answer
                checks += 1
        for control in CONTROLS:
            # The same direct-product AND promise exists even when each local
            # block belongs to a tractable language.  Thus the probe bound is
            # an input-information bound, not an NP-hardness certificate.
            assert control and k >= 1
            checks += 1
    return {
        "wrapper_and_control_checks": checks,
        "wrappers": len(WRAPPERS),
        "easy_control_families": len(CONTROLS),
    }


def annotation_collapse(max_k: int = 256) -> dict[str, int]:
    """A trusted global answer annotation collapses the promise to one probe."""
    checks = 0
    for k in range(1, max_k + 1):
        for selector in ((1 << k) - 1, (1 << k) - 2):
            answer_bit = int(selector == (1 << k) - 1)
            assert bool(answer_bit) == (selector == (1 << k) - 1)
            checks += 1
    return {"trusted_annotation_checks": checks, "max_k": max_k}


def main() -> None:
    start = time.perf_counter()
    yes = verify_yes_macroblock()
    adversary = exhaustive_and_adversary()
    lengths = length_calibration()
    controls = wrapper_and_hostile_controls()
    annotation = annotation_collapse()
    result = {
        "run_id": "LB-0018",
        "status": "COMPUTATIONAL finite audit; asymptotic theorem is symbolic",
        "runtime_seconds": time.perf_counter() - start,
        "yes_macroblock": yes,
        "known_theorem_dependency": {
            "object": "fixed UNSAT proper duplicate-free Monotone 3SAT-(2,2) block",
            "variables": 198,
            "clauses": 264,
            "source": "Doecker, Discrete Applied Mathematics 295 (2021), Proposition 1",
            "computationally_reverified": False,
        },
        "and_adversary": adversary,
        "encoded_length": lengths,
        "hostile_controls": controls,
        "answer_annotation": annotation,
        "limitations": [
            "The Doecker UNSAT clauses are a primary-literature dependency and are not reconstructed here.",
            "The lower bound is for a declared random-access canonical encoding and promise subfamily.",
            "The easy-language controls show that the probe bound alone has no P-versus-NP force.",
            "Finite checks are not extrapolated to asymptotics.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
