#!/usr/bin/env python3
"""ARC230 exact signed-clause-to-rank-one-leaf fiber test; dependency-free."""
from itertools import product
import json
def lit(l,x): return x[abs(l)-1] == (l>0)
def source(clauses,x): return all(any(lit(l,x) for l in c) for c in clauses)
def leaf(c,x):
    for a,b,d in product((0,1),repeat=3):
        if (a^b^d)==1 and all(not q or lit(l,x) for q,l in zip((a,b,d),c)):return True
    return False
def build(n,clauses):
    bag0=set(range(1,n+1))
    leaves=[]
    for j,c in enumerate(clauses):
        assert len(c)==3 and len({abs(l) for l in c})==3
        sel=tuple(n+3*j+i+1 for i in range(3))
        leaves.append(dict(source=j,bag=set(map(abs,c))|set(sel),binary=[(-sel[i],c[i]) for i in range(3)],xor=sel))
        assert len(bag0 & leaves[-1]['bag'])==3
    return leaves
clauses=[tuple(s[i]*(i+1) for i in range(3)) for s in product((-1,1),repeat=3)]
count=dict(single=0,formulas=0,fibers=0,sat=0,unsat=0)
for c in clauses:
    for x in product((0,1),repeat=3):
        assert source([c],x)==leaf(c,x);count['single']+=1
for mask in range(256):
    sourceclauses=[c for i,c in enumerate(clauses) if mask>>i&1]
    assert len(build(3,sourceclauses))==len(sourceclauses)
    vals=[]
    for x in product((0,1),repeat=3):
        lhs=source(sourceclauses,x)
        assert lhs==all(leaf(c,x) for c in sourceclauses)
        vals.append(lhs);count['fibers']+=1
    count['formulas']+=1
    if any(vals):count['sat']+=1
    else:count['unsat']+=1
assert count=={'single':64,'formulas':256,'fibers':2048,'sat':255,'unsat':1}
print(json.dumps(count,sort_keys=True))
