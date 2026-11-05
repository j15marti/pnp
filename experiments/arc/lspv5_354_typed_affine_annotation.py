#!/usr/bin/env python3
"""REFEREE354: typed GF(2)-annotation survival audit for native R_mix341.

This is a deliberately small checker for an unambiguous native fragment:
strict DIMACS sources, exact AND3 factors, optional certified affine annotations,
and XOR addition of two such annotations.  It tests that preserving the exact
Boolean factor while erasing its GF(2) certificate is not a type-preserving
normalization when a later XOR consumes that certificate.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from typing import Iterable


class Reject(ValueError):
    pass


Val = tuple[int, ...]


def parse_dimacs(text: str) -> tuple[int, list[tuple[int, ...]]]:
    lines = [line.strip() for line in text.splitlines()
             if line.strip() and not line.lstrip().startswith("c")]
    if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
        raise Reject("bad-header")
    try:
        n, m = map(int, lines[0].split()[2:])
    except ValueError as exc:
        raise Reject("bad-header-int") from exc
    if n < 0 or m < 0:
        raise Reject("negative-header")
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        try:
            row = tuple(map(int, line.split()))
        except ValueError as exc:
            raise Reject("bad-literal") from exc
        if not row or row[-1] != 0 or 0 in row[:-1]:
            raise Reject("bad-terminator")
        clause = row[:-1]
        if any(abs(lit) < 1 or abs(lit) > n for lit in clause):
            raise Reject("literal-out-of-range")
        clauses.append(clause)
    if len(clauses) != m:
        raise Reject("clause-count")
    return n, clauses


def vals(n: int) -> list[Val]:
    return list(itertools.product((0, 1), repeat=n))


def clause_value(clause: Iterable[int], v: Val) -> int:
    return int(any(v[abs(lit) - 1] == int(lit > 0) for lit in clause))


def source_models(n: int, clauses: list[tuple[int, ...]]) -> list[Val]:
    return [v for v in vals(n) if all(clause_value(c, v) for c in clauses)]


def table_of_clause(clause: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(clause_value(clause, v) for v in vals(n))


def and_table(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    if len(a) != len(b):
        raise Reject("table-length")
    return tuple(x & y for x, y in zip(a, b))


@dataclass(frozen=True)
class Affine:
    mask: int
    rhs: int

    def holds(self, v: Val) -> bool:
        parity = 0
        for i, bit in enumerate(v):
            if (self.mask >> i) & 1:
                parity ^= bit
        return parity == self.rhs

    def table(self, n: int) -> tuple[int, ...]:
        return tuple(int(self.holds(v)) for v in vals(n))

    def add(self, other: "Affine") -> "Affine":
        return Affine(self.mask ^ other.mask, self.rhs ^ other.rhs)


@dataclass(frozen=True)
class Factor:
    table: tuple[int, ...]
    affine: Affine | None


def exact_annotation(factor: Factor, n: int) -> bool:
    return factor.affine is not None and factor.table == factor.affine.table(n)


def typed_xor(left: Factor, right: Factor, n: int) -> Affine:
    if not exact_annotation(left, n):
        raise Reject("left-parent-lacks-exact-gf2-annotation")
    if not exact_annotation(right, n):
        raise Reject("right-parent-lacks-exact-gf2-annotation")
    assert left.affine is not None and right.affine is not None
    return left.affine.add(right.affine)


SOURCE = "p cnf 2 3\n1 0\n2 0\n1 2 0\n"
SOURCE_UNSAT = "p cnf 1 2\n1 0\n-1 0\n"


def witness() -> dict[str, object]:
    n, clauses = parse_dimacs(SOURCE)
    tables = [table_of_clause(c, n) for c in clauses]
    fx = Factor(and_table(tables[0], tables[2]), Affine(0b01, 1))
    fy = Factor(and_table(tables[1], tables[2]), Affine(0b10, 1))
    result = typed_xor(fx, fy, n)
    erased = Factor(fx.table, None)
    erased_rejection = ""
    try:
        typed_xor(erased, fy, n)
    except Reject as exc:
        erased_rejection = str(exc)
    else:
        raise AssertionError("type-erased XOR was accepted")
    return {
        "source_models": source_models(n, clauses),
        "node1_and3_table": fx.table,
        "node1_annotation": {"mask": fx.affine.mask, "rhs": fx.affine.rhs},
        "node2_and3_table": fy.table,
        "node2_annotation": {"mask": fy.affine.mask, "rhs": fy.affine.rhs},
        "node3_xor": {"mask": result.mask, "rhs": result.rhs},
        "erased_table_equal": erased.table == fx.table,
        "erased_rejection": erased_rejection,
    }


def run() -> dict[str, object]:
    checks = 0

    # Both-label and malformed-source controls.
    n, clauses = parse_dimacs(SOURCE)
    models = source_models(n, clauses)
    checks += 2
    assert models == [(1, 1)]
    nu, cu = parse_dimacs(SOURCE_UNSAT)
    checks += 2
    assert source_models(nu, cu) == []
    malformed = [
        "", "p cnd 2 0\n", "p cnf 2 1\n1 3 0\n",
        "p cnf 2 1\n1 2\n", "p cnf 2 2\n1 0\n",
    ]
    for text in malformed:
        try:
            parse_dimacs(text)
        except Reject:
            pass
        else:
            raise AssertionError(("malformed accepted", text))
        checks += 1

    w = witness()
    checks += 9
    assert w["source_models"] == [(1, 1)]
    assert w["node1_and3_table"] == (0, 0, 1, 1)
    assert w["node2_and3_table"] == (0, 1, 0, 1)
    assert w["node3_xor"] == {"mask": 0b11, "rhs": 0}
    assert w["erased_table_equal"] is True
    assert w["erased_rejection"] == "left-parent-lacks-exact-gf2-annotation"

    # Exhaustively characterize every Boolean factor over two variables and
    # every possible affine annotation.  Exactly 8 of 16 factors are affine,
    # each with one exact row among the 8 candidate mask/rhs pairs.
    affine_factor_count = 0
    exact_pairs: list[tuple[int, int, int]] = []
    for bits in itertools.product((0, 1), repeat=4):
        exact_here = 0
        for mask in range(4):
            for rhs in (0, 1):
                exact = bits == Affine(mask, rhs).table(2)
                checks += 1
                if exact:
                    exact_here += 1
                    exact_pairs.append((sum(bit << i for i, bit in enumerate(bits)), mask, rhs))
        checks += 1
        assert exact_here in (0, 1)
        affine_factor_count += exact_here
    checks += 1
    assert affine_factor_count == 8

    # Every pair of exact rows adds pointwise over GF(2).  This independently
    # validates the XOR rule used by the witness.
    rows = [Affine(mask, rhs) for mask in range(4) for rhs in (0, 1)]
    for a in rows:
        for b in rows:
            c = a.add(b)
            for v in vals(2):
                lhs = int(a.holds(v)) ^ int(b.holds(v))
                # Equation truth values are equal iff both rows have the same
                # residual parity; their sum equation must then be true.
                residual_a = int(not a.holds(v))
                residual_b = int(not b.holds(v))
                sum_holds = int(c.holds(v))
                checks += 2
                assert sum_holds == int(residual_a == residual_b)
                assert lhs == (1 ^ sum_holds)

    # Mutation controls against semantic and typing forgery.
    tx = Factor((0, 0, 1, 1), Affine(0b01, 1))
    ty = Factor((0, 1, 0, 1), Affine(0b10, 1))
    bad_factors = [
        Factor((0, 0, 1, 0), Affine(0b01, 1)),  # corrupted exact factor
        Factor(tx.table, Affine(0b01, 0)),       # wrong rhs
        Factor(tx.table, Affine(0b10, 1)),       # wrong mask
        Factor(tx.table, None),                  # erased type
    ]
    for bad in bad_factors:
        checks += 1
        assert not exact_annotation(bad, 2)
        try:
            typed_xor(bad, ty, 2)
        except Reject:
            pass
        else:
            raise AssertionError(("forged parent accepted", bad))
        checks += 1

    good = typed_xor(tx, ty, 2)
    checks += 4
    assert good == Affine(0b11, 0)
    assert good.table(2) == (1, 0, 0, 1)
    assert Affine(0b11, 1).table(2) != good.table(2)

    return {
        "schema": "Rmix341-typed-affine-annotation-audit-v1",
        "status": "PASS",
        "checks": checks,
        "witness": w,
        "exhaustive_two_variable_factors": {
            "factor_count": 16,
            "candidate_annotations_per_factor": 8,
            "affine_factor_count": affine_factor_count,
            "exact_annotation_count": len(exact_pairs),
        },
        "controls": {
            "sat_models": models,
            "unsat_models": [],
            "malformed_rejected": len(malformed),
            "mutations_rejected": len(bad_factors),
        },
        "claim_scope": (
            "Exact Boolean-factor preservation does not preserve native GF(2) "
            "consumer typing after the annotation is erased."
        ),
        "not_claimed": [
            "full R_mix341 checker",
            "counterexample to a consumer-aware annotation-preserving compiler",
            "B3 refutation",
            "machine lower bound",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
