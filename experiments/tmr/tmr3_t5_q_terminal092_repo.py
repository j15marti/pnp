#!/usr/bin/env python3
"""TMR-3/092 independent q-terminal extension, using the same T5 relation."""
from itertools import product
from tmr3_t5_three_terminal092_repo import relation

def q_family(q,k,p):
    if q<1 or k<2 or p<=q:raise ValueError
    E=set();ptr=q
    for _ in range(k):
        L=range(ptr,ptr+p-q);ptr+=p-q
        R=range(ptr,ptr+p);ptr+=p
        E.update((u,v) for u in list(range(q))+list(L) for v in R)
    return ptr,E

def q_formula(q,k,p):
    a=2**p+2**(p-q+1)-2
    b=2**(p-q)
    return 5*(a**k+(2**q-2)*b**k)

def vector(q,p):
    ret={}
    for term in product(range(5),repeat=q-1):
        z=0
        for left in product(range(5),repeat=p-q):
            support=sum(all(relation(x,y) for x in (0,)+term+left) for y in range(5))
            z+=support**p
        ret[term]=z
    return ret

def recognize(n,E):
    if not E or len(E)!=len(set(E)) or any(u==v or u<0 or v<0 or u>=n or v>=n for u,v in E):return None
    din=[0]*n;dout=[0]*n;adj=[set() for _ in range(n)]
    for u,v in E:
        din[v]+=1;dout[u]+=1;adj[u].add(v);adj[v].add(u)
    high=max(dout)
    S={v for v in range(n) if din[v]==0 and dout[v]==high}
    q=len(S);seen=set(S)
    if not q:return None
    expected=set();p0=None;blocks=[]
    for start in range(n):
        if start in seen:continue
        component={start};queue=[start];seen.add(start)
        for u in queue:
            for w in adj[u]-S-seen:
                component.add(w);queue.append(w);seen.add(w)
        blocks.append(component)
    if len(blocks)<2:return None
    for C in blocks:
        L={v for v in C if din[v]==0}
        R={v for v in C if dout[v]==0}
        p=len(R)
        if p<=q or L|R!=C or L&R or len(L)!=p-q or (p0 is not None and p!=p0):return None
        p0=p
        expected.update((u,v) for u in L|S for v in R)
    return (q,len(blocks),p0) if expected==set(E) else None

def self_test():
    checks=0
    for q in range(1,6):
        for p in range(q+1,min(q+4,9)):
            entries=vector(q,p)
            a=2**p+2**(p-q+1)-2
            b=2**(p-q)
            assert entries[(0,)*(q-1)]==a
            assert sum(v==b for v in entries.values())==2**q-2
            assert set(entries.values())<={0,a,b}
            assert q_formula(q,2,p)==5*sum(v*v for v in entries.values())
            checks+=4
    for q,k,p in ((2,2,4),(3,2,4),(4,2,5),(4,3,5),(10,15,20),(50,50,101)):
        n,E=q_family(q,k,p)
        assert recognize(n,E)==(q,k,p)
        assert n==q+k*(2*p-q) and len(E)==k*p*p
        checks+=2
    return checks

if __name__=="__main__":
    print({'checks':self_test(),'failures':0,'status':'constructive exact only; P vs NP open'})
