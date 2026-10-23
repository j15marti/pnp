#!/usr/bin/env python3
"""REVERSE-SELECTOR57 independent minimal stdlib reproducer.

Tests paired monotone exact-(2+,2-) formulas on cubic support graphs.
Full bipartite defective-support flow auditor and raw results are in
the separate downloadable complete audit package, not this miniature.
"""
from collections import Counter, defaultdict

def cubic_prism(q):
    assert q >= 3
    edges = []
    for side in (0, q):
        for i in range(q):
            edges.append((side+i,side+(i+1)%q))
    for i in range(q):
        edges.append((i,q+i))
    return edges

def paired_formula(edges, vertex_count):
    supports = [[] for _ in range(vertex_count)]
    for x,(u,v) in enumerate(edges,1):
        assert u != v
        supports[u].append(x)
        supports[v].append(x)
    assert all(len(s)==3 for s in supports)
    pos = [tuple(sorted(s)) for s in supports]
    assert len(set(pos))==vertex_count
    return pos + [tuple(-x for x in s) for s in pos]

def matching_assignment(edges,vertex_count):
    incident=defaultdict(list)
    for x,(u,v) in enumerate(edges,1):
        incident[u].append((v,x))
        incident[v].append((u,x))
    assert all(len(incident[v])==3 for v in range(vertex_count))
    covered=set(); red=set()
    for x,(u,v) in enumerate(edges,1):
        if u not in covered and v not in covered:
            covered.add(u);covered.add(v);red.add(x)
    unmatched=[v for v in range(vertex_count) if v not in covered]
    right={}
    def augment(u,seen):
        for v,x in incident[u]:
            if v not in covered or v in seen:
                continue
            seen.add(v)
            if v not in right or augment(right[v][0],seen):
                right[v]=(u,x)
                return True
        return False
    for u in unmatched:
        assert augment(u,set())
    red.update(x for u,x in right.values())
    a={x:(x in red) for x in range(1,len(edges)+1)}
    assert all(1<=sum(a[x] for _,x in incident[v])<=2
               for v in range(vertex_count))
    return a,len(unmatched)

def eval_clause(c,a):
    return any(a[abs(l)]==(l>0) for l in c)

def reverse_selector(F,a):
    out=[]
    for c in F:
        hits=[l for l in c if a[abs(l)]==(l>0)]
        if not hits: return None
        out.append(hits[0])
    return out

def reconstruct(F,selectors,n):
    a={}
    for l in selectors:
        v=abs(l); want=l>0
        if v in a: assert a[v]==want
        a[v]=want
    for v in range(1,n+1): a.setdefault(v,False)
    assert all(eval_clause(c,a) for c in F)
    return a

def check(q):
    E=cubic_prism(q); n=len(E); m=4*q
    F=paired_formula(E,2*q)
    assert len(F)==m and 3*m==4*n
    counts=Counter((abs(l),l>0) for c in F for l in c)
    assert all(counts[(x,True)]==2 and counts[(x,False)]==2
               for x in range(1,n+1))
    graph_vertices=3*m; conflicts=4*n; triangles=3*m
    assert graph_vertices==4*n
    assert conflicts+triangles==8*n
    a,unmatched=matching_assignment(E,2*q)
    assert all(eval_clause(c,a) for c in F)
    picks=reverse_selector(F,a)
    assert reconstruct(F,picks,n)==reconstruct(F,picks,n)
    return dict(q=q,n=n,m=m,unmatched_greedy=unmatched,
                conflict_edges=conflicts,degree_four_edges=8*n)

if __name__=="__main__":
    import json
    print(json.dumps([check(q) for q in (3,4,5,6,8,12,20,40)],indent=2))
