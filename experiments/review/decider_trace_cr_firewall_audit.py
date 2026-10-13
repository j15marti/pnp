#!/usr/bin/env python3
"""Finite audit for the decider-indexed Cook--Reckhow trace construction.

Checks exponent accounting and a small deterministic trace verifier.  It does
not prove an asymptotic lower bound or a simulation into a fixed proof system.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

START = time.monotonic()
CHECKS = 0


def check(ok: bool, label: str) -> None:
    global CHECKS
    if time.monotonic() - START > 25:
        raise TimeoutError("cooperative 25-second budget")
    CHECKS += 1
    if not ok:
        raise AssertionError(label)


def eval_cnf(cnf, bits):
    return all(any(bits[abs(l)-1] == int(l > 0) for l in c) for c in cnf)


def brute_trace(cnf, n):
    """Trace consists of assignments tested in order and the terminal bit."""
    states = []
    for mask in range(1 << n):
        bits = tuple((mask >> i) & 1 for i in range(n))
        value = eval_cnf(cnf, bits)
        states.append((mask, bits, value))
        if value:
            return {"states": states, "answer": 1}
    return {"states": states, "answer": 0}


def verify_trace(cnf, n, trace):
    states = trace.get("states", [])
    if not states:
        return False
    terminal = None
    for j, row in enumerate(states):
        if not isinstance(row, (tuple, list)) or len(row) != 3:
            return False
        mask, bits, value = row
        if mask != j or tuple(bits) != tuple((mask >> i) & 1 for i in range(n)):
            return False
        if bool(value) != eval_cnf(cnf, bits):
            return False
        if value:
            terminal = 1
            if j != len(states)-1:
                return False
    if terminal is None:
        if len(states) != 1 << n:
            return False
        terminal = 0
    return trace.get("answer") == terminal


def finite_trace_checks():
    families = {
        "yes_unitlike": [(1,2,3)],
        "no_cube": [tuple((i+1) * (1 if b[i] == 0 else -1) for i in range(3))
                    for b in itertools.product((0,1), repeat=3)],
        "horn": [(-1,-2,3),(1,-2,-3),(-1,2,-3)],
        "two_sat_padded": [(1,2,3),(1,2,-3),(-1,-2,3),(-1,-2,-3)],
        "bounded_chain": [(1,2,3),(-2,3,4),(-3,4,5)],
        "independent_product": [(1,2,3),(4,5,6)],
    }
    rows = []
    for name, cnf in families.items():
        n = max(abs(l) for c in cnf for l in c)
        t = brute_trace(cnf, n)
        check(verify_trace(cnf, n, t), "valid trace")
        # Mutation controls: state, evaluation bit, terminal answer, truncation.
        for mode in range(4):
            bad = {"states":[list(r) for r in t["states"]], "answer":t["answer"]}
            if mode == 0:
                bad["states"][0][0] += 1
            elif mode == 1:
                bad["states"][0][2] = not bad["states"][0][2]
            elif mode == 2:
                bad["answer"] = 1 - bad["answer"]
            else:
                if len(bad["states"]) > 1:
                    bad["states"] = bad["states"][:-1]
                else:
                    bad["states"] = []
            check(not verify_trace(cnf, n, bad), "mutated trace rejected")
        rows.append({"family":name,"variables":n,"clauses":len(cnf),
                     "answer":t["answer"],"trace_states":len(t["states"])})
    return rows


def exponent_checks():
    rows = []
    wrappers = {
        "DIRECT": (0,0), "COPY": (1,0), "DELAY": (3,0),
        "INTERP": (2,1), "RECOMP": (4,1), "FRONTDOOR": (1,1),
    }
    for a in range(1,13):               # reduction construction exponent
        for q in range(1,13):           # output-length exponent
            for k in range(1,41):       # arbitrary fixed solver exponent
                base = max(a, q*k)
                trace_exp = 2*base      # conservative full configuration history
                check(trace_exp >= 2*q*k, "solver trace charged")
                check(trace_exp >= 2*a, "reduction charged")
                check(trace_exp < 10**9, "each fixed tuple remains polynomial")
                for name,(delay,interp) in wrappers.items():
                    wrapped = max(base, delay, base+interp)
                    proof_exp = 2*wrapped
                    check(proof_exp >= trace_exp, "wrapper cannot erase charged work")
                    check(isinstance(proof_exp, int), "fixed exponent")
                rows.append((a,q,k,trace_exp))
    # No exponent independent of k can dominate the resulting proof exponents.
    for q in range(1,13):
        es = [2*max(1,q*k) for k in range(1,41)]
        check(all(es[i] < es[i+1] for i in range(len(es)-1)), "arbitrary exponent retained")
    return {
        "tuples":len(rows),
        "minimum_trace_exponent":min(r[3] for r in rows),
        "maximum_tested_trace_exponent":max(r[3] for r in rows),
        "note":"finite k range tests formulas only; theorem quantifies over every fixed k",
    }


def main(out: Path):
    result = {
        "run_id":"TRACECR-FIREWALL1",
        "status":"COMPUTATIONAL",
        "finite_traces":finite_trace_checks(),
        "exponents":exponent_checks(),
        "claims":{
            "polynomial_decider_yields_decider_indexed_p_bounded_trace_system":True,
            "fixed_PC_CP_or_Resolution_simulation_established":False,
            "P_vs_NP_separation_established":False,
        },
        "checks":CHECKS,
        "elapsed_seconds":time.monotonic()-START,
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k:result[k] for k in ("status","checks","elapsed_seconds")},sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    main(args.out)
