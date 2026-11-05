#!/usr/bin/env python3
"""Reproduce LSPV-4/412 semantic-support counterexample; no external libraries."""
import itertools, json, sys
F0={"nvars":2,"clauses":[[1,2],[1,-2]]}
F1={"nvars":2,"clauses":[[1,2],[1,-2],[-1]]}
GOOD={"support":[1,2],"truth":[0,1,0,1],"affine":{"mask":[1],"rhs":1}}

def assignments(n):
    for vs in itertools.product((0,1),repeat=n):
        yield {i+1:vs[i] for i in range(n)}
def eval_clause(c,a):
    return int(any(a[abs(v)]==int(v>0) for v in c))
def formula(F,a):
    return all(eval_clause(c,a) for c in F["clauses"])
def affine(row,a):
    return int(sum(a[v] for v in row["mask"])%2==row["rhs"])
def factor(spec,a):
    return spec["truth"][sum(a[v]<<j for j,v in enumerate(spec["support"]))]
def exact(spec):
    s=spec["support"];mask=spec["affine"]["mask"]
    if len(s)>3 or s!=sorted(set(s)) or mask!=sorted(set(mask)) or not set(mask).issubset(s):return False
    if len(spec["truth"])!=1<<len(s):return False
    return all(factor(spec,a)==affine(spec["affine"],a) for a in assignments(max(s) if s else 0))
def canon1(spec):
    return set(spec["support"])==set(spec["affine"]["mask"]) and exact(spec)

def run():
    checks=0
    sat=sum(formula(F0,a) for a in assignments(2));unsat=sum(formula(F1,a) for a in assignments(2))
    assert (sat,unsat)==(2,0);checks+=8
    for a in assignments(2):
        assert factor(GOOD,a)==eval_clause(F0["clauses"][0],a)*eval_clause(F0["clauses"][1],a)
        assert factor(GOOD,a)==affine(GOOD["affine"],a);checks+=2
    assert exact(GOOD) and not canon1(GOOD);checks+=2
    bad={"support":[1,2],"truth":[0,1,0,0],"affine":{"mask":[1],"rhs":1}}
    assert not exact(bad);checks+=1
    second={"support":[1],"truth":[1,0],"affine":{"mask":[1],"rhs":0}}
    assert exact(second) and canon1(second);checks+=2
    for a in assignments(2):
        assert factor(second,a)==1-a[1];checks+=1
    assert all(affine({"mask":[],"rhs":1},a)==0 for a in assignments(2));checks+=4
    dependent={"support":[1,2],"truth":[0,1,1,1],"affine":{"mask":[1],"rhs":1}}
    assert not exact(dependent);checks+=1
    matches=accepted=rejected=0
    for bits in itertools.product((0,1),repeat=4):
        for mask in ([],[1],[2],[1,2]):
            for rhs in (0,1):
                spec={"support":[1,2],"truth":list(bits),"affine":{"mask":mask,"rhs":rhs}}
                e=exact(spec);c=canon1(spec)
                assert not c or e;checks+=1
                if e:
                    matches+=1;accepted+=int(c);rejected+=int(not c)
    assert (matches,accepted,rejected)==(8,2,6)
    assert checks==158
    return {"status":"PASS","assertion_groups":checks,"source_SAT_models":sat,"source_UNSAT_models":unsat,
       "native_rule_replay_paid_nodes":3,"exact_affine_pairs":matches,
       "canon1_accepted":accepted,"canon1_false_rejected":rejected,
       "CANON1_defect":"An exact AND3 affine row can have a strict subset of syntactic support; original /341 allows it."}
if __name__=="__main__":
    result=run()
    print(json.dumps(result,sort_keys=True))
