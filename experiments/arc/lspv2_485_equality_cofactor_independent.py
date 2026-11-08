#!/usr/bin/env python3
"""LSPV-2/485 independent Python exact strict 3-CNF cofactor control."""
import json
def source(k):
    c=[]
    for i in range(k):
        x,y,u,v=4*i+1,4*i+2,4*i+3,4*i+4
        c.extend([(-x,y,u),(-x,y,-u),(x,-y,v),(x,-y,-v)])
    return c
def sat(clauses,bits):
    return all(any((bits[abs(l)-1] if l>0 else 1-bits[abs(l)-1]) for l in c) for c in clauses)
def packed(k,x,y,u=0,v=0):
    b=[]
    for i in range(k): b.extend([(x>>i)&1,(y>>i)&1,(u>>i)&1,(v>>i)&1])
    return b
def main():
    assertions=0;rows=[]
    for k in range(1,7):
        F=source(k)
        assert len(F)==4*k and all(len(c)==3 and len({abs(z) for z in c})==3 for c in F)
        assertions+=2
        for x in range(1<<k):
            for y in range(1<<k):
                assert sat(F,packed(k,x,y))==(x==y)
                assertions+=1
            assert sat(F,packed(k,x,x));assertions+=1
        for a in range(1<<k):
            for b in range(1<<k):
                if a!=b:
                    assert sat(F,packed(k,a,a)) and not sat(F,packed(k,b,a));assertions+=1
        counted=0
        if k<=4:
            for x in range(1<<k):
                n=sum(sat(F,packed(k,x,y,u,v)) for y in range(1<<k) for u in range(1<<k) for v in range(1<<k))
                assert n==1<<(2*k);assertions+=1;counted+=1
        rows.append(dict(k=k,clauses=4*k,vars=4*k,cofactor_count=1<<k,projection_labels=1,models_per_cofactor=1<<(2*k),counted=counted))
    for bad in [(1,1,2),(0,2,3),(1,2),(),(1,-1,3)]:
        assert len(bad)!=3 or len({abs(z) for z in bad})!=3 or 0 in bad
        assertions+=1
    print(json.dumps(dict(status='PASS',assertions=assertions,rows=rows),indent=2))
if __name__=='__main__':main()
