#!/usr/bin/env python3
"""Small independent CERTIFICATE-MINIMAX-GAP76 quickcheck, standard Python only.
The full DPLL and 21943-check audit was executed separately; this checks
the exact q=3 certificate/minimax claims and formula grammar.
"""
from functools import lru_cache
from itertools import combinations, product

def label(q, b):
    return all(any(b[q*i:q*(i+1)]) for i in range(q))

def cert(q, b):
    n=q*q
    x=sum(v<<j for j,v in enumerate(b))
    opponents=[]
    for y in range(1<<n):
        z=tuple((y>>j)&1 for j in range(n))
        if label(q,z)!=label(q,b):
            opponents.append(x^y)
    for k in range(n+1):
        for inds in combinations(range(n),k):
            s=sum(1<<j for j in inds)
            if all(s&d for d in opponents): return k
    raise AssertionError("missing certificate")

def depth(q):
    @lru_cache(None)
    def visit(state):
        rows=[state[i*q:(i+1)*q] for i in range(q)]
        if any(all(v==0 for v in r) for r in rows): return 0
        if all(any(v==1 for v in r) for r in rows): return 0
        return 1+min(max(visit(state[:i]+(0,)+state[i+1:]),
                         visit(state[:i]+(1,)+state[i+1:]))
                     for i,v in enumerate(state) if v==-1)
    d=visit((-1,)*(q*q))
    return d,visit.cache_info().currsize

def cnf(q,b):
    assert q>=3 and len(b)==q*q
    v=0
    def new():
        nonlocal v
        v+=1
        return v
    xs=[[new() for j in range(q)] for i in range(q)]
    clauses=[]
    for i in range(q):
        for j in range(q):
            a,t=new(),new()
            lit=xs[i][j] if b[i*q+j] else -xs[i][j]
            for sa,st in product((1,-1), repeat=2):
                clauses.append((lit,sa*a,st*t))
    for i in range(q):
        if q==3:
            clauses.append(tuple(xs[i]))
        else:
            ys=[new() for j in range(q-3)]
            clauses.append((xs[i][0],xs[i][1],ys[0]))
            for j in range(2,q-2):
                clauses.append((-ys[j-2],xs[i][j],ys[j-1]))
            clauses.append((-ys[-1],xs[i][-2],xs[i][-1]))
    assert v==4*q*q-3*q
    assert len(clauses)==5*q*q-2*q
    assert len(set(clauses))==len(clauses)
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in clauses)
    return v,clauses

def run():
    for q in (2,3):
        d,states=depth(q)
        assert d==q*q
        print("minimax",q,d,"states",states)
    sat=unsat=0
    q=3
    for m in range(1<<9):
        b=tuple((m>>j)&1 for j in range(9))
        assert cert(q,b)==3
        n,clauses=cnf(q,b)
        assert (n,len(clauses))==(27,39)
        if label(q,b): sat+=1
        else: unsat+=1
    assert (sat,unsat)==(343,169)
    print("q3 certificates",sat,unsat,"SAT/UNSAT", "OK")
    print("PROVED claims require the standalone LaTeX proof; these are finite controls")
if __name__=="__main__":run()
