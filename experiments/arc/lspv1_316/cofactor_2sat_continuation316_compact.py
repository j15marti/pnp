#!/usr/bin/env python3
"""LSPV-1 COFACTOR-2SAT-CONTINUATION316. Exact 2CNF-base semantic guard.
No universal SAT hardness or runtime claim. Python 3, standard library.
The full independent truth-mask verifier and raw results are in the run archive.
"""
from collections import Counter
from itertools import product

F9 = ((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
      (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6 = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def valid(F):
    if not F: return False
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 or
           not (all(v>0 for v in c) or all(v<0 for v in c)) for c in F):
        return False
    if len({tuple(sorted(c)) for c in F})!=len(F): return False
    cnt=Counter((abs(v),v>0) for c in F for v in c)
    n=max(abs(v) for c in F for v in c)
    return all(cnt[i,True]==cnt[i,False]==2 for i in range(1,n+1))

def components(F,p,x):
    assert valid(F) and x not in p
    H=[];A=[];B=[]
    for j,c in enumerate(F):
        if any(abs(v)!=x and abs(v) in p and p[abs(v)]==int(v>0) for v in c):
            continue
        if any(abs(v)==x for v in c):
            r=tuple(v for v in c if abs(v)!=x and abs(v) not in p)
            (A if x in c else B).append((j,r))
        else:
            H.append((j,tuple(v for v in c if abs(v) not in p)))
    return H,A,B

def twosat(rows):
    if any(len(c)>2 for _,c in rows): raise ValueError("not 2SAT")
    if any(not c for _,c in rows):return False
    v=sorted({abs(l) for _,c in rows for l in c})
    ix={x:i for i,x in enumerate(v)};n=len(v)
    g=[[] for _ in range(2*n)];h=[[] for _ in range(2*n)]
    def loc(l):return 2*ix[abs(l)]+int(l<0)
    def add(a,b):
        g[a].append(b);h[b].append(a)
    for tag,c in rows:
        if len(c)==1:
            a=loc(c[0]);add(a^1,a)
        elif len(c)==2:
            a=loc(c[0]);b=loc(c[1]);add(a^1,b);add(b^1,a)
    seen=set();order=[]
    def dfs(i):
        seen.add(i)
        for j in g[i]:
            if j not in seen:dfs(j)
        order.append(i)
    for i in range(2*n):
        if i not in seen:dfs(i)
    comp=[-1]*(2*n);label=0
    def back(i):
        comp[i]=label
        for j in h[i]:
            if comp[j]==-1:back(j)
    for i in reversed(order):
        if comp[i]==-1:
            back(i);label+=1
    return all(comp[2*i]!=comp[2*i+1] for i in range(n))

def guard(F,p,x):
    H,A,B=components(F,p,x)
    if any(len(c)>2 for _,c in H):
        return "UNRESOLVED",0
    calls=0
    for lhs,rhs in ((A,B),(B,A)):
        for j,rem in rhs:
            query=H+lhs+[(("assume",j,i),(-l,)) for i,l in enumerate(rem)]
            calls+=1
            if twosat(query):return "DEPENDENT",calls
    return "INDEPENDENT",calls

def up_refutes(rows):
    assigned={}
    while True:
        changed=False
        for _,c in rows:
            if any(abs(l) in assigned and assigned[abs(l)]==int(l>0) for l in c):
                continue
            rest=[l for l in c if abs(l) not in assigned]
            if not rest:return True
            if len(rest)==1:
                l=rest[0];i=abs(l);b=int(l>0)
                if i in assigned and assigned[i]!=b:return True
                if i not in assigned:assigned[i]=b;changed=True
        if not changed:return False

def old_guard(F,p,x):
    H,A,B=components(F,p,x)
    return all(up_refutes(H+[(("assume",j,i),(-l,)) for i,l in enumerate(c)])
               for j,c in A+B)

def truth(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def pointwise(F,p,x):
    n=max(abs(l) for c in F for l in c)
    free=[i for i in range(1,n+1) if i not in p and i!=x]
    m=[0,0]
    for vals in product((0,1),repeat=len(free)):
        a=dict(p);a.update(zip(free,vals))
        for b in (0,1):
            a[x]=b;m[b]+=truth(F,a)
        a[x]=0;t0=truth(F,a)
        a[x]=1;t1=truth(F,a)
        if t0!=t1:return False,None
    return True,m

def census(F):
    n=max(abs(l) for c in F for l in c);s=Counter()
    for x in range(1,n+1):
        rest=[i for i in range(1,n+1) if i!=x]
        for vals in product((-1,0,1),repeat=n-1):
            p={i:b for i,b in zip(rest,vals) if b!=-1}
            got,calls=guard(F,p,x)
            if got=="UNRESOLVED":s["unresolved"]+=1;continue
            s["eligible"]+=1
            truth_value,models=pointwise(F,p,x)
            assert truth_value==(got=="INDEPENDENT"),(p,x)
            s[got]+=1
            if got=="INDEPENDENT":
                if old_guard(F,p,x):s["UP"]+=1
                else:
                    s["strict_new"]+=1
                    if models[0]>0:s["strict_new_nonvacuous"]+=1
    return dict(s)

if __name__=="__main__":
    for name,F in (("F9",F9),("Y6",Y6)):
        assert valid(F)
        print(name,census(F))
    p={4:1,5:0,6:1,7:0,8:0}
    print("NONVACUOUS_F9",guard(F9,p,1),pointwise(F9,p,1),old_guard(F9,p,1))
