#!/usr/bin/env python3
"""Independent 25-state pair transfer audit for TMR-3/079.
Place in same directory as tmr3_t5_adhesion_two079.py before running.
"""
from itertools import combinations, product
from pathlib import Path
import importlib.util, json, time
base=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("solver",base/"tmr3_t5_adhesion_two079.py")
x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)
states=list(product(range(5),repeat=2))
M=[]
for a,b in states:
    row=[]
    for c,d in states:
        values=(a,b,c,d)
        weight=1
        for indices in combinations(range(4),3):
            weight*=x.w3(*(values[i] for i in indices))
        row.append(weight)
    M.append(row)
def transfer(r):
    values=[1]*25
    for _ in range(r):
        values=[sum(M[i][j]*values[i] for i in range(25)) for j in range(25)]
    return sum(values)
results={}
for r in (1,2,3,5,10,25,50,120):
    n,arcs=x.chain(r)
    t=time.perf_counter()
    result,stats=x.solve(n,arcs,budget=3)
    elapsed=time.perf_counter()-t
    assert result==transfer(r)
    results[str(r)]={"vertices":n,"arcs":len(arcs),"count":str(result),
                     "digits":len(str(result)),"splits":stats["splits"],
                     "max_interface":stats["max_interface"],
                     "max_cover":stats["max_cover"],"local_seconds":round(elapsed,4)}
factors=x.factors_for(list(combinations(range(4),3)))
U=(0,1)
cover=x.cover_search(set(range(4)),factors,U,3)
matrix=x.evaluate_base(set(range(4)),factors,U,cover)
results["boundary_message_rows"]=[matrix[5*i:5*i+5] for i in range(5)]
results["nonrankone_minor"]=matrix[0]*matrix[6]-matrix[1]*matrix[5]
assert results["nonrankone_minor"]==676
try:
    import networkx as nx
    result=[]
    for r in (2,3,6,10):
        n,arcs=x.chain(r)
        hubs,triples=x.incidence(n,x.normalize(n,arcs))
        G=nx.Graph();G.add_nodes_from(hubs)
        for e in triples:G.add_edges_from(combinations(e,2))
        result.append([r,len(list(nx.articulation_points(G)))])
    results["articulations"]=result
    assert all(a==0 for _,a in result)
except ImportError:
    results["articulations"]="NetworkX not installed, optional check skipped"
print(json.dumps(results,sort_keys=True,indent=2))
