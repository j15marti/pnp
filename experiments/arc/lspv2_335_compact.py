#!/usr/bin/env python3
"""LSPV-2 335 standalone stdlib canonical paired-NAE prism recognizer and paid DP.
This is a RESTRICTED polynomial upper bound, never a general SAT lower bound.
"""
from collections import Counter,defaultdict
import json,random
def prism(k):
    P=[(base+(i-1)%k+1,base+i+1,2*k+i+1) for base in (0,k) for i in range(k)]
    return P+[tuple(-x for x in c) for c in P]
def accept(F,n):
    if type(n)!=int or n<3 or n%3 or 3*len(F)!=4*n:return False
    q=Counter();s=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3 or any(type(x)!=int or not 1<=abs(x)<=n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        z=tuple(sorted(c))
        if z in s:return False
        s.add(z);q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))
def discover(F,n):
    if not accept(F,n):return 'MALFORMED',None
    P={frozenset(map(abs,c)):j for j,c in enumerate(F) if c[0]>0}
    N={frozenset(map(abs,c)):j for j,c in enumerate(F) if c[0]<0}
    if P.keys()!=N.keys():return 'UNRESOLVED',None
    ids=sorted(P.values());loc={v:i for i,v in enumerate(ids)}
    inc=defaultdict(list)
    for t,j in P.items():
        for v in t:inc[v].append(loc[j])
    E={};G=[{} for _ in ids]
    for v in range(1,n+1):
        a,b=sorted(inc[v])
        if a==b or (a,b) in E:return 'UNRESOLVED',None
        E[a,b]=v;G[a][b]=v;G[b][a]=v
    if any(len(q)!=3 for q in G):return 'UNRESOLVED',None
    k=n//3
    if k<3:return 'UNRESOLVED',None
    def check(mate):
        if len(mate)!=2*k or any(mate.get(mate[v])!=v for v in range(2*k)):return None
        H=[set(G[v])-{mate[v]} for v in range(2*k)];comps=[];left=set(range(2*k))
        while left:
            st=[min(left)];component=set(st);left-=component
            while st:
                v=st.pop()
                for w in H[v]&left:component.add(w);left.remove(w);st.append(w)
            comps.append(component)
        if len(comps)!=2 or any(len(t)!=k for t in comps):return None
        top=min(comps,key=min);u=min(top);v=min(H[u]);cycle=[u,v]
        while len(cycle)<k:
            z=next(w for w in H[cycle[-1]] if w!=cycle[-2])
            if z in cycle:return None
            cycle.append(z)
        if u not in H[cycle[-1]]:return None
        bottom=[mate[v] for v in cycle]
        if set(bottom)!=next(q for q in comps if q!=top):return None
        if any(bottom[(i+1)%k] not in H[bottom[i]] for i in range(k)):return None
        ordered=[v for i in range(k) for v in (G[cycle[i]][cycle[(i+1)%k]],
                   G[bottom[i]][bottom[(i+1)%k]],G[cycle[i]][bottom[i]])]
        return ordered,{v:ends for ends,v in E.items()}
    mate={}
    for (u,v),x in E.items():
        q=sum(b in G[a] for a in G[u] if a!=v for b in G[v] if b!=u)
        if q==2:
            if u in mate or v in mate:mate={};break
            mate[u]=v;mate[v]=u
    ans=check(mate)
    if ans is None and k==4:
        def try_m(left,m):
            if not left:return check(m)
            u=min(left)
            for v in G[u]:
                if v in left:
                    r=try_m(left-{u,v},{**m,u:v,v:u})
                    if r:return r
            return None
        ans=try_m(set(range(2*k)),{})
    return ('PRISM',ans) if ans else ('UNRESOLVED',None)
def exact_decision(F,n,found,pins=None):
    order,E=found;pins=pins or {};remaining=[3]*(2*(n//3));table={():1};peak=1;work=0
    for x in order:
        u,v=E[x];new={}
        for key,count in table.items():
            for bit in ([pins[x]] if x in pins else [0,1]):
                work+=1;d=dict(key);valid=True
                for vertex in (u,v):
                    d[vertex]=d.get(vertex,0)|(1<<bit)
                    if remaining[vertex]==1:
                        if d[vertex]!=3:valid=False;break
                        del d[vertex]
                if valid:
                    z=tuple(sorted(d.items()));new[z]=new.get(z,0)+count
        remaining[u]-=1;remaining[v]-=1;table=new
        assert len(table)<=730
        peak=max(peak,len(table))
    return table.get((),0),peak,work
if __name__=='__main__':
    R=[];rng=random.Random(335)
    for k in (3,4,5,6,8,10,16):
        n=3*k;F=prism(k);status,f=discover(F,n);assert status=='PRISM'
        count,peak,attempt=exact_decision(F,n,f)
        perm=list(range(1,n+1));rng.shuffle(perm)
        sh=[tuple((1 if x>0 else -1)*perm[abs(x)-1] for x in c) for c in F]
        rng.shuffle(sh);status2,g=discover(sh,n);assert status2=='PRISM'
        assert exact_decision(sh,n,g)[0]==count
        R.append({'k':k,'models':str(count),'peak_states':peak,'transitions':attempt})
    print(json.dumps({'status':'RESTRICTED_EXACT; P_VS_NP_OPEN','cases':R},indent=2))
