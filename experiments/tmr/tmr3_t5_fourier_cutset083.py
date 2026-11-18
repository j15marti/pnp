#!/usr/bin/env python3
"""TMR-3/083: exact Z5 Fourier cutset with 5**s retained states.
Uses no floating point. Run without arguments for deterministic regression checks.
"""
from itertools import product
from collections import deque
Z=(0,0,0,0)
I=(1,0,0,0)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def phase(a,k):
    q=[0]*5
    for i,x in enumerate(a): q[(i+k)%5]+=x
    return tuple(q[i]-q[4] for i in range(4))
def certificate(n,arcs):
    if type(n)!=int or n<0: raise ValueError('n')
    es=set()
    for e in arcs:
        if len(e)!=2: raise ValueError('arc')
        u,v=e
        if type(u)!=int or type(v)!=int or not(0<=u<n and 0<=v<n):
            raise ValueError('vertex')
        es.add((u,v))
    if any(u==v or (v,u) in es for u,v in es): return None
    adj=[set() for _ in range(n)]
    for u,v in es: adj[u].add(v);adj[v].add(u)
    par=[-1]*n;depth=[0]*n;eid=[-1]*n;seen=set();selected=set();edges=[];c=0
    for root in range(n):
        if root in seen: continue
        c+=1;seen.add(root);q=deque([root])
        while q:
            u=q.popleft()
            for v in sorted(adj[u]):
                if v in seen: continue
                seen.add(v);q.append(v);par[v]=u;depth[v]=depth[u]+1
                eid[v]=len(edges);edges.append((1,2) if (u,v) in es else (4,3))
                selected.add(frozenset((u,v)))
    rows=[];offset=[];t=len(edges)
    for u,v in sorted(es):
        if frozenset((u,v)) in selected: continue
        terms=[]
        while depth[u]>depth[v]: terms.append((eid[u],-1));u=par[u]
        while depth[v]>depth[u]: terms.append((eid[v],1));v=par[v]
        while u!=v:
            terms.extend(((eid[u],-1),(eid[v],1)));u=par[u];v=par[v]
        row=[0]*t;a=0
        for j,sgn in terms:
            base,step=edges[j];a+=sgn*base;row[j]=(row[j]+sgn*step)%5
        rows.append(row);offset.append(a%5)
    B=[];piv=[];gam=[]
    for j in range(t):
        rem=[row[j] for row in rows];coords=[]
        for b,p in zip(B,piv):
            w=rem[p];coords.append(w);rem=[(x-w*y)%5 for x,y in zip(rem,b)]
        if any(rem):
            p=next(i for i,x in enumerate(rem) if x);alpha=rem[p]
            B.append(tuple(x*pow(alpha,-1,5)%5 for x in rem));piv.append(p)
            coords.append(alpha)
        gam.append(coords)
    rho=len(B);gam=[tuple(g+[0]*(rho-len(g))) for g in gam]
    assert all(rows[i][j]==sum(B[k][i]*gam[j][k] for k in range(rho))%5
               for j in range(t) for i in range(len(rows)))
    return c,tuple(offset),tuple(B),tuple(gam)
def exact_count(n,arcs,s=0):
    cert=certificate(n,arcs)
    if cert is None:return 0
    c,offset,B,gam=cert;rho=len(B)
    if type(s)!=int or not(0<=s<=rho):raise ValueError('retained rank')
    h=rho-s
    low=list(product(range(5),repeat=s))
    idx={z:i for i,z in enumerate(low)}
    # Critical memory invariant: HIGH vectors are iterated, never materialized.
    high=lambda:product(range(5),repeat=h)
    numerator=Z
    for w in high():
        dp=[Z]*len(low);dp[idx[(0,)*s]]=I
        for g in gam:
            new=dp.copy();k=sum(w[i]*g[s+i] for i in range(h))%5
            for j,z in enumerate(low):
                if dp[j]!=Z:
                    target=tuple((z[i]+g[i])%5 for i in range(s))
                    p=idx[target];new[p]=add(new[p],phase(dp[j],k))
            dp=new
        for a in low:
            if dp[idx[a]]==Z:continue
            for b in high():
                z=a+b
                if all((off+sum(z[k]*B[k][i] for k in range(rho)))%5 in (1,3)
                       for i,off in enumerate(offset)):
                    numerator=add(numerator,phase(dp[idx[a]],
                        -sum(w[i]*b[i] for i in range(h))%5))
    assert numerator[1:]==(0,0,0) and numerator[0]%(5**h)==0
    return 5**c*(numerator[0]//(5**h))
def brute(n,es):
    return sum(all((a[v]-a[u])%5 in (1,3) for u,v in es)
               for a in product(range(5),repeat=n))
if __name__=='__main__':
    import random
    random.seed(83791);checks=0
    for n in range(6):
        for _ in range(22):
            arcs=[(u,v) for u in range(n) for v in range(n)
                  if random.randrange(8)==0]
            C=certificate(n,arcs)
            rho=len(C[2]) if C is not None else 0
            for s in range(rho+1):
                assert exact_count(n,arcs,s)==brute(n,arcs)
                checks+=1
    for n in (3,4,5,20,100):
        arcs=[(i,(i+1)%n) for i in range(n)]
        assert exact_count(n,arcs,0)==exact_count(n,arcs,1)
        checks+=1
    print('PASS:', checks, 'exact original-coloring comparisons')
