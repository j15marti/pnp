#!/usr/bin/env python3
"""Finite audit for certified dovetailed solver (not an asymptotic SAT proof).
Each of the eight proper clauses on three variables excludes one assignment.
A formula is SAT iff its 8-bit clause mask is not 255. Program certification
here exhausts ONLY the 256 finite formulas; it is NOT a formal all-length proof.
"""
import json
from collections import Counter
from pathlib import Path
OUT = Path(__file__).with_name("audit_results.json")
PROGRAMS = {
    "brute": {"code": "0000"},
    "guarded": {"code": "001000"},
    "padded": {"code": "001011"},
    "direct": {"code": "001010000"},
    "wrong_yes": {"code": "01000"},
    "wrong_no": {"code": "01001"},
}
def specification(mask):
    return mask != 255
def trace(name, mask):
    if name == "wrong_yes":
        return [True]
    if name == "wrong_no":
        return [False]
    if name == "direct":
        return [specification(mask)]
    if name == "guarded" and mask == 255:
        return [False]
    core = [None if (mask & (1 << a)) else True for a in range(8)]
    if True in core:
        core = core[:core.index(True) + 1]
    else:
        core[-1] = False
    return ([None] * 13 + core) if name == "padded" else core
def finite_certified_programs():
    yes, no = [], []
    for name in PROGRAMS:
        ok = all(trace(name, mask)[-1] == specification(mask) for mask in range(256))
        (yes if ok else no).append(name)
    return yes, no
def staged_race(mask, certified, max_stage=20):
    guest_steps = 0
    for stage in range(1, max_stage + 1):
        for name in certified:
            b = len(PROGRAMS[name]["code"])
            if b > stage:
                continue
            budget = 1 << (stage - b)
            steps = trace(name, mask)
            guest_steps += min(len(steps), budget)
            if len(steps) <= budget:
                return {"result": steps[-1], "winner": name,
                        "stage": stage, "guest_steps": guest_steps}
    raise AssertionError("A certified baseline must halt")
def run_audit():
    codes = [d["code"] for d in PROGRAMS.values()]
    assert len(codes) == len(set(codes))
    assert all(not d.startswith(c) for i, c in enumerate(codes)
               for j, d in enumerate(codes) if i != j)
    certified, rejected = finite_certified_programs()
    assert set(certified) == {"brute", "guarded", "padded", "direct"}
    assert set(rejected) == {"wrong_yes", "wrong_no"}
    wins = Counter()
    maximum_steps = 0
    max_ratio = 0.0
    total_trace = 0
    for mask in range(256):
        out = staged_race(mask, certified)
        assert out["result"] == specification(mask)
        wins[out["winner"]] += 1
        maximum_steps = max(maximum_steps, out["guest_steps"])
        best = min((1 << len(PROGRAMS[name]["code"])) * len(trace(name, mask))
                   for name in certified)
        max_ratio = max(max_ratio, out["guest_steps"] / best)
        total_trace += sum(len(trace(name, mask)) for name in PROGRAMS)
        for name in certified:
            b = len(PROGRAMS[name]["code"])
            t = len(trace(name, mask))
            assert out["guest_steps"] <= 10 * (b + t.bit_length() + 2) * (1 << b) * t
    assert sum(wins.values()) == 256
    return {
        "universe": "all proper three-variable width-three clause subsets",
        "formulas_tested": 256,
        "candidate_programs": 6,
        "toy_finite_certified": certified,
        "toy_finite_rejected": rejected,
        "solver_output_mismatches": 0,
        "per_candidate_dovetail_controls": 256 * len(certified),
        "winner_counts": dict(sorted(wins.items())),
        "maximum_abstract_guest_steps": maximum_steps,
        "maximum_ratio_guest_steps_to_weighted_best": max_ratio,
        "total_independent_trace_steps_counted": total_trace,
        "proof_scope": "bounded finite semantics, not proofs for general SAT",
        "machine_scope": "guest-step fairness only; physical simulation and proof verification extra",
        "P_vs_NP": "OPEN",
    }
if __name__ == "__main__":
    result = run_audit()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
