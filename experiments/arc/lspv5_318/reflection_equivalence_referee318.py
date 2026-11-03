#!/usr/bin/env python3
"""REFEREE318: reflection-family transfer and exact restriction controls.

This is a finite control for the transfer theorem, not an asymptotic lower bound.
"""

from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path

RAW = Path("results/raw/arc/lspv5_318/reflection_equivalence_referee318.json")


def full_clause_false_only_on(mask: int, variables: int = 3) -> list[int]:
    return [-(i + 1) if mask & (1 << i) else i + 1 for i in range(variables)]


def catalog() -> list[dict]:
    complete = [full_clause_false_only_on(mask) for mask in range(8)]
    formulas = [{"name": "U8", "vars": 3, "clauses": complete}]
    for removed in range(8):
        formulas.append({
            "name": f"S{removed}",
            "vars": 3,
            "clauses": [clause for i, clause in enumerate(complete) if i != removed],
        })
    return formulas


def valid_formula(formula: object) -> bool:
    if not isinstance(formula, dict) or set(formula) != {"name", "vars", "clauses"}:
        return False
    if formula["vars"] != 3 or not isinstance(formula["clauses"], list):
        return False
    for clause in formula["clauses"]:
        if not isinstance(clause, list) or not clause:
            return False
        if any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > 3 for lit in clause):
            return False
        if len(set(clause)) != len(clause):
            return False
    return True


def clause_satisfied(clause: list[int], mask: int) -> bool:
    return any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0) for lit in clause)


def models(formula: dict) -> list[int]:
    return [mask for mask in range(8) if all(clause_satisfied(c, mask) for c in formula["clauses"])]


def build_reflection(labels: list[str]) -> dict:
    """CNF for a false rejection: choose F with label UNSAT and satisfy F.

    Selector variables are 4..12; source variables remain 1..3.
    A SAT label contributes the unit not-selector. An UNSAT label contributes
    selector-gated source clauses. Thus the CNF is UNSAT iff no rejected
    catalog formula has a satisfying assignment.
    """
    cats = catalog()
    if len(labels) != len(cats) or any(label not in {"SAT", "UNSAT"} for label in labels):
        raise ValueError("labels must be nine SAT/UNSAT strings")
    selectors = [4 + i for i in range(len(cats))]
    clauses: list[list[int]] = [selectors[:]]
    for i, left in enumerate(selectors):
        for right in selectors[i + 1:]:
            clauses.append([-left, -right])
    for selector, formula, label in zip(selectors, cats, labels):
        if label == "SAT":
            clauses.append([-selector])
        else:
            clauses.extend([[-selector, *clause] for clause in formula["clauses"]])
    return {"vars": 12, "clauses": clauses, "selectors": selectors}


def cnf_models(cnf: dict) -> list[int]:
    found = []
    for mask in range(1 << cnf["vars"]):
        if all(clause_satisfied(c, mask) for c in cnf["clauses"]):
            found.append(mask)
    return found


def simplify_clause(clause: list[int], assignment: dict[int, bool]) -> list[int] | None:
    residual = []
    for lit in clause:
        variable = abs(lit)
        if variable not in assignment:
            residual.append(lit)
        elif assignment[variable] == (lit > 0):
            return None
    return residual


def specialize(cnf: dict, selected: int) -> list[list[int]]:
    assignment = {selector: i == selected for i, selector in enumerate(cnf["selectors"])}
    residual = []
    for clause in cnf["clauses"]:
        simplified = simplify_clause(clause, assignment)
        if simplified is not None and simplified not in residual:
            residual.append(simplified)
    return residual


def canonical(clause: list[int]) -> tuple[int, ...]:
    return tuple(sorted(set(clause), key=lambda lit: (abs(lit), lit < 0)))


def resolve(left: list[int], right: list[int], pivot: int) -> list[int]:
    if pivot not in left or -pivot not in right:
        if -pivot in left and pivot in right:
            left, right = right, left
        else:
            raise ValueError("pivot absent with opposite polarities")
    result = [lit for lit in left if lit != pivot] + [lit for lit in right if lit != -pivot]
    if any(-lit in result for lit in result):
        raise ValueError("tautological resolvent")
    return list(canonical(result))


def gated_u_resolution_proof(selector: int = 4) -> list[dict]:
    """Seven-node refutation of U8, with not-selector carried throughout."""
    current = [[-selector, *full_clause_false_only_on(mask)] for mask in range(8)]
    proof: list[dict] = []
    for pivot in (3, 2, 1):
        nxt = []
        used: set[int] = set()
        for i, left in enumerate(current):
            if i in used:
                continue
            mate = next(
                j
                for j, right in enumerate(current)
                if j not in used
                and j != i
                and (
                    (pivot in left and -pivot in right)
                    or (-pivot in left and pivot in right)
                )
            )
            right = current[mate]
            used.update({i, mate})
            child = resolve(left, right, pivot)
            proof.append({"pivot": pivot, "left": left, "right": right, "child": child})
            nxt.append(child)
        current = nxt
    assert current == [[-selector]] and len(proof) == 7
    return proof


def theorem_schema_ok(schema: object) -> tuple[bool, str]:
    required = {
        "fixed_R", "correct_total_poly_A", "poly_size_H", "H_unsat",
        "covers_every_unsat_length_le_N", "exact_source_specialization",
        "restriction_cost_nonincreasing", "poly_encoding_rescaling",
    }
    if not isinstance(schema, dict) or set(schema) != required:
        return False, "wrong schema fields"
    if any(type(schema[key]) is not bool for key in required):
        return False, "schema fields must be booleans"
    false = [key for key in required if not schema[key]]
    return (not false, "accepted" if not false else f"missing {false[0]}")


def xor_k4_models(charges: list[int]) -> int:
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    count = 0
    for mask in range(1 << len(edges)):
        parity = [0, 0, 0, 0]
        for i, (u, v) in enumerate(edges):
            bit = (mask >> i) & 1
            parity[u] ^= bit
            parity[v] ^= bit
        if parity == charges:
            count += 1
    return count


def main() -> None:
    started = time.perf_counter()
    cats = catalog()
    counts = [len(models(formula)) for formula in cats]
    assert counts == [0] + [1] * 8

    good_labels = ["UNSAT"] + ["SAT"] * 8
    bad_labels = good_labels[:]
    bad_labels[1] = "UNSAT"
    good = build_reflection(good_labels)
    bad = build_reflection(bad_labels)
    good_models = cnf_models(good)
    bad_models = cnf_models(bad)
    assert good_models == []
    assert len(bad_models) == 1
    bad_model = bad_models[0]
    assert bool(bad_model & (1 << (good["selectors"][1] - 1)))
    assert bad_model & 7 == 0

    specialized_u = specialize(good, 0)
    expected_u = [list(canonical(c)) for c in cats[0]["clauses"]]
    assert sorted(map(canonical, specialized_u)) == sorted(map(canonical, expected_u))

    gated_proof = gated_u_resolution_proof(good["selectors"][0])
    restricted_proof = []
    assignment = {selector: i == 0 for i, selector in enumerate(good["selectors"])}
    for node in gated_proof:
        left = simplify_clause(node["left"], assignment)
        right = simplify_clause(node["right"], assignment)
        child = simplify_clause(node["child"], assignment)
        assert left is not None and right is not None and child is not None
        assert resolve(left, right, node["pivot"]) == child
        restricted_proof.append({"pivot": node["pivot"], "left": left, "right": right, "child": child})
    assert restricted_proof[-1]["child"] == [] and len(restricted_proof) == 7

    full_good_proof_cost = len(gated_proof) + 9
    assert full_good_proof_cost == 16

    schema = {
        "fixed_R": True,
        "correct_total_poly_A": True,
        "poly_size_H": True,
        "H_unsat": True,
        "covers_every_unsat_length_le_N": True,
        "exact_source_specialization": True,
        "restriction_cost_nonincreasing": True,
        "poly_encoding_rescaling": True,
    }
    ok, _ = theorem_schema_ok(schema)
    assert ok
    schema_rejections = []
    for key in schema:
        bad_schema = schema | {key: False}
        accepted, reason = theorem_schema_ok(bad_schema)
        assert not accepted
        schema_rejections.append({"name": f"false {key}", "reason": reason})
    malformed_schemas = [
        ("missing field", {key: value for key, value in schema.items() if key != "fixed_R"}),
        ("extra field", schema | {"free_correctness_axiom": True}),
        ("nonboolean", schema | {"correct_total_poly_A": "assumed"}),
    ]
    for name, candidate in malformed_schemas:
        accepted, reason = theorem_schema_ok(candidate)
        assert not accepted
        schema_rejections.append({"name": name, "reason": reason})

    label_rejections = []
    for name, labels in [
        ("missing label", good_labels[:-1]),
        ("extra label", good_labels + ["SAT"]),
        ("nonsemantic label", good_labels[:1] + ["MAYBE"] + good_labels[2:]),
        ("nonstring label", good_labels[:1] + [1] + good_labels[2:]),
    ]:
        try:
            build_reflection(labels)
        except ValueError as error:
            label_rejections.append({"name": name, "reason": str(error)})
        else:
            raise AssertionError(f"accepted malformed labels: {name}")

    odd_xor = xor_k4_models([1, 0, 0, 0])
    even_xor = xor_k4_models([0, 0, 0, 0])
    assert odd_xor == 0 and even_xor == 8

    result = {
        "artifact": "REFLECTION-EQUIVALENCE-REFEREE318",
        "task_id": "6ad42a2a9a088191ab9042245f3b4393",
        "timestamp_pst": "2026-11-03 10:48",
        "theorem": {
            "forward": "If every UNSAT F of length <=N is an exact restriction of H_N and R-restriction never increases cost, then Wbar_R(N)<=W_R(H_N).",
            "reverse": "If |H_N|<=poly(N) and Wbar_R is polynomial, then W_R(H_N)<=Wbar_R(|H_N|)<=poly(N).",
            "conclusion": "For a witness-transparent polynomial reflection family, polynomial H_N proofs are equivalent up to polynomial rescaling to B3's conclusion; correctness alone does not yield them.",
        },
        "catalog": [{"name": formula["name"], "models": count} for formula, count in zip(cats, counts)],
        "reflection_controls": {
            "good_decider_models": len(good_models),
            "bad_decider_models": len(bad_models),
            "bad_model_selector": "S0",
            "bad_model_source_assignment": bad_model & 7,
            "good_cnf_clauses": len(good["clauses"]),
            "bad_cnf_clauses": len(bad["clauses"]),
            "exact_U8_specialization_clauses": len(specialized_u),
            "explicit_good_resolution_upper_bound": full_good_proof_cost,
            "restricted_U8_resolution_nodes": len(restricted_proof),
        },
        "xor_countercontrol": {"odd_k4_models": odd_xor, "even_k4_models": even_xor},
        "schema_rejections": schema_rejections,
        "label_rejections": label_rejections,
        "classification": {
            "abstract_reflection_equivalence": "PROVED",
            "strict_resolution_application": "PROVED_RESTRICTED",
            "Rmix341_restriction_closure": "OPEN",
            "generic_clocked_reflection_source_exactness": "OPEN_NOT_AUTOMATIC",
            "correctness_implies_short_reflection_proofs": "FALSIFIED",
            "B1_Rmix341": "OPEN",
            "B2_Rmix341": "OPEN",
            "B3_Rmix341": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    result["measurements"] = {
        "python_wall_seconds": time.perf_counter() - started,
        "python_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "assignments_checked": (1 << good["vars"]) + (1 << bad["vars"]) + 9 * 8 + 2 * 64,
        "resolution_nodes_checked": len(gated_proof) + len(restricted_proof),
        "malformed_controls_rejected": len(schema_rejections) + len(label_rejections),
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(json.dumps({"raw": str(RAW), "sha256": digest, **result["measurements"]}, indent=2))


if __name__ == "__main__":
    main()
