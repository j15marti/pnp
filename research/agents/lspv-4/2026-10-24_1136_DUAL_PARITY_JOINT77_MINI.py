#!/usr/bin/env python3
"""LSPV-4 DUAL-PARITY-JOINT77 minimal independent exact reproducer.
Run: python3 research/agents/lspv-4/2026-10-24_1136_DUAL_PARITY_JOINT77_MINI.py
Standard library only. Exhaustive for q<=2, not an asymptotic proof.
"""
from itertools import product
from collections import Counter
import json

def xor2(a,b,r):
    return ((-a,b),(a,-b)) if r==0 else ((a,b),(-a,-b))

def xor3(a,b,c):
    return tuple(tuple(-v if t else v for v,t in zip((a,b,c),bits))
                 for bits in product((0,1),repeat=3) if (sum(bits)%2)==1)

def make(q,e):
    assert q>=1 and len(e)==q
    n=2+2*q; C=[]; z=[3+2*j for j in range(q)]
    w=[4+2*j for j in range(q)]
    for j in range(q):
        C+=xor2(z[j],w[j],e[j])
        C += [(1,z[j]),(2,-z[j])]
    for head in (1,2):
        a=[head]+[u for pair in zip(z,w) for u in pair]
        p=[]
        for i in range(2*q-1):
            n+=1
            u,v=(a[0],a[1]) if i==0 else (p[-1],a[i+1])
            C+=xor3(u,v,n)
            p.append(n)
        C+=xor2(p[-1],a[-1],0)
    assert n==6*q and len(C)==20*q-4
    return n,tuple(C)

def evaluate(clauses,assignment):
    return all(any(assignment[abs(v)-1] == (v>0) for v in c)
               for c in clauses)

def check(q,e):
    n,C=make(q,e)
    count=sum(e)%2
    n2=sum(len(c)==2 for c in C)
    n3=sum(len(c)==3 for c in C)
    assert (n2,n3)==(4*q+4,16*q-8)
    supports={tuple(sorted(abs(v) for v in c)) for c in C if len(c)==3}
    assert len(supports)==4*q-2
    deg=Counter(v for s in supports for v in s)
    assert max(deg.values())<=2
    hitting=set(z for z in range(3,2*q+2))
    assert len(hitting)==2*q-1
    assert all(hitting.intersection(s) for s in supports)
    models=0
    for vals in product((False,True),repeat=n):
        models+=evaluate(C,vals)
    assert models==(2**q if count==1 else 0), (q,e,models)
    p=count
    assert {(x^p,y^p) for x,y in ((0,1),(1,0),(1,1))}==(
        {(0,0),(0,1),(1,0),(1,1)}-{(p,p)})
    return dict(q=q,e=''.join(map(str,e)),n=n,m=len(C),
                m2=n2,k=n3,h=2*q-1,models=models)

def run():
    rows=[check(q,e) for q in (1,2)
          for e in product((0,1),repeat=q)]
    image={(x^z,y^z,x^y^z) for x,y,z in product((0,1),repeat=3)
           if (x or y)}
    assert image==set(product((0,1),repeat=3))-{(0,0,0),(1,1,1)}
    assert all(len({(v[i],v[j]) for v in image})==4
               for i,j in ((0,1),(0,2),(1,2)))
    return {"status":"COMPUTATIONAL","failures":0,
            "cases":rows,"three_check_image":sorted(image)}

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
