#!/usr/bin/env python3
"""Exact T5 counting: mod-5 cycle-space DP and Z5-orbit bucket elimination."""
from collections import deque, defaultdict
from itertools import product

def beat(a,b): return (b-a)%5 in (1,3)
def parse(n,arcs):
    if type(n)!=int or n<0: raise ValueError('bad vertex count')
    e=set()
    for u,v in arcs:
        if type(u)!=int or type(v)!=int or not (0<=u<n and 0<=v<n):
            raise ValueError('bad vertex ID')
        e.add((u,v))
    return sorted(e),any(u==v or (v,u) in e for u,v in e)

def cycle_dp(n,arcs):
    es,invalid=parse(n,arcs)
    if invalid:return 0,{'contradiction':True}
    e=set(es); adj=[set() for _ in range(n)]
    for u,v in es:adj[u].add(v);adj[v].add(u)
    parent=[-1]*n;depth=[0]*n;edgeid=[-1]*n
    chosen=set();tree=[];visited=set();components=0
    for root in range(n):
        if root in visited:continue
        components+=1;visited.add(root);q=deque([root])
        while q:
            u=q.popleft()
            for v in sorted(adj[u]):
                if v in visited:continue
                visited.add(v);q.append(v);parent[v]=u;depth[v]=depth[u]+1
                base,step=(1,2) if (u,v) in e else (4,3)
                edgeid[v]=len(tree);tree.append((base,step))
                chosen.add(frozenset((u,v)))
    chords=[(u,v) for u,v in es if frozenset((u,v)) not in chosen]
    t=len(tree);r=len(chords);rows=[];offset=[]
    for start,end in chords:
        u,v=start,end;terms=[]
        while depth[u]>depth[v]:terms.append((edgeid[u],-1));u=parent[u]
        while depth[v]>depth[u]:terms.append((edgeid[v],1));v=parent[v]
        while u!=v:
            terms.extend(((edgeid[u],-1),(edgeid[v],1)))
            u=parent[u];v=parent[v]
        a=0;row=[0]*t
        for j,sign in terms:
            base,step=tree[j];a+=sign*base;row[j]=(row[j]+sign*step)%5
        offset.append(a%5);rows.append(row)
    basis=[];pivots=[];coords=[]
    for j in range(t):
        rem=[rows[i][j] for i in range(r)];c=[]
        for b,p in zip(basis,pivots):
            f=rem[p];c.append(f);rem=[(x-f*y)%5 for x,y in zip(rem,b)]
        if any(rem):
            p=next(i for i,x in enumerate(rem) if x);alpha=rem[p]
            inverse=pow(alpha,-1,5)
            basis.append(tuple(x*inverse%5 for x in rem));pivots.append(p)
            c.append(alpha)
        coords.append(c)
    rho=len(basis);coords=[tuple(c+[0]*(rho-len(c))) for c in coords]
    dp={(0,)*rho:1};free=0
    for delta in coords:
        if not any(delta):free+=1;continue
        nxt=defaultdict(int)
        for z,count in dp.items():
            nxt[z]+=count
            nxt[tuple((x+y)%5 for x,y in zip(z,delta))]+=count
        dp=nxt
    good=0
    for z,count in dp.items():
        if all((offset[i]+sum(z[j]*basis[j][i] for j in range(rho)))%5 in (1,3)
               for i in range(r)):
            good+=count
    return 5**components*2**free*good,{'components':components,'tree_bits':t,
          'chords':r,'mod5_rank':rho,'max_states':len(dp)}

def factor(scope,calc):
    scope=tuple(sorted(scope));table={}
    for tail in product(range(5),repeat=max(0,len(scope)-1)):
        vals=(0,)+tail if scope else ()
        table[tail]=calc(dict(zip(scope,vals)))
    return scope,table

def value(f,a):
    s,table=f
    if not s:return table[()]
    x=a[s[0]]
    return table[tuple((a[v]-x)%5 for v in s[1:])]

def orbit_elimination(n,arcs):
    es,invalid=parse(n,arcs)
    if invalid:return 0,{'contradiction':True}
    incoming=[[] for _ in range(n)];out=[[] for _ in range(n)]
    for u,v in es:incoming[v].append(u);out[u].append(v)
    sinks={v for v in range(n) if not out[v] and len(incoming[v])<=3}
    hubs=set(range(n))-sinks;fs=[];base=1
    for v in sorted(sinks):
        scope=tuple(sorted(incoming[v]))
        if not scope:base*=5
        else:fs.append(factor(scope,lambda a,sc=scope:
                   sum(all(beat(a[u],z) for u in sc) for z in range(5))))
    for u,v in es:
        if v not in sinks:
            fs.append(factor((u,v),lambda a,u=u,v=v:int(beat(a[u],a[v]))))
    adj={v:set() for v in hubs}
    for sc,_ in fs:
        for v in sc:adj[v].update(set(sc)-{v})
    order=[];width=0
    while adj:
        def key(v):
            ns=sorted(adj[v]);fill=sum(y not in adj[x]
                         for i,x in enumerate(ns) for y in ns[i+1:])
            return fill,len(ns),v
        v=min(adj,key=key);ns=adj[v];width=max(width,len(ns))
        for u in ns:adj[u].update(ns-{u});adj[u].discard(v)
        del adj[v];order.append(v)
    peak=sum(len(tab) for _,tab in fs)
    for v in order:
        bucket=[f for f in fs if v in f[0]]
        fs=[f for f in fs if v not in f[0]]
        rem=tuple(sorted(set().union(*(set(sc) for sc,_ in bucket))-{v}))
        table={}
        for tail in product(range(5),repeat=max(0,len(rem)-1)):
            a=dict(zip(rem,((0,)+tail if rem else ())))
            z=0
            for color in range(5):
                a[v]=color;p=1
                for f in bucket:
                    p*=value(f,a)
                    if not p:break
                z+=p
            table[tail]=z
        fs.append((rem,table))
        peak=max(peak,sum(len(tab) for _,tab in fs))
    assert all(not sc for sc,_ in fs)
    for _,tab in fs:base*=tab[()]
    return base,{'induced_width':width,'peak_orbit_entries':peak}

def cycle(n):return n,[(i,(i+1)%n) for i in range(n)]
def wheel(r):return 2*r+1,[(u,r+1+i) for i in range(r)
                                 for u in (0,i+1,1+(i+1)%r)]
def brute(n,arcs):
    return sum(all(beat(a[u],a[v]) for u,v in arcs)
           for a in product(range(5),repeat=n))

def test():
    checks=0
    for n,es in [cycle(3),cycle(4),wheel(4),wheel(5),
                 (7,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]),
                 (6,[(u,v) for u in range(6) for v in range(u+1,6)])]:
        target=brute(n,es)
        assert cycle_dp(n,es)[0]==target;checks+=1
        assert orbit_elimination(n,es)[0]==target;checks+=1
    for k in (6,10,80):
        assert orbit_elimination(*wheel(k))[0]==5*(3**k+1);checks+=1
    assert cycle_dp(*cycle(500))[1]['mod5_rank']==1;checks+=1
    print(checks,'compact checks passed')
if __name__=='__main__':test()
