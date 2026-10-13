#!/usr/bin/env python3
"""Bounded audit of the solver-trace-to-Resolution promotion gap.

The experiment deliberately stays finite.  It verifies that a fixed deterministic
CNF decider induces an efficiently checkable, solver-dependent trace system, and
that harmless input wrappers change those traces without turning them into
Resolution derivations.  It does *not* extrapolate a runtime lower bound.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Iterable


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


@dataclass(frozen=True)
class TraceRow:
    assignment: int
    first_falsified_clause: int | None


def variables(cnf: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in cnf for lit in clause}))


def clause_true(clause: Clause, assignment: int, pos: dict[int, int]) -> bool:
    for lit in clause:
        bit = (assignment >> pos[abs(lit)]) & 1
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return True
    return False


def exhaustive_decider(cnf: CNF) -> tuple[bool, list[TraceRow], int | None]:
    """Return the one-bit answer and a fully replayable deterministic trace."""
    vs = variables(cnf)
    pos = {v: i for i, v in enumerate(vs)}
    trace: list[TraceRow] = []
    for a in range(1 << len(vs)):
        bad = next((i for i, c in enumerate(cnf) if not clause_true(c, a, pos)), None)
        trace.append(TraceRow(a, bad))
        if bad is None:
            return True, trace, a
    return False, trace, None


def verify_trace(cnf: CNF, answer: bool, trace: list[TraceRow], witness: int | None) -> bool:
    """Replay every transition; runtime is linear in the submitted trace size."""
    vs = variables(cnf)
    pos = {v: i for i, v in enumerate(vs)}
    if not trace:
        return False
    expected = 0
    for row in trace:
        if row.assignment != expected:
            return False
        bad = next((i for i, c in enumerate(cnf) if not clause_true(c, row.assignment, pos)), None)
        if row.first_falsified_clause != bad:
            return False
        expected += 1
        if bad is None:
            return answer and witness == row.assignment and row is trace[-1]
    return (not answer) and witness is None and expected == (1 << len(vs))


def mutate_trace(trace: list[TraceRow]) -> list[TraceRow]:
    out = list(trace)
    row = out[len(out) // 2]
    wrong = 0 if row.first_falsified_clause is None else row.first_falsified_clause + 1
    out[len(out) // 2] = TraceRow(row.assignment, wrong)
    return out


def normalize(cnf: CNF) -> CNF:
    return tuple(sorted((tuple(sorted(c, key=lambda x: (abs(x), x < 0))) for c in cnf)))


def rename(cnf: CNF, mapping: dict[int, int]) -> CNF:
    return tuple(tuple((1 if lit > 0 else -1) * mapping[abs(lit)] for lit in c) for c in cnf)


def xor3_clauses(rhs: int) -> CNF:
    """CNF for x1 xor x2 xor x3 = rhs, by forbidding wrong assignments."""
    clauses: list[Clause] = []
    for a in range(8):
        parity = ((a >> 0) ^ (a >> 1) ^ (a >> 2)) & 1
        if parity != rhs:
            clauses.append(tuple(-(i + 1) if ((a >> i) & 1) else (i + 1) for i in range(3)))
    return tuple(clauses)


def gf2_eliminate(rows: Iterable[tuple[int, int]], nvars: int) -> tuple[bool, list[tuple[int, int, int]]]:
    """Row reduction; each certificate row records (pivot, mask, rhs)."""
    basis: dict[int, tuple[int, int]] = {}
    cert: list[tuple[int, int, int]] = []
    for mask0, rhs0 in rows:
        mask, rhs = mask0, rhs0
        while mask:
            p = mask.bit_length() - 1
            if p not in basis:
                basis[p] = (mask, rhs)
                cert.append((p, mask, rhs))
                break
            mask ^= basis[p][0]
            rhs ^= basis[p][1]
        if mask == 0 and rhs:
            cert.append((-1, 0, 1))
            return False, cert
    assert all(0 <= p < nvars for p in basis)
    return True, cert


def verify_gf2(rows: list[tuple[int, int]], nvars: int, answer: bool) -> bool:
    replay, _ = gf2_eliminate(rows, nvars)
    return replay == answer


def toy_uniform_family(k: int) -> CNF:
    """Uniformly generated UNSAT controls; no hardness is claimed for these toys."""
    return ((1, 2), (-1, 2), (1, -2), (-1, -2)) + tuple(
        (v, -v) for v in range(3, k + 1)
    )


def frontdoor_decider(cnf: CNF, max_k: int) -> tuple[bool, str, int]:
    """Fast exact-match front door, exhaustive correct fallback elsewhere."""
    for k in range(2, max_k + 1):
        if cnf == toy_uniform_family(k):
            return False, "uniform-family-frontdoor", k - 1
    answer, trace, _ = exhaustive_decider(cnf)
    return answer, "exhaustive-fallback", len(trace)


def main() -> None:
    base_2sat: CNF = ((1, 2), (-1, 2), (1, -2), (-1, -2))
    horn: CNF = ((1,), (-1, 2), (-2,))
    affine_unsat = xor3_clauses(0) + xor3_clauses(1)
    bounded_tw: CNF = ((1,), (-1, 2), (-2, 3), (-3,))
    independent: CNF = base_2sat + ((3, 4), (-3, 4))
    cases: dict[str, CNF] = {
        "2sat_unsat": base_2sat,
        "horn_unsat": horn,
        "affine_tseitin_cnf_unsat": affine_unsat,
        "bounded_treewidth_unsat": bounded_tw,
        "independent_product_unsat": independent,
        "redundant_clause_wrapper": base_2sat + (base_2sat[0],),
        "tautology_wrapper": base_2sat + ((1, -1),),
        "padding_wrapper": base_2sat + ((3, -3), (4, -4)),
        "renaming_wrapper": rename(base_2sat, {1: 2, 2: 1}),
        "alternate_order_wrapper": tuple(tuple(reversed(c)) for c in reversed(base_2sat)),
    }

    records = []
    for name, cnf in cases.items():
        t0 = time.perf_counter_ns()
        canon = normalize(cnf)
        t1 = time.perf_counter_ns()
        answer, trace, witness = exhaustive_decider(cnf)
        t2 = time.perf_counter_ns()
        verified = verify_trace(cnf, answer, trace, witness)
        mutation_rejected = not verify_trace(cnf, answer, mutate_trace(trace), witness)
        t3 = time.perf_counter_ns()
        assert verified and mutation_rejected
        records.append({
            "case": name,
            "variables": len(variables(cnf)),
            "clauses": len(cnf),
            "answer": answer,
            "trace_rows": len(trace),
            "preprocess_ns": t1 - t0,
            "decision_ns": t2 - t1,
            "verification_ns": t3 - t2,
            "trace_verified": verified,
            "single_row_mutation_rejected": mutation_rejected,
            "canonical_clause_count": len(canon),
        })

    # Same affine contradiction in its native representation: x1+x2+x3=0 and =1.
    affine_rows = [(0b111, 0), (0b111, 1)]
    affine_answer, affine_cert = gf2_eliminate(affine_rows, 3)
    assert not affine_answer and verify_gf2(affine_rows, 3, affine_answer)

    frontdoor_rows = []
    for k in range(2, 9):
        canonical = toy_uniform_family(k)
        wrapped = tuple(reversed(canonical))
        a0, path0, work0 = frontdoor_decider(canonical, 8)
        a1, path1, work1 = frontdoor_decider(wrapped, 8)
        assert not a0 and not a1
        assert path0 == "uniform-family-frontdoor"
        assert path1 == "exhaustive-fallback"
        frontdoor_rows.append({
            "k": k,
            "canonical_path": path0,
            "canonical_work_units": work0,
            "clause_order_wrapper_path": path1,
            "clause_order_wrapper_work_units": work1,
        })

    semantic = {
        "records_without_timing": [
            {k: v for k, v in r.items() if not k.endswith("_ns")} for r in records
        ],
        "affine_native": {
            "answer": affine_answer,
            "input_rows": len(affine_rows),
            "certificate_rows": len(affine_cert),
            "verified": verify_gf2(affine_rows, 3, affine_answer),
        },
        "frontdoor_control": frontdoor_rows,
        "typed_interface_audit": {
            "trace_rows_are_machine_transitions": True,
            "trace_rows_are_resolution_clauses": False,
            "resolution_inference_checked": False,
            "missing_promotion_arrow": "uniform model-preserving translation/p-simulation from every solver-induced trace system to Resolution",
        },
        "scope": "finite verifier and hostile-wrapper audit only; no asymptotic extrapolation",
    }
    semantic_bytes = json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "experiment": "solver_trace_proof_system_audit",
        "status": "COMPUTATIONAL",
        "records": records,
        "affine_native": semantic["affine_native"],
        "frontdoor_control": frontdoor_rows,
        "typed_interface_audit": semantic["typed_interface_audit"],
        "scope": semantic["scope"],
        "semantic_sha256": hashlib.sha256(semantic_bytes).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
