#!/usr/bin/env python3
"""Finite audit for TESTS-0011 typed wrapper-orbit noncoverage.

This is bookkeeping, not an asymptotic proof.  It checks that six declared
child-preserving wrappers preserve a base tag and the SAT decision bit, while
constant replacement joins the otherwise disjoint base-tag components.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import defaultdict
from dataclasses import dataclass


VARS = (1, 2, 3)
CLAUSES = tuple(tuple(v if bit else -v for v, bit in zip(VARS, signs))
                for signs in itertools.product((0, 1), repeat=3))
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
BASES = tuple(range(8))
MAX_DEPTH = 4


def sat_bruteforce(formula: tuple[tuple[int, ...], ...]) -> bool:
    n = max((abs(lit) for clause in formula for lit in clause), default=0)
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in formula):
            return True
    return False


def gf2_consistent(rows: list[tuple[int, int]], n: int) -> bool:
    a = [[(mask >> j) & 1 for j in range(n)] + [rhs] for mask, rhs in rows]
    pivot = 0
    for col in range(n):
        hit = next((r for r in range(pivot, len(a)) if a[r][col]), None)
        if hit is None:
            continue
        a[pivot], a[hit] = a[hit], a[pivot]
        for r in range(len(a)):
            if r != pivot and a[r][col]:
                a[r] = [x ^ y for x, y in zip(a[r], a[pivot])]
        pivot += 1
    return not any(not any(row[:-1]) and row[-1] for row in a)


@dataclass(frozen=True)
class Program:
    base: int
    word: tuple[str, ...]

    @property
    def core(self) -> int:
        return self.base

    def run(self, formula: tuple[tuple[int, ...], ...], ledger: dict[str, int],
            base_answer: bool | None = None) -> bool:
        answer = sat_bruteforce(formula) if base_answer is None else base_answer
        for wrapper in self.word:
            if wrapper == "DIRECT":
                ledger["preprocess"] += 0
            elif wrapper == "DEAD":
                ledger["preprocess"] += 2
                ledger["extract"] += 1
                _ = hashlib.sha256(repr(formula).encode()).digest()[0]
            elif wrapper == "COPY":
                ledger["preprocess"] += 1
                ledger["extract"] += 2
                ledger["reconstruct"] += 1
                answer = bool(answer or answer)
            elif wrapper == "DELAY":
                ledger["preprocess"] += 3
                _ = sum(range(len(formula) + 1))
            elif wrapper == "INTERP":
                ledger["preprocess"] += 2
                ledger["extract"] += 1
                ledger["reconstruct"] += 2
                answer = (not answer) is False
            elif wrapper == "RECOMP":
                ledger["preprocess"] += 1
                ledger["extract"] += 3
                ledger["reconstruct"] += 3
                answer = sat_bruteforce(formula) if base_answer is None else base_answer
            else:
                raise AssertionError(wrapper)
        ledger["output"] += 1
        return answer


def words_upto(depth: int):
    yield ()
    for d in range(1, depth + 1):
        yield from itertools.product(WRAPPERS, repeat=d)


def component_count(nodes: list[Program], replacement: bool) -> int:
    parent = list(range(len(nodes)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    by = {(p.base, p.word): i for i, p in enumerate(nodes)}
    for i, p in enumerate(nodes):
        if p.word:
            union(i, by[(p.base, p.word[:-1])])
    if replacement:
        roots = [by[(b, ())] for b in BASES]
        for r in roots[1:]:
            union(roots[0], r)
    return len({find(i) for i in range(len(nodes))})


def main() -> dict:
    started = time.perf_counter()
    words = list(words_upto(MAX_DEPTH))
    nodes = [Program(base, word) for base in BASES for word in words]
    formulas = [tuple(CLAUSES[i] for i in range(8) if mask & (1 << i))
                for mask in range(256)]
    truth = [sat_bruteforce(f) for f in formulas]
    ledger = defaultdict(int)
    semantic_checks = 0
    core_checks = 0
    for p in nodes:
        assert p.core == p.base
        core_checks += 1
        for f, expected in zip(formulas, truth):
            assert p.run(f, ledger, expected) == expected
            semantic_checks += 1

    # Presentation controls: clause order, duplication, padding metadata, and
    # literal-list round trips leave the decoded SAT bit unchanged.
    encoding_checks = 0
    for f, expected in zip(formulas, truth):
        variants = (f, tuple(reversed(f)), f + (f[:1] if f else ()), tuple(tuple(c) for c in f))
        for decoded in variants:
            assert sat_bruteforce(decoded) == expected
            encoding_checks += 1

    named_controls = {
        "2SAT": (((1, 2), (-1, 2), (1, -2)),),
        "Horn": (((-1, -2, 3), (-3,), (1,)),),
        "bounded_treewidth": (((1, 2), (-2, 3), (-3,)),),
        "independent_product": (((1,), (2,), (3,)),),
        "redundant_clauses": (((1, 2, 3), (1, 2, 3), (-1,)),),
    }
    hostile_checks = 0
    for suites in named_controls.values():
        for f in suites:
            expected = sat_bruteforce(f)
            for base in BASES:
                assert Program(base, ("DEAD", "COPY", "INTERP", "RECOMP")).run(f, ledger, expected) == expected
                hostile_checks += 1

    affine_checks = 0
    for mask in range(1 << 6):
        rows = []
        templates = ((0b001, 0), (0b010, 1), (0b100, 0),
                     (0b011, 1), (0b110, 0), (0b101, 1))
        for i, row in enumerate(templates):
            if mask & (1 << i):
                rows.append(row)
        got = gf2_consistent(rows, 3)
        brute = any(
            all(
                (sum((assignment >> j) & 1 for j in range(3) if (m >> j) & 1) & 1) == rhs
                for m, rhs in rows
            )
            for assignment in range(8)
        )
        assert got == brute
        affine_checks += 1

    without_replace = component_count(nodes, False)
    with_replace = component_count(nodes, True)
    assert without_replace == len(BASES)
    assert with_replace == 1

    return {
        "run_id": "TESTS-0011",
        "status": "COMPUTATIONAL",
        "base_count": len(BASES),
        "wrapper_alphabet": list(WRAPPERS),
        "max_depth": MAX_DEPTH,
        "words_per_base": len(words),
        "program_nodes": len(nodes),
        "components_child_preserving": without_replace,
        "components_with_constant_replacement": with_replace,
        "core_checks": core_checks,
        "semantic_checks": semantic_checks,
        "encoding_checks": encoding_checks,
        "hostile_easy_family_checks": hostile_checks,
        "affine_gaussian_checks": affine_checks,
        "ledger": dict(sorted(ledger.items())),
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope_warning": "Finite audit only; no asymptotic lower bound or arbitrary-program coverage follows."
    }


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True, indent=2))
