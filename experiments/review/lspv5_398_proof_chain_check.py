#!/usr/bin/env python3
"""REFEREE398: dependency and status audit for proof1.txt/proof2.txt."""
from __future__ import annotations
import argparse, hashlib, json, re, resource, sys, time
from pathlib import Path

NODE = re.compile(r"^\[(P[12]-[A-Z0-9-]+)\]\s+([^|]+)\|", re.M)
CLOSED = ("KNOWN THEOREM", "PROVED/EXACT", "PROVED/RESTRICTED")
NONCLOSING = ("OPEN", "CONDITIONAL", "CANDIDATE", "COMPUTATIONAL", "FALSIFIED/RETIRED")
REQUIRED = {
    "proof1": ["P1-00","P1-01","P1-02","P1-03","P1-04","P1-05"],
    "proof2": ["P2-00","P2-D1","P2-D2","P2-B1","P2-B2","P2-B4","P2-B5",
               "P2-F1","P2-F2","P2-F3","P2-F4","P2-F8","P2-C1","P2-C3"],
}
SPINES = {
    "P_equals_NP": ["P1-00","P1-01","P1-02","P1-03","P1-04","P1-05"],
    "P_not_equals_NP_Route_A": ["P2-A1","P2-A2","P2-A3","P2-A5"],
    "P_not_equals_NP_Route_B": ["P2-D1","P2-D2","P2-B1","P2-B2","P2-B5","P2-C1","P2-C3"],
}

def category(status: str) -> str:
    s=status.strip()
    for k in CLOSED + NONCLOSING:
        if s.startswith(k):
            return k
    if s.startswith("KNOWN ACCOUNTING"):
        return "KNOWN THEOREM"
    return "UNKNOWN"

def audit_text(p1: str, p2: str) -> dict:
    errors=[]
    parsed={}
    for name,text in (("proof1",p1),("proof2",p2)):
        nodes=NODE.findall(text)
        ids=[x[0] for x in nodes]
        dup=sorted({x for x in ids if ids.count(x)>1})
        if dup: errors.append(f"{name}: duplicate IDs {dup}")
        parsed.update({i: {"raw_status":s.strip(),"category":category(s)} for i,s in nodes})
        miss=sorted(set(REQUIRED[name])-set(ids))
        if miss: errors.append(f"{name}: missing required IDs {miss}")
        if "status: OPEN" not in text and "STATUS: OPEN" not in text:
            errors.append(f"{name}: overall OPEN status absent")
    for i,v in parsed.items():
        if v["category"]=="UNKNOWN": errors.append(f"{i}: unknown status {v['raw_status']!r}")
    exact_checks={
        "random3_exact_distribution": "binom(n,3)*2^3 ordinary width-three clauses" in p2,
        "random3_repetition_scope": "Repeated clauses are permitted" in p2,
        "random3_resolution_bound": "(1+epsilon)^n" in p2,
        "haken_control": "[P2-F1]" in p2 and "Extended Resolution" in p2,
        "tseitin_gf2_control": "[P2-F2]" in p2 and "GF(2)" in p2,
        "resxor_scope": "[P2-F3]" in p2 and "Res(XOR) is NOT R_mix341" in p2,
        "same_R_B3": "[P2-B2]" in p2 and "SAME preselected R" in p2,
        "branch_scope": "[P2-C1]" in p2 and "Gamma |- C" in p2,
    }
    for k,v in exact_checks.items():
        if not v: errors.append(f"missing safeguard: {k}")
    spine={}
    for name,deps in SPINES.items():
        blockers=[d for d in deps if d not in parsed or parsed[d]["category"] not in CLOSED]
        spine[name]={"dependencies":deps,"blockers":blockers,"closed":not blockers}
        if not blockers:
            errors.append(f"unsafe terminal closure: {name}")
    if parsed.get("P1-05",{}).get("category")!="CONDITIONAL":
        errors.append("P1-05 must remain CONDITIONAL")
    if parsed.get("P2-B4",{}).get("category")!="CONDITIONAL":
        errors.append("P2-B4 must remain CONDITIONAL")
    return {"ok":not errors,"errors":errors,"nodes":parsed,"spines":spine,
            "safeguards":exact_checks,
            "sha256":{"proof1":hashlib.sha256(p1.encode()).hexdigest(),
                      "proof2":hashlib.sha256(p2.encode()).hexdigest()}}

def main():
    started=time.perf_counter()
    ap=argparse.ArgumentParser()
    ap.add_argument("proof1", type=Path)
    ap.add_argument("proof2", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--hostile-controls", action="store_true")
    a=ap.parse_args()
    p1=a.proof1.read_text(); p2=a.proof2.read_text()
    result=audit_text(p1,p2)
    if a.hostile_controls:
        muts=[
          ("remove_F8",p1,p2.replace("[P2-F8]","[P2-Z8]",1)),
          ("claim_PeqNP",p1.replace("Overall status: OPEN","Overall status: PROVED",1),p2),
          ("duplicate_ID",p1+"\n[P1-01] OPEN | duplicate\n",p2),
          ("promote_B4",p1,p2.replace("[P2-B4] CONDITIONAL","[P2-B4] PROVED/EXACT",1)),
          ("erase_random_distribution",p1,p2.replace("binom(n,3)*2^3 ordinary width-three clauses","unspecified clauses",1)),
        ]
        controls=[]
        for name,x,y in muts:
            r=audit_text(x,y); controls.append({"name":name,"rejected":not r["ok"],"errors":r["errors"]})
        result["hostile_controls"]=controls
        if not all(x["rejected"] for x in controls):
            result["ok"]=False; result["errors"].append("hostile control escaped")
    result["resources"]={
        "wall_seconds":time.perf_counter()-started,
        "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "input_bytes":len(p1.encode())+len(p2.encode()),
        "logical_nodes_checked":len(result["nodes"]),
        "hostile_controls":len(result.get("hostile_controls",[])),
    }
    out=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.out: a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(out)
    print(out,end="")
    return 0 if result["ok"] else 1
if __name__=="__main__": raise SystemExit(main())

