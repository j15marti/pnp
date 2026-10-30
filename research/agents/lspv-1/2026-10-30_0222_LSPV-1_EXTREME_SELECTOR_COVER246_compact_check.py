#!/usr/bin/env python3
"""Standalone original-source extreme and proof-DAG checker. Python stdlib."""
import itertools
import json
import sys

def norm(c):
    a=set(c)
    assert not any(-x in a for x in a), "tautological resolvent"
    return tuple(sorted(a,key=lambda x:abs(x)))

def replay(formula,certificate):
    db={j:norm(c) for j,c in enumerate(formula)}
    for step in certificate["steps"]:
        u,v=step["parents"]
        p=step["pivot"]
        A,B=db[u],db[v]
        if p in A and -p in B: pos,neg=A,B
        elif p in B and -p in A: pos,neg=B,A
        else: raise AssertionError("bad pivot/source indices")
        derived=norm([x for x in pos if x!=p]+[x for x in neg if x!=-p])
        assert derived==norm(step["clause"])
        assert step["id"] not in db
        db[step["id"]]=derived
    if certificate["root_empty"] is not None:
        assert db[certificate["root_empty"]]==()
    return len(certificate["steps"])

def check_pair(F,record):
    j,k=record["pair"]
    vars_=sorted(set(abs(l) for l in F[j]+F[k]))
    for mode in ("SS","SU","US","UU"):
        possible=False
        for values in itertools.product((0,1),repeat=len(vars_)):
            env=dict(zip(vars_,values))
            def hits(clause,state):
                return all(env[abs(l)]==(int(l>0) if state=="S" else int(l<0))
                    for l in clause)
            if hits(F[j],mode[0]) and hits(F[k],mode[1]):
                possible=True
                break
        assert possible==record[mode],(j,k,mode)

def truth(F,a):
    return all(any(((a>>(abs(l)-1))&1)==(l>0) for l in C) for C in F)

def main(path):
    data=json.load(open(path))
    counter={"original_clauses":0,"source_occurrences":0,"pair_modes":0,
             "resolution_steps":0,"exhaustive_small_models":0}
    cases=data["source_indexed_records"]
    for name,obj in cases.items():
        F=obj["source_formula"]
        n=max(abs(l) for C in F for l in C)
        assert len(F)==len(obj["source_targets"])
        counter["original_clauses"]+=len(F)
        for C,row in zip(F,obj["source_targets"]):
            assert C==row["original_clause"]
            for l,occ in zip(C,row["occurrences"]):
                u=int(l<0)
                assert occ["literal"]==l
                assert (occ["S_all_true_value"],occ["invert_S_to_U"],
                        occ["U_all_false_value"],occ["invert_U_to_S"])==(1-u,u,u,1-u)
                counter["source_occurrences"]+=1
        for p in obj["pair_extremes"]:
            check_pair(F,p)
            counter["pair_modes"]+=4
        cert=obj["source_authentication_controller"]
        if cert:
            counter["resolution_steps"]+=replay(F,cert)
        if n<=15:
            count=sum(truth(F,a) for a in range(1<<n))
            if name=="STRICT22_W1_UNSAT": assert count==0
            if name=="STRICT22_W1_PRIME_SAT": assert count==168
            if name=="STRICT22_SHARP_SAT": assert count==4
            counter["exhaustive_small_models"]+=1<<n
    assert all(not p["UU"] for p in cases["ADAPTIVE_SUPPORT_TILE4_UNSAT"]["pair_extremes"])
    print(json.dumps({"status":"PASS","independent_rechecks":counter},sort_keys=True))

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python checker.py FULL_SOURCE_INDEXED_RAW.json")
    main(sys.argv[1])
