#!/usr/bin/env python3
"""ARC210 independently test the exact-(2P,2N) torus construction.
Standard library only. Seed fixed. No historical project solver imports.
"""
from collections import deque
import json, random
SEED=21020261028
rng=random.Random(SEED)

def make_torus(L):
    assert L>=6 and L%3==0
    x=lambda r,c:(r%L)*L+(c%L)
    clauses=[]
    for r in range(L):
        for off in (0,1):
            for j in range(L//3):
                c=(off+3*j)%L
                clauses.append(tuple(x(r,c+t)+1 for t in range(3)))
    for c in range(L):
        for off in (0,1):
            for j in range(L//3):
                r=(off+3*j)%L
                clauses.append(tuple(-(x(r+t,c)+1) for t in range(3)))
    return clauses

def audit_graph(L,clauses):
    n=L*L
    plus=[0]*n;minus=[0]*n
    adj=[set() for _ in range(n)]
    scope=[]
    for cl in clauses:
        vs=tuple(abs(lit)-1 for lit in cl)
        assert len(vs)==3 and len(set(vs))==3
        scope.append(frozenset(vs))
        for lit in cl:(plus if lit>0 else minus)[abs(lit)-1]+=1
        for v in vs:
            for u in vs:
                if u!=v:adj[v].add(u)
    assert len(clauses)==4*n//3
    assert len(set(clauses))==len(clauses)
    assert len(set(scope))==len(scope)
    assert all(v==2 for v in plus+minus)
    queue=deque([0]);seen={0}
    while queue:
        for u in adj[queue.popleft()]:
            if u not in seen:seen.add(u);queue.append(u)
    assert len(seen)==n
    for r in range(L):
        for c in range(L):
            v=r*L+c
            assert r*L+(c+1)%L in adj[v]
            assert ((r+1)%L)*L+c in adj[v]
    return adj

def width(order,adj):
    n=len(order)
    assert set(order)==set(range(n))
    p={v:i for i,v in enumerate(order)}
    last=[max(p[u] for u in adj[v]|{v}) for v in range(n)]
    death=[0]*n
    for d in last:death[d]+=1
    active=0;maximum=0;middle=None
    for i,v in enumerate(order):
        active+=1-death[i]
        maximum=max(maximum,active)
        if i+1==n//2:middle=active
    for i in (0,n//6,n//2-1,2*n//3,n-1):
        pref=set(order[:i+1])
        direct=sum(any(u not in pref for u in adj[v]) for v in pref)
        predicted=sum(p[v]<=i<last[v] for v in range(n))
        assert direct==predicted
    return maximum,middle

def sampled_cut(L,number=50):
    n=L*L;minimum=10**10
    for _ in range(number):
        chosen=set(rng.sample(range(n),n//2))
        crossing=0
        for v in chosen:
            r,c=divmod(v,L)
            crossing+=sum(u not in chosen for u in (r*L+(c+1)%L,r*L+(c-1)%L,
                           ((r+1)%L)*L+c,((r-1)%L)*L+c))
        assert crossing>=L
        minimum=min(minimum,crossing)
    return minimum

def main():
    rows=[]
    checks=0
    for L in (6,12,18,24,36,48):
        cl=make_torus(L);n=L*L
        adj=audit_graph(L,cl)
        checks+=4*n+len(cl)
        witness=[int(r%3==c%3) for r in range(L) for c in range(L)]
        assert all(any(witness[abs(v)-1]==(v>0) for v in clause) for clause in cl)
        checks+=len(cl)
        hit={r*L+c for r in range(L) for c in range(L) if r%3==c%3}
        assert len(hit)==n//3
        assert all(any(abs(v)-1 in hit for v in clause) for clause in cl)
        checks+=len(cl)
        row,mid=width(list(range(n)),adj)
        assert row<=5*L and mid>=L/4
        random_widths=[]
        for _ in range(10):
            order=list(range(n));rng.shuffle(order)
            wm,wmid=width(order,adj)
            assert wmid>=L/4
            random_widths.append(wm)
        rows.append(dict(L=L,n=n,clauses=len(cl),global_syntactic_backdoor=len(hit),
                         assignment_ones=sum(witness),row_major_max_frontier=row,
                         row_major_middle_frontier=mid,random_order_frontier_min_max=
                         [min(random_widths),max(random_widths)],
                         sampled_middle_grid_cut_min=sampled_cut(L),
                         proved_lower_frontier_floor=L/4,proved_row_major_upper=5*L))
    print(json.dumps(dict(status="PASS",seed=SEED,checks_min=checks,scaling=rows,
             limitations=["random tests do not prove widths for all orders",
                          "syntactic width does not imply a SAT time lower bound",
                          "no arbitrary-SAT compressor supplied"]),indent=2))
if __name__=="__main__": main()
