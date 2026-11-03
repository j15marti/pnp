#!/usr/bin/env python3
"""REFEREE317: finite controls for the Cook--Reckhow-to-B3 transfer gap."""

from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path

RAW = Path("results/raw/arc/lspv5_317/cook_reckhow_b3_transfer_referee317.json")


def valid_formula(obj: object) -> bool:
    if not isinstance(obj, dict) or set(obj) != {"vars", "clauses"}:
        return False
    variables, clauses = obj["vars"], obj["clauses"]
    if not isinstance(variables, int) or isinstance(variables, bool) or variables < 1:
        return False
    if not isinstance(clauses, list) or not clauses:
        return False
    for clause in clauses:
        if not isinstance(clause, list) or not clause:
            return False
        seen: set[int] = set()
        for lit in clause:
            if not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > variables:
                return False
            if lit in seen:
                return False
            seen.add(lit)
    return True


def clause_false(clause: list[int], mask: int) -> bool:
    for lit in clause:
        value = bool(mask & (1 << (abs(lit) - 1)))
        if value if lit > 0 else not value:
            return False
    return True


def brute_label(formula: dict) -> str:
    if not valid_formula(formula):
        return "MALFORMED"
    for mask in range(1 << formula["vars"]):
        if all(not clause_false(clause, mask) for clause in formula["clauses"]):
            return "SAT"
    return "UNSAT"


def contradictory_units(variables: int) -> dict:
    clauses: list[list[int]] = []
    for variable in range(1, variables + 1):
        clauses.extend([[variable], [-variable]])
    return {"vars": variables, "clauses": clauses}


def paired_sat(variables: int) -> dict:
    return {"vars": variables, "clauses": [[variable] for variable in range(1, variables + 1)]}


def tt_proof(formula: dict) -> list[dict]:
    if brute_label(formula) != "UNSAT":
        raise ValueError("truth-table proof exists only for valid UNSAT")
    proof = []
    for mask in range(1 << formula["vars"]):
        clause_index = next(i for i, clause in enumerate(formula["clauses"]) if clause_false(clause, mask))
        proof.append({"assignment": mask, "falsified_clause": clause_index})
    return proof


def verify_tt(formula: object, proof: object) -> tuple[bool, str]:
    if not valid_formula(formula):
        return False, "malformed formula"
    assert isinstance(formula, dict)
    if not isinstance(proof, list):
        return False, "proof must be a list"
    expected = 1 << formula["vars"]
    if len(proof) != expected:
        return False, "record count must be exactly 2^vars"
    for mask, record in enumerate(proof):
        if not isinstance(record, dict) or set(record) != {"assignment", "falsified_clause"}:
            return False, "malformed record"
        if record["assignment"] != mask:
            return False, "assignments must be canonical and exhaustive"
        index = record["falsified_clause"]
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(formula["clauses"]):
            return False, "invalid clause index"
        if not clause_false(formula["clauses"][index], mask):
            return False, "cited clause is not false"
    return True, "accepted"


def verify_decider_copy(formula: object, proof_copy: object) -> tuple[bool, str]:
    """Finite stand-in for D_A: statement copy plus an exact decider."""
    if not valid_formula(formula):
        return False, "malformed formula"
    if proof_copy != formula:
        return False, "proof is not the exact statement copy"
    return (True, "accepted") if brute_label(formula) == "UNSAT" else (False, "decider says SAT")


def corruptions(formula: dict, proof: list[dict]) -> list[tuple[str, object, object]]:
    cases: list[tuple[str, object, object]] = []
    cases.append(("missing record", formula, proof[:-1]))
    p = json.loads(json.dumps(proof)); p[1]["assignment"] = 0; cases.append(("duplicate assignment", formula, p))
    p = json.loads(json.dumps(proof)); p[0]["assignment"] = 1; cases.append(("noncanonical first assignment", formula, p))
    p = json.loads(json.dumps(proof)); p[0]["falsified_clause"] = 999; cases.append(("bad clause index", formula, p))
    p = json.loads(json.dumps(proof)); p[0]["falsified_clause"] = 0 if not clause_false(formula["clauses"][0], 0) else 1; cases.append(("true cited clause", formula, p))
    p = json.loads(json.dumps(proof)); p[0]["extra"] = 0; cases.append(("extra record field", formula, p))
    cases.append(("proof not list", formula, {"records": proof}))
    malformed = {"vars": formula["vars"], "clauses": [[0]]}; cases.append(("zero literal", malformed, proof))
    malformed = {"vars": formula["vars"], "clauses": [[formula["vars"] + 1]]}; cases.append(("out of range literal", malformed, proof))
    malformed = {"vars": formula["vars"], "clauses": []}; cases.append(("empty clause collection", malformed, proof))
    return cases


def main() -> None:
    started = time.perf_counter()
    rows = []
    total_tt_records = 0
    for variables in range(1, 13):
        unsat = contradictory_units(variables)
        sat = paired_sat(variables)
        assert brute_label(unsat) == "UNSAT"
        assert brute_label(sat) == "SAT"
        proof = tt_proof(unsat)
        ok, why = verify_tt(unsat, proof)
        assert ok and why == "accepted"
        sat_ok, _ = verify_tt(sat, proof)
        assert not sat_ok
        da_ok, _ = verify_decider_copy(unsat, json.loads(json.dumps(unsat)))
        da_sat, _ = verify_decider_copy(sat, json.loads(json.dumps(sat)))
        assert da_ok and not da_sat
        total_tt_records += len(proof)
        encoded = json.dumps(unsat, separators=(",", ":"), sort_keys=True)
        rows.append({
            "variables": variables,
            "formula_bytes": len(encoded.encode()),
            "tt_paid_records": len(proof),
            "decider_copy_bytes": len(encoded.encode()),
            "unsat_label": "UNSAT",
            "paired_label": "SAT",
        })

    base_formula = contradictory_units(4)
    base_proof = tt_proof(base_formula)
    rejected = []
    for name, formula, proof in corruptions(base_formula, base_proof):
        accepted, reason = verify_tt(formula, proof)
        assert not accepted
        rejected.append({"name": name, "reason": reason})

    da_corruptions = [
        ("changed copy", base_formula, paired_sat(4)),
        ("missing copy", base_formula, None),
        ("malformed statement", {"vars": 1, "clauses": [[0]]}, {"vars": 1, "clauses": [[0]]}),
    ]
    da_rejected = []
    for name, statement, copy in da_corruptions:
        accepted, reason = verify_decider_copy(statement, copy)
        assert not accepted
        da_rejected.append({"name": name, "reason": reason})

    result = {
        "artifact": "COOK-RECKHOW-B3-TRANSFER-REFEREE317",
        "task_id": "6ad42a2a9a088191ab9042245f3b4393",
        "timestamp_pst": "2026-11-03 09:48",
        "exact_statement": {
            "cook_reckhow": "A polynomially bounded propositional proof system exists iff NP=coNP.",
            "decider_system": "If A is a total correct P-time SAT decider, D_A uses a statement-copy proof and verifies validity plus A(F)=UNSAT.",
            "weakest_B3_transfer": "R length-simulates D_A: every valid UNSAT F has W_R(F)<=poly(|F|+|proof_DA(F)|).",
            "effective_p_simulation": "strictly stronger; it must compute the R proof in polynomial time",
        },
        "truth_table_countercontrol": {
            "rule": "one paid record for every assignment, citing an original clause falsified there",
            "sound_complete_effective": True,
            "minimum_records": "2^v by syntax",
            "purpose": "soundness, completeness, and effective checking alone do not imply polynomial boundedness",
        },
        "controls": rows,
        "malformed_tt_rejections": rejected,
        "malformed_decider_rejections": da_rejected,
        "classification": {
            "equivalence_under_fixed_correct_A": "PROVED",
            "completeness_implies_polynomial_bound": "FALSIFIED",
            "B1_Rmix341": "OPEN",
            "B2_Rmix341": "OPEN",
            "B3_Rmix341": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    result["measurements"] = {
        "python_wall_seconds": time.perf_counter() - started,
        "python_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "truth_table_records_verified": total_tt_records,
        "malformed_records_rejected": len(rejected) + len(da_rejected),
        "largest_truth_table_records": rows[-1]["tt_paid_records"],
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(json.dumps({"raw": str(RAW), "sha256": digest, **result["measurements"]}, indent=2))


if __name__ == "__main__":
    main()
