#!/usr/bin/env python3
"""Finite controls for DECISION-CONTEXT-SEPARATION202.

The symbolic theorem is in the paired LaTeX report.  This program checks small
instances independently and emits deterministic JSON.  It uses only the Python
standard library and is designed to finish well below 30 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time


Literal = tuple[str, bool]  # (name, positive polarity)
Clause = tuple[Literal, Literal, Literal]


def variables(t: int) -> list[str]:
    out = ["z"]
    for i in range(1, t + 1):
        out += [f"a{i}", f"b{i}", f"c{i}", f"d{i}"]
    return out


def source(t: int, signs: tuple[int, ...]) -> list[Clause]:
    assert len(signs) == t and set(signs) <= {0, 1}
    clauses: list[Clause] = []
    for i, bit in enumerate(signs, 1):
        clauses.append((("z", True), (f"a{i}", bit == 0), (f"b{i}", True)))
    for i in range(1, t + 1):
        clauses.append((("z", False), (f"c{i}", True), (f"d{i}", True)))
    return clauses


def eval_clause(clause: Clause, assignment: dict[str, int]) -> bool:
    return any(bool(assignment[name]) == positive for name, positive in clause)


def eval_cnf(clauses: list[Clause], assignment: dict[str, int]) -> bool:
    return all(eval_clause(c, assignment) for c in clauses)


def source_witness(t: int) -> dict[str, int]:
    a = {v: 0 for v in variables(t)}
    a["z"] = 0
    for i in range(1, t + 1):
        a[f"b{i}"] = 1
    return a


def pins(i: int) -> dict[str, int]:
    return {f"a{i}": 0, f"b{i}": 0, "c1": 0, "d1": 0}


def brute_context_sat(t: int, signs: tuple[int, ...], i: int) -> bool:
    names = variables(t)
    fixed = pins(i)
    free = [v for v in names if v not in fixed]
    clauses = source(t, signs)
    for bits in itertools.product((0, 1), repeat=len(free)):
        assignment = dict(fixed)
        assignment.update(zip(free, bits))
        if eval_cnf(clauses, assignment):
            return True
    return False


def compiled_pin(literal_value: int, u: int, v: int) -> bool:
    # (l or u or v)(l or u or ~v)(l or ~u or v)(l or ~u or ~v)
    return all(
        literal_value or (u if pu else 1 - u) or (v if pv else 1 - v)
        for pu, pv in itertools.product((True, False), repeat=2)
    )


def canonical_bit_length(t: int) -> int:
    # A concrete self-delimiting accounting surrogate used only for finite
    # size tables: two clauses per block, three variable identifiers and
    # three sign bits per clause, plus a binary header for t.
    width = max(1, (4 * t + 1).bit_length())
    return 2 * t * (3 * width + 3) + 2 * t.bit_length() + 8


def main() -> None:
    started = time.perf_counter()
    context_cases = 0
    source_witness_checks = 0
    signatures: dict[str, int] = {}

    for t in range(1, 5):
        seen = set()
        for signs in itertools.product((0, 1), repeat=t):
            assert eval_cnf(source(t, signs), source_witness(t))
            source_witness_checks += 1
            answers = tuple(int(brute_context_sat(t, signs, i)) for i in range(1, t + 1))
            context_cases += t
            assert answers == signs
            seen.add(answers)
        assert len(seen) == 2**t
        signatures[str(t)] = len(seen)

    gadget_rows = []
    for literal_value, u, v in itertools.product((0, 1), repeat=3):
        got = compiled_pin(literal_value, u, v)
        assert got == bool(literal_value)
        gadget_rows.append([literal_value, u, v, int(got)])

    information_table = []
    for t in range(1, 65):
        n = canonical_bit_length(t)
        information_table.append(
            {
                "t": t,
                "source_bits_surrogate": n,
                "decision_states": 1,
                "context_states": 2**t,
                "context_bits_lower_bound": t,
            }
        )

    payload = {
        "run_id": "DECISION-CONTEXT-SEPARATION202",
        "status": "PASS",
        "exhaustive_t_max": 4,
        "source_witness_checks": source_witness_checks,
        "context_sat_checks": context_cases,
        "distinct_context_signatures": signatures,
        "compiled_pin_truth_table": gadget_rows,
        "decision_summary_token": "FIXED_YES_BASE",
        "decision_summary_distinct_states": 1,
        "information_table": information_table,
        "limitations": [
            "Finite enumeration is not the symbolic proof.",
            "The promise class does not contain arbitrary SAT.",
            "No native Turing-machine runtime lower bound is claimed.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    payload["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
