#!/usr/bin/env python3
"""Independent finite replay of Q-critical Mycielski^3(C_t); stdlib only."""
import json
from collections import deque

WIN = ((1,3),(2,4),(0,3),(1,4),(0,2))

def sortedge(a,b): return (min(a,b),max(a,b))
def order(l,t): return t if l==0 else 2*order(l-1,t)+1

def graph(l,t):
    if l==0: return sortedge(0,t-1),*tuple((i,i+1) for i in range(t-1))
    n=order(l-1,t)
    old=graph(l-1,t)
    return tuple(old)+tuple(e for a,b in old for e in ((a,n+b),(b,n+a)))+tuple((n+i,2*n) for i in range(n))

def near(l,t,v):
    if l==0: return (v+1)%t
    n=order(l-1,t)
    return near(l-1,t,v) if v<n else (2*n if v<2*n else n)

def paint(l,t,e,v):
    a,b=e
    if l==0:
        s=a if (a+1)%t==b else b
        assert (s+1)%t in (a,b)
        return ((v-s-1)%t)%2
    n=order(l-1,t)
    k=l+1
    if b<n:
        if v<n:return paint(l-1,t,e,v)
        r=paint(l-1,t,e,a)
        if v==2*n:return r
        c=paint(l-1,t,e,v-n)
        return k if c==r else c
    if b==2*n:
        i=a-n
        old=sortedge(i,near(l-1,t,i))
        if v in (i,n+i,2*n):return k
        return paint(l-1,t,old,v if v<n else v-n)
    i=b-n
    old=sortedge(i,a)
    if v in (i,2*n):return k
    return paint(l-1,t,old,v if v<n else v-n)

def head(ca,cb):
    return ca if cb in WIN[ca] else cb

def q(h,u,v):
    return (u in WIN[h]) != (v in WIN[h])

def run(t):
    assert t>=5 and t%2
    es=graph(3,t)
    v=order(3,t);m=len(es)
    assert v==8*t+7 and m==46*t+6 and len(set(es))==m
    trials=list(range(m)) if t<=15 else sorted({0,m//2,m-1,*[j*m//20 for j in range(20)]})
    checked=0
    for j in trials:
        f=[paint(3,t,es[j],i) for i in range(v)]
        assert set(f)==set(range(5))
        only=[]
        for k,(a,b) in enumerate(es):
            h=head(f[a],f[b])
            good=q(h,f[a],f[b])
            assert good==(j!=k),(t,j,k)
            if f[a]==f[b]:only.append(k)
            checked+=1
        assert only==[j]
    return {'t':t,'Q_variables':v+m,'Q_clauses':m,
            'verified_deletions':len(trials),'direct_Q_checks':checked}

if __name__=='__main__':
    results=[run(t) for t in (5,7,9,11,15,21,31)]
    print(json.dumps({'status':'COMPUTATIONAL','results':results,
                      'total_deletions':sum(x['verified_deletions'] for x in results),
                      'total_checks':sum(x['direct_Q_checks'] for x in results)},indent=2))
