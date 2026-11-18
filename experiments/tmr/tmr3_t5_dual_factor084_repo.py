#!/usr/bin/env python3
"""TMR-3/084 dual Fourier factor elimination for T5; exact integers only.
Requires the predecessor tmr3_t5_fourier_cutset083.py in the same directory.
The large independent reference/audit is distributed separately.
"""
from collections import deque
from itertools import product
import argparse, json, random
from tmr3_t5_fourier_cutset083 import forest_certificate, count_bruteforce

O=(1,0,0,0)
Z=(0,0,0,0)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):
    v=[0]*5
    for i in range(4):
        for j in range(4):v[(i+j)%5]+=a[i]*b[j]
    return tuple(v[i]-v[4] for i in range(4))
def power(e):
    e%=5
    return (-1,-1,-1,-1) if e==4 else tuple(int(i==e) for i in range(4))

def dfs_matrix(n,arcs):
    E=set(tuple(e) for e in arcs)
    adj=[set() for _ in range(n)]
    for u,v in E:adj[u].add(v);adj[v].add(u)
    parent=[-1]*n;depth=[0]*n;eid=[-1]*n
    increments=[];chosen=set();seen=set();c=0
    for root in range(n):
        if root in seen:continue
        c+=1;seen.add(root);stack=[(root,iter(sorted(adj[root])))]
        while stack:
            u,it=stack[-1]
            try:v=next(it)
            except StopIteration:stack.pop();continue
            if v in seen:continue
            seen.add(v);parent[v]=u;depth[v]=depth[u]+1
            eid[v]=len(increments)
            increments.append((1,2) if (u,v) in E else (4,3))
            chosen.add(frozenset((u,v)))
            stack.append((v,iter(sorted(adj[v]))))
    chords=[(u,v) for u,v in sorted(E) if frozenset((u,v)) not in chosen]
    q=len(chords);t=len(increments);a=[];C=[]
    for U,V in chords:
        u,v=U,V;terms=[]
        while depth[u]>depth[v]:terms.append((eid[u],-1));u=parent[u]
        while depth[v]>depth[u]:terms.append((eid[v],1));v=parent[v]
        while u!=v:
            terms.extend(((eid[u],-1),(eid[v],1)))
            u=parent[u];v=parent[v]
        row=[0]*t;off=0
        for j,s in terms:
            base,diff=increments[j];off+=s*base
            row[j]=(row[j]+s*diff)%5
        a.append(off%5);C.append(tuple(row))
    return dict(c=c,t=t,q=q,a=a,C=C)

def width_order(C,t):
    q=len(C);adj=[set() for _ in range(q)]
    for j in range(t):
        supp=[i for i in range(q) if C[i][j]]
        for i in supp:adj[i].update(set(supp)-{i})
    active=set(range(q));order=[];w=0
    while active:
        def key(i):
            ns=adj[i]&active
            return (sum(u<v and v not in adj[u] for u in ns for v in ns),len(ns),i)
        i=min(active,key=key);ns=adj[i]&active
        w=max(w,len(ns))
        for u in ns:adj[u].update(ns-{u});adj[u].discard(i)
        active.remove(i);order.append(i)
    return order,w

def exact_count(n,arcs):
    cert=forest_certificate(n,arcs)
    if cert['unsat']:return 0,dict(contradiction=True)
    q=cert['chords'];t=cert['tree_bits'];rho=cert['rank']
    basis=cert['basis'];gamma=cert['gamma']
    bfs=dict(c=cert['components'],q=q,t=t,a=cert['offset'],
             C=[tuple(sum(basis[k][i]*gamma[j][k] for k in range(rho))%5
                      for j in range(t)) for i in range(q)])
    dfs=dfs_matrix(n,arcs)
    assert bfs['c']==dfs['c'] and bfs['q']==dfs['q'] and bfs['t']==dfs['t']
    candidates=[bfs,dfs]
    orders=[width_order(d['C'],t) for d in candidates]
    choice=min(range(2),key=lambda x:(orders[x][1],x))
    dat=candidates[choice];order,w=orders[choice]
    C=dat['C'];a=dat['a'];factors=[]
    def factor(scope,fn):
        scope=tuple(sorted(scope))
        return scope,{z:fn(dict(zip(scope,z))) for z in product(range(5),repeat=len(scope))}
    for i in range(q):
        factors.append(factor((i,),lambda x,i=i:plus(power(x[i]*(a[i]-1)),
                                                     power(x[i]*(a[i]-3)))))
    for j in range(t):
        supp=tuple(i for i in range(q) if C[i][j])
        factors.append(factor(supp,lambda x,supp=supp,j=j:
               plus(O,power(sum(C[i][j]*x[i] for i in supp)))))
    peak=sum(len(tab) for _,tab in factors)
    for i in order:
        bucket=[f for f in factors if i in f[0]]
        factors=[f for f in factors if i not in f[0]]
        scope=tuple(sorted(set().union(*(s for s,_ in bucket))-{i}))
        new={}
        for z in product(range(5),repeat=len(scope)):
            x=dict(zip(scope,z));value=Z
            for digit in range(5):
                x[i]=digit;p=O
                for s,table in bucket:p=mul(p,table[tuple(x[j] for j in s)])
                value=plus(value,p)
            new[z]=value
        factors.append((scope,new))
        peak=max(peak,sum(len(v) for _,v in factors)+sum(len(v) for _,v in bucket))
    numerator=O
    for scope,tab in factors:
        assert not scope
        numerator=mul(numerator,tab[()])
    assert numerator[1:]==(0,0,0) and numerator[0]%(5**q)==0
    result=(numerator[0]//(5**q))*5**dat['c']
    return result,dict(n=n,m=cert['tree_bits']+q,c=dat['c'],q=q,rho=rho,
               t=t,dual_width=w,bfs_width=orders[0][1],
               dfs_width=orders[1][1],chosen=('bfs','dfs')[choice],
               peak_factor_entries=peak)

def triangles(r):
    return 2*r+1,[(u,v) for j in range(r) for u,v in
                   ((2*j,2*j+1),(2*j+1,2*j+2),(2*j+2,2*j))]
def fibchain(k):
    return k+2,([(i,i+1) for i in range(k+1)]+
                 [(i+2,i) for i in range(k)])

def audit():
    rng=random.Random(84019);checks=0
    for n in range(1,6):
        for z in range(20):
            E=[]
            for i in range(n):
                for j in range(i+1,n):
                    u=rng.random()
                    if u<.34:E.append((i,j))
                    elif u<.68:E.append((j,i))
            got,_=exact_count(n,E)
            assert got==count_bruteforce(n,E);checks+=1
    for k in range(1,7):
        n,E=fibchain(k);got,s=exact_count(n,E)
        f,g=0,1
        for _ in range(k+3):f,g=g,f+g
        assert got==5*f and s['dual_width']<=1;checks+=1
    n,E=fibchain(100);got,s=exact_count(n,E)
    assert got==7502602681034480416385 and s['bfs_width']==99 and s['dfs_width']==1
    checks+=1
    n,E=triangles(101);got,s2=exact_count(n,E)
    assert got==5*3**101 and s2['dual_width']==0;checks+=1
    return dict(checks=checks,failures=0,chain100=s,triangles101=s2)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--test',action='store_true')
    p.add_argument('--n',type=int);p.add_argument('--arcs')
    a=p.parse_args()
    if a.test:print(json.dumps(audit(),indent=2))
    else:
        if a.n is None or a.arcs is None:p.error('need --n and --arcs')
        print(json.dumps(exact_count(a.n,json.loads(a.arcs)),indent=2))
