#!/usr/bin/env python3
"""TMR-5/093 independent compact verifier, standard library only."""
from itertools import product
from collections import deque
import json

S=(1,3)
A=[[int((j-i)%5 in S) for j in range(5)] for i in range(5)]

def matmul(B,C):
    return [[sum(B[i][t]*C[t][j] for t in range(5))
             for j in range(5)] for i in range(5)]

def power(k):
    B=[[int(i==j) for j in range(5)] for i in range(5)]
    for _ in range(k): B=matmul(B,A)
    return B

def count_source(n,edges,B):
    total=0
    for labels in product(range(5),repeat=n):
        weight=1
        for u,v in edges: weight*=B[labels[u]][labels[v]]
        total+=weight
    return total

def subdivide(n,edges,k):
    arcs=[];nxt=n
    for u,v in edges:
        prev=u
        for _ in range(k-1):
            arcs.append((prev,nxt));prev=nxt;nxt+=1
        arcs.append((prev,v))
    return nxt,arcs

def native_count(n,edges):
    adjacency=[[] for _ in range(n)]
    for u,v in edges:
        adjacency[u].append((v,1));adjacency[v].append((u,-1))
    order=sorted(range(n),key=lambda u:-len(adjacency[u]))
    labels=[-1]*n
    def dfs(j):
        if j==n:return 1
        u=order[j];total=0
        for x in range(5):
            if all((labels[v]<0 or
                    (A[x][labels[v]] if d==1 else A[labels[v]][x]))
                   for v,d in adjacency[u]):
                labels[u]=x
                total+=dfs(j+1)
                labels[u]=-1
        return total
    return dfs(0)

def test():
    rows={k:power(k)[0] for k in range(1,8)}
    assert rows[2]==[0,1,1,0,2]
    assert rows[3]==[3,0,3,1,1]
    assert rows[4]==[4,4,1,6,1]
    assert all(power(k)[i][j]>0 for k in range(4,8)
               for i in range(5) for j in range(5))
    for k in range(1,8):
        W=[[0]*5 for _ in range(5)]
        for start in range(5):
            for inc in product(S,repeat=k):
                W[start][(start+sum(inc))%5]+=1
        assert W==power(k)
    gadget_checks=0
    for u,v,a,b,c in product(range(5),repeat=5):
        sat=bool(A[u][a] and A[a][b] and A[b][c]
                 and A[u][c] and A[c][v])
        assert sat==((a==(u+1)%5) and (b==(u+2)%5)
                     and (c==(u+3)%5) and ((v-u)%5 in (1,4)))
        gadget_checks+=1
    all_arcs=[(u,v) for u in range(3) for v in range(3) if u!=v]
    small=0
    for mask in range(64):
        edges=[e for j,e in enumerate(all_arcs) if mask>>j&1]
        for k in range(1,5):
            z=count_source(3,edges,power(k))
            if k>=3:assert z>0
            small+=1
    K3=all_arcs
    k2_n,k2_arcs=subdivide(3,K3,2)
    k3_n,k3_arcs=subdivide(3,K3,3)
    assert (k2_n,len(k2_arcs))==(9,12)
    assert (k3_n,len(k3_arcs))==(15,18)
    assert count_source(3,K3,power(2))==native_count(k2_n,k2_arcs)==0
    assert count_source(3,K3,power(3))==native_count(k3_n,k3_arcs)==6075
    for pins in product(range(5),repeat=3):
        assert all(power(4)[pins[u]][pins[v]]>0 for u,v in K3)
    G7=[(u,v) for u in range(7) for v in range(7)
        if (v-u)%7 in (1,2,3)]
    assert count_source(7,G7,power(2))==0
    assert count_source(7,G7,power(3))>0
    return {'gadget_assignments':gadget_checks,'three_vertex_cases':small,
            'K3_two_subdivision_hom':0,'K3_three_subdivision_hom':6075,
            'G7_two_subdivision_hom':0,'transfer_rows':rows,
            'assertion_failures':0}

if __name__=='__main__':
    print(json.dumps(test(),sort_keys=True,indent=2))
