#!/usr/bin/env python3
"""REFEREE286: paid SAT-witness <-> cofactor-boundary certificate audit.

The all-input theorem below is certificate equivalence, not a SAT decider.
Finite controls are exhaustive and use original-variable/source-clause semantics.
"""
from __future__ import annotations

import argparse, collections, functools, itertools, json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
G6=((1,2,3),(1,2,4),(3,5,6),(4,5,6),
    (-1,-2,-3),(-1,-2,-4),(-3,-5,-6),(-4,-5,-6))
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
        if any(type(x) is not int or x==0 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def assignment(n,z):return {v:(z>>(v-1))&1 for v in range(1,n+1)}

def clause_counts(F,a):
    return [sum(a[abs(x)]==int(x>0) for x in c) for c in F]

def source_pivots(F,n,a):
    """One source scan: variables uniquely satisfying at least one source clause."""
    marked=set(); unique=[]
    for ci,c in enumerate(F):
        true=[abs(x) for x in c if a[abs(x)]==int(x>0)]
        if len(true)==1: marked.add(true[0]);unique.append((ci+1,true[0]))
    return marked,unique

def flip_pivots(F,n,a):
    out=set()
    for v in range(1,n+1):
        b=dict(a);b[v]^=1
        if sat(F,a) and not sat(F,b):out.add(v)
    return out

def boundary_audit(F,n):
    sats=[];pairs=[];by_var=[0]*n;min_piv=n+1;moments=collections.Counter()
    for z in range(1<<n):
        a=assignment(n,z)
        if not sat(F,a):continue
        sats.append(z);marked,unique=source_pivots(F,n,a);direct=flip_pivots(F,n,a)
        assert marked==direct
        counts=clause_counts(F,a);moments[tuple(counts.count(k) for k in range(4))]+=1
        assert len(unique)==counts.count(1)
        assert counts.count(1)-counts.count(3)==len(F)//2
        assert len(marked)>=n//3
        min_piv=min(min_piv,len(marked))
        for v in marked:
            pairs.append((z,v));by_var[v-1]+=1
    miter=[]
    for v in range(1,n+1):
        rest=[x for x in range(1,n+1) if x!=v];q=0
        for bits in range(1<<(n-1)):
            a={x:(bits>>i)&1 for i,x in enumerate(rest)}
            a[v]=0;f0=sat(F,a);a[v]=1;f1=sat(F,a)
            if f0!=f1:
                q+=1
                # miter witness -> exactly one source-checked SAT endpoint
                assert f0+f1==1
        miter.append(q)
    assert by_var==miter and len(pairs)==sum(miter)
    if sats:assert len(pairs)>=n*len(sats)//3
    return {"models":len(sats),"boundary":len(pairs),"per_variable":by_var,
            "minimum_witness_pivots":None if not sats else min_piv,
            "moment_distributions":{str(k):v for k,v in sorted(moments.items())}}

def pin_table(F,n,p):
    free=[v for v in range(1,n+1) if v not in p];truth=[]
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));truth.append(int(sat(F,a)))
    boundary=0
    for i in range(len(free)):
        for z in range(1<<len(free)):
            if not(z>>i&1) and truth[z]!=truth[z|(1<<i)]:boundary+=1
    return {"free":len(free),"models":sum(truth),"boundary":boundary,
            "constant_true":bool(truth) and all(truth),"constant_false":not any(truth)}

def pin_census(F,n):
    out=collections.Counter();rows=0
    for vals in itertools.product((None,0,1),repeat=n):
        p={i+1:x for i,x in enumerate(vals) if x is not None};r=pin_table(F,n,p);rows+=1<<r["free"]
        if r["constant_false"]:kind="UNSAT_ZERO_BOUNDARY"
        elif r["constant_true"]:kind="SAT_ZERO_BOUNDARY_CONSTANT_TRUE"
        elif r["boundary"]:kind="SAT_POSITIVE_BOUNDARY"
        else:raise AssertionError(r)
        out[kind]+=1
    assert sum(out.values())==3**n and rows==4**n
    return {"states":3**n,"completion_rows":rows,"classes":dict(out)}

def compile_private(F,n):
    gates=[];outs=[];depth={v:0 for v in range(1,n+1)}
    def add(op,x,y):
        z=n+len(gates)+1;gates.append((z,op,x,y));depth[z]=1+max(depth[abs(x)],depth[abs(y)]);return z
    for c in F:outs.append(add("OR",add("OR",c[0],c[1]),c[2]))
    while len(outs)>1:outs=[add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
    return gates,outs[0],depth[outs[0]]

def eval_private(gates,root,a):
    b=dict(a)
    for z,op,x,y in gates:
        X=b[abs(x)] if x>0 else 1-b[abs(x)];Y=b[abs(y)] if y>0 else 1-b[abs(y)]
        b[z]=int((X or Y) if op=="OR" else (X and Y))
    return bool(b[root])

def obdd_extrema(F,n):
    table=tuple(int(sat(F,assignment(n,z))) for z in range(1<<n));cost={}
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

def su_controls(F,n):
    checked=0
    for i,j in itertools.combinations(range(len(F)),2):
        for mi,mj in itertools.product((0,1),repeat=2): # 1=all true; 0=all false
            req={};ok=True
            for c,mode in ((F[i],mi),(F[j],mj)):
                for x in c:
                    val=int(x>0) if mode else int(x<0)
                    if abs(x) in req and req[abs(x)]!=val:ok=False
                    req[abs(x)]=val
            def has_mode(a,c,mode):
                vals=[a[abs(x)]==int(x>0) for x in c]
                return all(vals) if mode else not any(vals)
            brute=any(has_mode(a,F[i],mi) and has_mode(a,F[j],mj)
                      for a in (assignment(n,z) for z in range(1<<n)))
            assert brute==ok;checked+=1
    return checked

def malformed_count():
    bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    return sum(not canonical(F,max([abs(x) for c in F for x in c],default=3)) for F in bad)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert canonical(F9,9) and canonical(Y6,6) and canonical(G6,6) and canonical(F15,15)
    roots={"F9":boundary_audit(F9,9),"Y6":boundary_audit(Y6,6),"G6":boundary_audit(G6,6)}
    gates,root,depth=compile_private(F9,9);ones=0
    for z in range(512):
        a=assignment(9,z);b=eval_private(gates,root,a);assert b==sat(F9,a);ones+=b
    obdd=obdd_extrema(F9,9);assert (len(gates),depth,ones,obdd)==(35,6,70,{"best":52,"natural":66,"worst":80})
    siblings=[]
    for x1 in (0,1):
        p={1:x1,4:0,5:1,8:0};siblings.append({"pins":p,**pin_table(F9,9,p)})
    assert [x["models"] for x in siblings]==[7,0]
    # Root positivity equivalence is not hereditary under pins: constant-true residuals have B=0.
    census=pin_census(F9,9);assert census["classes"]["SAT_ZERO_BOUNDARY_CONSTANT_TRUE"]>0
    f15=[]
    for q in ((1,0,0,0,1,1,1,1,0),(0,0,0,0,1,1,1,1,0)):
        p=dict(zip(range(7,16),q));f15.append({"pins":p,**pin_table(F15,15,p)})
    assert [x["models"] for x in f15]==[2,0]
    malformed=malformed_count();assert malformed==6
    out={
      "run":"BOUNDARY-CERTIFICATE-EQUIVALENCE-REFEREE286","timestamp_pacific":"2026-11-02T02:48:00-08:00",
      "status":"PROVED_EXACT_CERTIFICATE_EQUIVALENCE_PLUS_COMPUTATIONAL_CONTROLS","P_vs_NP":"OPEN",
      "scope":"valid proper duplicate-free canonical Docker monotone 3-SAT-(2,2) originals; residuals noncanonical",
      "theorem":"For canonical F, (a,i) with F(a)=1 and i pivotal is in bijection with a satisfying input (i,z) of the cofactor-XOR miter. A source scan of a marks exactly the variables uniquely satisfying a source clause and hence all pivots; there are at least n/3. Conversely two source evaluations of a miter witness recover its unique SAT endpoint. Both transformations take O(N) word work and O(n) explicit-output bits. Finding either certificate is not free and a decider need not output one.",
      "nonheredity":"After pins, boundary zero means the residual function is constant, not specifically UNSAT; constant-true residuals are SAT with zero boundary.",
      "falsifiers":[
        "All n miter circuits or the total boundary count must be materialized before one boundary certificate can be checked.",
        "A boundary certificate is asymptotically smaller than an explicit SAT witness.",
        "Zero cofactor boundary is a hereditary UNSAT certificate after original-variable pins.",
        "Exponential boundary cardinality establishes arbitrary-decider SAT hardness."],
      "charged_transform":{"witness_to_pivots":"one full source verification/scan, O(N) word work; O(n) mark bits if all pivots emitted; output each (i,z) costs Theta(n) bits",
        "miter_to_witness":"two source evaluations and one n-bit endpoint output, O(N) word work and O(n) writable/output bits",
        "not_charged_as_free":"certificate discovery, policy selection/switching, failed attempts, miter acquisition, source/index/head reads, proof/GE, cache/replay, child/output access, DELAY/COPY/RECOMP, simultaneous live ancestors"},
      "roots":roots,"F9":{"forward":{"gates":len(gates),"depth":depth,"truth_rows":512,"ones":ones},"obdd":obdd,
        "same_original_siblings":siblings,"pin_census":census,"su_modes_checked":su_controls(F9,9)},
      "F15_same_original_siblings":f15,"malformed_rejected":malformed,
      "exact_gap":"No method finds a SAT witness/boundary edge or proves their absence in polynomial total work on all valid canonical originals. No arbitrary-A power-short transformation or strict same-machine FLMV numerical transfer is proved.",
      "inherited_not_replayed":["U198/V198","saturated-cycle affine terminal"]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"run":out["run"],"roots":roots,"pin_census":census,"F9":out["F9"],"ok":True},sort_keys=True))
if __name__=="__main__":main()
