#!/usr/bin/env python3
"""REFEREE380: source-authenticated positive-guard lifting for FACET-A.

This transforms the complete REFEREE379 strict-3 bit-PHP refutation into a
derivation of the guard unit from the LSPV-1/434 proper-3 guard.  It is a
declared FACET-A trace, not an execution of the historical R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "experiments/review/lspv5_379_full_cook_facet_a.py"
OUT = ROOT / "results/raw/review/2026-11-05_2352_LSPV5_GUARD_LIFT_FACETA380.json"

spec = importlib.util.spec_from_file_location("ref379", BASE_PATH)
ref379 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ref379)


def norm(clause):
    return sorted(set(clause), key=lambda x: (abs(x), 0 if x < 0 else 1))


def dimacs_text(vmax, clauses):
    return "p cnf %d %d\n%s\n" % (
        vmax, len(clauses), "\n".join(" ".join(map(str, c)) + " 0" for c in clauses)
    )


def guarded_trace(ell: int):
    base = ref379.FullCook(ell).finish()
    old_v = base["source_variables"]
    old_final = base["final_variables_after_def"]
    sources = base["trace"]["sources"]
    s_count = len(sources)
    guard = old_v + 1
    shift = s_count + 1
    new_source_v = old_v + shift

    def ren_lit(lit):
        sign = -1 if lit < 0 else 1
        v = abs(lit)
        return sign * (v if v <= old_v else v + shift)

    guarded_sources = []
    guard_nodes = []
    recovered = []
    for pos, src in enumerate(sources, start=1):
        a, b, c = src["clause"]
        y = old_v + 1 + pos
        left = norm([guard, a, y])
        right = norm([-y, b, c])
        guarded_sources.extend([
            {"id": f"GS{2 * pos - 1}", "clause": left},
            {"id": f"GS{2 * pos}", "clause": right},
        ])
        guard_nodes.append({
            "id": f"G_R{pos}", "kind": "res",
            "left": f"GS{2 * pos - 1}", "right": f"GS{2 * pos}", "pivot": y,
        })
        recovered.append(norm([guard, a, b, c]))

    lifted = []
    for node in base["trace"]["nodes"]:
        if node["kind"] == "def":
            out = {
                "id": node["id"], "kind": "def", "out": ren_lit(node["out"]),
                "a": ren_lit(node["a"]), "b": ren_lit(node["b"]),
            }
            if "parent_owner" in node:
                out["parent_owner"] = node["parent_owner"]
            if "input_owners" in node:
                out["input_owners"] = node["input_owners"]
            lifted.append(out)
        else:
            def ren_ref(ref):
                if ref.startswith("S") and ref[1:].isdigit():
                    return f"G_R{int(ref[1:])}"
                return ref

            lifted.append({
                "id": node["id"], "kind": "res",
                "left": ren_ref(node["left"]), "right": ren_ref(node["right"]),
                "pivot": ren_lit(node["pivot"]),
            })

    clauses = [s["clause"] for s in guarded_sources]
    dimacs = dimacs_text(new_source_v, clauses)
    n = 2**ell
    m_pairs = n * ((n + 1) * n // 2)
    expected_sources = m_pairs * (2 * ell - 2)
    assert s_count == expected_sources
    cook = n * (n + 1) * (27 * n**2 + 11 * n - 14) // 24
    old_formula = m_pairs * (4 * ell - 3) + (n + 1) * (2 * n * ell - 9) + cook
    assert base["paid_full_refutation_work"] == old_formula
    work_formula = old_formula + s_count
    span_formula = base["critical_path_full"] + 1

    return {
        "grammar": "FACET-A380-v1: guarded proper-3 sources, fresh signed-AND2 DEF facets, oriented RES",
        "ell": ell,
        "holes": n,
        "pigeons": n + 1,
        "old_source_variables": old_v,
        "old_final_variables": old_final,
        "old_source_clauses": s_count,
        "old_source_sha256": base["source_sha256"],
        "guard_variable": guard,
        "auxiliary_shift": shift,
        "source_variables": new_source_v,
        "final_variables_after_def": old_final + shift,
        "strict3_guarded_source_clauses": len(guarded_sources),
        "all_rule_binary_premise_source_floor": 2 * s_count - 1,
        "source_sha256": hashlib.sha256(dimacs.encode()).hexdigest(),
        "source_bytes": len(dimacs.encode()),
        "dimacs": dimacs,
        "base_refutation_work": base["paid_full_refutation_work"],
        "guard_recovery_res": s_count,
        "paid_guarded_unit_work": work_formula,
        "paid_guarded_unit_formula": work_formula,
        "critical_path_guarded_unit": span_formula,
        "critical_path_formula": span_formula,
        "final_guard_unit": base["final_empty"],
        "recovered_guarded_clauses": recovered,
        "trace": {"sources": guarded_sources, "nodes": guard_nodes + lifted},
    }


def main():
    traces = [guarded_trace(ell) for ell in (2, 3)]
    out = {
        "run": "LSPV-5/REFEREE380",
        "timestamp_PST": "2026-11-05 23:52",
        "status": "PROVED/RESTRICTED FACET-A guard lifting; COMPUTATIONAL complete finite unit traces",
        "historical_authoritative_checker": False,
        "target_is_refutation": False,
        "target": "derive the positive guard unit from a satisfiable guarded source",
        "traces": traces,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    summary = [{
        "ell": t["ell"], "guarded_sources": t["strict3_guarded_source_clauses"],
        "source_variables": t["source_variables"],
        "final_variables": t["final_variables_after_def"],
        "work": t["paid_guarded_unit_work"], "span": t["critical_path_guarded_unit"],
        "final": t["final_guard_unit"],
    } for t in traces]
    print(json.dumps({"run": out["run"], "traces": summary}, indent=2))


if __name__ == "__main__":
    main()
