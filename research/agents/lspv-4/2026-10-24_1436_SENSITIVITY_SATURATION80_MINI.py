#!/usr/bin/env python3
"""Independent, bounded exhaustive test for SENSITIVITY-SATURATION80."""
from itertools import product
import json

def models(n, clauses):
    return sum(all(any(x[abs(v)-1] == (v>0) for v in cl)
                   for cl in clauses)
               for x in product((False, True), repeat=n))

def source(q, b):
    c = [(1,q+2),(1,-(q+2)),(-(q+1),q+3),(-(q+1),-(q+3))]
    c.extend((-i, (i+1) if bit else -(i+1))
             for i,bit in enumerate(b,1))
    return q+3, c

def pad(n, clauses):
    out = []
    for i,(a,b) in enumerate(clauses,1):
        out.extend([(a,b,n+i),(a,b,-(n+i))])
    return n+len(clauses), out

def constants():
    u = [(1, 2, 4),(1, 2, -4),(1, -2, 4),(1, -2, -4),
         (-1, 2, 3),(-1, 2, -3),(-1, -2, 3),(-1, -2, -3)]
    s = [(1,2,3)] + u[1:]
    return u,s

def main():
    checks=0
    u,s = constants()
    assert len(u)==len(s)==len(set(u))==len(set(s))==8
    assert models(4,u)==0 and models(4,s)==1
    checks+=4
    for q in range(1,7):
        for b in product((0,1), repeat=q):
            n,clauses=source(q,b)
            assert (models(n,clauses)>0)==(b!=(1,)*q)
            checks+=1
            if q<=3:
                nn,cc=pad(n,clauses)
                assert models(nn,cc)==models(n,clauses)*2**len(clauses)
                checks+=1
        x=(1,)*q
        for omit in range(q):
            y=list(x); y[omit]=0
            assert all(x[i]==y[i] for i in range(q) if i!=omit)
            assert y!=(1,)*q
            checks+=2
    return {'run':'SENSITIVITY-SATURATION80-MINI','checks':checks,
            'failures':0,'max_q':6,
            'source_controls':sum(2**q for q in range(1,7))}

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
