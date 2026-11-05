#!/usr/bin/env python3
"""Finite controls for REFEREE358's mixed-to-Resolution retraction barrier.

The asymptotic impossibility theorem uses published Resolution lower bounds.
This program only checks that standard cubic Tseitin CNFs and the 4h-1 mixed
proof skeleton agree exactly on several finite graphs.  It is not evidence for
the asymptotic lower bound.
"""

from __future__ import annotations
import json
from itertools import product


GRAPHS = {
    "K4": (4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
    "K33": (6, [(i,j) for i in range(3) for j in range(3,6)]),
    "cube": (8, [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                  (0,4),(1,5),(2,6),(3,7)]),
    "Petersen": (10, [(0,1),(1,2),(2,3),(3,4),(4,0),
                       (5,7),(7,9),(9,6),(6,8),(8,5),
                       (0,5),(1,6),(2,7),(3,8),(4,9)]),
}


def validate_graph(h, edges):
    if not isinstance(h, int) or h <= 0:
        return False
    if any(not isinstance(e, tuple) or len(e) != 2 for e in edges):
        return False
    canon = []
    for u,v in edges:
        if not (isinstance(u,int) and isinstance(v,int) and 0 <= u < h and 0 <= v < h and u != v):
            return False
        canon.append(tuple(sorted((u,v))))
    if len(set(canon)) != len(canon):
        return False
    deg = [0]*h
    adj = [[] for _ in range(h)]
    for u,v in canon:
        deg[u]+=1; deg[v]+=1; adj[u].append(v); adj[v].append(u)
    if any(d != 3 for d in deg):
        return False
    seen={0}; todo=[0]
    while todo:
        u=todo.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); todo.append(v)
    return len(seen)==h


def incidence(h, edges):
    inc=[[] for _ in range(h)]
    for i,(u,v) in enumerate(edges, start=1):
        inc[u].append(i); inc[v].append(i)
    return inc


def vertex_clauses(vars3, rhs):
    clauses=[]
    for bits in product((0,1), repeat=3):
        if (bits[0]^bits[1]^bits[2]) != rhs:
            # block this falsifying row
            clauses.append(tuple(v if b==0 else -v for v,b in zip(vars3,bits)))
    return tuple(clauses)


def clause_true(clause, assignment):
    return any((assignment[abs(l)-1] == 1) == (l > 0) for l in clause)


def check_case(name, h, edges):
    assert validate_graph(h, edges)
    inc=incidence(h,edges)
    odd=[0]*h; odd[0]=1
    even=[0]*h
    out={"h":h,"edges":len(edges),"expected_mixed_nodes":4*h-1}
    for label,charges in (("odd",odd),("even",even)):
        cnf=[]; local_checks=0
        for v in range(h):
            cs=vertex_clauses(tuple(inc[v]),charges[v])
            assert len(cs)==4
            cnf.extend(cs)
            for bits in product((0,1),repeat=3):
                a=[0]*len(edges)
                for e,b in zip(inc[v],bits): a[e-1]=b
                relation=(bits[0]^bits[1]^bits[2])==charges[v]
                assert all(clause_true(c,a) for c in cs)==relation
                local_checks+=1
        models=0
        for a in product((0,1),repeat=len(edges)):
            if all(clause_true(c,a) for c in cnf): models+=1
        # Mixed skeleton: 3h paid local conjunction nodes, then h-1 row XORs.
        mask=0; rhs=0
        for v in range(h):
            row=0
            for e in inc[v]: row ^= 1 << (e-1)
            mask ^= row; rhs ^= charges[v]
        assert mask==0
        if label=="odd":
            assert rhs==1 and models==0
        else:
            assert rhs==0 and models==2**(len(edges)-h+1)
        out[label]={"clauses":len(cnf),"models":models,"local_truth_checks":local_checks,
                    "final_affine_mask":mask,"final_rhs":rhs}
    return out


def malformed_controls():
    fixtures=[
        (4,[(0,1),(0,1)]),
        (4,[(0,0),(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
        (4,[(0,1),(0,2),(0,3)]),
        (4,[(0,1),(0,2),(0,3),(1,2),(1,3),(2,4)]),
        (0,[]),
    ]
    rejected=sum(not validate_graph(h,e) for h,e in fixtures)
    assert rejected==len(fixtures)
    return {"fixtures":len(fixtures),"rejected":rejected}


def main():
    cases={name:check_case(name,h,edges) for name,(h,edges) in GRAPHS.items()}
    total_checks=sum(c[p]["local_truth_checks"] for c in cases.values() for p in ("odd","even"))
    print(json.dumps({
        "run":"LSPV5_REFEREE358",
        "status":{"finite_controls":"COMPUTATIONAL","asymptotic_resolution_lower_bound":"LITERATURE"},
        "cases":cases,
        "local_truth_checks":total_checks,
        "malformed":malformed_controls(),
        "scope":"Checks mixed proof skeleton only; does not prove the Resolution lower bound."
    },indent=2,sort_keys=True))


if __name__=="__main__": main()
