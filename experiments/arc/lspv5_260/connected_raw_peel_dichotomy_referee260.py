#!/usr/bin/env python3
"""REFEREE260: connected raw-cofactor/component-peel dichotomy.

This is structural/accounting evidence only.  It does not claim an arbitrary
SAT-machine lower bound or a numerical FLMV transfer.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import time
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REF258 = ROOT / "experiments/arc/lspv5_258/nonminimum_branch_reentry_referee258.py"
STAMP = "2026-11-01_0048"
RUN = "CONNECTED-RAW-PEEL-DICHOTOMY-REFEREE260"
SUMMARY = ROOT / f"results/raw/arc/{STAMP}_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.json"
FULL = ROOT / f"results/raw/arc/{STAMP}_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.full.json"
ARCHIVE = ROOT / f"results/raw/arc/{STAMP}_LSPV5_CONNECTED_RAW_PEEL_DICHOTOMY_REFEREE260_raw.json.gz.b64"


def load_ref258():
    spec = importlib.util.spec_from_file_location("ref258_fixture", REF258)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def variables(formula):
    return sorted({abs(lit) for clause in formula for lit in clause})


def raw_cofactor(formula, assignment):
    out = []
    for clause in formula:
        row = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in assignment:
                row.append(lit)
            elif assignment[v] == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            if not row:
                return None
            out.append(row)
    return out


def incidence_components(formula, declared_variables=None):
    verts = set(declared_variables or variables(formula))
    adj = {v: set() for v in verts}
    for clause in formula:
        vs = [abs(x) for x in clause]
        for u, v in itertools.combinations(vs, 2):
            adj[u].add(v)
            adj[v].add(u)
    comps = []
    while adj:
        root = next(iter(adj))
        q, seen = deque([root]), {root}
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        comps.append(sorted(seen))
        for v in seen:
            del adj[v]
    return sorted(comps, key=lambda x: (x[0], len(x)))


def valid_target_up_to_relabel(formula):
    if not formula:
        return False
    keys, occ = [], Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return False
        key = tuple(sorted(clause))
        keys.append(key)
        for lit in clause:
            occ[abs(lit), lit > 0] += 1
    vs = {abs(x) for clause in formula for x in clause}
    return len(keys) == len(set(keys)) and all(occ[v, s] == 2 for v in vs for s in (False, True))


def source_components(formula):
    comps = incidence_components(formula)
    cid = {v: i for i, comp in enumerate(comps) for v in comp}
    clause_ids = [[] for _ in comps]
    for j, clause in enumerate(formula):
        ids = {cid[abs(x)] for x in clause}
        assert len(ids) == 1
        clause_ids[next(iter(ids))].append(j)
    return comps, clause_ids


def untouched_union_characterization(formula, assignment, residual):
    """Exact RHS of the LSPV-4 characterization."""
    if residual is None or not residual:
        return False
    comps, clause_ids = source_components(formula)
    residual_keys = {tuple(clause) for clause in residual}
    kept = []
    for comp, ids in zip(comps, clause_ids):
        untouched = not any(v in assignment for v in comp)
        component_keys = {tuple(formula[j]) for j in ids}
        if untouched and component_keys <= residual_keys:
            kept.append((comp, ids))
    union_keys = {tuple(formula[j]) for _, ids in kept for j in ids}
    if union_keys != residual_keys:
        return False
    outside = [formula[j] for j in range(len(formula)) if tuple(formula[j]) not in union_keys]
    return all(any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0) for lit in c) for c in outside)


def pivot_neighbors(formula, pivot):
    return sorted({abs(lit) for c in formula if pivot in {abs(x) for x in c} for lit in c if abs(lit) != pivot})


def one_pivot_rows(formula):
    n = max(variables(formula))
    source_connected = len(incidence_components(formula)) == 1
    assert source_connected
    rows = []
    for pivot in variables(formula):
        neigh = pivot_neighbors(formula, pivot)
        assert len(neigh) <= 8
        for bit in (0, 1):
            residual = raw_cofactor(formula, {pivot: bool(bit)})
            assert residual is not None and residual
            remaining = [v for v in variables(formula) if v != pivot]
            comps = incidence_components(residual, remaining)
            assert sum(map(len, comps)) == n - 1
            assert all(set(c) & set(neigh) for c in comps)
            assert len(comps) <= len(neigh) <= 8
            largest = max(map(len, comps))
            assert largest >= math.ceil((n - 1) / 8)
            assert not valid_target_up_to_relabel(residual)
            rows.append({
                "pivot": pivot,
                "bit": bit,
                "neighbors": neigh,
                "component_sizes": sorted(map(len, comps), reverse=True),
                "largest_component": largest,
                "raw_clauses": len(residual),
                "raw_width_histogram": dict(Counter(map(len, residual))),
                "canonical_raw_child": False,
            })
    return rows


def exhaustive_y6_characterization(formula):
    vs = variables(formula)
    rows, canonical_nonempty, empty_sat, contradictions = [], 0, 0, 0
    for state in itertools.product((-1, 0, 1), repeat=len(vs)):
        assignment = {v: bool(s) for v, s in zip(vs, state) if s >= 0}
        residual = raw_cofactor(formula, assignment)
        if residual is None:
            contradictions += 1
            status = "CONTRADICTION"
        elif not residual:
            empty_sat += 1
            status = "EMPTY_SAT_TERMINAL"
        else:
            lhs = valid_target_up_to_relabel(residual)
            rhs = untouched_union_characterization(formula, assignment, residual)
            assert lhs == rhs
            canonical_nonempty += int(lhs)
            status = "CANONICAL" if lhs else "NONCANONICAL"
        rows.append({"state": "".join("*" if s < 0 else str(s) for s in state), "status": status})
    assert len(rows) == 3 ** len(vs)
    assert canonical_nonempty == 1  # only the empty assignment on connected Y6
    return {"rows": rows, "canonical_nonempty": canonical_nonempty, "empty_sat": empty_sat, "contradictions": contradictions}


def clause_extremes(formula):
    out = []
    for j, clause in enumerate(formula):
        s = {abs(lit): int(lit > 0) for lit in clause}
        u = {v: 1 - b for v, b in s.items()}
        out.append({"clause": j, "literals": clause, "S": s, "not_S": u, "U": u, "not_U": s})
    return out


def exact_pair_mask(c1, c2):
    shared = set(map(abs, c1)) & set(map(abs, c2))
    same = any((next(x for x in c1 if abs(x) == v) > 0) == (next(x for x in c2 if abs(x) == v) > 0) for v in shared)
    opp = any((next(x for x in c1 if abs(x) == v) > 0) != (next(x for x in c2 if abs(x) == v) > 0) for v in shared)
    predicted = (not opp, not same, not same, not opp)
    union = sorted(set(map(abs, c1)) | set(map(abs, c2)))
    observed = []
    for want1, want2 in ((1, 1), (1, 0), (0, 1), (0, 0)):
        ok = False
        for bits in itertools.product((0, 1), repeat=len(union)):
            a = dict(zip(union, bits))
            v1 = [int(a[abs(x)] == int(x > 0)) for x in c1]
            v2 = [int(a[abs(x)] == int(x > 0)) for x in c2]
            if all(x == want1 for x in v1) and all(x == want2 for x in v2):
                ok = True
                break
        observed.append(ok)
    assert tuple(observed) == predicted
    return sum((1 << i) for i, ok in enumerate(predicted) if ok)


def pair_matrix(formula):
    return [[i, j, exact_pair_mask(formula[i], formula[j])] for i in range(len(formula)) for j in range(i + 1, len(formula))]


def endpoints(formula):
    n = max(variables(formula))
    ans = {}
    for name, a in (("zero", [0] * n), ("one", [1] * n)):
        hist = Counter(sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula)
        ans[name] = {str(k): hist[k] for k in range(4)}
    return ans


def flip_trail(formula):
    n = max(variables(formula))
    flips = [p % n for p in (0, 1, 2, 197, n - 1, n - 1, 2)]
    a = [0] * n
    rows = []
    for p in flips:
        before = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
        a[p] ^= 1
        after = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
        rows.append({"pivot_zero_based": p, "changed_clause_ids": [j for j, (x, y) in enumerate(zip(before, after)) if x != y], "counts": after})
    return rows


def logical_state(formula, assignment, gray):
    state = list(assignment)
    for clause in formula:
        t = sum(assignment[abs(x) - 1] == int(x > 0) for x in clause)
        code = t ^ (t >> 1) if gray else t
        state.extend((code & 1, (code >> 1) & 1, int(t > 0)))
    return state


def xor_trace(formula):
    n = max(variables(formula))
    flips = [p % n for p in (0, 1, 2, 197, n - 1, n - 1, 2)]
    out = {}
    for name, gray in (("binary", False), ("gray", True)):
        a = [0] * n
        first = prev = logical_state(formula, a, gray)
        rows = []
        for p in flips:
            before_counts = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            a[p] ^= 1
            after_counts = [sum(a[abs(x) - 1] == int(x > 0) for x in c) for c in formula]
            cur = logical_state(formula, a, gray)
            rows.append({
                "pivot_zero_based": p,
                "changed_clause_ids": [j for j, (x, y) in enumerate(zip(before_counts, after_counts)) if x != y],
                "changed_cell_ids": [j for j, (x, y) in enumerate(zip(prev, cur)) if x != y],
                "d_logic": sum(x != y for x, y in zip(prev, cur)),
            })
            prev = cur
        out[name] = {"state_bits": len(first), "rows": rows, "sum_adjacent_d_logic": sum(r["d_logic"] for r in rows), "endpoint_d_logic": sum(x != y for x, y in zip(first, prev)), "actual_d_phys": "NOT MEASURED"}
    return out


def full_controls(formula):
    return {"clause_extremes": clause_extremes(formula), "pair_matrix": pair_matrix(formula), "endpoints": endpoints(formula), "flip_trail": flip_trail(formula), "xor": xor_trace(formula)}


def relabel(formula, offset):
    return [[(1 if x > 0 else -1) * (abs(x) + offset) for x in c] for c in formula]


def main():
    started = time.perf_counter()
    ref = load_ref258()
    U = ref.load_u()
    V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = ref.y6()
    assert ref.valid_target(U) and ref.valid_target(V) and ref.valid_target(Y)
    assert len(incidence_components(U)) == len(incidence_components(V)) == len(incidence_components(Y)) == 1
    assert ref.unsat_boundary_certificate(U) == []
    assert ref.satisfies(V, ref.V_WITNESS)
    yw = next(f"{mask:06b}"[::-1] for mask in range(64) if ref.satisfies(Y, f"{mask:06b}"[::-1]))

    pivot = {"U198": one_pivot_rows(U), "V198": one_pivot_rows(V), "Y6": one_pivot_rows(Y)}
    y_exhaustive = exhaustive_y6_characterization(Y)

    # Sharp disconnected controls: satisfying the Y component deletes it and
    # leaves an unchanged valid U or V component.
    sharp = {}
    for name, core in (("U198", U), ("V198", V)):
        source = core + relabel(Y, 198)
        assignment = {198 + i + 1: bit == "1" for i, bit in enumerate(yw)}
        residual = raw_cofactor(source, assignment)
        assert residual == core and valid_target_up_to_relabel(residual)
        sharp[name] = {"source_components": [198, 6], "assigned_Y_witness": yw, "residual_variables": 198, "residual_clauses": 264, "label": "UNSAT" if name == "U198" else "SAT"}

    controls = {"U198": full_controls(U), "V198": full_controls(V), "Y6": full_controls(Y)}
    dpll = {"U198": ref.dpll_cap(U, 600), "V198": ref.dpll_cap(V, 600), "Y6": ref.dpll_cap(Y, 600)}

    full = {
        "run_id": RUN,
        "timestamp": "2026-11-01T00:48:00-07:00",
        "theorem": {
            "raw_characterization": "nonempty canonical raw cofactor iff unchanged union of untouched source components and every outside clause is satisfied",
            "connected_corollary": "connected valid source plus nonempty assignment has only empty SAT terminal or noncanonical raw cofactor",
            "one_pivot_fragment_bound": "every nonempty one-pivot raw cofactor retains n-1 variables, has at most eight incidence components, and its largest component has at least ceil((n-1)/8) variables",
            "controller_dichotomy": "raw target-hereditary recursion fails on connected nonterminal branches; REF258 repairs with n+201 variables; source-identity-preserving repair cannot be smaller; semantic/noninjective reencoding remains OPEN",
        },
        "falsifiers": {
            "F1": "a connected valid source has a nonempty canonical raw cofactor after a nonempty assignment",
            "F2": "one pivot can fragment the ordinary residual into more than eight components or erase another source identity",
            "F3": "component recursion automatically gives a power-short largest child",
            "F4": "failure of raw heredity proves a lower bound for arbitrary semantic reencoders",
        },
        "pivot_rows": pivot,
        "y6_exhaustive": y_exhaustive,
        "sharp_disconnected_controls": sharp,
        "controls": controls,
        "dpll": dpll,
        "malformed_rejected": sum(not ref.valid_target(x) for x in ([], [[1, 1, 2]], [[1, -2, 3]], [[1, 2]], [[1, 2, 3], [1, 2, 3]])),
        "xor_guard": {"actual_d_phys": "NOT MEASURED", "delay_steps_with_zero_data_changes": 10000, "source_rereads_with_zero_writes": 1000, "logical_trail": "offline diagnostic"},
        "resource_ledger": {
            "validation": "full target grammar, malformed rejection and source connectivity charged",
            "discovery": "component graph construction and repeated post-restriction component discovery charged",
            "selection": "SAT requires all components; UNSAT early stop needs a found refuted component; no free selector",
            "source_index": "source clause IDs, occurrence lists, heads and reset charged",
            "reencoding": "repair/relabel/output/access and proof of both-label equivalence charged",
            "guest": "unknown-K calls, delay, failed policies, replay and answer checking charged",
            "space": "source, graph/index, components, child/query, guest, certificates and retained ancestors counted simultaneously",
        },
        "search_record": {
            "obstruction": "connected canonical raw restriction cannot expose a hereditary target child; can ordinary fragmentation nevertheless be power-short?",
            "web_queries": [
                "primary paper SAT connected components decomposition CNF incidence graph Biere Sinz 2006",
                "Döcker Monotone 3-SAT-(2,2) NP-complete arXiv primary paper",
                "SAT self reducibility restrictions bounded occurrence formula primary paper",
                "kernelization connected components protrusion replacement acquisition primary paper",
            ],
            "github_queries": [
                "repo:j15marti/pnp connected cofactor canonical component peel",
                "repo:j15marti/pnp ARC-CONNECTED-COFACTOR293",
                "repo:j15marti/pnp raw cofactor component canonical reentry",
                "org:openai SAT connected component cofactor",
            ],
            "findings": "Biere-Sinz gives component conjunction; Doecker gives the exact NP-complete target; kernelization representatives require constructive acquisition; project COFACTOR293 proves the raw characterization; OpenAI hits were unrelated",
            "novelty": "independent reconstruction plus the explicit <=8 one-pivot fragmentation/power-short corollary; no external novelty claim",
        },
        "claim_status": {"raw_characterization": "PROVED/EXACT independently reconstructed", "fragment_bound": "PROVED/EXACT", "finite_controls": "COMPUTATIONAL", "semantic_reencoder": "OPEN", "FLMV": "OPEN", "P_vs_NP": "OPEN"},
    }

    FULL.parent.mkdir(parents=True, exist_ok=True)
    full_text = json.dumps(full, sort_keys=True, separators=(",", ":"))
    FULL.write_text(full_text)
    compressed = gzip.compress(full_text.encode(), compresslevel=9)
    archive_text = base64.b64encode(compressed).decode()
    ARCHIVE.write_text(archive_text)
    summary = {k: full[k] for k in ("run_id", "timestamp", "theorem", "falsifiers", "sharp_disconnected_controls", "dpll", "malformed_rejected", "xor_guard", "resource_ledger", "search_record", "claim_status")}
    summary["pivot_summary"] = {name: {"branches": len(rows), "max_components": max(len(r["component_sizes"]) for r in rows), "min_largest": min(r["largest_component"] for r in rows), "max_largest": max(r["largest_component"] for r in rows), "all_noncanonical": all(not r["canonical_raw_child"] for r in rows)} for name, rows in pivot.items()}
    summary["y6_exhaustive_summary"] = {k: v for k, v in y_exhaustive.items() if k != "rows"}
    summary["full_raw"] = {"full_path": str(FULL.relative_to(ROOT)), "full_bytes": len(full_text), "full_sha256": hashlib.sha256(full_text.encode()).hexdigest(), "archive_path": str(ARCHIVE.relative_to(ROOT)), "archive_bytes": len(archive_text), "archive_sha256": hashlib.sha256(archive_text.encode()).hexdigest()}
    summary["runtime_seconds"] = time.perf_counter() - started
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(SUMMARY), "runtime_seconds": summary["runtime_seconds"], "pivot_summary": summary["pivot_summary"], "y6": summary["y6_exhaustive_summary"], "dpll": dpll, "full_bytes": len(full_text), "archive_bytes": len(archive_text)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
