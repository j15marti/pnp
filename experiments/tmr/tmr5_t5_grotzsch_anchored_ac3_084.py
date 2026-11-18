#!/usr/bin/env python3
"""Independent TMR-5/084 compact anchored AC3 reproduction on genuine T5 arcs."""
from collections import deque
from itertools import product

def base(negative):
    if not negative:
        return sorted((i, 5+(i+d)%6) for i in range(5) for d in range(4))
    r=[(i,(i+1)%5) for i in range(5)]
    e={tuple(sorted(x)) for x in r}
    for u,v in r:
        e.add(tuple(sorted((u,v+5))))
        e.add(tuple(sorted((v,u+5))))
    e.update((i+5,10) for i in range(5))
    assert len(e)==20
    return sorted(e)

def instance(negative,h,L):
    assert h>=1 and (L==0 or L>=2)
    n=0; old=[]; prev=None
    for i in range(h):
        d={}
        for j in range(11):
            if i and j==0:d[j]=prev
            else:d[j]=n;n+=1
        old += [(min(d[u],d[v]),max(d[u],d[v])) for u,v in base(negative)]
        prev=d[10]
    if L:
        grid={}
        for i,j in product(range(L),repeat=2):
            if (i,j)==(0,0):grid[i,j]=prev
            else:grid[i,j]=n;n+=1
        for i,j in product(range(L),repeat=2):
            if i+1<L:old.append(tuple(sorted((grid[i,j],grid[i+1,j]))))
            if j+1<L:old.append(tuple(sorted((grid[i,j],grid[i,j+1]))))
    arcs=[]
    for u,v in old:
        assert u<v
        a,b,c=n,n+1,n+2;n+=3
        arcs += [(u,a),(a,b),(b,c),(u,c),(c,v)]
    return n,arcs

def anchored_ac3(n,arcs,pin):
    D=[31]*n;D[pin]=1
    arcs2=[];watch=[[] for _ in range(n)]
    for u,v in arcs:
        for i,j,sgn in ((u,v,1),(v,u,-1)):
            k=len(arcs2);arcs2.append((i,j,sgn));watch[j].append(k)
    q=deque(range(len(arcs2)));seen=set(q)
    while q:
        k=q.popleft();seen.remove(k)
        i,j,sgn=arcs2[k]
        new=0
        for a in range(5):
            if D[i]>>a&1 and any(D[j]>>b&1 and ((b-a)%5 in (1,3) if sgn==1 else (a-b)%5 in (1,3)) for b in range(5)):
                new|=1<<a
        if not new:return False
        if new!=D[i]:
            D[i]=new
            for t in watch[i]:
                if t not in seen:seen.add(t);q.append(t)
    # A separate certificate: all remaining labels have a partner on every genuine directed arc.
    for u,v in arcs:
        for a in range(5):
            if D[u]>>a&1:
                assert any(D[v]>>b&1 and (b-a)%5 in (1,3) for b in range(5))
        for b in range(5):
            if D[v]>>b&1:
                assert any(D[u]>>a&1 and (b-a)%5 in (1,3) for a in range(5))
    assert all(D)
    return True

if __name__=='__main__':
    tested=0
    for h,L in ((1,0),(2,0),(3,0),(1,3),(2,4),(2,6)):
        for neg in (True,False):
            n,arcs=instance(neg,h,L)
            assert n==(70*h+7*L*L-6*L if L else 70*h+1)
            assert len(arcs)==100*h+10*L*(L-1)
            for pin in range(n):
                assert anchored_ac3(n,arcs,pin),(neg,h,L,pin)
                tested+=1
    assert tested==2244
    print('TMR-5/084 PASS, all 2244 anchored AC3 controls')
