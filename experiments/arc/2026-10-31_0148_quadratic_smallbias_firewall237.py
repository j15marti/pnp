#!/usr/bin/env python3
"""Exact finite audit for AFFINE-TO-QUADRATIC-SMALLBIAS-FIREWALL237.

No external packages.  Exhaustive chunks are deliberately <= 2^10 points.
The asymptotic theorem in the report is symbolic; these computations only replay
the finite identities and the original-clause SAT/UNSAT hostile controls.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import tracemalloc
from pathlib import Path

RUN = "AFFINE-TO-QUADRATIC-SMALLBIAS-FIREWALL237"


def parity(x: int) -> int:
    return x.bit_count() & 1


def qform(x: int, r: int) -> int:
    return parity(sum((((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1)) << i
                      for i in range(r)))


def qform_simple(x: int, r: int) -> int:
    v = 0
    for i in range(r):
        v ^= ((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1)
    return v


def bent_enumeration(r: int) -> dict:
    n = 2*r
    universe = list(range(1 << n))
    zero = [x for x in universe if qform_simple(x, r) == 0]
    one = len(universe) - len(zero)
    expected_zero = (1 << (2*r-1)) + (1 << (r-1))
    expected_one = (1 << (2*r-1)) - (1 << (r-1))
    assert len(zero) == expected_zero and one == expected_one
    max_num = 0
    spectrum = {}
    for a in range(1, 1 << n):
        num = sum(1 if parity(a & x) == 0 else -1 for x in zero)
        max_num = max(max_num, abs(num))
        spectrum[str(num)] = spectrum.get(str(num), 0) + 1
    # Restricting to q=0 multiplies by (1+(-1)^q)/2, hence half
    # of the unnormalised bent Walsh coefficient 2^r.
    assert max_num == (1 << (r-1))
    return {
        "r": r, "ambient_bits": n, "points": 1 << n,
        "zero_set_size": len(zero), "one_set_size": one,
        "max_nonzero_linear_bias_numerator": max_num,
        "max_nonzero_linear_bias_denominator": len(zero),
        "max_nonzero_linear_bias": max_num / len(zero),
        "predicted_bias": 1 / ((1 << r) + 1),
        "quadratic_gap_numerator": one,
        "quadratic_gap_denominator": 1 << n,
        "quadratic_gap": one / (1 << n),
        "walsh_numerator_spectrum_on_zero_set": spectrum,
        "assertions": 5 + ((1 << n) - 1),
    }


def clause_true_count(clause, assignment):
    return sum((assignment[abs(l)] if l > 0 else 1-assignment[abs(l)]) for l in clause)


def all_signed_clauses():
    out = []
    for signs in itertools.product([1, -1], repeat=3):
        out.append(tuple(signs[i]*(i+1) for i in range(3)))
    return out


def model_count(formula):
    models = []
    for bits in itertools.product([0, 1], repeat=3):
        a = {i+1: bits[i] for i in range(3)}
        if all(clause_true_count(c, a) >= 1 for c in formula):
            models.append(bits)
    return models


def dpll(formula, assignment=None, stats=None):
    if assignment is None: assignment = {}
    if stats is None: stats = {"nodes": 0, "literal_tests": 0}
    stats["nodes"] += 1
    while True:
        changed = False
        for c in formula:
            vals, unset = [], []
            for l in c:
                stats["literal_tests"] += 1
                v = abs(l)
                if v in assignment:
                    vals.append(assignment[v] if l > 0 else 1-assignment[v])
                else:
                    unset.append(l)
            if any(vals): continue
            if not unset: return False, None, stats
            if len(unset) == 1:
                l = unset[0]
                assignment[abs(l)] = 1 if l > 0 else 0
                changed = True
                break
        if not changed: break
    if all(any((assignment.get(abs(l), -1) if l > 0 else
                (1-assignment.get(abs(l), 2) if abs(l) in assignment else -1)) == 1
               for l in c) for c in formula):
        full = assignment.copy()
        for v in range(1, 4): full.setdefault(v, 0)
        return True, full, stats
    v = next(v for v in range(1, 4) if v not in assignment)
    for b in (0, 1):
        ok, wit, stats = dpll(formula, {**assignment, v: b}, stats)
        if ok: return True, wit, stats
    return False, None, stats


def extreme_controls(name, formula):
    occurrences = []
    for j, c in enumerate(formula):
        for l in c:
            s = 1 if l > 0 else 0
            occurrences.append({"clause": j, "var": abs(l), "sign": "+" if l > 0 else "-",
                                "S": s, "invert_S_is_U": 1-s,
                                "U": 1-s, "invert_U_is_S": s})
    pair_modes = []
    for j in range(len(formula)):
        for k in range(j+1, len(formula)):
            cj = {abs(l): l > 0 for l in formula[j]}
            ck = {abs(l): l > 0 for l in formula[k]}
            shared = set(cj) & set(ck)
            same = any(cj[v] == ck[v] for v in shared)
            opposite = any(cj[v] != ck[v] for v in shared)
            predicted = {"SS": not opposite, "UU": not opposite,
                         "SU": not same, "US": not same}
            actual = {}
            for mode in ("SS", "SU", "US", "UU"):
                req = {}
                good = True
                for which, clause in zip(mode, (formula[j], formula[k])):
                    for l in clause:
                        val = (1 if l > 0 else 0) if which == "S" else (0 if l > 0 else 1)
                        v = abs(l)
                        if v in req and req[v] != val: good = False
                        req[v] = val
                actual[mode] = good
            assert actual == predicted
            pair_modes.append({"j": j, "k": k, "same": same, "opposite": opposite,
                               "predicted": predicted, "actual": actual})
    endpoints = []
    for bits in ((0,0,0),(1,1,1),(0,0,1),(1,1,0)):
        a = {i+1: bits[i] for i in range(3)}
        counts = [clause_true_count(c, a) for c in formula]
        comp = {i+1: 1-bits[i] for i in range(3)}
        cc = [clause_true_count(c, comp) for c in formula]
        assert all(cc[i] == 3-counts[i] for i in range(len(counts)))
        endpoints.append({"assignment": bits, "truth_counts": counts,
                          "N": [counts.count(i) for i in range(4)],
                          "complement_truth_counts": cc})
    models = model_count(formula)
    ok, witness, stats = dpll(formula)
    assert ok == bool(models)
    if ok:
        assert all(clause_true_count(c, witness) >= 1 for c in formula)
    return {"name": name, "clauses": formula, "models": models, "model_count": len(models),
            "dpll": {"sat": ok, "witness": witness, **stats},
            "occurrences": occurrences, "pair_modes": pair_modes, "endpoints_and_flips": endpoints,
            "assertions": len(occurrences)*4 + len(pair_modes)*4 + len(endpoints)*(len(formula)+1) + 3}


def main():
    tracemalloc.start()
    bent = [bent_enumeration(r) for r in range(1, 6)]
    symbolic = []
    for r in range(1, 21):
        symbolic.append({
            "r": r,
            "zero_size": (1 << (2*r-1)) + (1 << (r-1)),
            "one_size": (1 << (2*r-1)) - (1 << (r-1)),
            "epsilon_numerator": 1,
            "epsilon_denominator": (1 << r) + 1,
            "quadratic_gap_numerator": (1 << r) - 1,
            "quadratic_gap_denominator": 2*(1 << r),
        })
    clauses = all_signed_clauses()
    h8 = extreme_controls("H8_UNSAT", clauses)
    # Remove the clause falsified by 001, leaving its unique model.
    target = {1:0, 2:0, 3:1}
    removed = next(c for c in clauses if clause_true_count(c, target) == 0)
    h7 = extreme_controls("H7_SAT", [c for c in clauses if c != removed])
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    out = {
        "run": RUN,
        "status": {"bent_firewall": "PROVED/EXACT symbolic; finite replay COMPUTATIONAL",
                   "affine_smallbias": "NOT REFUTED; restricted theorem preserved",
                   "sat_arc": "OPEN", "p_vs_np": "OPEN"},
        "symbolic_exact_rows": symbolic,
        "exhaustive_bent_rows": bent,
        "same_source_sat_unsat_controls": [h7, h8],
        "ledger": {
            "enumerated_points": sum(x["points"] for x in bent),
            "linear_character_sums": sum((x["points"]-1)*x["zero_set_size"] for x in bent),
            "producer_assertion_groups": sum(x["assertions"] for x in bent)+h7["assertions"]+h8["assertions"]+20,
            "tracemalloc_current_bytes": current, "tracemalloc_peak_bytes": peak,
            "chunking": "independent r=1..5 chunks; each at most 2^10 ambient points"
        },
        "limitations": [
            "The bent zero-set distribution is not the CHMY easy-source ensemble.",
            "The result blocks extending a small-bias-only proof to quadratic maps; it is not SAT hardness.",
            "Python events and allocation are not FLMV machine resources."
        ]
    }
    path = Path("results/raw/arc/2026-10-31_0148_LSPV5_QUADRATIC_SMALLBIAS_FIREWALL237_raw.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(out, indent=2, sort_keys=True)
    path.write_text(text+"\n", encoding="utf-8")
    digest = hashlib.sha256((text+"\n").encode()).hexdigest()
    print(json.dumps({"path": str(path), "sha256": digest, "ledger": out["ledger"],
                      "H7_models": h7["model_count"], "H8_models": h8["model_count"],
                      "r5_epsilon": bent[-1]["predicted_bias"],
                      "r5_quadratic_gap": bent[-1]["quadratic_gap"]}, indent=2))


if __name__ == "__main__":
    main()
