#!/usr/bin/env python3
"""Exactly project any chosen set of 1/2 variables by factoring untouched clauses.
Finite controls; no unrestricted complexity claim.
"""
from pathlib import Path
import json,itertools,sys,random
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_mixed_projection_test import Store,source_sat,bitcnf
from arc_linear22_projection_firewall import formula

def project(st,clauses, variables):
    cutset=set(v+1 for v in variables)
    common=[];touch=[]
    for c in clauses:
        if any(abs(x) in cutset for x in c):touch.append(c)
        else:common.append(c)
    H=st.from_cnf(common)
    arms=[]
    for vals in itertools.product((0,1),repeat=len(variables)):
        assign=dict(zip((v+1 for v in variables),vals))
        residual=[]
        for c in touch:
            known=[z for z in c if abs(z) in assign]
            if any(int(z>0)==assign[abs(z)] for z in known):continue
            residual.append(tuple(z for z in c if abs(z) not in assign))
        arms.append(st.from_cnf(residual))
    return st.gate('and',[H,st.gate('or',arms)])

def run(k):
    n,clauses=formula(k)
    st=Store();root=st.from_cnf(clauses)
    old=st.nodesizes(root)
    rows=[]
    for x,y in itertools.combinations(range(n),2):
        before=st.calls
        q=project(st,clauses,(x,y))
        z=st.nodesizes(q)
        rows.append(dict(x=x,y=y,delta=z['bits']-old['bits'],
           circuit_bits=z['bits'],gates=z['gates'],search_calls=st.calls-before))
    rng=random.Random(410+k)
    for row in rows[::max(1,len(rows)//80)]:
        q=project(st,clauses,(row['x'],row['y']))
        for _ in range(30):
            a=[rng.randrange(2) for _ in range(n)]
            vals=[]
            for b1,b2 in itertools.product([0,1],repeat=2):
                a[row['x']]=b1;a[row['y']]=b2
                vals.append(source_sat(clauses,a))
            assert st.evaluate(q,a)==any(vals)
    rows.sort(key=lambda z:z['delta'])
    return dict(k=k,n=n,pairs=len(rows),best=rows[:3],worst=rows[-1],
        shrinking=sum(x['delta']<0 for x in rows),not_shrinking=sum(x['delta']>=0 for x in rows),
        total_gate_call_proxy=sum(x['search_calls'] for x in rows),sampled_semantic_checks=30*len(rows[::max(1,len(rows)//80)]))

if __name__=='__main__':
    res=[run(7),run(9),run(11)]
    print(json.dumps(res,indent=2))
    with open(str(Path(__file__).resolve().parent / 'arc_two_pivot_lookahead_results.json'),'w') as f:json.dump(res,f,indent=2)
