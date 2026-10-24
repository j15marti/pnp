#!/usr/bin/env python3
"""CYCLE-AFFINE-SWITCH123: compact independent XOR-prism / chord audit.
Python stdlib, restricted-source theorem only. No unrestricted SAT lower bound.
The extended 335-check code and raw output are in the conversation ZIP.
"""
from itertools import product
from collections import deque
import json

def clauses_of(row,charge):
    return [tuple(-v if a else v for v,a in zip(row,bits))
            for bits in product((0,1),repeat=3)
            if sum(bits)%2 != charge]

def prism(r,odd):
    edges=[(s*r+i,s*r+(i+1)%r) for s in (0,1) for i in range(r)]
    edges += [(i,r+i) for i in range(r)]
    adj=[[] for _ in range(2*r)]
    for e,(u,v) in enumerate(edges,1):
        adj[u].append(e);adj[v].append(e)
    assert all(len(row)==3 for row in adj)
    charges=[0]*(2*r);charges[0]=int(odd)
    cnf=[cl for v in range(2*r) for cl in clauses_of(adj[v],charges[v])]
    return edges,adj,charges,cnf

def gaussian(rows,n):
    pivots={};xors=0
    for row,rhs in rows:
        mask=0
        for x in row: mask^=1<<(x-1)
        while mask:
            p=(mask&-mask).bit_length()-1
            if p not in pivots:
                pivots[p]=(mask,rhs)
                break
            mask^=pivots[p][0]
            rhs^=pivots[p][1]
            xors+=1
        if not mask and rhs:return False,None,xors
    x=0
    for p in sorted(pivots,reverse=True):
        mask,rhs=pivots[p]
        if rhs^((mask&x).bit_count()%2):x|=1<<p
    return True,[(x>>i)&1 for i in range(n)],xors

def evaluate(cnf,assignment):
    return all(any(assignment[abs(x)-1]==int(x>0) for x in c) for c in cnf)

def cutset(edges,incident,charges):
    n=len(incident);graph=[[] for _ in range(n)]
    for e,(u,v) in enumerate(edges,1):
        graph[u].append((v,e));graph[v].append((u,e))
    parent=[-1]*n;parent[0]=0;pe=[0]*n;order=[0]
    for v in order:
        for u,e in graph[v]:
            if parent[u]<0:parent[u]=v;pe[u]=e;order.append(u)
    assert len(order)==n
    tree=set(pe[1:])
    chords=[e for e in range(1,len(edges)+1) if e not in tree]
    calls=0;rowchecks=0
    for bits in product((0,1),repeat=len(chords)):
        calls+=1;fix=dict(zip(chords,bits));msg={};feasible=True
        for v in reversed(order):
            possible=set()
            for word in product((0,1),repeat=len(incident[v])):
                rowchecks+=1
                local=dict(zip(incident[v],word))
                if sum(word)%2!=charges[v]:continue
                if any(local[e]!=fix[e] for e in incident[v] if e in fix):continue
                if any(local[pe[u]] not in msg[u] for u,_ in graph[v] if parent[u]==v):continue
                possible.add(0 if v==0 else local[pe[v]])
            msg[v]=possible
            if not possible:feasible=False;break
        if feasible:return True,calls,rowchecks,len(chords)
    return False,calls,rowchecks,len(chords)

def run():
    checked=0;out=[]
    for r in (3,4,5,6,8,10):
        for odd in (False,True):
            edges,inc,charges,cnf=prism(r,odd)
            assert len(edges)==3*r and len(cnf)==8*r;checked+=1
            assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in cnf);checked+=1
            y,sol,xors=gaussian(zip(inc,charges),3*r)
            assert y== (not odd);checked+=1
            if y:assert evaluate(cnf,sol);checked+=1
            z,calls,rowchecks,q=cutset(edges,inc,charges)
            assert z==y and q==r+1;checked+=1
            if odd:
                assert calls==2**(r+1);checked+=1
                for v in range(2*r):
                    other=[(inc[u],charges[u]) for u in range(2*r) if u!=v]
                    sat,_,_=gaussian(other,3*r)
                    assert sat;checked+=1
            if r==3:
                brute=any(evaluate(cnf,b) for b in product((0,1),repeat=3*r))
                assert brute==y;checked+=1
            out.append({'r':r,'label':'UNSAT' if odd else 'SAT',
                        'cycle_rank':q,'cutset_assignments':calls,
                        'cutset_rows':rowchecks,'gaussian_row_xors':xors})
    print(json.dumps({'run':'CYCLE-AFFINE-SWITCH123-MINI','checked':checked,
                      'discrepancies':0,'cases':out,'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':run()
