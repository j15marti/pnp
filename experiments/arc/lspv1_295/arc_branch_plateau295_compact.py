#!/usr/bin/env python3
"""ARC-BRANCH-PLATEAU295 compact stdlib producer, no downloads or SAT oracle.
Full original U198/V198 fixtures and 808956-byte raw diagnostic are in the
companion reproducibility archive, not asserted to be embedded here.
"""
import itertools,collections,json,math

Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z=((1,2,4),(1,3,5),(2,3,6),(-1,-2,-7),(-1,-3,-8),(-2,-3,-9),
   (4,7,8),(5,7,9),(6,8,9),(-4,-5,-7),(-4,-6,-8),(-5,-6,-9))
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
   (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
M=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
   (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F=P+tuple(tuple(-x for x in c) for c in M)

def legal(F,n):
    if len(F)*3!=n*4 or n%3:return False
    h=collections.Counter()
    keys=set()
    for c in F:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        key=tuple(sorted(c))
        if key in keys:return False
        keys.add(key);h.update(c)
    return all(h[i]==2 and h[-i]==2 for i in range(1,n+1))

def metrics(F,p):
    f=p.count(None)
    u=r3=r2=h=0
    for c in F:
        fixedtrue=any(p[abs(l)-1]==int(l>0) for l in c if p[abs(l)-1] is not None)
        free=sum(p[abs(l)-1] is None for l in c)
        if fixedtrue:h+=free
        else:
            u+=1;r3+=free==3;r2+=free==2
    return dict(f=f,u=u,r3=r3,r2=r2,h=h,e=2*f-u)

def slots(F,p,x):
    pos=neg=0
    for c in F:
        if x not in c and -x not in c:continue
        if any(p[abs(l)-1]==int(l>0) for l in c if p[abs(l)-1] is not None):
            continue
        pos+=(x in c);neg+=(-x in c)
    return pos,neg

def independent(F,n):
    adj=[set() for _ in range(n)]
    for c in F:
        v=[abs(x)-1 for x in c]
        for x,y in itertools.combinations(v,2):
            adj[x].add(y);adj[y].add(x)
    assert max(map(len,adj))<=8
    available=set(range(n));ans=[]
    while available:
        v=min(available);ans.append(v);available-={v}|adj[v]
    assert len(ans)>=math.ceil(n/9)
    return ans

def bits(F,p):
    b=[]
    for x in p:b.extend((0,0) if x is None else ((0,1) if x==0 else (1,0)))
    for c in F:
        t=sum(p[abs(l)-1] is not None and p[abs(l)-1]==int(l>0) for l in c)
        q=sum(p[abs(l)-1] is None for l in c)
        b.extend((t&1,(t>>1)&1,q&1,(q>>1)&1,int(t>0)))
    return b

def source_extremes(F):
    return [[dict(variable=abs(l),literal=l,S=int(l>0),U=int(l<0),
                  invert_S_is_U=True,invert_U_is_S=True) for l in c] for c in F]

def modes(F):
    counts=collections.Counter()
    for j,c in enumerate(F):
        a={abs(l):int(l>0) for l in c}
        for d in F[j+1:]:
            b={abs(l):int(l>0) for l in d}
            ids=a.keys()&b.keys()
            same=any(a[x]==b[x] for x in ids)
            opp=any(a[x]!=b[x] for x in ids)
            key=''.join(str(int(z)) for z in (not opp,not same,not same,not opp))
            counts[key]+=1
    return dict(counts)

def completions(F,p):
    free=[i for i,v in enumerate(p) if v is None]
    n=0
    for a in itertools.product((0,1),repeat=len(free)):
        q=p[:]
        for i,v in zip(free,a):q[i]=v
        if all(any(q[abs(l)-1]==int(l>0) for l in c) for c in F):n+=1
    return n

def check(F,n,exhaustive):
    assert legal(F,n)
    I=independent(F,n)
    sibling=plateaus=0
    C=list(itertools.product((None,0,1),repeat=n)) if exhaustive else [
       (None,)*n,(None,)*6+(0,0,0,0,1,1,1,1,0),
       (None,)*6+(1,0,0,0,1,1,1,1,0)]
    for q in C:
        p=list(q);e=metrics(F,p)['e']
        for x in range(n):
            if p[x] is not None:continue
            a,b=slots(F,p,x+1)
            p0=p[:];p0[x]=0
            p1=p[:];p1[x]=1
            d0=metrics(F,p0)['e'];d1=metrics(F,p1)['e']
            assert d0==e-2+b and d1==e-2+a
            assert d0+d1==2*e-(4-a-b)
            assert d0<=e and d1<=e
            sibling+=1
            plateaus+=(d0==e and d1==e)
    traces=[]
    for policy in ("zero","one","alternate"):
        p=[None]*n;prev=bits(F,p);acc=0
        for k,x in enumerate(I,1):
            p[x]=0 if policy=="zero" else 1 if policy=="one" else k%2
            met=metrics(F,p)
            assert met==dict(f=n-k,u=len(F)-2*k,r3=len(F)-4*k,
                             r2=2*k,h=4*k,e=2*n-len(F))
            curr=bits(F,p);delta=sum(x!=y for x,y in zip(prev,curr))
            assert delta==9
            acc+=delta;prev=curr
        traces.append(dict(policy=policy,steps=len(I),logical_xor_sum=acc))
    assert not legal(F[:-1],n)
    assert not legal(((1,-2,3),)+F[1:],n)
    assert not legal((F[0],)+F,n)
    assert all(len(C)==3 for C in F)
    return dict(n=n,m=len(F),greedy_independent_ids=[x+1 for x in I],
                guaranteed_floor=math.ceil(n/9),
                checked_sibling_choices=sibling,
                same_e_both_siblings=plateaus,
                trails=traces,original_source_pair_modes=modes(F),
                source_occurrences=sum(len(z) for z in source_extremes(F)))

if __name__=="__main__":
    result={name:check(A,n,n<=9) for name,A,n in
            (("Y6",Y,6),("Z9",Z,9),("F15",F,15))}
    u=[None]*6+[0,0,0,0,1,1,1,1,0]
    s=[None]*6+[1,0,0,0,1,1,1,1,0]
    assert completions(F,u)==0 and completions(F,s)==2
    result["F15_matched_cubes"]={"UNSAT_models":0,"SAT_models":2}
    result["status"]="PASS"
    result["claim"]="syntactic plateau only; ARC/FLMV and P versus NP OPEN"
    print(json.dumps(result,sort_keys=True,indent=2))
