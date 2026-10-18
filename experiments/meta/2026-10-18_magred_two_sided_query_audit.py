#!/usr/bin/env python3
"""MAGRED-QCOVER2. Exact integer entropy/counting audits, Python stdlib only.

Computes conservative upper bounds on the number of small circuits and lower
bounds on the number of t-sparse truth tables. It is not an MCSP solver and
does not establish an unrestricted machine-time lower bound.
"""
import json
from fractions import Fraction
from pathlib import Path

def bitlen(x):
    assert x > 0
    return x.bit_length()

def audit():
    rows=[]
    for n in [16,20,24,28,32,40,48,64]:
        N=1<<n
        for beta in [Fraction(1,2), Fraction(3,4)]:
            if (n*beta.numerator) % beta.denominator:
                continue
            s=1<<(n*beta.numerator // beta.denominator)
            C=(8*beta.denominator + (beta.denominator-beta.numerator)-1)//(beta.denominator-beta.numerator)
            t=C*s
            if t>=N//2:
                rows.append({"n":n,"beta":str(beta),"s":s,"t":t,"admissible":False})
                continue
            choices=3*(n+s)**2
            Ubits=s*bitlen(choices)+bitlen((s+1)*(n+s))
            Lbits=t*(bitlen(N//t)-1)
            margin=Lbits-Ubits
            rows.append({
                "n":n,"beta":str(beta),"s":s,"N":N,"t":t,"C":C,
                "admissible":True,
                "circuit_log_upper_bits":Ubits,
                "sparse_family_log_lower_bits":Lbits,
                "sparse_entropy_margin_bits":margin,
                "sparse_hard_high_probability_certified":margin>=4,
                "deterministic_query_min_lower_bound":max(0,N-Ubits),
                "randomized_probe_min_lower_bound_if_entropy_margin_ge_4":
                    max(0,(N+4*t-1)//(4*t)) if margin>=4 else None
            })
    return {"report":"MAGRED-QCOVER2",
            "type":"exhaustive integer evaluation of 16 chosen parameter pairs",
            "rows":rows,
            "admissible":sum(bool(r["admissible"]) for r in rows),
            "entropy_certified":sum(bool(r.get("sparse_hard_high_probability_certified")) for r in rows),
            "monotonic_check":all(r["t"]<r["N"]//2 for r in rows if r["admissible"])}

if __name__=="__main__":
    out=Path("results/raw/meta/2026-10-18_MAGRED_QCOVER2.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    result=audit()
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"admissible":result["admissible"],"entropy_certified":result["entropy_certified"]},indent=2))
