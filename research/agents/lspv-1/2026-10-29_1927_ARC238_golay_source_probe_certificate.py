#!/usr/bin/env python3
"""ARC238: independent finite syndrome certificate, standard library only.
Scope: reusable 23-bit unary-source parity-SAT contexts, not general SAT.
Run: python 2026-10-29_1927_ARC238_golay_source_probe_certificate.py
"""
import itertools, json, random
def par(x): return x.bit_count() & 1
n=23
g=sum(1<<i for i in (0,1,5,6,7,9,11))
G=[g<<i for i in range(12)]
def rref(rows):
    rows=list(rows); piv=[]; k=0
    for i in range(n):
        j=next((j for j in range(k,len(rows)) if rows[j]&(1<<i)),None)
        if j is None: continue
        rows[k],rows[j]=rows[j],rows[k]
        for t in range(len(rows)):
            if t!=k and rows[t]&(1<<i): rows[t]^=rows[k]
        piv.append(i); k+=1
    return rows[:k],piv
B,P=rref(G)
assert len(P)==12
H=[]
for j in range(n):
    if j in P: continue
    x=1<<j
    for row,i in zip(B,P):
        if par(row&x): x^=1<<i
    assert all(par(x&c)==0 for c in G)
    H.append(x)
assert len(H)==11
def syn(x): return sum(par(x&h)<<i for i,h in enumerate(H))
errors=[0]+[sum(1<<i for i in I)
            for k in (1,2,3) for I in itertools.combinations(range(n),k)]
table={syn(e):e for e in errors}
assert len(errors)==len(table)==2048
piv={}
for i,c in enumerate(G):
    m=1<<i
    while c:
        j=c.bit_length()-1
        if j not in piv:
            piv[j]=(c,m)
            break
        v,a=piv[j]
        c^=v; m^=a
    assert c
def coords(c):
    m=0
    while c:
        v,a=piv[c.bit_length()-1]
        c^=v;m^=a
    return m
rng=random.Random(20261029)
for _ in range(5000):
    a=rng.getrandbits(n)
    w=rng.getrandbits(n)
    s=sum(par(a&c)<<i for i,c in enumerate(G))
    e=table[syn(w)]
    c=w^e
    assert syn(c)==0 and e.bit_count()<=3
    assert (par(s&coords(c))^par(e&a))==par(w&a)
print(json.dumps({"status":"COMPUTATIONAL","seed":20261029,"b":23,
   "L":12,"Q":3,"generator_polynomial":"0xae3",
   "distinct_syndromes":len(table),"error_patterns":len(errors),
   "randomized_query_checks":5000,
   "sphere_cover_exact":(1<<12)*2048==(1<<23)}))
