#!/usr/bin/env python3
"""Exact SAT interfaces: affine equations plus a table on linear coordinates.

Dependency-free research prototype, Python 3.10+.  No SAT oracle is used.
All vector spaces are over GF(2); a vector is a nonnegative integer bit mask.
The optional width cap returns an exception, never a SAT/UNSAT conclusion.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


def dot(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def indices(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def rref(equations: Iterable[tuple[int, int]]):
    """Canonical reduced row echelon form; None denotes inconsistency."""
    rows: dict[int, tuple[int, int]] = {}
    for mask, rhs in equations:
        if mask < 0 or rhs not in (0, 1):
            raise ValueError("Invalid GF(2) row")
        for p in sorted(rows):
            if (mask >> p) & 1:
                m, b = rows[p]
                mask ^= m
                rhs ^= b
        if not mask:
            if rhs:
                return None
            continue
        p = (mask & -mask).bit_length() - 1
        for j, (m, b) in list(rows.items()):
            if (m >> p) & 1:
                rows[j] = (m ^ mask, b ^ rhs)
        rows[p] = (mask, rhs)
    return tuple(rows[p] for p in sorted(rows))


def basis(vectors: Iterable[int]) -> tuple[int, ...]:
    return tuple(m for m, _ in rref((v, 0) for v in vectors))


def nullspace(rows: Iterable[int], n: int) -> tuple[int, ...]:
    rr = basis(rows)
    pivots = {(m & -m).bit_length() - 1 for m in rr}
    out = []
    for j in range(n):
        if j in pivots:
            continue
        v = 1 << j
        for m in rr:
            p = (m & -m).bit_length() - 1
            if (m >> j) & 1:
                v |= 1 << p
        out.append(v)
    return tuple(out)


def linear_combination(rows: tuple[int, ...], coefficients: int) -> int:
    out = 0
    for i in indices(coefficients):
        out ^= rows[i]
    return out


def coordinates(vector: int, row_basis: tuple[int, ...]) -> int:
    out = 0
    for i, m in enumerate(row_basis):
        p = (m & -m).bit_length() - 1
        if (vector >> p) & 1:
            vector ^= m
            out |= 1 << i
    if vector:
        raise ValueError("Vector is outside the declared span")
    return out


class WidthLimit(RuntimeError):
    """The exact construction needs a table exceeding the supplied budget."""


@dataclass
class Work:
    cap: int = 20
    table_evaluations: int = 0
    fourier_butterflies: int = 0
    max_width: int = 0
    joins: int = 0
    projections: int = 0
    normalizations: int = 0
    trace: list[dict] = field(default_factory=list)

    def charge_table(self, k: int):
        self.max_width = max(self.max_width, k)
        if k > self.cap:
            raise WidthLimit(f"Required table width {k} exceeds cap {self.cap}")
        self.table_evaluations += 1 << k


@dataclass(frozen=True)
class Interface:
    n: int
    equations: tuple[tuple[int, int], ...]
    forms: tuple[int, ...]
    table: tuple[bool, ...]

    @property
    def width(self) -> int:
        return len(self.forms)

    @property
    def support_mask(self) -> int:
        mask = 0
        for m, _ in self.equations:
            mask |= m
        for m in self.forms:
            mask |= m
        return mask

    def accepts(self, assignment: int) -> bool:
        if any(dot(m, assignment) != b for m, b in self.equations):
            return False
        z = sum(dot(m, assignment) << i for i, m in enumerate(self.forms))
        return self.table[z]


def false_interface(n: int) -> Interface:
    return Interface(n, ((0, 1),), (), (True,))


def true_interface(n: int) -> Interface:
    return Interface(n, (), (), (True,))


def canonical(n: int, equations, forms_with_shift,
              predicate: Callable[[int], bool], work: Work) -> Interface:
    """Reduce linear coordinates modulo the core BEFORE table enumeration."""
    rr = rref(equations)
    if rr is None:
        return false_interface(n)
    reduced = []
    for mask, shift in forms_with_shift:
        if mask >> n:
            raise ValueError("Form uses an undeclared variable")
        for m, b in rr:
            p = (m & -m).bit_length() - 1
            if (mask >> p) & 1:
                mask ^= m
                shift ^= b
        reduced.append((mask, shift))
    bb = basis(m for m, _ in reduced)
    coeffs = [(coordinates(m, bb), c) for m, c in reduced]
    work.charge_table(len(bb))
    table = []
    for z in range(1 << len(bb)):
        old = sum((dot(a, z) ^ c) << i for i, (a, c) in enumerate(coeffs))
        table.append(bool(predicate(old)))
    return Interface(n, rr, bb, tuple(table))


def normalize(rel: Interface, work: Work) -> Interface:
    """Exact affine hull extraction and translation-period quotient.

    For nonempty R the output width is dim(aff R)-dim(Stab R), the
    minimum possible width within this direct affine-core/table format.
    Enumeration is over the existing table, never over all boundary values.
    """
    work.normalizations += 1
    rel = canonical(rel.n, rel.equations, [(m, 0) for m in rel.forms],
                    rel.table.__getitem__, work)
    if rel.equations == ((0, 1),):
        return rel
    accepted = [z for z, b in enumerate(rel.table) if b]
    if not accepted:
        return false_interface(rel.n)
    k = rel.width
    origin = accepted[0]
    hull_eq = nullspace((z ^ origin for z in accepted), k)
    extra = [(linear_combination(rel.forms, h), dot(h, origin)) for h in hull_eq]
    if extra:
        rel = canonical(rel.n, (*rel.equations, *extra),
                        [(m, 0) for m in rel.forms], rel.table.__getitem__, work)
    k = rel.width
    if all(rel.table):
        return Interface(rel.n, rel.equations, (), (True,))
    # Exact unnormalized Walsh transform.  Translation periods are the
    # orthogonal complement of the span of nonzero Fourier frequencies.
    # Integer coefficients have at most k+2 signed bits; no rounding occurs.
    spectrum = [int(v) for v in rel.table]
    step = 1
    while step < len(spectrum):
        for start in range(0, len(spectrum), 2 * step):
            for j in range(start, start + step):
                a, b = spectrum[j], spectrum[j + step]
                spectrum[j], spectrum[j + step] = a + b, a - b
                work.fourier_butterflies += 1
        step *= 2
    quotient = basis(i for i, coefficient in enumerate(spectrum) if coefficient)
    if len(quotient) == k:
        return rel
    work.charge_table(len(quotient))
    result = [None] * (1 << len(quotient))
    for z, val in enumerate(rel.table):
        q = sum(dot(h, z) << i for i, h in enumerate(quotient))
        if result[q] is not None and result[q] != val:
            raise AssertionError("Invalid translation quotient")
        result[q] = val
    return Interface(rel.n, rel.equations,
                     tuple(linear_combination(rel.forms, h) for h in quotient),
                     tuple(bool(v) for v in result))


def join(left: Interface, right: Interface, work: Work) -> Interface:
    if left.n != right.n:
        raise ValueError("Ambient variable namespaces differ")
    work.joins += 1
    split = left.width
    lowmask = (1 << split) - 1
    rel = canonical(left.n, (*left.equations, *right.equations),
                    [(m, 0) for m in (*left.forms, *right.forms)],
                    lambda z: left.table[z & lowmask] and right.table[z >> split],
                    work)
    return normalize(rel, work)


def eliminate_equations(equations, variables: Iterable[int]):
    """Existentially eliminate selected columns of an affine system."""
    rows = list(equations)
    for v in variables:
        idx = next((i for i, (m, _) in enumerate(rows) if (m >> v) & 1), None)
        if idx is None:
            continue
        pm, pb = rows.pop(idx)
        rows = [(m ^ pm, b ^ pb) if (m >> v) & 1 else (m, b)
                for m, b in rows]
    return rows


def project(rel: Interface, private: Iterable[int], work: Work) -> Interface:
    """Return exists(private) rel, in the same representation class."""
    private = tuple(sorted(set(private)))
    if any(x < 0 or x >= rel.n for x in private):
        raise ValueError("Invalid private-variable index")
    work.projections += 1
    n, k = rel.n, rel.width
    rows = [*rel.equations,
            *((m | (1 << (n + i)), 0) for i, m in enumerate(rel.forms))]
    rows = eliminate_equations(rows, private)
    # Row operations on the y block split consistency constraints on s
    # from the full-row-rank map D1 y = e1 + C1 s.
    pivot_rows = []
    for i in range(k):
        idx = next((j for j, (m, _) in enumerate(rows)
                    if (m >> (n + i)) & 1), None)
        if idx is None:
            continue
        pm, pb = rows.pop(idx)
        rows = [(m ^ pm, b ^ pb) if (m >> (n + i)) & 1 else (m, b)
                for m, b in rows]
        pivot_rows.append((pm, pb))
    if any(m >> n for m, _ in rows):
        raise AssertionError("Uneliminated table coordinate")
    r = len(pivot_rows)
    work.charge_table(r)
    image = [False] * (1 << r)
    for y, accepted in enumerate(rel.table):
        if accepted:
            z = sum(dot(m >> n, y) << i for i, (m, _) in enumerate(pivot_rows))
            image[z] = True
    variable_mask = (1 << n) - 1
    out = canonical(n, rows,
                    [(m & variable_mask, b) for m, b in pivot_rows],
                    image.__getitem__, work)
    out = normalize(out, work)
    if out.support_mask & sum(1 << v for v in private):
        raise AssertionError("Projection retained a private variable")
    return out


def clause_interface(n: int, clauses: Iterable[tuple[int, ...]], work: Work) -> Interface:
    clauses = tuple(clauses)
    scope = sorted({abs(v) - 1 for c in clauses for v in c})
    if any(v < 0 or v >= n for v in scope):
        raise ValueError("Invalid literal")
    loc = {v: i for i, v in enumerate(scope)}
    def pred(z):
        return all(any(bool((z >> loc[abs(lit) - 1]) & 1) == (lit > 0)
                       for lit in clause) for clause in clauses)
    rel = canonical(n, (), [(1 << v, 0) for v in scope], pred, work)
    return normalize(rel, work)


def compile_cnf(n: int, clauses: Iterable[tuple[int, ...]], cap: int = 20):
    """Exact factor elimination with a deterministic scope-size heuristic.

    Identical-scope clauses are grouped first, which recognizes local XOR
    packets without semantic guessing.  WidthLimit is reported as unresolved.
    This is NOT claimed to be polynomial on arbitrary CNFs.
    """
    work = Work(cap=cap)
    if n < 0:
        raise ValueError("Negative variable count")
    clauses = tuple(tuple(c) for c in clauses)
    if any(lit == 0 or abs(lit) > n for c in clauses for lit in c):
        raise ValueError("Invalid CNF literal")
    # Sparse binary variable identifiers must not turn a short input into
    # exponentially long integer bit masks.  Relabel only occurring variables.
    original_ids = sorted({abs(lit) for c in clauses for lit in c})
    relabel = {v: i + 1 for i, v in enumerate(original_ids)}
    clauses = tuple(tuple(relabel[abs(lit)] if lit > 0 else -relabel[abs(lit)]
                          for lit in c) for c in clauses)
    n = len(original_ids)
    groups = {}
    for c in clauses:
        key = tuple(sorted({abs(v) for v in c}))
        groups.setdefault(key, []).append(c)
    try:
        factors = [clause_interface(n, cs, work) for _, cs in sorted(groups.items())]
        while any(f.support_mask for f in factors):
            if any(f.equations == ((0, 1),) for f in factors):
                return False, work
            active = sorted({v for f in factors for v in indices(f.support_mask)})
            def score(v):
                masks = [f.support_mask for f in factors if (f.support_mask >> v) & 1]
                combined = 0
                for m in masks:
                    combined |= m
                return combined.bit_count(), v
            v = min(active, key=score)
            bucket = [f for f in factors if (f.support_mask >> v) & 1]
            factors = [f for f in factors if not ((f.support_mask >> v) & 1)]
            bucket.sort(key=lambda f: (f.width, f.support_mask))
            acc = bucket[0]
            for f in bucket[1:]:
                acc = join(acc, f, work)
            before = acc.width
            acc = project(acc, [v], work)
            work.trace.append({"variable": original_ids[v], "bucket_factors": len(bucket),
                               "joined_width": before, "projected_width": acc.width})
            factors.append(acc)
        return all(f.accepts(0) for f in factors), work
    except WidthLimit as exc:
        work.trace.append({"unresolved": str(exc)})
        return None, work


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", help="DIMACS CNF path")
    parser.add_argument("--cap", type=int, default=20,
                        help="Maximum explicit table dimension; overflow is UNRESOLVED")
    args = parser.parse_args()
    n = None
    tokens = []
    expected = None
    with open(args.cnf, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                _, kind, ns, ms = line.split()
                if kind != "cnf" or n is not None:
                    raise ValueError("Expected one DIMACS CNF header")
                n, expected = int(ns), int(ms)
            else:
                tokens.extend(int(t) for t in line.split())
    if n is None:
        raise ValueError("Missing DIMACS header")
    clauses, current = [], []
    for lit in tokens:
        if lit:
            current.append(lit)
        else:
            clauses.append(tuple(current))
            current = []
    if current or len(clauses) != expected:
        raise ValueError("Malformed DIMACS clause list")
    result, work = compile_cnf(n, clauses, args.cap)
    print(json.dumps({"result": {True: "SAT", False: "UNSAT", None: "UNRESOLVED"}[result],
                      "work": vars(work)}, indent=2))
