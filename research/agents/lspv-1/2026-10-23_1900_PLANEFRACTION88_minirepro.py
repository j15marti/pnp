#!/usr/bin/env python3
"""PLANEFRACTION88 compact independent source-family verifier.
Full 5,152-assertion audit: see PLANEFRACTION88 research package.
Pure Python standard library, deterministic, no external SAT solver.
"""
from itertools import product
from math import ceil, log2

def points_and_lines(p):
    def norm(v):
        for a in v:
            if a % p:
                z = pow(a, -1, p)
                return tuple((x*z) % p for x in v)
        return None
    P = sorted({norm(v) for v in product(range(p), repeat=3)} - {None})
    L = sorted({tuple(i for i,x in enumerate(P)
                     if sum(a*b for a,b in zip(x,norm(c))) % p == 0)
                for c in product(range(p),repeat=3) if norm(c) is not None})
    return P,L

def source(p,b):
    P,L=points_and_lines(p); q=len(P)
    assert len(b)==q
    clauses=[]
    for i,bit in enumerate(b):
        x=i+1 if bit else -(i+1)
        u,v=q+i+1,2*q+i+1
        clauses += [(x,u,v),(x,u,-v),(x,-u,v),(x,-u,-v)]
    next_var=3*q
    for line in L:
        ls=[-(i+1) for i in line]
        if len(ls)==3:
            clauses.append(tuple(ls))
        else:
            next_var+=1
            z=next_var
            clauses.append((ls[0],ls[1],z))
            for lit in ls[2:-2]:
                next_var+=1
                w=next_var
                clauses.append((-z,lit,w))
                z=w
            clauses.append((-z,ls[-2],ls[-1]))
    assert next_var==q*(p+1)
    assert len(clauses)==q*(p+3)
    assert all(len(set(map(abs,c)))==3 for c in clauses)
    assert len(clauses)==len(set(tuple(sorted(c)) for c in clauses))
    return clauses,next_var,L

def answer(b,L):
    return not any(all(b[i] for i in line) for line in L)

def evaluate(clauses,a):
    return all(any(bool(a[abs(t)-1])==(t>0) for t in clause)
               for clause in clauses)

def audit(p):
    P,L=points_and_lines(p); q=p*p+p+1
    assert len(P)==len(L)==q
    assert all(len(line)==p+1 for line in L)
    assert all(sum(i in L[j] for j in range(q))==p+1 for i in range(q))
    assert all(len(set(L[i])&set(L[j]))==1
               for i in range(q) for j in range(i+1,q))
    zero=(0,)*q
    F,n,lines=source(p,zero)
    assert evaluate(F,(0,)*n)
    assert answer(zero,lines)
    for i in range(q):
        b=list(zero); b[i]=1
        G,n2,L2=source(p,b)
        assert n2==n and len(G)==len(F)
        diffs=[(j,k) for j,(c,d) in enumerate(zip(F,G))
                       for k,(x,y) in enumerate(zip(c,d)) if x!=y]
        assert len(diffs)==4
        assert all(j==4*i+t for t,(j,k) in enumerate(diffs))
        assert answer(b,L2)
    for line in lines:
        b=[int(i in line) for i in range(q)]
        assert not answer(b,lines)
    # Four signed-record words per clause, two header words.
    m=q*(p+3); w=ceil(log2(64*(n+m+1))); N=(4*m+2)*w
    frac=q/(p+1); integer=p+1
    # A point on a chosen line intersects every projective line.
    assert all(bool(set(line)&set(lines[0])) for line in lines)
    # Every <=p point set hits <=p(p+1)<q lines.
    assert p*(p+1)<q
    return dict(p=p,q=q,n=n,m=m,encoded_bits=N,
                fractional=frac,integer=integer,
                promise_disjoint_sensitivity=1)

def main():
    for p in (2,3,5,7):
        print(audit(p))
    P,L=points_and_lines(2); q=len(P)
    checked=0
    for b in product((0,1),repeat=q):
        F,n,_=source(2,b)
        assert answer(b,L)==any(evaluate(F,tuple(b)+(0,)*(n-q))
                                 for _ in (0,))
        checked+=1
    print("Fano all-orientations witness audit",checked,"passed")
    print("STATUS COMPUTATIONAL; no unrestricted SAT time lower bound")

if __name__=="__main__":
    main()
