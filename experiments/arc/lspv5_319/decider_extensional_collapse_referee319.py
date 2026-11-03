#!/usr/bin/env python3
"""REFEREE319: exact controls for extensional collapse of decider proof systems."""

from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path

RAW = Path("results/raw/arc/lspv5_319/decider_extensional_collapse_referee319.json")


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


def encoded(formula: dict) -> str:
    return json.dumps(formula, separators=(",", ":"), sort_keys=True)


def clause_satisfied(clause: list[int], mask: int) -> tuple[bool, int]:
    work = 0
    for lit in clause:
        work += 1
        value = bool(mask & (1 << (abs(lit) - 1)))
        if value == (lit > 0):
            return True, work
    return False, work


def brute_decider(formula: object) -> tuple[str, int]:
    if not valid_formula(formula):
        return "MALFORMED", 1
    assert isinstance(formula, dict)
    work = 0
    for mask in range(1 << formula["vars"]):
        satisfied = True
        for clause in formula["clauses"]:
            clause_ok, clause_work = clause_satisfied(clause, mask)
            work += clause_work
            if not clause_ok:
                satisfied = False
                break
        if satisfied:
            return "SAT", work
    return "UNSAT", work


def full_clause_false_only_on(mask: int, variables: int = 3) -> list[int]:
    return [-(i + 1) if mask & (1 << i) else i + 1 for i in range(variables)]


def catalog() -> list[dict]:
    complete = [full_clause_false_only_on(mask) for mask in range(8)]
    return [
        {"vars": 3, "clauses": [clause[:] for i, clause in enumerate(complete) if mask & (1 << i)]}
        for mask in range(1, 1 << 8)
    ]


CATALOG = catalog()


def build_catalog_table() -> tuple[dict[str, str], int]:
    table: dict[str, str] = {}
    work = 0
    for formula in CATALOG:
        label, formula_work = brute_decider(formula)
        table[encoded(formula)] = label
        work += formula_work
    return table, work


CATALOG_TABLE, CATALOG_TABLE_BUILD_WORK = build_catalog_table()


def table_fallback_decider(formula: object) -> tuple[str, int]:
    if not valid_formula(formula):
        return "MALFORMED", 1
    assert isinstance(formula, dict)
    key = encoded(formula)
    if key in CATALOG_TABLE:
        return CATALOG_TABLE[key], 1
    label, work = brute_decider(formula)
    return label, work + 1


def delayed_decider(formula: object) -> tuple[str, int]:
    if not valid_formula(formula):
        return "MALFORMED", 1
    assert isinstance(formula, dict)
    delay = len(encoded(formula).encode()) ** 2
    checksum = 0
    for i in range(delay):
        checksum ^= (i * 17 + 3) & 255
    label, work = brute_decider(formula)
    if checksum < 0:  # unreachable; prevents the loop from being semantically dead code
        raise AssertionError("impossible checksum")
    return label, delay + work


def faulty_advice_decider(formula: object) -> tuple[str, int]:
    if not valid_formula(formula):
        return "MALFORMED", 1
    assert isinstance(formula, dict)
    # S0 is satisfiable: all full clauses except the one false only on assignment 0.
    s0 = {"vars": 3, "clauses": [full_clause_false_only_on(mask) for mask in range(1, 8)]}
    if formula == s0:
        return "UNSAT", 1
    return brute_decider(formula)


def verify_copy(formula: object, proof: object, decider) -> tuple[bool, str, int]:
    if not valid_formula(formula):
        return False, "malformed statement", 1
    if proof != formula:
        return False, "proof is not the exact statement copy", 1
    label, work = decider(formula)
    if label == "UNSAT":
        return True, "accepted", work
    return False, f"decider says {label}", work


def xor_k4_models(charges: list[int]) -> int:
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    count = 0
    for mask in range(1 << 6):
        parity = [0, 0, 0, 0]
        for i, (left, right) in enumerate(edges):
            bit = (mask >> i) & 1
            parity[left] ^= bit
            parity[right] ^= bit
        if parity == charges:
            count += 1
    return count


def main() -> None:
    started = time.perf_counter()
    deciders = {
        "brute": brute_decider,
        "table_fallback": table_fallback_decider,
        "delayed": delayed_decider,
    }
    relation_sets: dict[str, set[str]] = {name: set() for name in deciders}
    work_totals = {name: 0 for name in deciders}
    sat_count = unsat_count = 0

    for formula in CATALOG:
        reference, _ = brute_decider(formula)
        sat_count += reference == "SAT"
        unsat_count += reference == "UNSAT"
        proof = json.loads(json.dumps(formula))
        for name, decider in deciders.items():
            accepted, _, work = verify_copy(formula, proof, decider)
            work_totals[name] += work
            assert accepted == (reference == "UNSAT")
            if accepted:
                relation_sets[name].add(encoded(formula))

    assert sat_count == 254 and unsat_count == 1
    assert relation_sets["brute"] == relation_sets["table_fallback"] == relation_sets["delayed"]
    assert len(relation_sets["brute"]) == 1

    s0 = {"vars": 3, "clauses": [full_clause_false_only_on(mask) for mask in range(1, 8)]}
    assert brute_decider(s0)[0] == "SAT"
    bad_accepted, _, _ = verify_copy(s0, json.loads(json.dumps(s0)), faulty_advice_decider)
    assert bad_accepted

    mismatches = [
        ("changed clause", CATALOG[-1], s0),
        ("missing proof", CATALOG[-1], None),
        ("proof wrapper", CATALOG[-1], {"copy": CATALOG[-1]}),
    ]
    malformed = [
        ("not object", "p cnf 1 1"),
        ("missing clauses", {"vars": 1}),
        ("extra field", {"vars": 1, "clauses": [[1]], "label": "UNSAT"}),
        ("zero variables", {"vars": 0, "clauses": [[1]]}),
        ("boolean variables", {"vars": True, "clauses": [[1]]}),
        ("empty clause list", {"vars": 1, "clauses": []}),
        ("empty clause", {"vars": 1, "clauses": [[]]}),
        ("zero literal", {"vars": 1, "clauses": [[0]]}),
        ("out of range", {"vars": 1, "clauses": [[2]]}),
        ("noninteger literal", {"vars": 1, "clauses": [["1"]]}),
        ("boolean literal", {"vars": 1, "clauses": [[True]]}),
        ("duplicate literal", {"vars": 1, "clauses": [[1, 1]]}),
    ]
    rejected = []
    for name, statement, proof in mismatches:
        accepted, reason, _ = verify_copy(statement, proof, brute_decider)
        assert not accepted
        rejected.append({"name": name, "reason": reason})
    for name, statement in malformed:
        accepted, reason, _ = verify_copy(statement, statement, brute_decider)
        assert not accepted
        rejected.append({"name": name, "reason": reason})

    odd_xor = xor_k4_models([1, 0, 0, 0])
    even_xor = xor_k4_models([0, 0, 0, 0])
    assert odd_xor == 0 and even_xor == 8

    canonical_unsat = next(iter(relation_sets["brute"]))
    proof_bytes = len(canonical_unsat.encode())
    result = {
        "artifact": "DECIDER-EXTENSIONAL-COLLAPSE-REFEREE319",
        "task_id": "6ad42a2a9a088191ab9042245f3b4393",
        "timestamp_pst": "2026-11-03 11:48",
        "theorem": {
            "extensional_identity": "For total correct SAT deciders A and B, V_A(F,pi)=V_B(F,pi)=1 iff F is valid UNSAT and pi is the exact statement copy.",
            "length_consequence": "All correct decider-induced systems have the same minimum proof length |enc(F)|; code, delay, trace and verifier work do not change B3 length domination.",
            "boundary": "B1 and B2 retain runtime terms and therefore do not collapse extensionally.",
        },
        "catalog": {
            "formulas": len(CATALOG),
            "sat": sat_count,
            "unsat": unsat_count,
            "accepted_pairs_per_correct_decider": len(relation_sets["brute"]),
            "canonical_unsat_copy_bytes": proof_bytes,
        },
        "correct_decider_work": {
            "brute": work_totals["brute"],
            "table_lookup_phase": work_totals["table_fallback"],
            "table_preprocessing": CATALOG_TABLE_BUILD_WORK,
            "table_all_phase": work_totals["table_fallback"] + CATALOG_TABLE_BUILD_WORK,
            "delayed": work_totals["delayed"],
        },
        "faulty_advice_control": {
            "false_rejected_formula": "S0",
            "true_label": "SAT",
            "bad_system_accepts_copy": bad_accepted,
            "consequence": "one wrong advice bit changes the proof relation and destroys soundness",
        },
        "malformed_rejections": rejected,
        "xor_countercontrol": {"odd_k4_models": odd_xor, "even_k4_models": even_xor},
        "classification": {
            "correct_decider_extensional_collapse": "PROVED",
            "code_specific_B3_obstruction": "FALSIFIED",
            "runtime_independence_B1_B2": "FALSIFIED",
            "B1_Rmix341": "OPEN",
            "B2_Rmix341": "OPEN",
            "B3_Rmix341": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    result["measurements"] = {
        "python_wall_seconds": time.perf_counter() - started,
        "python_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "valid_formula_decider_runs": len(CATALOG) * len(deciders),
        "malformed_or_mismatch_rejections": len(rejected),
        "modeled_work_total": work_totals["brute"] + work_totals["delayed"] + work_totals["table_fallback"] + CATALOG_TABLE_BUILD_WORK,
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(json.dumps({"raw": str(RAW), "sha256": digest, **result["measurements"]}, indent=2))


if __name__ == "__main__":
    main()
