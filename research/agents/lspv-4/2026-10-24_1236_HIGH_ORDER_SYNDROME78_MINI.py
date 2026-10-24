#!/usr/bin/env python3
"""LSPV-4 HIGH-ORDER-SYNDROME78: dependency-free independent mini auditor.
Use: python 2026-10-24_1236_HIGH_ORDER_SYNDROME78_MINI.py
"""
import itertools, json

def parity(a): return sum(a)%2

def xor3(a,b,c):
    out=[]
    for bits in itertools.product((0,1), repeat=3):
        if parity(bits):
            out.append(tuple(-v if bit else v for v,bit in zip((a,b,c),bits)))
    return out

def cnf(t,b):
    assert t>=3 and len(b)==t
    n=2*t
    rows=[(1,2)]
    for j in range(3,t+1):
        rows.extend(((-j,t+j),(j,-t-j)))
    p=3
    for j in range(4,t+1):
        n+=1
        rows.extend(xor3(p,j,n))
        p=n
    rows.extend(xor3(1,p,t+1))
    rows.extend(xor3(2,p,t+2))
    n+=1
    for j,z in enumerate(b,1):
        literal=t+j if z else -(t+j)
        rows.extend(((literal,n),(literal,-n)))
    assert n==3*t-2
    assert len(rows)==8*t-7
    return n,tuple(rows)

def inverse(b):
    p=parity(b[2:])
    return (b[0]^p,b[1]^p,*b[2:])

def image(b):
    x=inverse(b)
    return bool(x[0] or x[1])

def truth(c,a):
    return all(any(a[abs(l)-1] == (1 if l>0 else 0) for l in clause) for clause in c)

def models(n,rows):
    return sum(truth(rows,assignment)
               for assignment in itertools.product((0,1),repeat=n))

def run():
    groups=[];checks=0
    for t in range(3,9):
        universe=list(itertools.product((0,1),repeat=t))
        feasible={b for b in universe if image(b)}
        assert len(feasible)==3*2**(t-2)
        assert (0,)*t not in feasible
        checks+=2
        for omit in range(t):
            proj={tuple(b[j] for j in range(t) if j!=omit) for b in feasible}
            assert len(proj)==2**(t-1)
            checks+=1
        for j in range(t):
            b=tuple(int(i==j) for i in range(t))
            assert image(b)
            checks+=1
        for b in universe:
            n,c=cnf(t,b)
            assert len(c)==8*t-7
            assert all(len(row) in (2,3) for row in c)
            assert sum(len(row)==3 for row in c)==4*(t-1)
            checks+=3
            if t<=4:
                assert models(n,c)==(2 if image(b) else 0)
                checks+=1
        groups.append(dict(t=t,feasible=len(feasible),
                           total=2**t,all_proper_projections_full=True,
                           n=3*t-2,m=8*t-7))
    return dict(status="COMPUTATIONAL",checks=checks,failures=0,groups=groups)

if __name__=="__main__":
    print(json.dumps(run(),indent=2))
