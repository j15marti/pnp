#!/usr/bin/env python3
"""GATE303 restricted weak-backdoor size certificate on canonical source F_r.
Depends on previously published experiments/arc/lspv3_302/compact302.py.
Run: python experiments/arc/lspv3_303/compact303.py
"""
import importlib.util, json
from pathlib import Path

src = Path(__file__).resolve().parents[1] / "lspv3_302" / "compact302.py"
spec = importlib.util.spec_from_file_location("canonical302", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def one(r):
    edges,incidence,clauses=mod.source(r)
    n=len(edges)
    assert mod.grammar(n,clauses)
    witness=mod.recognize(n,clauses)
    assert witness is not None
    assert mod.hist(clauses,witness)==[0,len(clauses)//2,len(clauses)//2,0]
    assert mod.hist(clauses,set(range(1,n+1))-witness)==[0,len(clauses)//2,len(clauses)//2,0]
    cube=mod.cube(edges,incidence,clauses,r)
    bounds=[]
    for t in range(4):
        s=t+3
        q=r//s
        if q==0: continue
        patches=[]
        for a in range(q):
            for b in range(q):
                ports={4*(i*r+j)+p for i in range(a*s,(a+1)*s)
                        for j in range(b*s,(b+1)*s) for p in range(4)}
                variables={e for e,(u,v) in enumerate(edges,1) if u in ports and v in ports}
                assert len(variables)>=4*s*s+2*s*(s-1)
                patches.append((ports,variables))
        for e,(u,v) in enumerate(edges,1):
            assert sum(e in variables for ports,variables in patches)<=1
            assert sum(u in ports or v in ports for ports,variables in patches)<=2
        bounds.append({"target_tw":t,"grid_patches":q*q,
                       "weak_backdoor_size_min":(q*q+1)//2})
    return {"r":r,"variables":n,"clauses":len(clauses),
            "signed_vertex_max_degree":3,"signed_edge_max_degree":4,
            "source_SAT":True,"same_original_UNSAT_cube":cube,
            "bounds":bounds}

if __name__=="__main__":
    print(json.dumps([one(r) for r in (4,6,8,12,24)],indent=2))
