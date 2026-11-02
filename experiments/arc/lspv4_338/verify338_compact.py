#!/usr/bin/env python3
"""LSPV-4 338: independent source-only exact port conservation check.
Standard library only. This file deliberately has no repository solver imports.
"""
from itertools import product
from collections import Counter
import json

F9P = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9N = [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
Z6 = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]

def source(p,n):
    return list(map(tuple,p)) + [tuple(-x for x in c) for c in n]

def canonical(F,n):
    if type(n)!=int or n<3 or n%3 or type(F)!=list or len(F)!=4*n//3:
        return False
    occ=Counter();seen=set()
    for C in F:
        if not isinstance(C,(tuple,list)) or len(C)!=3: return False
        if any(type(x)!=int or x==0 or abs(x)>n for x in C): return False
        if len({abs(x) for x in C})!=3: return False
        if not (all(x>0 for x in C) or all(x<0 for x in C)): return False
        key=tuple(sorted(C))
        if key in seen: return False
        seen.add(key); occ.update(C)
    return all(occ[x]==occ[-x]==2 for x in range(1,n+1))

def literal(x,a):
    return bool(a[abs(x)-1]) == (x>0)

def truth(F,a):
    return all(any(literal(x,a) for x in C) for C in F)

def audit(F,n):
    assert canonical(F,n)
    m=len(F);ports=[0]*(3*m);hist=Counter();s=0
    for a in product((0,1),repeat=n):
        if not truth(F,a):continue
        s+=1
        levels=[sum(literal(x,a) for x in C) for C in F]
        N=(levels.count(1),levels.count(2),levels.count(3))
        hist[N]+=1
        assert sum(levels)==2*n and N[1]+2*N[2]==m//2
        for j,C in enumerate(F):
            for k,x in enumerate(C):
                ports[3*j+k]+=int(literal(x,a) and any(
                    literal(y,a) for h,y in enumerate(C) if h!=k))
    assert sum(ports)==sum((m-N[2])*qty for N,qty in hist.items())
    if s:assert sum(v>0 for v in ports)>=n and sum(ports)>=n*s
    return dict(n=n,m=m,models=s,positive_ports=sum(v>0 for v in ports),
                min_W11=min(ports),max_W11=max(ports),sum_W11=sum(ports),
                histogram={str(k):v for k,v in sorted(hist.items())},
                W11=ports)

def obdd(F,n):
    # Exact all-order ROBDD node counts from 2^n cofactor-subset states.
    allrows={a:truth(F,a) for a in product((0,1),repeat=n)}
    co={};w={}
    for S in range(1<<n):
        K=[i for i in range(n) if S>>i&1]
        R=[i for i in range(n) if not (S>>i&1)]
        values=set()
        for kv in product((0,1),repeat=len(K)):
            a=[0]*n
            for i,b in zip(K,kv):a[i]=b
            f=0
            for y,rv in enumerate(product((0,1),repeat=len(R))):
                for i,b in zip(R,rv):a[i]=b
                f |= int(allrows[tuple(a)])<<y
            values.add(f)
        co[S]=values
        for p,v in enumerate(R):
            stride=1<<(len(R)-p-1); count=0
            for f in values:
                if any(((f>>j)&1)!=((f>>(j|stride))&1)
                       for j in range(1<<len(R)) if not(j&stride)):
                    count+=1
            w[S,v]=count
    full=(1<<n)-1
    mn={full:(0,1)};mx={full:(0,1)}
    for S in range(full-1,-1,-1):
        options=[(v,w[S,v]+mn[S|1<<v][0],mn[S|1<<v][1],
                     w[S,v]+mx[S|1<<v][0],mx[S|1<<v][1])
                 for v in range(n) if not S>>v&1]
        best=min(x[1] for x in options); worst=max(x[3] for x in options)
        mn[S]=(best,sum(x[2] for x in options if x[1]==best))
        mx[S]=(worst,sum(x[4] for x in options if x[3]==worst))
    natural=0;S=0
    for i in range(n):
        natural+=w[S,i];S|=1<<i
    return dict(min=mn[0][0],min_orders=mn[0][1],
                natural=natural,max=mx[0][0],max_orders=mx[0][1],
                offline_cofactor_bits=(1<<n)**2)

def main():
    f9=source(F9P,F9N);z6=source(Z6,Z6)
    assert canonical(f9,9) and canonical(z6,6)
    A=audit(f9,9);B=audit(z6,6)
    assert (A['models'],A['sum_W11'],A['min_W11'],A['positive_ports'])==(70,781,13,36)
    assert (B['models'],B['sum_W11'],B['min_W11'],B['positive_ports'])==(18,144,6,24)
    d=obdd(f9,9)
    assert (d['min'],d['natural'],d['max'],d['min_orders'],d['max_orders'])==(52,66,80,72,48)
    pivot={}
    for x1 in (0,1):
        pins={1:x1,2:0,4:0,6:0}
        s=sum(truth(f9,a) and all(a[i-1]==v for i,v in pins.items())
              for a in product((0,1),repeat=9))
        pivot[x1]=s
    assert pivot=={0:0,1:3}
    malformed=[f9+[f9[0]],f9[:1]+[(1,1,6)]+f9[2:],
               f9[:1]+[(1,-5,6)]+f9[2:],
               f9[:1]+[(0,5,6)]+f9[2:],
               f9[:1]+[(10,5,6)]+f9[2:],
               f9[:1]+[(1.5,5,6)]+f9[2:]]
    assert all(not canonical(c,9) for c in malformed)
    result={'F9':A,'Z6':B,'F9_OBDD':d,'F9_pin_x2_x4_x6_0_x1_0_1':pivot,
            'malformed_rejected':len(malformed),
            'gate_count_private_F9':35,'gate_depth_private_F9':6}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
