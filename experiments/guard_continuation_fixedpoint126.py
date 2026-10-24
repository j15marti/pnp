#!/usr/bin/env python3
"""Finite audit for the iterated guarded-continuation fixed point.

The experiment verifies, on exhaustive and seeded controls, that d iterated
guard layers expose every guard word except 1^d without consulting the base
formula, while membership of 1^d is exactly the original SAT bit.  It also
checks that pinning all guards to one gives an ordinary proper 3-CNF whose
size is linear (not a power shrink) for every fixed d.
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


def simplify(formula: Formula, assignment: dict[int, bool]) -> tuple[Formula, bool]:
    out: list[Clause] = []
    for clause in formula:
        kept: list[int] = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                value = assignment[var]
                if value == (lit > 0):
                    satisfied = True
                    break
            else:
                kept.append(lit)
        if satisfied:
            continue
        if not kept:
            return (), False
        # The solver accepts short clauses internally.
        out.append(tuple(kept))  # type: ignore[arg-type]
    return tuple(out), True


def sat(formula: Formula, assignment: dict[int, bool] | None = None) -> bool:
    assignment = {} if assignment is None else dict(assignment)

    def rec(f: tuple[tuple[int, ...], ...], a: dict[int, bool]) -> bool:
        while True:
            f2, ok = simplify(f, a)  # type: ignore[arg-type]
            if not ok:
                return False
            if not f2:
                return True
            unit = next((c[0] for c in f2 if len(c) == 1), None)
            if unit is None:
                f = f2
                break
            v, val = abs(unit), unit > 0
            if v in a and a[v] != val:
                return False
            a[v] = val
            f = f2
        # Occurrence-biased branch, purely for audit speed.
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

    return rec(formula, assignment)


def proper(formula: Formula) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)


def guard_layer(formula: Formula, nvars: int) -> tuple[Formula, int, int]:
    guard = nvars + 1
    clauses: list[Clause] = []
    nxt = guard + 1
    for l1, l2, l3 in formula:
        aux = nxt
        nxt += 1
        clauses.append((-guard, l1, aux))
        clauses.append((-aux, l2, l3))
    return tuple(clauses), nxt - 1, guard


def iterate_guard(formula: Formula, nvars: int, depth: int) -> tuple[Formula, int, tuple[int, ...]]:
    guards: list[int] = []
    for _ in range(depth):
        formula, nvars, g = guard_layer(formula, nvars)
        guards.append(g)
    return formula, nvars, tuple(guards)


def force_true(var: int, a: int, b: int) -> tuple[Clause, ...]:
    return (
        (var, a, b),
        (var, a, -b),
        (var, -a, b),
        (var, -a, -b),
    )


def pin_guards(formula: Formula, nvars: int, guards: tuple[int, ...]) -> tuple[Formula, int]:
    clauses = list(formula)
    nxt = nvars + 1
    for g in guards:
        clauses.extend(force_true(g, nxt, nxt + 1))
        nxt += 2
    return tuple(clauses), nxt - 1


def encoded_bits(nvars: int, nclauses: int) -> int:
    w = math.ceil(math.log2(max(2, 64 * (nvars + nclauses + 1))))
    return (4 * nclauses + 2) * w


def all_sign_clauses() -> tuple[Clause, ...]:
    return tuple(tuple((i + 1) if b else -(i + 1) for i, b in enumerate(bits))
                 for bits in itertools.product((False, True), repeat=3))


def properize_binary(a: int, b: int, z: int) -> tuple[Clause, Clause]:
    return ((a, b, z), (a, b, -z))


def controls() -> list[tuple[str, Formula, int]]:
    p0 = ((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3))
    p1 = ((-1, -2, -3), (-1, 2, 3), (1, -2, 3), (1, 2, -3))
    horn_sat = ((-1, -2, 3), (1, 4, 5), (1, 4, -5), (1, -4, 5), (1, -4, -5))
    horn_unsat = horn_sat + ((-3, 6, 7), (-3, 6, -7), (-3, -6, 7), (-3, -6, -7))
    two_sat: list[Clause] = []
    for j, pair in enumerate(((1, 2), (-1, 2), (1, -2)), start=3):
        two_sat.extend(properize_binary(*pair, j))
    two_unsat = list(two_sat)
    two_unsat.extend(properize_binary(-1, -2, 6))
    return [
        ("affine_sat", p0, 3),
        ("affine_unsat", p0 + p1, 3),
        ("horn_sat", horn_sat, 7),
        ("horn_unsat", horn_unsat, 7),
        ("padded_2sat_sat", tuple(two_sat), 5),
        ("padded_2sat_unsat", tuple(two_unsat), 6),
    ]


def check_case(name: str, base: Formula, nvars: int, max_depth: int,
               counters: dict[str, int], ratios: list[dict[str, float | int | str]]) -> None:
    base_label = sat(base)
    assert proper(base), name
    for d in range(1, max_depth + 1):
        layered, n_layered, guards = iterate_guard(base, nvars, d)
        assert proper(layered)
        assert sat(layered), (name, d, "root")
        counters["root_sat_checks"] += 1
        for word in itertools.product((False, True), repeat=d):
            got = sat(layered, dict(zip(guards, word)))
            expected = (not all(word)) or base_label
            assert got == expected, (name, d, word, got, expected)
            counters["boundary_checks"] += 1
        pinned, n_pinned = pin_guards(layered, n_layered, guards)
        assert proper(pinned)
        assert sat(pinned) == base_label, (name, d, "pinned")
        counters["pinned_checks"] += 1
        if name.startswith("control") or name in {"affine_sat", "affine_unsat"}:
            ratios.append({
                "case": name,
                "depth": d,
                "base_clauses": len(base),
                "layered_clauses": len(layered),
                "pinned_clauses": len(pinned),
                "layered_bits": encoded_bits(n_layered, len(layered)),
                "pinned_bits": encoded_bits(n_pinned, len(pinned)),
                "pinned_over_layered": encoded_bits(n_pinned, len(pinned)) / encoded_bits(n_layered, len(layered)),
            })


def main() -> None:
    counters = {"cases": 0, "root_sat_checks": 0, "boundary_checks": 0, "pinned_checks": 0}
    ratios: list[dict[str, float | int | str]] = []
    signs = all_sign_clauses()
    for mask in range(1, 1 << len(signs)):
        base = tuple(signs[i] for i in range(8) if mask & (1 << i))
        check_case(f"exhaustive_{mask}", base, 3, 4, counters, ratios)
        counters["cases"] += 1

    for name, base, nvars in controls():
        check_case(name, base, nvars, 4, counters, ratios)
        counters["cases"] += 1

    rng = random.Random(126)
    for j in range(64):
        nvars = 5
        universe = [tuple(rng.sample(range(1, nvars + 1), 3)) for _ in range(12)]
        clauses: list[Clause] = []
        for variables in universe[: rng.randint(1, 8)]:
            clauses.append(tuple(v if rng.getrandbits(1) else -v for v in variables))  # type: ignore[arg-type]
        # Remove exact duplicates while preserving order.
        base = tuple(dict.fromkeys(clauses))
        check_case(f"random_{j}", base, nvars, 3, counters, ratios)
        counters["cases"] += 1

    source = Path(__file__).read_bytes()
    summary = {
        "status": "COMPUTATIONAL finite audit; theorem proved separately",
        "seed": 126,
        "counters": counters,
        "total_assertions": sum(v for k, v in counters.items() if k != "cases"),
        "formula_counts": {
            "m_depth_d": "2^d m",
            "n_depth_d": "n+(2^d-1)m+d",
            "pinned_m": "2^d m+4d",
            "pinned_n": "n+(2^d-1)m+3d",
        },
        "representative_ratios": ratios,
        "script_sha256": hashlib.sha256(source).hexdigest(),
    }
    Path("guard_continuation_fixedpoint126_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
