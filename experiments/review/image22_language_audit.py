#!/usr/bin/env python3
"""Bounded audit for the canonical compiler-image NP language.

This verifies finite encoding, witness, off-image mismatch, and exponent
bookkeeping identities.  It does not decide image nonmembership, prove a
machine lower bound, or extrapolate from tested instances.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import universal22 as u

RUN_ID = "IMAGE22COMP1"
START = time.monotonic()
COUNTS: Counter[str] = Counter()


def check(value: bool, group: str) -> None:
    if time.monotonic() - START > 25:
        raise TimeoutError("cooperative 25-second budget exceeded")
    COUNTS[group] += 1
    if not value:
        raise AssertionError(f"{group} assertion {COUNTS[group]}")


def encode_cnf(cnf: u.CNF) -> bytes:
    """One explicit canonical UTF-8 encoding used only by this audit."""
    return json.dumps(cnf, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def assignment_witness(n: int, bits: tuple[int, ...]) -> dict[int, int]:
    return dict(enumerate(bits, 1))


def image_yes_verifier(target: bytes, source: u.CNF, bits: tuple[int, ...]) -> bool:
    """NP verifier: source preimage + satisfying assignment are the witness."""
    try:
        u.check_proper(source)
        comp = u.compile22(source)
    except (ValueError, AssertionError):
        return False
    if len(bits) != comp.source_n:
        return False
    values = assignment_witness(comp.source_n, bits)
    return encode_cnf(comp.clauses) == target and u.eval_cnf(source, values)


def is_c22(cnf: u.CNF) -> bool:
    try:
        n = u.check_proper(cnf)
    except ValueError:
        return False
    occ = Counter(lit for clause in cnf for lit in clause)
    return all(occ[x] == 2 and occ[-x] == 2 for x in range(1, n + 1))


def find_model(cnf: u.CNF) -> tuple[int, ...] | None:
    n = u.check_proper(cnf)
    for bits in itertools.product((0, 1), repeat=n):
        if u.eval_cnf(cnf, assignment_witness(n, bits)):
            return bits
    return None


def main() -> dict:
    proper_2sat, _ = u.properize23([(1, 2), (-1, 2)])
    cases: dict[str, u.CNF] = {
        "single_clause": [(1, 2, 3)],
        "horn": [(1, -2, -3), (-1, 2, -3), (-1, -2, 3)],
        "properized_2sat": proper_2sat,
        "independent_product": [(1, 2, 3), (4, 5, 6)],
        "affine_tseitin_control": u.W1,
        "cube_unsat": [
            tuple((i + 1) * (1 if bits[i] == 0 else -1) for i in range(3))
            for bits in itertools.product((0, 1), repeat=3)
        ],
    }

    rows = []
    for name, source in cases.items():
        comp = u.compile22(source)
        target = encode_cnf(comp.clauses)
        source_bytes = encode_cnf(source)
        check(is_c22(comp.clauses), "target_domain")
        check(len(source_bytes) <= len(target), "finite_preimage_length")
        model = find_model(source) if comp.source_n <= 15 else None
        if model is not None:
            check(image_yes_verifier(target, source, model), "yes_witness")
            wrong = tuple(1 - bit for bit in model)
            if not u.eval_cnf(source, assignment_witness(comp.source_n, wrong)):
                check(not image_yes_verifier(target, source, wrong), "wrong_assignment")
        else:
            for bits in itertools.product((0, 1), repeat=comp.source_n):
                check(not image_yes_verifier(target, source, bits), "unsat_no_yes_witness")

        # The verifier must compare the complete canonical target, not a tag.
        mutated = bytearray(target)
        mutated[len(mutated) // 2] ^= 1
        witness = model if model is not None else (0,) * comp.source_n
        check(not image_yes_verifier(bytes(mutated), source, witness), "byte_mismatch")
        check(not image_yes_verifier(target + b" ", source, witness), "padding_mismatch")

        rows.append(
            {
                "case": name,
                "source_variables": comp.source_n,
                "source_clauses": len(source),
                "target_variables": comp.n,
                "target_clauses": len(comp.clauses),
                "source_bytes": len(source_bytes),
                "target_bytes": len(target),
                "source_satisfiable": model is not None,
            }
        )

    # If construction costs N^a and target length is at most N^q, a target
    # decider of exponent d composes with exponent max(a, q*d).  Arbitrary
    # fixed d remains polynomial; it is not erased.
    exponent_rows = []
    for a in range(1, 6):
        for q in range(1, 5):
            for d in range(1, 21):
                composed = max(a, q * d)
                check(composed >= d, "exponent_not_erased")
                check(composed < 100, "finite_polynomial_composition")
                exponent_rows.append((a, q, d, composed))

    # Standard wrappers change only fixed polynomial exponents in this ledger.
    wrapper_rows = []
    for d in range(1, 21):
        for delay in range(0, 8):
            copy = max(d, 1)
            dead = max(d, delay)
            recomp = 2 * d
            check(all(x >= d for x in (copy, dead, recomp)), "wrapper_charge")
            wrapper_rows.append((d, delay, copy, dead, recomp))

    elapsed = time.monotonic() - START
    return {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "seed": None,
        "method": "exhaustive on listed small sources plus exact integer bookkeeping",
        "assertions": sum(COUNTS.values()),
        "checks_by_group": dict(COUNTS),
        "elapsed_seconds": elapsed,
        "cases": rows,
        "exponent_identities": len(exponent_rows),
        "wrapper_identities": len(wrapper_rows),
        "limitations": [
            "No image-nonmembership algorithm is implemented or assumed.",
            "Finite source checks do not prove NP-completeness or a time lower bound.",
            "The source preimage and assignment are NP witnesses, not data forced on an arbitrary decider.",
        ],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "compiler_sha256": hashlib.sha256(Path(u.__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
