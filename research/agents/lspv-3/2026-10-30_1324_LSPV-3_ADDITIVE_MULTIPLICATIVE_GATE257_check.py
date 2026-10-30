#!/usr/bin/env python3
"""Run against raw.json from the complete LSPV-3 run257 archive.
Independent exhaustive labels, witnesses, local S/U masks, and FLMV fractions.
Does not import the producer or invoke any of its SAT solvers.
"""
import json,sys,itertools
from fractions import Fraction as Q

def models(F):
    vs=sorted({abs(l) for c in F for l in c})
    for bits in itertools.product((0,1),repeat=len(vs)):
        a=dict(zip(vs,bits))
        if all(any(a[abs(l)]==(l>0) for l in c) for c in F):
            yield a

def main(path):
    j=json.load(open(path))
    sat=unsat=checks=0
    for r in j["cases"]:
        F=r["clauses"]
        M=list(models(F))
        assert len(M)==r["models"],r["case"]
        sat+=bool(M);unsat+=not bool(M)
        for name in ("baseline_witness","adaptive_witness"):
            w=r[name]
            if M:
                assert w is not None
                a={int(v):int(b) for v,b in w.items()}
                assert all(any(a.get(abs(l),0)==(l>0) for l in c) for c in F)
            else:
                assert w is None
        checks+=len(M)+2
    assert (sat,unsat)==(52,6)
    g={x["case"]:x for x in j["cases"]}
    assert g["W1_STRICT22_UNSAT"]["models"]==0
    assert g["SWAP6_STRICT22_SAT"]["models"]==54
    for h in (0,1):
        for x in (0,1):
            r=g[f"GUARD_H{h}_X{x}"]
            assert bool(r["models"])==bool(h or x)
            assert r["decision"]["entry"]=="one-backdoor"
            assert r["decision"]["var"]==1
            assert [v[2] for v in r["decision"]["leaves"]]==[bool(h),bool(x)]
    for name,D in j["diagnostics"].items():
        F=g[name]["clauses"]
        assert len(F)==len(D["local_targets"])
        for t in D["local_targets"]:
            c=F[t["j"]-1]
            S={int(k):v for k,v in t["S"].items()}
            U={int(k):v for k,v in t["U"].items()}
            assert sum(S[abs(l)]==(l>0) for l in c)==len(c)
            assert sum(U[abs(l)]==(l>0) for l in c)==0
            checks+=2
        for p in D["extreme_compatibility"]:
            a=F[p["j"]-1];b=F[p["k"]-1]
            for x,y in itertools.product("SU",repeat=2):
                A={abs(l):int(l>0) if x=="S" else int(l<0) for l in a}
                B={abs(l):int(l>0) if y=="S" else int(l<0) for l in b}
                assert p["compat"][x+y]==all(A[v]==B[v] for v in A.keys()&B.keys())
                checks+=1
    c=Q(241,200);f=Q(1);best=Q(0);index=0
    for k in range(1,4):
        f=c*f/(1+f)
        d=min((1/f-c)/k,c**(-k))
        if d>best:best,index=d,k
    assert best==Q(11642479,23232400)
    assert index==2 and c**(-4)<best
    for r in j["flmv"]["trials"]:
        ds=Q(r["delta_scan"]);de=Q(r["delta_guest"])
        kstar=max(Q(11,10)+ds,Q(6,5)+2*de)
        assert kstar==Q(r["fixed_K"])
        assert (kstar<c)==r["enters_forbidden_test"]
    print(json.dumps({"status":"PASS","cases":sat+unsat,"SAT":sat,
                      "UNSAT":unsat,"checks":checks,
                      "FLMV_d":str(best),"maximizer_k":index},sort_keys=True))

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "raw.json")
