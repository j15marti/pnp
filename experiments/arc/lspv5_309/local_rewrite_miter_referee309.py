#!/usr/bin/env python3
"""Produce strict-Resolution certificates for paid local circuit rewrites.

REFEREE309: AND/XOR commutativity, associativity, congruence, equality
transitivity, and complete contradictory-output miter refutations.
"""
from __future__ import annotations
import json, resource, sys, time
from collections import defaultdict
from itertools import product
from pathlib import Path

def norm(xs):
    s=set(xs)
    if any(-x in s for x in s): return None
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def and_slots(q,a,b):
    return [norm((-q,a)),norm((-q,b)),norm((q,-a,-b))]

def xor_slots(q,a,b):
    return [norm((a,b,-q)),norm((a,-b,q)),norm((-a,b,q)),norm((-a,-b,-q))]

def resolve(c1,c2,p):
    if p not in c1 or -p not in c2:return None
    return norm([x for x in c1 if x!=p]+[x for x in c2 if x!=-p])

def prove(name,groups,targets,limit=30000):
    clauses=[]; parents=[]; kinds=[]; seen={}; pos=defaultdict(set); neg=defaultdict(set)
    def add(c,kind,par=None):
        if c is None or c in seen:return None
        i=len(clauses); seen[c]=i; clauses.append(c);parents.append(par);kinds.append(kind)
        for x in c:(pos if x>0 else neg)[abs(x)].add(i)
        return i
    for kind,cs in groups:
        for c in cs:add(c,kind)
    frontier=list(range(len(clauses)))
    nt=[norm(t) for t in targets]
    while frontier and not all(t in seen for t in nt):
        i=frontier.pop(0); c=clauses[i]; generated=[]
        for lit in c:
            v=abs(lit)
            for j in list(neg[v] if lit>0 else pos[v]):
                if i==j:continue
                if lit>0:r=resolve(c,clauses[j],v); par=(i,j,v)
                else:r=resolve(clauses[j],c,v); par=(j,i,v)
                if r is not None and r not in seen:generated.append((r,par))
        for r,par in generated:
            if r in seen:continue
            k=add(r,"RES",par); frontier.append(k)
        if len(clauses)>limit:raise RuntimeError(name+" closure limit")
    if not all(t in seen for t in nt):raise AssertionError(name+" target absent")
    tids=[seen[t] for t in nt]; need=set()
    def visit(i):
        if i in need:return
        need.add(i)
        if parents[i]:visit(parents[i][0]);visit(parents[i][1])
    for i in tids:visit(i)
    order=sorted(need); rem={x:i for i,x in enumerate(order)}; lines=[]
    for old in order:
        L={"clause":list(clauses[old]),"kind":kinds[old]}
        if parents[old]:
            a,b,p=parents[old];L.update(left=rem[a],right=rem[b],pivot=p)
        lines.append(L)
    return {"name":name,"lines":lines,"targets":[rem[i] for i in tids],
            "resolution_lines":sum(L["kind"]=="RES" for L in lines),
            "closure_clauses":len(clauses)}

def eval_cnf(cnf,n):
    models=[]
    for bits in product((0,1),repeat=n):
        A={i+1:bits[i] for i in range(n)}
        if all(any((x>0)==bool(A[abs(x)]) for x in c) for c in cnf):
            models.append("".join(map(str,bits)))
    return models

def malformed():
    def parse(s):
        z=s.split()
        if len(z)<4 or z[:2]!=["p","cnf"]:return False
        try:n,m=int(z[2]),int(z[3]); xs=[int(x) for x in z[4:]]
        except ValueError:return False
        cs=[];cur=[]
        for x in xs:
            if x==0:cs.append(cur);cur=[]
            elif not 1<=abs(x)<=n:return False
            else:cur.append(x)
        return not cur and len(cs)==m
    cases={"valid_sat":"p cnf 1 1 1 0","valid_unsat":"p cnf 1 2 1 0 -1 0",
           "bad_header":"cnf 1 1 1 0","bad_count":"p cnf 1 2 1 0",
           "bad_var":"p cnf 1 1 2 0","unterminated":"p cnf 1 1 1",
           "nonnumeric":"p cnf 1 1 x 0"}
    return {k:parse(v) for k,v in cases.items()}

def main():
    start=time.perf_counter()
    a,b,c,x,xp,y,u,v,p,q,r,s=range(1,13)
    specs=[]
    for gate,slots in (("and",and_slots),("xor",xor_slots)):
        specs.append(prove(f"{gate}_commutativity",
            [(f"DEF_{gate}_q_ab",slots(q,a,b)),(f"DEF_{gate}_r_ba",slots(r,b,a))],
            [(-q,r),(q,-r)]))
        specs.append(prove(f"{gate}_associativity",
            [(f"DEF_{gate}_u_ab",slots(u,a,b)),(f"DEF_{gate}_v_uc",slots(v,u,c)),
             (f"DEF_{gate}_p_bc",slots(p,b,c)),(f"DEF_{gate}_q_ap",slots(q,a,p))],
            [(-v,q),(v,-q)]))
        specs.append(prove(f"{gate}_congruence_left",
            [("ASSUME_x_eq_xp",[norm((-x,xp)),norm((x,-xp))]),
             (f"DEF_{gate}_q_xy",slots(q,x,y)),(f"DEF_{gate}_r_xpy",slots(r,xp,y))],
            [(-q,r),(q,-r)]))
        specs.append(prove(f"{gate}_commuted_miter",
            [(f"DEF_{gate}_q_ab",slots(q,a,b)),(f"DEF_{gate}_r_ba",slots(r,b,a)),
             ("UNIT_q",[norm((q,))]),("UNIT_not_r",[norm((-r,))])],[()]))
        specs.append(prove(f"{gate}_associated_miter",
            [(f"DEF_{gate}_u_ab",slots(u,a,b)),(f"DEF_{gate}_v_uc",slots(v,u,c)),
             (f"DEF_{gate}_p_bc",slots(p,b,c)),(f"DEF_{gate}_q_ap",slots(q,a,p)),
             ("UNIT_v",[norm((v,))]),("UNIT_not_q",[norm((-q,))])],[()]))
    specs.append(prove("equality_transitivity",
        [("ASSUME_q_eq_r",[norm((-q,r)),norm((q,-r))]),
         ("ASSUME_r_eq_s",[norm((-r,s)),norm((r,-s))])],
        [(-q,s),(q,-s)]))

    # Nonclone associated circuits have no input-fixing gate bijection: first
    # gate supports {a,b} on the left and {b,c} on the right.
    nonclone={"left_gate_supports":[[a,b],[u,c]],"right_gate_supports":[[b,c],[a,p]],
              "input_fixing_gate_isomorphism":False}
    # Same-label associated circuits are SAT; replacing right XOR by AND makes
    # contradictory outputs SAT (a,b,c)=(0,1,1).
    xor_same=xor_slots(u,a,b)+xor_slots(v,u,c)+xor_slots(p,b,c)+xor_slots(q,a,p)+[norm((v,)),norm((q,))]
    mixed_neighbor=xor_slots(u,a,b)+xor_slots(v,u,c)+and_slots(p,b,c)+xor_slots(q,a,p)+[norm((v,)),norm((-q,))]
    controls={
      "xor_associated_same_label_models":eval_cnf(xor_same,10)[:16],
      "xor_vs_and_neighbor_models":eval_cnf(mixed_neighbor,10)[:16],
      "malformed":malformed(),
      "nonclone_structure":nonclone,
      "rejected_shortcuts":{
        "semantic_equivalence_axiom":"REJECT: no authenticated source or fixed rule",
        "output_trace_only":"REJECT: contradictory output units prove UNSAT only with an equivalence certificate",
        "instance_advice":"REJECT: rewrite library is fixed before circuits"}}
    identity=[z for z in specs if "miter" not in z["name"] and z["name"]!="equality_transitivity"]
    B=max(z["resolution_lines"] for z in identity if "commutativity" in z["name"] or "associativity" in z["name"])
    C=max(z["resolution_lines"] for z in identity if "congruence" in z["name"])
    out={"tag":"LOCAL-REWRITE-MITER-REFEREE309",
         "fixed_fragment":"source-independent two-input signed AND/XOR VARDEF plus strict binary RES",
         "templates":specs,
         "constants":{"base_identity_res_max_B":B,"congruence_res_max_C":C,
           "context_measure":"a_i = number of distinct affected ancestor gates rebuilt in step i; two input changes are charged separately",
           "rewrite_bound":"W <= (B+4)r + (2C+4)sum(a_i) + 2",
           "instantiated_bound":f"W <= {B+4}r + {2*C+4}sum(a_i) + 2"},
         "totals":{"templates":len(specs),"resolution_lines":sum(z["resolution_lines"] for z in specs),
                   "certificate_lines":sum(len(z["lines"]) for z in specs),
                   "max_resolution_lines":max(z["resolution_lines"] for z in specs)},
         "controls":controls,
         "producer":{"wall_seconds":time.perf_counter()-start,
                     "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     "python":sys.version.split()[0]}}
    path=Path(sys.argv[1] if len(sys.argv)>1 else "referee309.json")
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out["constants"],sort_keys=True));print(json.dumps(out["totals"],sort_keys=True))
    print(json.dumps({"same_label_sat":bool(controls["xor_associated_same_label_models"]),
                      "mixed_neighbor_sat":bool(controls["xor_vs_and_neighbor_models"]),
                      "wall_seconds":out["producer"]["wall_seconds"],"peak_rss_kib":out["producer"]["peak_rss_kib"]},sort_keys=True))

if __name__=="__main__":main()
