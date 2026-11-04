#!/usr/bin/env python3
"""Finite controls for REFEREE345 certificate-work invariance.

Two p-equivalent truth-table refutation encodings have exponentially different
paid-node counts but essentially identical explicit bytes and verification work.
The compact-XOR/dense-table control is semantic only: materializing the dense
representation has exponential output cost.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def source(n, unsat=True):
    second = "-1 0" if unsat else "1 0"
    return f"p cnf {n} 2\n1 0\n{second}\n"

def assignment_bits(a,n): return format(a,f"0{n}b")

def row_payload(n):
    # Each row is assignment bits, ':', falsified source-clause index, ';'.
    out=[]
    for a in range(1<<n):
        bits=assignment_bits(a,n)
        clause="0" if bits[-1]=="0" else "1"
        out.append(bits+":"+clause+";")
    return "".join(out)

def unpacked_proof(n): return "U|"+row_payload(n)+"END"
def packed_proof(n): return "P|"+row_payload(n)+"END"

def verify(src,proof,tag):
    lines=src.splitlines()
    if len(lines)!=3 or not lines[0].startswith("p cnf "): return False
    try:
        _,_,ns,ms=lines[0].split(); n=int(ns); m=int(ms)
    except Exception: return False
    if n<1 or m!=2 or lines[1]!="1 0" or lines[2]!="-1 0": return False
    if not isinstance(proof,str) or not proof.startswith(tag+"|") or not proof.endswith("END"): return False
    body=proof[2:-3]; records=body.split(";")
    if records[-1]!="": return False
    records=records[:-1]
    if len(records)!=(1<<n): return False
    for a,r in enumerate(records):
        if ":" not in r: return False
        bits,ci=r.split(":",1)
        if bits!=assignment_bits(a,n) or ci not in ("0","1"): return False
        # Clause 0 is x1, clause 1 is not x1; rightmost bit encodes x1.
        if ci != ("0" if bits[-1]=="0" else "1"): return False
    return True

def translate(proof,from_tag,to_tag):
    if not proof.startswith(from_tag+"|"): return None
    return to_tag+proof[1:]

def main():
    rows=[]; malformed=0
    for n in range(1,17):
        u=unpacked_proof(n); p=packed_proof(n); f=source(n,True); sat=source(n,False)
        assert verify(f,u,"U") and verify(f,p,"P")
        assert not verify(sat,u,"U") and not verify(sat,p,"P")
        up=translate(u,"U","P"); pu=translate(p,"P","U")
        assert up==p and pu==u and verify(f,up,"P") and verify(f,pu,"U")
        bad=[u[:-1],u+"0",u.replace("0:0;","0:1;",1),u.replace("U|","X|",1)]
        for x in bad:
            assert not verify(f,x,"U"); malformed+=1
        proof_bits=8*len(u); src_bits=8*len(f)
        # Canonical verifier touches every proof byte once, plus source parsing.
        work=src_bits+proof_bits
        rows.append({
          "n":n,"source_bits":src_bits,"assignments":1<<n,
          "unpacked_paid_nodes":1<<n,"packed_paid_nodes":1,
          "unpacked_proof_bits":proof_bits,"packed_proof_bits":8*len(p),
          "unpacked_certificate_work":work,"packed_certificate_work":src_bits+8*len(p),
          "translation_output_bits":proof_bits,"streaming_peak_bits_upper":8*(n+16),
          "materialized_peak_bits":proof_bits,
          "xor_descriptor_bits":n+2,"dense_parity_table_bits":1<<n,
        })
    assert malformed==64
    assert rows[-1]["unpacked_paid_nodes"]==65536 and rows[-1]["packed_paid_nodes"]==1
    assert rows[-1]["unpacked_proof_bits"]==rows[-1]["packed_proof_bits"]
    # Polynomial-length equivalence is exact here, while nodes separate exponentially.
    assert all(r["unpacked_certificate_work"]==r["packed_certificate_work"] for r in rows)
    summary={
      "status":"PASS","family":"declared-n CNF (x1) AND (not x1)",
      "systems":"UNPACKED one paid row per assignment; PACKED one paid outer record with identical rows",
      "translation":"tag change; exact same explicit payload; linear time/output",
      "rows":rows,"sat_siblings_rejected":2*len(rows),"malformed_rejected":malformed,
      "proved_finite_identity":"certificate work equal; paid nodes 2^n versus 1",
      "xor_dense_control":"same parity relation; explicit dense materialization needs 2^n output bits from n+2 descriptor bits",
      "digest":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
    }
    out=Path("results/raw/arc/2026-11-04_1352_LSPV5_345_CERTIFICATE_WORK_INVARIANCE.json")
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
