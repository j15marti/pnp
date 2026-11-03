#!/usr/bin/env python3
"""REFEREE316: exact controls for a family-local backward-simulation lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import resource
import time
from pathlib import Path

RAW = Path("results/raw/arc/lspv5_316/family_local_backtranslation_referee316.json")


def php_cnf(pigeons: int, holes: int) -> tuple[list[list[int]], int]:
    """Standard functional PHP: every pigeon enters a hole; no shared hole."""
    def var(p: int, h: int) -> int:
        return p * holes + h + 1

    clauses = [[var(p, h) for h in range(holes)] for p in range(pigeons)]
    for h in range(holes):
        for p, q in itertools.combinations(range(pigeons), 2):
            clauses.append([-var(p, h), -var(q, h)])
    return clauses, pigeons * holes


def count_cnf_models(clauses: list[list[int]], variables: int) -> int:
    total = 0
    for mask in range(1 << variables):
        if all(any((bool(mask & (1 << (abs(lit) - 1))) if lit > 0 else
                        not bool(mask & (1 << (abs(lit) - 1)))) for lit in clause)
               for clause in clauses):
            total += 1
    return total


def k4_edges() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(4), 2))


def count_tseitin_models(charges: tuple[int, int, int, int]) -> int:
    edges = k4_edges()
    total = 0
    for mask in range(1 << len(edges)):
        ok = True
        for vertex in range(4):
            parity = 0
            for i, edge in enumerate(edges):
                if vertex in edge:
                    parity ^= (mask >> i) & 1
            ok &= parity == charges[vertex]
        total += int(ok)
    return total


REQUIRED = {
    "direction": "R_to_P",
    "proof_quantifier": "every_R_refutation",
    "same_source": True,
    "overhead": "polynomial_in_N_plus_R_cost",
}


def validate_transfer_schema(record: dict) -> tuple[bool, str]:
    for field, expected in REQUIRED.items():
        if record.get(field) != expected:
            return False, f"{field}: expected {expected!r}"
    if not isinstance(record.get("C"), (int, float)) or record["C"] <= 0:
        return False, "C must be positive"
    if not isinstance(record.get("d"), int) or isinstance(record.get("d"), bool) or record["d"] < 1:
        return False, "d must be a positive integer"
    return True, "accepted"


def derived_log2_floor(lower_log2: float, C: float, d: int, N: int) -> float | None:
    """If L/C)^(1/d) >= 2N, return log2 of certified half bound."""
    root_log2 = (lower_log2 - math.log2(C)) / d
    if root_log2 < 1 + math.log2(max(N, 1)):
        return None
    return root_log2 - 1


def main() -> None:
    started = time.perf_counter()

    php_rows = []
    for holes in (1, 2, 3):
        unsat, uvars = php_cnf(holes + 1, holes)
        sat, svars = php_cnf(holes, holes)
        unsat_models = count_cnf_models(unsat, uvars)
        sat_models = count_cnf_models(sat, svars)
        assert unsat_models == 0
        assert sat_models == math.factorial(holes)
        php_rows.append({
            "holes": holes,
            "unsat_pigeons": holes + 1,
            "unsat_variables": uvars,
            "unsat_clauses": len(unsat),
            "unsat_models": unsat_models,
            "paired_sat_pigeons": holes,
            "paired_sat_variables": svars,
            "paired_sat_models": sat_models,
        })

    tseitin = {
        "graph": "K4",
        "edges": len(k4_edges()),
        "even_charge_models": count_tseitin_models((0, 0, 0, 0)),
        "odd_charge_models": count_tseitin_models((1, 0, 0, 0)),
        "xor_rank_expectation": 3,
    }
    assert tseitin["even_charge_models"] == 8
    assert tseitin["odd_charge_models"] == 0

    valid = {
        "direction": "R_to_P",
        "proof_quantifier": "every_R_refutation",
        "same_source": True,
        "overhead": "polynomial_in_N_plus_R_cost",
        "C": 7,
        "d": 3,
    }
    ok, reason = validate_transfer_schema(valid)
    assert ok and reason == "accepted"

    malformed = [
        {**valid, "direction": "P_to_R"},
        {**valid, "proof_quantifier": "some_R_refutation"},
        {**valid, "proof_quantifier": "optimizer_output_only"},
        {**valid, "same_source": False},
        {**valid, "overhead": "unbounded_computable"},
        {**valid, "C": 0},
        {**valid, "d": 0},
        {**valid, "d": 1.5},
    ]
    malformed_rows = []
    for i, record in enumerate(malformed):
        accepted, why = validate_transfer_schema(record)
        assert not accepted
        malformed_rows.append({"case": i + 1, "rejection": why})

    # Synthetic arithmetic only: it checks the algebra without assigning Haken's
    # unspecified positive constant.  N_n is a conservative encoding proxy.
    arithmetic_rows = []
    for c in (1 / 8, 1 / 16):
        for d in (1, 2, 3, 4):
            first = None
            for n in range(16, 4097):
                N = math.ceil(n ** 3 * math.log2(n + 2))
                floor = derived_log2_floor(c * n, 7, d, N)
                if floor is not None:
                    first = {"n": n, "N_proxy": N, "certified_log2_floor": floor}
                    break
            arithmetic_rows.append({"synthetic_c": c, "d": d, "first_threshold": first})
    assert all(row["first_threshold"] is not None for row in arithmetic_rows)

    result = {
        "artifact": "FAMILY-LOCAL-BACKTRANSLATION-REFEREE316",
        "task_id": "6ad42a2a9a088191ab9042245f3b4393",
        "timestamp_pst": "2026-11-03 08:48",
        "theorem_schema": {
            "weakest_premise": "W_P(F_n)>=L(n) and W_P(F_n)<=C(N_n+W_R(F_n))^d",
            "convenient_sufficient_premise": "every R-refutation pi of the same F_n has a P-refutation rho with cost_P(rho)<=C(N_n+cost_R(pi))^d",
            "conclusion": "W_R(F_n)>=(W_P(F_n)/C)^(1/d)-N_n",
            "free_optimizer_search": True,
            "machine_translation_required": False,
            "scope": "family-local minimum-cost implication; not B1, B2, or B3",
        },
        "transfer_hierarchy": [
            "T0 direct minimum domination",
            "T1 existential projection of one minimum R-proof",
            "T2 existential projection of every R-proof",
            "T3 effective polynomial-time projection of every R-proof",
        ],
        "established_family_controls": php_rows,
        "mandatory_xor_control": tseitin,
        "valid_schema": valid,
        "malformed_schema_rejections": malformed_rows,
        "synthetic_arithmetic_sanity": arithmetic_rows,
        "classification": {
            "lemma": "PROVED",
            "Haken_to_Rmix341": "BLOCKED by polynomial ER/ER2 PHP proofs",
            "B1": "OPEN",
            "B2": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    result["measurements"] = {
        "python_wall_seconds": time.perf_counter() - started,
        "python_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "assertion_classes": 6,
        "php_assignments_enumerated": sum((1 << r["unsat_variables"]) + (1 << r["paired_sat_variables"]) for r in php_rows),
        "tseitin_assignments_enumerated": 2 * (1 << len(k4_edges())),
        "malformed_records_rejected": len(malformed_rows),
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(json.dumps({"raw": str(RAW), "sha256": digest, **result["measurements"]}, indent=2))


if __name__ == "__main__":
    main()
