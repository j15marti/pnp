#!/usr/bin/env python3
"""Audit for BOUNDARY-SUPPORT-UNIVERSALITY127.

For a proper 3CNF F and a linear-size comparator C_{d,h}(b)=[int(b)<h],
construct a proper 3CNF whose exact boundary projection is

    Q(b) = C_{d,h}(b) OR SAT(F).

Hence every requested number 0..2^d-1 of SAT-hard boundary points can be
realized while the unpinned parent has a direct b=0 satisfying branch.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from pathlib import Path

Clause = tuple[int, int, int]
Formula = tuple[Clause, ...]


def simplify(formula: tuple[tuple[int, ...], ...], assignment: dict[int, bool]):
    out: list[tuple[int, ...]] = []
    for clause in formula:
        kept: list[int] = []
        for lit in clause:
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    break
            else:
                kept.append(lit)
        else:
            if not kept:
                return (), False
            out.append(tuple(kept))
    return tuple(out), True


def sat(formula: Formula, fixed: dict[int, bool] | None = None) -> bool:
    def rec(f: tuple[tuple[int, ...], ...], a: dict[int, bool]) -> bool:
        while True:
            f, ok = simplify(f, a)
            if not ok:
                return False
            if not f:
                return True
            unit = next((c[0] for c in f if len(c) == 1), None)
            if unit is None:
                break
            v, val = abs(unit), unit > 0
            if v in a and a[v] != val:
                return False
            a[v] = val
        counts: dict[int, int] = {}
        for c in f:
            for lit in c:
                counts[abs(lit)] = counts.get(abs(lit), 0) + 1
        v = max(counts, key=counts.get)
        for val in (True, False):
            b = dict(a)
            b[v] = val
            if rec(f, b):
                return True
        return False

    return rec(formula, {} if fixed is None else dict(fixed))


def brute_label(formula: Formula, nvars: int) -> bool:
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in formula):
            return True
    return False


class ProperBuilder:
    def __init__(self, nvars: int):
        self.nvars = nvars
        self.clauses: list[Clause] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        if len(lits) == 3:
            if len({abs(x) for x in lits}) != 3:
                raise ValueError(f"nonproper ternary {lits}")
            self.clauses.append(tuple(lits))  # type: ignore[arg-type]
        elif len(lits) == 2:
            if abs(lits[0]) == abs(lits[1]):
                raise ValueError(f"repeated binary {lits}")
            z = self.var()
            self.add(lits[0], lits[1], z)
            self.add(lits[0], lits[1], -z)
        elif len(lits) == 1:
            a, b = self.var(), self.var()
            x = lits[0]
            self.add(x, a, b)
            self.add(x, a, -b)
            self.add(x, -a, b)
            self.add(x, -a, -b)
        else:
            raise ValueError("only width 1..3 supported")

    def equiv_and(self, y: int, p: int, q: int) -> None:
        # y <-> (p and q), where p,q may be signed literals.
        self.add(-p, -q, y)
        self.add(p, -y)
        self.add(q, -y)

    def equiv_or(self, y: int, p: int, q: int) -> None:
        # y <-> (p or q).
        self.add(p, q, -y)
        self.add(-p, y)
        self.add(-q, y)


def comparator(builder: ProperBuilder, bits_msb: tuple[int, ...], h: int) -> int:
    """Return an output variable constrained to [unsigned bits < h]."""
    d = len(bits_msb)
    if not (0 <= h <= 1 << d):
        raise ValueError("bad threshold")
    if h == 0:
        out = builder.var()
        builder.add(-out)
        return out
    if h == (1 << d):
        out = builder.var()
        builder.add(out)
        return out
    equal = builder.var()
    less = builder.var()
    builder.add(equal)
    builder.add(-less)
    for pos, bit in enumerate(bits_msb):
        hbit = (h >> (d - 1 - pos)) & 1
        new_equal = builder.var()
        builder.equiv_and(new_equal, equal, bit if hbit else -bit)
        if hbit:
            new_less_term = builder.var()
            builder.equiv_and(new_less_term, equal, -bit)
            new_less = builder.var()
            builder.equiv_or(new_less, less, new_less_term)
            less = new_less
        equal = new_equal
    return less


def construct(base: Formula, nbase: int, d: int, h: int):
    boundary = tuple(range(nbase + 1, nbase + d + 1))
    b = ProperBuilder(nbase + d)
    c = comparator(b, boundary, h)
    comparator_clause_count = len(b.clauses)
    for l1, l2, l3 in base:
        a = b.var()
        b.add(c, l1, a)
        b.add(-a, l2, l3)
    return tuple(b.clauses), b.nvars, boundary, c, comparator_clause_count


def all_sign_clauses() -> tuple[Clause, ...]:
    return tuple(tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(row))
                 for row in itertools.product((False, True), repeat=3))


def properize_binary(a: int, b: int, z: int) -> tuple[Clause, Clause]:
    return ((a, b, z), (a, b, -z))


def hostile_controls() -> list[tuple[str, Formula, int]]:
    parity0 = ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))
    parity1 = ((-1, -2, -3), (-1, 2, 3), (1, -2, 3), (1, 2, -3))
    horn_sat = ((-1, -2, 3), (-2, -3, 4), (-3, -4, 5), (-4, -5, 1))
    dual_horn_sat = tuple(tuple(-x for x in c) for c in horn_sat)
    two_sat: list[Clause] = []
    for j, pair in enumerate(((1, 2), (-1, 2), (1, -2)), start=3):
        two_sat.extend(properize_binary(*pair, j))
    two_unsat = list(two_sat)
    two_unsat.extend(properize_binary(-1, -2, 6))
    independent = parity0 + tuple(tuple((abs(x) + 3) if x > 0 else -(abs(x) + 3) for x in c)
                                  for c in parity0)
    return [
        ("affine_sat", parity0, 3),
        ("affine_unsat", parity0 + parity1, 3),
        ("proper_horn_sat", horn_sat, 5),
        ("proper_dual_horn_sat", dual_horn_sat, 5),
        ("padded_2sat_sat", tuple(two_sat), 5),
        ("padded_2sat_unsat", tuple(two_unsat), 6),
        ("independent_components_sat", independent, 6),
    ]


def encoded_bits(nvars: int, nclauses: int) -> int:
    w = math.ceil(math.log2(max(2, 64 * (nvars + nclauses + 1))))
    return (4 * nclauses + 2) * w


def run_case(name: str, base: Formula, nbase: int, depths: tuple[int, ...],
             stats: dict[str, int], examples: list[dict]) -> None:
    base_label = brute_label(base, nbase)
    stats["base_cases"] += 1
    stats["base_sat"] += int(base_label)
    stats["base_unsat"] += int(not base_label)
    for d in depths:
        hs = sorted({1, 1 << (d - 1), (1 << d) - 1, 1 << d})
        for h in hs:
            formula, nvars, boundary, _, comp_m = construct(base, nbase, d, h)
            assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)
            assert sat(formula), (name, d, h, "root")
            stats["constructed_roots"] += 1
            feasible = 0
            for value in range(1 << d):
                word = tuple(bool((value >> (d - 1 - i)) & 1) for i in range(d))
                got = sat(formula, dict(zip(boundary, word)))
                expected = (value < h) or base_label
                assert got == expected, (name, d, h, value, got, expected)
                feasible += int(got)
                stats["boundary_checks"] += 1
            expected_feasible = (1 << d) if base_label else h
            assert feasible == expected_feasible
            stats["support_count_checks"] += 1
            # The first hard point, if present, is source-equivalent.
            if h < (1 << d):
                hard_word = tuple(bool((h >> (d - 1 - i)) & 1) for i in range(d))
                assert sat(formula, dict(zip(boundary, hard_word))) == base_label
                stats["hard_corner_checks"] += 1
            if len(examples) < 16 and (name in {"allclauses", "single"}):
                examples.append({
                    "case": name,
                    "base_sat": base_label,
                    "d": d,
                    "h": h,
                    "hard_points": (1 << d) - h,
                    "formula_clauses": len(formula),
                    "comparator_clauses": comp_m,
                    "formula_variables": nvars,
                    "encoded_bits": encoded_bits(nvars, len(formula)),
                })


def main() -> None:
    stats = {k: 0 for k in (
        "base_cases", "base_sat", "base_unsat", "constructed_roots",
        "boundary_checks", "support_count_checks", "hard_corner_checks")}
    examples: list[dict] = []
    signs = all_sign_clauses()
    for mask in range(1, 1 << 8):
        base = tuple(signs[i] for i in range(8) if mask & (1 << i))
        name = "allclauses" if mask == 255 else ("single" if mask & (mask - 1) == 0 else f"mask{mask}")
        run_case(name, base, 3, (1, 2, 3, 4), stats, examples)

    for name, base, nbase in hostile_controls():
        run_case(name, base, nbase, (2, 4), stats, examples)

    rng = random.Random(127)
    for j in range(64):
        clauses: list[Clause] = []
        for _ in range(rng.randint(1, 8)):
            vs = rng.sample(range(1, 6), 3)
            clauses.append(tuple(v if rng.getrandbits(1) else -v for v in vs))  # type: ignore[arg-type]
        run_case(f"random{j}", tuple(dict.fromkeys(clauses)), 5, (3, 5), stats, examples)

    source = Path(__file__).read_bytes()
    result = {
        "status": "COMPUTATIONAL finite audit; theorem proved separately",
        "seed": 127,
        "stats": stats,
        "assertion_accounted_checks": sum(stats.values()),
        "identity": "Q_F,d,h(b) = [unsigned(b) < h] OR SAT(F)",
        "hard_boundary_count": "2^d-h, arbitrarily selectable from 0 through 2^d-1",
        "parent": "always SAT for h>=1 via boundary word 0",
        "size": "n+m+O(d) variables and 2m+O(d) proper ternary clauses",
        "examples": examples,
        "script_sha256": hashlib.sha256(source).hexdigest(),
    }
    Path("boundary_support_universality127_summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
