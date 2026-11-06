#!/usr/bin/env python3
"""Falsify the tempting 35-node LOCAL-to-annotation shortcut on bridge control."""
from __future__ import annotations
import argparse, hashlib, json, resource, time
from pathlib import Path

N, A, MB = 15, 1 << 15, (1 << 15) // 8

def source():
    edges=[]
    for off in (0,5):
        for u in range(4):
            for v in range(u+1,4):
                edges += [(off,off+4),(off+4,off+1)] if (u,v)==(0,1) else [(off+u,off+v)]
    edges.append((4,9)); inc=[[] for _ in range(10)]
    for i,(u,v) in enumerate(edges,1):inc[u].append(i);inc[v].append(i)
    chi=[1]+[0]*9; F=[]; by=[]
    for v in range(10):
        ids=[]
        for t in range(8):
            b=((t>>2)&1,(t>>1)&1,t&1)
            if b[0]^b[1]^b[2]==chi[v]:continue
            ids.append(len(F));F.append([(-e if b[j] else e) for j,e in enumerate(inc[v])])
        by.append(ids)
    dimacs="p cnf 15 40\n"+"".join(" ".join(map(str,c))+" 0\n" for c in F)
    return edges,inc,chi,F,by,dimacs

def lit(l,a):return ((a>>(abs(l)-1))&1)==(l>0)
def cmask(c):return sum(1<<a for a in range(A) if any(lit(x,a) for x in c))
def amask(vs,r):return sum(1<<a for a in range(A) if sum((a>>(v-1))&1 for v in vs)%2==r)
def h(m):return hashlib.sha256(m.to_bytes(MB,"little")).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);z=ap.parse_args();t=time.perf_counter()
    edges,inc,chi,F,by,dimacs=source();sha=hashlib.sha256(dimacs.encode()).hexdigest()
    assert sha=="4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18"
    models=[];one={}
    for a in range(A):
        bad=[i for i,c in enumerate(F) if not any(lit(x,a) for x in c)]
        if not bad:models.append(a)
        if len(bad)==1:one.setdefault(bad[0],a)
    assert not models and len(one)==36
    sides=[]
    for side,endpoint in (((0,1,2,3,4),4),((5,6,7,8,9),9)):
        internal=[v for v in side if v!=endpoint]; vs=[]; rhs=0
        for v in internal:vs=sorted(set(vs)^set(inc[v]));rhs^=chi[v]
        boundary=amask(vs,rhs);bridge=15;non=[e for e in inc[endpoint] if e!=bridge]
        schi=0
        for v in side:schi^=chi[v]
        selected=[]
        for sid in by[endpoint]:
            wrong={abs(x):int(x<0) for x in F[sid]}
            if wrong[bridge]==1^schi and wrong[non[0]]^wrong[non[1]]==rhs:selected.append(sid)
        assert len(selected)==2
        pair=cmask(F[selected[0]])&cmask(F[selected[1]]);joined=pair&boundary;unit=amask([bridge],schi)
        support=sorted(set(vs)|{bridge});matches=[]
        for subset in range(1<<len(support)):
            row=[support[i] for i in range(len(support)) if subset>>i&1]
            for r in (0,1):
                if amask(row,r)==joined:matches.append({"vars":row,"rhs":r})
        witness=next(a for a in range(A) if unit>>a&1 and not joined>>a&1)
        assert joined&~unit==0 and joined!=unit and not matches
        sides.append({"vertices":list(side),"endpoint":endpoint,"boundary":{"vars":vs,"rhs":rhs},
          "selected_source_ids":selected,"joined_support":support,"side_charge":schi,
          "joined_models":joined.bit_count(),"unit_models":unit.bit_count(),"joined_implies_unit":True,
          "joined_equals_unit":False,"any_exact_affine_annotation":False,
          "joined_mask_sha256":h(joined),"unit_mask_sha256":h(unit),
          "unit_not_joined_witness":witness,
          "witness_bits":{str(v):(witness>>(v-1))&1 for v in support}})
    out={"run":"LSPV-5/REFEREE387","timestamp_pst":"2026-11-06 06:48 PST",
      "status":"PROVED-RESTRICTED semantic annotation firewall; COMPUTATIONAL exhaustive finite replay",
      "source":{"variables":N,"clauses":F,"edges":edges,"incident":inc,"charges":chi,"dimacs_sha256":sha},
      "core":sorted(one),"deletion_witnesses":{str(k):v for k,v in sorted(one.items())},
      "attempt":{"base_trace_work":37,"proposed_work":35,
        "rewrite":"replace each LOCAL by a unit affine annotation on its parent AND3; replace final RES by XOR",
        "verdict":"ILLEGAL: each joined factor strictly implies, but is not exactly equivalent to, the proposed unit row"},
      "sides":sides,"consequence":{"global_interval":"35 <= W_Rmix341(F_bridge) <= 37 remains open",
        "excluded_class":"the specific two-LOCAL coalescing rewrite and every single-row annotation of either joined factor",
        "not_excluded":"another legal 35- or 36-node mixed DAG"},
      "resource":{"assignments_scanned":A,"candidate_affine_rows_per_side":16,
        "logical_candidate_nodes_replayed":35,"explicit_evidence_bits":2*MB*8,
        "elapsed_seconds":round(time.perf_counter()-t,6),"max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
      "scope":"Independent declared-semantic /341 replay; not the unavailable authoritative historical byte checker; no asymptotic mixed lower bound"}
    p=Path(z.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"pass":True,"out":str(p),"joined_models":[x["joined_models"] for x in sides],
      "unit_models":[x["unit_models"] for x in sides],"affine_matches":[x["any_exact_affine_annotation"] for x in sides]},sort_keys=True))
if __name__=="__main__":main()
