#!/usr/bin/env python3
"""ARC250 independent compact finite controls; NOT a physical FLMV simulator."""
from itertools import combinations, product
from math import ceil,log2
import json
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
S=list(W);S[9]=(-5,6,-15);S[13]=(-3,-6,-15)
def sat(F,a):return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in F)
def count(F,n):return sum(sat(F,a) for a in product((0,1),repeat=n))
def target(c,extreme):return {abs(l):(int(l>0) if extreme=='S' else int(l<0)) for l in c}
def compatible(c,d,x,y):
    a=target(c,x);b=target(d,y)
    return all(a[v]==b[v] for v in a.keys()&b.keys())
def up(F,a):
    a=dict(a)
    while True:
        changed=False
        for c in F:
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            free=[l for l in c if abs(l) not in a]
            if not free:return None
            if len(free)==1:
                l=free[0];v=abs(l);b=int(l>0)
                if v in a and a[v]!=b:return None
                if v not in a:a[v]=b;changed=True
        if not changed:return a
def dpll(F,a=None):
    a=up(F,a or {})
    if a is None:return False,1
    if all(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F):return True,1
    v=min(abs(l) for c in F for l in c if abs(l) not in a)
    nodes=1
    for b in (0,1):
        ans,steps=dpll(F,a|{v:b});nodes+=steps
        if ans:return True,nodes
    return False,nodes
def restrict(F,pin):
    return [tuple(l for l in c if abs(l) not in pin) for c in F if not any(abs(l) in pin and pin[abs(l)]==int(l>0) for l in c)]
def main():
    out=[];pairs=0;cofactors=0
    for name,F,expected in (('W1_UNSAT',W,0),('SWAP6_SAT',S,54)):
        n=15;m=len(F);h=2+3*(1+ceil(log2(n+1)))
        assert m==4*n//3
        assert all(sum(l==v for c in F for l in c)==2 and sum(l==-v for c in F for l in c)==2 for v in range(1,n+1))
        for c in F:
            assert {v:1-b for v,b in target(c,'S').items()}==target(c,'U')
        for c,d in combinations(F,2):
            same=any(l in d for l in c);opp=any(-l in d for l in c)
            for x,y in product('SU',repeat=2):
                assert compatible(c,d,x,y)==(not(opp if x==y else same));pairs+=1
        for a in ((0,)*n,(1,)*n):
            b=tuple(1-v for v in a)
            for c in F:
                def t(u):return sum(u[abs(l)-1]==int(l>0) for l in c)
                assert t(a)+t(b)==3
        actual=count(F,n);assert actual==expected
        decision,baseline_nodes=dpll(F);assert decision==(expected>0)
        children=[dpll(restrict(F,{1:b})) for b in (0,1)]
        assert (children[0][0] or children[1][0])==decision
        for k in (0,1,2):
            for vs in combinations(range(1,n+1),k):
                for bs in product((0,1),repeat=k):
                    pin=dict(zip(vs,bs));child=restrict(F,pin)
                    untouched=sum(all(abs(l) not in pin for l in c) for c in F)
                    assert untouched>=m-4*k and len(child)>=untouched
                    cofactors+=1
        out.append({'source':name,'models':actual,'DPLL_nodes':baseline_nodes,'two_child_DPLL_nodes':sum(x[1] for x in children),'parent_clause_bits_excluding_header':m*h})
    N=2**12;D=8;q=ceil(N**.6);m=ceil(N**.5)
    print(json.dumps({'scope':'finite controls, not a universal SAT compiler or physical Turing-machine execution','source_controls':out,'pair_modes':pairs,'cofactor_pins':cofactors,'synthetic_DELAY_total':q*m**D},sort_keys=True,indent=2))
if __name__=='__main__':main()
