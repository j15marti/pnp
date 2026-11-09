#!/usr/bin/env python3
"""Independent arbitrary-length identifier audit for tracker node P2-L1-534.

This checks only the explicit-identifier reduction.  It does not execute the
external subexponential SAT machine or any R_mix341 checker.
"""
from __future__ import annotations

import itertools
import json
import math
import random
import resource
import sys
import time


Literal = tuple[str, bool]
Formula = list[list[Literal]]


def encode(formula: Formula) -> str:
    rows = ["cnf"]
    for clause in formula:
        rows.append("c" + "".join((" +" if sign else " -") + name for name, sign in clause))
    return "\n".join(rows) + "\n"


def parse(source: str) -> Formula:
    if not source.startswith("cnf\n") or not source.endswith("\n"):
        raise ValueError("header/termination")
    body = source[4:-1]
    if not body:
        return []
    formula: Formula = []
    for row in body.split("\n"):
        parts = row.split(" ")
        if not parts or parts[0] != "c" or any(not x for x in parts[1:]):
            raise ValueError("clause")
        clause: list[Literal] = []
        for token in parts[1:]:
            if len(token) < 2 or token[0] not in "+-":
                raise ValueError("sign")
            name = token[1:]
            if not name.startswith("1") or any(ch not in "01" for ch in name):
                raise ValueError("noncanonical identifier")
            clause.append((name, token[0] == "+"))
        formula.append(clause)
    return formula


def source_sat(formula: Formula) -> bool:
    names = sorted({name for clause in formula for name, _ in clause})
    if len(names) > 16:
        raise ValueError("finite audit variable cap")
    for bits in itertools.product((False, True), repeat=len(names)):
        assignment = dict(zip(names, bits))
        if all(any(assignment[name] == sign for name, sign in clause) for clause in formula):
            return True
    return False


def simplify(formula: Formula, assignment: dict[str, bool]) -> Formula:
    out: Formula = []
    for clause in formula:
        if any(name in assignment and assignment[name] == sign for name, sign in clause):
            continue
        residual: list[Literal] = []
        seen: set[Literal] = set()
        for literal in clause:
            if literal[0] not in assignment and literal not in seen:
                residual.append(literal)
                seen.add(literal)
        if any((name, not sign) in seen for name, sign in seen):
            continue
        out.append(residual)
    return out


def to_three_cnf(formula: Formula) -> tuple[list[list[int]], int]:
    names = sorted({name for clause in formula for name, _ in clause})
    dense = {name: i + 1 for i, name in enumerate(names)}
    next_var = len(names)
    out: list[list[int]] = []
    for clause in formula:
        row = [dense[name] if sign else -dense[name] for name, sign in clause]
        if len(row) <= 3:
            out.append(row)
            continue
        auxiliaries = list(range(next_var + 1, next_var + len(row) - 2))
        next_var += len(auxiliaries)
        out.append([row[0], row[1], auxiliaries[0]])
        for j in range(1, len(auxiliaries)):
            out.append([-auxiliaries[j - 1], row[j + 1], auxiliaries[j]])
        out.append([-auxiliaries[-1], row[-2], row[-1]])
    return out, next_var


def integer_cnf_sat(formula: list[list[int]], nvars: int) -> bool:
    if nvars > 22:
        raise ValueError("finite audit variable cap")
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in formula):
            return True
    return False


def cutoff(nbits: int) -> int:
    logn = math.log2(nbits)
    return math.floor(math.log2(nbits / (logn * logn)))


def audit(formula: Formula) -> dict[str, int | bool]:
    source = encode(formula)
    assert parse(source) == formula
    nbits = len(source.encode("ascii")) * 8
    # The theorem sends finitely many small lengths to a fixed fallback.  For
    # finite controls we use level 1 there, which leaves every canonical name
    # in the residual and preserves the same occurrence accounting.
    level = max(1, cutoff(nbits))
    names = sorted({name for clause in formula for name, _ in clause})
    short = [name for name in names if len(name) < level]
    long_occurrences = sum(len(name) >= level for clause in formula for name, _ in clause)
    # Canonical nonempty binary names of length < level are fewer than 2^level.
    assert len(short) < 2**level
    # Every long occurrence contributes at least level actual source bits.
    assert long_occurrences * level <= nbits
    expected = source_sat(formula)
    found = False
    max_guest_vars = 0
    for values in itertools.product((False, True), repeat=len(short)):
        residual = simplify(formula, dict(zip(short, values)))
        assert sum(map(len, residual)) <= long_occurrences
        guest, guest_vars = to_three_cnf(residual)
        assert all(len(row) <= 3 for row in guest)
        assert guest_vars <= 2 * long_occurrences
        found |= integer_cnf_sat(guest, guest_vars)
        max_guest_vars = max(max_guest_vars, guest_vars)
    assert found == expected
    return {
        "source_bits": nbits,
        "cutoff": level,
        "short_ids": len(short),
        "branches": 2 ** len(short),
        "long_occurrences": long_occurrences,
        "max_guest_vars": max_guest_vars,
        "sat": expected,
        "max_identifier_bits": max((len(name) for name in names), default=0),
    }


def canonical_names(width: int) -> list[str]:
    return ["1" + "".join(bits) for bits in itertools.product("01", repeat=width - 1)]


def cases() -> list[Formula]:
    huge_a = "1" + "0" * 8191
    huge_b = "1" + "01" * 4095
    long5 = ["1" + format(i, "02047b") for i in range(1, 6)]
    base: list[Formula] = [
        [],
        [[]],
        [[(huge_a, True)], [(huge_a, False)]],
        [[(huge_a, True), (huge_b, True)], [(huge_a, False)], [(huge_b, False)]],
        [[(name, True) for name in canonical_names(3)] + [(huge_a, True)],
         [(name, False) for name in canonical_names(3)], [(huge_a, False)]],
        [[(name, True) for name in long5]] + [[(name, False)] for name in long5],
    ]
    rng = random.Random(460)
    pool = canonical_names(1) + canonical_names(2) + canonical_names(3) + [huge_a, huge_b]
    for _ in range(35):
        chosen = rng.sample(pool, rng.randint(1, min(7, len(pool))))
        formula: Formula = []
        for _ in range(rng.randint(1, 7)):
            width = rng.randint(1, min(5, len(chosen)))
            row = [(name, bool(rng.getrandbits(1))) for name in rng.sample(chosen, width)]
            formula.append(row)
        base.append(formula)
    return base


def malformed_controls() -> int:
    bad = [
        "", "CNF\n", "cnf", "cnf\nc +01\n", "cnf\nc +0\n",
        "cnf\nc +1  -1\n", "cnf\nx +1\n", "cnf\nc +1\ntrailer\n",
        "cnf\nc +\n", "cnf\nc 1\n",
    ]
    rejected = 0
    for source in bad:
        try:
            parse(source)
        except ValueError:
            rejected += 1
    assert rejected == len(bad)
    return rejected


def cumulative_envelope_control() -> dict[str, float]:
    # A numerical control for the omitted max_{m<=N} step.  The proof in the
    # report uses a split at sqrt(N); these sample epsilons merely catch a
    # reversed max/pointwise implementation.
    values = {}
    for power in (12, 16, 20, 24):
        n = 2**power
        terms = []
        for m_power in range(4, power + 1):
            m = 2**m_power
            eps = 1 / math.sqrt(math.log2(m))
            terms.append(eps * m / math.log2(m))
        values[str(n)] = max(terms) / (n / math.log2(n))
    assert values[str(2**24)] < values[str(2**12)]
    return values


def main() -> None:
    started = time.perf_counter()
    rows = [audit(formula) for formula in cases()]
    result = {
        "run": "LSPV5-460-IDCUT-INDEPENDENT-v1",
        "status": "PASS",
        "configurations": len(rows),
        "sat": sum(bool(row["sat"]) for row in rows),
        "unsat": sum(not bool(row["sat"]) for row in rows),
        "branches": sum(int(row["branches"]) for row in rows),
        "malformed_rejected": malformed_controls(),
        "max_source_bits": max(int(row["source_bits"]) for row in rows),
        "max_identifier_bits": max(int(row["max_identifier_bits"]) for row in rows),
        "max_cutoff": max(int(row["cutoff"]) for row in rows),
        "max_guest_vars": max(int(row["max_guest_vars"]) for row in rows),
        "cumulative_envelope_ratios": cumulative_envelope_control(),
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "external_subexponential_machine_executed": False,
        "openai_lean_build_executed": False,
        "historical_Rmix341_checker_executed": False,
        "scope": "explicit identifier reduction and worst-case envelope only",
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
