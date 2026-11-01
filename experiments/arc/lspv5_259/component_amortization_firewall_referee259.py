#!/usr/bin/env python3
"""REFEREE259: certified component peel versus q4 repair overhead."""
from __future__ import annotations

import ast
import base64
import gzip
import hashlib
import importlib.util
import itertools
import json
import time
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REF258 = ROOT / "experiments/arc/lspv5_258/nonminimum_branch_reentry_referee258.py"
SUMMARY = ROOT / "results/raw/arc/2026-10-31_2348_LSPV5_COMPONENT_AMORTIZATION_FIREWALL_REFEREE259_raw.json"
FULL = ROOT / "results/raw/arc/2026-10-31_2348_LSPV5_COMPONENT_AMORTIZATION_FIREWALL_REFEREE259_raw.full.json"
ARCHIVE = ROOT / "results/raw/arc/2026-10-31_2348_LSPV5_COMPONENT_AMORTIZATION_FIREWALL_REFEREE259_raw.json.gz.b64"


def load_ref258():
    spec = importlib.util.spec_from_file_location("ref258", REF258)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def shift_formula(formula, offset):
    return [[(1 if x > 0 else -1) * (abs(x) + offset) for x in c] for c in formula]


def pad(core, small, copies):
    out = [c[:] for c in core]
    offset = max(abs(x) for c in core for x in c)
    width = max(abs(x) for c in small for x in c)
    for i in range(copies):
        out.extend(shift_formula(small, offset + i * width))
    return out


def component_sizes(formula):
    by_var = {}
    for j, c in enumerate(formula):
        for x in c:
            by_var.setdefault(abs(x), []).append(j)
    seen_v, seen_c, sizes = set(), set(), []
    for start in sorted(by_var):
        if start in seen_v:
            continue
        q = deque([("v", start)])
        vs, cs = set(), set()
        while q:
            kind, i = q.popleft()
            if kind == "v":
                if i in seen_v:
                    continue
                seen_v.add(i)
                vs.add(i)
                for j in by_var[i]:
                    q.append(("c", j))
            else:
                if i in seen_c:
                    continue
                seen_c.add(i)
                cs.add(i)
                for x in formula[i]:
                    q.append(("v", abs(x)))
        sizes.append({"variables": len(vs), "clauses": len(cs), "min_variable": min(vs)})
    return sorted(sizes, key=lambda z: z["min_variable"])


def exact_pair_modes(a, b):
    variables = sorted({abs(x) for x in a + b})
    got = set()
    for bits in itertools.product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        ta = sum(assignment[abs(x)] == (x > 0) for x in a)
        tb = sum(assignment[abs(x)] == (x > 0) for x in b)
        if ta in (0, 3) and tb in (0, 3):
            got.add(("S" if ta == 3 else "U") + ("S" if tb == 3 else "U"))
    return sorted(got)


def pair_matrix_cached(formula):
    rows, signatures, patterns = [], Counter(), {}
    for i, j in itertools.combinations(range(len(formula)), 2):
        same = any(x in formula[j] for x in formula[i])
        opposite = any(-x in formula[j] for x in formula[i])
        expected = [x for x, ok in zip(("SS", "SU", "US", "UU"), (not opposite, not same, not same, not opposite)) if ok]
        key = (same, opposite, len({abs(x) for x in formula[i] + formula[j]}))
        if key not in patterns:
            patterns[key] = exact_pair_modes(formula[i], formula[j])
        assert patterns[key] == expected
        row = {"i": i, "j": j, "SS": not opposite, "SU": not same, "US": not same, "UU": not opposite}
        rows.append(row)
        signatures["".join("1" if row[x] else "0" for x in ("SS", "SU", "US", "UU"))] += 1
    return {"rows": rows, "signature_counts": dict(signatures), "exact_pattern_modes": {str(k): v for k, v in patterns.items()}}


def endpoints(formula):
    out = {}
    n = max(abs(x) for c in formula for x in c)
    for name, bits in (("zero", "0" * n), ("one", "1" * n)):
        hist = Counter()
        for c in formula:
            hist[sum((bits[abs(x) - 1] == "1") == (x > 0) for x in c)] += 1
        out[name] = {str(i): hist[i] for i in range(4)}
    return out


def full_control(ref, formula):
    n = max(abs(x) for c in formula for x in c)
    # Keep the same adversarial pattern across sizes, but map every checkpoint
    # to a real source variable (Y6 has only six variables).
    flips = [p % n for p in (0, 1, 2, 197, n - 6, n - 1, n - 1, 2)]
    return {
        "clause_extremes": ref.clause_extremes(formula),
        "pair_matrix": pair_matrix_cached(formula),
        "endpoints": endpoints(formula),
        "xor": ref.xor_trace(formula, flips),
    }


def main():
    started = time.perf_counter()
    ref = load_ref258()
    U = ref.load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = ref.y6()
    assert ref.valid_target(U) and ref.valid_target(V) and ref.valid_target(Y)
    assert ref.unsat_boundary_certificate(U) == []
    assert ref.satisfies(V, ref.V_WITNESS)
    yw = next(f"{mask:06b}"[::-1] for mask in range(64) if ref.satisfies(Y, f"{mask:06b}"[::-1]))

    D = U[:1] + U[2:]
    d_partial = ref.dpll_witness(D)
    assert d_partial is not None
    dw = ref.complete_witness(D, d_partial, 198)
    U_child = ref.build_child(U, 3, True, D, dw)
    V_child = ref.build_child(V, 3, True, D, dw)
    vw_child = V_child["extend"](ref.V_WITNESS)
    assert ref.valid_target(U_child["child"]) and ref.valid_target(V_child["child"])
    assert ref.satisfies(V_child["child"], vw_child)

    cases = {}
    formulas = {}
    for p in (33, 34):
        for name, core in (("U", U), ("V", V)):
            F = pad(core, Y, p)
            formulas[p, name] = F
            assert ref.valid_target(F)
            comps = component_sizes(F)
            assert len(comps) == p + 1 and comps[0]["variables"] == 198
            witness = None if name == "U" else ref.V_WITNESS + yw * p
            if witness is not None:
                assert ref.satisfies(F, witness)
            n = 198 + 6 * p
            m = 264 + 8 * p
            cases[f"{name}_p{p}"] = {
                "label": "UNSAT" if name == "U" else "SAT",
                "variables": n,
                "clauses": m,
                "components": comps,
                "padding_variables": 6 * p,
                "padding_clauses": 8 * p,
                "encoding_bits": ref.encoding_length(n, m),
                "child_variables": 399,
                "child_clauses": 532,
                "child_encoding_bits": ref.encoding_length(399, 532),
                "delta_variables_child_minus_source": 399 - n,
                "delta_clauses_child_minus_source": 532 - m,
                "delta_bits_child_minus_source": ref.encoding_length(399, 532) - ref.encoding_length(n, m),
                "witness_sha256": None if witness is None else hashlib.sha256(witness.encode()).hexdigest(),
            }

    threshold = []
    for p in range(0, 41):
        n, m = 198 + 6 * p, 264 + 8 * p
        threshold.append({
            "padding_copies": p,
            "padding_variables": 6 * p,
            "source_variables": n,
            "source_clauses": m,
            "source_bits": ref.encoding_length(n, m),
            "child_variables": 399,
            "child_clauses": 532,
            "child_bits": ref.encoding_length(399, 532),
            "strict_structural_shrink": 399 < n and 532 < m,
            "strict_bit_shrink": ref.encoding_length(399, 532) < ref.encoding_length(n, m),
        })
    assert not threshold[33]["strict_structural_shrink"]
    assert threshold[34]["strict_structural_shrink"]
    assert not threshold[33]["strict_bit_shrink"]
    assert threshold[34]["strict_bit_shrink"]

    dpll = {}
    for p in (33, 34):
        for name in ("U", "V"):
            dpll[f"{name}_p{p}_source"] = ref.dpll_cap(formulas[p, name], cap=600)
    dpll["U_child"] = ref.dpll_cap(U_child["child"], cap=600)
    dpll["V_child"] = ref.dpll_cap(V_child["child"], cap=600)

    controls = {
        "U_p34": full_control(ref, formulas[34, "U"]),
        "V_p34": full_control(ref, formulas[34, "V"]),
        "Y6": full_control(ref, Y),
    }
    malformed = [[], [[1, -2, 3]], [[1, 1, 2]], Y + [Y[0]], [[1, 2, 3]]]
    assert all(not ref.valid_target(x) for x in malformed)

    result = {
        "run_id": "COMPONENT-AMORTIZATION-FIREWALL-REFEREE259",
        "timestamp": "2026-10-31T23:48:00-07:00",
        "claim_status": {
            "certificate_carrying_component_peel": "PROVED/EXACT",
            "minimum_strict_structural_threshold": "PROVED/EXACT",
            "finite_controls": "COMPUTATIONAL",
            "power_short_all_input": "OPEN and not supplied by component peel",
            "arbitrary_A_Phi": "OPEN",
            "FLMV": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "falsifiers": {
            "F1": "fewer than 204 certified padding variables can strictly amortize the q4 +201/+268 structural overhead",
            "F2": "strict additive shrink automatically yields N^lambda power shrink",
            "F3": "component selection and SAT certificates are free, including on UNSAT sources",
            "F4": "padding/component/XOR statistics distinguish the U198 and V198 labels",
        },
        "theorem": {
            "quantifiers": "For every valid canonical F=G disjoint-union P, every pivot x in G, branch b, and checked SAT witnesses for every component of P",
            "equivalence": "SAT(F restricted by x=b) iff SAT(R(G,x=b))",
            "sizes": "if P has h variables then it has 4h/3 clauses, and R has (n-h+201,m-4h/3+268)",
            "strict_structural_shrink": "iff h>201; since h is divisible by 3, minimum h is 204",
            "power_short_condition": "n-h+201 <= n^lambda requires h >= n+201-n^lambda; the retained answer-bearing core must already have at most n^lambda-201 variables",
            "selection_firewall": "on UNSAT F the retained G must contain an UNSAT component and every peeled component needs a SAT certificate; choosing it is not free",
        },
        "actual_controls": cases,
        "threshold_table": threshold,
        "child": {
            "variables": 399,
            "clauses": 532,
            "bits": ref.encoding_length(399, 532),
            "V_witness_sha256": hashlib.sha256(vw_child.encode()).hexdigest(),
            "V_witness": vw_child,
            "D_witness_sha256": hashlib.sha256(dw.encode()).hexdigest(),
            "D_witness": dw,
            "closure": U_child["closure"],
        },
        "dpll_comparison": dpll,
        "controls": controls,
        "malformed_rejected": len(malformed),
        "xor_guard": {
            "actual_d_phys": "NOT MEASURED",
            "unaligned_source_child": "not compared by XOR",
            "delay": {"native_steps": 10000, "data_bit_changes": 0},
            "reread": {"reads": 1000, "writes": 0},
            "interpretation": "offline source-indexed logical diagnostic only",
        },
        "resource_ledger": {
            "validation": "full canonical grammar and component discovery charged",
            "certificate_acquisition": "SAT witnesses for every peeled component must be found or supplied; only verification is cheap once present",
            "selection": "UNSAT source requires retaining an answer-bearing UNSAT component; a perfect selector is not free",
            "source_access": "component IDs, renaming, q4 descriptor and source/critical-template bits charged",
            "child_access": "Q4-VIRTUAL-INDEX290 gives O(log N) scratch and reads per bit after O(N) descriptor scan, but child length still grows on the core",
            "output": "materialized child and certificate streams are charged",
            "guest": "unknown-K guest calls, delay, copying, replay and failure count",
            "space": "source indices, component queue, certificates, child/query, guest, ancestors and caches count at peak",
        },
        "search_record": {
            "web_queries": [
                "SAT incidence graph connected component decomposition satisfiability primary paper preprocessing",
                "kernelization replacement gadget constant additive overhead protrusion replacement primary paper",
                "parameterized complexity polynomial kernel power size reduction definition primary paper",
                "bounded occurrence SAT disjoint union components exact occurrence primary paper",
            ],
            "findings": [
                "Biere-Sinz 2006 proves independent SAT components may be solved separately",
                "kernelization literature requires answer-preserving acquired reductions and does not make representatives or acquisition free",
                "bounded-occurrence literature supplies enforcers but no numerical FLMV transfer",
            ],
            "github_queries": [
                "repo:j15marti/pnp component peel q4 branch reentry",
                "repo:j15marti/pnp component amortization power-short",
                "repo:j15marti/pnp NONMINIMUM-BRANCH-REENTRY-REFEREE258",
                "org:openai SAT connected component kernelization",
                "org:openai Monotone 3-SAT component decomposition",
            ],
            "github_findings": "REF258 and Q4-VIRTUAL-INDEX290 leave net shrink open; CHILD-SCAN-AMORTIZATION272 is model-restricted; OpenAI searches found no relevant implementation",
            "novelty": "project-local theorem only; no external novelty claim",
        },
        "corpus_audit": {
            "reviewed": [
                "root main/AGENTS/CODEX/pnp-research skill",
                "REDIRECT1/CONTRACT1 and named affine/construction/ARC gates",
                "REF255-258",
                "issue 3",
                "LSPV-1 SPILL294 and PLATEAU295",
                "LSPV-2 Q4-VIRTUAL-INDEX290",
                "LSPV-3 GATE292",
                "latest verified LSPV-4 INDEX-HEAD291; 23:36 write absent at preflight",
            ],
            "duplication": "component conjunction is known and already used in project; new statement is the exact +201/+268 amortization threshold and power-short firewall",
            "stale": "LSPV-1 PLATEAU295 lacks required REPORT token in opening marker; LSPV-3 GATE292 lacks both opening marker and sentinel",
        },
        "runtime_seconds": time.perf_counter() - started,
    }

    FULL.parent.mkdir(parents=True, exist_ok=True)
    full_bytes = (json.dumps(result, separators=(",", ":"), sort_keys=True) + "\n").encode()
    FULL.write_bytes(full_bytes)
    archive_bytes = base64.b64encode(gzip.compress(full_bytes, compresslevel=9, mtime=0)) + b"\n"
    ARCHIVE.write_bytes(archive_bytes)
    summary_keys = ("run_id", "timestamp", "claim_status", "falsifiers", "theorem", "actual_controls", "threshold_table", "child", "dpll_comparison", "malformed_rejected", "xor_guard", "resource_ledger", "search_record", "corpus_audit", "runtime_seconds")
    summary = {k: result[k] for k in summary_keys}
    summary["control_summary"] = {
        name: {
            "clauses": len(control["clause_extremes"]),
            "pairs": len(control["pair_matrix"]["rows"]),
            "pair_signatures": control["pair_matrix"]["signature_counts"],
            "endpoints": control["endpoints"],
            "xor": {enc: {k: v[k] for k in ("state_bits", "sum_adjacent_d_logic", "endpoint_d_logic", "actual_d_phys")} for enc, v in control["xor"].items()},
        }
        for name, control in controls.items()
    }
    summary["full_raw"] = {
        "archive_path": str(ARCHIVE.relative_to(ROOT)),
        "full_json_bytes": len(full_bytes),
        "archive_text_bytes": len(archive_bytes),
        "full_sha256": hashlib.sha256(full_bytes).hexdigest(),
        "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "summary": str(SUMMARY),
        "runtime_seconds": result["runtime_seconds"],
        "full_bytes": len(full_bytes),
        "archive_bytes": len(archive_bytes),
        "threshold": {k: cases[k] for k in ("U_p33", "V_p33", "U_p34", "V_p34")},
        "dpll": dpll,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
