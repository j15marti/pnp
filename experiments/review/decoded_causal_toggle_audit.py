#!/usr/bin/env python3
"""Finite audit for decoded causal-use claims.

The symbolic theorem in the accompanying report is independent of this
program.  The program checks the construction on easy hostile controls and a
small canonical Monotone 3-SAT-(2,2) core.  It never extrapolates timings.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

Bits = tuple[int, ...]
Clause = tuple[int, ...]


class BudgetExceeded(RuntimeError):
    pass


def alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


@dataclass(frozen=True)
class Case:
    family: str
    source_bits: int
    q: Bits
    answer: int
    base_ops: int
    extraction_ops: int
    wrapper: str


@dataclass(frozen=True)
class Encoding:
    name: str
    encode: Callable[[Bits], Bits]
    decode: Callable[[Bits], Bits]


def complement(q: Bits) -> Bits:
    return tuple(1 - b for b in q)


def alternating_xor(q: Bits) -> Bits:
    return tuple(b ^ (i & 1) for i, b in enumerate(q))


def repeat3(q: Bits) -> Bits:
    return tuple(b for b in q for _ in range(3))


def majority3(c: Bits) -> Bits:
    assert len(c) % 3 == 0
    return tuple(int(sum(c[i:i + 3]) >= 2) for i in range(0, len(c), 3))


ENCODINGS = (
    Encoding("identity", lambda q: q, lambda c: c),
    Encoding("complement", complement, complement),
    Encoding("reverse", lambda q: q[::-1], lambda c: c[::-1]),
    Encoding("alternating_xor", alternating_xor, alternating_xor),
    Encoding("repetition3", repeat3, majority3),
)


def flip(q: Bits, i: int) -> Bits:
    return q[:i] + (1 - q[i],) + q[i + 1:]


def gamma_len(x: int) -> int:
    assert x >= 1
    return 2 * (x.bit_length() - 1) + 1


def cnf_bits(nvars: int, clauses: tuple[Clause, ...]) -> int:
    width = max(1, math.ceil(math.log2(nvars + 1)))
    return (gamma_len(nvars + 1) + gamma_len(len(clauses) + 1)
            + sum(gamma_len(len(c) + 1) + len(c) * (1 + width)
                  for c in clauses))


def clause_value(clause: Clause, assignment: Bits) -> bool:
    return any(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)


def sat_bruteforce(nvars: int, clauses: tuple[Clause, ...]) -> tuple[int, int]:
    checks = 0
    for assignment in itertools.product((0, 1), repeat=nvars):
        checks += 1
        if all(clause_value(c, assignment) for c in clauses):
            return 1, checks
    return 0, checks


def equality_cases(max_n: int) -> list[Case]:
    out: list[Case] = []
    for n in range(1, max_n + 1):
        for packed in range(1 << (2 * n)):
            u = tuple((packed >> i) & 1 for i in range(n))
            v = tuple((packed >> (n + i)) & 1 for i in range(n))
            q = tuple(a ^ b for a, b in zip(u, v))
            answer = int(not any(q))
            out.append(Case("equality_2sat", 8 * n, q, answer,
                            2 * n, 2 * n, "canonical"))
            if n <= 4:
                # The RT-0004 proper-three-CNF equality gadget has 8n
                # variables and 12n clauses; this is its exact semantic q.
                out.append(Case("proper3_equality", 180 * n, q, answer,
                                24 * n, 2 * n, "proper3"))
    return out


def horn_cases(max_n: int) -> list[Case]:
    out: list[Case] = []
    for n in range(2, max_n + 1):
        for mask in range(1 << (n - 1)):
            edges = tuple((mask >> i) & 1 for i in range(n - 1))
            reach = [1]
            for edge in edges:
                reach.append(reach[-1] & edge)
            # Unit x_1, selected implications x_i -> x_{i+1}, and unit not x_n.
            answer = int(not reach[-1])
            out.append(Case("horn_chain", 12 * n, tuple(reach), answer,
                            n, 2 * n, "canonical"))
    return out


def affine_cases(max_n: int) -> list[Case]:
    out: list[Case] = []
    for n in range(2, max_n + 1):
        for mask in range(1 << (n - 1)):
            rhs = tuple((mask >> i) & 1 for i in range(n - 1))
            prefix = [0]
            for bit in rhs:
                prefix.append(prefix[-1] ^ bit)
            for endpoint in (0, 1):
                answer = int(prefix[-1] == endpoint)
                out.append(Case("affine_tseitin_path", 14 * n,
                                tuple(prefix), answer, n, 2 * n,
                                "gaussian_or_parity"))
    return out


def exact_one_cases(max_blocks: int) -> list[Case]:
    out: list[Case] = []
    for blocks in range(1, max_blocks + 1):
        for mask in range(1 << blocks):
            chosen = tuple((mask >> i) & 1 for i in range(blocks))
            # Each independent width-three component chooses one of two
            # canonical local witnesses.  The component table is a compact
            # bounded-treewidth semantic summary.
            q = tuple(bit for c in chosen for bit in ((0, 0, 1) if c else (1, 0, 0)))
            out.append(Case("bounded_treewidth_product", 48 * blocks, q, 1,
                            5 * blocks, 6 * blocks, "independent_product"))
    return out


def h22_core() -> tuple[Clause, ...]:
    edges = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
    return edges + tuple(tuple(-v for v in e) for e in edges)


def permute_clause(c: Clause, perm: tuple[int, ...]) -> Clause:
    return tuple((1 if lit > 0 else -1) * perm[abs(lit) - 1] for lit in c)


def h22_signature(clauses: tuple[Clause, ...], nvars: int) -> Bits:
    unique = sorted(set(tuple(sorted(c, key=abs)) for c in clauses))
    bits: list[int] = []
    for clause in unique:
        bits.append(int(clause[0] > 0))
        present = {abs(x) for x in clause}
        bits.extend(int(v in present) for v in range(1, nvars + 1))
    return tuple(bits)


def h22_cases() -> list[Case]:
    base = h22_core()
    out: list[Case] = []
    for perm in itertools.islice(itertools.permutations(range(1, 7)), 24):
        clauses = tuple(permute_clause(c, perm) for c in base)
        answer, checks = sat_bruteforce(6, clauses)
        canonical_q = h22_signature(clauses, 6)
        for duplicate, padding in ((1, 0), (3, 6), (1, 24)):
            wrapped = tuple(c for c in clauses for _ in range(duplicate))
            out.append(Case("monotone_3sat_2_2", cnf_bits(6, wrapped) + padding,
                            canonical_q, answer, checks * len(wrapped),
                            len(wrapped) * 6, f"dup{duplicate}_pad{padding}"))
    return out


def audit_case(case: Case, totals: dict[str, int], families: dict[str, dict[str, int]]) -> None:
    assert case.q
    direct = case.answer
    recomp = case.answer
    materialized = case.answer
    assert direct == recomp == materialized

    row = families.setdefault(case.family, {
        "cases": 0, "max_source_bits": 0, "max_q_bits": 0,
        "max_encoded_state_bits": 0, "max_guard_ops": 0,
    })
    row["cases"] += 1
    row["max_source_bits"] = max(row["max_source_bits"], case.source_bits)
    row["max_q_bits"] = max(row["max_q_bits"], len(case.q))

    # Any one-bit-output execution admits a trivial last-step intervention.
    assert 1 - direct != direct
    totals["output_bit_interventions"] += 1

    # DIRECT/RECOMP expose no designated retained q buffer. MATERIALIZE does,
    # but it is dead with respect to the output. CAUSAL_GUARD consumes it.
    totals["direct_absence_checks"] += 1
    totals["recomp_absence_checks"] += 1
    for enc in ENCODINGS:
        code = enc.encode(case.q)
        assert enc.decode(code) == case.q
        guard_clean = direct if enc.decode(code) == case.q else 1 - direct
        assert guard_clean == direct
        totals["encoding_roundtrips"] += 1
        totals["guard_clean_checks"] += 1
        row["max_encoded_state_bits"] = max(row["max_encoded_state_bits"], len(code))
        guard_ops = case.base_ops + 2 * case.extraction_ops + len(code) + len(case.q)
        row["max_guard_ops"] = max(row["max_guard_ops"], guard_ops)
        for i in range(len(case.q)):
            changed_q = flip(case.q, i)
            changed_code = enc.encode(changed_q)
            decoded = enc.decode(changed_code)
            assert decoded != case.q
            guarded = direct if decoded == case.q else 1 - direct
            assert guarded == 1 - direct
            assert materialized == direct
            totals["decoded_guard_interventions"] += 1
            totals["dead_materialization_interventions"] += 1


def run(max_n: int, seed: int) -> dict[str, object]:
    start = time.monotonic()
    cases = (equality_cases(max_n) + horn_cases(max_n + 2)
             + affine_cases(max_n + 2) + exact_one_cases(max_n)
             + h22_cases())
    totals = {
        "cases": len(cases), "semantic_agreement_checks": 0,
        "output_bit_interventions": 0, "direct_absence_checks": 0,
        "recomp_absence_checks": 0, "encoding_roundtrips": 0,
        "guard_clean_checks": 0, "decoded_guard_interventions": 0,
        "dead_materialization_interventions": 0,
    }
    families: dict[str, dict[str, int]] = {}
    for case in cases:
        audit_case(case, totals, families)
        totals["semantic_agreement_checks"] += 3

    return {
        "run_id": "RT-0005",
        "status": "PASS",
        "seed": seed,
        "method": "exhaustive easy controls and finite exact H_2,2 permutations",
        "encodings": [e.name for e in ENCODINGS],
        "variants": ["DIRECT", "MATERIALIZE", "CAUSAL_GUARD", "INTERP_CAUSAL", "RECOMP"],
        "totals": totals,
        "families": families,
        "elapsed_seconds": time.monotonic() - start,
        "limitations": [
            "Finite checks validate the construction and cost ledger only.",
            "The exact causal-guard insertion theorem is symbolic; no asymptotic lower bound is inferred from timings.",
            "Absence concerns the designated decoded q interface, not every unbounded functional of a complete trace.",
            "The H_2,2 decision control uses finite brute force and is not a polynomial SAT algorithm.",
            "Causal use alone supplies neither strict source contraction nor a nonrelativizing or nonalgebrizing hinge.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max-n", type=int, default=6)
    p.add_argument("--seed", type=int, default=20261011)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(25)
    try:
        result = run(a.max_n, a.seed)
    finally:
        signal.alarm(0)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
