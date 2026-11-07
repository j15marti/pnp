#!/usr/bin/env python3
"""Exact one-split Polynomial Calculus guard-lifting compiler.

Independent finite control for the symbolic lemma in REFEREE402.  This is not
an execution of the historical R_mix341 checker or any authoritative PC tool.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import resource
import time
import tracemalloc
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Fraction]


def norm(p: Polynomial) -> Polynomial:
    return {tuple(sorted(m)): c for m, c in p.items() if c}


def add(a: Polynomial, b: Polynomial, alpha=1, beta=1) -> Polynomial:
    out: Polynomial = {}
    for m, c in a.items():
        out[m] = out.get(m, Fraction()) + Fraction(alpha) * c
    for m, c in b.items():
        out[m] = out.get(m, Fraction()) + Fraction(beta) * c
    return norm(out)


def mul_var(p: Polynomial, var: str) -> Polynomial:
    out: Polynomial = {}
    for m, c in p.items():
        mm = tuple(sorted(m + (var,)))
        out[mm] = out.get(mm, Fraction()) + c
    return norm(out)


def const(c: int) -> Polynomial:
    return {(): Fraction(c)} if c else {}


def variable(v: str) -> Polynomial:
    return {(v,): Fraction(1)}


def one_minus(v: str) -> Polynomial:
    return add(const(1), variable(v), 1, -1)


def product(a: Polynomial, b: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(sorted(ma + mb))
            out[m] = out.get(m, Fraction()) + ca * cb
    return norm(out)


def degree(p: Polynomial) -> int:
    return max((len(m) for m in p), default=-1)


def serial(p: Polynomial) -> list[list[object]]:
    return [[list(m), int(c.numerator), int(c.denominator)] for m, c in sorted(p.items())]


def pkey(p: Polynomial) -> str:
    return json.dumps(serial(p), separators=(",", ":"))


@dataclass
class Line:
    ident: int
    kind: str
    poly: Polynomial
    parents: tuple[int, ...] = ()
    alpha: Fraction = Fraction(1)
    beta: Fraction = Fraction(1)
    var: str | None = None
    name: str | None = None


def boolean_axiom(v: str) -> Polynomial:
    return add(mul_var(variable(v), v), variable(v), 1, -1)


def verify(lines: list[Line], sources: dict[str, Polynomial], assumptions: dict[str, Polynomial]) -> dict:
    seen: dict[int, Polynomial] = {}
    inference_nodes = 0
    source_reads = 0
    for line in lines:
        if line.ident in seen:
            raise AssertionError("duplicate line id")
        if any(parent not in seen for parent in line.parents):
            raise AssertionError("forward or missing parent")
        if line.kind == "source":
            assert line.name in sources and line.poly == sources[line.name]
            source_reads += 1
        elif line.kind == "bool":
            assert line.var and line.poly == boolean_axiom(line.var)
            source_reads += 1
        elif line.kind == "assumption":
            assert line.name in assumptions and line.poly == assumptions[line.name]
            source_reads += 1
        elif line.kind == "lin":
            assert len(line.parents) == 2
            expected = add(seen[line.parents[0]], seen[line.parents[1]], line.alpha, line.beta)
            assert line.poly == expected
            inference_nodes += 1
        elif line.kind == "mul":
            assert len(line.parents) == 1 and line.var
            assert line.poly == mul_var(seen[line.parents[0]], line.var)
            inference_nodes += 1
        else:
            raise AssertionError(f"unknown kind {line.kind}")
        seen[line.ident] = line.poly
    assert lines and lines[-1].poly == const(1)
    return {
        "lines": len(lines),
        "inference_nodes": inference_nodes,
        "source_reads": source_reads,
        "monomial_occurrences": sum(len(x.poly) for x in lines),
        "maximum_degree": max(degree(x.poly) for x in lines),
    }


def branch_proofs(start: int) -> tuple[dict[str, Polynomial], list[Line], list[Line]]:
    x, y = variable("x"), variable("y")
    nx, ny = one_minus("x"), one_minus("y")
    sources = {
        "C_xy": product(nx, ny),
        "C_xny": product(nx, y),
        "C_nxy": product(x, ny),
        "C_nxny": product(x, y),
    }
    # x=0 branch: C_xy + C_xny = 1-x; then add assumption x=0.
    a = start
    left = [
        Line(a, "source", sources["C_xy"], name="C_xy"),
        Line(a + 1, "source", sources["C_xny"], name="C_xny"),
        Line(a + 2, "lin", add(sources["C_xy"], sources["C_xny"]), (a, a + 1)),
        Line(a + 3, "assumption", x, name="x_zero"),
        Line(a + 4, "lin", const(1), (a + 2, a + 3)),
    ]
    # x=1 branch: C_nxy + C_nxny = x; then add assumption 1-x=0.
    b = start + 100
    right = [
        Line(b, "source", sources["C_nxy"], name="C_nxy"),
        Line(b + 1, "source", sources["C_nxny"], name="C_nxny"),
        Line(b + 2, "lin", add(sources["C_nxy"], sources["C_nxny"]), (b, b + 1)),
        Line(b + 3, "assumption", nx, name="x_one"),
        Line(b + 4, "lin", const(1), (b + 2, b + 3)),
    ]
    return sources, left, right


def guard_lift(
    branch: list[Line], sources: dict[str, Polynomial], assumption_name: str,
    guard: Polynomial, guard_kind: str, start: int
) -> tuple[list[Line], int]:
    """Derive guard from sources by lifting every branch line."""
    out: list[Line] = []
    mapped: dict[int, int] = {}
    source_ids: dict[tuple[str, str], int] = {}
    next_id = start

    def emit(line: Line) -> int:
        nonlocal next_id
        out.append(line)
        next_id = max(next_id, line.ident + 1)
        return line.ident

    def available_source(line: Line) -> int:
        key = (line.kind, line.name or line.var or "")
        if key in source_ids:
            return source_ids[key]
        ident = next_id
        emit(Line(ident, line.kind, line.poly, var=line.var, name=line.name))
        source_ids[key] = ident
        return ident

    bool_x = None
    for line in branch:
        if line.kind in {"source", "bool"}:
            base = available_source(line)
            if guard_kind == "x":
                ident = next_id
                emit(Line(ident, "mul", mul_var(line.poly, "x"), (base,), var="x"))
                mapped[line.ident] = ident
            else:
                xp = next_id
                emit(Line(xp, "mul", mul_var(line.poly, "x"), (base,), var="x"))
                gp = next_id
                emit(Line(gp, "lin", add(line.poly, mul_var(line.poly, "x"), 1, -1), (base, xp), Fraction(1), Fraction(-1)))
                mapped[line.ident] = gp
        elif line.kind == "assumption":
            assert line.name == assumption_name
            if bool_x is None:
                bool_x = next_id
                emit(Line(bool_x, "bool", boolean_axiom("x"), var="x"))
            ident = next_id
            target = add({}, boolean_axiom("x"), 0, -1)
            emit(Line(ident, "lin", target, (bool_x, bool_x), Fraction(-1), Fraction(0)))
            assert target == product(guard, line.poly)
            mapped[line.ident] = ident
        elif line.kind == "lin":
            ident = next_id
            expected = add(out_by_id(out, mapped[line.parents[0]]), out_by_id(out, mapped[line.parents[1]]), line.alpha, line.beta)
            emit(Line(ident, "lin", expected, (mapped[line.parents[0]], mapped[line.parents[1]]), line.alpha, line.beta))
            assert expected == product(guard, line.poly)
            mapped[line.ident] = ident
        elif line.kind == "mul":
            ident = next_id
            expected = mul_var(out_by_id(out, mapped[line.parents[0]]), line.var or "")
            emit(Line(ident, "mul", expected, (mapped[line.parents[0]],), var=line.var))
            assert expected == product(guard, line.poly)
            mapped[line.ident] = ident
        else:
            raise AssertionError("branch line kind")
    final = mapped[branch[-1].ident]
    assert out_by_id(out, final) == guard
    return out, final


def out_by_id(lines: list[Line], ident: int) -> Polynomial:
    for line in reversed(lines):
        if line.ident == ident:
            return line.poly
    raise KeyError(ident)


def compile_case_split() -> tuple[list[Line], dict]:
    start = 2**31 + 17
    sources, left, right = branch_proofs(start)
    assumptions = {"x_zero": variable("x"), "x_one": one_minus("x")}
    left_stats = verify(left, sources, {"x_zero": assumptions["x_zero"]})
    right_stats = verify(right, sources, {"x_one": assumptions["x_one"]})
    left_lift, left_final = guard_lift(left, sources, "x_zero", one_minus("x"), "one_minus_x", 2**40 + 1)
    right_lift, right_final = guard_lift(right, sources, "x_one", variable("x"), "x", 2**41 + 1)
    combined = left_lift + right_lift
    join_id = 2**42 + 1
    combined.append(Line(join_id, "lin", const(1), (left_final, right_final)))
    compiled_stats = verify(combined, sources, {})
    assert not any(line.kind == "assumption" for line in combined)
    assert out_by_id(combined, left_final) == one_minus("x")
    assert out_by_id(combined, right_final) == variable("x")
    meta = {
        "left_branch": left_stats,
        "right_branch": right_stats,
        "compiled": compiled_stats,
        "left_guard": serial(out_by_id(combined, left_final)),
        "right_guard": serial(out_by_id(combined, right_final)),
        "source_sha256": hashlib.sha256("\n".join(f"{k}:{pkey(v)}" for k, v in sorted(sources.items())).encode()).hexdigest(),
    }
    return combined, meta


def corruption_controls(compiled: list[Line], sources: dict[str, Polynomial]) -> dict[str, bool]:
    controls: dict[str, bool] = {}

    def rejects(lines: list[Line]) -> bool:
        try:
            verify(lines, sources, {})
            return False
        except (AssertionError, KeyError):
            return True

    missing_join = compiled[:-1]
    controls["omitted_and_branch_join"] = rejects(missing_join)
    bad_parent = [Line(**vars(x)) for x in compiled]
    bad_parent[-1].parents = (bad_parent[-1].parents[0], 999999999999999)
    controls["missing_parent"] = rejects(bad_parent)
    bad_orientation = [Line(**vars(x)) for x in compiled]
    bad_orientation[-1].alpha = Fraction(-1)
    controls["wrong_linear_orientation"] = rejects(bad_orientation)
    leaked = [Line(**vars(x)) for x in compiled]
    leaked[-1].kind = "assumption"
    leaked[-1].name = "x_zero"
    leaked[-1].parents = ()
    controls["assumption_leak"] = rejects(leaked)
    duplicate = [Line(**vars(x)) for x in compiled]
    duplicate[-1].ident = duplicate[-2].ident
    controls["duplicate_large_id"] = rejects(duplicate)
    assert all(controls.values())
    return controls


def pcr_tree_controls(max_depth: int = 8) -> list[dict]:
    """Check the explicit-leaf guard partition used by the PCR corollary."""
    rows = []
    for depth in range(1, max_depth + 1):
        leaves = list(itertools.product((0, 1), repeat=depth))
        evaluations = 0
        for assignment in itertools.product((0, 1), repeat=depth):
            # Each leaf guard is one PCR monomial: choose x_i or bar(x_i).
            values = [int(all(a == bit for a, bit in zip(assignment, leaf))) for leaf in leaves]
            assert sum(values) == 1
            evaluations += len(values)
        omitted = leaves[:-1]
        missing_witness = leaves[-1]
        assert sum(int(all(a == bit for a, bit in zip(missing_witness, leaf))) for leaf in omitted) == 0
        rows.append({
            "depth": depth,
            "leaves": 2**depth,
            "pcr_guard_monomials_per_leaf": 1,
            "pc_worst_expanded_guard_monomials": 2**depth,
            "guard_evaluations": evaluations,
            "omitted_leaf_witness_rejected": True,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    tracemalloc.start()
    compiled, meta = compile_case_split()
    sources, _, _ = branch_proofs(2**31 + 17)
    corruptions = corruption_controls(compiled, sources)
    pcr_rows = pcr_tree_controls()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result = {
        "status": "PASS",
        "scope": "one explicit Boolean split in native PC; not historical R_mix341",
        "theorem_control": {
            "length_bound": "at most 3*(L0+L1)+1 lines under the safe compiler",
            "size_bound": "at most 4*(S0+S1)+2 monomial occurrences under the safe compiler",
            "degree_bound": "max(d0,d1)+1",
            "sharing_scope": "polynomial in explicit context-labelled branch traces; no free incompatible-context reuse",
        },
        "example": meta,
        "compiled_trace": [
            {
                "id": x.ident, "kind": x.kind, "poly": serial(x.poly), "parents": list(x.parents),
                "alpha": [x.alpha.numerator, x.alpha.denominator],
                "beta": [x.beta.numerator, x.beta.denominator], "var": x.var, "name": x.name,
            }
            for x in compiled
        ],
        "corruptions_rejected": corruptions,
        "pcr_tree_controls": pcr_rows,
        "elapsed_seconds": time.perf_counter() - started,
        "python_tracemalloc_current_bytes": current,
        "python_tracemalloc_peak_bytes": peak,
        "process_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "disclaimer": "independent implementation, not an authoritative checker execution",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
