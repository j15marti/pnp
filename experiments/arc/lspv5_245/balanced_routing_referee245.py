#!/usr/bin/env python3
"""REFEREE245: balanced-articulation guest aggregation and routing ledgers.

Standard Python only.  Finite counters are logical proxies, not FLMV steps.
The symbolic inequality is checked with exact integers.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

RUN = "LSPV5_BALANCED_ROUTING_REFEREE245"
STAMP = "2026-10-31 09:48 PDT"
ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_0948_LSPV5_BALANCED_ROUTING_REFEREE245_raw.json"
SUMMARY = ROOT / "results/summaries/arc/2026-10-31_0948_LSPV5_BALANCED_ROUTING_REFEREE245_summary.json"


def star(k: int, unsat: bool):
    """GATE278 family: all blocks pin -x; UNSAT mate pins last block +x."""
    clauses = []
    n = 1
    blocks = []
    for i in range(k):
        y, z = n + 1, n + 2
        n += 2
        pin = 1 if unsat and i == k - 1 else -1
        ids = []
        for sy, sz in itertools.product((1, -1), repeat=2):
            ids.append(len(clauses) + 1)
            clauses.append((pin, sy * y, sz * z))
        for _ in range(k - 1):
            p, q = n + 1, n + 2
            n += 2
            ids.append(len(clauses) + 1)
            clauses.append((y, p, q))
        blocks.append({"pin": pin, "clauses": ids, "vars": [y, z]})
    assert n == 1 + 2 * k * k
    assert len(clauses) == k * (k + 3)
    return clauses, n, blocks


def dimacs(clauses, n):
    return "p cnf %d %d\n%s" % (n, len(clauses), "".join(" ".join(map(str, c)) + " 0\n" for c in clauses))


def primal(clauses, n):
    graph = [set() for _ in range(n + 1)]
    for clause in clauses:
        for a, b in itertools.combinations({abs(x) for x in clause}, 2):
            graph[a].add(b)
            graph[b].add(a)
    return graph


def components(graph, banned):
    seen, out = {banned}, []
    for root in range(1, len(graph)):
        if root in seen:
            continue
        seen.add(root)
        stack, group = [root], set()
        while stack:
            v = stack.pop()
            group.add(v)
            for w in graph[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(group)
    return out


def restrict_child(clauses, group, pivot, bit):
    selected = []
    for clause in clauses:
        private = {abs(l) for l in clause if abs(l) != pivot}
        if not private or private.isdisjoint(group):
            continue
        assert private <= group
        if any(abs(l) == pivot and (l > 0) == bit for l in clause):
            continue
        selected.append(tuple(l for l in clause if abs(l) != pivot))
    active = sorted({abs(l) for c in selected for l in c})
    ren = {v: i + 1 for i, v in enumerate(active)}
    dense = [tuple((1 if l > 0 else -1) * ren[abs(l)] for l in c) for c in selected]
    return dense, len(active)


def dpll(clauses):
    nodes = probes = 0
    def rec(assign):
        nonlocal nodes, probes
        nodes += 1
        while True:
            unit = None
            all_sat = True
            for clause in clauses:
                sat = False
                rem = []
                for lit in clause:
                    probes += 1
                    v = abs(lit)
                    if v in assign:
                        if assign[v] == (lit > 0):
                            sat = True
                            break
                    else:
                        rem.append(lit)
                if sat:
                    continue
                all_sat = False
                if not rem:
                    return None
                if len(rem) == 1:
                    unit = rem[0]
                    break
            if unit is None:
                if all_sat:
                    return dict(assign)
                break
            v, val = abs(unit), unit > 0
            if v in assign and assign[v] != val:
                return None
            assign[v] = val
        freq = Counter(abs(l) for c in clauses for l in c if abs(l) not in assign)
        if not freq:
            return dict(assign)
        v = freq.most_common(1)[0][0]
        for val in (True, False):
            nxt = dict(assign)
            nxt[v] = val
            ans = rec(nxt)
            if ans is not None:
                return ans
        return None
    model = rec({})
    return model, {"nodes": nodes, "literal_probes": probes}


def true_counts(clauses, assignment):
    return [sum(assignment.get(abs(l), False) == (l > 0) for l in c) for c in clauses]


def local_controls(clauses, n, full=False):
    occurrences = []
    for j, c in enumerate(clauses, 1):
        S = {str(abs(l)): int(l > 0) for l in c}
        U = {v: 1 - b for v, b in S.items()}
        occurrences.append({"clause": j, "literals": list(c), "S": S, "invert_S_U": U,
                            "U": U, "invert_U_S": S})
    pair_counts = Counter()
    matrix = []
    for a in range(len(clauses)):
        A = {abs(l): int(l > 0) for l in clauses[a]}
        for b in range(a + 1, len(clauses)):
            B = {abs(l): int(l > 0) for l in clauses[b]}
            shared = A.keys() & B.keys()
            same = any(A[v] == B[v] for v in shared)
            opp = any(A[v] != B[v] for v in shared)
            modes = {"SS": not opp, "SU": not same, "US": not same, "UU": not opp}
            pair_counts[tuple(modes.values())] += 1
            if full:
                matrix.append({"source_clauses": [a + 1, b + 1], "shared": sorted(shared), **modes})
    trail = []
    assignment = {v: False for v in range(1, n + 1)}
    for step, flip in enumerate([None, 1, 2, 3, n], 0):
        if flip is not None:
            assignment[flip] = not assignment[flip]
        counts = true_counts(clauses, assignment)
        trail.append({"step": step, "flip": flip, "N": [counts.count(r) for r in range(4)],
                      "per_clause_true_literals": counts if full else None})
    zero = {v: False for v in range(1, n + 1)}
    one = {v: True for v in range(1, n + 1)}
    tz, to = true_counts(clauses, zero), true_counts(clauses, one)
    assert all(to[i] == 3 - tz[i] for i in range(len(clauses)))
    return {
        "per_occurrence_local_extremes": occurrences if full else {"count": 3 * len(clauses)},
        "compatibility_matrix": matrix if full else {"pairs": len(clauses) * (len(clauses) - 1) // 2,
                                                       "pattern_counts": {str(k): v for k, v in pair_counts.items()}},
        "zero_endpoint": {"N": [tz.count(r) for r in range(4)], "SAT": 0 not in tz},
        "one_endpoint": {"N": [to.count(r) for r in range(4)], "SAT": 0 not in to},
        "flip_trail": trail,
    }


def pin_resolution(block, clauses):
    ids = block["clauses"][:4]
    c = [set(clauses[j - 1]) for j in ids]
    pin = block["pin"]
    y = next(abs(l) for l in clauses[ids[0] - 1] if abs(l) != 1)
    z = next(abs(l) for l in clauses[ids[0] - 1] if abs(l) not in (1, y))
    def resolve(a, b, v):
        out = (a - {v}) | (b - {-v})
        assert not any(-l in out for l in out)
        return out
    p1 = resolve(c[0], c[1], z)
    p2 = resolve(c[2], c[3], z)
    unit = resolve(p1, p2, y)
    assert unit == {pin}
    return {"source_clause_ids": ids, "steps": [sorted(p1), sorted(p2), sorted(unit)], "unit": pin}


def main():
    started = time.perf_counter()
    records = []
    assertion_units = 0
    for k in (3, 5, 7, 9, 15):
        for unsat in (False, True):
            clauses, n, blocks = star(k, unsat)
            source_text = dimacs(clauses, n)
            N = len(source_text.encode())
            graph = primal(clauses, n)
            groups = components(graph, 1)
            assert len(groups) == k
            children = []
            guest_nodes = guest_probes = 0
            for bit in (False, True):
                for i, group in enumerate(groups):
                    child, cn = restrict_child(clauses, group, 1, bit)
                    text = dimacs(child, max(1, cn))
                    model, work = dpll(child)
                    guest_nodes += work["nodes"]
                    guest_probes += work["literal_probes"]
                    children.append({"bit": int(bit), "component": i + 1, "n": cn,
                                     "m": len(child), "bytes": len(text.encode()),
                                     "SAT": model is not None})
            V = sum(x["bytes"] for x in children)
            M = max(x["bytes"] for x in children)
            model, baseline = dpll(clauses)
            assert (model is None) == unsat
            join = any(all(x["SAT"] for x in children if x["bit"] == bit) for bit in (0, 1))
            assert join == (not unsat)
            spectrum = []
            for K in range(1, 9):
                actual = sum(x["bytes"] ** K for x in children)
                bound = V * (M ** (K - 1))
                assert actual <= bound
                spectrum.append({"K": K, "sum_MK": actual, "V_Mmax_Kminus1": bound,
                                 "ratio": actual / bound})
                assertion_units += 1
            proofs = [pin_resolution(b, clauses) for b in blocks]
            if unsat:
                assert proofs[0]["unit"] == -1 and proofs[-1]["unit"] == 1
            else:
                assert all(p["unit"] == -1 for p in proofs)
            controls = local_controls(clauses, n, full=(k == 3))
            record = {
                "name": f"STAR{k}_{'UNSAT' if unsat else 'SAT'}",
                "label": "UNSAT" if unsat else "SAT", "k": k, "n": n, "m": len(clauses),
                "source_bytes": N, "source_sha256": hashlib.sha256(source_text.encode()).hexdigest(),
                "components": k, "children": children, "total_child_bytes": V, "max_child_bytes": M,
                "guest_spectrum": spectrum,
                "routing_ledgers": {
                    "serial_full_source_scans_clause_visits": 2 * k * len(clauses),
                    "simultaneous_materialized_child_bytes": V,
                    "sequential_peak_one_child_bytes": M,
                    "concurrent_linear_state_bytes_proxy": V,
                },
                "baseline_dpll": baseline,
                "all_child_dpll": {"nodes": guest_nodes, "literal_probes": guest_probes},
                "pin_resolution_proofs": proofs,
                "unsat_final_resolution": [-1, 1, []] if unsat else None,
                "controls": controls,
            }
            records.append(record)
            assertion_units += 20 + 3 * len(clauses) + 4 * len(clauses) * (len(clauses) - 1) // 2
    raw = {
        "run": RUN, "timestamp": STAMP, "status": "PROVED/EXACT restricted algebra; COMPUTATIONAL finite controls; ARC OPEN",
        "seed": None, "records": records, "assertion_units": assertion_units,
        "theorem": {
            "statement": "For K>=1, sum_i M_i^K <= (sum_i M_i) max_i(M_i)^(K-1).",
            "arc_specialization": "V=N^(1+o(1)), Mmax=N^(1/2+o(1)) gives guest time N^(1/2+K/2+o(1)).",
            "limitation": "Does not bound separator discovery, clause routing, virtual access, fallback, or all implementations."
        },
        "limitations": [
            "Python counters are not native FLMV transitions or space.",
            "The routing ledgers describe explicit strategies, not a universal time-space lower bound.",
            "No all-input balanced separator or hereditary ARC compiler is proved.",
            "P versus NP remains OPEN."
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(raw, indent=2) + "\n")
    raw_sha = hashlib.sha256(RAW.read_bytes()).hexdigest()
    summary = {
        "run": RUN, "records": len(records), "SAT": sum(r["label"] == "SAT" for r in records),
        "UNSAT": sum(r["label"] == "UNSAT" for r in records), "assertion_units": assertion_units,
        "raw_sha256": raw_sha, "max_k": max(r["k"] for r in records),
        "all_guest_bounds_pass": True, "status": "PASS; restricted theorem only; P vs NP OPEN"
    }
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
