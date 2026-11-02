#!/usr/bin/env python3
"""Compact finite controls for MOVING-DECIDER-MINIMAX338. Standard library."""
from itertools import product
from collections import Counter
C=((),(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))
def parse(x):
    return int(x[1:],2) if len(x)==10 and x[0]=='1' and set(x)<={'0','1'} else None
def val(m,a):
    return all(not(m>>i&1) or any(((a>>(abs(z)-1))&1)==int(z>0) for z in cl)
               for i,cl in enumerate(C))
def label(x):
    m=parse(x)
    if m is None:return "MALFORMED"
    return "SAT" if any(val(m,a) for a in range(4)) else "UNSAT"
def run(x,policy):
    m=parse(x)
    if m is None:return ("MALFORMED",len(x)+1)
    t=len(x)
    order={"forward":(0,1,2,3),"reverse":(3,2,1,0),
           "units":(1,3,0,2)}.get(policy,(0,1,2,3))
    if policy=="empty":
        t+=1
        if m&1:return ("UNSAT",t)
    if policy=="units":
        t+=1
        if (m&2 and m&4) or (m&8 and m&16):return ("UNSAT",t)
    for a in order:
        t+=1
        if val(m,a):return ("SAT",t)
    return ("UNSAT",t)
policies=("forward","reverse","empty","units")
counts=Counter();worst={p:0 for p in policies};portfolio=0
for bits in product("01",repeat=10):
    x="".join(bits);target=label(x);counts[target]+=1;times=[]
    for p in policies:
        got,t=run(x,p);assert got==target,(x,p)
        worst[p]=max(worst[p],t);times.append(t)
    portfolio=max(portfolio,4*min(times))
assert counts==Counter(SAT=95,UNSAT=417,MALFORMED=512)
assert sum(2**j for j in range(11))==2047
assert portfolio==56
assert label("1000000000")=="SAT" # untrusted fast UNSAT would be wrong
print({"counts":dict(counts),"worst_costs":worst,"trusted_portfolio_bound":portfolio,
       "prefix_states":2047,"status":"FINITE CONTROL, not arbitrary-SAT hardness"})
