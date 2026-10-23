#!/usr/bin/env python3
"""Self-contained exact Euler-NAE and monotone repair mini auditor, no dependencies."""
from collections import defaultdict
from itertools import product

# Eight distinct 3-supports, each of six source variables appearing four times.
H=[(0,1,2),(0,3,4),(1,3,5),(2,4,5),
   (3,4,5),(1,2,5),(0,2,4),(0,1,3)]

def euler_two_witness(clauses, a):
    m=len(clauses)
    occ=defaultdict(list)
    for ci,C in enumerate(clauses):
        assert len(set(C))==len(C)
        for j,v in enumerate(C):occ[v].append((ci,j))
    edges=[]
    for v in sorted(occ):
        assert len(occ[v])%2==0
        L=sorted(occ[v])
        for j in range(0,len(L),2):
            edges.append((L[j][0],L[j+1][0],L[j],L[j+1]))
    real=len(edges)
    deg=[0]*m
    for p,q,*_ in edges:deg[p]+=1;deg[q]+=1
    odd=[i for i,d in enumerate(deg) if d%2]
    assert len(odd)%2==0
    for j in range(0,len(odd),2):edges.append((odd[j],odd[j+1],None,None))
    adj=[[] for _ in range(m)]
    for ei,(p,q,*_) in enumerate(edges):adj[p].append(ei);adj[q].append(ei)
    used=[False]*len(edges); idx=[0]*m;head={}
    for s in range(m):
        stack=[s]
        while stack:
            v=stack[-1]
            while idx[v]<len(adj[v]) and used[adj[v][idx[v]]]:idx[v]+=1
            if idx[v]==len(adj[v]):stack.pop();continue
            ei=adj[v][idx[v]];idx[v]+=1
            if used[ei]:continue
            used[ei]=True
            p,q,*_=edges[ei]
            t=q if v==p else p
            head[ei]=t
            stack.append(t)
    assert all(used)
    true=set()
    for ei in range(real):
        p,q,op,oq=edges[ei]
        true.add(op if head[ei]==p else oq)
    signed=[]
    for ci,C in enumerate(clauses):
        signed.append(tuple((v+1 if bool(a[v])==((ci,j) in true) else -(v+1)) for j,v in enumerate(C)))
    return signed

def truth_counts(F,a):
    return [sum((L>0)==bool(a[abs(L)-1]) for L in C) for C in F]

def repair_monotone(F):
    m=len(F)
    pos=[i for i,C in enumerate(F) if all(v>0 for v in C)]
    neg=[i for i,C in enumerate(F) if all(v<0 for v in C)]
    assert len(pos)==len(neg)==m//2
    slots=defaultdict(lambda: [[],[]])
    for ci,C in enumerate(F):
        for j,L in enumerate(C):slots[abs(L)][int(L>0)].append((ci,j))
    edge=[];adj=defaultdict(list)
    for v in sorted(slots):
        P,Q=slots[v][1],slots[v][0]
        assert len(P)==len(Q)==2
        for p,q in zip(P,Q):
            ei=len(edge);edge.append((p,q));adj[p[0]].append(ei)
    match={}
    def visit(u,seen):
        for ei in adj[u]:
            v=edge[ei][1][0]
            if v in seen:continue
            seen.add(v)
            if v not in match or visit(match[v][0],seen):
                match[v]=(u,ei)
                return True
        return False
    for u in pos:assert visit(u,set())
    assert len(match)==m//2
    G=[list(C) for C in F]
    for u,ei in match.values():
        for ci,j in edge[ei]:G[ci][j]*=-1
    return [tuple(C) for C in G]

def check():
    n=6;checks=0
    for a in product((0,1),repeat=n):
        F=euler_two_witness(H,a)
        counts=truth_counts(F,a)
        complement=truth_counts(F,tuple(1-x for x in a))
        assert all(x in (1,2) for x in counts+complement)
        assert all(x+y==3 for x,y in zip(counts,complement))
        for v in range(1,n+1):
            assert sum(L==v for C in F for L in C)==2
            assert sum(L==-v for C in F for L in C)==2
        checks+=1
    source=[tuple(v+1 if i<4 else -(v+1) for v in C) for i,C in enumerate(H)]
    R=repair_monotone(source)
    hamming=sum(x!=y for C,D in zip(source,R) for x,y in zip(C,D))
    assert hamming==len(source)==8
    assert all(x in (1,2) for x in truth_counts(R,[1]*n)+truth_counts(R,[0]*n))
    for v in range(1,n+1):
        assert sum(L==v for C in R for L in C)==2
        assert sum(L==-v for C in R for L in C)==2
    checks+=1
    for q in range(1,5):
        for bits in product((0,1),repeat=q):
            z=lambda i:i+1
            u=q+2;v=q+3
            clauses=[(z(0),u),(z(0),-u),(-z(q),v),(-z(q),-v)]
            clauses += [(-z(i),z(i+1) if bit else -z(i+1)) for i,bit in enumerate(bits)]
            sat=any(all(any((L>0)==bool(a[abs(L)-1]) for L in C) for C in clauses)
                    for a in product((0,1),repeat=q+3))
            assert sat== (not all(bits))
            checks+=1
    print({'checked_cases':checks,'failures':0,'monotone_optimal_hamming':8,
           'scope':'finite reproducibility only; P versus NP OPEN'})

if __name__=='__main__':check()
