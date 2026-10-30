#!/usr/bin/env python3
"""Independent checker for ARC-DELAY-QUERY-FIREWALL223."""
from fractions import Fraction
from itertools import product
import json, os

RAW="results/raw/arc/2026-10-30_1148_ARC_DELAY_QUERY_FIREWALL223_raw.json"
OUT="results/raw/arc/2026-10-30_1148_ARC_DELAY_QUERY_FIREWALL223_check.json"

def lit_true(l,a):return bool(a[abs(l)-1])==(l>0)
def main():
    with open(RAW) as f:r=json.load(f)
    checks=0
    for s in r["sources"]:
        cnf=[tuple(c) for c in s["clauses"]]; n=s["n"]; cnt=0
        for a in product((0,1),repeat=n):
            sat=all(any(lit_true(l,a) for l in c) for c in cnf)
            cnt+=sat; checks+=len(cnf)
            vals=[sum(lit_true(l,a) for l in c) for c in cnf]
            abar=tuple(1-x for x in a)
            valsbar=[sum(lit_true(l,abar) for l in c) for c in cnf]
            assert all(x+y==3 for x,y in zip(vals,valsbar)); checks+=len(cnf)
        assert cnt==s["model_count"]; checks+=1
        for row in s["occurrence_targets"]:
            for o in row["occurrences"]:
                assert o["S_value"]==o["invert_U_to_S"]
                assert o["U_value"]==o["invert_S_to_U"]
                assert o["S_value"]+o["U_value"]==1; checks+=3
        for p in s["pair_compatibility"]:
            m=p["matrix"]
            assert m["SS"]==m["UU"]==(not p["opposite_polarity"])
            assert m["SU"]==m["US"]==(not p["same_polarity"]); checks+=4
    eps=Fraction(*r["affine"]["epsilon"]); assert eps<=Fraction(1,4); checks+=1
    assert r["affine"]["point_checks"]==32768
    assert r["affine"]["set_checks"]==1048576; checks+=2
    lam=Fraction(*r["wrappers"]["parameters"]["lambda"])
    for row in r["wrappers"]["rows"]:
        eta=Fraction(*row["eta"]); D=row["delay_or_copy_exponent"]
        actual=Fraction(*row["actual_guest_exponent"])
        tb=Fraction(*row["claimed_time_envelope"]); sb=Fraction(*row["claimed_space_envelope"])
        assert actual==eta*D
        assert row["time_violation"]==(actual>tb)
        assert row["space_violation"]==(actual>sb)
        if eta==lam: assert not row["time_violation"] and not row["space_violation"]
        checks+=4
    out={"status":"PASS","independent_checks":checks,
         "verified":"both-label source semantics, complement identity, S/U inversions, pair modes, affine ledger dimensions, exact wrapper inequalities"}
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    with open(OUT,"w") as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()
