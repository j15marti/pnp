#!/usr/bin/env python3
"""DOMAIN-COLLAPSE55 minimal exact source-coherence hostile control.
Run: python repro_minimal.py. Python stdlib only.
Fixed-order signed CNF, exhaustive full model check at t=2.
"""
from itertools import product

def formula(t, defect):
    V=2*t
    x=lambda v,c:3*v+c+1
    p=lambda v:3*V+v+1
    clauses=[]
    for v in range(V):
        a,b,c=x(v,0),x(v,1),x(v,2)
        clauses.extend(((a,b,c),(-a,-b),(-a,-c),(-b,-c),(-c,p(v)),(-c,-p(v))))
    for u in range(t):
        for v in range(t,2*t):
            if defect and u==0 and v==t:
                clauses.extend(((-x(u,0),-x(v,1)),(-x(u,1),-x(v,0))))
            else:
                clauses.extend(((-x(u,0),-x(v,0)),(-x(u,1),-x(v,1))))
    assert len(clauses)==12*t+2*t*t
    return clauses

def extract(t,clauses):
    """Read ALL signed source clauses, reject malformed grammar."""
    V=2*t
    x=lambda v,c:3*v+c+1
    p=lambda v:3*V+v+1
    pos=0
    for v in range(V):
        a,b,c=x(v,0),x(v,1),x(v,2)
        spec=[(a,b,c),(-a,-b),(-a,-c),(-b,-c),(-c,p(v)),(-c,-p(v))]
        for expected in spec:
            if tuple(clauses[pos])!=expected:return None
            pos+=1
    edges=[]
    for u in range(t):
        for v in range(t,2*t):
            current=[tuple(clauses[pos]),tuple(clauses[pos+1])];pos+=2
            neq=[(-x(u,0),-x(v,0)),(-x(u,1),-x(v,1))]
            eq=[(-x(u,0),-x(v,1)),(-x(u,1),-x(v,0))]
            if current==neq:bit=1
            elif current==eq:bit=0
            else:return None
            edges.append((u,v,bit))
    return edges if pos==len(clauses) else None

def dsu_decide(V,edges):
    parent=list(range(V));rel=[0]*V
    def find(v):
        if v==parent[v]:return v,0
        root,parity=find(parent[v]);rel[v]^=parity;parent[v]=root
        return root,rel[v]
    for u,v,bit in edges:
        ru,pu=find(u);rv,pv=find(v)
        if ru==rv:
            if (pu^pv)!=bit:return False
        else:parent[rv]=ru;rel[rv]=pu^pv^bit
    return True

def evaluate(clauses,assignment):
    return all(any((assignment[abs(l)-1] if l>0 else not assignment[abs(l)-1]) for l in C) for C in clauses)

def main():
    checks=0
    for t in (2,3,4,5,8,16,32,64):
        for defect in (False,True):
            F=formula(t,defect)
            relations=extract(t,F)
            assert relations is not None
            assert dsu_decide(2*t,relations)==(not defect)
            checks+=1
            if t==2:
                count=sum(evaluate(F,a) for a in product((False,True),repeat=8*t))
                assert count==(32 if not defect else 0)
                checks+=1
            malformed=F.copy();malformed[0]=(-F[0][0],)+F[0][1:]
            assert extract(t,malformed) is None
            checks+=1
    print('DOMAIN-COLLAPSE55 minimal source audit:',checks,'checks passed')

if __name__=='__main__':main()
