#!/usr/bin/env python3
"""LSPV-5 red-team: near-linear guest re-entry is not ARC contraction.

This is an exact finite/asymptotic accounting control, not a SAT lower bound.
It authenticates canonical sources, constructs a connected valid F9-chain,
checks same-source opposite labels at t=1, and charges DELAY/COPY/RECOMP.
"""
from __future__ import annotations

import argparse, json
from itertools import product
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),
     (8,12,14),(9,13,15),(10,14,15),(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),
     (-4,-5,-13),(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
     (-9,-10,-14),(-10,-7,-15))
PS={1:0,2:0,8:1,9:1}; PU={3:0,6:1,7:1,9:1}
YPS={5:0,6:1}; YPU={3:1,4:0,5:0,6:1}
F15PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def valid(F,n):
    if 3*len(F)!=4*n:return False
    seen=set(); deg={(v,s):0 for v in range(1,n+1) for s in (0,1)}
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)>n or x==0 for x in c):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        for x in c:deg[abs(x),int(x>0)]+=1
    return all(v==2 for v in deg.values())

def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def models(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]; out=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if sat(F,a):out.append(a)
    return out

def residual(F,p):
    return [tuple(x for x in c if abs(x) not in p) for c in F
            if not any(abs(x) in p and p[abs(x)]==int(x>0) for x in c)]

def enc_bits(F,n):
    w=max(1,n.bit_length()); h=max(8,max(n,len(F)).bit_length())
    return 2*h+sum(2+len(c)*(1+w) for c in F)

def connected_chain(t):
    F=[tuple((1 if x>0 else -1)*(abs(x)+9*b) for x in c)
       for b in range(t) for c in F9]
    # Swap the first literal of positive clause 0 across each boundary.  This
    # preserves every signed occurrence count and creates cross-block edges.
    for b in range(t-1):
        i=12*b; j=12*(b+1); A=list(F[i]); B=list(F[j]); A[0],B[0]=B[0],A[0]
        F[i]=tuple(A);F[j]=tuple(B)
    return tuple(F)

def shifted(p,t):return {v+9*b:x for b in range(t) for v,x in p.items()}

def primal_connected(F,n):
    G={v:set() for v in range(1,n+1)}
    for c in F:
        vs=list(map(abs,c))
        for u in vs:
            G[u].update(v for v in vs if v!=u)
    seen={1}; stack=[1]
    while stack:
        u=stack.pop()
        for v in G[u]-seen:seen.add(v);stack.append(v)
    return len(seen)==n

def protocol(N,M,q):
    Q=M**q; iw=(M+1).bit_length()
    return {
      "q":q,"DELAY_native_steps_lower_bound":Q,
      "RECOMP_virtual_bit_queries":Q,"RECOMP_full_parent_reads":N*Q,
      "RECOMP_index_writes_lower_bound":Q*iw,
      "COPY_child_writes":M,"COPY_child_plus_index_peak_writable_bits":M+iw,
      "logical_residual_endpoint_xor":0,
      "warning":"DELAY and source reads may have zero logical data-bit delta; COPY may have zero logical residual delta while writing a shadow."
    }

def malformed(F):
    return (F+(F[0],), tuple(((-c[0],)+c[1:] if i==0 else c) for i,c in enumerate(F)),
            tuple(((c[0],c[0],c[2]) if i==0 else c) for i,c in enumerate(F)),
            F[1:], tuple(((c[0],c[1],999) if i==0 else c) for i,c in enumerate(F)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    assert valid(F9,9) and valid(Y6,6) and valid(F15,15)
    assert all(not valid(x,9) for x in malformed(F9))
    f9root=models(F9,9,{}); fs=models(F9,9,PS); fu=models(F9,9,PU)
    ys=models(Y6,6,YPS); yu=models(Y6,6,YPU); f15s=models(F15,15,F15PS)
    assert (len(f9root),len(fs),len(fu),len(ys),len(yu),len(f15s))==(70,2,0,6,0,2)
    RS,RU=residual(F9,PS),residual(F9,PU)
    N,MS,MU=enc_bits(F9,9),enc_bits(RS,9),enc_bits(RU,9)
    assert (N,MS,MU)==(220,88,78)
    exhaustive=[]
    for bits in product((0,1),repeat=5):
        a={**PU,**dict(zip([1,2,4,5,8],bits))}
        bad=[j for j,c in enumerate(F9) if not any(a[abs(x)]==int(x>0) for x in c)]
        assert bad;exhaustive.append({"free_bits":bits,"first_falsified_original_clause":bad[0]})
    fam=[]
    for t in (1,2,3,4,8,16,32):
        F=connected_chain(t);n=9*t
        assert valid(F,n) and primal_connected(F,n)
        p=shifted(PS,t); R=residual(F,p);Nt=enc_bits(F,n);Mt=enc_bits(R,n)
        fam.append({"t":t,"n":n,"m":len(F),"connected":True,"valid":True,
                    "source_bits":Nt,"residual_bits":Mt,"ratio":Mt/Nt,
                    "residual_clauses":len(R)})
    out={
      "run":"LSPV5_NEARLINEAR_GUEST_REENTRY_REFEREE267",
      "timestamp_pacific":"2026-11-01 07:48 PST",
      "classification":"PROVED exact black-box re-entry lemma; COMPUTATIONAL finite controls; NOT an all-SAT lower bound",
      "obstruction":"Exact fallback gives completeness, but a reachable near-linear guest call preserves an arbitrary unknown polynomial exponent; full-parent lazy access adds a factor N.",
      "falsifiers":[
        "A selector can obtain strict ARC contraction while handing an arbitrary unknown-exponent guest a Theta(N)-bit residual.",
        "Exact fallback plus finite local terminals implies polynomial total work.",
        "Logical XOR lower-bounds DELAY, read-only RECOMP, or shadow COPY work.",
        "Finite F9/Y6/F15/U198/V198 coverage proves an all-input potential."
      ],
      "lemma":{
        "statement":"If a reachable state waits for a correct A_q on a child of M(N)>=c*N^lambda bits, where A_q delays M^q steps before a fixed exact decider, then T_D^{A_q}(N)>=M(N)^q=Omega(N^(lambda*q)). If a faithful lazy interface instead services M^q child-bit requests by Theta(N)-bit source rescans, its access work is Omega(N*M^q). Thus lambda=1 is not a power-short unknown-exponent ARC contraction.",
        "quantifiers":"For every fixed q>=1, A_q is a uniform correct polynomial decider whenever the base A_0 is. The lower bound is conditional on an actual reachable call that waits for A_q; it is not a lower bound on controllers that avoid that call.",
        "recurrence":"T_D^A(F)>=C_grammar+C_acquire+C_select+C_emit+T_A(child)+C_verify+C_output; for A_q, T_Aq(child)>=M^q. With lazy RECOMP Q=M^q, C_access>=NQ. Exact fallback T_fb proves termination only; if T_fb is exponential, T_D remains exponential absent a separate global progress bound.",
        "space":"COPY retains at least M child bits plus index/guest work; streaming can reduce retained child space but random child access is then paid by recomputation/source reads. Simultaneous peak, not additive phase maxima, is required.",
        "gap":"This rejects one monolithic near-linear black-box route. It neither proves P!=NP nor rules out a different controller with power-short children, decomposition, or a direct polynomial algorithm."
      },
      "sources":{
        "F9":{"valid":True,"root_models":70,"SAT_cube_models":2,"UNSAT_cube_models":0,
              "source_bits":N,"SAT_residual_bits":MS,"UNSAT_residual_bits":MU,
              "UNSAT_completion_rows":len(exhaustive),"UNSAT_proof":exhaustive},
        "Y6":{"valid":True,"root_models":len(models(Y6,6,{})),"SAT_cube_models":6,"UNSAT_cube_models":0},
        "F15":{"valid":True,"SAT_cube_models":2},"malformed_rejections":5
      },
      "connected_family":fam,
      "charged_protocols":{"F9_SAT":[protocol(N,MS,q) for q in (1,2,3)],
                           "F9_UNSAT":[protocol(N,MU,q) for q in (1,2,3)]},
      "xor_status":"OFFLINE diagnostic only; zero endpoint delta is compatible with arbitrarily many DELAY/READ/RECOMP steps and changed-then-restored index cells.",
      "heredity_status":"Original chain members are valid target inputs; residual children are noncanonical and require paid encoding/access. No target-valid reencoder is proved.",
      "P_versus_NP":"OPEN"
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","F9":(70,2,0),"Y6":(20,6,0),"F15_SAT":2,
                      "family_rows":len(fam),"N_M":(N,MS,MU),"P_vs_NP":"OPEN"},indent=2))
if __name__=='__main__':main()
