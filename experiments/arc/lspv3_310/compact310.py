#!/usr/bin/env python3
"""LSPV-3 GATE310 compact polarity-anchor recognizer and exact transfer."""
import collections,itertools,json,random,sys
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
def family(t):
    F=[]
    for i in range(t):
        at=lambda k:9*i+k
        F.append((at(1),at(6),9*((i+1)%t)+5))
        F.extend(tuple(at(x) for x in c) for c in P[1:])
        F.extend(tuple(-at(x) for x in c) for c in Q)
    return 9*t,F
def valid(n,F):
    if type(n)!=int or n<=0 or len(F)*3!=4*n:return False
    occ=collections.Counter(); seen=set()
    for c in F:
        if len(c)!=3 or len(set(abs(v) for v in c))!=3:return False
        if not all(type(v)==int and 1<=abs(v)<=n for v in c):return False
        if not(all(v>0 for v in c) or all(v<0 for v in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for v in c:occ[(abs(v),v>0)]+=1
    return all(occ[(v,s)]==2 for v in range(1,n+1) for s in (False,True))
def orientation(n,F):
    if n<18 or n%9:return None
    parent=list(range(n+1))
    def root(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    neg=[set(abs(v) for v in c) for c in F if c[0]<0]
    for c in neg:
        a,b,d=tuple(c);parent[root(b)]=root(a);parent[root(d)]=root(a)
    comps=collections.defaultdict(set)
    for v in range(1,n+1):comps[root(v)].add(v)
    groups=list(comps.values());t=n//9
    if len(groups)!=t or any(len(g)!=9 for g in groups):return None
    owner={x:i for i,g in enumerate(groups) for x in g}
    ins=[[] for _ in groups];outs=[[] for _ in groups];positive=[[] for _ in groups];negative=[[] for _ in groups]
    for C in neg:negative[owner[next(iter(C))]].append(C)
    for C0 in F:
        if C0[0]<0:continue
        C=set(C0);d=collections.defaultdict(set)
        for x in C:d[owner[x]].add(x)
        if len(d)==1:positive[next(iter(d))].append(C)
        elif sorted(map(len,d.values()))==[1,2]:
            i=next(i for i,v in d.items() if len(v)==2)
            j=next(i for i,v in d.items() if len(v)==1)
            outs[i].append((j,d[i]));ins[j].append((i,next(iter(d[j]))))
        else:return None
    if any(len(positive[i])!=5 or len(negative[i])!=6 or len(outs[i])!=1 or len(ins[i])!=1 for i in range(t)):return None
    suc={i:outs[i][0][0] for i in range(t)}
    order=[];i=0
    for _ in range(t):
        if i in order:return None
        order.append(i);i=suc[i]
    if i!=0:return None
    recovered={}
    for i in range(t):
        pair=outs[i][0][1];x5=ins[i][0][1]
        vv=[z for z in pair if any(z in C and x5 in C for C in positive[i])]
        if len(vv)!=1:return None
        x1=vv[0];x6=next(iter(pair-{x1}))
        cls=[C for C in positive[i] if {x1,x5}<=C]
        if len(cls)!=1:return None
        x3=next(iter(cls[0]-{x1,x5}))
        cls=[C for C in negative[i] if {x1,x6}<=C]
        if len(cls)!=1:return None
        x7=next(iter(cls[0]-{x1,x6}))
        v29=[C-{x1} for C in negative[i] if x1 in C and x6 not in C]
        v48=[C-{x6} for C in negative[i] if x6 in C and x1 not in C]
        p469=[C-{x6} for C in positive[i] if x6 in C]
        if len(v29)!=1 or len(v48)!=1 or len(p469)!=1:return None
        c9=v29[0]&p469[0];c4=v48[0]&p469[0]
        if len(c9)!=1 or len(c4)!=1:return None
        x9=next(iter(c9));x4=next(iter(c4))
        x2=next(iter(v29[0]-{x9}));x8=next(iter(v48[0]-{x4}))
        d={1:x1,2:x2,3:x3,4:x4,5:x5,6:x6,7:x7,8:x8,9:x9}
        if set(d.values())!=groups[i]:return None
        if set(map(frozenset,positive[i]))!={frozenset(d[x] for x in C) for C in P[1:]}:return None
        if set(map(frozenset,negative[i]))!={frozenset(d[x] for x in C) for C in Q}:return None
        recovered[i]=d
    for i in range(t):
        cross=[c for c in F if c[0]>0 and set(c)&groups[i] and set(c)&groups[suc[i]] and len(set(c)&groups[i])==2]
        if len(cross)!=1 or set(cross[0])!={recovered[i][1],recovered[i][6],recovered[suc[i]][5]}:return None
    return [recovered[i] for i in order]
def multiply(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mat(pins):
    M=[[0,0],[0,0]]
    for a,b in itertools.product((0,1),repeat=2):
        for bits in range(256):
            v={5:a};v.update({x:(bits>>k)&1 for k,x in enumerate((1,2,3,4,6,7,8,9))})
            if any(v[x]!=z for x,z in pins.items()):continue
            if not all(any(v[x] for x in C) for C in P[1:]):continue
            if not all(any(not v[x] for x in C) for C in Q):continue
            if not(v[1] or v[6] or b):continue
            M[a][b]+=1
    return M
def decide(n,F,pin):
    if not valid(n,F):return 'MALFORMED',None,None
    dual=False;L=orientation(n,F)
    if L is None:
        L=orientation(n,[tuple(-x for x in C) for C in F]);dual=L is not None
    if L is None:return 'UNRESOLVED',None,None
    M=[]
    for d in L:
        P0={j:(1-pin[x] if dual else pin[x]) for j,x in d.items() if x in pin}
        M.append(mat(P0))
    out=[[1,0],[0,1]]
    for x in M:out=multiply(out,x)
    models=out[0][0]+out[1][1]
    return ('SAT' if models else 'UNSAT'),models,{'blocks':len(L),'complemented':dual,'matrices':M}
if __name__=='__main__':
    t=int(sys.argv[1]) if len(sys.argv)>1 else 3
    n,F=family(t);a={};b={}
    for i in range(t):
        for x,v in ((1,1),(2,0),(3,1),(4,0),(8,0)):
            a[9*i+x]=v;b[9*i+x]=v
    b[2]=1;b[3]=0
    rng=random.Random(310+t);ids=list(range(1,n+1));rng.shuffle(ids)
    mapv=dict(zip(range(1,n+1),ids))
    F=[tuple((1 if x>0 else -1)*mapv[abs(x)] for x in c) for c in F];rng.shuffle(F)
    print(json.dumps({'n':n,'SAT':decide(n,F,{mapv[k]:v for k,v in a.items()})[:2],
                      'UNSAT':decide(n,F,{mapv[k]:v for k,v in b.items()})[:2]},sort_keys=True))
