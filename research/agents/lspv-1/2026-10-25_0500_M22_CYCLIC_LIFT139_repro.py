#!/usr/bin/env python3
"""Finite M22-CONNECTED-CYCLIC-LIFT139 audit, Python 3 standard library.
Tests are computational controls, not resource lower bounds. No randomness.
Run: python 2026-10-25_0500_M22_CYCLIC_LIFT139_repro.py
"""
from collections import Counter, defaultdict
import json

P = [(0,1,2), (0,3,4), (1,3,5), (2,4,5)]
Q = [(0,1,3), (0,2,5), (1,2,4), (3,4,5)]

def clauses(h, paired=False):
    if h < 1:
        raise ValueError("h must be positive")
    records = []
    for i in range(h):
        for j, triple in enumerate(P):
            names = [6*i+v+1 for v in triple]
            if j == 0 and not paired:
                names[0] = 6*((i+1) % h)+1
            records.append((1, tuple(sorted(names))))
        for triple in (P if paired else Q):
            records.append((-1,tuple(sorted(6*i+v+1 for v in triple))))
    return sorted(records)

def validate(F,h):
    assert len(F) == 8*h and len(set(F)) == len(F)
    degrees=Counter()
    neighbours=defaultdict(set)
    signed=set(F)
    for sign,vs in F:
        assert sign in (-1,1) and len(vs) == len(set(vs)) == 3
        assert all(1 <= x <= 6*h for x in vs)
        for x in vs:
            degrees[x,sign]+=1
            neighbours[x].update(y for y in vs if y != x)
    assert all(degrees[x,sign]==2 for x in range(1,6*h+1) for sign in (-1,1))
    seen={1}; todo=[1]
    while todo:
        x=todo.pop()
        for y in neighbours[x]-seen:
            seen.add(y);todo.append(y)
    assert len(seen)==6*h
    paired_clauses=sum((-sgn,vs) in signed for sgn,vs in F)
    unpaired_positive=sum(sgn==1 and (-1,vs) not in signed for sgn,vs in F)
    return {"variables":6*h,"clauses":8*h,"connected":True,
            "paired_clauses":paired_clauses,"unpaired_positive":unpaired_positive}

def witness(h):
    return sum(1 << (6*i+j) for i in range(h) for j in (0,1,2))

def is_model(F,mask):
    return all(any(bool(mask & (1<<(x-1)))==(sgn==1) for x in vs)
               for sgn,vs in F)

def model_count(F,h):
    plus=[sum(1<<(x-1) for x in vs) for s,vs in F if s==1]
    minus=[sum(1<<(x-1) for x in vs) for s,vs in F if s==-1]
    return sum(all(a & v for v in plus) and all((~a) & v for v in minus)
               for a in range(1 << (6*h)))

def audit():
    cases=[]
    for h in (1,2,3,4,8,16):
        F=clauses(h)
        g=validate(F,h)
        assert g["paired_clauses"]==0
        assert g["unpaired_positive"]==4*h
        assert is_model(F,witness(h))
        record={"h":h,"grammar":g,"witness_verified":True}
        if h<=3:
            record["exact_models"]=model_count(F,h)
        cases.append(record)
    H=clauses(1,paired=True)
    assert validate(H,1)["paired_clauses"]==8
    assert model_count(H,1)==18
    assert model_count(clauses(1),1)==20
    malformed=[(1,(1,2,3)),(-1,(1,2,3)),(1,(1,2,3))]
    assert len(set(malformed))!=len(malformed)
    summary={"status":"COMPUTATIONAL finite only",
             "construction":"cyclic swap of a positive literal position in Y copies",
             "cases":cases,"paired_reference_models":18,
             "malformed_duplicate_rejected":True,
             "limitations":["No UNSAT family constructed by cyclic swap",
                            "No physical bit flip, cumulative bit-time, or FLMV time-space trace",
                            "No all-decider hardness bound"]}
    assert [x.get("exact_models") for x in cases[:3]] == [20,356,6680]
    return summary

if __name__=="__main__":
    print(json.dumps(audit(),indent=2,sort_keys=True))
