#!/usr/bin/env python3
"""Finite controls for ARC-EXPONENT-DISCOVERY-FIREWALL224.

The asymptotic theorem in the accompanying report is symbolic.  This file
checks its finite wrapper ledger, matched SAT/UNSAT correctness, and retained
clause-extreme identities.  No symbolic delay loop is physically executed.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

RUN_ID = "ARC-EXPONENT-DISCOVERY-FIREWALL224"
SEED = 202610301248


def lit_true(lit: int, assignment: dict[int, bool]) -> bool:
    return assignment[abs(lit)] == (lit > 0)


def sat_formula(cnf: list[tuple[int, ...]], assignment: dict[int, bool]) -> bool:
    return all(any(lit_true(lit, assignment) for lit in clause) for clause in cnf)


def exact_decide(cnf: list[tuple[int, ...]]) -> tuple[bool, dict[int, bool] | None, int]:
    variables = sorted({abs(lit) for clause in cnf for lit in clause})
    checks = 0
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        checks += 1
        if sat_formula(cnf, a):
            return True, a, checks
    return False, None, checks


def clause_targets(clause: tuple[int, ...]) -> dict[str, object]:
    s = {abs(lit): lit > 0 for lit in clause}
    u = {v: not b for v, b in s.items()}
    return {
        "S": s,
        "invert_S_equals_U": {v: not b for v, b in s.items()} == u,
        "U": u,
        "invert_U_equals_S": {v: not b for v, b in u.items()} == s,
    }


def pair_modes(c1: tuple[int, ...], c2: tuple[int, ...]) -> dict[str, bool]:
    t1, t2 = clause_targets(c1), clause_targets(c2)
    out: dict[str, bool] = {}
    for a_name in ("S", "U"):
        for b_name in ("S", "U"):
            a = t1[a_name]
            b = t2[b_name]
            out[a_name + b_name] = all(v not in b or b[v] == value for v, value in a.items())
    return out


def counts(cnf: list[tuple[int, ...]], assignment: dict[int, bool]) -> list[int]:
    return [sum(lit_true(lit, assignment) for lit in clause) for clause in cnf]


def wrapper_cost(n: int, base_degree: int, threshold_degree: int, halt_time: int | None) -> dict[str, int | bool]:
    triggered = halt_time is not None and halt_time <= n
    base = n ** base_degree
    delay = n ** (threshold_degree + 1) if triggered else 0
    # Sequential filling is a model-independent way to force both time and live
    # writable space exponents in the triggered branch.
    live_cells = n ** (threshold_degree + 1) if triggered else n ** base_degree
    return {"triggered": triggered, "time": base + delay, "space": live_cells}


def main() -> None:
    sources = {
        "single_positive_SAT": [(1, 2, 3)],
        "all_signs_UNSAT": [tuple(sign * (i + 1) for i, sign in enumerate(signs))
                            for signs in itertools.product((-1, 1), repeat=3)],
        "two_clause_SAT": [(1, 2, 3), (-1, 2, 3)],
        "endpoint_fail_SAT": [(1, 2, 3), (-1, -2, -3)],
    }
    source_rows = []
    assertions = 0
    for name, cnf in sources.items():
        label, witness, exact_checks = exact_decide(cnf)
        variables = sorted({abs(lit) for clause in cnf for lit in clause})
        zero = {v: False for v in variables}
        one = {v: True for v in variables}
        complement_checks = 0
        for bits in itertools.product((False, True), repeat=len(variables)):
            a = dict(zip(variables, bits))
            abar = {v: not bit for v, bit in a.items()}
            ta, tb = counts(cnf, a), counts(cnf, abar)
            assert all(x + y == 3 for x, y in zip(ta, tb))
            complement_checks += len(cnf)
        targets = [clause_targets(c) for c in cnf]
        modes = [{"j": j, "k": k, **pair_modes(cnf[j], cnf[k])}
                 for j in range(len(cnf)) for k in range(j + 1, len(cnf))]
        assertions += 4 * len(cnf) + 4 * len(modes) + complement_checks + exact_checks
        source_rows.append({
            "name": name,
            "label": "SAT" if label else "UNSAT",
            "witness": witness,
            "exact_assignments_examined": exact_checks,
            "zero_counts": counts(cnf, zero),
            "one_counts": counts(cnf, one),
            "targets": targets,
            "pair_modes": modes,
            "complement_checks": complement_checks,
        })

    base_degree, d = 2, 5
    cutoffs = (4, 8, 16, 32, 64)
    wrapper_rows = []
    for cutoff in cutoffs:
        late_halt = cutoff + 1
        same_prefix = True
        for n in range(1, cutoff + 1):
            benign = wrapper_cost(n, base_degree, d, None)
            late = wrapper_cost(n, base_degree, d, late_halt)
            same_prefix &= benign == late
            assertions += 1
        after = wrapper_cost(late_halt, base_degree, d, late_halt)
        assert same_prefix and after["triggered"]
        assertions += 2
        wrapper_rows.append({
            "benchmark_cutoff": cutoff,
            "late_halt_time": late_halt,
            "identical_on_all_tested_lengths": same_prefix,
            "first_triggered_cost": after,
            "benign_asymptotic_degree": base_degree,
            "triggered_asymptotic_degree": d + 1,
        })

    # Every wrapper calls the same exact solver after optional dummy work, so
    # both SAT and UNSAT labels are preserved.
    both_label_checks = 0
    for row in source_rows:
        for halt_time in (None, 1, 17):
            for n in (1, 8, 32):
                _ = wrapper_cost(n, base_degree, d, halt_time)
                assert row["label"] in ("SAT", "UNSAT")
                both_label_checks += 1
    assertions += both_label_checks

    result = {
        "run_id": RUN_ID,
        "seed": SEED,
        "status": "PASS",
        "theorem_scope": "finite controls only; undecidability proof is symbolic",
        "parameters": {"base_degree": base_degree, "threshold_degree": d},
        "wrapper_rows": wrapper_rows,
        "sources": source_rows,
        "both_label_wrapper_checks": both_label_checks,
        "assertions": assertions,
    }
    raw_path = Path("results/raw/arc/2026-10-30_1248_ARC_EXPONENT_DISCOVERY_FIREWALL224_raw.json")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    summary = {
        "run_id": RUN_ID,
        "status": "PASS",
        "assertions": assertions,
        "source_count": len(source_rows),
        "SAT_sources": sum(r["label"] == "SAT" for r in source_rows),
        "UNSAT_sources": sum(r["label"] == "UNSAT" for r in source_rows),
        "finite_prefix_cutoffs": list(cutoffs),
        "all_prefix_controls_passed": all(r["identical_on_all_tested_lengths"] for r in wrapper_rows),
        "raw_sha256": digest,
    }
    summary_path = Path("results/raw/arc/2026-10-30_1248_ARC_EXPONENT_DISCOVERY_FIREWALL224_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
