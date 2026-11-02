#!/usr/bin/env python3
"""REFEREE284: paid source-live residual recompilation.

Exact claims are restricted to a clause-private fan-in-two OR/AND evaluator.
The finite audit is exhaustive on all 3^9 F9 pin cubes and all continuations.
"""
from __future__ import annotations

import argparse
import collections
import functools
import itertools
import json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
     (7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),
     (7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def canonical(F,n):
    if not F or n%3 or 3*len(F)!=4*n:return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(not isinstance(x,int) or x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def lit_value(x,a):
    return None if abs(x) not in a else a[abs(x)]==int(x>0)

def restrict_source(F,p):
    out=[]
    for c in F:
        vals=[lit_value(x,p) for x in c]
        if True in vals:continue
        r=tuple(x for x,v in zip(c,vals) if v is None)
        if not r:return "FALSE"
        out.append(r)
    return tuple(out) if out else "TRUE"

def unit_close(F,p):
    a=dict(p); probes=scans=0
    while True:
        changed=False
        for c in F:
            scans+=1; unknown=[]; satisfied=False
            for x in c:
                probes+=1; v=lit_value(x,a)
                if v is True:satisfied=True;break
                if v is None:unknown.append(x)
            if satisfied:continue
            if not unknown:return a,"FALSE",probes,scans
            if len(unknown)==1:
                x=unknown[0]; value=int(x>0)
                if abs(x) in a and a[abs(x)]!=value:return a,"FALSE",probes,scans
                if abs(x) not in a:
                    a[abs(x)]=value;changed=True;break
        if not changed:break
    return a,restrict_source(F,a),probes,scans

def compile_private(R,n):
    """Return gates/root for the declared clause-private architecture."""
    if R in ("TRUE","FALSE"):return (),R
    gates=[]
    def add(op,a,b):
        z=n+len(gates)+1;gates.append((z,op,a,b));return z
    outs=[]
    for c in R:
        q=c[0]
        for x in c[1:]:q=add("OR",q,x)
        outs.append(q)
    while len(outs)>1:
        outs=[add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i]
              for i in range(0,len(outs),2)]
    return tuple(gates),outs[0]

def eval_residual(R,a):
    if R=="TRUE":return True
    if R=="FALSE":return False
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in R)

def eval_circuit(gates,root,a):
    if root=="TRUE":return True
    if root=="FALSE":return False
    b=dict(a)
    for z,op,x,y in gates:
        xv=b[abs(x)]==int(x>0);yv=b[abs(y)]==int(y>0)
        b[z]=(xv or yv) if op=="OR" else (xv and yv)
    return b[abs(root)]==int(root>0)

def expected_gates(R):
    if R in ("TRUE","FALSE"):return 0
    return sum(map(len,R))-1

def private_source_circuit(F,n):
    gates,root=compile_private(F,n); clauses=[]
    for z,op,a,b in gates:
        if op=="OR":clauses.extend(((-a,z),(-b,z),(a,b,-z)))
        else:clauses.extend(((a,-z),(b,-z),(-a,-b,z)))
    clauses.append((root,))
    return gates,tuple(clauses),root

def up_cnf(F,p):
    a=dict(p)
    while True:
        changed=False
        for c in F:
            unknown=[];satisfied=False
            for x in c:
                v=lit_value(x,a)
                if v is True:satisfied=True;break
                if v is None:unknown.append(x)
            if satisfied:continue
            if not unknown:return True,(),a
            if len(unknown)==1:
                x=unknown[0];v=int(x>0)
                if abs(x) in a and a[abs(x)]!=v:return True,(),a
                if abs(x) not in a:a[abs(x)]=v;changed=True;break
        if not changed:break
    R=restrict_source(F,a)
    return False,R,a

def sat_source(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def model_count(F,p):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in p];q=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,bits));q+=sat_source(F,a)
    return q

def all_pin_audit(F,n,with_tseitin=False):
    states=rows=formula_checks=reduced=term_true=term_false=0
    hist=collections.Counter();spurious=collections.Counter();gate_sum=0
    T=None
    if with_tseitin:
        base,T,root=private_source_circuit(F,n)
        assert len(base)==3*len(F)-1 and root
    for vals in itertools.product((None,0,1),repeat=n):
        p={i+1:v for i,v in enumerate(vals) if v is not None};states+=1
        R=restrict_source(F,p);g,root=compile_private(R,n);want=expected_gates(R)
        assert len(g)==want;formula_checks+=1;gate_sum+=len(g)
        hist[str(want)]+=1
        if R=="TRUE":term_true+=1
        elif R=="FALSE":term_false+=1
        elif len(g)<3*len(F)-1:reduced+=1
        free=[v for v in range(1,n+1) if v not in p]
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(p);a.update(zip(free,bits));
            assert sat_source(F,a)==eval_residual(R,a)==eval_circuit(g,root,a)
            rows+=1
        if with_tseitin:
            contradiction,src,_,_=unit_close(F,p)
            if src=="FALSE" or (src not in ("TRUE","FALSE") and any(len(c)>2 for c in src)):continue
            tc,enc,_=up_cnf(T,p)
            if not tc and enc not in ("TRUE","FALSE") and any(len(c)==3 for c in enc):
                spurious["SAT" if model_count(F,p) else "UNSAT"]+=1
    return {"pin_states":states,"continuation_rows":rows,"gate_formula_checks":formula_checks,
            "strict_reductions":reduced,"terminal_true":term_true,"terminal_false":term_false,
            "gate_sum":gate_sum,"gate_histogram":dict(sorted(hist.items(),key=lambda x:int(x[0]))),
            "source_width_le2_but_tseitin_ternary":dict(spurious)}

def obdd_extrema(F,n):
    table=tuple(int(sat_source(F,{i+1:(z>>i)&1 for i in range(n)})) for z in range(1<<n))
    cost={}
    for S in range(1<<n):
        prefix=[i for i in range(n) if S>>i&1]
        for v in range(n):
            if S>>v&1:continue
            rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
            for pa in range(1<<len(prefix)):
                base=sum(((pa>>k)&1)<<i for k,i in enumerate(prefix));lo=hi=0
                for rb in range(1<<len(rest)):
                    z=base+sum(((rb>>k)&1)<<i for k,i in enumerate(rest))
                    lo|=table[z]<<rb;hi|=table[z|(1<<v)]<<rb
                if lo!=hi:pairs.add((lo,hi))
            cost[S,v]=len(pairs)
    full=(1<<n)-1
    @functools.lru_cache(None)
    def dp(S,worst=False):
        if S==full:return 0
        q=[cost[S,v]+dp(S|1<<v,worst) for v in range(n) if not(S>>v&1)]
        return max(q) if worst else min(q)
    S=natural=0
    for v in range(n):natural+=cost[S,v];S|=1<<v
    return {"best":dp(0),"natural":natural,"worst":dp(0,True)}

def malformed_controls():
    bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    return sum(not canonical(F,max([abs(x) for c in F for x in c],default=3)) for F in bad)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert canonical(F9,9) and canonical(Y6,6) and canonical(F15,15)
    f9=all_pin_audit(F9,9,True);y6=all_pin_audit(Y6,6,False)
    assert f9["pin_states"]==3**9 and f9["continuation_rows"]==4**9
    assert f9["source_width_le2_but_tseitin_ternary"]=={"SAT":951,"UNSAT":1}
    assert y6["pin_states"]==3**6 and y6["continuation_rows"]==4**6
    siblings=[]
    for p in ({1:0,4:0,5:1,8:0},{1:1,4:0,5:1,8:0}):
        close,R,probes,scans=unit_close(F9,p);g,root=compile_private(R,9)
        siblings.append({"pins":p,"models":model_count(F9,p),"up_residual":R,
                         "residual_literals":0 if R in ("TRUE","FALSE") else sum(map(len,R)),
                         "recompiled_gates":len(g),"formula":expected_gates(R),
                         "source_up_probes":probes,"source_up_scans":scans})
    assert [(x["models"],x["recompiled_gates"]) for x in siblings]==[(7,9),(0,13)]
    f15pins=[dict(zip(range(7,16),q)) for q in ((1,0,0,0,1,1,1,1,0),(0,0,0,0,1,1,1,1,0))]
    f15controls=[]
    for p in f15pins:
        R=restrict_source(F15,p);g,_=compile_private(R,15)
        f15controls.append({"models":model_count(F15,p),"residual":R,"gates":len(g),"formula":expected_gates(R)})
    assert [x["models"] for x in f15controls]==[2,0]
    obdd=obdd_extrema(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    assert malformed_controls()==6
    out={
      "run":"SOURCE-LIVE-RECOMPILE-REFEREE284","status":"PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL",
      "P_vs_NP":"OPEN","seed":284,
      "exact_theorem":"For every CNF F and coherent original-variable pin p, paid source restriction yields TRUE/FALSE or residual R. In the declared clause-private fan-in-two OR/AND architecture with free signed literals, the exact gate count is L(R)-1 for every nonterminal R.",
      "scope":"Exact architecture theorem and polynomial compiler upper bound; not an unrestricted circuit minimum, SAT solver, or arbitrary-machine lower bound.",
      "falsifiers":[
        "Residual ternary clauses in a precompiled full-biconditional Tseitin CNF are necessary continuation work.",
        "Every exact continuation representation must retain the precompiled auxiliary cones.",
        "The L(R)-1 rebuild is free or decides general residual SAT.",
        "A finite or architecture-specific residual saving yields strict same-machine FLMV transport."],
      "F9":f9,"Y6":y6,"same_original_F9":siblings,"same_original_F15":f15controls,
      "F9_forward":{"models":model_count(F9,{}),"private_gates":35,"depth":6,"obdd":obdd},
      "controls":{"Y6_models":model_count(Y6,{}),"F15_models":model_count(F15,{}),"malformed_rejected":6,
                  "wrappers":{"DELAY":"read-only work can add time without changing residual bits",
                              "COPY":"materialized copies are charged",
                              "RECOMP":"trades retained circuit space for paid source rereads",
                              "DEAD":"satisfied source clauses and private cones can be discarded after paid liveness discovery"}},
      "charged_work":"T_rebuild=Theta(N_source_reads+L(R)_writes) on random access/RAM accounting; sequential/index-head realizations charge their actual scans and moves. A full adaptive recurrence additionally sums grammar, all failed policy discovery/switching, proof/GE/SCC, semantic cache equality/replay, child/output/bit access, guests and every executed successor.",
      "peak_space":"Materialized rebuild O(L(R) log N) bits plus source/index/head/proof/cache/ancestor/guest state; streaming/recomputation can lower retained gates only by paid rereads. No free semantic representative.",
      "gap":"Recompilation removes a representation artifact but supplies no well-founded all-input polynomial aggregate-work potential and no arbitrary-A power-short A->Phi(A) or strict same-machine FLMV numerical transfer.",
      "literature_queries":[
        "primary paper partial evaluation Boolean circuits constant propagation cone of influence reduction SAT Tseitin encoding",
        "primary paper CNF preprocessing variable elimination blocked clause elimination SAT source aware circuit simplification",
        "primary paper knowledge compilation conditioning Boolean circuits OBDD residual functions",
        "primary paper Tseitin transformation unit propagation circuit encoding propagation completeness"],
      "github_queries":["j15marti/pnp dead auxiliary source aware recompilation Tseitin residual",
                        "j15marti/pnp L(R)-1 residual gates source aware",
                        "github.com/openai Tseitin constant propagation circuit simplify",
                        "github.com/openai cone of influence SAT circuit"]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")

if __name__=="__main__":main()
