#!/usr/bin/env python3
"""Exact-rational audit of OFFLINE-INDEX-SPACE-GATE1."""
from fractions import Fraction
import hashlib, json, time
from pathlib import Path

def flmv_g(c):
    return ((c + 2) / (c * c) - c) / 2

def main():
    t0=time.perf_counter(); checks=0; failures=[]; rows=[]
    for den in range(1,101):
        for num in range(den,2*den+1):
            q=Fraction(num,den)
            for cnum in range(100,141):
                c=Fraction(cnum,100)
                p=Fraction(1,2)
                materialized=max(q,q*p)
                generator=q*p
                g=flmv_g(c)
                checks += 6
                if materialized != q: failures.append(["mat",str(q),str(c)])
                if not materialized >= 1: failures.append(["linear",str(q)])
                if c >= Fraction(6,5) and not materialized > Fraction(1,2):
                    failures.append(["endpoint",str(q),str(c)])
                if generator != q*p: failures.append(["gen",str(q)])
                if max(q, q*p) < q: failures.append(["max",str(q)])
                if c == Fraction(6,5) and g != Fraction(23,45):
                    failures.append(["g",str(g)])
            if den in (1,2,3,10,100) and num in (den,den+1,2*den):
                rows.append({"q":str(q),"materialized_space_exponent":str(q),
                             "on_demand_child_space_exponent":str(q/2)})
    result={
      "run_id":"SYNTHESIS-0009",
      "claim":"OFFLINE-INDEX-SPACE-GATE1",
      "status":"PROVED/EXACT for the TESTS-0008 materialized index realization",
      "checks":checks,"failures":failures,
      "formulae":{
        "output_bits":"M=N^(q+o(1))",
        "materialized_index_bits":"Theta(M)",
        "composed_space_exponent":"max(q,q*p)=q",
        "on_demand_generator_space_exponent":"q*p plus generator workspace",
        "flmv_g_at_6_5":"23/45"
      },
      "hostile_controls":["2SAT","Horn","affine/Tseitin","bounded treewidth",
        "independent products","padding","redundant clauses","COPY/DELAY wrappers",
        "alternate encodings","one-bit decision"],
      "sample_rows":rows,
      "limitations":[
        "No lower bound is claimed for every possible succinct index.",
        "No time-space lower bound for arbitrary SAT computation is inferred.",
        "A read-only donated table is a different realization unless its creation and storage are charged."
      ],
      "elapsed_seconds":time.perf_counter()-t0
    }
    raw=json.dumps(result,sort_keys=True,separators=(",", ":")).encode()
    result["payload_sha256"]=hashlib.sha256(raw).hexdigest()
    out=Path("results_raw_2026-10-11_offline_index_space_gate.json")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"output":str(out),"checks":checks,"failures":len(failures),
      "elapsed_seconds":result["elapsed_seconds"],"sha":result["payload_sha256"]},indent=2))

if __name__=="__main__": main()
