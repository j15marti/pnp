#!/usr/bin/env python3
"""Finite controls for REFEREE334's node/bit normalization firewall."""
from __future__ import annotations

import json
import resource


def well_formed(cnf):
    if not isinstance(cnf, dict) or not isinstance(cnf.get("n"), int) or cnf["n"] < 0:
        return False
    if not isinstance(cnf.get("clauses"), list):
        return False
    n = cnf["n"]
    for clause in cnf["clauses"]:
        if not isinstance(clause, list):
            return False
        for lit in clause:
            if not isinstance(lit, int) or lit == 0 or abs(lit) > n:
                return False
    return True


def clause_value(clause, assignment):
    return any((assignment[abs(lit) - 1] if lit > 0 else not assignment[abs(lit) - 1]) for lit in clause)


def assignment_bits(n, number):
    return tuple(bool((number >> i) & 1) for i in range(n))


def decide_with_trace(cnf):
    assert well_formed(cnf)
    rows = []
    for number in range(1 << cnf["n"]):
        a = assignment_bits(cnf["n"], number)
        failed = next((i for i, c in enumerate(cnf["clauses"]) if not clause_value(c, a)), None)
        if failed is None:
            return {"label": "SAT", "witness": list(a), "rows": rows}
        rows.append({"number": number, "assignment": list(a), "failed_clause": failed})
    return {"label": "UNSAT", "rows": rows}


def verify_unsat_trace(cnf, proof):
    if not well_formed(cnf) or not isinstance(proof, dict) or proof.get("label") != "UNSAT":
        return False
    rows = proof.get("rows")
    if not isinstance(rows, list) or len(rows) != (1 << cnf["n"]):
        return False
    for number, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("number") != number:
            return False
        a = assignment_bits(cnf["n"], number)
        if row.get("assignment") != list(a):
            return False
        i = row.get("failed_clause")
        if not isinstance(i, int) or i < 0 or i >= len(cnf["clauses"]):
            return False
        if clause_value(cnf["clauses"][i], a):
            return False
    return True


def truth_cnf(n, truth_mask):
    clauses = []
    for number in range(1 << n):
        if not ((truth_mask >> number) & 1):
            a = assignment_bits(n, number)
            clauses.append([-(i + 1) if bit else i + 1 for i, bit in enumerate(a)])
    return {"n": n, "clauses": clauses}


def horn_chain(k):
    clauses = [[1]]
    clauses += [[-i, i + 1] for i in range(1, k)]
    clauses += [[-k]]
    return {"n": k, "clauses": clauses}


def chain_resolution_payload(k):
    steps = []
    current = 0
    for i in range(1, k):
        steps.append({"pivot": i, "left": current, "right": i, "result": [i + 1]})
        current = k + 1 + len(steps) - 1
    steps.append({"pivot": k, "left": current, "right": k, "result": []})
    return {"kind": "RES_CHAIN", "k": k, "steps": steps}


def verify_chain_payload(payload):
    if not isinstance(payload, dict) or payload.get("kind") != "RES_CHAIN":
        return False
    k, steps = payload.get("k"), payload.get("steps")
    if not isinstance(k, int) or k < 1 or not isinstance(steps, list) or len(steps) != k:
        return False
    expected = [[i + 2] for i in range(k - 1)] + [[]]
    return all(isinstance(s, dict) and s.get("pivot") == i + 1 and s.get("result") == expected[i]
               for i, s in enumerate(steps))


checks = 0


def check(value, message):
    global checks
    if not value:
        raise AssertionError(message)
    checks += 1


truth_fixtures = 0
sat_fixtures = 0
unsat_fixtures = 0
for n in range(1, 4):
    for truth_mask in range(1 << (1 << n)):
        cnf = truth_cnf(n, truth_mask)
        trace = decide_with_trace(cnf)
        truth_fixtures += 1
        check(well_formed(cnf), "generated CNF malformed")
        if truth_mask == 0:
            unsat_fixtures += 1
            check(trace["label"] == "UNSAT", "UNSAT label")
            check(verify_unsat_trace(cnf, trace), "valid trace rejected")
        else:
            sat_fixtures += 1
            check(trace["label"] == "SAT", "SAT label")
            fake = {"label": "UNSAT", "rows": trace["rows"]}
            check(not verify_unsat_trace(cnf, fake), "SAT accepted as UNSAT")

horn_controls = []
for k in range(1, 13):
    cnf = horn_chain(k)
    trace = decide_with_trace(cnf)
    payload = chain_resolution_payload(k)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    wrapped = json.dumps({"kind": "WRAP", "payload": payload}, sort_keys=True, separators=(",", ":"))
    check(trace["label"] == "UNSAT" and verify_unsat_trace(cnf, trace), "Horn trace")
    check(verify_chain_payload(payload), "Resolution payload")
    check(json.loads(wrapped)["payload"] == payload, "unwrap")
    check(len(wrapped) >= len(encoded), "wrapper length")
    horn_controls.append({"k": k, "resolution_nodes": k, "wrap_nodes": 1,
                          "payload_bytes": len(encoded), "wrapped_bytes": len(wrapped)})

base = truth_cnf(3, 0)
valid = decide_with_trace(base)
corruptions = []
corruptions.append({"label": "SAT", "rows": valid["rows"]})
corruptions.append({"label": "UNSAT", "rows": valid["rows"][:-1]})
r = json.loads(json.dumps(valid)); r["rows"][1]["number"] = 2; corruptions.append(r)
r = json.loads(json.dumps(valid)); r["rows"][2]["assignment"][0] = not r["rows"][2]["assignment"][0]; corruptions.append(r)
r = json.loads(json.dumps(valid)); r["rows"][3]["failed_clause"] = 999; corruptions.append(r)
r = json.loads(json.dumps(valid)); r["rows"][4]["failed_clause"] = (r["rows"][4]["failed_clause"] + 1) % len(base["clauses"]); corruptions.append(r)
for i, bad in enumerate(corruptions):
    check(not verify_unsat_trace(base, bad), f"corruption {i} accepted")

malformed = [None, {}, {"n": -1, "clauses": []}, {"n": 2, "clauses": [[0]]},
             {"n": 2, "clauses": [[3]]}, {"n": 2, "clauses": "bad"},
             {"n": 2, "clauses": [[1, "x"]]}]
for i, bad in enumerate(malformed):
    check(not well_formed(bad), f"malformed {i} accepted")

summary = {
    "artifact": "NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334",
    "truth_function_fixtures": truth_fixtures,
    "sat_fixtures": sat_fixtures,
    "unsat_fixtures": unsat_fixtures,
    "horn_wrap_controls": horn_controls,
    "corrupt_traces_rejected": len(corruptions),
    "malformed_rejected": len(malformed),
    "checks": checks,
    "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "theorem": {
        "counterexample": "Wrap(Res) and Res are mutually linear-time translatable in proof bytes, but Haken PHP has Wrap node cost 1 and Resolution node cost 2^Omega(h)",
        "repair": "polynomial node-to-bit normalization plus a polynomial explicit-proof compiler yields polynomial node-cost reflection",
        "optimality_frontier": "length-optimal systems suffice for existential B1; p-optimal systems additionally give a fully charged compiler"
    },
    "classification": {
        "proved": ["Wrap counterexample", "normalization-transfer lemma", "trace-system sufficiency"],
        "restricted": ["ordinary Resolution Haken anchor", "fixed-grammar Rmix341 normalization subject to private LOCAL-CONVERT wires"],
        "open": ["B1_Rmix341", "B2_Rmix341", "B3_Rmix341", "p_optimality_Rmix341", "P!=NP"]
    }
}
print(json.dumps(summary, sort_keys=True))
