#!/usr/bin/env python3
"""REFEREE281: paid one-variable existential projection circuits.

The circuit computes (exists x)F, not the forward function F itself.  It is an
exact SAT-preserving escape from forward-evaluator gate counts, but repeated
elimination is not proved polynomial.
"""
from __future__ import annotations
import argparse,collections,itertools,json
from functools import lru_cache
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
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,z):
    return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)

def best_matching(F,ids):
    ids=tuple(ids)
    E={(i,j):len(set(map(abs,F[i]))&set(map(abs,F[j]))) for i,j in itertools.combinations(ids,2)}
    E={e:w for e,w in E.items() if w}
    @lru_cache(None)
    def go(mask):
        if not mask:return 0,()
        p=(mask&-mask).bit_length()-1;i=ids[p];best=go(mask&~(1<<p))
        for q in range(p+1,len(ids)):
            if not(mask>>q)&1:continue
            j=ids[q];e=(min(i,j),max(i,j))
            if e in E:
                w,pairs=go(mask&~(1<<p)&~(1<<q));cand=(w+E[e],pairs+((i,j,E[e]),))
                if cand[0]>best[0]:best=cand
        return best
    return go((1<<len(ids))-1)

class Circuit:
    def __init__(self):self.g=[]
    @staticmethod
    def X(v):return f"x{v}"
    def add(self,op,a,b):
        z=f"g{len(self.g)}";self.g.append({"op":op,"a":a,"b":b});return z
    def value(self,out,z):
        vals=[]
        def val(t):return (z>>(int(t[1:])-1))&1 if t[0]=="x" else vals[int(t[1:])]
        for g in self.g:
            a,b=val(g["a"]),val(g["b"])
            vals.append(int((a and b) if g["op"]=="AND" else ((a or b) if g["op"]=="OR" else not(a and b))))
        return val(out)
    def depth(self,t):
        if t[0]=="x":return 0
        g=self.g[int(t[1:])];return 1+max(self.depth(g["a"]),self.depth(g["b"]))

def join_and(C,outs):
    if not outs:return None
    while len(outs)>1:
        nxt=[]
        for i in range(0,len(outs),2):
            nxt.append(C.add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i])
        outs=nxt
    return outs[0]

def singleton(C,c):
    a,b,d=sorted(map(abs,c))
    return C.add("OR",C.add("OR",C.X(a),C.X(b)),C.X(d)) if c[0]>0 else C.add("NAND",C.add("AND",C.X(a),C.X(b)),C.X(d))

def matched_pair(C,F,i,j):
    A=set(map(abs,F[i]));B=set(map(abs,F[j]));common=sorted(A&B);ra=sorted(A-B);rb=sorted(B-A)
    if F[i][0]>0 and len(common)==2:
        return C.add("OR",C.add("OR",C.X(common[0]),C.X(common[1])),C.add("AND",C.X(ra[0]),C.X(rb[0])))
    if F[i][0]>0:
        return C.add("OR",C.X(common[0]),C.add("AND",C.add("OR",C.X(ra[0]),C.X(ra[1])),C.add("OR",C.X(rb[0]),C.X(rb[1]))))
    if len(common)==2:
        return C.add("NAND",C.add("AND",C.X(common[0]),C.X(common[1])),C.add("OR",C.X(ra[0]),C.X(rb[0])))
    return C.add("NAND",C.X(common[0]),C.add("OR",C.add("AND",C.X(ra[0]),C.X(ra[1])),C.add("AND",C.X(rb[0]),C.X(rb[1]))))

def build_remaining(C,F,ids):
    pos=[i for i in ids if F[i][0]>0];neg=[i for i in ids if F[i][0]<0]
    wp,mp=best_matching(F,pos);wn,mn=best_matching(F,neg);pairs=mp+mn;used={q for p in pairs for q in p[:2]}
    outs=[matched_pair(C,F,i,j) for i,j,w in pairs]
    outs += [singleton(C,F[i]) for i in ids if i not in used]
    return join_and(C,outs),wp+wn,[list(x) for x in pairs]

def projected_circuit(F,v):
    incp=[i for i,c in enumerate(F) if v in c];incn=[i for i,c in enumerate(F) if -v in c]
    assert len(incp)==len(incn)==2
    C=Circuit();tails_p=[sorted(set(map(abs,F[i]))-{v}) for i in incp];tails_n=[sorted(set(map(abs,F[i]))-{v}) for i in incn]
    cp=set(tails_p[0])&set(tails_p[1]);cn=set(tails_n[0])&set(tails_n[1]);d=int(bool(cp))+int(bool(cn))
    if cp:
        a=next(iter(cp));u=next(iter(set(tails_p[0])-{a}));w=next(iter(set(tails_p[1])-{a}))
        P=C.add("OR",C.X(a),C.add("AND",C.X(u),C.X(w)))
    else:
        P=C.add("AND",C.add("OR",C.X(tails_p[0][0]),C.X(tails_p[0][1])),C.add("OR",C.X(tails_p[1][0]),C.X(tails_p[1][1])))
    if cn:
        a=next(iter(cn));u=next(iter(set(tails_n[0])-{a}));w=next(iter(set(tails_n[1])-{a}))
        N=C.add("NAND",C.X(a),C.add("OR",C.X(u),C.X(w)))
    else:
        N=C.add("AND",C.add("NAND",C.X(tails_n[0][0]),C.X(tails_n[0][1])),C.add("NAND",C.X(tails_n[1][0]),C.X(tails_n[1][1])))
    Q=C.add("OR",P,N)
    remaining=[i for i,c in enumerate(F) if v not in map(abs,c)]
    H,W,pairs=build_remaining(C,F,remaining)
    out=C.add("AND",H,Q) if H is not None else Q
    expected=3*len(F)-5-W-d
    assert len(C.g)==expected
    return C,out,{"variable":v,"gate_count":len(C.g),"depth":C.depth(out),"remaining_matching_weight":W,
                  "incident_tail_shares":d,"remaining_pairs":pairs,"output":out,"gates":C.g}

def projection_models(F,n,v):
    count=0
    for y in range(1<<(n-1)):
        lo=y&((1<<(v-1))-1);hi=y>>(v-1);z=lo|(hi<<v)
        count+=sat(F,z) or sat(F,z|(1<<(v-1)))
    return count

def forward_matched_count(F):
    p=[i for i,c in enumerate(F) if c[0]>0];n=[i for i,c in enumerate(F) if c[0]<0]
    W=best_matching(F,p)[0]+best_matching(F,n)[0]
    return 3*len(F)-1-W,W

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        pred=(not opp,not same,not same,not opp);act=[False]*4
        for z in range(1<<n):
            AS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in A);AU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in A)
            BS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in B);BU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in B)
            act=[u or w for u,w in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(act)==pred;checks+=4
    return checks

def obdd_counts(F,n):
    costs={};full=(1<<n)-1
    for mask in range(1<<n):
        A=[i for i in range(n) if (mask>>i)&1];R=[i for i in range(n) if not(mask>>i)&1];S=set()
        for aa in range(1<<len(A)):
            sig=0
            for rr in range(1<<len(R)):
                z=sum(((aa>>k)&1)<<i for k,i in enumerate(A))+sum(((rr>>k)&1)<<i for k,i in enumerate(R));sig|=sat(F,z)<<rr
            S.add(sig)
        for p,v in enumerate(R):
            q=0
            for sig in S:
                lo=hi=0
                for y in range(1<<(len(R)-1)):
                    i=(y&((1<<p)-1))|((y>>p)<<(p+1));lo|=((sig>>i)&1)<<y;hi|=((sig>>(i|1<<p))&1)<<y
                q+=lo!=hi
            costs[mask,v]=q
    @lru_cache(None)
    def dp(mask,worst=False):
        if mask==full:return 0
        vals=[costs[mask,v]+dp(mask|1<<v,worst) for v in range(n) if not(mask>>v)&1]
        return max(vals) if worst else min(vals)
    mask=natural=0
    for v in range(n):natural+=costs[mask,v];mask|=1<<v
    return {"best":dp(0),"natural":natural,"worst":dp(0,True)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    fixtures={"Y6":(Y6,6),"F9":(F9,9),"F15":(F15,15)};all_meta={};rows=0
    for name,(F,n) in fixtures.items():
        assert canonical(F,n);projects=[];forward,W=forward_matched_count(F)
        for v in range(1,n+1):
            C,out,meta=projected_circuit(F,v);models=0
            for y in range(1<<(n-1)):
                lo=y&((1<<(v-1))-1);hi=y>>(v-1);z=lo|(hi<<v);want=int(sat(F,z) or sat(F,z|1<<(v-1)))
                assert C.value(out,z)==want;models+=want;rows+=1
            assert models==projection_models(F,n,v);meta["projected_models"]=models;projects.append(meta)
        all_meta[name]={"n":n,"m":len(F),"forward_matched_gates":forward,"forward_matching_weight":W,"projections":projects}
    common={3:0,5:1,6:0,7:0,8:0};free=[2,4,9];low=high=proj=0
    for y,bits in enumerate(itertools.product((0,1),repeat=3)):
        z=sum(value<<(var-1) for var,value in common.items())+sum(value<<(var-1) for var,value in zip(free,bits))
        qa=sat(F9,z);qb=sat(F9,z|1);low+=qa;high+=qb;proj+=qa or qb
        assert qa==int(bits[0] and bits[2]) and not qb
    assert (low,high,proj)==(2,0,2)
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not canonical(x,max([abs(v) for c in x for v in c],default=3)) for x in malformed)
    obdd=obdd_counts(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    controls={"projection_truth_rows":rows,"F9_same_original_child_models":{"x1_0_SAT":low,"x1_1_UNSAT":high,"exists_x1":proj},
              "F9_SU_modes":su_modes(F9),"malformed_rejected":6,"F9_OBDD_nodes":obdd}
    result={"run":"EXISTENTIAL-LOCAL-PROJECTION-REFEREE281","timestamp_pst":"2026-11-01 21:48","status":"PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL","P_vs_NP":"OPEN",
      "obstruction":"A lower bound on a circuit computing the full forward function F does not lower-bound a SAT-equivalent circuit computing an existential projection; discovering and iterating projections must still be charged.",
      "theorem":"For canonical F and original variable x, the declared source-local projection architecture computes (exists x)F exactly with g=3m-5-W_x-d_x gates, where W_x is maximum matching weight among nonincident same-sign clauses and d_x counts the two incident same-sign tail-sharing opportunities.",
      "fixtures":all_meta,"controls":controls,
      "falsified":["every SAT-preserving circuit state must compute the same forward function F","the 28-gate F9 forward evaluator lower-bounds every first decision-preserving circuit","a 52-node best-order OBDD is necessary before a source-aware first existential projection"],
      "charged_work":{"one_projection":"grammar/source authentication + four incident lists + remaining intersection graph + maximum-weight matching + gate/provenance writes + exact source-index/head access","controller":"W_D=grammar+source/index/head+all discovery, failed choices and switches+projection/circuit writes+semantic/proof/GE checks+cache/replay+child/output/bit access+guest DELAY/COPY/RECOMP+sum over every evaluated successor","peak":"maximum co-live source parser, incidence lists, matching graph/state, projected circuit, proof/cache, ancestors, children, index/head and guest space"},
      "exact_gap":"One projection is polynomial and removes one input, but repeated elimination may create overlapping noncanonical circuits/functions of exponential size; no polynomial bound on the total successor/projection sum or policy acquisition is proved.",
      "scope":["projected circuit is not C_F and is not a canonical child","exact only in the declared source-local matched architecture","not unrestricted circuit minimization","not an all-input SAT solver","no arbitrary-A power-short Phi(A)","no strict same-machine FLMV numerical transfer"],
      "literature_queries":["primary paper bucket elimination SAT existential variable elimination Dechter","Bryant 1986 graph based algorithms Boolean function manipulation ordered binary decision diagrams existential quantification","Davis Putnam 1960 variable elimination satisfiability resolution paper","GitHub j15marti/pnp existential projection; Davis-Putnam; 3m-5 circuit","GitHub org:openai existential quantification BDD; variable elimination SAT"],
      "github_findings":{"project":"many general existential/cofactor references; no exact 3m-5-W_x-d_x source-local formula found","openai":"zero code-search hits for both queried phrases; absence is not novelty evidence"},
      "large_controls":{"U198_V198":"inherited authenticated opposite-label controls; not used to prove this local projection theorem"}}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","rows":rows,"F9_projection_gates":[p["gate_count"] for p in all_meta["F9"]["projections"]],"F9_projection_models":[p["projected_models"] for p in all_meta["F9"]["projections"]],"controls":controls,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
