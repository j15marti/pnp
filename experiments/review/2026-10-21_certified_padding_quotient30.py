#!/usr/bin/env python3
"""Audit CERTIFIED-PADDING-QUOTIENT30.

The script constructs two proper-3CNF padding orbits.  One has a SAT core,
the other an UNSAT core.  Each payload bit controls only the sign of a fresh
literal in a clause that is independently satisfiable by setting a fresh
guard variable to 1.  A promised streaming canonicalizer erases those signs.

This is a restricted positive control, not an all-input SAT reduction.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass, asdict
from pathlib import Path


Clause = tuple[int, int, int]
Formula = tuple[Clause, ...]


def sat_core() -> Formula:
    # Every clause contains positive x1, hence x1=1 satisfies the core.
    four = tuple((1, s2 * 2, s3 * 3) for s2 in (-1, 1) for s3 in (-1, 1))
    return four + four


def unsat_core() -> Formula:
    # All eight sign patterns on three variables; every assignment falsifies one.
    return tuple(
        (s1 * 1, s2 * 2, s3 * 3)
        for s1 in (-1, 1)
        for s2 in (-1, 1)
        for s3 in (-1, 1)
    )


def payload_clause(i: int, bit: int) -> Clause:
    a = 4 + 3 * i
    b = a + 1
    c = a + 2
    return (a, b, c if bit == 0 else -c)


def orbit_formula(label: str, bits: tuple[int, ...]) -> Formula:
    core = sat_core() if label == "SAT" else unsat_core()
    return core + tuple(payload_clause(i, bit) for i, bit in enumerate(bits))


def canonicalize_promised(formula: Formula) -> Formula:
    out = list(formula[:8])
    for i, clause in enumerate(formula[8:]):
        a = 4 + 3 * i
        assert clause[0] == a and clause[1] == a + 1 and abs(clause[2]) == a + 2
        out.append((a, a + 1, a + 2))
    return tuple(out)


def proper_3cnf(formula: Formula) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in formula)


def eval_formula(formula: Formula, assignment: int) -> bool:
    for clause in formula:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def brute_sat(formula: Formula) -> bool:
    nvars = max(abs(lit) for clause in formula for lit in clause)
    return any(eval_formula(formula, a) for a in range(1 << nvars))


def encode_formula(formula: Formula) -> bytes:
    # Fixed-width signed records make every orbit member have identical length.
    nvars = max(abs(lit) for clause in formula for lit in clause)
    width = len(str(nvars))
    header = f"v={nvars:0{width}d};m={len(formula):0{width}d};w={width};"
    body = "".join("".join(("+" if x > 0 else "-") + f"{abs(x):0{width}d}" for x in c) + ";" for c in formula)
    return (header + body).encode("ascii")


@dataclass
class Audit:
    max_r: int = 12
    formulas_checked: int = 0
    proper_checks: int = 0
    collapse_checks: int = 0
    label_separation_checks: int = 0
    equal_length_checks: int = 0
    brute_truth_checks: int = 0
    failures: int = 0


def check(cond: bool, audit: Audit, field: str) -> None:
    setattr(audit, field, getattr(audit, field) + 1)
    if not cond:
        audit.failures += 1
        raise AssertionError(field)


def run() -> dict:
    audit = Audit()
    rows = []
    for r in range(audit.max_r + 1):
        canon = {}
        lengths = {"SAT": set(), "UNSAT": set()}
        for label in ("SAT", "UNSAT"):
            targets = set()
            for bits in itertools.product((0, 1), repeat=r):
                f = orbit_formula(label, bits)
                audit.formulas_checked += 1
                check(proper_3cnf(f), audit, "proper_checks")
                lengths[label].add(len(encode_formula(f)))
                targets.add(canonicalize_promised(f))
                check(canonicalize_promised(f) == orbit_formula(label, (0,) * r), audit, "collapse_checks")
                if r <= 4:
                    check(brute_sat(f) == (label == "SAT"), audit, "brute_truth_checks")
            canon[label] = next(iter(targets))
            check(len(targets) == 1, audit, "collapse_checks")
            check(len(lengths[label]) == 1, audit, "equal_length_checks")
        check(canon["SAT"] != canon["UNSAT"], audit, "label_separation_checks")
        check(lengths["SAT"] == lengths["UNSAT"], audit, "equal_length_checks")
        rows.append({
            "r": r,
            "orbit_size_per_label": 1 << r,
            "clauses": 8 + r,
            "variables": 3 + 3 * r,
            "encoded_bytes": next(iter(lengths["SAT"])),
            "canonical_targets": 2,
        })

    # A structural witness, separate from brute force: all payload clauses have
    # a fresh positive guard variable, so they cannot alter the core's status.
    structural = {
        "sat_witness": "x1=1 and every payload guard a_i=1",
        "unsat_reason": "the first eight clauses contain all sign patterns on x1,x2,x3",
        "stream_ledger": {
            "passes": 1,
            "source_rereads": 0,
            "input_records": "3(8+r) literals plus header",
            "output_records": "3(8+r) literals plus header",
            "workspace_bits": "O(log r) counter plus one O(log r)-bit literal record",
            "record_ram_time": "Theta(encoded length)",
            "scope": "promised certified padding orbit only",
        },
        "kt_upper_bound": "polylog(M) for each of the two canonical template families",
        "mktp_consequence": "for fixed k, p=M^(1/k+o(1)) eventually exceeds polylog(M), so both labels map to MKTP-YES",
    }
    payload = {"run_id": "CERTIFIED-PADDING-QUOTIENT30", "audit": asdict(audit), "rows": rows, "proof_ledger": structural}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    return payload


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
