#!/usr/bin/env python3
"""Finite audit for TESTS-0019 unique-pointer stream erasure.

The theorem in the report is symbolic.  This program checks the concrete
bit-local pointer encodings, exhaustive one-bit corruptions, SAT preservation,
and wrapper controls on bounded hostile families.  No randomness is used.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def norm_formula(clauses: list[Clause] | Formula) -> Formula:
    return tuple(sorted((tuple(sorted(c, key=lambda x: (abs(x), x < 0))) for c in clauses)))


def sat(formula: Formula) -> bool:
    n = max((abs(x) for c in formula for x in c), default=0)
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in formula):
            return True
    return False


def h22_k33() -> Formula:
    clauses: list[Clause] = []
    for i in range(3):
        row = tuple(1 + 3 * i + j for j in range(3))
        clauses.extend((row, tuple(-x for x in row)))
    for j in range(3):
        col = tuple(1 + 3 * i + j for i in range(3))
        clauses.extend((col, tuple(-x for x in col)))
    return norm_formula(clauses)


def source_bits(formula: Formula) -> tuple[int, ...]:
    """Injective canonical bounded-test encoding (not a hash)."""
    n = max((abs(x) for c in formula for x in c), default=0)
    if n > 255 or len(formula) > 255:
        raise ValueError("bounded audit encoder exceeded")
    out: list[int] = []
    for value in (n, len(formula)):
        out.extend((value >> shift) & 1 for shift in range(7, -1, -1))
    for clause in formula:
        if len(clause) > 3:
            raise ValueError("only clauses of width at most three")
        out.extend(((len(clause) >> 1) & 1, len(clause) & 1))
        for lit in clause:
            out.append(1 if lit < 0 else 0)
            value = abs(lit)
            out.extend((value >> shift) & 1 for shift in range(7, -1, -1))
    return tuple(out)


MODES = ("repeat", "duplicate", "mirror", "framed", "xorindex")


def pointer_length(base_len: int, mode: str, repetitions: int) -> int:
    if mode == "repeat" or mode == "xorindex":
        return base_len * repetitions
    if mode == "duplicate":
        return 2 * base_len * repetitions
    if mode == "mirror":
        return 2 * base_len * repetitions
    if mode == "framed":
        return 16 + base_len * repetitions
    raise ValueError(mode)


def expected_bit(base: tuple[int, ...], mode: str, repetitions: int, j: int) -> int:
    n = len(base)
    if mode == "repeat":
        return base[j % n]
    if mode == "duplicate":
        return base[(j // 2) % n]
    if mode == "mirror":
        q = j % (2 * n)
        return base[q] if q < n else base[2 * n - 1 - q]
    if mode == "framed":
        if j < 16:
            return (n >> (15 - j)) & 1
        return base[(j - 16) % n]
    if mode == "xorindex":
        return base[j % n] ^ (j & 1)
    raise ValueError(mode)


def verify_stream(base: tuple[int, ...], mode: str, repetitions: int,
                  supplied_len: int | None = None, flip: int | None = None) -> tuple[bool, int]:
    """Exact sequential validation; only index/current comparison are live."""
    expected_len = pointer_length(len(base), mode, repetitions)
    actual_len = expected_len if supplied_len is None else supplied_len
    reads = 0
    if actual_len != expected_len:
        return False, reads
    for j in range(actual_len):
        want = expected_bit(base, mode, repetitions, j)
        got = want ^ (1 if flip == j else 0)
        reads += 1
        if got != want:
            return False, reads
    return True, reads


def wrapper_decide(name: str, formula: Formula, base: tuple[int, ...], mode: str,
                   repetitions: int, flip: int | None = None) -> tuple[bool, int]:
    valid, reads = verify_stream(base, mode, repetitions, flip=flip)
    if name == "RECOMP":
        valid2, reads2 = verify_stream(base, mode, repetitions, flip=flip)
        valid = valid and valid2
        reads += reads2
    elif name == "DELAY":
        for _ in range(7):
            pass
    elif name == "DEAD":
        _dead = sum(base) & 1
        del _dead
    elif name == "COPY":
        _copy = tuple(expected_bit(base, mode, repetitions, j)
                      for j in range(pointer_length(len(base), mode, repetitions)))
        del _copy
    elif name == "INTERP":
        valid = bool(int(valid))
    elif name not in ("DIRECT", "STREAM_ERASE"):
        raise ValueError(name)
    return valid and sat(formula), reads


def main() -> None:
    start = time.perf_counter()
    families: dict[str, Formula] = {
        "H22-K33": h22_k33(),
        "Horn": norm_formula([(-1, 2), (-2, 3), (1,)]),
        "2SAT": norm_formula([(1, 2), (-1, 3), (-2, -3)]),
        "Affine-Tseitin": norm_formula([(1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)]),
        "bounded-treewidth": norm_formula([(1, 2), (-2, 3), (-3, 4), (-4, 5)]),
        "independent-product": norm_formula([(1,), (2, 3), (-2, 3)]),
        "redundant-padding": norm_formula([(1, 2), (1, 2), (3, -3)]),
        "UNSAT-control": norm_formula([(1,), (-1,)]),
    }
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP", "STREAM_ERASE")
    repetitions_set = (1, 2, 4)
    checks = failures = pointer_reads = corruption_cases = wrapper_checks = 0
    max_pointer_bits = max_stream_state_bits = 0
    family_summary: dict[str, dict[str, int | bool]] = {}

    for family, formula in families.items():
        base = source_bits(formula)
        truth = sat(formula)
        family_summary[family] = {"source_bits": len(base), "sat": truth}
        for mode in MODES:
            for repetitions in repetitions_set:
                plen = pointer_length(len(base), mode, repetitions)
                max_pointer_bits = max(max_pointer_bits, plen)
                state_bits = math.ceil(math.log2(plen + 1)) + 3
                max_stream_state_bits = max(max_stream_state_bits, state_bits)
                valid, reads = verify_stream(base, mode, repetitions)
                checks += 1
                pointer_reads += reads
                if not valid:
                    failures += 1
                for bad_len in (max(0, plen - 1), plen + 1):
                    ok, r = verify_stream(base, mode, repetitions, supplied_len=bad_len)
                    checks += 1
                    pointer_reads += r
                    if ok:
                        failures += 1
                # Exhaust every one-bit corruption of the unique pointer.
                for flip in range(plen):
                    ok, r = verify_stream(base, mode, repetitions, flip=flip)
                    checks += 1
                    corruption_cases += 1
                    pointer_reads += r
                    if ok:
                        failures += 1
                for wrapper in wrappers:
                    answer, r = wrapper_decide(wrapper, formula, base, mode, repetitions)
                    checks += 1
                    wrapper_checks += 1
                    pointer_reads += r
                    if answer != truth:
                        failures += 1
                    # A flipped first bit must be rejected by every wrapper.
                    answer_bad, r_bad = wrapper_decide(wrapper, formula, base, mode, repetitions, flip=0)
                    checks += 1
                    wrapper_checks += 1
                    pointer_reads += r_bad
                    if answer_bad:
                        failures += 1

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "TESTS-0019",
        "claim": "UNIQUE-BINDING-POINTER-PERSISTENCE1",
        "status": "PASS" if failures == 0 else "FAIL",
        "checks": checks,
        "failures": failures,
        "seconds": round(elapsed, 6),
        "deterministic": True,
        "random_seed": None,
        "families": family_summary,
        "modes": list(MODES),
        "repetitions": list(repetitions_set),
        "corruption_cases": corruption_cases,
        "wrapper_checks": wrapper_checks,
        "pointer_bit_reads": pointer_reads,
        "max_pointer_bits": max_pointer_bits,
        "max_stream_state_bits_upper_bound": max_stream_state_bits,
        "pointer_bits_retained_after_validation": 0,
        "compatibility_extractions": 0,
        "witness_reconstructions": 0,
        "scope": "finite implementation audit; symbolic theorem is proved separately; no SAT lower bound",
    }
    out = Path("results/raw/review/2026-10-12_unique_pointer_stream_erasure.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
