#!/usr/bin/env python3
"""T5 path-relation saturation and high-girth PC certificate, no dependencies."""
from itertools import product
from collections import deque
import json

P={1,3}
F=(1<<25)-1
EQ=sum(1<<(6*a) for a in range(5))

def path(signs):
    residues={0}
    for s in signs: residues={(a+s*d)%5 for a in residues for d in P}
    return sum(1<<(5*a+b) for a in range(5) for b in range(5)
               if (b-a)%5 in residues)

def comp(x,y):
    return sum(1<<(5*a+c) for a in range(5) for c in range(5)
               if any(x>>(5*a+b)&1 and y>>(5*b+c)&1 for b in range(5)))

def cert(n, arcs):
    A=set(arcs)
    adj=[[] for _ in range(n)]
    for u,v in A:
        assert u!=v and (v,u) not in A
        adj[u].append(v); adj[v].append(u)
    M=[[F]*n for _ in range(n)]
    for src in range(n):
        M[src][src]=EQ
        q=deque([src]); parent={src:None}
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in parent: parent[v]=u;q.append(v)
        for dst in range(n):
            if dst not in parent or dst==src: continue
            steps=[]; v=dst
            while v!=src:
                u=parent[v]
                steps.append(1 if (u,v) in A else -1)
                v=u
            if len(steps)<=3:M[src][dst]=path(steps[::-1])
    # For girth >=7 the shortest path of length <=3 is unique.
    for u in range(n):
        for v in range(n):
            assert M[u][v]
            for w in range(n):
                assert M[u][v]&comp(M[u][w],M[w][v])==M[u][v]
    return n**3

def run():
    walks=0; cases=0; triples=0
    for k in range(1,8):
        for signs in product((-1,1),repeat=k):
            x=path(signs)
            assert x.bit_count()==5*min(5,k+1)
            if k>=4:assert x==F
            walks+=1
    for n in (7,8):
        ring=[(i,(i+1)%n) for i in range(n)]
        for mask in range(1<<n):
            arcs=[(u,v) if mask>>i&1 else (v,u)
                  for i,(u,v) in enumerate(ring)]
            triples+=cert(n,arcs);cases+=1
    return dict(revision='tmr5-t5-pc071-min-v1',walks=walks,
                ring_cases=cases,path_consistency_triples=triples,failures=0)

if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
