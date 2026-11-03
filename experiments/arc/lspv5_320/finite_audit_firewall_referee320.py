#!/usr/bin/env python3
"""Finite-prefix audit firewall controls for REFEREE320.

This is a finite reproducibility program, not a SAT lower bound.  It checks the
concrete controls supporting the symbolic theorem in the accompanying report.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/lspv5_320/finite_audit_firewall_referee320.json"


def encode_cnf(clauses: list[list[int]]) -> str:
    n = max((abs(x) for c in clauses for x in c), default=0)
    rows = [f"p cnf {n} {len(clauses)}"]
    rows += [" ".join(map(str, c)) + " 0" for c in clauses]
    return "\n".join(rows) + "\n"


def parse_cnf(s: str):
    lines = s.splitlines()
    if not lines or len(lines[0].split()) != 4:
        return None
    h = lines[0].split()
    if h[:2] != ["p", "cnf"]:
        return None
    try:
        n, m = int(h[2]), int(h[3])
    except ValueError:
        return None
    if n < 0 or m < 0 or len(lines) != m + 1:
        return None
    clauses = []
    for line in lines[1:]:
        try:
            vals = [int(x) for x in line.split()]
        except ValueError:
            return None
        if not vals or vals[-1] != 0 or 0 in vals[:-1]:
            return None
        c = vals[:-1]
        if any(abs(x) > n for x in c):
            return None
        clauses.append(c)
    return n, clauses


def correct_decider(s: str):
    parsed = parse_cnf(s)
    work = len(s.encode())
    if parsed is None:
        return "MALFORMED", work, None
    n, clauses = parsed
    # Descending order makes the all-positive-unit control terminate at once.
    for mask in range((1 << n) - 1, -1, -1):
        work += 1
        if all(any(((mask >> (abs(l)-1)) & 1) == (1 if l > 0 else 0) for l in c)
               for c in clauses):
            return "SAT", work, mask
    return "UNSAT", work, None


def charged_equal(a: str, b: str):
    aa, bb = a.encode(), b.encode()
    work = 1
    if len(aa) != len(bb):
        return False, work
    for x, y in zip(aa, bb):
        work += 1
        if x != y:
            return False, work
    return True, work


def forged_decider(s: str, exception: str):
    eq, work = charged_equal(s, exception)
    if eq:
        return "UNSAT", work, None
    label, delegated, witness = correct_decider(s)
    return label, work + delegated, witness


def complete_clauses_3():
    return [[v if bit else -v for v, bit in zip((1,2,3), bits)]
            for bits in itertools.product((0,1), repeat=3)]


def model_count(clauses, n):
    return sum(all(any(((mask >> (abs(l)-1)) & 1) == (1 if l > 0 else 0)
                       for l in c) for c in clauses) for mask in range(1 << n))


def tseitin_k4(charge):
    edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    incident = {v: [] for v in range(4)}
    for i,(u,v) in enumerate(edges,1):
        incident[u].append(i); incident[v].append(i)
    clauses=[]
    for v in range(4):
        es=incident[v]
        for bits in itertools.product((0,1), repeat=3):
            if (sum(bits)&1) != charge[v]:
                clauses.append([(-e if bit else e) for e,bit in zip(es,bits)])
    return clauses


def positive_unit_exception(bound):
    k=1
    while True:
        s=encode_cnf([[i] for i in range(1,k+1)])
        if len(s.encode()) > bound:
            return s,k
        k += 1


def main():
    started=time.perf_counter()
    atoms=complete_clauses_3()
    catalog=[]
    for bits in range(1,256):
        cs=[atoms[i] for i in range(8) if (bits>>i)&1]
        s=encode_cnf(cs)
        label,work,wit=correct_decider(s)
        catalog.append({"bits":bits,"bytes":len(s.encode()),"label":label,
                        "work":work,"witness":wit})
    assert sum(x["label"]=="UNSAT" for x in catalog)==1
    malformed=["", "p cnf", "p dnf 1 0\n", "p cnf x 0\n",
               "p cnf 1 -1\n", "p cnf 1 1\n1\n", "p cnf 1 1\n2 0\n",
               "p cnf 1 2\n1 0\n", "p cnf 1 1\na 0\n",
               "p cnf 1 1\n0 1\n", "p cnf 0 1\n1 0\n",
               "p cnf 1 0\nextra\n"]
    audits=[]
    for bound in [32,64,96,128,192,256]:
        exc,k=positive_unit_exception(bound)
        al,aw,am=correct_decider(exc)
        bl,bw,bm=forged_decider(exc,exc)
        assert al=="SAT" and bl=="UNSAT" and len(exc.encode())>bound
        short_checked=0
        for row in catalog:
            if row["bytes"]<=bound:
                # Reconstruct only the finite catalog entry.
                cs=[atoms[i] for i in range(8) if (row["bits"]>>i)&1]
                s=encode_cnf(cs)
                assert correct_decider(s)[0]==forged_decider(s,exc)[0]
                short_checked += 1
        malformed_checked=0
        for s in malformed:
            if len(s.encode())<=bound:
                assert correct_decider(s)[0]==forged_decider(s,exc)[0]=="MALFORMED"
                malformed_checked += 1
        audits.append({"bound":bound,"exception_bytes":len(exc.encode()),
                       "exception_variables":k,"correct_label":al,
                       "forged_label":bl,"correct_work":aw,"forged_work":bw,
                       "short_catalog_checked":short_checked,
                       "malformed_checked":malformed_checked,
                       "witness_all_ones":am==(1<<k)-1,
                       "symbolic_all_strings_le_bound_agree":True})

    unsat=encode_cnf(atoms)
    assert correct_decider(unsat)[0]=="UNSAT"
    for a in audits:
        exc,_=positive_unit_exception(a["bound"])
        assert forged_decider(unsat,exc)[0]=="UNSAT"

    odd=tseitin_k4([1,0,0,0]); even=tseitin_k4([0,0,0,0])
    odd_models=model_count(odd,6); even_models=model_count(even,6)
    assert (odd_models,even_models)==(0,8)

    payload={
      "run":"FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320",
      "task_id":"6ad42a2a9a088191ab9042245f3b4393",
      "timestamp_pst":"2026-11-03 12:48",
      "audits":audits,
      "catalog":{"formulas":255,"sat":254,"unsat":1,
                 "total_correct_work":sum(x["work"] for x in catalog)},
      "malformed_count":len(malformed),
      "both_label_control":{"sat_exception_family":True,"unsat_complete_cube":True},
      "tseitin_k4":{"odd_models":odd_models,"even_models":even_models},
      "all_phase":{"producer_wall_seconds":time.perf_counter()-started,
                   "producer_peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   "optimizer_discovery_charged_separately":True,
                   "logical_minimum_claimed":False},
      "status":{"finite_controls":"COMPUTATIONAL","symbolic_theorem":"PROVED_IN_REPORT",
                "B1":"OPEN","B2":"OPEN","B3":"OPEN","P_vs_NP":"OPEN"}
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    OUT.write_text(raw)
    print(json.dumps({"output":str(OUT),"sha256":hashlib.sha256(raw.encode()).hexdigest(),
                      "audits":len(audits),"catalog":len(catalog),
                      "odd_even":[odd_models,even_models]},sort_keys=True))

if __name__=="__main__": main()
