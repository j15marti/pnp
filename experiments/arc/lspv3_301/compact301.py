#!/usr/bin/env python3
"""GATE301 compact source/affine-matroid countercontrol (Python stdlib only).
This reproduces the connected M22 construction and dense coordinate-change
falsifier. Full acquired GF(2) solver and independent verifier are separately
archived. This is NOT an all-input polynomial SAT algorithm; P vs NP OPEN.
"""
from itertools import product
from collections import Counter, defaultdict
import json
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
P={2:0,3:1,5:0}

def make(r):
    f=[]; p={}
    for k in range(r):
        f.extend(tuple((1 if v>0 else -1)*(abs(v)+6*k) for v in c) for c in Y6)
        p.update({v+6*k:b for v,b in P.items()})
    for k in range(r-1):
        i,j=8*k+6,8*(k+1)+6
        a,b=list(f[i]),list(f[j])
        a[0],b[2]=b[2],a[0]
        f[i]=tuple(a); f[j]=tuple(b)
    return f,p

def verify(f,r):
    n=6*r
    assert len(f)==8*r and len({tuple(sorted(c)) for c in f})==len(f)
    assert all(len(set(map(abs,c)))==3 and
               (all(v>0 for v in c) or all(v<0 for v in c)) for c in f)
    q=Counter(v for c in f for v in c)
    assert all(q[v]==q[-v]==2 for v in range(1,n+1))
    edges=defaultdict(set)
    for c in f:
        for a in c:
            for b in c:edges[abs(a)].add(abs(b))
    seen={1}; todo=[1]
    while todo:
        for b in edges[todo.pop()]:
            if b not in seen:seen.add(b);todo.append(b)
    assert len(seen)==n

def solve(f,p):
    free=[v for v in range(1,max(abs(x) for c in f for x in c)+1) if v not in p]
    good=0
    for w in product((0,1),repeat=len(free)):
        a=dict(p); a.update(zip(free,w))
        good+=all(any(a[abs(x)]==int(x>0) for x in c) for c in f)
    return good

def matroid_component_dimensions(forms,clauses):
    # Independent basis followed by fundamental circuit and source-clause unions.
    piv={}; basis=[]
    for form in forms:
        x=form
        while x:
            k=x.bit_length()-1
            if k not in piv:
                piv[k]=x; basis.append(form); break
            x^=piv[k]
    b={}
    for j,v in enumerate(basis):
        x=v;label=1<<j
        while x:
            k=x.bit_length()-1
            if k not in b:
                b[k]=(x,label); break
            x^=b[k][0]; label^=b[k][1]
    def expression(v):
        result=0
        while v:
            x,y=b[v.bit_length()-1]
            v^=x; result^=y
        return result
    coeff=[expression(v) for v in forms]
    parent=list(range(len(basis)))
    def root(x):
        while x!=parent[x]: x=parent[x]
        return x
    def unite(x,y):
        a,c=root(x),root(y)
        if a!=c:parent[c]=a
    for v in coeff:
        ids=[i for i in range(len(parent)) if (v>>i)&1]
        for k in ids[1:]:unite(ids[0],k)
    for clause in clauses:
        ids=sorted(set(i for j in clause for i in range(len(parent))
                       if (coeff[j]>>i)&1))
        for k in ids[1:]:unite(ids[0],k)
    counts=Counter(root(i) for i in range(len(parent)))
    return sorted(counts.values())

def main():
    summary={}
    for r in [1,2,4,8,12]:
        f,p=make(r);verify(f,r)
        h=2*r;mask=(1<<h)-1
        natural=[1<<i for i in range(h)]
        # In even dimension, (I+J)^2=I, and z_i = XOR_{j != i} t_j.
        dense=[mask^(1<<i) for i in range(h)]
        clauses=[(2*k,2*k+1) for k in range(r)]
        c1=matroid_component_dimensions(natural,clauses)
        c2=matroid_component_dimensions(dense,clauses)
        assert c1==c2==[2]*r
        assert all((dense[a]|dense[b])==mask for a,b in clauses)
        if r<=4:assert solve(f,p)==3**r
        summary[str(r)]={'n':6*r,'cycles':r,'nullity':h,
                         'matroid_components':r,'component_dimensions':c1,
                         'source_models':3**r,'projection_candidates':2**h,
                         'nominal_cycle_branches':3**r,
                         'component_candidates':4*r,
                         'dense_raw_factor_scope':h}
    print(json.dumps({'gate':'GATE301','status':'RESTRICTED_EXACT',
                      'P_vs_NP':'OPEN','sources':summary},indent=2))

if __name__=='__main__':main()
