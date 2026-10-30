#!/usr/bin/env python3
"""HITTING-CUBE-FIREWALL-REFEREE221.

Clause-indexed extreme-target audit plus a charged hitting-formula controller.
Selected event counters describe this Python implementation; they are not a
RAM, Turing-machine, CDCL, or arbitrary-algorithm lower bound.
"""
from __future__ import annotations

import itertools
import json
import random
import time
import tracemalloc
from collections import Counter

RUN = "HITTING-CUBE-FIREWALL-REFEREE221"
SEED = 202610300548


def false_clause(bits):
    """The clause on variables 1..len(bits) falsified exactly by bits."""
    return tuple(i + 1 if b == 0 else -(i + 1) for i, b in enumerate(bits))


ALL8 = [false_clause(bits) for bits in itertools.product((0, 1), repeat=3)]
REMOVED = false_clause((0, 0, 1))
HIT7 = [c for c in ALL8 if c != REMOVED]
HIT8 = list(ALL8)
XOR_EVEN = [false_clause(bits) for bits in itertools.product((0, 1), repeat=3)
            if sum(bits) % 2 == 1]
DUP_HIT7 = HIT7 + [HIT7[0]]
HORN = [(-1, -2, 3), (-3, -4, -5), (-1, -4, -6), (2, -3, -6)]


def parity3(vars_, charge):
    """Four proper clauses encoding xor(vars_) == charge."""
    return [tuple(v if b == 0 else -v for v, b in zip(vars_, bits))
            for bits in itertools.product((0, 1), repeat=3)
            if sum(bits) % 2 != charge]


# Odd-charge K4 Tseitin contradiction.  Edge variables are
# 12,13,14,23,24,34 -> 1..6.  Gaussian elimination refutes it immediately;
# the generic source controller must not mistake its clause conflicts for a
# new general shortcut.
TSEITIN_K4_ODD = []
for incident, charge in [((1, 2, 3), 1), ((1, 4, 5), 0),
                         ((2, 4, 6), 0), ((3, 5, 6), 0)]:
    TSEITIN_K4_ODD += parity3(incident, charge)


def pad2(c, z):
    return [tuple(c) + (z,), tuple(c) + (-z,)]


PADDED_2SAT = []
for pair in ((1, 2), (1, -2), (-1, 2), (-1, -2)):
    PADDED_2SAT += pad2(pair, 3)

W1 = [(-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
      (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
      (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
      (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
      (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14)]
SWAP6 = [tuple(-lit if abs(lit) == 6 and j in (9, 13) else lit for lit in c)
         for j, c in enumerate(W1)]


def planted_dense():
    rng = random.Random(SEED)
    planted = 0b10110101
    out, seen = [], set()
    while len(out) < 24:
        vs = tuple(sorted(rng.sample(range(1, 9), 3)))
        c = tuple(rng.choice((-1, 1)) * v for v in vs)
        if c in seen:
            continue
        if not any((((planted >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)
                   for lit in c):
            continue
        seen.add(c)
        out.append(c)
    return out


CASES = [
    ("HIT7_BOTH_ENDPOINTS_FAIL_SAT", HIT7),
    ("HIT8_UNSAT", HIT8),
    ("XOR_EVEN_HITTING_SAT", XOR_EVEN),
    ("DUPLICATE_HIT7_SAT", DUP_HIT7),
    ("HORN_SAT", HORN),
    ("PADDED_2SAT_UNSAT", PADDED_2SAT),
    ("TSEITIN_K4_ODD_UNSAT", TSEITIN_K4_ODD),
    ("W1_STRICT22_UNSAT", W1),
    ("SWAP6_STRICT22_SAT", SWAP6),
    ("DENSE_PLANTED_SAT", planted_dense()),
]


def nvars(formula):
    return max(abs(lit) for clause in formula for lit in clause)


def lit_true(lit, assignment):
    return (((assignment >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)


def clause_true_count(clause, assignment):
    return sum(lit_true(lit, assignment) for lit in clause)


def status(formula, assignment):
    counts = [clause_true_count(c, assignment) for c in formula]
    hist = [counts.count(r) for r in range(4)]
    return {
        "assignment_mask": assignment,
        "bitstring_x1_first": "".join(str((assignment >> i) & 1)
                                         for i in range(nvars(formula))),
        "per_original_clause_true_literal_counts": counts,
        "N0_N1_N2_N3": hist,
        "formula_SAT": hist[0] == 0,
    }


def local_targets(formula):
    answer = []
    for j, clause in enumerate(formula):
        occurrences = []
        for p, lit in enumerate(clause):
            s_value = int(lit > 0)
            u_value = 1 - s_value
            occurrences.append({
                "occurrence": f"x_{{{abs(lit)},{j}}}",
                "position": p,
                "literal": lit,
                "explicit_sign": "+" if lit > 0 else "-",
                "preferred_S_value": s_value,
                "S_local_all_literals_true": s_value,
                "invert_S_is_U": 1 - s_value,
                "U_local_all_literals_false": u_value,
                "invert_U_is_S": 1 - u_value,
            })
        answer.append({"clause_index": j, "original_clause": list(clause),
                       "occurrences": occurrences})
    return answer


def target_requirements(clause, mode):
    want_true = mode == "S"
    return {abs(lit): int((lit > 0) == want_true) for lit in clause}


def combine_targets(formula, indices, modes):
    partial, conflicts = {}, set()
    for j, mode in zip(indices, modes):
        for var, value in target_requirements(formula[j], mode).items():
            if var in partial and partial[var] != value:
                conflicts.add(var)
            partial[var] = value
    return not conflicts, sorted(conflicts), partial


def pair_extremes(formula):
    rows = []
    for j, k in itertools.combinations(range(len(formula)), 2):
        cj, ck = formula[j], formula[k]
        shared = sorted(set(map(abs, cj)) & set(map(abs, ck)))
        same, opposite = [], []
        for var in shared:
            sj = next(lit > 0 for lit in cj if abs(lit) == var)
            sk = next(lit > 0 for lit in ck if abs(lit) == var)
            (same if sj == sk else opposite).append(var)
        modes = {}
        union = sorted(set(map(abs, cj)) | set(map(abs, ck)))
        for mode in ("SS", "SU", "US", "UU"):
            symbolic, bad, partial = combine_targets(formula, (j, k), mode)
            witnesses = []
            for bits in itertools.product((0, 1), repeat=len(union)):
                assignment = dict(zip(union, bits))
                values = [sum(assignment[abs(lit)] == int(lit > 0)
                              for lit in formula[q]) for q in (j, k)]
                if all(values[t] == (3 if mode[t] == "S" else 0)
                       for t in range(2)):
                    witnesses.append({str(v): assignment[v] for v in union})
            assert symbolic == bool(witnesses)
            modes[mode] = {
                "feasible": symbolic,
                "conflicting_variables": bad,
                "first_coherent_witness": witnesses[0] if witnesses else None,
                "coherent_witness_count": len(witnesses),
            }
        rows.append({
            "clause_indices": [j, k],
            "same_polarity_shared": same,
            "opposite_polarity_shared": opposite,
            "is_conflict_graph_edge": bool(opposite),
            "modes": modes,
        })
    return rows


def triple_extremes(formula):
    feasible = infeasible = 0
    examples = []
    for indices in itertools.combinations(range(len(formula)), 3):
        for modes in itertools.product("SU", repeat=3):
            ok, bad, _ = combine_targets(formula, indices, modes)
            feasible += int(ok)
            infeasible += int(not ok)
            if len(examples) < 24:
                examples.append({"clause_indices": list(indices),
                                 "mode": "".join(modes), "feasible": ok,
                                 "conflicting_variables": bad})
    return {"feasible_modes": feasible, "infeasible_modes": infeasible,
            "first_24_indexed_modes": examples}


def flip_trails(formula):
    n = nvars(formula)
    trails = []
    sequences = [list(range(1, min(n, 6) + 1)),
                 list(range(min(n, 6), 0, -1))]
    for start in (0, (1 << n) - 1):
        for sequence in sequences:
            assignment = start
            trail = [status(formula, assignment)]
            for var in sequence:
                before = status(formula, assignment)
                assignment ^= 1 << (var - 1)
                after = status(formula, assignment)
                predicted = []
                for clause in formula:
                    delta = sum(1 if not lit_true(lit, before["assignment_mask"]) else -1
                                for lit in clause if abs(lit) == var)
                    predicted.append(before["per_original_clause_true_literal_counts"][
                        len(predicted)] + delta)
                assert predicted == after["per_original_clause_true_literal_counts"]
                trail.append({"flipped_original_variable": var, "state": after})
            trails.append({"start": "0^n" if start == 0 else "1^n",
                           "flip_sequence": sequence, "trail": trail})
    return trails


def source_resolvents(formula, limit=48):
    result = []
    n = nvars(formula)
    for j, k in itertools.combinations(range(len(formula)), 2):
        for pivot_lit in formula[j]:
            if -pivot_lit not in formula[k]:
                continue
            resolvent = tuple(sorted((set(formula[j]) - {pivot_lit}) |
                                     (set(formula[k]) - {-pivot_lit}),
                                     key=lambda x: (abs(x), x)))
            if any(-lit in resolvent for lit in resolvent):
                continue
            cube = {abs(lit): int(lit < 0) for lit in resolvent}
            checked = 0
            for assignment in range(1 << n):
                if all(((assignment >> (var - 1)) & 1) == value
                       for var, value in cube.items()):
                    checked += 1
                    assert not all(any(lit_true(lit, assignment) for lit in formula[q])
                                   for q in (j, k))
            result.append({
                "parent_clause_indices": [j, k],
                "pivot_variable": abs(pivot_lit),
                "resolvent": list(resolvent),
                "prohibited_partial_cube": {str(v): z for v, z in cube.items()},
                "checked_cube_completions": checked,
                "proof": "Falsifying the non-tautological resolvent leaves opposite pivot units in the two indexed source parents.",
            })
            if len(result) >= limit:
                return result
    return result


def conflict_edges(formula, ledger=None):
    edges = []
    for j, k in itertools.combinations(range(len(formula)), 2):
        clash = False
        for a in formula[j]:
            for b in formula[k]:
                if ledger is not None:
                    ledger["literal_pair_comparisons"] += 1
                if a == -b:
                    clash = True
        if clash:
            edges.append((j, k))
    return edges


def is_hitting(formula, ledger=None):
    return len(conflict_edges(formula, ledger)) == len(formula) * (len(formula) - 1) // 2


def exact_enumeration(formula):
    n = nvars(formula)
    models = []
    false_multiplicity = Counter()
    profiles = Counter()
    minimum_middle = None
    for assignment in range(1 << n):
        state = status(formula, assignment)
        false_count = state["N0_N1_N2_N3"][0]
        false_multiplicity[false_count] += 1
        profiles[tuple(state["N0_N1_N2_N3"])] += 1
        if state["formula_SAT"]:
            models.append(assignment)
            middle = sum(state["N0_N1_N2_N3"][1:3])
            minimum_middle = middle if minimum_middle is None else min(minimum_middle, middle)
    return {
        "assignments": 1 << n,
        "model_count": len(models),
        "first_model_mask": models[0] if models else None,
        "first_model_bitstring": ("".join(str((models[0] >> i) & 1) for i in range(n))
                                  if models else None),
        "false_clause_multiplicity_histogram": {str(k): v for k, v in sorted(false_multiplicity.items())},
        "profile_histogram": [{"N0_N1_N2_N3": list(p), "assignments": z}
                              for p, z in sorted(profiles.items())],
        "minimum_middle_clauses_over_models": minimum_middle,
    }


def restrict_formula(formula, var, value):
    reduced = []
    for clause in formula:
        if any(abs(lit) == var and int(lit > 0) == value for lit in clause):
            continue
        reduced.append(tuple(lit for lit in clause if abs(lit) != var))
    return reduced


def hitting_model_count(formula, remaining, ledger):
    ledger["count_calls"] += 1
    if any(len(clause) == 0 for clause in formula):
        return 0
    assert is_hitting(formula, ledger)
    total = 1 << len(remaining)
    for clause in formula:
        ledger["cube_terms"] += 1
        total -= 1 << (len(remaining) - len(clause))
    assert total >= 0
    return total


def hitting_decide_and_witness(formula):
    n = nvars(formula)
    ledger = Counter(literal_pair_comparisons=0, count_calls=0, cube_terms=0,
                     restrictions=0, witness_clause_checks=0)
    if not is_hitting(formula, ledger):
        return None, None, ledger
    remaining = set(range(1, n + 1))
    count = hitting_model_count(formula, remaining, ledger)
    if count == 0:
        ledger["selected_events"] = sum(ledger.values())
        return False, None, ledger
    current = list(formula)
    witness = {}
    for var in range(1, n + 1):
        trial = restrict_formula(current, var, 0)
        ledger["restrictions"] += sum(len(c) for c in current)
        if hitting_model_count(trial, remaining - {var}, ledger) > 0:
            witness[var] = 0
            current = trial
        else:
            witness[var] = 1
            current = restrict_formula(current, var, 1)
            ledger["restrictions"] += sum(len(c) for c in current)
        remaining.remove(var)
    for clause in formula:
        ledger["witness_clause_checks"] += len(clause)
        assert any(witness[abs(lit)] == int(lit > 0) for lit in clause)
    ledger["selected_events"] = sum(v for k, v in ledger.items()
                                    if k != "selected_events")
    return True, witness, ledger


def up(formula, assignment, ledger):
    assignment = dict(assignment)
    while True:
        changed = False
        for clause in formula:
            ledger["clause_scans"] += 1
            if any(abs(lit) in assignment and assignment[abs(lit)] == int(lit > 0)
                   for lit in clause):
                continue
            unassigned = []
            for lit in clause:
                ledger["literal_scans"] += 1
                if abs(lit) not in assignment:
                    unassigned.append(lit)
            if not unassigned:
                return None
            if len(unassigned) == 1:
                lit = unassigned[0]
                var, value = abs(lit), int(lit > 0)
                if var in assignment and assignment[var] != value:
                    return None
                if var not in assignment:
                    assignment[var] = value
                    ledger["unit_assignments"] += 1
                    changed = True
        if not changed:
            return assignment


def dpll(formula, trace_memory=True):
    n = nvars(formula)
    ledger = Counter(nodes=0, branches=0, clause_scans=0,
                     literal_scans=0, unit_assignments=0)

    def recurse(assignment):
        ledger["nodes"] += 1
        closed = up(formula, assignment, ledger)
        if closed is None:
            return None
        if len(closed) == n:
            return closed
        var = next(v for v in range(1, n + 1) if v not in closed)
        for value in (0, 1):
            ledger["branches"] += 1
            found = recurse({**closed, var: value})
            if found is not None:
                return found
        return None

    started = time.perf_counter()
    if trace_memory:
        tracemalloc.start()
    witness = recurse({})
    peak = None
    if trace_memory:
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    ledger["selected_events"] = sum(v for k, v in ledger.items()
                                    if k != "selected_events")
    return {"sat": witness is not None, "witness": witness,
            "selected_events": ledger["selected_events"], "events": dict(ledger),
            "seconds": time.perf_counter() - started, "peak_bytes": peak}


def controller(formula):
    started = time.perf_counter()
    tracemalloc.start()
    answer, witness, hledger = hitting_decide_and_witness(formula)
    fallback = None
    if answer is None:
        fallback = dpll(formula, trace_memory=False)
        answer = fallback["sat"]
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    selected = hledger.get("selected_events", sum(hledger.values()))
    if fallback:
        selected += fallback["selected_events"]
    return {
        "sat": answer,
        "used_hitting_shortcut": fallback is None,
        "hitting_witness": witness,
        "hitting_events": dict(hledger),
        "fallback": fallback,
        "selected_events": selected,
        "seconds": time.perf_counter() - started,
        "peak_bytes": peak,
    }


def audit_case(name, formula):
    started = time.perf_counter()
    pair_rows = pair_extremes(formula)
    exact = exact_enumeration(formula)
    hit = is_hitting(formula)
    if hit:
        predicted = (1 << nvars(formula)) - sum(
            1 << (nvars(formula) - len(c)) for c in formula)
        assert predicted == exact["model_count"]
    else:
        predicted = None
    baseline = dpll(formula)
    augmented = controller(formula)
    assert baseline["sat"] == augmented["sat"] == (exact["model_count"] > 0)
    endpoints = {"0^n": status(formula, 0),
                 "1^n": status(formula, (1 << nvars(formula)) - 1)}
    return {
        "name": name,
        "n": nvars(formula), "m": len(formula),
        "source_formula": [list(c) for c in formula],
        "proper_width_three": all(len(c) == 3 and len(set(map(abs, c))) == 3
                                  for c in formula),
        "local_clause_targets": local_targets(formula),
        "pair_extreme_compatibility": pair_rows,
        "triple_extreme_compatibility": triple_extremes(formula),
        "global_endpoints": endpoints,
        "intermediate_flip_trails": flip_trails(formula),
        "source_resolvent_prohibited_cubes": source_resolvents(formula),
        "conflict_graph": {
            "edges": [list(e) for e in conflict_edges(formula)],
            "complete": hit,
            "edge_count": len(conflict_edges(formula)),
            "all_false_cubes_pairwise_disjoint": hit,
        },
        "exact_enumeration": exact,
        "hitting_closed_form_model_count": predicted,
        "baseline_UP_DPLL": baseline,
        "hitting_prepass_then_fallback": augmented,
        "audit_seconds": time.perf_counter() - started,
    }


def main():
    started = time.perf_counter()
    cases = [audit_case(name, formula) for name, formula in CASES]
    by_name = {c["name"]: c for c in cases}
    assert by_name["HIT7_BOTH_ENDPOINTS_FAIL_SAT"]["exact_enumeration"]["model_count"] == 1
    assert not by_name["HIT7_BOTH_ENDPOINTS_FAIL_SAT"]["global_endpoints"]["0^n"]["formula_SAT"]
    assert not by_name["HIT7_BOTH_ENDPOINTS_FAIL_SAT"]["global_endpoints"]["1^n"]["formula_SAT"]
    assert by_name["HIT7_BOTH_ENDPOINTS_FAIL_SAT"]["exact_enumeration"]["minimum_middle_clauses_over_models"] == 6
    assert by_name["HIT8_UNSAT"]["exact_enumeration"]["model_count"] == 0
    out = {
        "run_id": RUN,
        "timestamp": "2026-10-30T05:48:00-07:00",
        "seed": SEED,
        "claims": {
            "known_hitting_theorem": "If every two source clauses clash, their falsifying cubes are pairwise disjoint and the exact model count is 2^n-sum_C 2^(n-|C|).",
            "proper_3cnf_corollary": "A hitting proper width-three formula has at most eight clauses and is UNSAT iff it has exactly eight clauses.",
            "falsifier": "The seven-clause fixed-support hitting formula has complete conflict graph and both endpoints fail, yet has the unique model 001 and exactly six middle clauses.",
            "scope": "Restricted hitting formulas; no arbitrary-SAT or P-versus-NP implication.",
        },
        "cases": cases,
        "summary": {
            "cases": len(cases),
            "total_complete_assignments": sum(c["exact_enumeration"]["assignments"] for c in cases),
            "total_occurrences": sum(3 * c["m"] for c in cases),
            "total_pair_modes": sum(4 * len(c["pair_extreme_compatibility"]) for c in cases),
            "total_triple_modes": sum(c["triple_extreme_compatibility"]["feasible_modes"] +
                                      c["triple_extreme_compatibility"]["infeasible_modes"] for c in cases),
            "total_resolvent_cube_completions": sum(
                sum(r["checked_cube_completions"] for r in c["source_resolvent_prohibited_cubes"])
                for c in cases),
            "all_controller_answers_match_exact_enumeration": all(
                c["hitting_prepass_then_fallback"]["sat"] ==
                (c["exact_enumeration"]["model_count"] > 0) for c in cases),
            "hitting_cases": [c["name"] for c in cases if c["conflict_graph"]["complete"]],
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    with open("2026-10-30_0548_HITTING-CUBE-FIREWALL-REFEREE221_raw.json", "w") as handle:
        json.dump(out, handle, indent=2, sort_keys=True)
    summary = {
        "run_id": RUN, "summary": out["summary"], "elapsed_seconds": out["elapsed_seconds"],
        "cases": [{
            "name": c["name"], "n": c["n"], "m": c["m"],
            "hitting": c["conflict_graph"]["complete"],
            "models": c["exact_enumeration"]["model_count"],
            "minimum_middle": c["exact_enumeration"]["minimum_middle_clauses_over_models"],
            "endpoint_0_sat": c["global_endpoints"]["0^n"]["formula_SAT"],
            "endpoint_1_sat": c["global_endpoints"]["1^n"]["formula_SAT"],
            "baseline_nodes": c["baseline_UP_DPLL"]["events"]["nodes"],
            "baseline_events": c["baseline_UP_DPLL"]["selected_events"],
            "controller_used_hitting": c["hitting_prepass_then_fallback"]["used_hitting_shortcut"],
            "controller_events": c["hitting_prepass_then_fallback"]["selected_events"],
            "baseline_seconds": c["baseline_UP_DPLL"]["seconds"],
            "controller_seconds": c["hitting_prepass_then_fallback"]["seconds"],
            "baseline_peak_bytes": c["baseline_UP_DPLL"]["peak_bytes"],
            "controller_peak_bytes": c["hitting_prepass_then_fallback"]["peak_bytes"],
        } for c in cases],
    }
    with open("2026-10-30_0548_HITTING-CUBE-FIREWALL-REFEREE221_summary.json", "w") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
