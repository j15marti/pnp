#!/usr/bin/env python3
"""Independent finite audit for the arbitrary-selector realization theorem.

The symbolic theorem is proved in the accompanying report.  This script
exhausts every two-block selector for h <= 3, checks both the one-clause and
private-variable guard realizations, checks every one-clause deletion, audits
dense affine selectors over GF(2), and records the exponent firewalls.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction


def bits(x: int, h: int) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(h))


def full_sign_clause_value(row: int, s: int, h: int) -> bool:
    """C_s is false exactly at row s."""
    rb = bits(row, h)
    sb = bits(s, h)
    return any((rb[i] == 1) if sb[i] == 0 else (rb[i] == 0) for i in range(h))


def one_clause_bad_blocks(selector: tuple[int, ...], row: int, h: int, B: int) -> list[int]:
    bad = []
    for j in range(B):
        clauses = [s for s, target in enumerate(selector) if target == j]
        if not all(full_sign_clause_value(row, s, h) for s in clauses):
            bad.append(j)
    return bad


def private_guard_block_sat(selector: tuple[int, ...], row: int, h: int, B: int, j: int) -> bool:
    """Existentially solve fresh u_s in (C_s or u_s)&(C_s or not u_s)."""
    for s, target in enumerate(selector):
        if target != j:
            continue
        if not full_sign_clause_value(row, s, h):
            return False
    return True


def formula_models_after_delete(h: int, deleted: int) -> list[int]:
    rows = range(1 << h)
    return [
        row
        for row in rows
        if all(s == deleted or full_sign_clause_value(row, s, h) for s in rows)
    ]


def affine_selector(row: int, h: int) -> int:
    """A=(J+I) over GF(2): output bit i is parity of all inputs except i."""
    rb = bits(row, h)
    out = 0
    for i in range(h):
        bit = 0
        for k in range(h):
            if k != i:
                bit ^= rb[k]
        out |= bit << i
    return out


def path_attainable(word: str) -> set[int]:
    cur = {0}
    for ch in word:
        steps = {1, 3} if ch == "F" else {2, 4}
        cur = {(x + y) % 5 for x in cur for y in steps}
    return cur


def main() -> None:
    checks = 0
    maps = 0
    rows_checked = 0
    deletion_cases = 0
    per_h = []

    for h in (1, 2, 3):
        R = 1 << h
        local_maps = 0
        local_rows = 0
        for selector in itertools.product(range(2), repeat=R):
            maps += 1
            local_maps += 1
            for row in range(R):
                bad = one_clause_bad_blocks(selector, row, h, 2)
                assert bad == [selector[row]]
                checks += 1
                for j in range(2):
                    assert private_guard_block_sat(selector, row, h, 2, j) == (j != selector[row])
                    checks += 1
                rows_checked += 1
                local_rows += 1
            for deleted in range(R):
                assert formula_models_after_delete(h, deleted) == [deleted]
                checks += 1
                deletion_cases += 1
        per_h.append({"h": h, "selector_maps": local_maps, "row_checks": local_rows})

    affine = []
    for h in (2, 4, 6):
        R = 1 << h
        images = [affine_selector(row, h) for row in range(R)]
        assert sorted(images) == list(range(R))
        checks += 1
        for row in range(R):
            assert affine_selector(affine_selector(row, h), h) == row
            checks += 1
            for input_bit in range(h):
                changed = affine_selector(row ^ (1 << input_bit), h) ^ affine_selector(row, h)
                assert changed.bit_count() == h - 1
                checks += 1
        affine.append({
            "h": h,
            "permutation": True,
            "self_inverse": True,
            "changed_output_bits_per_input_flip": h - 1,
        })

    scaling = []
    for q in (64, 128, 256, 512, 1024):
        log2_table = Fraction(195, 1000) * q + math.log2(math.ceil(Fraction(65, 100) * q))
        scaling.append({
            "log2_N": q,
            "selector_table_effective_exponent": float(log2_table / q),
            "below_sqrt_N": log2_table < Fraction(q, 2),
        })
        assert log2_table < Fraction(q, 2)
        checks += 1

    path_words = ["BBB", "FBB", "FFF", "BB"]
    expected_forbidden = [{4}, {3}, {1}, {0, 2}]
    forbidden = []
    for word, expected in zip(path_words, expected_forbidden):
        got = set(range(5)) - path_attainable(word)
        assert got == expected
        checks += 1
        forbidden.append(sorted(got))
    coverage = [sum(delta in f for f in expected_forbidden) for delta in range(5)]
    assert coverage == [1, 1, 1, 1, 1]
    checks += 1

    child_exponent = Fraction(195 + 650 + 350, 1000)
    assert child_exponent == Fraction(239, 200)
    checks += 1
    alpha_boundary = Fraction(134070, 100000) - Fraction(133, 100)
    assert alpha_boundary == Fraction(107, 10000)
    assert Fraction(106, 10000) < alpha_boundary
    checks += 2

    source_sha = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    out = {
        "status": "PASS",
        "mode": "exhaustive for all two-block selectors at h=1,2,3; exact algebraic controls otherwise",
        "selector_maps": maps,
        "selector_rows_checked": rows_checked,
        "one_clause_deletion_cases": deletion_cases,
        "assertions": checks,
        "per_h": per_h,
        "affine_J_plus_I_even_h": affine,
        "scaling": scaling,
        "explicit_full_child_bits_exponent": float(child_exponent),
        "advice_enumeration_alpha_boundary": float(alpha_boundary),
        "safe_alpha": 0.0106,
        "t5_H9_path_words": path_words,
        "t5_H9_forbidden_differences": forbidden,
        "t5_H9_unique_bad_path_per_difference": coverage,
        "python": sys.version.split()[0],
        "script_sha256": source_sha,
        "limitations": [
            "finite checks do not prove asymptotic runtime lower bounds",
            "the arbitrary-selector theorem is symbolic and is proved separately",
            "the T5 check authenticates the four endpoint relations, not every source arc of H9 or H33",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
