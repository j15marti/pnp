#!/usr/bin/env python3
"""QUIET_EQUIV67 standalone stdlib proof-control reproduction.
Exact on the declared connected B_q+T_q family, NOT a general SAT solver.
The full total hybrid including DPLL fallback is in the linked local package.
"""
import json
from itertools import product

def lid(x):
    return 2 * (abs(x)-1) + (0 if x > 0 else 1)

def decode(z):
    return (z//2+1) * (1 if z%2==0 else -1)

def solve_2sat(n, clauses):
    g=[[] for _ in range(2*n)]; rg=[[] for _ in range(2*n)]
    arcs=0
    for clause in clauses:
        if not clause: return None, None, arcs
        if len(clause)>2: raise ValueError("not binary")
        a=clause[0]
        pairs=[(-a,a)] if len(clause)==1 else [(-a,clause[1]),(-clause[1],a)]
        for x,y in pairs:
            u,v=lid(x),lid(y)
            g[u].append(v);rg[v].append(u);arcs+=1
    seen=[False]*(2*n);order=[]
    for root in range(2*n):
        if seen[root]:continue
        seen[root]=True; stack=[(root,0)]
        while stack:
            u,k=stack[-1]
            if k<len(g[u]):
                v=g[u][k];stack[-1]=(u,k+1)
                if not seen[v]:seen[v]=True;stack.append((v,0))
            else: order.append(u);stack.pop()
    comp=[-1]*(2*n);t=0
    for root in reversed(order):
        if comp[root]!=-1:continue
        comp[root]=t;stack=[root]
        while stack:
            u=stack.pop()
            for v in rg[u]:
                if comp[v]==-1:comp[v]=t;stack.append(v)
        t+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):
        return None,comp,arcs
    a={i+1:comp[2*i]>comp[2*i+1] for i in range(n)}
    return a,comp,arcs

def quiet(q,negative=False):
    n=3*q
    B=[]
    for x in range(1,n):
        B.extend([(-x,x+1),(x,-x-1)])
    T=[(3*i+1,3*i+2,3*i+3) for i in range(q)]
    if negative:T[-1]=tuple(-v for v in T[-1])
    return n,B,T

def replay(F,a):
    return all(any(a[abs(v)] == (v>0) for v in c) for c in F)

def audit(q,negative):
    n,B,T=quiet(q,negative)
    first,comp,r1=solve_2sat(n,B)
    assert first is not None
    assert all(comp[lid(i)]==comp[lid(1)] for i in range(1,n+1))
    reps={}
    for j,t in enumerate(comp):
        z=lid(decode(j))
        # choose signed literal 1 or -1 matching the SCC of each signed source
        reps[j]=1 if t==comp[lid(1)] else -1
    Q=[tuple(dict.fromkeys(reps[comp[lid(v)]] for v in c)) for c in T]
    assert all(len(c)==1 for c in Q)
    ans,_,r2=solve_2sat(n,B+Q)
    if ans is not None:assert replay(B+T,ans)
    assert (ans is None)==negative
    if q<=10:
        calls=0; label='UNSAT'
        # exact declared exhaustive static backdoor baseline
        for bits in product((False,True),repeat=q):
            calls+=1
            forced=dict(zip((3*i+1 for i in range(q)),bits))
            # B forces every source variable to have the same value
            if len(set(bits))!=1:continue
            possible=all(any((bits[0] if v>0 else not bits[0]) for v in c) for c in T)
            if possible:label='SAT';break
        assert calls==2**q
        assert label==('UNSAT' if negative else 'SAT')
    else:calls=None
    return dict(q=q,label='UNSAT' if negative else 'SAT',
                n=n,m=len(B)+len(T),initial_ternaries=q,
                after_quotient_ternaries=0,implication_arcs=r1+r2,
                declared_complete_backdoor_calls=calls)

def main():
    rows=[]
    for q in (2,4,6,8,10,16,32,64,128,256,512):
        for neg in (False,True):
            rows.append(audit(q,neg))
    assert len(rows)==22
    print(json.dumps(dict(status='COMPUTATIONAL; P versus NP OPEN',
                          tests=len(rows),failures=0,results=rows),indent=2))

if __name__=='__main__':
    main()
