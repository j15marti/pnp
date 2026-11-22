#!/usr/bin/env python3
"""Residual closure audit, networkx==3.5; finite source tests, not TM timings."""
from collections import defaultdict, Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import networkx as nx


def recognize(rows):
    tables = {}
    for row in rows:
        if not row:
            return 'UNSAT', []
        scope = tuple(sorted(abs(x) for x in row))
        if len(scope)>3 or 0 in scope or len(set(scope))!=len(scope):
            return 'UNKNOWN', []
        forbidden = sum(int(next(z for z in row if abs(z)==x)<0)<<i
                        for i,x in enumerate(scope))
        tables[scope]=tables.get(scope,(1<<(1<<len(scope)))-1)&~(1<<forbidden)
    if any(table==0 for table in tables.values()):
        return 'UNSAT', []
    factors=[]
    occurrence=Counter()
    for scope, table in sorted(tables.items()):
        if table==0:
            return 'UNSAT', []
        b=next((b for b in range(len(scope)+1) if table==sum(
            1<<m for m in range(1<<len(scope)) if m.bit_count()==b)),None)
        if b is None:
            return 'UNKNOWN', []
        factors.append((scope,b))
        occurrence.update(scope)
    if any(d>2 for d in occurrence.values()):
        return 'UNKNOWN', []
    return 'ADMITTED', factors


def solve(rows):
    status, factors=recognize(rows)
    if status!='ADMITTED':
        return status,0
    occ=defaultdict(list)
    for v,(scope,b) in enumerate(factors):
        for x in scope:
            occ[x].append(v)
    q=len(factors)
    edges=[(vs[0],vs[1] if len(vs)==2 else q) for x,vs in sorted(occ.items())]
    D=sum(len(vs)==1 for vs in occ.values())
    degrees=[0]*(q+1)
    for u,v in edges:
        degrees[u]+=1
        degrees[v]+=1
    calls=0
    for t in range(D+1):
        b=[b for _,b in factors]+[t]
        H=nx.Graph()
        ports=[[] for _ in degrees]
        for e,(u,v) in enumerate(edges):
            a,z=2*e,2*e+1
            H.add_edge(a,z)
            ports[u].append(a)
            ports[v].append(z)
        fresh=2*len(edges)
        for v,degree in enumerate(degrees):
            assert 0<=b[v]<=degree
            for j in range(degree-b[v]):
                H.add_node(fresh)
                H.add_edges_from((fresh,p) for p in ports[v])
                fresh+=1
        calls+=1
        M=nx.max_weight_matching(H,maxcardinality=True)
        if 2*len(M)==len(H):
            return 'SAT',calls
    return 'UNSAT',calls


def restrict(rows,pins):
    out=[]
    for row in rows:
        if any(abs(z) in pins and pins[abs(z)]==int(z>0) for z in row):
            continue
        out.append(tuple(z for z in row if abs(z) not in pins))
    return out


def expand(factors):
    return [tuple(-x if bit else x for x,bit in zip(scope,bits))
            for scope,b in factors for bits in product((0,1),repeat=len(scope))
            if sum(bits)!=b]


def brute(rows):
    names=sorted({abs(z) for row in rows for z in row})
    for bits in product((0,1),repeat=len(names)):
        a=dict(zip(names,bits))
        if all(any(a[abs(z)]==int(z>0) for z in row) for row in rows):
            return 'SAT'
    return 'UNSAT'


def run():
    assert nx.__version__=='3.5'
    edges=list(combinations(range(4),2))
    scopes=[tuple(i+1 for i,e in enumerate(edges) if v in e) for v in range(4)]
    cases=[]
    totals=Counter()
    for demand in [(1,1,1,1),(2,2,2,2),(2,1,1,1)]:
        rows=expand(list(zip(scopes,demand)))
        for choices in product((-1,0,1),repeat=6):
            pins={i+1:x for i,x in enumerate(choices) if x>=0}
            residual=restrict(rows,pins)
            answer,calls=solve(residual)
            assert answer!='UNKNOWN'
            assert answer==brute(residual)
            totals[answer]+=1
            cases.append(dict(demands=demand,pins=choices,label=answer,matching_calls=calls))
    extra=[]
    controls=[('single_incidence',[((1,2),1),((2,3),1)]),
              ('forced_zero',[((1,2),0),((2,3),1)]),
              ('saturated',[((1,2),2),((2,3),1)]),
              ('scope_merge_sat',[((1,2),1),((1,2),1)]),
              ('scope_merge_unsat',[((1,2),1),((1,2),2)])]
    for name,fac in controls:
        rows=expand(fac)
        answer,calls=solve(rows)
        assert answer==brute(rows)
        extra.append(dict(name=name,label=answer,matching_calls=calls))
    # Exact witness that the old ternary-only syntactic class is not closed.
    restricted=restrict(expand(list(zip(scopes,(1,1,1,1)))),{1:0})
    assert any(len(row)==2 for row in restricted)
    assert solve(restricted)[0]=='SAT'
    assert solve([(1,2,3)])[0]=='UNKNOWN'
    return dict(target='DYNAMIC-RESIDUAL-FACTOR-CLOSURE1',
                recovery_revision='7962e8fd645db04d0168eb90c8a2449b13a1e073',
                networkx=nx.__version__,mode='exhaustive restrictions; no seed',
                cases=cases,case_count=len(cases),totals=dict(totals),controls=extra,
                old_admission_counterexample=restricted,
                sat_but_unknown=[1,2,3],
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                limitations='Finite source audit, no compiled images or TM timing; polynomial proof separate.')


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
