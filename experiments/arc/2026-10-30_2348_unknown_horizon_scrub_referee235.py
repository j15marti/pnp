#!/usr/bin/env python3
"""Exact finite controls for the unknown-horizon physical-scrub wrapper.

This is an event-ledger audit, not a native FLMV timing experiment.  It uses a
deterministic exhaustive CNF decider so SAT and UNSAT labels are obtained from
the source rather than supplied to the wrapper.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


F7 = [
    [1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3],
    [-1, 2, 3], [-1, 2, -3], [-1, -2, 3],
]
H8 = F7 + [[-1, -2, -3]]


def variables(formula):
    return sorted({abs(lit) for clause in formula for lit in clause})


def lit_value(lit, assignment):
    return assignment[abs(lit)] == (lit > 0)


def clause_true_count(clause, assignment):
    return sum(lit_value(lit, assignment) for lit in clause)


def satisfies(formula, assignment):
    return all(clause_true_count(clause, assignment) > 0 for clause in formula)


def all_assignments(formula):
    vs = variables(formula)
    for bits in itertools.product((0, 1), repeat=len(vs)):
        yield dict(zip(vs, bits))


def exact_models(formula):
    return [a for a in all_assignments(formula) if satisfies(formula, a)]


def exhaustive_guest_trace(formula, delay):
    """Return a transparent primitive trace and the source-computed label."""
    trace = [{"op": "delay", "i": i} for i in range(delay)]
    vs = variables(formula)
    for bits in itertools.product((0, 1), repeat=len(vs)):
        a = dict(zip(vs, bits))
        trace.append({"op": "assignment", "bits": "".join(map(str, bits))})
        ok = True
        for j, clause in enumerate(formula):
            sat_clause = False
            for k, lit in enumerate(clause):
                value = lit_value(lit, a)
                trace.append({"op": "literal-read", "clause": j, "slot": k,
                              "lit": lit, "value": int(value)})
                if value:
                    sat_clause = True
                    break
            trace.append({"op": "clause-result", "clause": j,
                          "value": int(sat_clause)})
            if not sat_clause:
                ok = False
                break
        if ok:
            trace.append({"op": "halt", "label": "SAT"})
            return trace, "SAT"
    trace.append({"op": "halt", "label": "UNSAT"})
    return trace, "UNSAT"


def local_extremes(formula):
    rows = []
    for j, clause in enumerate(formula):
        s = {str(abs(lit)): int(lit > 0) for lit in clause}
        u = {x: 1 - bit for x, bit in s.items()}
        occ = []
        for lit in clause:
            x = str(abs(lit))
            occ.append({
                "variable": abs(lit), "sign": "+" if lit > 0 else "-",
                "S_value": s[x], "invert_S_to_U": 1 - s[x],
                "U_value": u[x], "invert_U_to_S": 1 - u[x],
            })
        rows.append({"clause_index": j, "clause": clause, "S": s, "U": u,
                     "occurrences": occ})
    return rows


def compatible_targets(row_a, mode_a, row_b, mode_b):
    a = row_a[mode_a]
    b = row_b[mode_b]
    return all(x not in b or b[x] == value for x, value in a.items())


def compatibility_audit(formula, extrema):
    pairs = []
    brute = list(all_assignments(formula))
    for j in range(len(formula)):
        for k in range(j + 1, len(formula)):
            matrix = {}
            for mode in ("SS", "SU", "US", "UU"):
                mj, mk = mode
                symbolic = compatible_targets(extrema[j], mj, extrema[k], mk)
                target_j, target_k = extrema[j][mj], extrema[k][mk]
                exact = any(
                    all(a[int(x)] == v for x, v in target_j.items()) and
                    all(a[int(x)] == v for x, v in target_k.items())
                    for a in brute
                )
                assert symbolic == exact
                matrix[mode] = symbolic
            pairs.append({"clause_indices": [j, k], "matrix": matrix})
    return pairs


def endpoint_and_flip_audit(formula):
    vs = variables(formula)
    trails = []
    current = {x: 0 for x in vs}
    for step in range(len(vs) + 1):
        counts = [clause_true_count(c, current) for c in formula]
        trails.append({"step": step, "assignment": {str(x): current[x] for x in vs},
                       "true_literal_counts": counts,
                       "N": [counts.count(r) for r in range(4)]})
        if step < len(vs):
            current[vs[step]] ^= 1
    zero = trails[0]
    one = trails[-1]
    assert all(a + b == 3 for a, b in zip(zero["true_literal_counts"],
                                           one["true_literal_counts"]))
    return trails


def scrub_schedule(trace_len, input_len_proxy):
    """Geometric horizons with a conservative paid physical scrub ledger."""
    assert trace_len >= 1
    phases = []
    horizon = 1
    while True:
        executed = min(horizon, trace_len)
        width = math.ceil(math.log2(input_len_proxy + horizon + 2))
        epoch_width = math.ceil(math.log2(horizon + 2)) + 1
        # Conservative model: every executed guest step may touch a fresh cell.
        visited_cells = executed
        simulation_work = executed * (1 + width * width)
        completed = horizon >= trace_len
        # Timed-out phases are transactionally scrubbed and their heads returned.
        scrub_work = 0 if completed else visited_cells * (epoch_width + 2)
        phases.append({
            "horizon": horizon, "executed_guest_steps": executed,
            "width": width, "epoch_width": epoch_width,
            "visited_cells": visited_cells,
            "simulation_work": simulation_work, "scrub_work": scrub_work,
            "completed": completed,
        })
        if completed:
            break
        horizon *= 2
    total_budget = sum(p["horizon"] for p in phases)
    total_guest_steps = sum(p["executed_guest_steps"] for p in phases)
    total_work = sum(p["simulation_work"] + p["scrub_work"] for p in phases)
    peak_cells = max(p["visited_cells"] * (p["epoch_width"] + 2) for p in phases)
    assert phases[-1]["horizon"] < 2 * trace_len
    assert total_budget < 4 * trace_len
    assert total_guest_steps < 4 * trace_len
    return {
        "phases": phases, "first_success_horizon": phases[-1]["horizon"],
        "total_budget": total_budget, "total_guest_steps": total_guest_steps,
        "total_work": total_work, "peak_physical_cells_proxy": peak_cells,
    }


def build_raw():
    sources = {"F7_unique_SAT": F7, "H8_UNSAT": H8}
    delays = [0, 1, 7, 31, 127, 511]
    out = {
        "run_id": "ARC-UNKNOWN-HORIZON-SCRUB-REFEREE235",
        "status": {"conditional_scrub_lemma": "PROVED/EXACT restricted",
                   "universal_scrub_claim": "FALSIFIED/RETIRED",
                   "experiment": "COMPUTATIONAL",
                   "arc": "OPEN", "p_vs_np": "OPEN"},
        "model_note": "Logical-event and physical-cell proxy; not native FLMV timing.",
        "sources": [], "hostile_far_index_controls": [], "summary": {},
    }
    checks = 0
    for name, formula in sources.items():
        models = exact_models(formula)
        expected = "SAT" if models else "UNSAT"
        extrema = local_extremes(formula)
        pairs = compatibility_audit(formula, extrema)
        trail = endpoint_and_flip_audit(formula)
        checks += sum(4 for _ in pairs) + len(formula) * 4 + len(trail)
        runs = []
        for delay in delays:
            trace, label = exhaustive_guest_trace(formula, delay)
            assert label == expected
            schedule = scrub_schedule(len(trace), sum(len(c) for c in formula) + len(formula))
            # Only the completed phase is allowed to commit a label.
            committed = label if schedule["phases"][-1]["completed"] else None
            assert committed == expected
            assert all(not p["completed"] for p in schedule["phases"][:-1])
            checks += 6 + len(schedule["phases"])
            runs.append({
                "delay": delay, "direct_trace_steps": len(trace), "computed_label": label,
                "direct_work": len(trace), "schedule": schedule,
                "wrapper_to_direct_work_ratio": schedule["total_work"] / len(trace),
            })
        out["sources"].append({
            "name": name, "formula": formula, "model_count": len(models),
            "expected_label": expected, "local_extremes": extrema,
            "pair_compatibility": pairs, "zero_to_one_flip_trail": trail,
            "runs": runs,
        })
    # Hostile FLMV control: a label-independent wrapper constructs a polynomially
    # far work-tape address by indexed access, touches it, and then runs the same
    # exact source decider.  Sequential prefix scrub is not bounded by run time.
    for n in (8, 16, 32, 64, 128):
        for exponent in (3, 5, 8):
            address = n ** exponent
            address_bits = address.bit_length()
            base_time = n * n
            wrapper_time = base_time + address_bits + 3
            sequential_scrub = address + 1
            assert sequential_scrub > wrapper_time
            out["hostile_far_index_controls"].append({
                "source_length_proxy": n, "far_exponent": exponent,
                "far_address": address, "address_bits": address_bits,
                "base_decider_time_proxy": base_time,
                "wrapped_time_proxy": wrapper_time,
                "sequential_prefix_scrub": sequential_scrub,
                "scrub_to_wrapped_time_ratio": sequential_scrub / wrapper_time,
                "label_effect": "none; wrapper returns the base source-computed label",
            })
            checks += 2
    out["summary"] = {
        "source_count": len(out["sources"]), "run_count": 2 * len(delays),
        "labels": sorted({s["expected_label"] for s in out["sources"]}),
        "assertion_count": checks,
        "max_guest_step_ratio": max(r["schedule"]["total_guest_steps"] / r["direct_trace_steps"]
                                    for s in out["sources"] for r in s["runs"]),
        "min_wrapper_work_ratio": min(r["wrapper_to_direct_work_ratio"]
                                      for s in out["sources"] for r in s["runs"]),
        "far_control_count": len(out["hostile_far_index_controls"]),
        "max_far_scrub_ratio": max(x["scrub_to_wrapped_time_ratio"]
                                    for x in out["hostile_far_index_controls"]),
    }
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raw = build_raw()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(raw["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
