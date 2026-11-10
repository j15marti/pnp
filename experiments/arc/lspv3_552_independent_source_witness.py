#!/usr/bin/env python3
"""Independent source/witness and graph-size audit for LSPV-3/552.
Does not invoke the recovered /341 producer/checker or import their code.
"""
import json
from collections import deque
from itertools import combinations

def initial():
    e = [(i,j) for i,j in combinations(range(4),2) if (i,j)!=(0,1)]
    e += [(0,4),(1,4)]
    for i in range(3):
        j = (i+1)%3
        if (i,j)!=(0,1): e.append((5+i,5+j))
        e.extend([(8+i,8+j),(5+i,8+i)])
    e += [(5,11),(6,11),(4,11)]
    e.remove((0,4))
    e.insert(12,(0,4))
    return 12,e

def grow(n,edges):
    edges=list(edges)
    idx=[i for i,e in enumerate(edges) if 8 in e]
    assert len(idx)==3
    for j,new in [(idx[1],n),(idx[2],n+1)]:
        edges[j]=tuple(new if x==8 else x for x in edges[j])
    edges += [(8,n),(n,n+1),(n+1,8)]
    return n+2,edges

def connected(n,edges,drop=-1):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        if i==drop:continue
        adj[u].append(v)
        adj[v].append(u)
    seen={0}
    todo=deque([0])
    while todo:
        for v in adj[todo.popleft()]:
            if v not in seen:seen.add(v);todo.append(v)
    return len(seen)==n

def clauses(n,edges):
    result=[]
    for v in range(n):
        inc=[i for i,(a,b) in enumerate(edges) if v in (a,b)]
        assert len(inc)==3
        for mask in range(8):
            bits=[(mask>>j)&1 for j in range(3)]
            forbidden = (bits[0]==bits[1]) if v==0 else (sum(bits)%2==1)
            if forbidden:
                result.append(tuple(-(e+1) if b else e+1 for e,b in zip(inc,bits)))
    return result

def run():
    n,edges=initial()
    out=[]
    for t in range(6):
        E=len(edges)
        assert E==3*n//2 and n==12+2*t and E==18+3*t
        assert len(set(tuple(sorted(e)) for e in edges))==E
        assert all(a!=b for a,b in edges)
        assert all(sum(v in e for e in edges)==3 for v in range(n))
        assert connected(n,edges) and not connected(n,edges,17)
        assert [i for i,e in enumerate(edges) if 0 in e]==[0,1,12]
        F=clauses(n,edges)
        w=[0]*E
        for e in (0,2,5,12):w[e]=1
        assert all(any(w[abs(l)-1]==int(l>0) for l in cl) for cl in F)
        assert all(sum(w[i] for i,e in enumerate(edges) if v in e)%2==0 for v in range(n))
        assert (w[0]^w[1])==1 and (w[0]^w[1]^w[12])==0
        assert len(F)==4*n
        out.append({'t':t,'vertices':n,'variables':E,'clauses':len(F),'paid_records':4*n-1,
                    'satisfying_assignment':''.join(map(str,w)), 'satisfied_clauses':len(F),
                    'bridge_edge_17':True})
        n,edges=grow(n,edges)
    assert [(v,3*v//2) for v in range(4,13,2)]==[(4,6),(6,9),(8,12),(10,15),(12,18)]
    print(json.dumps({'test':'LSPV-3/552 independent graph+SAT check', 'all_six_pass':True,
     'first_possible_uncertified_cubic_size':{'vertices':12,'variables':18,'clauses':48,'paid_records':47},
     'rows':out},indent=2))

if __name__=='__main__':run()
