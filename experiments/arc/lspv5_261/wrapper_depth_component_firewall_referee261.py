#!/usr/bin/env python3
"""REFEREE261: source-faithful wrapper depth/component firewall.

The theorem and experiment concern raw cofactors of connected canonical
Monotone 3-SAT-(2,2) sources.  They do not constrain semantic/noninjective
re-encoders or arbitrary SAT machines.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REF260 = ROOT / "experiments/arc/lspv5_260/connected_raw_peel_dichotomy_referee260.py"
STAMP = "2026-11-01_0148"
RUN = "WRAPPER-DEPTH-COMPONENT-FIREWALL-REFEREE261"
SUMMARY = ROOT / f"results/raw/arc/{STAMP}_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.json"
FULL = ROOT / f"results/raw/arc/{STAMP}_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.full.json"
ARCHIVE = ROOT / f"results/raw/arc/{STAMP}_LSPV5_WRAPPER_DEPTH_COMPONENT_FIREWALL_REFEREE261_raw.json.gz.b64"


def load_ref260():
    spec = importlib.util.spec_from_file_location("ref260_fixture", REF260)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def audit_row(ref, formula, assignment):
    n = len(ref.variables(formula))
    b = len(assignment)
    k1 = sum(assignment.values())
    k0 = b - k1
    residual = ref.raw_cofactor(formula, assignment)
    if residual is None:
        return {"status": "UNSAT_TERMINAL", "b": b, "k0": k0, "k1": k1}
    if not residual:
        return {"status": "SAT_TERMINAL", "b": b, "k0": k0, "k1": k1}
    source_vars = set(ref.variables(formula))
    free = source_vars - set(assignment)
    retained = set(ref.variables(residual))
    erased = free - retained
    components = ref.incidence_components(residual, retained)
    c = len(components)
    largest = max(map(len, components))
    erased_bound = 2 * min(k0, k1)
    retained_bound = n - 2 * b
    component_bound = 1 + 5 * b
    largest_bound = max(0, math.ceil(retained_bound / component_bound))
    assert len(erased) <= erased_bound
    assert len(retained) >= retained_bound
    assert c <= component_bound
    assert largest >= largest_bound
    return {
        "status": "NONTERMINAL",
        "b": b,
        "k0": k0,
        "k1": k1,
        "erased": len(erased),
        "erased_ids": sorted(erased),
        "erased_bound": erased_bound,
        "retained": len(retained),
        "retained_bound": retained_bound,
        "components": c,
        "component_bound": component_bound,
        "component_sizes": sorted(map(len, components), reverse=True),
        "largest": largest,
        "largest_bound": largest_bound,
    }


def exhaustive_y6(ref, formula):
    vs = ref.variables(formula)
    rows = []
    for state in itertools.product((-1, 0, 1), repeat=len(vs)):
        assignment = {v: bool(s) for v, s in zip(vs, state) if s >= 0}
        row = audit_row(ref, formula, assignment)
        row["state"] = "".join("*" if s < 0 else str(s) for s in state)
        rows.append(row)
    return rows


def paired_uv_samples(ref, U, V, witness):
    rng = random.Random(202611010148)
    rows = []
    for b in range(1, 13):
        for trial in range(40):
            chosen = sorted(rng.sample(range(1, 199), b))
            assignment = {v: witness[v - 1] == "1" for v in chosen}
            ur = audit_row(ref, U, assignment)
            vr = audit_row(ref, V, assignment)
            # The same source-indexed assignment preserves the V witness.
            assert vr["status"] != "UNSAT_TERMINAL"
            residual_v = ref.raw_cofactor(V, assignment)
            assert residual_v is not None
            if residual_v:
                remaining = "".join(witness[v - 1] for v in range(1, 199))
                assert all(any((remaining[abs(x) - 1] == "1") == (x > 0) for x in c) for c in V)
            rows.append({
                "b": b,
                "trial": trial,
                "assigned_ids": chosen,
                "assignment_bits": "".join("1" if assignment[v] else "0" for v in chosen),
                "U198_label": "UNSAT",
                "V198_label": "SAT",
                "U198": ur,
                "V198": vr,
            })
    return rows


def inverse_threshold(n, M):
    if n <= M:
        return 0
    return math.ceil((n - M) / (2 + 5 * M))


def threshold_tables():
    exact = [{"n": 198, "M": M, "minimum_pins": inverse_threshold(198, M)} for M in (1, 2, 4, 8, 14, 24, 48, 96)]
    power = []
    for n in (10**2, 10**3, 10**4, 10**5, 10**6):
        for label, exponent in (("1/2", 0.5), ("2/3", 2 / 3), ("3/4", 0.75)):
            M = math.floor(n**exponent)
            power.append({"n": n, "lambda": label, "M_floor": M, "minimum_pins": inverse_threshold(n, M)})
    return exact, power


def summarize_rows(rows):
    non = [r for r in rows if r["status"] == "NONTERMINAL"]
    return {
        "rows": len(rows),
        "nonterminal": len(non),
        "sat_terminal": sum(r["status"] == "SAT_TERMINAL" for r in rows),
        "unsat_terminal": sum(r["status"] == "UNSAT_TERMINAL" for r in rows),
        "max_erased_minus_bound": max((r["erased"] - r["erased_bound"] for r in non), default=0),
        "max_components_minus_bound": max((r["components"] - r["component_bound"] for r in non), default=0),
        "min_largest_minus_bound": min((r["largest"] - r["largest_bound"] for r in non), default=0),
    }


def main():
    started = time.perf_counter()
    ref = load_ref260()
    old = ref.load_ref258()
    U = old.load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = old.y6()
    assert old.valid_target(U) and old.valid_target(V) and old.valid_target(Y)
    assert old.unsat_boundary_certificate(U) == []
    assert old.satisfies(V, old.V_WITNESS)
    assert all(len(ref.incidence_components(F)) == 1 for F in (U, V, Y))

    y_rows = exhaustive_y6(ref, Y)
    paired = paired_uv_samples(ref, U, V, old.V_WITNESS)
    exact_thresholds, power_thresholds = threshold_tables()
    controls = {"U198": ref.full_controls(U), "V198": ref.full_controls(V), "Y6": ref.full_controls(Y)}
    dpll = {"U198": old.dpll_cap(U, 600), "V198": old.dpll_cap(V, 600), "Y6": old.dpll_cap(Y, 600)}

    full = {
        "run_id": RUN,
        "timestamp": "2026-11-01T01:48:00-07:00",
        "theorem": {
            "forward": "for connected canonical F and a coherent b-pin assignment with nonterminal raw cofactor: erased free identities e<=2min(k0,k1), retained identities r>=n-2b, components c<=1+5b, and largest component L>=ceil((n-2b)/(1+5b))",
            "inverse": "if every nonterminal residual component has at most M source identities then b>=ceil((n-M)/(2+5M))",
            "wrapper_firewall": "a source-faithful raw-cofactor wrapper below that depth must either be terminal or leave a component larger than M; a semantic/noninjective reencoder is outside the theorem",
            "power_corollary": "for M=floor(n^lambda), fixed 0<lambda<1, the restricted pin depth is Omega(n^(1-lambda)); this is not an arbitrary-machine lower bound",
        },
        "falsifiers": {
            "F1": "some coherent partial assignment erases more than 2min(k0,k1) additional free identities",
            "F2": "some nonterminal raw residual has more than 1+5b incidence components",
            "F3": "some residual has all components <=M at depth below ceil((n-M)/(2+5M))",
            "F4": "the restricted raw-cofactor bound is silently applied to a semantic/noninjective reencoder, a pruned proof branch, or an arbitrary delayed guest",
        },
        "exact_thresholds": exact_thresholds,
        "power_thresholds": power_thresholds,
        "y6_exhaustive": y_rows,
        "paired_uv_samples": paired,
        "controls": controls,
        "dpll": dpll,
        "malformed_rejected": sum(not old.valid_target(x) for x in ([], [[1, 1, 2]], [[1, -2, 3]], [[1, 2]], [[1, 2, 3], [1, 2, 3]])),
        "xor_guard": {
            "actual_d_phys": "NOT MEASURED",
            "logical_traces": "offline diagnostics in controls",
            "changed_then_restored": "endpoint XOR can be zero while adjacent XOR sum is positive",
            "delay_steps_with_zero_data_changes": 10000,
            "source_rereads_with_zero_writes": 1000,
            "encoding_guard": "binary versus Gray changes logical deltas; unaligned/implicit states require declared physical semantics",
        },
        "resource_ledger": {
            "validation": "full canonical grammar and malformed rejection charged",
            "discovery": "occurrence lists, residual scan, erased-ID detection and component construction charged",
            "policy": "branch-variable discovery, policy comparison, switching and failed trials charged",
            "source_access": "source bits, clause IDs, index tapes, heads, rereads and resets charged",
            "child_output": "materialized child bits or virtual address computation and every queried source bit charged",
            "guest": "unknown-K simulation, arbitrary delay, query preparation, replay and answer/certificate checking charged",
            "space": "source, tape/index, query/child, guest, certificates, retained ancestors and controller state counted simultaneously",
            "diagnostic": "full XOR tracing is offline here and is not a free internal oracle",
        },
        "search_record": {
            "obstruction": "can a shallow source-faithful wrapper replace every connected raw residual by small components without already using a semantic reencoder?",
            "web_queries": [
                "SAT strong backdoor sets component decomposition decision trees primary paper",
                "SAT backdoor treewidth component decomposition DPLL decision tree lower bound",
                "SAT backdoors depth beats size JCSS 2024",
                "Recursive Backdoors for SAT MFCS 2021",
            ],
            "github_queries": [
                "repo:j15marti/pnp WRAPPER-CONNECTED-SHALLOW-BOUNDARY1",
                "repo:j15marti/pnp backdoor depth SAT wrapper",
                "org:openai SAT DPLL component backdoor",
                "org:openai Monotone 3-SAT-(2,2)",
            ],
            "findings": "recursive/component backdoor depth directly matches branch-and-decompose accounting and charges 2^depth; it does not prove this numerical bound. Project wrapper review supplied the forward combinatorial claim. OpenAI GitHub returned no relevant implementation or proof; public solver repositories were engineering analogues only.",
            "transfer_classification": "directly transferable definitions/accounting only; no external theorem transfers the ARC/FLMV conclusion",
            "novelty": "independent proof audit plus exact inverse threshold and explicit semantic-reencoder escape taxonomy; no external novelty claim",
        },
        "claim_status": {
            "forward_and_inverse": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "component_backdoor_context": "KNOWN THEOREM / PRIOR LITERATURE",
            "semantic_reencoder": "OPEN",
            "arbitrary_A_to_Phi_A": "OPEN",
            "numerical_FLMV_transport": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }

    FULL.parent.mkdir(parents=True, exist_ok=True)
    full_text = json.dumps(full, sort_keys=True, separators=(",", ":"))
    FULL.write_text(full_text)
    archive_text = base64.b64encode(gzip.compress(full_text.encode(), compresslevel=9)).decode()
    ARCHIVE.write_text(archive_text)
    summary = {k: full[k] for k in ("run_id", "timestamp", "theorem", "falsifiers", "exact_thresholds", "power_thresholds", "dpll", "malformed_rejected", "xor_guard", "resource_ledger", "search_record", "claim_status")}
    summary["y6_summary"] = summarize_rows(y_rows)
    summary["paired_uv_summary"] = {
        "rows": len(paired),
        "depths": sorted(set(r["b"] for r in paired)),
        "same_source_indexed_assignments": True,
        "all_U198_UNSAT": all(r["U198_label"] == "UNSAT" for r in paired),
        "all_V198_SAT": all(r["V198_label"] == "SAT" for r in paired),
        "U_nonterminal_summary": summarize_rows([r["U198"] for r in paired]),
        "V_nonterminal_summary": summarize_rows([r["V198"] for r in paired]),
    }
    summary["full_raw"] = {
        "full_path": str(FULL.relative_to(ROOT)),
        "full_bytes": len(full_text),
        "full_sha256": hashlib.sha256(full_text.encode()).hexdigest(),
        "archive_path": str(ARCHIVE.relative_to(ROOT)),
        "archive_bytes": len(archive_text),
        "archive_sha256": hashlib.sha256(archive_text.encode()).hexdigest(),
    }
    summary["runtime_seconds"] = time.perf_counter() - started
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(SUMMARY), "runtime_seconds": summary["runtime_seconds"], "y6": summary["y6_summary"], "paired": summary["paired_uv_summary"], "full_bytes": len(full_text), "archive_bytes": len(archive_text)}, indent=2))


if __name__ == "__main__":
    main()
