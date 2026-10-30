#!/usr/bin/env python3
"""ARC-DELAY-QUERY-FIREWALL223 reproducer.

Independent finite controls for (i) the affine small-bias fiber lemma,
(ii) the mandatory large guest-query DELAY/COPY firewall, and (iii) matched
ordinary 3CNF SAT/UNSAT source semantics with clause-indexed S/U diagnostics.
Finite counters are not FLMV-native machine bounds.
"""
from fractions import Fraction
from itertools import product
from collections import Counter
import hashlib, json, os, time, tracemalloc

RUN = "ARC-DELAY-QUERY-FIREWALL223"
RAW = "results/raw/arc/2026-10-30_1148_ARC_DELAY_QUERY_FIREWALL223_raw.json"
SUMMARY = "results/raw/arc/2026-10-30_1148_ARC_DELAY_QUERY_FIREWALL223_summary.json"

def lit_true(lit, a):
    return bool(a[abs(lit)-1]) == (lit > 0)

def truth_counts(cnf, a):
    vals = [sum(lit_true(l, a) for l in c) for c in cnf]
    return vals, [vals.count(i) for i in range(4)]

def models(cnf):
    n = max(abs(l) for c in cnf for l in c)
    out = []
    for a in product((0,1), repeat=n):
        if all(any(lit_true(l,a) for l in c) for c in cnf): out.append(a)
    return out

def occurrence_audit(cnf):
    rows=[]
    for j,c in enumerate(cnf):
        occ=[]
        for l in c:
            sat = 1 if l>0 else 0
            unsat = 1-sat
            occ.append({"variable":abs(l),"sign":"+" if l>0 else "-",
                        "S_value":sat,"invert_S_to_U":1-sat,
                        "U_value":unsat,"invert_U_to_S":1-unsat})
        rows.append({"clause_index":j,"clause":list(c),"occurrences":occ})
    pairs=[]
    for j in range(len(cnf)):
        for k in range(j+1,len(cnf)):
            sj={abs(l):l>0 for l in cnf[j]}; sk={abs(l):l>0 for l in cnf[k]}
            shared=set(sj)&set(sk)
            same=any(sj[v]==sk[v] for v in shared)
            opp=any(sj[v]!=sk[v] for v in shared)
            matrix={"SS":not opp,"UU":not opp,"SU":not same,"US":not same}
            # exact enumeration of the shared demands
            def feasible(mode):
                req={}
                for which,cl in zip(mode,(cnf[j],cnf[k])):
                    for l in cl:
                        v=abs(l); val=(1 if l>0 else 0)
                        if which=="U": val=1-val
                        if v in req and req[v]!=val: return False
                        req[v]=val
                return True
            exact={m:feasible(m) for m in ("SS","SU","US","UU")}
            assert matrix==exact
            pairs.append({"source_clause_indices":[j,k],"shared":sorted(shared),
                          "same_polarity":same,"opposite_polarity":opp,
                          "matrix":matrix})
    return rows,pairs

def source_record(name,cnf):
    n=max(abs(l) for c in cnf for l in c)
    ms=models(cnf)
    occ,pairs=occurrence_audit(cnf)
    trail=[]
    cur=[0]*n
    order=list(range(n))+list(range(n-1,-1,-1))
    for step,i in enumerate(order):
        cur[i]^=1
        vals,buckets=truth_counts(cnf,cur)
        trail.append({"step":step+1,"flipped_variable":i+1,
                      "assignment":cur[:],"true_literal_counts":vals,"N":buckets})
    endpoints={}
    for tag,a in (("zero",(0,)*n),("one",(1,)*n)):
        vals,buckets=truth_counts(cnf,a)
        endpoints[tag]={"assignment":list(a),"true_literal_counts":vals,"N":buckets,
                        "formula_sat":all(v>0 for v in vals)}
    return {"name":name,"n":n,"m":len(cnf),"clauses":[list(c) for c in cnf],
            "model_count":len(ms),"witness":list(ms[0]) if ms else None,
            "occurrence_targets":occ,"pair_compatibility":pairs,
            "endpoints":endpoints,"flip_trail":trail}

# GF(16), modulus x^4+x+1.  CHMY-style output coordinate j is <a^j,b>.
def gf_mul(a,b):
    r=0
    for _ in range(4):
        if b&1:r^=a
        b>>=1
        carry=a&8
        a=(a<<1)&15
        if carry:a^=3
    return r

def gf_pow(a,j):
    r=1
    while j:
        if j&1:r=gf_mul(r,a)
        a=gf_mul(a,a); j//=2
    return r

def parity(x): return x.bit_count()&1

def primitive_distribution():
    cnt=Counter()
    for a in range(16):
        for b in range(16):
            y=0
            for j in range(1,5):
                y=(y<<1)|parity(gf_pow(a,j)&b)
            cnt[y]+=1
    return cnt

def mat_apply(rows,x):
    y=0
    for r in rows:y=(y<<1)|parity(r&x)
    return y

def affine_audit():
    cnt=primitive_distribution(); total=sum(cnt.values()); assert total==256
    biases={}
    for v in range(1,16):
        num=sum(c*(1 if parity(v&x)==0 else -1) for x,c in cnt.items())
        biases[v]=Fraction(abs(num),total)
    eps=max(biases.values()); assert eps<=Fraction(1,4)
    point_checks=set_checks=0; max_point_num=0; max_set_num=0
    for code in range(1<<12):
        rows=[(code>>(4*(2-i)))&15 for i in range(3)]
        pd=Counter(); pu=Counter()
        for x,c in cnt.items():pd[mat_apply(rows,x)]+=c
        for x in range(16):pu[mat_apply(rows,x)]+=1
        diffs=[]
        for y in range(8):
            d=abs(pd[y]-16*pu[y]); diffs.append(pd[y]-16*pu[y])
            assert d<=eps*256; max_point_num=max(max_point_num,d); point_checks+=1
        for mask in range(256):
            B=mask.bit_count()
            d=abs(sum(diffs[y] for y in range(8) if mask>>y&1))
            assert d<=B*eps*256; max_set_num=max(max_set_num,d); set_checks+=1
    max_point=Fraction(max_point_num,256); max_set=Fraction(max_set_num,256)
    return {"distribution_support":len(cnt),"epsilon":[eps.numerator,eps.denominator],
            "character_checks":15,"matrices":4096,"point_checks":point_checks,
            "set_checks":set_checks,"max_point_gap":[max_point.numerator,max_point.denominator],
            "max_set_gap":[max_set.numerator,max_set.denominator],
            "counting_correction":"log2 B = O((u+1) log(m+u+2)); +1 is required when u=0"}

def wrapper_audit():
    alpha=Fraction(11,10); gamma=Fraction(3,5); lam=Fraction(1,2); sigma=Fraction(1,2)
    rows=[]
    for eta in (Fraction(1,1),Fraction(3,4),Fraction(1,2)):
        first_time=first_space=None
        for D in range(1,41):
            actual=eta*D
            time_bound=max(alpha,gamma+lam*D)
            space_bound=max(sigma,lam*D)
            tfail=actual>time_bound; sfail=actual>space_bound
            if tfail and first_time is None:first_time=D
            if sfail and first_space is None:first_space=D
            rows.append({"eta":[eta.numerator,eta.denominator],"delay_or_copy_exponent":D,
                         "actual_guest_exponent":[actual.numerator,actual.denominator],
                         "claimed_time_envelope":[time_bound.numerator,time_bound.denominator],
                         "claimed_space_envelope":[space_bound.numerator,space_bound.denominator],
                         "time_violation":tfail,"space_violation":sfail})
        if eta>lam:
            assert first_time is not None and first_space is not None
        else:
            assert first_time is None and first_space is None
    return {"parameters":{"alpha":[11,10],"gamma":[3,5],"lambda":[1,2],"sigma":[1,2]},
            "rows":rows,
            "exact_statement":"for every eta>lambda, choose D>max(K0,alpha/eta,gamma/(eta-lambda)); a completed eta-scale DELAY/COPY guest call violates the advertised arbitrary-A recurrence"}

def main():
    start=time.perf_counter(); tracemalloc.start()
    sat=[(1,2,3),(-1,-2,-3)]
    unsat=[]
    for bits in product((0,1),repeat=3):
        # clause falsified exactly by bits
        unsat.append(tuple((-(i+1) if bits[i] else i+1) for i in range(3)))
    sources=[source_record("ENDPOINT_BOTH_FAIL_SAT",sat),source_record("HITTING8_UNSAT",unsat)]
    assert sources[0]["model_count"]==6 and sources[1]["model_count"]==0
    affine=affine_audit(); wrappers=wrapper_audit()
    cur,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    raw={"run":RUN,"status":{"delay_query_lemma":"PROVED/EXACT conditional necessary condition",
         "affine_smallbias":"PROVED/EXACT restricted independent finite referee",
         "experiments":"COMPUTATIONAL","arbitrary_A_Phi":"OPEN","P_vs_NP":"OPEN"},
         "sources":sources,"affine":affine,"wrappers":wrappers,
         "runtime_seconds":time.perf_counter()-start,"tracemalloc_peak_bytes":peak}
    os.makedirs(os.path.dirname(RAW),exist_ok=True)
    with open(RAW,"w") as f:json.dump(raw,f,indent=2,sort_keys=True)
    summary={"run":RUN,"source_models":{s["name"]:s["model_count"] for s in sources},
             "occurrence_targets":sum(sum(len(c["occurrences"]) for c in s["occurrence_targets"]) for s in sources),
             "pair_modes":4*sum(len(s["pair_compatibility"]) for s in sources),
             "affine_checks":affine["character_checks"]+affine["point_checks"]+affine["set_checks"],
             "wrapper_rows":len(wrappers["rows"]),"runtime_seconds":raw["runtime_seconds"],
             "tracemalloc_peak_bytes":peak}
    with open(SUMMARY,"w") as f:json.dump(summary,f,indent=2,sort_keys=True)
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=="__main__":main()
