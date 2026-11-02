#!/usr/bin/env python3
"""REFEREE285: exact lazy/indexed continuation updates.

The theorem is about retained representations of F|p, not SAT decision.
All finite F9/Y6 controls are exhaustive.  No producer state is reused by the
independent verifier.
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
CODE={None:0,0:1,1:2}                 # U=00, 0/F=01, 1/T=10

def canonical(F,n):
    if not F or n%3 or 3*len(F)!=4*n:return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(type(x) is not int or not x or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def restrict_source(F,p):
    out=[]
    for c in F:
        states=[]
        for x in c:
            if abs(x) not in p:states.append(None)
            else:states.append(p[abs(x)]==int(x>0))
        if True in states:continue
        r=tuple(x for x,s in zip(c,states) if s is None)
        if not r:return "FALSE"
        out.append(r)
    return tuple(out) if out else "TRUE"

def occurrence_index(F,n):
    out=[[] for _ in range(n+1)]
    for ci,c in enumerate(F):
        for si,x in enumerate(c):out[abs(x)].append((ci,si))
    assert all(len(out[v])==4 for v in range(1,n+1))
    return out

def descriptor(F,n,p):
    """Fixed records: pin trits, signed occurrence U/F/T trits, summaries."""
    pins=tuple(CODE[p.get(v)] for v in range(1,n+1))
    slots=[]; summaries=[]
    for c in F:
        row=[]
        for x in c:
            if abs(x) not in p:s=None
            else:s=int(p[abs(x)]==int(x>0))
            row.append(CODE[s])
        slots.append(tuple(row))
        summaries.append((int(2 in row),sum(z==0 for z in row),sum(z==1 for z in row)))
    return pins,tuple(slots),tuple(summaries)

def decode(F,D):
    _,slots,_=D; out=[]
    for c,row in zip(F,slots):
        if 2 in row:continue
        r=tuple(x for x,z in zip(c,row) if z==0)
        if not r:return "FALSE"
        out.append(r)
    return tuple(out) if out else "TRUE"

def pop2(a,b):return (a^b).bit_count()

def model_count(F,n,p):
    free=[v for v in range(1,n+1) if v not in p];q=0
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));q+=sat(F,a)
    return q

def audit_states(F,n):
    states=rows=0;labels={};direct={}
    for vals in itertools.product((None,0,1),repeat=n):
        p={i+1:z for i,z in enumerate(vals) if z is not None}
        D=descriptor(F,n,p);R=restrict_source(F,p)
        assert decode(F,D)==R
        states+=1;direct[vals]=D
        free=[v for v in range(1,n+1) if v not in p];mc=0
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(p);a.update(zip(free,bits));b=sat(F,a);mc+=b;rows+=1
            if R=="TRUE":assert b
            elif R=="FALSE":assert not b
            else:assert b==all(any(a[abs(x)]==int(x>0) for x in c) for c in R)
        labels[vals]=mc>0
    return states,rows,labels,direct

def transition_audit(F,n,labels,direct):
    occ=occurrence_index(F,n);tot=pin_ext=label_flips=0
    slot_changes=summary_changes=core_dphys=0
    shist=collections.Counter();dhist=collections.Counter()
    for vals,D0 in direct.items():
        for v in range(1,n+1):
            old=vals[v-1]
            for new in (None,0,1):
                if new==old:continue
                nv=list(vals);nv[v-1]=new;nv=tuple(nv);D1=direct[nv]
                pin_diff=[i for i,(a,b) in enumerate(zip(D0[0],D1[0]),1) if a!=b]
                changed={(ci,si) for ci,(r0,r1) in enumerate(zip(D0[1],D1[1]))
                         for si,(a,b) in enumerate(zip(r0,r1)) if a!=b}
                assert pin_diff==[v] and changed==set(occ[v]) and len(changed)==4
                sc=sum(a!=b for a,b in zip(D0[2],D1[2]));shist[sc]+=1
                d=pop2(CODE[old],CODE[new])+sum(pop2(D0[1][ci][si],D1[1][ci][si]) for ci,si in changed)
                dhist[d]+=1;core_dphys+=d;summary_changes+=sc;slot_changes+=4;tot+=1
                if old is None and new is not None:pin_ext+=1
                if labels[vals]!=labels[nv]:label_flips+=1
    return {"directed_single_trit_transitions":tot,"pin_extension_transitions":pin_ext,
            "label_changing_transitions":label_flips,"occurrence_record_changes":slot_changes,
            "clause_summary_record_changes":summary_changes,
            "summary_change_histogram":dict(sorted(shist.items())),
            "core_fixed_layout_bit_xor":core_dphys,"core_dphys_histogram":dict(sorted(dhist.items()))}

def trail(F,n,gray):
    seq=[z^(z>>1) if gray else z for z in range(1<<n)]
    ds=[]
    for z in seq:
        p={v:(z>>(v-1))&1 for v in range(1,n+1)};ds.append(descriptor(F,n,p))
        assert sat(F,p)==all(s[0] for s in ds[-1][2])
    flips=occ=summary=core=0
    for z,w,a,b in zip(seq,seq[1:],ds,ds[1:]):
        h=(z^w).bit_count();flips+=h;occ+=4*h;core+=5*h
        summary+=sum(x!=y for x,y in zip(a[2],b[2]))
    endpoint=(seq[0]^seq[-1]).bit_count()
    return {"assignments":len(seq),"variable_flips":flips,"occurrence_record_changes":occ,
            "clause_summary_record_changes":summary,"core_fixed_layout_bit_xor":core,
            "endpoint_variable_delta":endpoint,"endpoint_occurrence_delta":4*endpoint,
            "endpoint_core_dphys":5*endpoint}

def private_stats(F):
    m=len(F);depth=2+(m-1).bit_length()
    return {"gates":3*m-1,"depth":depth}

def obdd_extrema(F,n):
    table=tuple(int(sat(F,{i+1:(z>>i)&1 for i in range(n)})) for z in range(1<<n));cost={}
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

def malformed_count():
    bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    return sum(not canonical(F,max([abs(x) for c in F for x in c],default=3)) for F in bad)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert canonical(F9,9) and canonical(Y6,6) and canonical(F15,15)
    fs,fr,fl,fd=audit_states(F9,9);ys,yr,_,_=audit_states(Y6,6)
    assert (fs,fr,ys,yr)==(3**9,4**9,3**6,4**6)
    trans=transition_audit(F9,9,fl,fd)
    assert trans["directed_single_trit_transitions"]==6*9*3**8
    assert trans["pin_extension_transitions"]==2*9*3**8
    siblings=[]
    for x1 in (0,1):
        p={1:x1,4:0,5:1,8:0};D=descriptor(F9,9,p)
        siblings.append({"pins":p,"models":model_count(F9,9,p),"residual":decode(F9,D),
                         "touched_clause_ids_for_x1":[ci+1 for ci,_ in occurrence_index(F9,9)[1]]})
    assert [x["models"] for x in siblings]==[7,0]
    f15=[]
    for q in ((1,0,0,0,1,1,1,1,0),(0,0,0,0,1,1,1,1,0)):
        p=dict(zip(range(7,16),q));f15.append({"pins":p,"models":model_count(F15,15,p)})
    assert [x["models"] for x in f15]==[2,0]
    obdd=obdd_extrema(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    binary=trail(F9,9,False);gray=trail(F9,9,True)
    assert binary["variable_flips"]==1013 and gray["variable_flips"]==511
    out={
      "run":"INDEXED-RESIDUAL-UPDATE-REFEREE285","status":"PROVED_EXACT_REPRESENTATION_PLUS_COMPUTATIONAL",
      "P_vs_NP":"OPEN","seed":285,
      "exact_theorem":"For every valid canonical source F and coherent original-variable pin state p, (F,p) is an exact retained continuation representation. A one-variable SET/UNSET/FLIP changes one pin record. With a paid source occurrence index and fixed occurrence cache, exactly four signed occurrence records and at most four clause-summary records change. Decoding is pointwise F|p. This does not decide existential SAT.",
      "models":{"lazy_pin":"retain authenticated source plus pin vector; O(1) word update, O(N) evaluation/decoding scan",
                "indexed_cache":"one source scan builds four occurrence addresses per variable; O(1) word update in the canonical bounded-occurrence grammar; O(N log N) retained bits",
                "fixed_bits":"U=00, false/0=01, true/1=10; core dphys counts pin and occurrence cells only; summaries reported separately",
                "tape_caveat":"word-RAM O(1) is not a native FLMV tape bound; binary addresses, head moves and index-tape semantics must be charged"},
      "falsifiers":[
        "Every adjacent coherent pin requires a fresh Omega(N) residual-circuit rebuild.",
        "Exact continuation equivalence requires a semantic equality oracle or assignment recovery.",
        "A constant-size retained-state update decides the residual SAT label.",
        "Logical/physical update distance alone yields an arbitrary-machine SAT lower bound."],
      "F9":{"models":sum(sat(F9,{v:(z>>(v-1))&1 for v in range(1,10)}) for z in range(512)),
            "pin_states":fs,"continuation_rows":fr,"transitions":trans,
            "forward_private":private_stats(F9),"obdd":obdd,"same_original":siblings,
            "binary_trail":binary,"gray_trail":gray},
      "Y6":{"models":sum(sat(Y6,{v:(z>>(v-1))&1 for v in range(1,7)}) for z in range(64)),
            "pin_states":ys,"continuation_rows":yr},
      "F15_same_original":f15,"malformed_rejections":malformed_count(),
      "charged_work":"Preprocess grammar/source and 4n occurrence addresses once. Each indexed RAM pin transition reads/writes the pin, four occurrence slots, and up to four three-slot clause summaries. Serialization/rebuild still pays Theta(N+|R_p|); evaluating a continuation scans source unless more caches are acquired. Search additionally charges every policy attempt/failure/switch, proof/GE/SCC, cache equality/replay, child/output/bit access and DELAY/COPY/RECOMP guest.",
      "peak_space":"Lazy pins use O(n) trit bits beyond authenticated source; indexed cache uses O(N log N) bits for addresses plus O(N) slot/summary bits and rollback frames. Simultaneously live ancestors, proofs, caches, children and guests remain charged.",
      "gap":"The theorem removes a per-transition reconstruction necessity but gives no SAT decision, no all-input polynomial aggregate-work potential, no arbitrary-A power-short A->Phi(A), and no strict same-machine numerical FLMV transfer.",
      "literature_queries":["incremental SAT solving assumptions primary paper MiniSat Een Sorensson 2003",
        "knowledge compilation conditioning OBDD primary paper Darwiche Marquis 2002",
        "dynamic Boolean formula evaluation updates bounded occurrence CNF primary paper",
        "watched literals SAT solver original Chaff 2001"],
      "github_queries":["j15marti/pnp occurrence index residual update pin unpin",
        "j15marti/pnp Gray binary pin trail physical writes",
        "github.com/openai SAT incremental assumptions watched literal occurrence list"]}
    assert out["F9"]["models"]==70 and out["Y6"]["models"]==20 and out["malformed_rejections"]==6
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")

if __name__=="__main__":main()
