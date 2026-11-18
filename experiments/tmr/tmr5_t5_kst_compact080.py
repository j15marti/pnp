#!/usr/bin/env python3
"""TMR-5/080 compact independent T5 endpoint and Kst mixed source checker.
This is smaller than the full locally executed 347372-check independent verifier."""
import itertools, json
def R(x,y): return (y-x)%5 in (1,3)
def H(s,t,neg):
    E={(a,b) for a in range(s) for b in range(s,s+t)}
    if neg:
        E.remove((0,s)); E.remove((1,s+1))
        E.add((0,1)); E.add((s,s+1))
    return sorted(E)
def D(s,t,neg):
    n=s+t;E=H(s,t,neg);arcs=[]
    for j,(u,v) in enumerate(E):
        a,b,c=n+3*j,n+3*j+1,n+3*j+2
        arcs+= [(u,a),(a,b),(b,c),(u,c),(c,v)]
    return n+3*len(E),arcs
def base_count(s,t,neg):
    E=H(s,t,neg);n=s+t;z=0
    for x in itertools.product(range(5),repeat=n):
        if all((x[u]-x[v])%5 in (1,4) for u,v in E):z+=1
    return z
checks=0
for u,v in itertools.product(range(5),repeat=2):
    good=[]
    for a,b,c in itertools.product(range(5),repeat=3):
        if all(R(x,y) for x,y in [(u,a),(a,b),(b,c),(u,c),(c,v)]):good.append((a,b,c))
        checks+=1
    want=[((u+1)%5,(u+2)%5,(u+3)%5)] if (v-u)%5 in (1,4) else []
    assert good==want
out=[]
for s,t in [(3,3),(3,4),(4,3)]:
    for neg in (False,True):
        n,A=D(s,t,neg)
        assert len(A)==5*s*t and n==s+t+3*s*t
        got=base_count(s,t,neg)
        want=0 if neg else 5*(2**s+2**t-2)
        assert got==want
        checks+=5**(s+t)
        out.append([s,t,int(neg),got,n,len(A)])
print(json.dumps({'revision':'TMR5_080_compact_v1','gadget_assignments':3125,'checks':checks,'sources':out,'failures':0},sort_keys=True))
