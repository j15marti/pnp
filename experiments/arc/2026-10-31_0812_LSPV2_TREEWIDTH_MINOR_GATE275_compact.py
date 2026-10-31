#!/usr/bin/env python3
"""TREEWIDTH-MINOR-GATE275 paired YES/NO witness; Python 3, standard library only."""
from itertools import combinations, product
def sat(f,a):return all(any(a[abs(l)-1]==(l>0) for l in c) for c in f)
def edges(f):
    return {frozenset(p) for c in f for p in combinations(sorted({abs(l) for l in c}),2)}
def build(f,n):
    out=[];owner={i:i for i in range(1,n+1)}
    for j,c in enumerate(f):
        yy=[n+3*j+k+1 for k in range(3)]
        out.append(tuple(-v for v in yy))
        for l,y in zip(c,yy):
            out.extend([(l,y),(-l,-y)])
            owner[y]=abs(l)
    return out,owner
def paired(n,unsat):
    f=list(combinations(range(1,n+1),3))
    if unsat:
        for mask in range(7):
            f.append(tuple(x if mask>>(x-1)&1 else -x for x in (1,2,3)))
    else:f.extend([(1,2,3)]*7)
    return f
def main():
    cases=eq=minor=0
    for n in range(4,8):
        for no in (False,True):
            f=paired(n,no);t,owner=build(f,n)
            assert len(t)==7*len(f)
            assert edges(f)=={frozenset(owner[v] for v in edge) for edge in edges(t)
                              if len({owner[v] for v in edge})==2}
            minor+=3*len(f)
            assert len(edges(f))==n*(n-1)//2
            bags=[set(range(1,n+1))]
            for j,c in enumerate(f):
                bags.append({abs(l) for l in c}|set(range(n+3*j+1,n+3*j+4)))
            assert max(len(b)-1 for b in bags)==max(n-1,5)
            for edge in edges(t):assert any(edge<=b for b in bags)
            satcount=0
            for a in product((False,True),repeat=n):
                y=[not(a[abs(l)-1]==(l>0)) for c in f for l in c]
                assert sat(f,a)==sat(t,a+tuple(y))
                eq+=1;satcount+=sat(f,a)
            assert (satcount==0)==no
            cases+=1
    print({'cases':cases,'SAT':4,'UNSAT':4,
           'source_assignment_equivalences':eq,
           'verified_graph_minor_contractions':minor,
           'claim':'tw(F)<=tw(T(F))<=max(tw(F),5); w>=5 gives equality',
           'ARC':'OPEN'})
if __name__=='__main__':main()
