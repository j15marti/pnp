#!/usr/bin/env python3
"""Reproduce the ARC-DP quadratic-output firewall.

Every invocation is intentionally small (<30 s).  The experiment constructs
same-gadget SAT/UNSAT proper-3CNF twins, eliminates one pivot by complete
Davis--Putnam resolution, checks the exact r^2 cross product, and compares a
transactional bounded-elimination controller with plain UP-DPLL.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
import tracemalloc
from pathlib import Path

Clause = tuple[int, ...]


def false_clause(bits: tuple[int, int, int]) -> Clause:
    return tuple(-i if b else i for i, b in enumerate(bits, 1))


def core(sat: bool) -> list[Clause]:
    cs = [false_clause(bits) for bits in itertools.product((0, 1), repeat=3)]
    if sat:
        cs.remove((-1, -2, -3))  # unique core model 111
    return cs


def family(r: int, sat: bool) -> tuple[list[Clause], dict]:
    pivot = 4
    pos, neg = [], []
    next_var = 5
    for _ in range(r):
        a, b = next_var, next_var + 1
        next_var += 2
        pos.append((pivot, a, b))
    for _ in range(r):
        c, d = next_var, next_var + 1
        next_var += 2
        neg.append((-pivot, c, d))
    clauses = core(sat) + pos + neg
    return clauses, {"pivot": pivot, "positive": pos, "negative": neg,
                     "nvars": next_var - 1, "core_clauses": len(core(sat))}


def dimacs_bits(clauses: list[Clause], nvars: int | None = None) -> int:
    if nvars is None:
        nvars = max((abs(l) for c in clauses for l in c), default=0)
    body = [f"p cnf {nvars} {len(clauses)}\n"]
    body.extend(" ".join(map(str, c)) + " 0\n" for c in clauses)
    return len("".join(body).encode("utf-8")) * 8


def normalize(c: Clause) -> Clause | None:
    s = set(c)
    if any(-x in s for x in s):
        return None
    return tuple(sorted(s, key=lambda x: (abs(x), x < 0)))


def eliminate(clauses: list[Clause], pivot: int, budget_bits: int | None = None):
    pos = [c for c in clauses if pivot in c]
    neg = [c for c in clauses if -pivot in c]
    keep = [c for c in clauses if pivot not in c and -pivot not in c]
    out = list(keep)
    provenance = []
    attempted = 0
    aborted = False
    for i, p in enumerate(pos):
        for j, n in enumerate(neg):
            attempted += 1
            resolvent = normalize(tuple(x for x in p if x != pivot) +
                                  tuple(x for x in n if x != -pivot))
            if resolvent is not None and resolvent not in out:
                out.append(resolvent)
                provenance.append({"positive_index": i, "negative_index": j,
                                   "resolvent": list(resolvent)})
            if budget_bits is not None and dimacs_bits(out) > budget_bits:
                aborted = True
                return {"aborted": True, "attempted_pairs": attempted,
                        "partial_output_bits": dimacs_bits(out),
                        "partial_clauses": len(out), "provenance": provenance}
    return {"aborted": aborted, "attempted_pairs": attempted, "clauses": out,
            "output_bits": dimacs_bits(out), "provenance": provenance}


def properize_width4(clauses: list[Clause]):
    maxv = max(abs(l) for c in clauses for l in c)
    out: list[Clause] = []
    bridges = 0
    for c in clauses:
        if len(c) <= 3:
            out.append(c)
        elif len(c) == 4:
            maxv += 1
            bridges += 1
            out.append((c[0], c[1], maxv))
            out.append((-maxv, c[2], c[3]))
        else:
            raise ValueError("unexpected clause width")
    return out, maxv, bridges


def clause_true_count(c: Clause, assignment: dict[int, bool]) -> int:
    return sum(assignment[abs(l)] == (l > 0) for l in c)


def satisfies(clauses: list[Clause], assignment: dict[int, bool]) -> bool:
    return all(clause_true_count(c, assignment) > 0 for c in clauses)


def restrict(clauses: list[Clause], var: int, value: bool):
    out = []
    for c in clauses:
        if (var if value else -var) in c:
            continue
        nc = tuple(l for l in c if l != (-var if value else var))
        if not nc:
            return None
        out.append(nc)
    return out


def unit_propagate(clauses: list[Clause], counters: dict):
    cs = list(clauses)
    while True:
        unit = next((c[0] for c in cs if len(c) == 1), None)
        if unit is None:
            return cs
        counters["unit_steps"] += 1
        cs = restrict(cs, abs(unit), unit > 0)
        if cs is None:
            counters["conflicts"] += 1
            return None


def dpll(clauses: list[Clause]):
    counters = {"calls": 0, "branches": 0, "unit_steps": 0,
                "conflicts": 0, "clause_visits_proxy": 0, "peak_clauses": 0}

    def rec(cs: list[Clause]):
        counters["calls"] += 1
        counters["clause_visits_proxy"] += len(cs)
        counters["peak_clauses"] = max(counters["peak_clauses"], len(cs))
        cs = unit_propagate(cs, counters)
        if cs is None:
            return False
        if not cs:
            return True
        var = min(abs(l) for c in cs for l in c)
        counters["branches"] += 1
        for value in (False, True):
            nxt = restrict(cs, var, value)
            if nxt is not None and rec(nxt):
                return True
        return False

    answer = rec(list(clauses))
    counters["answer"] = answer
    counters["total_work_proxy"] = (counters["calls"] + counters["branches"] +
                                      counters["unit_steps"] + counters["conflicts"] +
                                      counters["clause_visits_proxy"])
    return counters


def local_extreme_controls(clauses: list[Clause], nvars: int):
    per_clause = []
    for j, c in enumerate(clauses):
        s_target = {abs(l): (l > 0) for l in c}
        u_target = {v: not b for v, b in s_target.items()}
        occurrences = []
        for l in c:
            occurrences.append({"variable": abs(l), "sign": "+" if l > 0 else "-",
                                "S_value": l > 0, "invert_S_equals_U": not (l > 0),
                                "U_value": not (l > 0), "invert_U_equals_S": l > 0})
        per_clause.append({"source_clause_index": j, "clause": list(c),
                           "S_target": s_target, "invert_S_U_target": u_target,
                           "U_target": u_target, "invert_U_S_target": s_target,
                           "occurrences": occurrences})

    pair_matrix = []
    for j in range(len(clauses)):
        for k in range(j + 1, len(clauses)):
            cj, ck = clauses[j], clauses[k]
            vars_union = sorted({abs(l) for l in cj + ck})
            observed = {key: False for key in ("SS", "SU", "US", "UU")}
            for bits in itertools.product((False, True), repeat=len(vars_union)):
                a = dict(zip(vars_union, bits))
                tj, tk = clause_true_count(cj, a), clause_true_count(ck, a)
                if tj in (0, 3) and tk in (0, 3):
                    observed[("S" if tj == 3 else "U") +
                             ("S" if tk == 3 else "U")] = True
            same = any(l in ck for l in cj)
            opposite = any(-l in ck for l in cj)
            predicted = {"SS": not opposite, "UU": not opposite,
                         "SU": not same, "US": not same}
            if observed != predicted:
                raise AssertionError((j, k, observed, predicted))
            pair_matrix.append({"clause_indices": [j, k], "same_polarity_shared": same,
                                "opposite_polarity_shared": opposite,
                                "compatibility": observed})

    def status(assignment: dict[int, bool]):
        counts = [clause_true_count(c, assignment) for c in clauses]
        return {"true_literal_counts": counts,
                "N0_N1_N2_N3": [counts.count(i) for i in range(4)],
                "formula_satisfied": all(x > 0 for x in counts)}

    zero = {i: False for i in range(1, nvars + 1)}
    one = {i: True for i in range(1, nvars + 1)}
    trail = []
    cur = dict(zero)
    trail.append({"flip_prefix": [], **status(cur)})
    for i in range(1, nvars + 1):
        cur[i] = True
        trail.append({"flip_prefix": list(range(1, i + 1)), **status(cur)})
    return {"per_clause_local_extremes": per_clause,
            "pair_compatibility_matrix": pair_matrix,
            "all_zero": status(zero), "all_one": status(one),
            "intermediate_prefix_flip_trail": trail}


def run_case(r: int, sat: bool, controls: bool):
    clauses, meta = family(r, sat)
    source_bits = dimacs_bits(clauses, meta["nvars"])
    full = eliminate(clauses, meta["pivot"])
    child = full["clauses"]
    proper, proper_nvars, bridges = properize_width4(child)
    expected = r * r
    resolvents = [c for c in child if len(c) == 4]
    assert len(resolvents) == expected == len(set(resolvents))
    assert all(normalize(c) is not None for c in resolvents)
    assert not any(set(a) < set(b) for a in resolvents for b in resolvents if a != b)
    base = dpll(clauses)
    txn = eliminate(clauses, meta["pivot"], budget_bits=source_bits)
    assert txn["aborted"]
    safe = dpll(clauses)  # exact fallback; partial child is discarded
    safe["transaction_attempted_pairs"] = txn["attempted_pairs"]
    safe["transaction_partial_output_bits"] = txn["partial_output_bits"]
    source_scan = sum(len(c) for c in clauses)
    # The selected-event ledger charges the initial literal scan, six literal
    # touches per attempted parent pair, every buffered/output bit, and the
    # full fallback trace.  It is intentionally not called a native-TM count.
    base["source_scan_literal_events"] = source_scan
    base["charged_total_work_proxy"] = source_scan + base["total_work_proxy"]
    safe["source_scan_literal_events"] = source_scan
    safe["resolution_literal_events"] = 6 * txn["attempted_pairs"]
    safe["buffer_write_bit_events"] = txn["partial_output_bits"]
    safe["charged_total_work_proxy"] = (source_scan + 6 * txn["attempted_pairs"] +
                                        txn["partial_output_bits"] +
                                        safe["total_work_proxy"])
    assert base["answer"] == sat == safe["answer"]
    result = {
        "r": r, "label": "SAT" if sat else "UNSAT", "source_clauses": len(clauses),
        "source_variables": meta["nvars"], "source_bits": source_bits,
        "complete_dp_resolvents": len(resolvents), "expected_r_squared": expected,
        "dp_child_clauses": len(child), "dp_child_bits": full["output_bits"],
        "dp_to_source_bit_ratio": full["output_bits"] / source_bits,
        "sqrt_source_bit_budget": math.isqrt(source_bits),
        "proper3_child_clauses": len(proper), "proper3_child_variables": proper_nvars,
        "proper3_child_bits": dimacs_bits(proper, proper_nvars), "bridges": bridges,
        "complete_dp_charged_work_proxy": (source_scan + 6 * expected + full["output_bits"]),
        "complete_dp_peak_explicit_bits": full["output_bits"],
        "baseline_up_dpll": base, "transactional_dp_then_fallback": safe,
        "first_three_resolution_provenance": full["provenance"][:3],
    }
    if controls:
        result["original_clause_SU_controls"] = local_extreme_controls(clauses, meta["nvars"])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--sizes", default="2,4,8,16")
    args = parser.parse_args()
    sizes = [int(x) for x in args.sizes.split(",")]
    tracemalloc.start()
    start = time.perf_counter()
    cases = []
    for r in sizes:
        for sat in (True, False):
            cases.append(run_case(r, sat, controls=(r == min(sizes))))
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    out = {
        "run_id": "ARC-DP-QUADRATIC-OUTPUT-FIREWALL234",
        "status": "PROVED/EXACT family plus COMPUTATIONAL checks",
        "machine": "CPython 3 deterministic RAM; UTF-8 DIMACS bit accounting",
        "elapsed_seconds": elapsed, "python_peak_bytes": peak,
        "same_gadget_both_labels": True,
        "transaction_rule": "abort and discard if explicit DP child exceeds source bits; then exact UP-DPLL fallback",
        "cases": cases,
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(path), "elapsed_seconds": elapsed,
                      "peak_bytes": peak, "cases": len(cases)}, sort_keys=True))


if __name__ == "__main__":
    main()
