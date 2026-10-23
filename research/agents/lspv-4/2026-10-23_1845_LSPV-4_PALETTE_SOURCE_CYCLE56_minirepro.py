#!/usr/bin/env python3
"""PALETTE-SOURCE-CYCLE56 minimal verifier; standard library only."""
from itertools import product

def graph(bits):
    q=len(bits);assert q>=3
    edges=[(0,1),(1,2),(2,0)]
    def x(i):return 3+2*(i%q)
    for i in range(q):edges.extend(((0,x(i)),(0,x(i)+1),(x(i),x(i)+1)))
    for i,b in enumerate(bits):edges.append((x(i+1),x(i) if b else x(i)+1))
    assert len(edges)==4*q+3
    assert len(set(tuple(sorted(e)) for e in edges))==len(edges)
    return 2*q+3,edges

def onehot(V,edges):
    vid=lambda v,c:3*v+c+1
    clauses=[]
    for v in range(V):
        clauses.append(tuple(vid(v,c) for c in range(3)))
        clauses.extend((-vid(v,a),-vid(v,b)) for a,b in ((0,1),(0,2),(1,2)))
    for u,v in edges:
        clauses.extend((-vid(u,c),-vid(v,c)) for c in range(3))
    return clauses

def count_colors(V,edges):
    adj=[set() for _ in range(V)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    colors=[-1]*V
    order=sorted(range(V),key=lambda i:-len(adj[i]))
    def rec(i):
        if i==V:return 1
        v=order[i];forbidden={colors[j] for j in adj[v]}
        total=0
        for c in range(3):
            if c not in forbidden:
                colors[v]=c;total+=rec(i+1)
        colors[v]=-1
        return total
    return rec(0)

def main():
    flips=0
    for q in range(3,9):
        yes=no=0
        for bits in product(range(2),repeat=q):
            V,E=graph(bits);C=onehot(V,E)
            assert V==2*q+3 and len(C)==20*q+21
            assert sum(len(c)==3 for c in C)==2*q+3
            assert sum(len(c)==2 for c in C)==18*q+18
            assert all(len({abs(v) for v in c})==len(c) for c in C)
            sat=sum(bits)%2==0
            if sat:yes+=1
            else:no+=1
            if q<=5:assert count_colors(V,E)==(12 if sat else 0)
            for i in range(q):
                flipped=list(bits);flipped[i]^=1
                V2,E2=graph(flipped);C2=onehot(V2,E2)
                diff=[(j,h) for j,(a,b) in enumerate(zip(C,C2)) for h,(va,vb) in enumerate(zip(a,b)) if va!=vb]
                assert len(diff)==3 and (sum(flipped)%2==0)!=sat
                flips+=1
        assert yes==no==2**(q-1)
        print(f"q={q} yes={yes} no={no} n={6*q+9} k={2*q+3} m={20*q+21}")
    print("verified single-field flips",flips)

if __name__=="__main__":main()
