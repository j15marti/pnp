#!/usr/bin/env python3
"""Recompute exact restricted LSPV-4 ARC298 dense-basis and triangle index ledger.
Full independent verifier and original SAT/UNSAT fixtures are in the companion
reproducibility archive. Python word operations are not native FLMV steps.
"""
from collections import Counter
import json, math
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F=P+tuple(tuple(-x for x in c) for c in Q)
PINS={7:1,8:0,9:0,10:0,11:1,12:1,13:1,14:1,15:0}
def build(t):
    g=[[ (abs(x)+15*i)*(1 if x>0 else -1) for x in clause]
       for i in range(t) for clause in F]
    for i in range(t-1):
        a=i*20; b=(i+1)*20+5
        g[a][2],g[b][1]=g[b][1],g[a][2]
    return tuple(tuple(row) for row in g)
def valid(g,t):
    C=Counter((abs(x),x>0) for row in g for x in row)
    return (len(g)==20*t and len(set(tuple(sorted(c)) for c in g))==len(g)
        and all(len(c)==3 and len(set(map(abs,c)))==3
                and (all(x>0 for x in c) or all(x<0 for x in c)) for c in g)
        and all(C[v,True]==2 and C[v,False]==2 for v in range(1,15*t+1)))
def connected(g,t):
    A={v:set() for v in range(1,15*t+1)}
    for row in g:
        for v in map(abs,row): A[v].update(map(abs,row))
    seen={1}; todo=[1]
    for v in todo:
        for w in A[v]:
            if w not in seen:seen.add(w);todo.append(w)
    return len(seen)==15*t
def triangles(g,p):
    covered=[j for j,row in enumerate(g)
        if any(abs(x) in p and p[abs(x)]==int(x>0) for x in row)]
    uncovered=[j for j in range(len(g)) if j not in set(covered)]
    free=[v for v in range(1,max(map(abs,(x for c in g for x in c)))+1) if v not in p]
    C=Counter((abs(x),x>0) for j in covered for x in g[j] if abs(x) not in p)
    eta=sum(min(C[v,True],C[v,False]) for v in free)
    edges=[(j,*[abs(x) for x in g[j] if abs(x) not in p])
        for j in uncovered if sum(abs(x) not in p for x in g[j])==2]
    incidence={v:[] for v in free}
    for j,u,v in edges:incidence[u].append((j,v));incidence[v].append((j,u))
    assert all(len(x)<=4 for x in incidence.values())
    tri=set(); events=0
    for j,u,v in edges:
        for k,x in incidence[u]:
            if j==k:continue
            for l,y in incidence[v]:
                if j==l or k==l:continue
                events+=1
                if x==y:tri.add(tuple(sorted((j,k,l))))
    selected=[];used=set()
    for z in sorted(tri):
        if not used.intersection(z):selected.append(z);used.update(z)
    return len(edges),len(tri),events,len(selected),2*len(free)-len(uncovered)-eta-len(selected)
def encode(g,t):
    n=15*t;m=20*t;B=n.bit_length();H=m.bit_length()
    bits=[]
    for z in (n,m):bits.extend((z>>k)&1 for k in range(H-1,-1,-1))
    for row in g:
        for z in row:
            bits.append(int(z<0))
            bits.extend((abs(z)>>k)&1 for k in range(B-1,-1,-1))
    return bits
def local_bit(t,pos):
    n=15*t;m=20*t;B=n.bit_length();H=m.bit_length()
    if pos<H:return (n>>(H-1-pos))&1
    if pos<2*H:return (m>>(2*H-1-pos))&1
    a=pos-2*H; rec=a//(B+1);bit=a%(B+1);clause=rec//3
    slot=rec%3;block=clause//20;local=clause%20
    v=abs(F[local][slot])+15*block
    if local==0 and slot==2 and block<t-1:v=15*(block+1)+11
    if local==5 and slot==1 and block>0:v=15*(block-1)+7
    return int(F[local][slot]<0) if bit==0 else (v>>(B-bit))&1
def run():
    growth=[]
    for t in (1,2,4,8,16,32,64):
        g=build(t);assert valid(g,t) and connected(g,t)
        p={15*i+v:bit for i in range(t) for v,bit in PINS.items()}
        E,tri,events,nu,delta=triangles(g,p)
        assert (E,tri,events,nu,delta)==(8*t,4*t,20*t,2*t,0)
        H=(20*t).bit_length();B=(15*t).bit_length()
        N=2*H+60*t*(B+1)
        if t<=32:
            bits=encode(g,t);assert len(bits)==N
            assert all(bits[z]==local_bit(t,z) for z in range(N))
        mask=sum(15*i+v for i in range(t) for v in range(1,7))
        assert mask==45*t*t-24*t
        growth.append(dict(t=t,N=N,free=6*t,rank=6*t,E=E,nu=nu,
            triangles=tri,candidates=events,
            adjacency_bits=16*t*(H+B),basis_cells=mask,
            basis_nonzero=12*t,offline_data_XOR=24*t,
            naive_E_source_scans_bit_reads=E*N,
            local_bit_validated=(t<=32)))
    print(json.dumps(dict(status='RESTRICTED_IMPLEMENTATION',growth=growth,
        p_vs_np='OPEN',native_indexed_TM_full_runtime='NOT_MEASURED'),indent=2))
if __name__=='__main__':run()
