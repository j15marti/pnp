#!/usr/bin/env python3
"""Signed renaming and clause reorder controls for one-pivot DP/reentry and factored DAG."""
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_linear22_projection_firewall import formula,factored_projection
from arc_linear22_dp_reentry import dp,convert_resolvents,local_equiv_for_pivot
from arc_mixed_projection_test import Store,bitcnf

def run(seed):
    k=7;n,cs=formula(k)
    rng=random.Random(seed)
    perm=list(range(1,n+1));rng.shuffle(perm)
    flips={i:rng.choice((-1,1)) for i in range(1,n+1)}
    transformed=[]
    for c in cs:
        d=[(1 if z>0 else -1)*flips[abs(z)]*perm[abs(z)-1] for z in c]
        rng.shuffle(d);transformed.append(tuple(d))
    rng.shuffle(transformed)
    assert len(transformed)==4*k
    store=Store();root=store.from_cnf(transformed);sz=store.nodesizes(root)
    assert sz['gates']==4*k+1 and sz['lits']==2*n
    rankchecks=0
    for x in range(n):
        f=factored_projection(store,transformed,x)
        z=store.nodesizes(f)
        assert z['gates']==sz['gates']+3
        assert z['lits']==sz['lits']-2
        assert z['edges']==sz['edges']-1
        assert z['bits']==sz['bits']+8
        c,r=dp(transformed,x+1)
        out,to=convert_resolvents(c,r,n,x+1)
        assert len(out)==len(transformed)+4
        assert len(out[0])==3
        assert bitcnf(out,n+3)>bitcnf(transformed,n)
        rankchecks+=local_equiv_for_pivot(transformed,x+1)
    return {'seed':seed,'pivot_checks':n,'local_assignments':rankchecks,'dag_delta_bits':8}

if __name__=='__main__':
    out=[run(20261030+i) for i in range(6)]
    print(json.dumps(out,indent=2))
    with open(str(Path(__file__).resolve().parent / 'arc_linear22_signed_relabel_results.json'),'w') as f:json.dump(out,f,indent=2)
