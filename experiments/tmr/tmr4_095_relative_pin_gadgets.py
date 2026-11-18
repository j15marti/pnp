#!/usr/bin/env python3
"""Small executable witness-recovery smoke test; see the full /095 audit package."""
from itertools import product
R=lambda a,b:(b-a)%5 in (1,3)

def extend(n,arcs,pins):
    e=list(arcs)
    for v,d in pins:
        prev=0
        for i in range((d or 5)):
            last=i==(d or 5)-1
            w=v if last else n
            if not last:n+=1
            z=n;n+=1
            e.extend(((prev,w),(prev,z),(z,w)))
            prev=w
    return n,sorted(set(e))

def decide(n,arcs):
    # Uniform source solver, not a gadget-informed pin oracle.
    inc=[[] for _ in range(n)]
    for u,v in arcs:
        inc[u].append((u,v));inc[v].append((u,v))
    x=[-1]*n
    def rec(i):
        if i==n:return tuple(x)
        for a in range(5):
            x[i]=a
            if all(x[u]<0 or x[v]<0 or R(x[u],x[v]) for u,v in inc[i]):
                w=rec(i+1)
                if w is not None:return w
        x[i]=-1
        return None
    return rec(0)

def witness(n,arcs):
    if n==0:return ()
    if decide(n,arcs) is None:return None
    pins=[]
    for v in range(1,n):
        for d in range(5):
            N,E=extend(n,arcs,pins+[(v,d)])
            if decide(N,E) is not None:
                pins.append((v,d));break
        else:raise AssertionError('no surviving difference')
    ans=(0,)+(tuple(d for _,d in pins))
    assert all(R(ans[u],ans[v]) for u,v in arcs)
    return ans

def check():
    assert witness(0,[])==()
    for a,b,z in product(range(5),repeat=3):
        assert (R(a,b) and R(a,z) and R(z,b))==(b==(a+1)%5 and z==(a+3)%5)
    for d in range(5):
        N,E=extend(2,[],[(1,d)])
        for a,b in product(range(5),repeat=2):
            ways=[0]*5;ways[a]=1
            for _ in range(d or 5):
                nxt=[0]*5
                for x,y,z in product(range(5),repeat=3):
                    if R(x,y) and R(x,z) and R(z,y):nxt[y]+=ways[x]
                ways=nxt
            assert ways[b]==int((b-a)%5==d)
        assert N<=11 and len(E)<=15
    sample=[(1,[]),(1,[(0,0)]),(2,[(0,1)]),(2,[(0,1),(1,0)]),
            (3,[(0,1),(1,2),(2,0)]),(4,[(0,1),(0,2),(1,3),(2,3)])]
    for n,edges in sample:
        expected=next((p for p in product(range(5),repeat=n)
                       if all(R(p[u],p[v]) for u,v in edges)),None)
        got=witness(n,edges)
        assert (got is None)==(expected is None)
        if got is not None:assert all(R(got[u],got[v]) for u,v in edges)
    print('PASS: 125 triangles, 125 chain endpoints, six graph-source witnesses')
if __name__=='__main__':check()
