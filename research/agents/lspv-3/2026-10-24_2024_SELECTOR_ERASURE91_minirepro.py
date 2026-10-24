#!/usr/bin/env python3
"""Finite selector-mask and Tseitin-prism audit, independent of SAT packages.
No finite test implies unrestricted SAT hardness. Python standard library only.
"""
from itertools import product
import json, hashlib, argparse
from pathlib import Path

CHECKS = 0
def test(statement, label):
    global CHECKS
    CHECKS += 1
    if not statement: raise AssertionError(label)

def parity(x): return x.bit_count() & 1

def prism(q):
    test(q >= 3, "prism q")
    edges = []
    for layer in range(2):
        for j in range(q):
            edges.append(((layer,j),(layer,(j+1)%q)))
    for j in range(q): edges.append(((0,j),(1,j)))
    verts = [(a,j) for a in range(2) for j in range(q)]
    star = {v:tuple(k+1 for k,(a,b) in enumerate(edges) if v in (a,b)) for v in verts}
    test(len(edges)==3*q and len(verts)==2*q,"prism size")
    for v in verts: test(len(star[v])==3,"cubic")
    return verts,edges,star

def source(q, odd):
    vs,es,star=prism(q)
    charge={v:int(odd and v==vs[0]) for v in vs}
    clauses=[]
    for v in vs:
        for bits in range(8):
            if parity(bits)!=charge[v]:
                cl=tuple((-e if bits&(1<<j) else e) for j,e in enumerate(star[v]))
                clauses.append((v,bits,cl))
    test(len(clauses)==8*q,"clause count")
    for _,_,cl in clauses: test(len({abs(x) for x in cl})==3,"proper")
    return dict(q=q,verts=vs,edges=es,clauses=clauses,charge=charge)

def sat_clause(c,x):
    return any(bool(x&(1<<(abs(l)-1)))==(l>0) for l in c)

def count_source(F):
    es,cs=F['edges'],F['clauses']
    n_model=0
    one_deleted=[0]*len(cs)
    for a in range(1<<len(es)):
        failed=[i for i,(_,_,cl) in enumerate(cs) if not sat_clause(cl,a)]
        if not failed: n_model+=1
        if len(failed)==1: one_deleted[failed[0]]+=1
    odd=any(F['charge'].values())
    test(n_model==(0 if odd else 2**(len(es)-len(F['verts'])+1)), "SAT parity")
    if odd:
        expected=2**(len(es)-len(F['verts'])-1)
        for count in one_deleted: test(count==expected,"min UNSAT deletion count")
    return dict(source_variables=len(es),clauses=len(cs),SAT_models=n_model,
                deleted_clause_lifts_min=min(one_deleted),
                deleted_clause_lifts_max=max(one_deleted),
                enumerated_edge_assignments=1<<len(es))

def detached(truth,keep):
    ks=[j for j in range(3) if (keep>>j)&1]
    for vals in product((0,1),repeat=len(ks)):
        A=B=False
        for u in product((0,1),repeat=3):
            if any(u[j]!=value for j,value in zip(ks,vals)): continue
            A |= sum(u)%2==1
            B |= sum(u)<=1 and all(not u[j] or truth[j] for j in range(3))
        if A and B: return True
    return False

def run():
    for truth in product((False,True),repeat=3):
        for mask in range(8):
            test(detached(truth,mask)==(any(truth) if mask==7 else True),
                 "detached projection mask identity")
    groups=[]
    for q in (3,4,5,6):
        sat,unsat=source(q,False),source(q,True)
        test([tuple(map(abs,c)) for _,_,c in sat["clauses"]]
             ==[tuple(map(abs,c)) for _,_,c in unsat["clauses"]], "matched unsigned supports")
        sdata,udata=count_source(sat),count_source(unsat)
        controls=0
        # One witness for every omitted original clause, then all three
        # ways to omit an associated shared selector coordinate.
        selected=[None]*len(unsat['clauses'])
        for assignment in range(1<<len(unsat['edges'])):
            failures=[i for i,(_,_,cl) in enumerate(unsat['clauses'])
                      if not sat_clause(cl,assignment)]
            if len(failures)==1 and selected[failures[0]] is None:
                selected[failures[0]]=assignment
        for i,(_,_,cl) in enumerate(unsat['clauses']):
            a=selected[i]
            test(a is not None, "one-clause witness exists")
            truth=tuple(bool(a&(1<<(abs(l)-1)))==(l>0) for l in cl)
            test(truth==(False,False,False),"violated selected clause")
            for j in range(3):
                test(detached(truth,7^(1<<j)),"single selector erased")
                controls+=1
        udata.update(selector_bits=3*len(unsat['clauses']),
                     erasure_checks=controls)
        groups.append(dict(q=q,SAT=sdata,UNSAT=udata))
    return dict(status="COMPUTATIONAL finite audit, not all-decider coverage",
                seed=None,checks=CHECKS,
                local_truth_mask_checks=64,groups=groups,unexpected_discrepancies=0)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="selector_erasure91_results.json")
    args=parser.parse_args()
    d=run()
    data=json.dumps(d,indent=2,sort_keys=True)+"\n"
    Path(args.out).write_text(data,encoding="utf-8")
    print("PASS",CHECKS,"checks; output SHA256",hashlib.sha256(data.encode()).hexdigest())
