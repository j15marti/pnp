#!/usr/bin/env python3
"""Independent checker for ARC-BATCHED-POLARITY-SELECT260.
Usage: python compact_check.py FULL_RAW_JSON
The 2.4 MB expanded raw JSON is in the per-run reproducibility bundle.
"""
import bisect, itertools, json, math, sys

def t(cl, a):
    return sum(a[abs(l)-1] == (1 if l > 0 else 0) for l in cl)

def sat(F, n):
    return sum(all(t(c, a) for c in F) for a in itertools.product((0,1), repeat=n))

def check(row, idx):
    F, n = row["clauses"], row["n"]
    q, B, r = row["q"], row["batch"], row["profile"]
    assert sat(F, n) == row["number_of_sat_models"]
    assert bool(row["number_of_sat_models"]) == row["baseline"]["sat"] == row["augmented"]["sat"]
    assert r["source_scans"] == (q+B-1)//B
    assert r["candidate_generations"] == q
    assert r["record_probes"] == sum(map(len, F))*r["source_scans"]
    for side in ("baseline","augmented"):
        w = row[side]["witness"]
        if w is not None:
            assert len(w) == n and all(t(c,w)>0 for c in F)
        else: assert sat(F,n) == 0
    seed = 202610301900 + idx
    aa = 1+((seed*7+3)%(n-1)) if n>1 else 0
    if n>1:
        while math.gcd(aa,n)!=1: aa=(aa%n)+1
    bb=(seed*5+1)%n
    candidates=[(aa*j+bb)%n+1 for j in range(q)]
    positive = {v:sum(l==v for cl in F for l in cl) for v in candidates}
    negative = {v:sum(l==-v for cl in F for l in cl) for v in candidates}
    selected=[v for v in candidates if positive[v]>=2 and negative[v]>=2]
    assert r["selected_variable"]==(max(selected) if selected else candidates[0])
    assert r["qualified_count"]==len(selected)
    ref=sorted([[v,positive[v],negative[v]] for v in selected])
    assert ref == row["reference_qualified_profiles"]
    for clause, target in zip(F,row["original_clause_S_U_targets"]):
        assert target["literals"]==clause
        for lit,occ in zip(clause,target["occurrences"]):
            assert lit==occ["signed_literal"]
            assert occ["S"]==int(lit>0)==occ["inverse_U"]
            assert occ["U"]==int(lit<0)==occ["inverse_S"]
    models=list(itertools.product((0,1),repeat=n))
    for record in row["pair_compatibility"]:
        i,j=[k-1 for k in record["source_clause_indices"]]
        observed=[]
        for m1,m2 in itertools.product(("S","U"),repeat=2):
            v1=len(F[i]) if m1=="S" else 0
            v2=len(F[j]) if m2=="S" else 0
            observed.append(int(any(t(F[i],a)==v1 and t(F[j],a)==v2 for a in models)))
        assert observed==record["SS_SU_US_UU"]
    for trail in row["coherent_endpoint_flip_trails"]:
        a=trail["assignment"]
        comp=trail["complement"]
        assert comp==[1-v for v in a]
        vals=[t(cl,a) for cl in F]
        assert vals==trail["clause_t"]
        assert [vals.count(k) for k in range(4)]==trail["N0_N1_N2_N3"]
        assert all(t(c,a)+t(c,comp)==len(c) for c in F)
    proof=row["non_tautological_resolvent"]
    if proof:
        i,j=[k-1 for k in proof["parents"]]
        p=proof["pivot"]
        pivot=p if p in F[i] else -p
        assert pivot in F[i] and -pivot in F[j]
        R=(set(F[i])-{pivot})|(set(F[j])-{-pivot})
        assert set(proof["resolvent"])==R and not any(-z in R for z in R)
        rho={int(k):int(v) for k,v in proof["prohibited_cube"].items()}
        assert rho=={abs(z):int(z<0) for z in R}
        for a in models:
            if all(t(c,a)>0 for c in F):
                assert not all(a[k-1]==v for k,v in rho.items())
    assert row["baseline_selected_events"]==row["baseline"]["literal_tests"]
    assert row["augmented_selected_events"]==(
        row["augmented"]["literal_tests"]+r["record_probes"]
        +r["search_comparison_upper"]+r["candidate_generations"])

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python compact_check.py FULL_RAW_JSON")
    raw=json.load(open(sys.argv[1]))
    assert raw["seed"]==202610301900
    for idx, row in enumerate(raw["cases"]): check(row,idx)
    print(json.dumps({"independent_source_checks":len(raw["cases"]),
                       "sat_unsat":raw["summary"],
                       "pair_extreme_modes":raw["totals"]["pair_mode_checks"],
                       "status":"PASS"},sort_keys=True))

if __name__=="__main__": main()
