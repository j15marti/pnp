#!/usr/bin/env python3
"""Standalone exact Q criticality controls, no dependencies. CLOCKJOIN49."""
from itertools import product
W=(set((1,3)),set((2,4)),set((0,3)),set((1,4)),set((0,2)))
def q(h,x,y): return (x in W[h])!=(y in W[h])
def p(h,x,y): return x in W[h] and y in W[h]
def graph(L):
    assert L>=5 and L%2
    V=L+3
    E={(i,j) for i in range(3) for j in range(i+1,3)}
    E|={(i,j) for i in range(3) for j in range(3,V)}
    E|={(min(3+i,3+(i+1)%L),max(3+i,3+(i+1)%L)) for i in range(L)}
    return V,sorted(E)
def is_5_colorable(V,E):
    A=[set() for _ in range(V)]
    for a,b in E:A[a].add(b);A[b].add(a)
    order=sorted(range(V),key=lambda v:(-len(A[v]),v))
    colors=[-1]*V
    def recurse(t):
        if t==V:return colors.copy()
        v=order[t]
        for c in range(5):
            if all(colors[z]!=c for z in A[v]):
                colors[v]=c
                out=recurse(t+1)
                if out is not None:return out
                colors[v]=-1
        return None
    return recurse(0)
def deleted_coloring(L,edge):
    a,b=edge;X=[-1]*(L+3)
    if b<3:
        for v in range(3):X[v]=0 if v in (a,b) else 1
        X[3]=2
        for j in range(1,L):X[3+j]=3+(j%2==1)
    elif a>=3:
        for v in range(3):X[v]=v
        start=b-3 if b-3==(a-3+1)%L else a-3
        for j in range(L):X[3+(start+j)%L]=3+j%2
    else:
        for v in range(3):X[v]=v
        X[b]=a
        for j in range(1,L):X[3+(b-3+j)%L]=3+j%2
    return X
def main():
    assert sum(q(*abc) for abc in product(range(5),repeat=3))==60
    assert sum(p(*abc) for abc in product(range(5),repeat=3))==20
    tests=0;deletions=0
    for L in (5,7,9):
        V,E=graph(L)
        assert len(E)==4*L+3 and is_5_colorable(V,E) is None
        assert all(p(2,0,0) for e in E)
        for ix,edge in enumerate(E):
            X=deleted_coloring(L,edge)
            assert X[edge[0]]==X[edge[1]]
            assert all(X[a]!=X[b] for j,(a,b) in enumerate(E) if j!=ix)
            heads=[0 if j==ix else (X[a] if X[b] in W[X[a]] else X[b])
                   for j,(a,b) in enumerate(E)]
            truth=[q(heads[j],X[a],X[b]) for j,(a,b) in enumerate(E)]
            assert sum(not t for t in truth)==1 and not truth[ix]
            tests+=len(E);deletions+=1
        print('L',L,'vertices',V,'edges',len(E),'critical_deletions',len(E))
    assert (tests,deletions)==(3011,93)
    print('PASS original Q checks',tests,'complete one-clause witnesses',deletions)
if __name__=='__main__':main()
