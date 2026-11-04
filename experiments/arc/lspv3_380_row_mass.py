#!/usr/bin/env python3
"""LSPV-3/380: exhaustive minimum h-1-XOR-tree expanded-row width.

This is a finite restricted subsystem diagnostic, not a general SAT lower bound.
Run: python3 experiments/arc/lspv3_380_row_mass.py
"""
import functools
import itertools
import json

def graph(name):
    if name == "K4":
        return 4, [(i,j) for i in range(4) for j in range(i+1,4)]
    if name == "K33":
        return 6, [(i,j) for i in range(3) for j in range(3,6)]
    if name == "CUBE":
        return 8, [(i,i^(1<<k)) for i in range(8) for k in range(3) if i<(i^(1<<k))]
    if name == "PENTAGON_PRISM":
        return 10, [(i,(i+1)%5) for i in range(5)] + [(i+5,(i+1)%5+5) for i in range(5)] + [(i,i+5) for i in range(5)]
    raise ValueError(name)

def run(name):
    h,edges=graph(name)
    assert len(edges)*2==3*h
    assert all(sum(v in e for e in edges)==3 for v in range(h))
    full=(1<<h)-1
    cuts=[sum(((s>>u)^(s>>v))&1 for u,v in edges) for s in range(1<<h)]
    @functools.lru_cache(None)
    def dp(s):
        if s.bit_count()==1: return 0,None
        best=(10**10,None)
        first=s&(-s)
        a=(s-1)&s
        while a:
            if a&first:
                v=dp(a)[0]+dp(s^a)[0]+cuts[s]
                if v<best[0]: best=(v,(a,s^a))
            a=(a-1)&s
        return best
    proof=[]
    def build(s):
        if s.bit_count()==1:
            v=s.bit_length()-1
            mask=sum(1<<j for j,e in enumerate(edges) if v in e)
            return "s"+str(v),mask,int(v==0)
        a,b=dp(s)[1]; x,m,p=build(a); y,n,q=build(b)
        z="d"+str(len(proof))
        mask=m^n; rhs=p^q
        assert mask.bit_count()==cuts[s]
        proof.append(dict(id=z,parents=[x,y],support=s,mask=mask,rhs=rhs,width=mask.bit_count()))
        return z,mask,rhs
    _,mask,rhs=build(full)
    assert (mask,rhs)==(0,1) and len(proof)==h-1
    assert sum(x["width"] for x in proof)==dp(full)[0]
    # Matched source-local 4-clause parity constraints.
    counts=[]
    for charge in (1,0):
        models=0
        for bits in range(1<<len(edges)):
            if all((sum((bits>>j)&1 for j,e in enumerate(edges) if v in e)&1)==int(charge==1 and v==0) for v in range(h)):
                models+=1
        counts.append(models)
    assert counts==[0,1<<(len(edges)-h+1)]
    return dict(graph=name,h=h,edges=edges,xor_nodes=h-1,
        exact_min_aggregate_width=dp(full)[0],odd_models=counts[0],
        even_models=counts[1],proof=proof)
def main():
    cases=[run(name) for name in ("K4","K33","CUBE","PENTAGON_PRISM")]
    print(json.dumps(dict(id="LSPV3-380",model="min h-1 binary XOR gates from authentic vertex parity rows",seed=None,cases=cases,
        limits="Not a full mixed-R optimum, not a machine-time lower bound."),indent=2,sort_keys=True))
if __name__=="__main__": main()
