#!/usr/bin/env python3
"""Reproduce three q=4 SAT/UNSAT functional-gate controls, stdlib only."""
from itertools import product

def make(q, beta, b):
    assert q >= 4 and q % 2 == 0 and len(beta)==len(b)==q
    h=1; e=list(range(2,q+2)); z=list(range(q+2,2*q+3))
    u,v,x=2*q+3,2*q+4,2*q+5
    nxt=x; guards=[]; gates=[]; clauses=[]
    def fresh():
        nonlocal nxt
        nxt+=1
        return nxt
    for i in range(q):
        eq=(h,e[i-1],e[i])
        for bits in product((0,1),repeat=3):
            if sum(bits)%2==beta[i]: continue
            lit=tuple(v if bit==0 else -v for v,bit in zip(eq,bits))
            G=fresh(); t=fresh()
            guards.append(G); gates.append((G,t,lit[0]))
            clauses.extend([(-G,t),(-lit[0],t),(G,lit[0],-t),(t,lit[1],lit[2])])
    B=[(z[0],u),(z[0],-u),(-z[-1],v),(-z[-1],-v)]
    B += [(-z[i-1],z[i] if b[i-1] else -z[i]) for i in range(1,q+1)]
    for c in B:
        G=fresh();guards.append(G);clauses.append((-G,*c))
    cycle=(x,*guards)
    clauses += [(-cycle[i],cycle[(i+1)%len(cycle)]) for i in range(len(cycle))]
    return nxt,clauses,(x,h,e,z,u,v,guards,gates,B)

def sat(clauses,a):
    return all(any(a[abs(lit)]==int(lit>0) for lit in c) for c in clauses)

def check(q,beta,b):
    n,C,(x,h,e,z,u,v,guards,gates,B)=make(q,beta,b)
    assert n==11*q+9 and len(C)==22*q+9
    assert sum(len(c)==2 for c in C)==13*q+5
    assert sum(len(c)==3 for c in C)==9*q+4
    assert all(len(set(map(abs,c)))==len(c) for c in C)
    source_n=2*q+5; checks=4; models=0
    for bits in product((0,1),repeat=source_n):
        a={i:bits[i-1] for i in range(1,source_n+1)}
        expect=(all(a[e[i-1]]^a[e[i]]^a[h]==beta[i] for i in range(q))
                if a[x]==0 else sat(B,a))
        for guard in guards:a[guard]=a[x]
        for _,t,lit in gates:
            a[t]=int(bool(a[x]) or a[abs(lit)]==int(lit>0))
        assert sat(C,a)==expect
        models+=int(expect);checks+=1
    assert (models>0)==((sum(beta)%2==0) or (0 in b));checks+=1
    return q,models,checks

if __name__=="__main__":
    q=4
    cases=[("UNSAT",[1,0,0,0],[1]*q),
           ("affine_SAT",[0]*q,[1]*q),
           ("binary_SAT",[1,0,0,0],[0,1,1,1])]
    total=0
    for name,beta,b in cases:
        qq,models,checks=check(q,beta,b)
        total+=checks
        print(name,"q=",qq,"models=",models,"checks=",checks)
    print("TOTAL_CHECKS",total,"FAILURES 0")
