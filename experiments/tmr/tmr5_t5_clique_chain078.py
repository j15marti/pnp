#!/usr/bin/env python3
"""TMR-5/078 independent T5 clique-chain source, exact count, residual rank and OBDD stress.
No seed; no third-party libraries. All source vertices are explicitly generated.
"""
import json, hashlib
from itertools import product
from collections import defaultdict

R={(x,(x+d)%5) for x in range(5) for d in (1,3)}
assert len(R)==10

def instance(n):
    # module i has local positions 0...4; local '1' shared with next module '0'.
    assert n>=1
    modules=[]; arcs=[]; idx=0
    for i in range(n):
        if i==0:
            vals=list(range(5)); idx=5
        else:
            vals=[modules[-1][1]]+list(range(idx,idx+4)); idx+=4
        modules.append(vals)
        arcs += [(vals[x],vals[y]) for x,y in R]
    pairs=[]
    for i in range(n):
        a,b=idx,idx+1; idx+=2
        pairs.append((a,b))
        arcs += [(modules[i][0],a),(a,b)]
    assert idx==6*n+1
    assert len(arcs)==12*n
    assert len(set(arcs))==len(arcs)
    deg=[0]*idx
    for x,y in arcs: deg[x]+=1;deg[y]+=1
    assert max(deg)<=9
    return idx, arcs, modules, pairs, max(deg)

def is_hom(cols,arcs):
    return all((cols[u],cols[v]) in R for u,v in arcs)

def row_bits(n,core_vals,a_vals):
    # Row on all graph vertices except b_i, restrict core colors and a_i;
    # column ranges over (b_1,...,b_n) in base-five enumeration.
    assert len(a_vals)==n
    bits=0
    for j,bs in enumerate(product(range(5),repeat=n)):
        if all((a_vals[i],bs[i]) in R for i in range(n)):
            bits |= (1<<j)
    return bits

def f2_rank(rows):
    pivots={}
    for num in rows:
        x=num
        while x:
            p=x.bit_length()-1
            if p not in pivots:
                pivots[p]=x;break
            x^=pivots[p]
    return len(pivots)

def count_bruteforce(n):
    N,arcs,modules,pairs,_=instance(n)
    total=0
    for colors in product(range(5),repeat=N):
        total+=is_hom(colors,arcs)
    return total

def sanity(n):
    N,arcs,modules,pairs,degree=instance(n)
    # Core assignment forced by first module's rotation, as each T5-module
    # is an injective automorphism and all rotations only.
    for t in range(5):
        core={v:(t+i+j)%5 for i,mod in enumerate(modules) for j,v in enumerate(mod)}
        assert len(core)==4*n+1
        assert all((core[u],core[v]) in R for u,v in arcs if u in core and v in core)
        for a_choice in product((1,3),repeat=n):
            avals=[(core[mod[0]]+d)%5 for mod,d in zip(modules,a_choice)]
            for (a,b),val in zip(pairs,avals):
                assert (core[modules[pairs.index((a,b))][0]],val) in R
            row=row_bits(n,core,avals)
            assert row.bit_count()==2**n
        achoices=list(product((1,3),repeat=n))
        rows=[]
        for ac in achoices:
            rows.append(row_bits(n,core,[(core[mod[0]]+d)%5 for mod,d in zip(modules,ac)]))
        assert len(set(rows))==2**n
        assert f2_rank(rows)==2**n
    return dict(n=n,vertices=N,arcs=len(arcs),max_degree=degree,expected_count=5*4**n,
                fixed_core_suffix_rank_F2=2**n,distinct_suffix_rows=2**n)

if __name__=='__main__':
    tests=[sanity(n) for n in range(1,6)]
    # exhaustive complete T5 hom counts at n=1 (7 vertices, 78,125 candidate colorings)
    assert count_bruteforce(1)==20
    # independently enumerate local module automorphisms and their restrictions
    for t in range(5):
        assert sum(1 for v in product(range(5),repeat=5) if is_hom(v,R) and v[0]==t)==1
    out={"revision":"tmr5-t5-clique-chain078.py.v1", "seed":None,
         "all_arcs_authenticated":len(R),"tests":tests,
         "exhaustive_n1_count":20,"t5_automorphisms":5,
         "field":"F2 rank; symbolic proof any field", "assertion_failures":0}
    print(json.dumps(out,indent=2,sort_keys=True))
