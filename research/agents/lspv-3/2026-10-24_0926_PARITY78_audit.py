#!/usr/bin/env python3
"""PARITY-DIRECT-DECIDER78 independent proper-3CNF recognizer controls.
Python stdlib only, deterministic, no random seeds.
The small graph is the triangular prism (6 cubic vertices, 9 edges).
"""
from collections import defaultdict
from itertools import product
import json
from pathlib import Path

PRISM_EDGES = [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)]

def make_tseitin(num_vertices, edges, charges):
    inc=defaultdict(list)
    for i,(u,v) in enumerate(edges,1):
        assert u!=v
        inc[u].append(i); inc[v].append(i)
    assert len(charges)==num_vertices
    assert all(len(inc[v])==3 for v in range(num_vertices))
    clauses=[]
    for v in range(num_vertices):
        triple=sorted(inc[v])
        for bits in product(range(2),repeat=3):
            if (sum(bits)%2)!=charges[v]:
                clauses.append(tuple(-x if b else x for x,b in zip(triple,bits)))
    return clauses

def recognize(clauses):
    """Either None or (SAT label, charge vector, component sizes). Exact if accepted."""
    if not clauses or any(len(c)!=3 or len(set(abs(x) for x in c))!=3 for c in clauses):
        return None
    groups=defaultdict(list)
    for c in clauses:
        groups[tuple(sorted(abs(x) for x in c))].append(c)
    vertex_keys=sorted(groups)
    charges=[]; incid=defaultdict(list)
    for vi,key in enumerate(vertex_keys):
        C=groups[key]
        if len(C)!=4:
            return None
        patterns=set()
        for clause in C:
            signed={abs(l):(l<0) for l in clause}
            patterns.add(tuple(int(signed[e]) for e in key))
        if len(patterns)!=4 or len({sum(a)%2 for a in patterns})!=1:
            return None
        charge=1-(sum(next(iter(patterns)))%2)
        charges.append(charge)
        for e in key: incid[e].append(vi)
    if any(len(v)!=2 for v in incid.values()):
        return None
    parent=list(range(len(vertex_keys)))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]; a=parent[a]
        return a
    for u,v in incid.values():
        ru,rv=find(u),find(v)
        if ru!=rv: parent[ru]=rv
    xor=defaultdict(int); component_n=defaultdict(int)
    for vi,c in enumerate(charges):
        root=find(vi)
        xor[root]^=c
        component_n[root]+=1
    return (all(x==0 for x in xor.values()), tuple(charges), tuple(sorted(component_n.values())))

def count_sat(clauses, num_edge_vars):
    # Enumerate all Boolean edge assignments, wholly independent of recognizer.
    cnt=0
    for bits in product(range(2),repeat=num_edge_vars):
        for C in clauses:
            if not any((bits[abs(l)-1]==(1 if l>0 else 0)) for l in C):
                break
        else:
            cnt+=1
    return cnt

def test():
    stats={'graph':'triangular_prism','vertices':6,'edge_variables':9,'clauses_per_formula':24,
           'all_charge_vectors':64,'sat_inputs':0,'unsat_inputs':0,'classification_checks':0,
           'witnesses_total':0,'mutant_rejections':0,'disconnected_checks':0}
    base=None
    for charges in product(range(2),repeat=6):
        clauses=make_tseitin(6,PRISM_EDGES,charges)
        label=(sum(charges)%2==0)
        rec=recognize(clauses)
        assert rec is not None and rec[0]==label and rec[2]==(6,)
        count=count_sat(clauses,9)
        assert count==(16 if label else 0)
        stats['sat_inputs' if label else 'unsat_inputs']+=1
        stats['classification_checks']+=1
        stats['witnesses_total']+=count
        if charges==(1,0,0,0,0,0): base=clauses
    assert base is not None
    for i in range(len(base)):
        for j in range(3):
            mod=list(base)
            tmp=list(mod[i]); tmp[j]=-tmp[j]; mod[i]=tuple(tmp)
            assert recognize(mod) is None
            stats['mutant_rejections']+=1
    # Disconnected two prisms, each odd charge, but globally even total charge.
    edges2=PRISM_EDGES+[(u+6,v+6) for u,v in PRISM_EDGES]
    clauses2=make_tseitin(12,edges2,(1,0,0,0,0,0,1,0,0,0,0,0))
    rec=recognize(clauses2)
    assert rec is not None and not rec[0] and rec[2]==(6,6)
    stats['disconnected_checks']+=1
    clauses3=make_tseitin(12,edges2,(0,0,0,0,0,0,0,0,0,0,0,0))
    rec=recognize(clauses3)
    assert rec is not None and rec[0] and rec[2]==(6,6)
    stats['disconnected_checks']+=1
    stats['total_assertion_categories']=stats['classification_checks']+stats['mutant_rejections']+stats['disconnected_checks']
    return stats
if __name__=='__main__':
    s=test()
    out=Path(__file__).with_name('PARITY78_raw.json')
    out.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    print(json.dumps(s,sort_keys=True))
